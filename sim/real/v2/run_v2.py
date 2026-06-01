"""
run_v2.py — drive the v2 model ladder over every domain with TEXT-LABEL output
(no tool-calls), caching every call. Resumable: nothing already cached is re-queried.

Reaches Ollama on the China Mac via an SSH tunnel at http://localhost:11434.
Cache: results/raw/{model}__{domain}.json keyed by item id, with parsed label, raw
text, prompt/eval token counts and latency. Batch per model (Ollama keeps it loaded).
"""
from __future__ import annotations
import json, os, sys, time, urllib.request
import datasets as D

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "results", "raw")
os.makedirs(RAW, exist_ok=True)
OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# The pre-registered ladder (PREREGISTRATION.md §1.4). A model absent at run time is
# skipped + logged; analysis requires >= 8 actually run.
LADDER = [
    ("qwen2.5:0.5b-instruct", "qwen0.5b", 0.5),
    ("llama3.2:1b",           "llama1b",  1.0),
    ("qwen2.5:1.5b-instruct", "qwen1.5b", 1.5),
    ("gemma2:2b",             "gemma2b",  2.0),
    ("qwen2.5:3b-instruct",   "qwen3b",   3.0),
    ("llama3.2:3b",           "llama3b",  3.0),
    ("phi3.5:latest",         "phi3.5",   3.8),
    ("qwen2.5:7b-instruct",   "qwen7b",   7.0),
    ("mistral:7b",            "mistral7b",7.0),   # OK in v2: text output, no tool-calls
    ("llama3.1:8b",           "llama8b",  8.0),
]

# ---------------------------------------------------------------------------
def messages(domain, item, classes, gloss):
    labels = ", ".join(classes)
    if domain == "mcqa":
        sys_p = ("Answer the multiple-choice question. Reply with ONLY the letter of the "
                 "correct option (" + labels + "). No other words.")
    elif domain == "topic":
        sys_p = ("Classify the news text into exactly one topic:\n"
                 + "\n".join(f"- {c}: {gloss[c]}" for c in classes)
                 + "\n\nReply with ONLY the topic label (" + labels + "). No other words.")
    else:  # intent
        sys_p = ("You are an intent classifier. Classify the message into exactly one intent:\n"
                 + "\n".join(f"- {c}: {gloss[c]}" for c in classes)
                 + "\n\nReply with ONLY the intent label (" + labels + "). No other words.")
    return [{"role": "system", "content": sys_p}, {"role": "user", "content": item["text"]}]

def parse(text, classes, domain):
    t = (text or "").strip().lower()
    if domain == "mcqa":
        for c in classes:                      # find a standalone A/B/C/D
            if t == c.lower() or t.startswith(c.lower() + ".") or t.startswith(c.lower() + ")") \
               or t.startswith(c.lower() + " ") or t == c.lower() + ".":
                return c
        for ch in t:
            if ch.upper() in classes:
                return ch.upper()
        return "?"
    for c in classes:                          # exact / leading
        if t == c or t.startswith(c):
            return c
    hits = [c for c in classes if c in t.replace(" ", "_") or c.replace("_", " ") in t]
    return hits[0] if len(hits) == 1 else (hits[0] if hits else "?")

def call(model, msgs, temperature=0.0, seed=1234):
    body = {"model": model, "messages": msgs, "stream": False,
            "options": {"temperature": temperature, "num_predict": 8, "seed": seed}}
    req = urllib.request.Request(OLLAMA + "/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.load(r)
    return {"text": resp["message"]["content"], "prompt_tokens": resp.get("prompt_eval_count"),
            "eval_tokens": resp.get("eval_count"), "total_ns": resp.get("total_duration"),
            "wall_s": time.time() - t0}

def run(model_tag, short, domain):
    d = D.load(domain)
    classes, gloss = d["classes"], d["gloss"]
    path = os.path.join(RAW, f"{short}__{domain}.json")
    cache = json.load(open(path)) if os.path.exists(path) else {}
    todo = [it for it in d["items"] if str(it["id"]) not in cache]
    print(f"[{short} / {domain}] {len(cache)} cached, {len(todo)} to run", flush=True)
    for n, it in enumerate(todo):
        for attempt in range(3):
            try:
                out = call(model_tag, messages(domain, it, classes, gloss)); break
            except Exception as e:
                if attempt == 2:
                    print(f"  !! {short} {domain} #{it['id']}: {e}", flush=True)
                    out = {"text": "", "prompt_tokens": None, "eval_tokens": None,
                           "total_ns": None, "wall_s": None}
                else:
                    time.sleep(2)
        out["pred"] = parse(out["text"], classes, domain)
        out["gold"] = it["gold"]
        cache[str(it["id"])] = out
        if (n + 1) % 40 == 0 or n + 1 == len(todo):
            json.dump(cache, open(path, "w"), indent=2)
    json.dump(cache, open(path, "w"), indent=2)
    acc = sum(v["pred"] == v["gold"] for v in cache.values()) / max(len(cache), 1)
    unp = sum(v["pred"] == "?" for v in cache.values())
    print(f"[{short} / {domain}] done. acc={acc:.3f} unparsed={unp}/{len(cache)}", flush=True)
    return acc

def available_models():
    """Ladder entries whose tag is actually present in Ollama (exact tag match)."""
    try:
        tags = {m["name"] for m in json.loads(
            urllib.request.urlopen(OLLAMA + "/api/tags", timeout=30).read())["models"]}
    except Exception as e:
        print("warn: could not list tags, trusting full ladder:", e)
        return list(LADDER)
    avail, missing = [], []
    for tag, short, p in LADDER:
        (avail if tag in tags else missing).append((tag, short, p))
    if missing:
        print("MISSING (skipped, logged):", [t for t, _, _ in missing])
    return avail

def main():
    domains = sys.argv[1].split(",") if len(sys.argv) > 1 else D.DOMAINS
    avail = available_models()
    print("models to run:", [s for _, s, _ in avail], flush=True)
    for tag, short, p in avail:                # batch per model
        for dom in domains:
            run(tag, short, dom)

if __name__ == "__main__":
    main()

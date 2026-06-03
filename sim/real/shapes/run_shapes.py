"""
run_shapes.py — drive the Lever-2 ladder over the task SHAPES, caching every call.
Resumable: nothing already cached is re-queried. Reaches Ollama on the China Mac via the
SSH tunnel (http://localhost:11434).

reason/seqstate: the model's free-form output is parsed to a discrete pred IN this runner.
code: only the raw generated code is cached here (pred is produced separately by
execute_code.py — the sandboxed execution is decoupled so it can be deferred safely).

Cache: results/raw/{short}__{shape}.json keyed by item id.
Run:  python3 run_shapes.py reason,seqstate        (all models)
      python3 run_shapes.py code qwen7b            (one shape, one model)
"""
from __future__ import annotations
import json, os, sys, re, time, urllib.request
import datasets_shapes as D

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "results", "raw")
os.makedirs(RAW, exist_ok=True)
OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# pre-registered 8-model ladder (PREREGISTRATION_lever2.md §3)
LADDER = [
    ("qwen2.5:0.5b-instruct", "qwen0.5b", 0.5),
    ("llama3.2:1b",           "llama1b",  1.0),
    ("qwen2.5:1.5b-instruct", "qwen1.5b", 1.5),
    ("gemma2:2b",             "gemma2b",  2.0),
    ("qwen2.5:3b-instruct",   "qwen3b",   3.0),
    ("llama3.2:3b",           "llama3b",  3.0),
    ("qwen2.5:7b-instruct",   "qwen7b",   7.0),
    ("llama3.1:8b",           "llama8b",  8.0),
]

NUM_PREDICT = 512   # room for chain-of-thought / multi-step traces / code


def messages(shape, item):
    if shape == "reason":
        sysp = "You are a careful math solver. Show your reasoning, then give the final integer."
    elif shape == "seqstate":
        sysp = ("You carefully track a register through a sequence of modular operations, "
                "one step at a time.")
    else:  # code
        sysp = "You are an expert Python programmer."
    return [{"role": "system", "content": sysp},
            {"role": "user", "content": item["text"]}]


def _last_int(text):
    """Prefer the integer after the last '####'; else the last integer in the text."""
    if not text:
        return None
    hsh = re.findall(r"####\s*(-?\d+)", text)
    if hsh:
        return int(hsh[-1])
    ints = re.findall(r"-?\d+", text)
    return int(ints[-1]) if ints else None


def parse_pred(shape, text, item):
    if shape == "reason":
        n = _last_int(text)
        return str(n % D.K_REASON) if n is not None else "?"
    if shape == "seqstate":
        n = _last_int(text)
        return str(n % D.K_SEQ) if n is not None else "?"
    # code: pred is deferred to execute_code.py; store placeholder
    return "__CODE__"


def call(model, msgs, temperature=0.0, seed=1234):
    body = {"model": model, "messages": msgs, "stream": False,
            "options": {"temperature": temperature, "num_predict": NUM_PREDICT, "seed": seed}}
    req = urllib.request.Request(OLLAMA + "/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
    return {"text": resp["message"]["content"], "prompt_tokens": resp.get("prompt_eval_count"),
            "eval_tokens": resp.get("eval_count"), "total_ns": resp.get("total_duration"),
            "wall_s": time.time() - t0}


def run(model_tag, short, shape):
    d = D.load(shape)
    path = os.path.join(RAW, f"{short}__{shape}.json")
    cache = json.load(open(path)) if os.path.exists(path) else {}
    todo = [it for it in d["items"] if str(it["id"]) not in cache]
    print(f"[{short} / {shape}] {len(cache)} cached, {len(todo)} to run", flush=True)
    for n, it in enumerate(todo):
        for attempt in range(3):
            try:
                out = call(model_tag, messages(shape, it)); break
            except Exception as e:
                if attempt == 2:
                    print(f"  !! {short} {shape} #{it['id']}: {e}", flush=True)
                    out = {"text": "", "prompt_tokens": None, "eval_tokens": None,
                           "total_ns": None, "wall_s": None}
                else:
                    time.sleep(2)
        out["pred"] = parse_pred(shape, out["text"], it)
        out["gold"] = it["gold"]
        cache[str(it["id"])] = out
        if (n + 1) % 20 == 0 or n + 1 == len(todo):
            json.dump(cache, open(path, "w"), indent=2)
    json.dump(cache, open(path, "w"), indent=2)
    if shape != "code":
        acc = sum(v["pred"] == v["gold"] for v in cache.values()) / max(len(cache), 1)
        unp = sum(v["pred"] == "?" for v in cache.values())
        print(f"[{short} / {shape}] done. acc={acc:.3f} unparsed={unp}/{len(cache)}", flush=True)
    else:
        print(f"[{short} / {shape}] generated {len(cache)} code samples (exec deferred)", flush=True)


def available_models():
    try:
        tags = {m["name"] for m in json.loads(
            urllib.request.urlopen(OLLAMA + "/api/tags", timeout=30).read())["models"]}
    except Exception as e:
        print("warn: could not list tags, trusting full ladder:", e); return list(LADDER)
    avail, missing = [], []
    for tag, short, p in LADDER:
        (avail if tag in tags else missing).append((tag, short, p))
    if missing:
        print("MISSING (skipped, logged):", [t for t, _, _ in missing])
    return avail


def unload(tag):
    try:
        body = json.dumps({"model": tag, "keep_alive": 0, "prompt": ""}).encode()
        urllib.request.urlopen(urllib.request.Request(
            OLLAMA + "/api/generate", data=body, headers={"Content-Type": "application/json"}),
            timeout=30).read()
    except Exception:
        pass
    time.sleep(2)


def main():
    shapes = sys.argv[1].split(",") if len(sys.argv) > 1 else D.SHAPES
    avail = available_models()
    only = sys.argv[2].split(",") if len(sys.argv) > 2 else None
    if only:
        avail = [m for m in avail if m[1] in only]
    print("shapes:", shapes, "| models:", [s for _, s, _ in avail], flush=True)
    for tag, short, p in avail:
        for sh in shapes:
            run(tag, short, sh)
        unload(tag)


if __name__ == "__main__":
    main()

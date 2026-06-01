"""
datasets.py — build the v2 multi-domain labeled corpora (the Axis-A breadth test).

Three public, abstractly-describable domains, each with the SAME structure as v1:
each item has a ground-truth correct label over K classes, and a model's text output
IS its chosen label.

  D1  intent     — CLINC150 confusable assistant-router slice          (K=6)
  D2  mcqa       — MMLU-style multiple-choice QA, mixed subjects        (K=4, A/B/C/D)
  D3  topic      — AG News topic classification                        (K=4)

Sources are fetched once (this Mac has cloud access) and cached to results/v2/data/
as {domain}.json = {classes, gloss, items:[{id,text,gold}], split:{fit,holdout}}.
No model is called here. Seeded + stratified fit/holdout (50/50).
"""
from __future__ import annotations
import json, os, random, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "results", "data")
os.makedirs(DATA, exist_ok=True)
SEED = 7
N_PER_DOMAIN = 240

def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "value-v2/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def _hf_rows(dataset, split, length, config=None, total=240):
    """Page the HuggingFace datasets-server REST API → list of row dicts."""
    rows, off = [], 0
    while len(rows) < total:
        url = (f"https://datasets-server.huggingface.co/rows?dataset={dataset}"
               + (f"&config={config}" if config else "") + f"&split={split}"
               f"&offset={off}&length={min(100, length)}")
        data = json.loads(_get(url))
        batch = data.get("rows", [])
        if not batch:
            break
        rows += [r["row"] for r in batch]
        off += len(batch)
    return rows

def _stratified_split(items, classes, seed=SEED, frac=0.5):
    by = {c: [] for c in classes}
    for it in items:
        by[it["gold"]].append(it["id"])
    rng = random.Random(seed)
    fit, hold = [], []
    for c in classes:
        ids = sorted(by[c]); rng.shuffle(ids)
        k = int(round(len(ids) * frac))
        fit += ids[:k]; hold += ids[k:]
    return {"fit": sorted(fit), "holdout": sorted(hold)}

def _finish(domain, classes, gloss, items):
    rng = random.Random(SEED)
    rng.shuffle(items)
    for i, it in enumerate(items):
        it["id"] = i
    out = {"domain": domain, "classes": classes, "gloss": gloss, "items": items,
           "split": _stratified_split(items, classes), "n": len(items), "K": len(classes)}
    path = os.path.join(DATA, f"{domain}.json")
    json.dump(out, open(path, "w"), indent=2)
    from collections import Counter
    print(f"[{domain}] {len(items)} items, K={len(classes)} -> {path}")
    print(f"   class balance: {dict(Counter(it['gold'] for it in items))}")
    return out

# ---------------------------------------------------------------------------
def build_intent():
    """D1: CLINC150 — 6 confusable time/task assistant-router intents."""
    raw = json.loads(_get("https://raw.githubusercontent.com/clinc/oos-eval/master/data/data_full.json"))
    pool = raw["train"] + raw["test"] + raw["val"]
    classes = ["alarm", "timer", "reminder", "calendar", "todo_list", "meeting_schedule"]
    gloss = {
        "alarm": "set/change/check a wake-up ALARM at a clock time",
        "timer": "set/check a countdown TIMER for a duration",
        "reminder": "manage REMINDERS to do a specific task",
        "calendar": "ask what events are on the CALENDAR by date",
        "todo_list": "manage a TO-DO LIST of tasks for the day",
        "meeting_schedule": "ask when a MEETING with someone is scheduled",
    }
    by = {c: [] for c in classes}
    seen = set()
    for text, intent in pool:
        if intent in by and text.strip().lower() not in seen:
            seen.add(text.strip().lower()); by[intent].append(text.strip())
    rng = random.Random(SEED)
    per = N_PER_DOMAIN // len(classes)
    items = []
    for c in classes:
        texts = sorted(set(by[c])); rng.shuffle(texts)
        items += [{"text": t, "gold": c} for t in texts[:per]]
    return _finish("intent", classes, gloss, items)

def build_mcqa():
    """D2: MMLU-style MCQA (mixed subjects), K=4 = A/B/C/D."""
    rows = _hf_rows("cais/mmlu", "test", 100, config="all", total=N_PER_DOMAIN + 40)
    classes = ["A", "B", "C", "D"]
    gloss = {c: f"answer option {c}" for c in classes}
    items = []
    for r in rows:
        q = r.get("question"); ch = r.get("choices"); ans = r.get("answer")
        if not q or not ch or len(ch) != 4 or ans is None:
            continue
        text = q.strip() + "\n" + "\n".join(f"{classes[i]}. {ch[i]}" for i in range(4))
        items.append({"text": text, "gold": classes[int(ans)]})
        if len(items) >= N_PER_DOMAIN:
            break
    return _finish("mcqa", classes, gloss, items)

def build_topic():
    """D3: AG News topic classification, K=4."""
    rows = _hf_rows("fancyzhx/ag_news", "test", 100, config="default", total=N_PER_DOMAIN + 200)
    classes = ["world", "sports", "business", "scitech"]
    gloss = {"world": "world / international news", "sports": "sports news",
             "business": "business / finance / economy news",
             "scitech": "science and technology news"}
    lbl = {0: "world", 1: "sports", 2: "business", 3: "scitech"}
    # balance across the 4 classes
    by = {c: [] for c in classes}
    for r in rows:
        c = lbl.get(r.get("label"))
        if c and r.get("text"):
            by[c].append(r["text"].strip())
    per = N_PER_DOMAIN // 4
    items = []
    for c in classes:
        items += [{"text": t, "gold": c} for t in by[c][:per]]
    return _finish("topic", classes, gloss, items)

DOMAINS = ["intent", "mcqa", "topic"]

def load(domain):
    return json.load(open(os.path.join(DATA, f"{domain}.json")))

if __name__ == "__main__":
    build_intent()
    build_mcqa()
    build_topic()

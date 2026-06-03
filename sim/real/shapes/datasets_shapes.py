"""
datasets_shapes.py — build the Lever-2 task-SHAPE corpora (PREREGISTRATION_lever2.md §2).

Three shapes with DISCRETE gold, each emitted in the SAME schema as v2's datasets.py
({domain, classes, gloss, items:[{id,text,gold,...}], split, n, K}) so the v2 analysis
machinery is reused unchanged:

  reason    GSM8K free-form CoT -> integer ; X = gold mod 4              (K=4)  [public]
  seqstate  synthetic register-machine rollout -> final state mod 6      (K=6)  [synthetic, exact gold]
  code      MBPP free-form function -> executed output, hash mod 4       (K=4)  [public]

No model is called here. Sources fetched once (cloud) and cached to results/data/.
Seeded + stratified fit/holdout (50/50), seed 7. Frozen per the pre-registration.
"""
from __future__ import annotations
import json, os, random, re, hashlib, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "results", "data")
os.makedirs(DATA, exist_ok=True)
SEED = 7

K_REASON, N_REASON = 4, 150
K_SEQ, N_SEQ, L_SEQ = 6, 150, 5
K_CODE, N_CODE = 4, 96


def _get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "value-lever2/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()

def _hf_rows(dataset, split, config=None, total=200):
    rows, off = [], 0
    while len(rows) < total:
        url = (f"https://datasets-server.huggingface.co/rows?dataset={dataset}"
               + (f"&config={config}" if config else "") + f"&split={split}"
               f"&offset={off}&length=100")
        data = json.loads(_get(url))
        batch = data.get("rows", [])
        if not batch:
            break
        rows += [r["row"] for r in batch]
        off += len(batch)
    return rows

def hash_modk(obj_repr: str, k: int) -> int:
    return int(hashlib.sha256(obj_repr.encode()).hexdigest(), 16) % k

def _stratified_split(items, classes, seed=SEED, frac=0.5):
    by = {c: [] for c in classes}
    for it in items:
        by[it["gold"]].append(it["id"])
    rng = random.Random(seed); fit, hold = [], []
    for c in classes:
        ids = sorted(by[c]); rng.shuffle(ids); k = int(round(len(ids) * frac))
        fit += ids[:k]; hold += ids[k:]
    return {"fit": sorted(fit), "holdout": sorted(hold)}

def _finish(domain, classes, gloss, items, extra=None):
    rng = random.Random(SEED); rng.shuffle(items)
    for i, it in enumerate(items):
        it["id"] = i
    out = {"domain": domain, "classes": classes, "gloss": gloss, "items": items,
           "split": _stratified_split(items, classes), "n": len(items), "K": len(classes)}
    if extra:
        out.update(extra)
    json.dump(out, open(os.path.join(DATA, f"{domain}.json"), "w"), indent=2)
    from collections import Counter
    print(f"[{domain}] {len(items)} items, K={len(classes)} -> results/data/{domain}.json")
    print(f"   gold-class balance: {dict(sorted(Counter(it['gold'] for it in items).items()))}")
    return out


# ── reason: GSM8K ─────────────────────────────────────────────────────────────
def build_reason():
    rows = _hf_rows("openai/gsm8k", "test", config="main", total=400)
    classes = [str(i) for i in range(K_REASON)]
    gloss = {c: f"final answer ≡ {c} (mod {K_REASON})" for c in classes}
    items = []
    for r in rows:
        q, a = r.get("question"), r.get("answer")
        if not q or not a:
            continue
        m = re.search(r"####\s*(-?[\d,]+)", a)
        if not m:
            continue
        val = m.group(1).replace(",", "")
        if not re.fullmatch(r"-?\d+", val):
            continue
        gold_int = int(val)
        if gold_int < 0:
            continue
        items.append({
            "text": q.strip() + "\n\nSolve step by step, then end with `#### <integer>`.",
            "gold": str(gold_int % K_REASON), "gold_int": gold_int,
        })
        if len(items) >= N_REASON:
            break
    return _finish("reason", classes, gloss, items)


# ── seqstate: synthetic sequential register-machine rollout ────────────────────
def build_seqstate():
    classes = [str(i) for i in range(K_SEQ)]
    gloss = {c: f"final register value = {c} (mod {K_SEQ})" for c in classes}
    rng = random.Random(SEED)
    items = []
    # oversample then stratify-balance toward uniform gold
    pool = []
    for _ in range(N_SEQ * 6):
        s0 = rng.randint(0, K_SEQ - 1)
        ops, val, lines = [], s0, []
        for _ in range(L_SEQ):
            kind = rng.choice(["+", "-", "*"])
            a = rng.randint(1, K_SEQ - 1)
            ops.append(f"{kind}{a}")
            if kind == "+": val = (val + a) % K_SEQ
            elif kind == "-": val = (val - a) % K_SEQ
            else: val = (val * a) % K_SEQ
        opstr = ", ".join(ops)
        text = (f"A register holds an integer, reduced modulo {K_SEQ} after every "
                f"operation (so it stays in 0..{K_SEQ-1}).\n"
                f"Start: register = {s0}.\n"
                f"Apply these operations in order (each: op then take mod {K_SEQ}): {opstr}.\n"
                f"Apply them one at a time, show each intermediate value, then end with "
                f"`#### <final value 0..{K_SEQ-1}>`.")
        pool.append({"text": text, "gold": str(val), "s0": s0, "ops": ops})
    # balance across classes
    by = {c: [] for c in classes}
    for it in pool:
        by[it["gold"]].append(it)
    per = N_SEQ // K_SEQ
    for c in classes:
        items += by[c][:per]
    return _finish("seqstate", classes, gloss, items)


# ── code: MBPP, executed-output hash ───────────────────────────────────────────
_ASSERT_RE = re.compile(r"assert\s+(\w+)\s*\((.*)\)\s*==\s*(.+?)\s*$")

def build_code():
    rows = _hf_rows("google-research-datasets/mbpp", "test", config="full", total=400)
    classes = [str(i) for i in range(K_CODE)]
    gloss = {c: f"executed output hashes to class {c} (mod {K_CODE})" for c in classes}
    items = []
    for r in rows:
        prompt, tests, ref = r.get("text"), r.get("test_list"), r.get("code")
        if not prompt or not tests or not ref:
            continue
        m = _ASSERT_RE.match(tests[0].strip())
        if not m:
            continue
        fn, args, rhs = m.group(1), m.group(2), m.group(3).strip()
        # gold output literal = eval(rhs) in a clean namespace (no model code involved)
        try:
            gold_out = eval(rhs, {"__builtins__": {}}, {})
        except Exception:
            continue
        gold_cls = str(hash_modk(repr(gold_out), K_CODE))
        items.append({
            "text": (f"Write a Python function named `{fn}` that solves:\n{prompt.strip()}\n"
                     f"Reply with ONLY the function definition in a ```python code block."),
            "gold": gold_cls, "fn": fn, "call": f"{fn}({args})",
            "gold_out_repr": repr(gold_out),
        })
        if len(items) >= N_CODE:
            break
    return _finish("code", classes, gloss, items, extra={"K_hash": K_CODE})


SHAPES = ["reason", "seqstate", "code"]

def load(domain):
    return json.load(open(os.path.join(DATA, f"{domain}.json")))

if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or SHAPES
    if "reason" in which:   build_reason()
    if "seqstate" in which: build_seqstate()
    if "code" in which:     build_code()

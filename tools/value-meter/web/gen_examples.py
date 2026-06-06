"""
gen_examples.py — convert cached harness runs into small, self-contained record
sets the web demo can load (and reproduce the paper's numbers on, live).

Usage:  python3 gen_examples.py <repo_root> <out_dir>
"""
import json
import os
import sys

REPO, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def from_run(run_path, data_path, note):
    """Emit {classes, note, records:[{gold,pred,cost_tokens,cost_latency}]} in id order."""
    run = json.load(open(run_path))
    data = json.load(open(data_path))
    classes = data["classes"]
    order = [str(it["id"]) for it in sorted(data["items"], key=lambda x: x["id"])]
    recs = []
    for sid in order:
        o = run.get(sid)
        if o is None:
            continue
        toks = (o.get("prompt_tokens") or 0) + (o.get("eval_tokens") or 0)
        ns = o.get("total_ns")
        rec = {"gold": o["gold"], "pred": o["pred"]}
        if toks:
            rec["cost_tokens"] = toks
        if ns:
            rec["cost_latency"] = round(ns / 1e9, 4)
        recs.append(rec)
    return {"classes": classes, "note": note, "records": recs}


V2 = os.path.join(REPO, "sim", "real", "v2", "results")
SH = os.path.join(REPO, "sim", "real", "shapes", "results")

examples = {
    "intent_qwen0.5b.json": from_run(
        os.path.join(V2, "raw", "qwen0.5b__intent.json"),
        os.path.join(V2, "data", "intent.json"),
        "qwen0.5b on a 6-way intent router (CLINC150 slice). A 0.5B model already "
        "near the ceiling: reproduces the paper's I=1.4166 nats, out-of-sample ΔG=1.3077."),
    "seqstate_llama3b.json": from_run(
        os.path.join(SH, "raw", "llama3b__seqstate.json"),
        os.path.join(SH, "data", "seqstate.json"),
        "llama3b on a synthetic register-machine rollout (the widest-information shape). "
        "Reproduces I=1.5629 nats, ΔG=1.3427; note the high dissipation and high token cost."),
    "topic_llama1b.json": from_run(
        os.path.join(V2, "raw", "llama1b__topic.json"),
        os.path.join(V2, "data", "topic.json"),
        "llama1b on AG-News topic classification — a near-chance point: I≈0.029 nats, "
        "barely above the permutation null. Shows what 'no value extracted' looks like."),
}

for name, obj in examples.items():
    json.dump(obj, open(os.path.join(OUT, name), "w"), indent=1)
    print(f"   wrote {name}: {len(obj['records'])} records")

# carry over the toy stated-belief example (shows agent-reported-prob dissipation)
toy_src = os.path.join(REPO, "tools", "value-meter", "examples", "toy_agent_with_belief.json")
if os.path.exists(toy_src):
    toy = json.load(open(toy_src))
    toy["note"] = ("a synthetic agent that REPORTS its own belief (prob vector) — so "
                   "dissipation is measured against its stated probabilities, not a "
                   "constructed one. ~75% accurate, well-calibrated.")
    json.dump(toy, open(os.path.join(OUT, "toy_agent_with_belief.json"), "w"), indent=1)
    print(f"   wrote toy_agent_with_belief.json: {len(toy['records'])} records")

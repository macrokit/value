"""
bench_data.py — load the Macrokit launch-benchmark corpus + cached model runs and
map them into the value framework.

Mapping (HANDOFF ★):
    World X   = the CORRECT action per task = the gold tool/macro to route to
                (6 maintainer macros + a "none" class for the no-macro tasks).
    Signal Y_a= model a's CHOSEN action = the tool it actually called
                (or "none" when it replied in free text / called nothing).
    q(x)      = the empirical distribution of correct actions over the corpus.
    r(x)      = the reference/baseline belief; we use r = q (the action marginal),
                so a model with no signal grows value at rate 0 and the capacity
                identity ΔG = I(X;Y) holds for the oracle posterior.

Every quantity downstream is computed with sim/value_sim.py, in nats. Accuracy is
only a sanity-check ladder; the value quantities (I, ΔG, D(q‖p)) are the result.

The benchmark is a tool-use / intent-routing task; per Sacred Rule #1 the public
write-up describes it abstractly ("a 100-task tool-use benchmark"), never by its
Macrokit/maintainer specifics.
"""
from __future__ import annotations
import glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH = os.path.expanduser("~/Documents/macrokit/core/bench")
RUNS = os.path.join(BENCH, "runs")
LOCAL_RUNS = os.path.join(HERE, "results", "bench_runs")   # local copies, re-runnable

# The action/label space: the 6 macros + "none" (no-macro). Frozen order.
ACTIONS = [
    "triage_pull_request", "triage_issue", "generate_release_notes",
    "close_stale_issues", "suggest_reviewers", "capture_workflow_log", "none",
]
AIDX = {a: i for i, a in enumerate(ACTIONS)}

# Capability ladder rungs. Each rung is matched against a run's modelId/display by
# substring patterns, so it discovers runs regardless of whether the parallel
# benchmark session named them as ollama tags or llama-server ids.
RUNGS = [
    ("qwen1.5b", 1.5, ["1.5b", "1_5b", "1.5B"]),
    ("qwen3b",   3.0, ["3b", "3B"]),
    ("qwen7b",   7.0, ["7b", "7B"]),
    ("llama8b",  8.0, ["8b", "8B", "llama3.1", "llama-3.1"]),
]

def _norm(tool):
    """Map a raw tool field (None / unknown / macro name) to an ACTIONS label."""
    if tool is None or tool == "None" or tool == "":
        return "none"
    return tool if tool in AIDX else "none"   # unknown/hallucinated tool -> treated as no valid action

def _all_run_paths():
    paths = glob.glob(os.path.join(LOCAL_RUNS, "*.jsonl")) + glob.glob(os.path.join(RUNS, "*.jsonl"))
    return [p for p in paths if not p.endswith(".summary.json")]

def _header(path):
    try:
        with open(path) as f:
            o = json.loads(f.readline())
        return o if o.get("type") == "header" else {}
    except Exception:
        return {}

def classify_run(path):
    """Assign a run file to a ladder rung (short, params) by inspecting its header.
    Returns None for unmatched or excluded (mistral) runs."""
    h = _header(path)
    blob = (str(h.get("modelId", "")) + " " + str(h.get("modelDisplay", "")) + " " +
            os.path.basename(path)).lower()
    if "mistral" in blob:                       # dropped: Ollama tool-call incompat
        return None
    for short, params, pats in RUNGS:
        if any(p.lower() in blob for p in pats):
            return short, params
    return None

def parse_run(path):
    recs = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        if o.get("type") != "task":
            continue
        gold = _norm(o["expected"].get("tool"))
        pred = _norm(o.get("actualTool"))
        tool_score = o.get("toolScore", 0) or 0
        args_score = o.get("argsScore", 0) or 0
        recs.append({
            "task_id": o["taskId"],
            "bucket": o["bucket"],
            "difficulty": o.get("difficulty"),
            "gold": gold,
            "pred": pred,
            "args_ok": bool(args_score),
            "full_ok": bool(tool_score and args_score),
            "score": float(tool_score) + float(args_score),     # 0,1,2
            "latency_ms": o.get("latencyMs"),
            "bailout": o.get("bailOutCode"),
        })
    return {"path": path, "tasks": recs}

EXPECTED_N = 100   # the frozen corpus size; partial runs are excluded as artifacts

def _run_quality(run):
    """(accuracy, n_tasks) — used to pick the best run of a model and to reject
    crash artifacts. A tool-call plumbing failure collapses to ~all 'none' and a
    near-zero accuracy, so it loses to any real run of the same model."""
    n = len(run["tasks"]) or 1
    acc = sum(t["pred"] == t["gold"] for t in run["tasks"]) / n
    return acc, len(run["tasks"])

def is_artifact(run, none_thresh=0.85):
    """True if the run looks like a tool-call plumbing artifact, not real behavior."""
    n = len(run["tasks"]) or 1
    none_frac = sum(t["pred"] == "none" for t in run["tasks"]) / n
    acc = sum(t["pred"] == t["gold"] for t in run["tasks"]) / n
    return none_frac > none_thresh and acc < 0.30

def available_fleet(require_complete=True, drop_artifacts=True):
    """Discover all run files, classify each to a ladder rung, and keep the BEST
    complete run per rung — best = highest accuracy (so a crash artifact loses to a
    real run of the same model), then most tasks. Returns [(short, params, run), ...]
    in ladder order. Naming-robust, mistral-excluded, artifact-rejecting."""
    best = {}                                    # short -> (params, run, quality)
    for path in _all_run_paths():
        cls = classify_run(path)
        if not cls:
            continue
        short, params = cls
        run = parse_run(path)
        if require_complete and len(run["tasks"]) != EXPECTED_N:
            continue
        if drop_artifacts and is_artifact(run):
            continue
        q = _run_quality(run)
        cur = best.get(short)
        if cur is None or q > cur[2]:
            best[short] = (params, run, q)
    out = []
    for short, params, _ in RUNGS:
        if short in best:
            params_b, run, _ = best[short]
            out.append((short, params_b, run))
    return out

def task_ids(run):
    return [t["task_id"] for t in run["tasks"]]

# ---------------------------------------------------------------------------
# Corpus loader + a model-independent stratified split (so fit/holdout are the
# same task ids for every model).
# ---------------------------------------------------------------------------
def load_corpus():
    """All 100 tasks from bench/tasks/*.jsonl as {task_id, gold, bucket, difficulty}."""
    import glob as _g
    out = []
    for f in sorted(_g.glob(os.path.join(BENCH, "tasks", "*.jsonl"))):
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            o = json.loads(line)
            out.append({"task_id": o["id"], "gold": _norm(o["expected"].get("tool")),
                        "bucket": o["bucket"], "difficulty": o.get("difficulty")})
    return out

def stratified_split(seed=7, frac=0.5):
    """Deterministic stratified (by gold action) fit/holdout split over the corpus."""
    import random
    corpus = load_corpus()
    by = {}
    for t in corpus:
        by.setdefault(t["gold"], []).append(t["task_id"])
    rng = random.Random(seed)
    fit, hold = [], []
    for g in sorted(by):
        ids = sorted(by[g]); rng.shuffle(ids)
        k = int(round(len(ids) * frac))
        fit += ids[:k]; hold += ids[k:]
    return set(fit), set(hold)

if __name__ == "__main__":
    print("ACTIONS:", ACTIONS)
    for short, p, run in available_fleet():
        n = len(run["tasks"])
        acc = sum(t["pred"] == t["gold"] for t in run["tasks"]) / n
        full = sum(t["full_ok"] for t in run["tasks"]) / n
        print(f"  {short:9} ({p}B)  n={n}  tool-acc={acc:.3f}  full(tool+args)={full:.3f}  <- {os.path.basename(run['path'])}")

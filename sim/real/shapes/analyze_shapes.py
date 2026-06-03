"""
analyze_shapes.py — score the Lever-2 task-SHAPE runs against the frozen thresholds
(PREREGISTRATION_lever2.md §4). Cache-only; calls no models.

Reuses the EXACT v2 pipeline (confusion -> I = mutual_information; calibrated posterior on
the seeded fit split; out-of-sample ΔG on holdout = mean ln p(x|y)/r(x)), mirrored here so
the same numbers are produced for the new shapes AND recomputed for v2's 3 classification
domains (for the cross-shape pooled regression L2-d). Adds the permutation-null I floor.

Run: python3 analyze_shapes.py   -> results/lever2_analysis.json + verdict to stdout
"""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ))
import value_sim as v
import datasets_shapes as DS

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "results", "raw")
V2 = os.path.join(HERE, "..", "v2")
V2_RAW = os.path.join(V2, "results", "raw")
RNG = np.random.default_rng(7)
N_BOOT = 2000

NEW_SHAPES = ["reason", "seqstate", "code"]
V2_DOMAINS = ["intent", "mcqa", "topic"]
LADDER_SHORT = ["qwen0.5b", "llama1b", "qwen1.5b", "gemma2b", "qwen3b", "llama3b", "qwen7b", "llama8b"]
DEGRADED_UNPARSED = 0.50


def spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    if len(x) < 3: return float("nan")
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])

def boot_ci(stat_fn, n, level=0.95):
    vals = [stat_fn(RNG.integers(0, n, n)) for _ in range(N_BOOT)]
    vals = [x for x in vals if x == x]
    lo, hi = np.percentile(vals, [(1-level)/2*100, (1+level)/2*100])
    return float(lo), float(hi)

def load_data(shape, v2=False):
    p = os.path.join(V2 if v2 else HERE, "results", "data", f"{shape}.json")
    return json.load(open(p))

def load_run(short, shape, v2=False):
    p = os.path.join(V2_RAW if v2 else RAW, f"{short}__{shape}.json")
    return json.load(open(p)) if os.path.exists(p) else None

def confusion(run, classes, ylab, ids=None):
    idx = {c: i for i, c in enumerate(classes)}; yidx = {y: i for i, y in enumerate(ylab)}
    C = np.zeros((len(classes), len(ylab)))
    for sid, o in run.items():
        if ids is not None and int(sid) not in ids: continue
        if o["gold"] not in idx or o["pred"] not in yidx: continue
        C[idx[o["gold"]], yidx[o["pred"]]] += 1
    return C

def calib(C_fit, alpha=0.5):
    P = C_fit + alpha
    return P / P.sum(axis=0, keepdims=True)

def marginal(data):
    classes = data["classes"]; c = np.zeros(len(classes)); idx = {x: i for i, x in enumerate(classes)}
    for it in data["items"]:
        c[idx[it["gold"]]] += 1
    return c / c.sum(), classes

def per_item_value(run, post, classes, ylab, ids, r):
    idx = {c: i for i, c in enumerate(classes)}; yidx = {y: i for i, y in enumerate(ylab)}
    vals = {}
    for sid, o in run.items():
        if int(sid) not in ids: continue
        if o["gold"] not in idx or o["pred"] not in yidx: continue
        x = idx[o["gold"]]; y = yidx[o["pred"]]
        vals[int(sid)] = float(np.log(post[x, y] / r[x]))
    return vals

def accuracy(run, ids=None):
    its = [(o["gold"], o["pred"]) for s, o in run.items() if ids is None or int(s) in ids]
    return float(np.mean([g == p for g, p in its])) if its else float("nan")

def unparsed_rate(run):
    return float(np.mean([o["pred"] in ("?", "__CODE__") for o in run.values()])) if run else 1.0

def perm_null_I(run, classes, ylab, n_shuf=20):
    """Mean I over label-shuffles of Y — the finite-sample bias floor (L2-e)."""
    idx = {c: i for i, c in enumerate(classes)}; yidx = {y: i for i, y in enumerate(ylab)}
    golds = [idx[o["gold"]] for o in run.values() if o["gold"] in idx and o["pred"] in yidx]
    preds = [yidx[o["pred"]] for o in run.values() if o["gold"] in idx and o["pred"] in yidx]
    rng = np.random.default_rng(13); Is = []
    for _ in range(n_shuf):
        sp = rng.permutation(preds)
        C = np.zeros((len(classes), len(ylab)))
        for g, y in zip(golds, sp): C[g, y] += 1
        Is.append(v.mutual_information(C))
    return float(np.mean(Is))


def points_for(shape, v2=False):
    """Return list of (short, acc, I, dG_hold, I_null) for one shape/domain."""
    data = load_data(shape, v2); classes = data["classes"]; ylab = classes + ["?"]
    if not v2 and shape == "code":
        ylab = classes + ["?"]
    r, _ = marginal(data); split = data["split"]; fit, hold = set(split["fit"]), set(split["holdout"])
    n = data["n"]; pts = []
    for short in LADDER_SHORT:
        run = load_run(short, shape, v2)
        if not run or len(run) < 0.95 * n: continue
        if unparsed_rate(run) > DEGRADED_UNPARSED:
            print(f"     !! EXCLUDED {short}/{shape}: {unparsed_rate(run):.0%} unparseable (plumbing)")
            continue
        C = confusion(run, classes, ylab); I = v.mutual_information(C); acc = accuracy(run)
        post = calib(confusion(run, classes, ylab, fit))
        vals = per_item_value(run, post, classes, ylab, hold, r)
        dG = float(np.mean(list(vals.values()))) if vals else float("nan")
        pts.append((short, acc, I, dG, perm_null_I(run, classes, ylab)))
    return pts


def analyze():
    out = {"shapes": {}, "checks": []}
    def rec(name, ok, detail):
        out["checks"].append((name, bool(ok), detail))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    # ── per-shape (L2-a, L2-b) ────────────────────────────────────────────────
    completed_new, all_pts_new = [], []
    print("\n=== Per-shape (L2-a Spearman(I,acc)>0.70 ; L2-b slope(ΔG~I) CI excludes 0) ===")
    for shape in NEW_SHAPES:
        pts = points_for(shape, v2=False)
        if len(pts) < 6:
            print(f"  [----] {shape}: only {len(pts)} models present (<6) — not yet complete, skipped")
            out["shapes"][shape] = {"status": "incomplete", "n_models": len(pts),
                                    "points": [(p[0], p[1], p[2], p[3], p[4]) for p in pts]}
            continue
        accs = [p[1] for p in pts]; Is = [p[2] for p in pts]; dGs = [p[3] for p in pts]
        nulls = [p[4] for p in pts]
        print(f"  {shape}: " + "  ".join(f"{p[0]}(acc={p[1]:.2f},I={p[2]:.3f},ΔG={p[3]:.3f})" for p in pts))
        # capability spread check (CAP)
        if max(accs) - min(accs) < 0.10:
            rec(f"{shape} CAP — capability spread", False,
                f"acc range {min(accs):.2f}–{max(accs):.2f} < 0.10 ⇒ uninformative at this scale")
            out["shapes"][shape] = {"status": "cap_no_spread", "acc_range": [min(accs), max(accs)],
                                    "points": [(p[0], p[1], p[2], p[3], p[4]) for p in pts]}
            continue
        rho = spearman(accs, Is)
        rlo, rhi = boot_ci(lambda idx: spearman([accs[i] for i in idx], [Is[i] for i in idx]), len(pts))
        a = rec(f"L2-a {shape} Spearman(I,acc)>0.70", rho > 0.70, f"ρ={rho:.3f} CI[{rlo:.3f},{rhi:.3f}] n={len(pts)}")
        def slope(idx, X=Is, Y=dGs):
            X = np.array([X[i] for i in idx]); Y = np.array([Y[i] for i in idx])
            return float(np.polyfit(X, Y, 1)[0])
        s = slope(range(len(pts))); slo, shi = boot_ci(slope, len(pts))
        b = rec(f"L2-b {shape} slope(ΔG~I) CI excludes 0", slo > 0, f"slope={s:.3f} CI[{slo:.3f},{shi:.3f}]")
        # L2-e info floor
        floor_ok = sum(1 for I, nl in zip(Is, nulls) if I > 3 * max(nl, 1e-9)) >= 0.9 * len(pts)
        rec(f"L2-e {shape} info-floor (I>3×null, ≥90%)", floor_ok,
            f"null≈{np.mean(nulls):.3f} vs I≈{np.mean(Is):.3f}")
        completed_new.append(shape); all_pts_new += pts
        out["shapes"][shape] = {"status": "complete", "rho": rho, "slope": s,
                                "points": [(p[0], p[1], p[2], p[3], p[4]) for p in pts]}

    # ── pooled across new shapes (L2-c) ───────────────────────────────────────
    print("\n=== Pooled across completed NEW shapes (L2-c slope CI excl 0 AND ∈[0.5,1.5]) ===")
    if len(completed_new) >= 2:
        Is = [p[2] for p in all_pts_new]; dGs = [p[3] for p in all_pts_new]
        def slope(idx):
            X = np.array([Is[i] for i in idx]); Y = np.array([dGs[i] for i in idx])
            return float(np.polyfit(X, Y, 1)[0])
        s = slope(range(len(all_pts_new))); slo, shi = boot_ci(slope, len(all_pts_new))
        rec("L2-c pooled-new slope ∈[0.5,1.5] & CI excl 0", slo > 0 and 0.5 <= s <= 1.5,
            f"slope={s:.3f} CI[{slo:.3f},{shi:.3f}] n={len(all_pts_new)} shapes={completed_new}")
    else:
        print(f"  [----] only {len(completed_new)} new shapes complete (<2) — L2-c deferred")

    # ── cross-shape with classification (L2-d) ────────────────────────────────
    print("\n=== Cross-shape incl. v2 classification (L2-d ρ>0.80 & slope CI excl 0) ===")
    v2_pts = []
    for dom in V2_DOMAINS:
        try:
            v2_pts += points_for(dom, v2=True)
        except Exception as e:
            print(f"  (v2 {dom} unavailable: {e})")
    if len(completed_new) >= 2 and v2_pts:
        pool = all_pts_new + v2_pts
        accs = [p[1] for p in pool]; Is = [p[2] for p in pool]; dGs = [p[3] for p in pool]
        rho = spearman(accs, Is)
        rlo, rhi = boot_ci(lambda idx: spearman([accs[i] for i in idx], [Is[i] for i in idx]), len(pool))
        rec("L2-d cross-shape Spearman(I,acc)>0.80", rho > 0.80, f"ρ={rho:.3f} CI[{rlo:.3f},{rhi:.3f}] n={len(pool)}")
        def slope(idx):
            X = np.array([Is[i] for i in idx]); Y = np.array([dGs[i] for i in idx])
            return float(np.polyfit(X, Y, 1)[0])
        s = slope(range(len(pool))); slo, shi = boot_ci(slope, len(pool))
        rec("L2-d cross-shape slope(ΔG~I) CI excludes 0", slo > 0, f"slope={s:.3f} CI[{slo:.3f},{shi:.3f}]")
        out["pooled_all"] = {"rho": rho, "slope": s, "n": len(pool)}
    else:
        print("  [----] need ≥2 new shapes + v2 points — L2-d deferred")

    # ── verdict ───────────────────────────────────────────────────────────────
    checks = out["checks"]
    n_pass = sum(1 for _, ok, _ in checks if ok)
    print("\n" + "=" * 70)
    print(f"LEVER-2: {n_pass}/{len(checks)} checks passed (completed shapes: {completed_new})")
    for nm, ok, _ in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {nm}")
    print("=" * 70)
    out["completed_new_shapes"] = completed_new
    json.dump(out, open(os.path.join(HERE, "results", "lever2_analysis.json"), "w"), indent=2)
    print("→ results/lever2_analysis.json")


if __name__ == "__main__":
    analyze()

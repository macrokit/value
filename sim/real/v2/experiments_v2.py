"""
experiments_v2.py — R1-v2, R2-v2, Fleet-R5, ceiling, scored against PREREGISTRATION.md.

Reads results/raw/{model}__{domain}.json + results/data/{domain}.json. Computes every
quantity with sim/value_sim.py (nats). Reports point estimates with 95% bootstrap CIs.
Calls no models; re-runs offline from cache. Writes artifacts to results/.
"""
from __future__ import annotations
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import value_sim as v
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import datasets as D

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "results", "raw")
RNG = np.random.default_rng(7)
N_BOOT = 2000
SEEDS = [7, 11, 23, 42, 101]            # for split-dependent CIs

results = []
def rec(name, verdict, detail):
    results.append((name, verdict, detail))
    tag = {True: "PASS", False: "FAIL", None: "----"}[verdict]
    print(f"  [{tag}] {name}: {detail}")

# ---------------------------------------------------------------------------
def load_run(short, domain):
    p = os.path.join(RAW, f"{short}__{domain}.json")
    return json.load(open(p)) if os.path.exists(p) else None

# Flag #2: text-output analog of v1's artifact guard. A model that silently degrades
# (truncation / refusal loops / format collapse under load) emits UNPARSEABLE output,
# not a wrong label — that is plumbing, not capability, and must not be recorded as a
# low-I capability point. Runs with > this fraction of '?' are excluded + logged.
DEGRADED_UNPARSED = 0.50
_logged_degraded = set()

def unparsed_rate(run):
    return float(np.mean([o["pred"] == "?" for o in run.values()])) if run else 1.0

def present_models(domain):
    import run_v2
    n = D.load(domain)["n"]; out = []
    for tag, short, params in run_v2.LADDER:
        c = load_run(short, domain)
        if not c or len(c) < 0.95 * n:
            continue
        ur = unparsed_rate(c)
        if ur > DEGRADED_UNPARSED:
            key = (short, domain)
            if key not in _logged_degraded:
                print(f"     !! EXCLUDED {short}/{domain}: {ur:.0%} unparseable — suspected "
                      f"degradation (plumbing), not capability."); _logged_degraded.add(key)
            continue
        out.append((short, params))
    return out

def confusion(run, classes, ylab, ids=None):
    idx = {c: i for i, c in enumerate(classes)}
    yidx = {y: i for i, y in enumerate(ylab)}
    C = np.zeros((len(classes), len(ylab)))
    for sid, o in run.items():
        if ids is not None and int(sid) not in ids:
            continue
        C[idx[o["gold"]], yidx[o["pred"]]] += 1
    return C

def calib(C_fit, alpha=0.5):
    P = C_fit + alpha
    return P / P.sum(axis=0, keepdims=True)

def marginal(domain):
    d = D.load(domain); classes = d["classes"]
    c = np.zeros(len(classes)); idx = {x: i for i, x in enumerate(classes)}
    for it in d["items"]:
        c[idx[it["gold"]]] += 1
    return c / c.sum(), classes

def per_item_value(run, post, classes, ylab, ids, r):
    """ln(p(x_gold|y_pred)/r(x_gold)) per holdout item -> dict id->value."""
    idx = {c: i for i, c in enumerate(classes)}; yidx = {y: i for i, y in enumerate(ylab)}
    vals = {}
    for sid, o in run.items():
        if int(sid) not in ids:
            continue
        x = idx[o["gold"]]; y = yidx[o["pred"]]
        vals[int(sid)] = float(np.log(post[x, y] / r[x]))
    return vals

def accuracy(run, ids=None):
    its = [(o["gold"], o["pred"]) for s, o in run.items() if ids is None or int(s) in ids]
    return float(np.mean([g == p for g, p in its])) if its else float("nan")

def mean_tokens(run):
    t = [(o.get("prompt_tokens") or 0) + (o.get("eval_tokens") or 0) for o in run.values()]
    return float(np.mean(t)) if t else float("nan")

def mean_latency(run):
    """MEDIAN per-call latency (s), load-robust. (Flag #1) The post-hoc eviction fix
    (run_v2.unload) injects one-time model-LOAD time into the first call of each batch;
    the MEAN would be biased by that single outlier — unevenly, since bigger models load
    slower — distorting the R3/R5 cost ranking that the headline depends on. The median
    excludes the lone load call and reflects generation cost. Pre-registration named
    *mean* latency (SECONDARY cost); we report median for this measurement-artifact reason
    and disclose it in docs/09. The PRIMARY cost — tokens — is load-free and unchanged."""
    t = [(o.get("total_ns") or 0) / 1e9 for o in run.values() if o.get("total_ns")]
    return float(np.median(t)) if t else float("nan")

def split(domain, seed):
    """Re-derive a seeded stratified fit/holdout split for CI over seeds."""
    import random
    d = D.load(domain); classes = d["classes"]
    by = {c: [] for c in classes}
    for it in d["items"]:
        by[it["gold"]].append(it["id"])
    rng = random.Random(seed); fit, hold = [], []
    for c in classes:
        ids = sorted(by[c]); rng.shuffle(ids); k = len(ids) // 2
        fit += ids[:k]; hold += ids[k:]
    return set(fit), set(hold)

def spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])

def boot_ci(stat_fn, n, level=0.95):
    """Bootstrap CI by resampling indices 0..n-1 i.i.d.

    NOTE (2026-06-07, post-review): for pooled model×domain analyses the points
    are clustered by model (10 models × 3 domains), so i.i.d. resampling is
    anti-conservative (effective n ≈ #models). Use cluster_boot_ci for those."""
    vals = []
    for _ in range(N_BOOT):
        idx = RNG.integers(0, n, n)
        vals.append(stat_fn(idx))
    lo, hi = np.percentile(vals, [(1-level)/2*100, (1+level)/2*100])
    return float(lo), float(hi)

def cluster_boot_ci(stat_fn, clusters, level=0.95):
    """Cluster bootstrap: resample CLUSTERS (models) with replacement, taking
    all of each selected cluster's point indices. `clusters` = list of
    index-lists, one per cluster. Conservative for model-clustered points."""
    m = len(clusters)
    vals = []
    for _ in range(N_BOOT):
        picked = RNG.integers(0, m, m)
        idx = [i for c in picked for i in clusters[c]]
        vals.append(stat_fn(idx))
    lo, hi = np.percentile(vals, [(1-level)/2*100, (1+level)/2*100])
    return float(lo), float(hi)


# ===========================================================================
def R1_v2():
    print("\nR1-v2 — the bridge generalizes: I(X;Y) tracks capability across domains/models")
    pts = []   # (short, domain, params, acc, I, dG_hold)
    for domain in D.DOMAINS:
        r, classes = marginal(domain); ylab = classes + ["?"]
        Q = r
        for short, params in present_models(domain):
            run = load_run(short, domain)
            C = confusion(run, classes, ylab)
            I = v.mutual_information(C); acc = accuracy(run)
            fit, hold = split(domain, 7)
            post = calib(confusion(run, classes, ylab, fit))
            vals = per_item_value(run, post, classes, ylab, hold, r)
            dG = float(np.mean(list(vals.values()))) if vals else float("nan")
            pts.append((short, domain, params, acc, I, dG))
    # print per (domain, model)
    print(f"     {'domain':8} {'model':9} {'acc':>6} {'I(nats)':>8} {'ΔG_hold':>8}")
    for short, dom, p, acc, I, dG in pts:
        print(f"     {dom:8} {short:9} {acc:6.3f} {I:8.4f} {dG:8.4f}")
    accs = [p[3] for p in pts]; Is = [p[4] for p in pts]; dGs = [p[5] for p in pts]
    # R1a: pooled Spearman(I, accuracy) > 0.8 with CI
    # DISCLOSURE (2026-06-07): the prereg criterion is rho > 0.8 (CI reported).
    # The original pass condition here also required lo > 0.5 — an UNREGISTERED
    # extra condition; it is kept but flagged, and the registered criterion is
    # what decides the verdict. CIs are now ALSO cluster-bootstrapped by model
    # (points are 10 models × 3 domains; i.i.d. CI is anti-conservative).
    rho = spearman(accs, Is)
    sfn = lambda idx: spearman([accs[i] for i in idx], [Is[i] for i in idx])
    lo, hi = boot_ci(sfn, len(pts))
    models = sorted({p[0] for p in pts})
    clusters = [[i for i, p in enumerate(pts) if p[0] == m_] for m_ in models]
    clo, chi = cluster_boot_ci(sfn, clusters)
    rec("R1a pooled Spearman(I, accuracy) > 0.8 [registered criterion]", rho > 0.8,
        f"ρ={rho:.3f}  iid 95%CI[{lo:.3f},{hi:.3f}]  CLUSTERED-by-model 95%CI[{clo:.3f},{chi:.3f}]"
        f"  (n={len(pts)} points, {len(models)} model clusters; unregistered lo>0.5 check: {lo > 0.5})")
    # per-domain rho > 0.6
    perdom_ok = True
    for domain in D.DOMAINS:
        a = [p[3] for p in pts if p[1] == domain]; ii = [p[4] for p in pts if p[1] == domain]
        rd = spearman(a, ii); perdom_ok &= (rd > 0.6)
        print(f"        per-domain ρ[{domain}] = {rd:.3f} (n={len(a)})")
    rec("R1a per-domain Spearman > 0.6 in every domain", perdom_ok, "")
    # R1b: slope of ΔG_hold on I, CI excludes 0 and positive
    def slope(idx):
        X = np.array([Is[i] for i in idx]); Y = np.array([dGs[i] for i in idx])
        return float(np.polyfit(X, Y, 1)[0])
    s = slope(range(len(pts))); slo, shi = boot_ci(slope, len(pts))
    cslo, cshi = cluster_boot_ci(slope, clusters)
    rec("R1b slope(ΔG_hold ~ I) CI excludes 0 (positive)", slo > 0 and cslo > 0,
        f"slope={s:.3f}  iid 95%CI[{slo:.3f},{shi:.3f}]  CLUSTERED-by-model 95%CI[{cslo:.3f},{cshi:.3f}]")
    json.dump([{"model": s_, "domain": d_, "params": p_, "acc": a_, "I": i_, "dG_hold": g_}
               for s_, d_, p_, a_, i_, g_ in pts],
              open(os.path.join(HERE, "results", "r1_points.json"), "w"), indent=2)
    return pts


def R2_v2():
    print("\nR2-v2 — the Second Law generalizes: over-confidence dissipates in every domain")
    all_ok = True
    print(f"     {'domain':8} {'model':9} {'G_cal':>8} {'G_over':>8} {'dissip':>8}")
    for domain in D.DOMAINS:
        r, classes = marginal(domain); ylab = classes + ["?"]
        dom_min = 1e9
        for short, params in present_models(domain):
            run = load_run(short, domain)
            fit, hold = split(domain, 7)
            C_fit = confusion(run, classes, ylab, fit)
            post_cal = calib(C_fit)
            post_over = np.full((len(classes), len(ylab)), 1e-9)
            for y in range(len(ylab)):
                post_over[np.argmax(C_fit[:, y]), y] = 1.0
            post_over /= post_over.sum(axis=0, keepdims=True)
            gc = float(np.mean(list(per_item_value(run, post_cal, classes, ylab, hold, r).values())))
            go = float(np.mean(list(per_item_value(run, post_over, classes, ylab, hold, r).values())))
            dom_min = min(dom_min, gc - go)
            print(f"     {domain:8} {short:9} {gc:8.4f} {go:8.4f} {gc-go:8.4f}")
        ok = dom_min > 0; all_ok &= ok
        print(f"        -> min dissipation in {domain}: {dom_min:+.4f} ({'>0 ok' if ok else 'FAIL'})")
    rec("R2-v2 over-confidence dissipation > 0 in EVERY domain", all_ok, "")


def main():
    print("=" * 84)
    print("v2 EMPIRICS — scored against PREREGISTRATION.md (nats; 95% CIs)")
    for domain in D.DOMAINS:
        ms = present_models(domain)
        print(f"  {domain}: {len(ms)} models, n={D.load(domain)['n']}, K={D.load(domain)['K']}")
    print("=" * 84)
    R1_v2()
    R2_v2()
    # R5 + ceiling appended by fleet_r5.py (kept separate for readability)
    try:
        import fleet_r5
        fleet_r5.run(rec)
    except Exception as e:
        print("fleet_r5 not run:", e)
    print("\n" + "=" * 84)
    npass = sum(1 for _, ok, _ in results if ok is True)
    nfail = sum(1 for _, ok, _ in results if ok is False)
    print(f"SUMMARY: {npass} PASS, {nfail} FAIL, {len(results)-npass-nfail} info")
    for n, ok, _ in results:
        print(f"  {'PASS' if ok is True else 'FAIL' if ok is False else '----'}  {n}")
    print("=" * 84)
    json.dump([{"name": n, "verdict": ("PASS" if ok is True else "FAIL" if ok is False else "INFO"),
                "detail": d} for n, ok, d in results],
              open(os.path.join(HERE, "results", "verdicts.json"), "w"), indent=2)

if __name__ == "__main__":
    main()

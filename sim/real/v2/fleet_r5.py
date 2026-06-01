"""
fleet_r5.py — Axis C headline: the heterogeneous, cost-constrained fleet.

The fleet is naturally SPECIALIZED: different models lead on different domains, so on a
mixed multi-domain query stream their per-item errors are far less correlated than v1's
same-task generalists (verified). Under a compute budget we race routing policies on
realized task-value per unit cost (tokens primary, latency secondary):

  round-robin, equal-weight pool, best-single, value-price (∝ I_a(domain)/cost_a),
  hand-tuned (best fit-accuracy per domain — the strong cost-blind adversary),
  hand-tuned-cost-aware (best fit-accuracy/cost per domain — an even stronger adversary).

Pre-registered: value-price must beat round-robin AND equal-weight (required);
beating hand-tuned is the strong win. Reported honestly with paired-bootstrap CIs.
"""
from __future__ import annotations
import json, os
import numpy as np
import experiments_v2 as E
import datasets as D
import value_sim as v

HERE = os.path.dirname(os.path.abspath(__file__))
RNG = np.random.default_rng(7)
N_BOOT = 2000

def _prep(seed):
    """Per (domain,model): holdout per-item value, costs, fit accuracy, fit I."""
    info = {}
    fleet = None
    for domain in D.DOMAINS:
        r, classes = E.marginal(domain); ylab = classes + ["?"]
        fit, hold = E.split(domain, seed)
        models = E.present_models(domain)
        if fleet is None:
            fleet = [m for m, _ in models]
        for short, params in models:
            run = E.load_run(short, domain)
            post = E.calib(E.confusion(run, classes, ylab, fit))
            vals = E.per_item_value(run, post, classes, ylab, hold, r)
            tok = E.mean_tokens(run)
            info[(domain, short)] = {
                "vals": vals,                      # id -> realized value (nats)
                "cost_tok": tok,
                "cost_lat": E.mean_latency(run),
                # Principled, HARDWARE-INDEPENDENT compute proxy (post-hoc sensitivity
                # analysis, cache-only): a dense forward pass costs ~2·params·tokens
                # FLOPs, so active-params(B) × tokens is ∝ FLOPs ∝ energy. This answers
                # the "you picked the cost metric that won" objection — latency is
                # hardware/scheduling-dependent; FLOPs are not.
                "cost_compute": params * tok,
                "acc_fit": E.accuracy(run, fit),
                "I_fit": v.mutual_information(E.confusion(run, classes, ylab, fit)),
                "post": post, "classes": classes, "ylab": ylab, "r": r, "run": run,
            }
    # the mixed holdout stream: (domain, id)
    stream = []
    for domain in D.DOMAINS:
        _, hold = E.split(domain, seed)
        stream += [(domain, i) for i in sorted(hold)]
    return info, fleet, stream

def _policy_arrays(info, fleet, stream, cost_key):
    """For each policy -> (value[], cost[]) over the stream (paired)."""
    pol = {p: ([], []) for p in ["round_robin", "equal_pool", "best_single",
                                  "value_price", "hand_tuned", "hand_cost"]}
    # global best-single by mean fit accuracy across domains
    acc_overall = {m: np.mean([info[(d, m)]["acc_fit"] for d in D.DOMAINS if (d, m) in info]) for m in fleet}
    best_overall = max(fleet, key=lambda m: acc_overall[m])
    rr_i = 0
    for (domain, iid) in stream:
        avail = [m for m in fleet if (domain, m) in info and iid in info[(domain, m)]["vals"]]
        if not avail:
            continue
        def val(m): return info[(domain, m)]["vals"][iid]
        def cost(m): return info[(domain, m)][cost_key]
        # round-robin
        m = avail[rr_i % len(avail)]; rr_i += 1
        pol["round_robin"][0].append(val(m)); pol["round_robin"][1].append(cost(m))
        # equal-weight pool: average posteriors of all avail models for this item
        r = info[(domain, avail[0])]["r"]; classes = info[(domain, avail[0])]["classes"]
        ylab = info[(domain, avail[0])]["ylab"]; idx = {c: i for i, c in enumerate(classes)}
        yidx = {y: i for i, y in enumerate(ylab)}
        ppool = np.zeros(len(classes))
        for mm in avail:
            o = info[(domain, mm)]["run"][str(iid)]
            ppool += info[(domain, mm)]["post"][:, yidx[o["pred"]]]
        ppool /= len(avail)
        xg = idx[info[(domain, avail[0])]["run"][str(iid)]["gold"]]
        pol["equal_pool"][0].append(float(np.log(ppool[xg] / r[xg])))
        pol["equal_pool"][1].append(sum(cost(mm) for mm in avail))
        # best-single (global)
        bm = best_overall if best_overall in avail else max(avail, key=lambda m: acc_overall[m])
        pol["best_single"][0].append(val(bm)); pol["best_single"][1].append(cost(bm))
        # value-price: argmax I_a(domain)/cost_a
        vp = max(avail, key=lambda m: info[(domain, m)]["I_fit"] / max(cost(m), 1e-9))
        pol["value_price"][0].append(val(vp)); pol["value_price"][1].append(cost(vp))
        # hand-tuned: argmax fit accuracy in domain (cost-blind)
        ht = max(avail, key=lambda m: info[(domain, m)]["acc_fit"])
        pol["hand_tuned"][0].append(val(ht)); pol["hand_tuned"][1].append(cost(ht))
        # hand-tuned cost-aware: argmax fit accuracy / cost
        hc = max(avail, key=lambda m: info[(domain, m)]["acc_fit"] / max(cost(m), 1e-9))
        pol["hand_cost"][0].append(val(hc)); pol["hand_cost"][1].append(cost(hc))
    return {k: (np.array(a), np.array(b)) for k, (a, b) in pol.items()}

def _vpc(arr):  # value per unit cost
    v_, c_ = arr
    return float(v_.sum() / c_.sum()) if c_.sum() else float("nan")

def error_correlation(info, fleet, stream):
    """Mean pairwise per-item error agreement on the stream (lower = more diverse)."""
    err = {}
    for (domain, iid) in stream:
        for m in fleet:
            if (domain, m) in info and str(iid) in info[(domain, m)]["run"]:
                o = info[(domain, m)]["run"][str(iid)]
                err.setdefault(m, {})[(domain, iid)] = int(o["pred"] != o["gold"])
    keys = [k for k in fleet if k in err]
    agrees = []
    for i in range(len(keys)):
        for j in range(i+1, len(keys)):
            a, b = err[keys[i]], err[keys[j]]
            common = set(a) & set(b)
            if common:
                agrees.append(np.mean([a[c] == b[c] for c in common]))
    return float(np.mean(agrees)) if agrees else float("nan")

def run(rec):
    print("\nFleet-R5 — heterogeneous, cost-constrained routing (THE headline)")
    info, fleet, stream = _prep(seed=7)
    print(f"     fleet = {fleet}  (specialists by domain competence)")
    print(f"     mixed holdout stream: {len(stream)} queries across {len(D.DOMAINS)} domains")
    ec = error_correlation(info, fleet, stream)
    print(f"     mean pairwise error-agreement = {ec:.3f} (diversity metric; lower = less correlated errors)")

    for cost_key, unit, scale in [("cost_tok", "per-1k-tokens", 1000), ("cost_lat", "per-10s-latency", 10),
                                  ("cost_compute", "per-compute (params×tok, FLOP-proxy)", 1000)]:
        pol = _policy_arrays(info, fleet, stream, cost_key)
        vpc = {k: _vpc(a) * scale for k, a in pol.items()}
        print(f"\n     value {unit} (cost = {cost_key}):")
        for k in ["round_robin", "equal_pool", "best_single", "hand_tuned", "hand_cost", "value_price"]:
            print(f"       {k:14} {vpc[k]:+.4f}")
        # paired bootstrap CIs of differences
        def diff_ci(pa, pb):
            va, ca = pol[pa]; vb, cb = pol[pb]; n = len(va)
            ds = []
            for _ in range(N_BOOT):
                idx = RNG.integers(0, n, n)
                da = va[idx].sum()/ca[idx].sum(); db = vb[idx].sum()/cb[idx].sum()
                ds.append((da - db) * scale)
            return float(np.mean(ds)), float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))
        tag = f"[{unit}]"
        # REQUIRED: value-price must beat round-robin AND equal-weight (CI excludes 0).
        # STRONG: beating the hand-tuned adversary is a real PASS/FAIL — a CI that
        # overlaps 0 is an honest tie/loss, NOT rounded up to a win (Flag #3). best_single
        # and hand_cost are reported informationally with CIs.
        kinds = {"round_robin": "REQUIRED", "equal_pool": "REQUIRED", "hand_tuned": "STRONG",
                 "best_single": "info", "hand_cost": "info"}
        for adv in ["round_robin", "equal_pool", "best_single", "hand_tuned", "hand_cost"]:
            m, lo, hi = diff_ci("value_price", adv)
            kind = kinds[adv]
            verdict = None if kind == "info" else (lo > 0)   # strict: CI must exclude 0
            note = "" if (verdict is None or lo > 0) else "  (CI overlaps 0 → honest tie/loss)"
            rec(f"R5 {tag} value-price > {adv} ({kind})",
                verdict, f"Δ={m:+.4f} 95%CI[{lo:+.4f},{hi:+.4f}]{note}")
    _ceiling(info, fleet, rec)
    # dump
    json.dump({"fleet": fleet, "n_stream": len(stream), "error_agreement": ec},
              open(os.path.join(HERE, "results", "fleet_r5.json"), "w"), indent=2)

def _ceiling(info, fleet, rec):
    print("\n     Ceiling & diversity (R4 at scale):")
    all_le = True; lifts = []
    for domain in D.DOMAINS:
        r, classes = E.marginal(domain); ylab = classes + ["?"]; Hx = v.entropy(r)
        idx = {c: i for i, c in enumerate(classes)}; yidx = {y: i for i, y in enumerate(ylab)}
        runs = {m: E.load_run(m, domain) for m, _ in E.present_models(domain)}
        singles = {m: v.mutual_information(E.confusion(runs[m], classes, ylab)) for m in runs}
        ny = len(ylab); best = None
        ms = list(runs)
        for i in range(len(ms)):
            for j in range(i+1, len(ms)):
                a, b = runs[ms[i]], runs[ms[j]]
                C = np.zeros((len(classes), ny*ny))
                for sid in a:
                    if sid in b:
                        x = idx[a[sid]["gold"]]; C[x, yidx[a[sid]["pred"]]*ny + yidx[b[sid]["pred"]]] += 1
                Iab = v.mutual_information(C)
                if Iab > Hx + 1e-6:
                    all_le = False
                lift = Iab - max(singles[ms[i]], singles[ms[j]])
                if best is None or Iab > best[1]:
                    best = (f"{ms[i]}+{ms[j]}", Iab, lift)
        if best is None:
            print(f"       {domain}: H(X)={Hx:.3f}  (<2 models — skipped)")
            continue
        lifts.append(best[2])
        print(f"       {domain}: H(X)={Hx:.3f}  best pair {best[0]} joint I={best[1]:.3f} "
              f"(lift +{best[2]:.3f}); all pairs ≤ H(X): {all_le}")
    rec("Ceiling: all pairwise joint I ≤ H(X)", all_le, "data-processing bound holds empirically")
    rec("Diversity: best diverse pair lifts joint I over best single (every domain)",
        all(l > 1e-3 for l in lifts), f"lifts={[round(x,3) for x in lifts]}")

"""
analyze_stage2.py — apply the FROZEN Stage-2 bands (PREREGISTRATION.md §4–§5, as
amended by amendments 1–2) to the saved reports. Cache-only; calls no models.

Part A (P1–P4): exact enumeration over structure atoms with the ELICITED posteriors.
Part B (P5–P6): the Stage-1 conventions verbatim + the doc-18 uniformity clause.
Assembles the three-outcome verdict. Writes results/stage2_analysis.json.

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "field", "real"))
from stage2a import make_structures, coalition_cells, exact_I, true_posterior  # noqa
from analyze_stage1 import fit_pq                                              # noqa

A_PATH = os.path.join(HERE, "results", "stage2a_reports.json")
B_PATH = os.path.join(HERE, "results", "stage2b_raw.json")
OUT = os.path.join(HERE, "results", "stage2_analysis.json")

LN2 = float(np.log(2))
H8 = 3 * LN2
RNG = np.random.default_rng(31)

# frozen bands (§4)
P1_TOL, P2_MARGIN, P2E_GAP, P3_SLACK = 0.05, -0.03, LN2 / 2, 0.02
P4_ORDER_REQ, P4_CLONE_GAP = 4, 0.10
P_BAND, Q_BAND, R2_MIN, RATIO_BAND = (0.6, 1.4), (-1.4, -0.6), 0.70, (0.33, 3.0)
MIN_INREGIME, MIN_SPAN = 6, 4.0
# frozen 2B constants (Stage-1 verbatim)
K, K_G, V_UNIF = 16, 12, 21.25
GS, GAMMAS = [0.25, 0.7, 2.0], [2.0, 6.0, 18.0]
B_POINTS, B_DELTA = [("B1", 6.0, 0.7), ("B2", 18.0, 0.7)], 0.5

CHECKS = []
def chk(name, ok, detail):
    CHECKS.append({"name": name, "pass": bool(ok), "detail": detail})
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


# ══════════════════════════════════════════════════════════════════ Part A
def rep_post(reports, name, Sset, y_S, n):
    key = f"{name}|{Sset}|{y_S}"
    r = reports.get(key)
    if r is None:
        return None, 0
    return np.clip(np.array(r["posterior"]), 1e-12, None), r["n_good"]

def q_of(st):
    return np.full(st["n"], 1 / st["n"])

def G_S_coalition(st, reports, name, Sset):
    """Ĝ_S from coalition-level elicited posteriors, exact enumeration."""
    q = q_of(st); tot, gate_ok = 0.0, True
    cells = coalition_cells(st, Sset)
    for y_S, py in cells.items():
        p_hat, n_good = rep_post(reports, name, tuple(Sset), tuple(y_S), st["n"])
        if p_hat is None or n_good < 6:
            gate_ok = False
            p_hat = q
        p_hat = p_hat / p_hat.sum()
        # E over true joint restricted to this cell
        for p, x, ys in st["atoms"]:
            if tuple(ys[a] for a in Sset) == tuple(y_S):
                tot += p * np.log(p_hat[x] / q[x])
    return tot, gate_ok

def G_S_product(st, reports, name, Sset):
    """Secondary diagnostic: naive-Bayes product fusion of INDIVIDUAL reports."""
    q = q_of(st); tot = 0.0
    for p, x, ys in st["atoms"]:
        log_odds = np.log(q)
        for a in Sset:
            p_a, _ = rep_post(reports, name, (a,), (ys[a],), st["n"])
            p_a = (p_a if p_a is not None else q)
            log_odds = log_odds + np.log(p_a / q)
        fused = np.exp(log_odds - log_odds.max()); fused /= fused.sum()
        tot += p * np.log(max(fused[x], 1e-12) / q[x])
    return tot

def part_A(rep):
    reports = rep["elicitation"]
    structures = make_structures()
    out = {"G_coalition": {}, "G_product": {}, "I_exact": {}, "Ihat": {},
           "elic_gate_fail": [], "protocol_capped_structures": []}

    # A3.1: ENFORCE the §5 elicitation gate — a structure with any <6/12 cell is
    # protocol-CAP'd for this pass (reported, not fitted).
    capped = set()
    for key, v in reports.items():
        if v["n_good"] < 6:
            out["elic_gate_fail"].append(key)
            capped.add(key.split("|")[0])
    out["protocol_capped_structures"] = sorted(capped)
    if capped:
        print(f"  [gate] protocol-CAP'd structures (cells <6/12): {sorted(capped)}")

    # per-structure quantities
    for name, st in structures.items():
        if name in capped:
            continue
        q = q_of(st)
        for size in range(1, st["m"] + 1):
            for Sset in itertools.combinations(range(st["m"]), size):
                G, ok = G_S_coalition(st, reports, name, Sset)
                out["G_coalition"][f"{name}|{Sset}"] = G
                out["G_product"][f"{name}|{Sset}"] = G_S_product(st, reports, name, Sset)
                out["I_exact"][f"{name}|{Sset}"] = exact_I(st, Sset)
                if not ok:
                    out["elic_gate_fail"].append(f"{name}|{Sset}")
        # Î_a (claimed information: KL under the reported measure), per agent
        for a in range(st["m"]):
            ih = 0.0
            for y_S, py in coalition_cells(st, (a,)).items():
                p_hat, _ = rep_post(reports, name, (a,), tuple(y_S), st["n"])
                p_hat = (p_hat if p_hat is not None else q); p_hat = p_hat / p_hat.sum()
                ih += py * float(np.sum(p_hat * np.log(p_hat / q)))
            out["Ihat"][f"{name}|{a}"] = ih

    # P1 gap law — equal-weight parimutuel with individual reports, (a)–(d)
    worst_gap, gaps = 0.0, {}
    p1_names = [n for n in ["a_disjoint", "b_overlap", "c_clones", "d_noisy"]
                if n not in capped]
    for name in p1_names:
        st = structures[name]; q = q_of(st); m = st["m"]
        G = np.zeros(m)
        for p, x, ys in st["atoms"]:
            b = np.zeros((m, st["n"]))
            for a in range(m):
                p_a, _ = rep_post(reports, name, (a,), (ys[a],), st["n"])
                p_a = (p_a if p_a is not None else q)
                b[a] = p_a / p_a.sum()
            B = b.mean(axis=0)
            for a in range(m):
                G[a] += p * np.log(max(b[a, x], 1e-12) / max(B[x], 1e-12))
        for a in range(m):
            for c in range(a + 1, m):
                dev = abs((G[a] - G[c]) -
                          (out["Ihat"][f"{name}|{a}"] - out["Ihat"][f"{name}|{c}"]))
                gaps[f"{name}|{a}{c}"] = dev
                worst_gap = max(worst_gap, dev)
    out["P1_worst_gap"] = worst_gap
    chk(f"P1 gap law |ΔĜ − ΔÎ| ≤ 0.05 (pairs, {p1_names})", worst_gap <= P1_TOL,
        f"worst = {worst_gap:.4f} nats" +
        (f" [protocol-CAP'd: {sorted(capped)}]" if capped else ""))

    # P2 submodularity (coalition-level Ĝ_S) + the (e) control
    worst_margin = 1e9
    for name in p1_names:
        m = structures[name]["m"]
        Gd = {S: out["G_coalition"][f"{name}|{S}"]
              for size in range(1, m + 1) for S in itertools.combinations(range(m), size)}
        Gd[()] = 0.0
        for S in list(Gd):
            for T in list(Gd):
                if set(S) <= set(T):
                    for a in range(m):
                        if a not in T:
                            mS = Gd[tuple(sorted(set(S) | {a}))] - Gd[S]
                            mT = Gd[tuple(sorted(set(T) | {a}))] - Gd[T]
                            worst_margin = min(worst_margin, mS - mT)
    out["P2_worst_margin"] = worst_margin
    chk(f"P2 submodularity margins ≥ −0.03 ({p1_names})", worst_margin >= P2_MARGIN,
        f"worst margin = {worst_margin:.4f}")
    if "e_xor" in capped:
        chk("P2e XOR control (protocol-CAP'd this pass)", False, "gate-excluded")
    else:
        ge = {S: out["G_coalition"][f"e_xor|{S}"] for S in [(0,), (1,), (0, 1)]}
        e_gap = (ge[(0, 1)] - ge[(0,)]) - (ge[(1,)] - 0.0)
        out["P2e_gap"] = e_gap
        chk("P2e XOR control supermodular gap ≥ ln2/2", e_gap >= P2E_GAP,
            f"gap = {e_gap:.4f} (ln2 = {LN2:.4f})")

    # P3 ceiling
    worst_ceil = -1e9
    for key, G in out["G_coalition"].items():
        H = H8 if not key.startswith("e_xor") else LN2
        worst_ceil = max(worst_ceil, G - H)
    out["P3_worst_over"] = worst_ceil
    chk("P3 joint ceiling Ĝ_S ≤ H(X) + 0.02", worst_ceil <= P3_SLACK,
        f"worst overage = {worst_ceil:.4f}")

    # P4 live market (A3.2 parse gate 0.90)
    mk = rep["market"]
    all_pr = [p for nm in mk for r in mk[nm] for p in r.get("parse_by_agent", [0.0])]
    mkt_parse = float(np.mean(all_pr)) if all_pr else 0.0
    out["market_parse"] = mkt_parse
    if mkt_parse < 0.90:
        chk("P4 market (protocol-CAP: parse < 0.90)", False,
            f"overall parse = {mkt_parse:.2f}")
    order_hits = sum(1 for r in mk["L_ladder"]
                     if r["final_wealth"][0] > r["final_wealth"][1] > r["final_wealth"][2])
    clone_ok_runs, clone_gaps = 0, []
    for r in mk["C_clones"]:
        w1, w2 = r["final_wealth"][0], r["final_wealth"][1]
        gap = abs(w1 - w2) / max((w1 + w2) / 2, 1e-9)
        clone_gaps.append(gap)
        clone_ok_runs += gap <= P4_CLONE_GAP
    out["P4"] = {"ladder_order_hits": order_hits, "clone_gaps": clone_gaps,
                 "market_parse": mkt_parse}
    if mkt_parse >= 0.90:
        chk("P4a ladder wealth ordered by Î (≥4/5 seeds)", order_hits >= P4_ORDER_REQ,
            f"{order_hits}/5 seeds ordered (parse {mkt_parse:.2f})")
        chk("P4b clone terminal-wealth gap ≤ 10% (≥4/5 seeds)", clone_ok_runs >= P4_ORDER_REQ,
            f"gaps = {[round(g,3) for g in clone_gaps]}")

    # secondary diagnostic: product fusion tracks (a)–(d), fails (e)
    non_e = [k for k in out["G_coalition"] if not k.startswith("e_xor")]
    if non_e:
        prod_dev = max(abs(out["G_product"][k] - out["G_coalition"][k]) for k in non_e)
        e_prod = out["G_product"].get("e_xor|(0, 1)")
        out["secondary_product_fusion"] = {
            "max_dev_ad": prod_dev, "e_pair_product_G": e_prod,
            "note": "diagnostic only (A2.1): expected small dev on (a)-(d), ~0 on (e)"}
        print(f"  [diag] product fusion: max|Δ| (fit structs) = {prod_dev:.4f}; "
              f"(e) pair Ĝ_product = {e_prod}")
    return out


# ══════════════════════════════════════════════════════════════════ Part B
def part_B(raw):
    grid = []
    print("\n2B grid (regime rule + uniformity clause):")
    for gamma in GAMMAS:
        for g in GS:
            runs = raw.get(f"A|gamma={gamma}|g={g}", [])
            if not runs:
                continue
            res = np.array([r["residual_ss"] for r in runs])
            s = {"gamma": gamma, "g": g, "n": len(runs),
                 "residual_mean": float(res.mean()),
                 "residual_std": float(res.std(ddof=1)),
                 "V_mean": float(np.mean([r["V_ss"] for r in runs])),
                 "k_bar": float(np.mean([r["k_bar_ss"] for r in runs])),
                 "above": float(np.mean([r["frac_above_peak"] for r in runs])),
                 "parse_min": float(min(r["parse_rate"] for r in runs))}
            s["predicted"] = s["V_mean"] * g / gamma
            s["ratio"] = s["residual_mean"] / s["predicted"] if s["predicted"] > 0 else np.nan
            fails = []
            if s["V_mean"] < 0.25 * V_UNIF: fails.append("V collapsed")
            if s["k_bar"] > K_G - 2: fails.append("k̄ at peak")
            if s["above"] > 0.20: fails.append("above-peak>0.2")
            if s["parse_min"] < 0.90: fails.append("parse")
            if s["residual_mean"] <= 0: fails.append("residual≤0")
            s["non_responsive"] = (abs(s["V_mean"] - V_UNIF) <= 0.25 * V_UNIF
                                   and abs(s["k_bar"] - 7.5) <= 1.0)
            s["in_regime"] = not fails
            s["regime_fails"] = fails
            grid.append(s)
            tag = ("NON-RESPONSIVE" if s["non_responsive"] else
                   ("in-regime" if s["in_regime"] else f"excl({','.join(fails)})"))
            print(f"  γ={gamma:5.1f} g={g:4.2f}: res={s['residual_mean']:6.3f}"
                  f"±{s['residual_std']:.3f} V={s['V_mean']:5.2f} k̄={s['k_bar']:5.2f} "
                  f"pred={s['predicted']:5.2f} [{tag}]")

    inreg = [c for c in grid if c["in_regime"]]
    nonresp = sum(1 for c in grid if c["non_responsive"])
    out = {"grid": grid, "n_in_regime": len(inreg), "n_non_responsive": nonresp}

    sigma_in = float(np.median([c["residual_std"] for c in inreg])) if inreg else np.nan
    r_across = (max(c["residual_mean"] for c in inreg) -
                min(c["residual_mean"] for c in inreg)) if inreg else 0.0
    preds = [c["predicted"] for c in inreg]
    span = max(preds) / max(min(preds), 1e-9) if preds else 0
    gate = bool(inreg) and r_across > 3 * sigma_in
    out["signal"] = {"sigma_in": sigma_in, "R_across": r_across, "span": span,
                     "gate": gate}

    p5 = {"outcome": None}
    if len(inreg) < MIN_INREGIME or span < MIN_SPAN:
        p5["outcome"] = "CAP"
        p5["reason"] = (f"insufficient in-regime span: {len(inreg)} conds, {span:.1f}x"
                        + (f"; {nonresp}/9 non-responsive" if nonresp else ""))
    else:
        p, q, lnC, r2 = fit_pq(inreg)
        boots = []
        for _ in range(2000):
            bc = []
            ok = True
            for c in inreg:
                runs = raw[f"A|gamma={c['gamma']}|g={c['g']}"]
                pick = [runs[i]["residual_ss"]
                        for i in RNG.integers(0, len(runs), len(runs))]
                m = float(np.mean(pick))
                if m <= 0: ok = False; break
                bc.append({"gamma": c["gamma"], "g": c["g"], "residual_mean": m})
            if ok:
                bp, bq, *_ = fit_pq(bc); boots.append((bp, bq))
        boots = np.array(boots)
        p_ci = [float(np.percentile(boots[:, 0], 2.5)), float(np.percentile(boots[:, 0], 97.5))]
        q_ci = [float(np.percentile(boots[:, 1], 2.5)), float(np.percentile(boots[:, 1], 97.5))]
        mean_ratio = float(np.mean([c["ratio"] for c in inreg]))
        loo = np.array([fit_pq([c for j, c in enumerate(inreg) if j != i])[:2]
                        for i in range(len(inreg))])
        loo_stable = (loo[:, 0].ptp() < 0.5 and loo[:, 1].ptp() < 0.5)
        p5.update({"p": p, "q": q, "R2": r2, "p_ci": p_ci, "q_ci": q_ci,
                   "mean_ratio": mean_ratio, "loo_stable": bool(loo_stable)})
        in_p = P_BAND[0] <= p <= P_BAND[1]; in_q = Q_BAND[0] <= q <= Q_BAND[1]
        ci_out = (p_ci[1] < P_BAND[0] or p_ci[0] > P_BAND[1] or
                  q_ci[1] < Q_BAND[0] or q_ci[0] > Q_BAND[1])
        if gate and r2 >= R2_MIN and in_p and in_q and RATIO_BAND[0] <= mean_ratio <= RATIO_BAND[1]:
            p5["outcome"] = "CONFIRM"
        elif gate and r2 >= R2_MIN and loo_stable and ci_out:
            p5["outcome"] = "FALSIFY"
        else:
            p5["outcome"] = "CAP"
            p5["reason"] = "gates not jointly met (see values)"
        print(f"\n  P5 fit: residual ∝ g^{p:.3f} γ^{q:.3f} R²={r2:.3f} "
              f"CIs p{p_ci} q{q_ci} ratio={mean_ratio:.2f}")
    out["P5"] = p5
    chk(f"P5 exponents (outcome)", p5["outcome"] == "CONFIRM", p5["outcome"] +
        (f" — {p5.get('reason','')}" if p5["outcome"] != "CONFIRM" else ""))

    # P6 direction
    p6 = {"points": []}
    floor = sigma_in * np.sqrt(2 / 8) if np.isfinite(sigma_in) else np.nan
    for bid, gamma, g in B_POINTS:
        r0r = raw.get(f"A|gamma={gamma}|g={g}", [])
        rga = raw.get(f"{bid}_dgamma|gamma={gamma + B_DELTA}|g={g}", [])
        rgg = raw.get(f"{bid}_dg|gamma={gamma}|g={g - B_DELTA}", [])
        if not (r0r and rga and rgg):
            continue
        r0 = float(np.mean([r["residual_ss"] for r in r0r]))
        eg = (r0 - float(np.mean([r["residual_ss"] for r in rga]))) / B_DELTA
        egg = (r0 - float(np.mean([r["residual_ss"] for r in rgg]))) / B_DELTA
        sig = (abs(eg) * B_DELTA > floor and abs(egg) * B_DELTA > floor)
        ratio = egg / eg if abs(eg) > 1e-9 else float("inf")
        p6["points"].append({"id": bid, "eff_gamma": eg, "eff_g": egg,
                             "ratio": ratio, "resolvable": bool(sig)})
        print(f"  P6 {bid}: eff_γ={eg:+.3f} eff_g={egg:+.3f} ratio={ratio:.2f} "
              f"{'resolvable' if sig else 'below floor'}")
    pts = p6["points"]
    if len(pts) == 2 and all(x["resolvable"] for x in pts) and all(x["ratio"] > 1 for x in pts):
        p6["verdict"] = "CONFIRMED"
    elif pts and pts[0]["resolvable"] and pts[0]["ratio"] < 1:
        p6["verdict"] = "FALSIFIED"
    else:
        p6["verdict"] = "INCONCLUSIVE"
    out["P6"] = p6
    chk("P6 direction (verdict)", p6.get("verdict") == "CONFIRMED", p6.get("verdict", "n/a"))
    return out


def main():
    out = {}
    print("=" * 76)
    print("STAGE-2 ANALYSIS — frozen bands of PREREGISTRATION.md (+ amendments 1–2)")
    print("=" * 76)
    if os.path.exists(A_PATH):
        rep = json.load(open(A_PATH))
        out["tier_A"], out["model_A"] = rep["tier"], rep["model"]
        print(f"\nPart A (2A, tier={rep['tier']}):")
        out["A"] = part_A(rep)
    else:
        print("\n(2A reports missing — Part A skipped)")
    if os.path.exists(B_PATH):
        print("\nPart B (2B):")
        out["B"] = part_B(json.load(open(B_PATH)))
    else:
        print("\n(2B raw missing — Part B skipped)")

    out["checks"] = CHECKS
    n_pass = sum(1 for c in CHECKS if c["pass"])
    print("\n" + "=" * 76)
    print(f"STAGE 2: {n_pass}/{len(CHECKS)} frozen checks pass")
    # top-level decision per §4 (P1–P3 + P5 primary)
    names = {c["name"].split()[0]: c["pass"] for c in CHECKS}
    primary = all(names.get(k, False) for k in ["P1", "P2", "P2e", "P3"]) and \
              (out.get("B", {}).get("P5", {}).get("outcome") == "CONFIRM")
    out["primary_pass"] = bool(primary)
    with open(OUT, "w") as f:
        json.dump(out, f, indent=1)
    print(f"→ {OUT}")


if __name__ == "__main__":
    main()

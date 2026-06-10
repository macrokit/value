"""
analyze_stage1.py — apply the FROZEN Stage-1 decision rule (PREREGISTRATION_stage1.md
§2–§4) to results/stage1_raw.json. Cache-only; calls no models.

Outputs results/stage1_redo.json with:
  - per-condition means + regime flags (the §2 mechanical rule)
  - the free log-log exponent fit (p, q) with seed-bootstrap 95% CIs
  - the single-regressor fit vs ln(V·g/γ) and ratio stats (doc-13-comparable)
  - the signal gate (R_across vs 3·σ_in, raw-seed-std convention)
  - the scaling outcome: exactly one of CONFIRM / FALSIFY / CAP
  - the direction verdict: exactly one of CONFIRMED / FALSIFIED / INCONCLUSIVE

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_PATH = os.path.join(HERE, "results", "stage1_raw.json")
OUT_PATH = os.path.join(HERE, "results", "stage1_redo.json")

# frozen constants (§1–§4)
K, K_G, K_STAR = 16, 12, 0
V_UNIF = (K**2 - 1) / 12.0          # 21.25
V_MIN = 0.25 * V_UNIF               # 5.3125
KBAR_MAX = K_G - 2                  # 10
ABOVE_MAX = 0.20
PARSE_MIN = 0.90
GS = [0.25, 0.7, 2.0]
GAMMAS = [2.0, 6.0, 18.0]
B_POINTS = [("B1", 6.0, 0.7), ("B2", 18.0, 0.7)]
B_DELTA = 0.5
N_BOOT = 2000
P_BAND = (0.60, 1.40)
Q_BAND = (-1.40, -0.60)
R2_MIN = 0.70
RATIO_BAND = (0.33, 3.0)
MIN_INREGIME = 6
MIN_SPAN = 4.0
RNG = np.random.default_rng(11)


def cond_key(tag, gamma, g):
    return f"{tag}|gamma={gamma}|g={g}"


def cond_stats(runs):
    res = np.array([r["residual_ss"] for r in runs])
    return {
        "n_seeds": len(runs),
        "residual_mean": float(res.mean()),
        "residual_std": float(res.std(ddof=1)) if len(runs) > 1 else float("nan"),
        "V_mean": float(np.mean([r["V_ss"] for r in runs])),
        "k_bar_mean": float(np.mean([r["k_bar_ss"] for r in runs])),
        "above_peak_mean": float(np.mean([r["frac_above_peak"] for r in runs])),
        "parse_min": float(min(r["parse_rate"] for r in runs)),
    }


def regime_flags(s):
    """The §2 mechanical regime rule. Returns (in_regime, list-of-failed-clauses)."""
    fails = []
    if s["V_mean"] < V_MIN:
        fails.append(f"V_ss {s['V_mean']:.2f} < {V_MIN:.2f}")
    if s["k_bar_mean"] > KBAR_MAX:
        fails.append(f"k̄ {s['k_bar_mean']:.2f} > {KBAR_MAX}")
    if s["above_peak_mean"] > ABOVE_MAX:
        fails.append(f"above-peak {s['above_peak_mean']:.2f} > {ABOVE_MAX}")
    if s["parse_min"] < PARSE_MIN:
        fails.append(f"parse {s['parse_min']:.2f} < {PARSE_MIN}")
    if s["residual_mean"] <= 0:
        fails.append("residual ≤ 0")
    return (len(fails) == 0), fails


def fit_pq(conds):
    """OLS ln(res) = lnC + p ln g + q ln γ on condition means. Returns (p,q,lnC,R²)."""
    X = np.array([[1.0, np.log(c["g"]), np.log(c["gamma"])] for c in conds])
    y = np.array([np.log(c["residual_mean"]) for c in conds])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    yhat = X @ beta
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return float(beta[1]), float(beta[2]), float(beta[0]), r2


def main():
    with open(RAW_PATH) as f:
        raw = json.load(f)
    out = {"frozen": {"P_BAND": P_BAND, "Q_BAND": Q_BAND, "R2_MIN": R2_MIN,
                      "RATIO_BAND": RATIO_BAND, "V_MIN": V_MIN,
                      "signal_gate": "R_across > 3*sigma_in (raw seed std)"}}

    # ── per-condition stats + regime rule ────────────────────────────────────
    grid = []
    print("=" * 78)
    print("STAGE-1 ANALYSIS — frozen rule of PREREGISTRATION_stage1.md")
    print("=" * 78)
    print("\nA-grid condition means (regime rule applied):")
    for gamma in GAMMAS:
        for g in GS:
            runs = raw.get(cond_key("A", gamma, g), [])
            if not runs:
                print(f"  γ={gamma} g={g}: MISSING")
                continue
            s = cond_stats(runs)
            s["gamma"], s["g"] = gamma, g
            s["predicted"] = s["V_mean"] * g / gamma
            s["ratio"] = s["residual_mean"] / s["predicted"]
            s["in_regime"], s["regime_fails"] = regime_flags(s)
            grid.append(s)
            tag = "in-regime" if s["in_regime"] else f"EXCLUDED ({'; '.join(s['regime_fails'])})"
            print(f"  γ={gamma:5.1f} g={g:4.2f}: res={s['residual_mean']:6.3f}±{s['residual_std']:.3f} "
                  f"V={s['V_mean']:5.2f} k̄={s['k_bar_mean']:5.2f} above={s['above_peak_mean']:.2f} "
                  f"pred={s['predicted']:5.2f} ratio={s['ratio']:5.2f}  [{tag}]")
    out["grid"] = grid

    inreg = [c for c in grid if c["in_regime"]]
    n_in = len(inreg)
    preds = [c["predicted"] for c in inreg]
    span = (max(preds) / max(min(preds), 1e-9)) if preds else 0.0

    # ── signal gate ───────────────────────────────────────────────────────────
    sigma_in = float(np.median([c["residual_std"] for c in inreg])) if inreg else float("nan")
    r_across = (max(c["residual_mean"] for c in inreg) -
                min(c["residual_mean"] for c in inreg)) if inreg else 0.0
    gate_signal = r_across > 3 * sigma_in
    print(f"\nIn-regime: {n_in}/9 conditions; predicted span = {span:.1f}x "
          f"(need ≥{MIN_SPAN}x over ≥{MIN_INREGIME} conditions)")
    print(f"Signal gate: R_across={r_across:.3f} vs 3·σ_in={3*sigma_in:.3f} → "
          f"{'PASS' if gate_signal else 'FAIL'}")
    out["signal"] = {"sigma_in": sigma_in, "R_across": r_across, "pass": bool(gate_signal),
                     "n_in_regime": n_in, "span": span}

    scaling = None
    detail = {}
    if n_in < MIN_INREGIME or span < MIN_SPAN:
        scaling = "CAP"
        detail["cap_reason"] = (f"insufficient in-regime span: {n_in} conditions, "
                                f"{span:.1f}x (need ≥{MIN_INREGIME} and ≥{MIN_SPAN}x)")
    else:
        # ── primary fit + bootstrap ───────────────────────────────────────────
        p_hat, q_hat, lnC, r2 = fit_pq(inreg)
        # seed bootstrap: resample seeds per condition, recompute means, refit
        boots = []
        runs_by_cond = {(c["gamma"], c["g"]):
                        raw[cond_key("A", c["gamma"], c["g"])] for c in inreg}
        for _ in range(N_BOOT):
            bconds = []
            ok = True
            for c in inreg:
                runs = runs_by_cond[(c["gamma"], c["g"])]
                pick = [runs[i] for i in RNG.integers(0, len(runs), len(runs))]
                m = float(np.mean([r["residual_ss"] for r in pick]))
                if m <= 0:
                    ok = False
                    break
                bconds.append({"gamma": c["gamma"], "g": c["g"], "residual_mean": m})
            if ok:
                bp, bq, *_ = fit_pq(bconds)
                boots.append((bp, bq))
        boots = np.array(boots)
        p_ci = [float(np.percentile(boots[:, 0], 2.5)), float(np.percentile(boots[:, 0], 97.5))]
        q_ci = [float(np.percentile(boots[:, 1], 2.5)), float(np.percentile(boots[:, 1], 97.5))]

        # secondary: single-regressor vs ln(V g / γ) + ratios
        lx = np.array([np.log(c["predicted"]) for c in inreg])
        ly = np.array([np.log(c["residual_mean"]) for c in inreg])
        sl, ic = np.polyfit(lx, ly, 1)
        r2_single = 1 - np.sum((ly - (sl * lx + ic))**2) / np.sum((ly - ly.mean())**2)
        mean_ratio = float(np.mean([c["ratio"] for c in inreg]))

        # leave-one-out stability of the free fit
        loo = np.array([fit_pq([c for j, c in enumerate(inreg) if j != i])[:2]
                        for i in range(n_in)])
        loo_stable = (float(loo[:, 0].max() - loo[:, 0].min()) < 0.5 and
                      float(loo[:, 1].max() - loo[:, 1].min()) < 0.5 and
                      (np.all(np.sign(loo[:, 1]) == np.sign(loo[0, 1])) if q_hat != 0 else True))

        print(f"\nFree fit: residual ∝ g^{p_hat:.3f} γ^{q_hat:.3f}  R²={r2:.3f}")
        print(f"  bootstrap 95% CIs: p ∈ [{p_ci[0]:.3f}, {p_ci[1]:.3f}], "
              f"q ∈ [{q_ci[0]:.3f}, {q_ci[1]:.3f}]  (theorem: p=+1, q=−1)")
        print(f"  single-regressor vs V·g/γ: slope={sl:.3f} R²={r2_single:.3f}; "
              f"mean ratio={mean_ratio:.3f}")
        print(f"  leave-one-out stable: {loo_stable}")
        detail = {"p": p_hat, "q": q_hat, "lnC": lnC, "R2": r2,
                  "p_ci": p_ci, "q_ci": q_ci,
                  "single_slope": float(sl), "single_R2": float(r2_single),
                  "mean_ratio": mean_ratio, "loo_stable": bool(loo_stable),
                  "loo_p_range": [float(loo[:, 0].min()), float(loo[:, 0].max())],
                  "loo_q_range": [float(loo[:, 1].min()), float(loo[:, 1].max())]}

        # ── decision rule (§3, in order) ──────────────────────────────────────
        in_p = P_BAND[0] <= p_hat <= P_BAND[1]
        in_q = Q_BAND[0] <= q_hat <= Q_BAND[1]
        in_ratio = RATIO_BAND[0] <= mean_ratio <= RATIO_BAND[1]
        p_ci_disjoint = p_ci[1] < P_BAND[0] or p_ci[0] > P_BAND[1]
        q_ci_disjoint = q_ci[1] < Q_BAND[0] or q_ci[0] > Q_BAND[1]

        if gate_signal and r2 >= R2_MIN and in_p and in_q and in_ratio:
            scaling = "CONFIRM"
        elif gate_signal and r2 >= R2_MIN and loo_stable and (p_ci_disjoint or q_ci_disjoint):
            scaling = "FALSIFY"
            detail["falsify_axis"] = ("p" if p_ci_disjoint else "") + \
                                     ("q" if q_ci_disjoint else "")
        else:
            scaling = "CAP"
            fails = []
            if not gate_signal: fails.append("signal gate")
            if r2 < R2_MIN: fails.append(f"R²={r2:.2f}<0.70")
            if not loo_stable: fails.append("LOO unstable")
            if not (p_ci_disjoint or q_ci_disjoint) and not (in_p and in_q):
                fails.append("exponents outside band but CIs overlap (underpowered)")
            if (in_p and in_q) and not in_ratio:
                fails.append(f"ratio {mean_ratio:.2f} outside {RATIO_BAND}")
            detail["cap_reason"] = "; ".join(fails) if fails else "rule fall-through"

    out["scaling"] = {"outcome": scaling, **detail}
    print(f"\nSCALING OUTCOME: {scaling}" +
          (f"  ({detail.get('cap_reason','')})" if scaling == "CAP" else ""))

    # ── direction test (§4) ───────────────────────────────────────────────────
    print("\nDirection test (δ=0.5):")
    sigma_floor = sigma_in * np.sqrt(2 / 8)
    dir_results = []
    for bid, gamma, g in B_POINTS:
        r0_runs = raw.get(cond_key("A", gamma, g), [])
        dgam_runs = raw.get(cond_key(f"{bid}_dgamma", gamma + B_DELTA, g), [])
        dg_runs = raw.get(cond_key(f"{bid}_dg", gamma, g - B_DELTA), [])
        if not (r0_runs and dgam_runs and dg_runs):
            print(f"  {bid}: MISSING runs")
            continue
        r0 = float(np.mean([r["residual_ss"] for r in r0_runs]))
        rg = float(np.mean([r["residual_ss"] for r in dgam_runs]))
        rgg = float(np.mean([r["residual_ss"] for r in dg_runs]))
        eff_gamma = (r0 - rg) / B_DELTA
        eff_g = (r0 - rgg) / B_DELTA
        sig_gamma, sig_g = abs(r0 - rg), abs(r0 - rgg)
        resolvable = sig_gamma > sigma_floor and sig_g > sigma_floor
        ratio = eff_g / eff_gamma if abs(eff_gamma) > 1e-9 else float("inf")
        dir_results.append({"id": bid, "gamma": gamma, "g": g, "r0": r0,
                            "eff_gamma": eff_gamma, "eff_g": eff_g, "ratio": ratio,
                            "sig_gamma": sig_gamma, "sig_g": sig_g,
                            "resolvable": bool(resolvable)})
        print(f"  {bid} (γ={gamma}, g={g}): r0={r0:.3f}  eff_γ={eff_gamma:+.3f} "
              f"eff_g={eff_g:+.3f}  ratio={ratio:.2f}  "
              f"signals=({sig_gamma:.3f},{sig_g:.3f}) vs floor {sigma_floor:.3f}  "
              f"{'resolvable' if resolvable else 'BELOW FLOOR'}")

    if len(dir_results) == 2 and all(d["resolvable"] for d in dir_results) \
            and all(d["ratio"] > 1 for d in dir_results):
        direction = "CONFIRMED"
    elif dir_results and dir_results[0]["resolvable"] and dir_results[0]["ratio"] < 1:
        direction = "FALSIFIED"
    else:
        direction = "INCONCLUSIVE"
    out["direction"] = {"verdict": direction, "floor": float(sigma_floor),
                        "points": dir_results}
    print(f"\nDIRECTION VERDICT: {direction}")

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n→ {OUT_PATH}")


if __name__ == "__main__":
    main()

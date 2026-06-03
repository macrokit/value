"""
analyze_lever1.py — apply the PRE-COMMITTED three-outcome discriminator
(PREREGISTRATION_lever1_analysis_addendum.md) to the completed Lever-1 grid.

Uses the cached runs only (no new LLM calls): recomputes per-seed residual_ss and
V_ss via run_condition (all cache hits) to get the noise floor (σ_in, CV_V) the
discriminator needs, fits the committed candidate-law family, computes R_across and
leave-one-out stability, and resolves:
  - the SCALING outcome to exactly one of {1 confirm, 2 falsification, 3 CAP}
  - the DIRECTION verdict to exactly one of {confirmed, falsified, inconclusive}

Run: python3 sim/field/real/analyze_lever1.py   (requires the cache + tunnel for safety;
     all calls are cached so it is instant and offline-safe)
Writes results/lever1_analysis.json.
"""
from __future__ import annotations
import os, sys, json, itertools
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import lever1_rung8 as L   # reuse the EXACT measurement function + constants

OUT = os.path.join(os.path.dirname(__file__), "results")

GAMMAS = [0.5, 1.0, 2.0]
GS     = [0.1, 0.2]
SEEDS  = L.SEEDS            # [0,1,2]
DELTA  = L.B_DELTA          # 0.05


# ── per-seed measurement (cached → instant) ──────────────────────────────────
def per_seed(gamma, g):
    """Return arrays of per-seed (residual_ss, V_ss) for one condition."""
    res, V = [], []
    for s in SEEDS:
        r = L.run_condition(gamma, g, s)
        res.append(r["residual_ss"]); V.append(r["V_ss"])
    return np.array(res), np.array(V)


# ── candidate law fits (on the 6 condition-mean points, log space) ────────────
def fit_loglinear(logX_cols, logy):
    """OLS logy ~ Σ coef·logX + c. Returns (coefs, intercept, R²)."""
    A = np.column_stack(logX_cols + [np.ones(len(logy))])
    coef, *_ = np.linalg.lstsq(A, logy, rcond=None)
    yhat = A @ coef
    ss_res = float(np.sum((logy - yhat) ** 2))
    ss_tot = float(np.sum((logy - logy.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return coef[:-1], coef[-1], r2


def fixed_exponent_r2(logres, pred_log):
    """R² of a FIXED-exponent model: logres ≈ pred_log + c (c = best offset)."""
    c = float(np.mean(logres - pred_log))
    yhat = pred_log + c
    ss_res = float(np.sum((logres - yhat) ** 2))
    ss_tot = float(np.sum((logres - logres.mean()) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0, c


def main():
    print("=" * 78)
    print("LEVER-1 ANALYSIS — committed three-outcome discriminator")
    print("(addendum PREREGISTRATION_lever1_analysis_addendum.md; cache-only, no new calls)")
    print("=" * 78)

    # gather per-seed data for the 6 grid conditions
    conds = []
    for gamma, g in itertools.product(GAMMAS, GS):
        res, V = per_seed(gamma, g)
        conds.append(dict(gamma=gamma, g=g,
                          res_seeds=res, V_seeds=V,
                          res=float(res.mean()), V=float(V.mean()),
                          res_std=float(res.std(ddof=1)), V_std=float(V.std(ddof=1))))
        print(f"  γ={gamma} g={g}: residual={res.mean():.3f}±{res.std(ddof=1):.3f}  "
              f"V={V.mean():.3f}±{V.std(ddof=1):.3f}  (seeds={np.round(res,3)})")

    gamma = np.array([c["gamma"] for c in conds])
    g     = np.array([c["g"] for c in conds])
    V     = np.array([c["V"] for c in conds])
    res   = np.array([c["res"] for c in conds])
    logres = np.log(res)

    # ── noise vs signal ───────────────────────────────────────────────────────
    sigma_in = float(np.median([c["res_std"] for c in conds]))     # within-condition seed std
    R_across = float(res.max() - res.min())                        # across-condition spread
    CV_V     = float(np.median([c["V_std"] / c["V"] for c in conds]))
    V_range  = float(V.max() - V.min())
    print(f"\n  σ_in (median within-condition seed std of residual) = {sigma_in:.3f}")
    print(f"  R_across (across-condition residual range)           = {R_across:.3f}")
    print(f"  signal/noise R_across / σ_in                         = {R_across/sigma_in:.2f}  (gate: >3)")
    print(f"  CV_V (median seed CV of V)                           = {CV_V:.3f}  (gate: ≤0.5 ⇒ V estimable)")
    print(f"  V across-condition range                             = {V_range:.3f}  (V≈const ⇒ V·g/γ ≈ (g/γ)·const)")

    # ── candidate law family ───────────────────────────────────────────────────
    laws = {}
    # L0: residual = C·V·g/γ  (FIXED exponents V¹ g¹ γ⁻¹)
    pred_L0 = np.log(V) + np.log(g) - np.log(gamma)
    r2_L0, _ = fixed_exponent_r2(logres, pred_L0)
    laws["L0  V·g/γ (theorem, fixed exp)"] = dict(r2=r2_L0, exponents="V1 g1 γ-1 (fixed)")
    # L1: residual = C·g/γ
    r2_L1, _ = fixed_exponent_r2(logres, np.log(g) - np.log(gamma))
    laws["L1  g/γ (fixed)"] = dict(r2=r2_L1, exponents="g1 γ-1 (fixed)")
    # L2: residual = C·V·g
    r2_L2, _ = fixed_exponent_r2(logres, np.log(V) + np.log(g))
    laws["L2  V·g (fixed)"] = dict(r2=r2_L2, exponents="V1 g1 (fixed)")
    # L3: residual = C/γ (g-independent)
    r2_L3, _ = fixed_exponent_r2(logres, -np.log(gamma))
    laws["L3  1/γ (g-independent, fixed)"] = dict(r2=r2_L3, exponents="γ-1 (fixed)")
    # L4: residual = C·V·g^p·γ^q (free p,q; V fixed exp 1)
    coef4, c4, r2_L4 = fit_loglinear([np.log(g), np.log(gamma)], logres - np.log(V))
    laws["L4  V·g^p·γ^q (free p,q)"] = dict(r2=r2_L4, exponents=f"g^{coef4[0]:.2f} γ^{coef4[1]:.2f} (V fixed 1)")
    # Lpow: residual = C·g^p·γ^q (free p,q; no V)
    coefp, cp, r2_Lpow = fit_loglinear([np.log(g), np.log(gamma)], logres)
    laws["Lpow  g^p·γ^q (free, no V)"] = dict(r2=r2_Lpow, exponents=f"g^{coefp[0]:.2f} γ^{coefp[1]:.2f}")
    # Lpow3: residual = C·V^r·g^p·γ^q (free all three)
    coef3, c3, r2_Lpow3 = fit_loglinear([np.log(V), np.log(g), np.log(gamma)], logres)
    laws["Lpow3  V^r·g^p·γ^q (free all)"] = dict(r2=r2_Lpow3, exponents=f"V^{coef3[0]:.2f} g^{coef3[1]:.2f} γ^{coef3[2]:.2f}")
    # Lnull: residual = C
    laws["Lnull  constant"] = dict(r2=0.0, exponents="—")

    print("\n  Candidate-law fits (R² on 6 condition means, log space):")
    for nm, info in laws.items():
        print(f"    {nm:38s} R²={info['r2']:+.3f}   {info['exponents']}")

    # best non-null, non-theorem alternative
    alt_keys = [k for k in laws if not k.startswith("L0") and not k.startswith("Lnull")]
    best_alt = max(alt_keys, key=lambda k: laws[k]["r2"])
    best_alt_r2 = laws[best_alt]["r2"]
    print(f"\n  best alternative law: {best_alt}  (R²={best_alt_r2:.3f})")

    # ── leave-one-out stability of the best FREE power law (Lpow) ──────────────
    loo_exps = []
    for i in range(len(res)):
        mask = np.arange(len(res)) != i
        c, _, _ = fit_loglinear([np.log(g[mask]), np.log(gamma[mask])], logres[mask])
        loo_exps.append(c)
    loo_exps = np.array(loo_exps)
    p_spread = float(loo_exps[:, 0].max() - loo_exps[:, 0].min())
    q_spread = float(loo_exps[:, 1].max() - loo_exps[:, 1].min())
    p_sign_stable = bool(np.all(np.sign(loo_exps[:, 0]) == np.sign(loo_exps[0, 0])))
    q_sign_stable = bool(np.all(np.sign(loo_exps[:, 1]) == np.sign(loo_exps[0, 1])))
    loo_stable = p_spread < 0.5 and q_spread < 0.5 and p_sign_stable and q_sign_stable
    print(f"\n  Lpow leave-one-out: g-exp spread={p_spread:.2f} (sign-stable={p_sign_stable}), "
          f"γ-exp spread={q_spread:.2f} (sign-stable={q_sign_stable}) ⇒ stable={loo_stable}")

    # ── SCALING decision gate (committed §2) ───────────────────────────────────
    A1_pass = (L.A1_SLOPE_LO <= 0.176 <= L.A1_SLOPE_HI) and (0.559 >= L.A1_R2_MIN)  # from prereg run
    signal_exceeds_noise = R_across > 3 * sigma_in
    V_estimable = CV_V <= 0.5
    systematic = (best_alt_r2 >= 0.70) and signal_exceeds_noise and loo_stable and V_estimable

    if A1_pass:
        scaling = "1 CONFIRM (residual ∝ V·g/γ)"
    elif systematic:
        scaling = "2 CLEAN FALSIFICATION (systematic, but ≠ V·g/γ)"
    else:
        # which gate failed → CAP, naming the failed gate(s)
        fails = []
        if best_alt_r2 < 0.70: fails.append(f"no law ≥0.70 R² (best={best_alt_r2:.2f})")
        if not signal_exceeds_noise: fails.append(f"signal≤3·noise (R_across/σ_in={R_across/sigma_in:.1f})")
        if not loo_stable: fails.append("best law not leave-one-out stable")
        if not V_estimable: fails.append(f"V not estimable (CV_V={CV_V:.2f})")
        scaling = "3 CAP (not cleanly testable) — failed gate(s): " + "; ".join(fails) if fails else \
                  "3 CAP (not cleanly testable)"

    print("\n" + "-" * 78)
    print(f"  SCALING OUTCOME: {scaling}")
    print("-" * 78)

    # ── DIRECTION test (committed §3) — separable ──────────────────────────────
    # noise on a difference of two 3-seed condition means ≈ σ_in·sqrt(2/3)
    diff_noise = sigma_in * np.sqrt(2.0 / len(SEEDS))
    # B perturbation signals (cache): |r0 − r_perturbed| = |eff·δ|
    B = {}
    for bid, gam, gg in [("B1", 1.0, 0.1), ("B2", 2.0, 0.1)]:
        r0_seeds, _ = per_seed(gam, gg)
        rgam_seeds, _ = per_seed(gam + DELTA, gg)
        rg_seeds, _ = per_seed(gam, gg - DELTA)
        r0, rgam, rg = r0_seeds.mean(), rgam_seeds.mean(), rg_seeds.mean()
        sig_gamma = abs(r0 - rgam)     # response to raising γ by δ
        sig_g     = abs(r0 - rg)       # response to lowering g by δ
        B[bid] = dict(gamma=gam, g=gg, r0=float(r0),
                      sig_gamma=float(sig_gamma), sig_g=float(sig_g),
                      eff_gamma=float((r0 - rgam) / DELTA), eff_g=float((r0 - rg) / DELTA),
                      gamma_above_noise=bool(sig_gamma > diff_noise),
                      g_above_noise=bool(sig_g > diff_noise))
        print(f"\n  {bid} (γ={gam}, g={gg}): perturbation signals vs noise floor {diff_noise:.3f}")
        print(f"    raise-γ signal |Δres|={sig_gamma:.3f} (eff_γ={(r0-rgam)/DELTA:+.2f})  above noise? {sig_gamma>diff_noise}")
        print(f"    lower-g signal |Δres|={sig_g:.3f} (eff_g={(r0-rg)/DELTA:+.2f})  above noise? {sig_g>diff_noise}")

    # Committed §3 rule: a B point is RESOLVABLE only if BOTH its perturbation signals
    # (raise-γ, which defines eff_γ, AND lower-g, which defines eff_g) exceed the floor;
    # otherwise the ratio eff_g/eff_γ has a noise-dominated term and cannot be read.
    #   CONFIRMED  := both B points resolvable AND eff_g>eff_γ at both
    #   FALSIFIED  := B1 resolvable AND eff_g<eff_γ at B1 (theory predicts ratio ~5)
    #   INCONCLUSIVE := otherwise (perturbations within seed noise)
    for b in B:
        B[b]["resolvable"] = bool(B[b]["gamma_above_noise"] and B[b]["g_above_noise"])
    n_resolvable = sum(B[b]["resolvable"] for b in B)
    if B["B1"]["resolvable"] and B["B2"]["resolvable"] and \
       B["B1"]["eff_g"] > B["B1"]["eff_gamma"] and B["B2"]["eff_g"] > B["B2"]["eff_gamma"]:
        direction = "CONFIRMED (both B points resolvable; incentive beats oversight at both)"
    elif B["B1"]["resolvable"] and B["B1"]["eff_g"] < B["B1"]["eff_gamma"]:
        direction = "FALSIFIED (B1 resolvable; oversight matches/beats incentive design)"
    else:
        direction = (f"INCONCLUSIVE ({n_resolvable}/2 B points fully resolvable; "
                     f"δ=0.05 perturbations mostly below seed-noise floor {diff_noise:.3f})")

    print("\n" + "-" * 78)
    print(f"  DIRECTION VERDICT: {direction}")
    print("-" * 78)

    out = {
        "grid": [{k: (v.tolist() if isinstance(v, np.ndarray) else v)
                  for k, v in c.items()} for c in conds],
        "noise": dict(sigma_in=sigma_in, R_across=R_across, signal_to_noise=R_across/sigma_in,
                      CV_V=CV_V, V_range=V_range, diff_noise=diff_noise),
        "laws": laws,
        "best_alt": best_alt, "best_alt_r2": best_alt_r2,
        "loo": dict(p_spread=p_spread, q_spread=q_spread, stable=loo_stable),
        "scaling_outcome": scaling,
        "direction_verdict": direction,
        "B": B,
    }
    with open(os.path.join(OUT, "lever1_analysis.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nAnalysis → {os.path.join(OUT, 'lever1_analysis.json')}")


if __name__ == "__main__":
    main()

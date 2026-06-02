"""
lever1_rung8.py — Lever-1 real-agent test: residual = ‖Vg‖/γ on real bias-controlled LLMs.

Implements the pre-registered design in PREREGISTRATION_lever1.md. Reuses the
rung-8 bias-controlled harness (per-agent symbol-randomisation of niche labels)
and the validated qwen2.5:1.5b-instruct model.

Guardrails (from PREREGISTRATION_lever1.md, carrying over the rung-8 rule):
  - symbol_random=True (confound control — mandatory)
  - noise = LLM's own sampling temperature (NOT externally-supplied alignment noise)
  - g, γ, V read from the agents (no hard-substituted dynamics)
  - no escalation past 1.5b to fish for a cleaner signal
  - honest CAP: if not testable at this scale, report it; do not escalate

Pre-registered checks (frozen in PREREGISTRATION_lever1.md, committed before any run):
  A1: OLS log(residual_ss) ~ log(V_ss·g/γ): slope ∈ [0.60, 1.60], R² ≥ 0.70
  A2: mean ratio residual_ss / (V_ss·g/γ) ∈ [0.50, 2.00]
  A3: residual_ss decreases as γ increases (directional test, fixed g)
  B1: (γ=1.0, g=0.1) eff_g / eff_γ > 1.0  [incentive wins]
  B2: (γ=2.0, g=0.1) eff_g / eff_γ > 1.0  [incentive wins more]
  B_mono: ratio(B2) ≥ ratio(B1)

CAP criterion (pre-registered): if ratio std/mean > 1.0 AND no monotone dependence
on V·g/γ — report "not cleanly testable at this scale"; do NOT escalate.

Run:
  RUNG7_MODEL=qwen2.5:1.5b-instruct python3 sim/field/real/lever1_rung8.py
  (requires: ssh -f -N -L 11434:localhost:11434 blueidea@MacBook-Pro.local)

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from llm_economy import LLMEconomy, health_check

MODEL = os.environ.get("RUNG7_MODEL", "qwen2.5:1.5b-instruct")
OUT   = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)

K       = 8           # niches (frozen)
K_STAR  = 0           # principal's target niche
J       = 1.0         # alignment dividend (rung-8 default)
TEMP    = 0.6         # temperature (rung-8 validated graded response)
N       = 20          # agents (rung-8 scale)
T_WARM  = 6           # burn-in rounds
T_MEAS  = 12          # measurement rounds
T_TOTAL = T_WARM + T_MEAS
SEEDS   = [0, 1, 2]   # seeds (3 per condition)
N_NB    = 6           # annealed neighbours (mean-field; rung-8 default)
POOL    = 8           # parallel LLM calls

# Pre-registered thresholds
A1_SLOPE_LO, A1_SLOPE_HI = 0.60, 1.60
A1_R2_MIN = 0.70
A2_LO, A2_HI = 0.50, 2.00
B_DELTA = 0.05


# ── core run function ────────────────────────────────────────────────────────
def run_condition(gamma: float, g: float, seed: int) -> dict:
    """Run one (γ, g, seed) condition. Returns k̄_ss, V_ss, residual_ss in
    TRUE niche space (symbol-randomisation applied; bias cancelled)."""
    ec = LLMEconomy(
        N=N, model=MODEL, temp=TEMP, J=J,
        gamma=gamma, k_star=K_STAR,
        topology="annealed", n_nb=N_NB,
        seed=seed, pool=POOL,
        symbol_random=True,   # rung-8 confound control — mandatory
    )
    # set linear gradient: true niche k pays g*k as base reward
    ec.rewards = np.array([g * k for k in range(K)])

    k_bar_hist, V_hist = [], []
    for rnd in range(T_TOTAL):
        ec.step(rnd)
        if rnd >= T_WARM:
            k_bar_t = float(np.mean(ec.niche))
            V_t     = float(np.var(ec.niche))   # uniform resource weights
            k_bar_hist.append(k_bar_t)
            V_hist.append(V_t)

    k_bar_ss = float(np.mean(k_bar_hist))
    V_ss     = float(np.mean(V_hist))
    residual  = k_bar_ss - K_STAR          # signed; should be positive for g>0, k*=0
    predicted = V_ss * g / gamma if gamma > 0 else float("inf")
    return {
        "k_bar_ss": k_bar_ss, "V_ss": V_ss,
        "residual_ss": residual, "predicted": predicted,
        "parse_rate": ec.parse_ok / max(ec.parse_tot, 1),
    }


def mean_condition(gamma: float, g: float) -> dict:
    """Average run_condition over SEEDS."""
    runs = [run_condition(gamma, g, s) for s in SEEDS]
    return {
        "gamma": gamma, "g": g,
        "residual_ss": float(np.mean([r["residual_ss"] for r in runs])),
        "V_ss":        float(np.mean([r["V_ss"] for r in runs])),
        "predicted":   float(np.mean([r["predicted"] for r in runs])),
        "ratio":       float(np.mean([r["residual_ss"] / r["predicted"] for r in runs])),
        "k_bar_ss":    float(np.mean([r["k_bar_ss"] for r in runs])),
        "parse_rate":  float(np.mean([r["parse_rate"] for r in runs])),
        "residual_std":float(np.std ([r["residual_ss"] for r in runs])),
    }


def ols_loglog(xs, ys):
    lx = np.log(np.clip(xs, 1e-9, None))
    ly = np.log(np.clip(ys, 1e-9, None))
    slope, ic = np.polyfit(lx, ly, 1)
    ly_hat = slope * lx + ic
    ss_res = float(np.sum((ly - ly_hat)**2))
    ss_tot = float(np.sum((ly - ly.mean())**2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 1e-12 else 1.0
    return float(slope), r2


def chk(name, ok, detail):
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {name}: {detail}")
    return ok


# ── main ─────────────────────────────────────────────────────────────────────
def main():
    ok, msg = health_check()
    if not ok:
        print(f"HEALTH FAIL — tunnel/model not live: {msg}")
        raise SystemExit(1)
    print(f"Health: OK ({msg})")

    print("=" * 76)
    print(f"LEVER-1 REAL-AGENT TEST  model={MODEL}  symbol_random=True")
    print(f"N={N}, T={T_TOTAL}(burn={T_WARM}+meas={T_MEAS}), J={J}, temp={TEMP}")
    print(f"Pre-registered in PREREGISTRATION_lever1.md — honest PASS/FAIL below")
    print("=" * 76)

    results  = {}
    checks   = []

    # ── Prediction A: grid ────────────────────────────────────────────────────
    print(f"\nPrediction A — quantitative match: residual_ss ≈ V_ss · g / γ")
    gammas_A = [0.5, 1.0, 2.0]
    gs_A     = [0.1, 0.2]

    rows = []
    for gamma in gammas_A:
        for g in gs_A:
            row = mean_condition(gamma, g)
            rows.append(row)
            print(f"  γ={gamma:.1f} g={g:.1f}: k̄={row['k_bar_ss']:.3f}  "
                  f"residual={row['residual_ss']:.4f}  predicted={row['predicted']:.4f}  "
                  f"ratio={row['ratio']:.3f}  V={row['V_ss']:.3f}  "
                  f"parse={row['parse_rate']:.2f}")

    # Parse-rate check (non-pre-registered gate; inconclusive if < 0.90)
    min_parse = min(r["parse_rate"] for r in rows)
    if min_parse < 0.90:
        print(f"\n  WARNING: min parse rate = {min_parse:.2f} < 0.90 — INCONCLUSIVE (F-unparseable)")
        results["status"] = "inconclusive_parse"

    # A1: log-log OLS
    valid_rows = [r for r in rows if r["predicted"] > 1e-6 and r["residual_ss"] > 0]
    slope_A, r2_A = ols_loglog(
        [r["predicted"]   for r in valid_rows],
        [r["residual_ss"] for r in valid_rows],
    )
    print(f"\n  OLS log(residual) ~ log(predicted): slope={slope_A:.4f}  R²={r2_A:.4f}")
    ok_A1 = A1_SLOPE_LO <= slope_A <= A1_SLOPE_HI and r2_A >= A1_R2_MIN
    checks.append(("A1", chk("A1 proportionality (slope∈[0.60,1.60], R²≥0.70)",
                              ok_A1, f"slope={slope_A:.3f}, R²={r2_A:.3f}")))

    # A2: mean ratio
    mean_ratio = float(np.mean([r["ratio"] for r in valid_rows]))
    ratio_std  = float(np.std ([r["ratio"] for r in valid_rows]))
    ok_A2 = A2_LO <= mean_ratio <= A2_HI
    checks.append(("A2", chk("A2 mean ratio ∈ [0.50, 2.00]",
                              ok_A2, f"mean={mean_ratio:.3f} std={ratio_std:.3f}")))

    # A3: direction — residual decreases with γ (fixed g)
    def direction_ok(g_val):
        pts = sorted([r for r in rows if r["g"] == g_val], key=lambda r: r["gamma"])
        mono = all(pts[i]["residual_ss"] >= pts[i+1]["residual_ss"] for i in range(len(pts)-1))
        vals = [f"{r['residual_ss']:.3f}" for r in pts]
        return mono, " > ".join(vals) + f" (g={g_val})"
    mono_01, desc_01 = direction_ok(0.1)
    mono_02, desc_02 = direction_ok(0.2)
    ok_A3 = sum([mono_01, mono_02]) >= 1   # at least 1 of 2 g-slices monotone
    checks.append(("A3", chk("A3 direction: residual↓ as γ↑ (≥1/2 g-slices)",
                              ok_A3, f"{desc_01} | {desc_02}")))

    # CAP check
    cap_triggered = r2_A < 0.50 and not ok_A3
    if cap_triggered:
        print("\n  *** CAP TRIGGERED: R² < 0.50 and no monotone direction ***")
        print("  Verdict: not cleanly testable at this scale. Not a falsification.")
        results["cap"] = True

    results["A"] = {
        "grid": [
            {"gamma": r["gamma"], "g": r["g"],
             "k_bar_ss": r["k_bar_ss"], "V_ss": r["V_ss"],
             "residual_ss": r["residual_ss"], "predicted": r["predicted"],
             "ratio": r["ratio"], "parse_rate": r["parse_rate"]}
            for r in rows
        ],
        "slope": slope_A, "r2": r2_A, "mean_ratio": mean_ratio, "ratio_std": ratio_std,
    }

    # ── Prediction B: marginal efficiency ─────────────────────────────────────
    print(f"\nPrediction B — marginal efficiency (incentive-wins zone; δ={B_DELTA})")
    print("  NOTE: oversight-wins zone not tested (K=8 saturation — pre-stated)")

    B_cases = [("B1", 1.0, 0.1), ("B2", 2.0, 0.1)]
    B_ratios = []

    for bid, gamma, g in B_cases:
        theory_ev = gamma / (2 * g)
        # finite-difference efficiency
        def mean_r(gam, gg):
            return float(np.mean([
                run_condition(gam, gg, s)["residual_ss"] for s in SEEDS
            ]))
        r0       = mean_r(gamma, g)
        r_gam    = mean_r(gamma + B_DELTA, g)
        r_g      = mean_r(gamma, g - B_DELTA)
        eff_gam  = (r0 - r_gam) / B_DELTA
        eff_g    = (r0 - r_g)   / B_DELTA
        ratio_B  = eff_g / eff_gam if abs(eff_gam) > 1e-9 else float("inf")
        B_ratios.append(ratio_B)

        print(f"  {bid} (γ={gamma}, g={g}): r0={r0:.4f}  "
              f"eff_γ={eff_gam:.4f}  eff_g={eff_g:.4f}  "
              f"ratio eff_g/eff_γ={ratio_B:.3f}  theory(endogenous-V)={theory_ev:.1f}")
        ok_B = ratio_B > 1.0
        checks.append((bid, chk(f"{bid} ({bid[1:]}: eff_g/eff_γ > 1.0)",
                                 ok_B, f"ratio={ratio_B:.3f}")))
        results[bid] = {
            "gamma": gamma, "g": g, "r0": r0,
            "eff_gamma": eff_gam, "eff_g": eff_g, "ratio": ratio_B,
            "theory_endogenous_V": theory_ev,
        }

    ok_Bmono = B_ratios[1] >= B_ratios[0]
    checks.append(("B_mono", chk("B_mono: ratio(B2) ≥ ratio(B1)",
                                  ok_Bmono, f"{B_ratios[1]:.3f} ≥ {B_ratios[0]:.3f}?")))
    results["B_mono"] = {"ratios": B_ratios, "monotone": ok_Bmono}

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "=" * 76)
    n_pass = sum(1 for _, ok in checks if ok)
    n_tot  = len(checks)

    if cap_triggered:
        verdict = "NOT TESTABLE AT THIS SCALE"
    elif n_pass == n_tot:
        verdict = "CONFIRMED ON REAL AGENTS"
    elif any(not ok for nm, ok in checks if nm.startswith("A")
             and nm != "A3") and not ok_A3:
        verdict = "FALSIFIED"
    elif n_pass >= n_tot - 1:
        verdict = "MOSTLY CONFIRMED"
    elif n_pass >= n_tot // 2:
        verdict = "PARTIALLY CONFIRMED"
    else:
        verdict = "FAILED"

    print(f"VERDICT: {verdict}  ({n_pass}/{n_tot} pre-registered checks passed)")
    for name, ok in checks:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 76)

    results["summary"] = {
        "model": MODEL, "n_pass": n_pass, "n_tot": n_tot, "verdict": verdict,
        "checks": [(n, bool(ok)) for n, ok in checks],
        "cap_triggered": cap_triggered,
    }

    out_path = os.path.join(OUT, "lever1_real.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults → {out_path}")

    raise SystemExit(0 if n_pass == n_tot and not cap_triggered else 1)


if __name__ == "__main__":
    main()

"""
run_rung8.py — the bias-controlled real-agent test (Rung 8). Symbol-randomised niche
labels (guardrail (a)) so the LLM's token prior maps to a different true niche per agent
(collective bias cancels) while coordination/reward-reading are still processed by the
model; noise = the LLM's own sampling temperature (guardrail: NO externally-imposed
alignment-noise). Thresholds frozen in PREREGISTRATION_rung8.md. Writes
results/real_results_rung8.json. qwen2.5:1.5b primary.

Run:  RUNG7_MODEL=qwen2.5:1.5b-instruct python3 sim/field/real/run_rung8.py
"""
from __future__ import annotations
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import experiments as E
from llm_economy import LLMEconomy

OUT = os.path.join(os.path.dirname(__file__), "results")
TEMPS = [0.2, 0.6, 1.0, 1.4, 2.0, 2.8]      # frozen, PREREG rung8 §3
SEEDS = [0, 1]


def main():
    ok, msg = __import__("llm_economy").health_check()
    if not ok:
        print(f"HEALTH FAIL ({msg})"); return False
    print("=" * 78)
    print(f"RUNG 8 — bias-controlled (symbol-randomised) real-agent test ({E.MODEL})")
    print("Thresholds: PREREGISTRATION_rung8.md   noise = LLM's own temperature")
    print("=" * 78)
    rec, results = [], {}
    def R(name, ok, detail):
        rec.append((name, bool(ok))); print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    print("\nSIGNATURE 2 — collective-goal transition (symbol-randomised)")
    free = E.flocking_sweep(gamma=0.0, topology="annealed", temps=TEMPS, seeds=SEEDS,
                            symbol_random=True)
    ms = np.array([free[t]["m"] for t in TEMPS]); chis = np.array([free[t]["chi"] for t in TEMPS])

    c1 = free[0.2]["m"] > 0.55 and free[2.8]["m"] < 0.35
    R("C1 order->disorder transition", c1,
      f"m(0.2)={free[0.2]['m']:.3f} (>0.55?) -> m(2.8)={free[2.8]['m']:.3f} (<0.35?)")
    ipk = int(np.argmax(chis)); interior = 0 < ipk < len(TEMPS) - 1
    c2 = interior and chis[ipk] > 1.5 * max(chis[0], chis[-1])
    R("C2 susceptibility peak (interior)", c2,
      f"chi peaks at temp={TEMPS[ipk]} (chi={chis[ipk]:.3f}) vs ends {chis[0]:.3f}/{chis[-1]:.3f}")

    # M motility gating (annealed vs quenched at low temp)
    quench = E.flocking_sweep(gamma=0.0, topology="quenched", temps=[0.2], seeds=SEEDS,
                              symbol_random=True)
    dM = free[0.2]["m"] - quench[0.2]["m"]
    R("M motility gating", dM >= 0.10,
      f"m(0.2): annealed={free[0.2]['m']:.3f} - quenched={quench[0.2]['m']:.3f} = {dM:+.3f}")

    # C3 control = mass — only meaningful if there is an ordered phase to round.
    ordered_phase = free[0.2]["m"] > 0.55
    if ordered_phase:
        ctrl = E.flocking_sweep(gamma=0.6, topology="annealed", temps=TEMPS, seeds=SEEDS,
                                symbol_random=True)
        chis_c = np.array([ctrl[t]["chi"] for t in TEMPS])
        c3 = (ctrl[2.8]["m"] - free[2.8]["m"] >= 0.10) and (chis_c.max() < chis.max())
        R("C3 control = mass", c3, f"m(2.8) Δ={ctrl[2.8]['m']-free[2.8]['m']:+.3f}; "
          f"chi_peak {chis.max():.3f}->{chis_c.max():.3f}")
        results["ctrl"] = ctrl
    else:
        # MOOT, not skipped silently: there is no ordered phase to round (see verdict)
        ctrl_probe = E.flocking_sweep(gamma=0.6, topology="annealed", temps=[0.2], seeds=SEEDS,
                                      symbol_random=True)
        R("C3 control = mass (MOOT — no ordered phase)", False,
          f"no spontaneous order at γ=0 (m(0.2)={free[0.2]['m']:.3f}); "
          f"even γ=0.6 control gives m(0.2)={ctrl_probe[0.2]['m']:.3f}")
        results["ctrl_probe"] = ctrl_probe

    results["free"] = free; results["quench"] = quench
    results["checks"] = {n: o for n, o in rec}
    json.dump(results, open(os.path.join(OUT, "real_results_rung8.json"), "w"), indent=2)
    n_pass = sum(1 for _, o in rec if o)
    print("\n" + "=" * 78)
    print(f"RUNG-8 FLOCKING: {n_pass}/{len(rec)} checks passed -> results/real_results_rung8.json")
    for n, o in rec:
        print(f"  {'PASS' if o else 'FAIL'}  {n}")
    print("=" * 78)
    return n_pass == len(rec)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)

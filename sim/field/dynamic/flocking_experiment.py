"""
flocking_experiment.py — does a population of value-agents whose goals evolve
undergo a collective-goal (order->disorder) PHASE TRANSITION, as an EMERGENT
property of the LatticeEconomy, with the critical signatures doc 08 §5 predicts?

Thrust-B test of doc 08 §5 (HANDOFF). The agents' alignment weights are not fixed
(as in plain Vicsek) — they EVOLVE by a resource replicator: aligning with neighbors
is a positive-sum dividend (doc 04 §4), so well-aligned agents capture resource and
their goal spreads. We MEASURE, sweeping the idiosyncrasy noise η:

  C1  order->disorder transition: collective-goal magnitude m=|<e^{iθ}>| collapses
      from ordered (m~1) to disordered (m~0) as η rises.
  C2  a susceptibility PEAK χ(η)=N(<m²>-<m>²) near the critical noise η_c — the
      finite-size signature of a continuous transition (fluctuations maximal at η_c).
  C3  the is/ought MASS test (doc 08 §6, sharpened by docs/10): turning on a control
      field γ>0 (alignment design toward a principal goal θ*) acts as a symmetry-
      breaking MASS term — it should ROUND the transition: m stays nonzero deep into
      the noisy regime and the susceptibility peak is suppressed. Goals are Goldstone
      (soft, transition sharp) only when UNCONTROLLED; control gives them a mass.

Honest scope: toy lattice agents, fixed in space (the XY/lattice-Vicsek variant, not
motile Vicsek), scalar noise, single principal goal. A PASS shows the collective-goal
transition AND the control=mass prediction emerge from a value economy with evolving
goals+resource — strong internal evidence for doc 08 §5–6 — but is not a measurement
on real agents. Finite L: these are finite-size crossovers, not thermodynamic-limit
critical exponents (that needs finite-size scaling across L, noted as future work).

Run:  python3 sim/field/dynamic/flocking_experiment.py
"""
from __future__ import annotations
import os, json
import numpy as np
from economy import FlockEconomy

OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)


def sweep(etas, gamma, N=400, Lbox=10.0, v0=0.3, repl=0.5, steps=500, burn=320,
          seeds=(0, 1, 2, 3)):
    """For each noise η, run the motile FlockEconomy to steady state and average the
    measured order parameter and susceptibility over seeds."""
    out = {}
    for eta in etas:
        m, chi = [], []
        for s in seeds:
            ec = FlockEconomy(N=N, Lbox=Lbox, v0=v0, eta=eta, gamma=gamma,
                              repl=repl, seed=s)
            r = ec.run(steps=steps, burn=burn)
            m.append(r["m"]); chi.append(r["chi"])
        out[eta] = dict(m=float(np.mean(m)), chi=float(np.mean(chi)))
    return out


def main():
    print("=" * 76)
    print("flocking_experiment — does a value economy with EVOLVING goals undergo a")
    print("collective-goal phase transition? (Thrust B / doc 08 §5–6)")
    print("=" * 76)
    results, summary = [], {}

    def record(name, ok, detail):
        results.append((name, ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    etas = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85]

    # --- uncontrolled population (γ=0): Goldstone goals, sharp transition --------
    print("\nUncontrolled (γ=0): sweeping idiosyncrasy noise η")
    free = sweep(etas, gamma=0.0)
    m_curve = "  ".join(f"η={e}:{free[e]['m']:.2f}" for e in etas)
    chi_curve = "  ".join(f"{free[e]['chi']:.2f}" for e in etas)
    print(f"    m(η):   {m_curve}")
    print(f"    χ(η):   {chi_curve}")

    m_lo, m_hi = free[etas[0]]["m"], free[etas[-1]]["m"]
    c1_ok = m_lo > 0.7 and m_hi < 0.3
    record("C1 order->disorder transition (γ=0)", c1_ok,
           f"m(η={etas[0]})={m_lo:.2f} (ordered) -> m(η={etas[-1]})={m_hi:.2f} (disordered)")

    chis = np.array([free[e]["chi"] for e in etas])
    eta_c_idx = int(np.argmax(chis))
    eta_c = etas[eta_c_idx]
    # a genuine peak: interior maximum, and clearly above the ordered- & disordered-end χ
    peak_interior = 0 < eta_c_idx < len(etas) - 1
    c2_ok = peak_interior and chis[eta_c_idx] > 2.0 * max(chis[0], chis[-1])
    record("C2 susceptibility peak near η_c (continuous-transition signature, γ=0)", c2_ok,
           f"χ peaks at η_c≈{eta_c} (χ_peak={chis[eta_c_idx]:.2f} vs ends "
           f"{chis[0]:.2f}/{chis[-1]:.2f})")

    # --- controlled population (γ>0): mass term, transition rounded (doc 08 §6) --
    print("\nControlled (γ=0.4): a control field = symmetry-breaking MASS (doc 08 §6)")
    ctrl = sweep(etas, gamma=0.4)
    mc_curve = "  ".join(f"η={e}:{ctrl[e]['m']:.2f}" for e in etas)
    cc_curve = "  ".join(f"{ctrl[e]['chi']:.2f}" for e in etas)
    print(f"    m(η):   {mc_curve}")
    print(f"    χ(η):   {cc_curve}")
    chis_c = np.array([ctrl[e]["chi"] for e in etas])
    # mass rounds the transition: collective goal survives noise (m higher at large η)
    # AND the susceptibility peak is suppressed relative to the uncontrolled case
    m_hi_ctrl = ctrl[etas[-1]]["m"]
    rounded = m_hi_ctrl > m_hi + 0.1 and chis_c.max() < chis.max()
    record("C3 control acts as a MASS: transition rounded (m survives, χ-peak suppressed)",
           rounded,
           f"m(η={etas[-1]}): {m_hi:.2f}(γ=0) -> {m_hi_ctrl:.2f}(γ=0.4); "
           f"χ_peak: {chis.max():.2f}(γ=0) -> {chis_c.max():.2f}(γ=0.4)")

    summary = dict(etas=etas, free=free, ctrl=ctrl, eta_c=eta_c,
                   chi_peak_free=float(chis.max()), chi_peak_ctrl=float(chis_c.max()))
    json.dump(summary, open(os.path.join(OUT, "flocking_results.json"), "w"), indent=2)

    n_pass = sum(1 for _, ok in results if ok)
    print("\n" + "=" * 76)
    print(f"SUMMARY: {n_pass}/{len(results)} checks passed   (cached -> results/flocking_results.json)")
    for name, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 76)
    return n_pass == len(results)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)

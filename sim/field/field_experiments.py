"""
field_experiments.py — does the field theory of value (docs/08) actually have its
claimed phenomenology when you simulate it?

Two falsifiable checks of doc 08, each PASS/FAIL against a *quantitative* prediction:

  F1  Demand-shock propagation (doc 08 §3): does a localized demand shock travel as a
      WAVE (front position linear in t, speed ∝ 1/√τ) at large lag τ, and DIFFUSE
      (front ∝ √t) at small τ?  -> the telegrapher crossover.
  F2  Collective-goal formation (doc 08 §5): does a population of goal-directors
      undergo an order->disorder PHASE TRANSITION as noise rises (Vicsek/Toner-Tu)?

Honesty (doc 08 §9): F1 simulates the coarse-grained field dynamics, so it tests
whether the predicted SCALING (linear-vs-sqrt, v∝1/√τ) holds — non-trivial, but not
evidence about real agents. F2 reproduces known active-matter physics, confirming our
goal field IS an active-matter order parameter. Neither is empirical validation on
real systems; both check internal consistency of the doc-08 construction.

Run:  python3 sim/field/field_experiments.py
"""
from __future__ import annotations
import numpy as np

results = []
def record(name, ok, detail):
    results.append((name, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ---------------------------------------------------------------------------
# F1 — demand-shock propagation via the telegrapher dynamics on a 1D ring
#   τ φ_tt + φ_t = D φ_xx   (doc 08 §3); explicit leapfrog-ish scheme, dx=1.
# ---------------------------------------------------------------------------
def simulate_front(tau, D=50.0, total_time=None, M=1600, dt=0.02, thresh=0.05):
    """Inject a Gaussian pulse at center; track the right-moving leading edge.
    Returns (times, front_positions) measured from the center.
    NOTE: a telegrapher wave damps over ~2τ while travelling at c=√(D/τ), so it
    only covers ~2√(Dτ) sites before dying — D must be large enough that this is
    many sites, and the run time must scale with τ (a few decay times), else you
    just track the diffusive tail of a dead wave."""
    if total_time is None:
        total_time = 3.0 * tau                            # ~1.5 damping times
    steps = int(np.clip(total_time / dt, 200, 80000))
    x = np.arange(M)
    c = M // 2
    phi = np.exp(-((x - c) ** 2) / (2 * 8.0 ** 2))     # localized demand shock
    phi /= phi.max()
    phi_old = phi.copy()                                # start at rest (φ_t=0)
    a = tau / dt**2 + 1.0 / (2 * dt)
    b = 2 * tau / dt**2
    cc = tau / dt**2 - 1.0 / (2 * dt)
    times, fronts = [], []
    rec_every = max(1, steps // 200)
    for n in range(steps):
        lap = np.roll(phi, -1) + np.roll(phi, 1) - 2 * phi
        phi_new = (D * lap + b * phi - cc * phi_old) / a
        phi_old, phi = phi, phi_new
        if n % rec_every == 0:
            right = np.abs(phi[c:])                      # right half
            pk = right.max()
            if pk < 1e-9:
                continue
            idx = np.where(right > thresh * pk)[0]       # RELATIVE threshold:
            if len(idx):                                 # robust to wave damping
                times.append((n + 1) * dt)
                fronts.append(idx.max())                 # leading-edge distance
    return np.array(times), np.array(fronts)

def fit_quality(t, pos):
    """R^2 of pos ~ A*t (wave) and pos ~ B*sqrt(t) (diffusion), after dropping the
    initial transient (the finite-width pulse splitting before it becomes a front)."""
    if len(t) < 8:
        return -1, -1, 0.0
    k = len(t) // 4                                       # skip first 25% (transient)
    t = t[k:] - t[k]; pos = pos[k:] - pos[k]              # re-zero to the front motion
    def r2(model):
        ss_res = np.sum((pos - model) ** 2)
        ss_tot = np.sum((pos - pos.mean()) ** 2) + 1e-12
        return 1 - ss_res / ss_tot
    A = np.sum(t * pos) / np.sum(t * t)                  # least-sq through origin
    st = np.sqrt(t)
    B = np.sum(st * pos) / np.sum(st * st)
    return r2(A * t), r2(B * st), A                      # (R2_linear, R2_sqrt, speed)

def simulate_spread(tau, D=50.0, total_time=None, M=1600, dt=0.02):
    """Same telegrapher integration, but record the second spatial moment σ²(t)
    about the center — the clean ballistic-vs-diffusive discriminator:
    wave (two packets at ±ct) → σ² ∝ t² ; diffusion → σ² ∝ t."""
    if total_time is None:
        total_time = 3.0 * tau
    steps = int(np.clip(total_time / dt, 200, 80000))
    x = np.arange(M); c = M // 2
    w = (x - c).astype(float) ** 2
    phi = np.exp(-((x - c) ** 2) / (2 * 8.0 ** 2)); phi /= phi.max()
    phi_old = phi.copy()
    a = tau / dt**2 + 1.0 / (2 * dt); b = 2 * tau / dt**2; cc = tau / dt**2 - 1.0 / (2 * dt)
    times, sig2 = [], []
    rec_every = max(1, steps // 200)
    for n in range(steps):
        lap = np.roll(phi, -1) + np.roll(phi, 1) - 2 * phi
        phi_old, phi = phi, (D * lap + b * phi - cc * phi_old) / a
        if n % rec_every == 0:
            aw = np.abs(phi); tot = aw.sum()
            if tot > 1e-9:
                times.append((n + 1) * dt); sig2.append(float((w * aw).sum() / tot))
    return np.array(times), np.array(sig2)

def spread_regime(t, s2):
    """R² of σ² ~ A·t (diffusive) vs σ² ~ B·t² (ballistic/wave), through origin."""
    if len(t) < 8:
        return -1, -1
    s2 = s2 - s2[0]
    A = np.sum(t * s2) / np.sum(t * t)
    B = np.sum(t**2 * s2) / np.sum(t**4)
    tot = np.sum((s2 - s2.mean()) ** 2) + 1e-12
    r2 = lambda m: 1 - np.sum((s2 - m) ** 2) / tot
    return r2(A * t), r2(B * t * t)        # (R²_linear/diffusion, R²_quadratic/wave)

def F1_demand_wave():
    print("\nF1 — demand-shock propagation (doc 08 §3): wave at large τ, diffusion at small τ")
    D = 50.0
    # (a) WAVE regime (large τ): ballistic spreading σ² ∝ t² ; also speed ≈ √(D/τ)
    ts, s2 = simulate_spread(tau=8.0, D=D)
    r2lin_w, r2quad_w = spread_regime(ts, s2)
    t_w, p_w = simulate_front(tau=8.0, D=D); _, _, v_w = fit_quality(t_w, p_w)
    wave_ok = r2quad_w > r2lin_w and r2quad_w > 0.97
    record("F1a wave regime (τ=8): ballistic spread σ² ∝ t²",
           wave_ok, f"R²_quad={r2quad_w:.3f} > R²_lin={r2lin_w:.3f}; front speed≈{v_w:.3f} "
                    f"(pred √(D/τ)={np.sqrt(D/8):.3f})")

    # (b) DIFFUSION regime (τ→0): diffusive spreading σ² ∝ t (dt small for stability)
    td, s2d = simulate_spread(tau=0.02, D=D, total_time=8.0, dt=0.005)
    r2lin_d, r2quad_d = spread_regime(td, s2d)
    diff_ok = r2lin_d > r2quad_d and r2lin_d > 0.97
    record("F1b diffusion regime (τ=0.02): diffusive spread σ² ∝ t",
           diff_ok, f"R²_lin={r2lin_d:.3f} > R²_quad={r2quad_d:.3f}")

    # (b) quantitative scaling: measured wave speed ∝ 1/√τ  (v = √(D/τ))
    taus = np.array([4.0, 8.0, 16.0, 32.0])
    measured, predicted = [], []
    for tau in taus:
        t, p = simulate_front(tau=tau, D=D)
        _, _, v = fit_quality(t, p)
        measured.append(v); predicted.append(np.sqrt(D / tau))
    measured, predicted = np.array(measured), np.array(predicted)
    ratio = measured / predicted
    rel_spread = ratio.std() / ratio.mean()
    scaling_ok = rel_spread < 0.10                       # ratio ~const => v ∝ 1/√τ
    record("F1c speed scaling v ∝ 1/√τ (telegrapher)",
           scaling_ok,
           f"measured/√(D/τ) = {np.array2string(ratio, precision=3)} "
           f"(spread {rel_spread*100:.1f}%, should be ~const)")


# ---------------------------------------------------------------------------
# F2 — collective-goal formation: Vicsek/XY order-disorder transition on a 2D lattice
#   goal-director angle θ_i aligns with neighbors + noise η (doc 08 §4-5)
# ---------------------------------------------------------------------------
def vicsek_order(N=300, Lbox=7.0, r=1.0, v0=0.3, eta=0.5, steps=150, seed=0):
    """Vicsek self-propelled particles (the model whose continuum limit is
    Toner-Tu, doc 08 §0). Particles MOVE and align with neighbors within radius r,
    plus scalar noise η∈[0,1]; motion is what lets a 2D flock order (beats
    Mermin-Wagner). Returns the polar order parameter m=|<e^{iθ}>|."""
    rng = np.random.default_rng(seed)
    pos = rng.uniform(0, Lbox, size=(N, 2))
    th = rng.uniform(-np.pi, np.pi, size=N)
    for _ in range(steps):
        d = pos[:, None, :] - pos[None, :, :]
        d -= Lbox * np.round(d / Lbox)                   # periodic min-image
        nb = (d[:, :, 0]**2 + d[:, :, 1]**2) <= r * r    # neighbor mask (incl. self)
        mean_th = np.arctan2(nb @ np.sin(th), nb @ np.cos(th))
        th = mean_th + eta * rng.uniform(-np.pi, np.pi, size=N)
        pos = (pos + v0 * np.stack([np.cos(th), np.sin(th)], axis=1)) % Lbox
    return float(np.abs(np.mean(np.exp(1j * th))))

def F2_flocking_transition():
    print("\nF2 — collective-goal formation (doc 08 §5): order-disorder phase transition")
    etas = [0.05, 0.15, 0.3, 0.5, 0.7, 0.9]
    m = {e: float(np.mean([vicsek_order(eta=e, seed=s) for s in range(2)])) for e in etas}
    curve = "  ".join(f"η={e}:{m[e]:.2f}" for e in etas)
    print(f"    order parameter m(η):  {curve}")
    m_low = m[0.05]; m_high = m[0.9]
    transition_ok = m_low > 0.7 and m_high < 0.3
    record("F2 order->disorder transition exists",
           transition_ok, f"m(low noise)={m_low:.2f} (ordered) -> m(high noise)={m_high:.2f} (disordered)")
    # monotone-ish decline = a transition, not noise
    vals = [m[e] for e in etas]
    mono_ok = vals[0] > vals[-1] and (vals[0] - vals[-1]) > 0.5
    record("F2 monotone collapse of collective goal with noise",
           mono_ok, f"Δm = {vals[0]-vals[-1]:.2f} across the noise sweep")


def main():
    print("=" * 74)
    print("field_experiments — does doc 08's field theory have its claimed phenomenology?")
    print("=" * 74)
    F1_demand_wave()
    F2_flocking_transition()
    n_pass = sum(1 for _, ok, _ in results if ok)
    print("\n" + "=" * 74)
    print(f"SUMMARY: {n_pass}/{len(results)} checks passed")
    for name, ok, _ in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 74)
    raise SystemExit(0 if n_pass == len(results) else 1)


if __name__ == "__main__":
    main()

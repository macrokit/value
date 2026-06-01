"""
wave_experiment.py — does a demand shock propagate as a WAVE with the telegrapher
dispersion crossover, as an EMERGENT property of the RingEconomy agent rules?

This is the Thrust-B test of doc 08 §3 (HANDOFF). Unlike sim/field/field_experiments.py
(which integrated the telegrapher PDE), here the telegrapher equation is NOWHERE in
the code — RingEconomy only has agents shipping resource toward value with a finite
flow-adjustment lag τ_J. We MEASURE whether the field that emerges shows:

  W1  ballistic spreading σ²(t) ∝ t² at large lag (wave) vs σ² ∝ t at small lag
      (diffusion) — the regime split.
  W2  wave speed v ∝ 1/√τ_J  (the telegrapher v=√(D/τ) scaling, measured emergently).
  W3  the DISPERSION CROSSOVER (the central falsifiable prediction, doc 08 §3):
      short-wavelength modes (q>q*) oscillate (waves); long-wavelength modes (q<q*)
      decay monotonically (diffusion); the measured crossover q* matches 1/(2√(Dτ)).

Honest scope: this is a toy agent economy (one resource good, scalar price, ring
topology, linear flow rule). A PASS shows the telegrapher structure is the emergent
continuum limit of THESE agent rules — strong internal evidence the field theory is a
coarse-graining, not analogy — but it is not yet a measurement on real agents/markets.

Run:  python3 sim/field/dynamic/wave_experiment.py
"""
from __future__ import annotations
import os, json
import numpy as np
from economy import RingEconomy

OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)


def spreading_run(tau_J, N=2400, sigma=50.0, e0=1.0, rho0=1.0, dt=0.02,
                  total_time=None, pulse_w=6.0, pulse_a=0.3):
    """Localized demand shock: displace resource in a Gaussian pulse at the ring
    center (someone suddenly values resource here), ρ uniform, flows at rest. Evolve
    and record σ²(t), the second spatial moment of |δe| about center — the clean
    ballistic(t²)-vs-diffusive(t) discriminator. D ≡ σ ρ0/e0² is the emergent
    diffusion constant; wave speed predicted √(D/τ_J)."""
    total_time = total_time or 3.0 * max(tau_J, 0.5)
    steps = int(np.clip(total_time / dt, 200, 60000))
    ec = RingEconomy(N=N, e0=e0, rho0=rho0, sigma=sigma, tau_J=tau_J, dt=dt)
    x = np.arange(N); c = N // 2
    ec.e = e0 + pulse_a * np.exp(-((x - c) ** 2) / (2 * pulse_w ** 2))
    w = (x - c).astype(float) ** 2
    rec_every = max(1, steps // 200)
    times, sig2, fronts, peaks = [], [], [], []
    thresh = 0.05
    for n in range(steps):
        ec.step()
        if n % rec_every == 0:
            d = np.abs(ec.e - e0); tot = d.sum()
            if tot < 1e-12:
                continue
            times.append((n + 1) * dt)
            sig2.append(float((w * d).sum() / tot))
            right = d[c:]; pk = right.max()
            idx = np.where(right > thresh * pk)[0]
            fronts.append(float(idx.max()) if len(idx) else 0.0)
            # PEAK position in the right half: does the disturbance PROPAGATE (peak
            # travels, a wave) or DECAY IN PLACE (peak stays at injection site,
            # diffusion)? Robust to the fast wave-precursor that confounds the front.
            peaks.append(float(np.argmax(right)))
    return (np.array(times), np.array(sig2), np.array(fronts),
            np.array(peaks), sigma * rho0 / e0 ** 2)


def front_regime(t, pos):
    """The defining wave-vs-diffusion discriminator: does the disturbance PROPAGATE
    (front position ∝ t, a traveling front) or SPREAD IN PLACE (front ∝ √t, a
    diffusive blob)? Returns (R²_linear, R²_sqrt), through origin, after dropping the
    initial transient. Robust to telegrapher damping (uses the relative-threshold
    leading edge, not the second moment)."""
    if len(t) < 8:
        return -1.0, -1.0
    k = len(t) // 4
    t = t[k:] - t[k]; pos = pos[k:] - pos[k]
    st = np.sqrt(t)
    A = np.sum(t * pos) / np.sum(t * t)
    B = np.sum(st * pos) / np.sum(st * st)
    tot = np.sum((pos - pos.mean()) ** 2) + 1e-12
    r2 = lambda m: 1 - np.sum((pos - m) ** 2) / tot
    return r2(A * t), r2(B * st)


def front_speed(t, pos):
    """Speed from pos ~ v·t (after dropping the first 25% transient)."""
    if len(t) < 8:
        return 0.0
    k = len(t) // 4
    t = t[k:] - t[k]; pos = pos[k:] - pos[k]
    return float(np.sum(t * pos) / np.sum(t * t))


def classify_mode(a_q, settle_frac=0.15):
    """Wave vs diffusion for a single seeded Fourier mode: a diffusive mode decays
    monotonically (no zero crossing after a brief settle); a wave mode oscillates
    (the modal amplitude changes sign). Return (n_sign_changes, is_wave)."""
    k = int(settle_frac * len(a_q))
    a = a_q[k:]
    if len(a) < 4 or np.max(np.abs(a)) < 1e-12:
        return 0, False
    a = a / np.max(np.abs(a))
    sig = np.sign(a)
    sig = sig[np.abs(a) > 0.02]              # ignore near-zero noise floor
    if len(sig) < 4:
        return 0, False
    changes = int(np.sum(np.abs(np.diff(sig)) > 0))
    return changes, changes >= 1


def main():
    print("=" * 76)
    print("wave_experiment — does a demand shock travel as a telegrapher wave,")
    print("EMERGENT from RingEconomy agent rules? (Thrust B / doc 08 §3)")
    print("=" * 76)
    results, summary = [], {}

    def record(name, ok, detail):
        results.append((name, ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    # --- W1: propagation vs in-place spreading ------------------------------
    # The defining difference: a WAVE propagates (the disturbance PEAK travels at
    # finite speed v); DIFFUSION spreads in place (the peak stays at the injection
    # site and decays). Peak position is robust to the fast wave-precursor that, for
    # any finite τ, always rides the leading edge (telegrapher signal speed √(D/τ)).
    print("\nW1 — propagation regime: peak travels (wave, large lag) vs peak pinned (diffusion)")
    tw, _, _, pkw, D = spreading_run(tau_J=8.0, total_time=1.8 * 8.0)
    r2lin_w, _ = front_regime(tw, pkw)            # peak ∝ t ?
    v_peak = front_speed(tw, pkw); v_pred = np.sqrt(D / 8.0)
    wave_ok = r2lin_w > 0.95 and abs(v_peak / v_pred - 1) < 0.2 and pkw.max() > 10
    record("W1a wave regime (τ_J=8): disturbance PEAK propagates ∝ t", wave_ok,
           f"R²_lin={r2lin_w:.3f}; peak speed≈{v_peak:.3f} (pred √(D/τ)={v_pred:.3f}, D={D:.1f}); "
           f"peak travels {pkw.max():.0f} sites")
    # overdamped limit: τ_J = dt so the flow relaxes fully to its instantaneous Darcy
    # value each step (dt/τ_J = 1) — no residual inertia, the clean diffusive limit
    td, s2d, _, pkd, _ = spreading_run(tau_J=0.005, dt=0.005, total_time=14.0)
    # diffusion: peak pinned at injection site AND bulk σ² grows ∝ t (in-place spread)
    k = len(td) // 4
    tt = td[k:] - td[k]; ss = s2d[k:] - s2d[k]
    Aq = np.sum(tt * ss) / np.sum(tt * tt)          # σ² ~ A·t (diffusion)
    Bq = np.sum(tt ** 2 * ss) / np.sum(tt ** 4)     # σ² ~ B·t² (wave)
    tot = np.sum((ss - ss.mean()) ** 2) + 1e-12
    r2_s2_lin = 1 - np.sum((ss - Aq * tt) ** 2) / tot
    r2_s2_quad = 1 - np.sum((ss - Bq * tt * tt) ** 2) / tot
    diff_ok = pkd.max() <= 3 and r2_s2_lin > r2_s2_quad and r2_s2_lin > 0.95
    record("W1b diffusion regime (τ_J→0): peak PINNED, bulk σ²∝t (spreads in place)", diff_ok,
           f"peak travels {pkd.max():.0f} sites (pinned); σ²∝t R²_lin={r2_s2_lin:.3f} > "
           f"R²_quad={r2_s2_quad:.3f}")
    summary["W1"] = dict(D=D, r2lin_peak_wave=r2lin_w, v_peak=v_peak, v_pred=v_pred,
                         peak_travel_wave=float(pkw.max()), peak_travel_diff=float(pkd.max()),
                         r2_s2_lin_diff=r2_s2_lin, r2_s2_quad_diff=r2_s2_quad)

    # --- W2: speed scaling v ∝ 1/√τ_J --------------------------------------
    print("\nW2 — wave-speed scaling v ∝ 1/√τ_J (telegrapher v=√(D/τ), measured)")
    taus = np.array([4.0, 8.0, 16.0, 32.0])
    meas, pred = [], []
    for tj in taus:
        t, _, _, pk, D = spreading_run(tau_J=tj, total_time=1.8 * tj)
        meas.append(front_speed(t, pk)); pred.append(np.sqrt(D / tj))
    meas, pred = np.array(meas), np.array(pred)
    ratio = meas / pred
    rel = ratio.std() / ratio.mean()
    scaling_ok = rel < 0.12
    record("W2 speed scaling v ∝ 1/√τ_J", scaling_ok,
           f"measured/√(D/τ) = {np.array2string(ratio, precision=3)} (spread {rel*100:.1f}%)")
    summary["W2"] = dict(taus=taus.tolist(), measured=meas.tolist(),
                         predicted=pred.tolist(), ratio=ratio.tolist(), rel_spread=rel)

    # --- W3: dispersion crossover q* ---------------------------------------
    print("\nW3 — dispersion crossover q* (doc 08 §3): short modes wave, long modes diffuse")
    tau_J = 8.0; N = 2400; sigma = 50.0; e0 = 1.0; rho0 = 1.0
    D = sigma * rho0 / e0 ** 2
    q_pred = 1.0 / (2.0 * np.sqrt(D * tau_J))     # predicted crossover wavenumber
    idxs = [2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 32, 44, 60]
    modes = []
    first_wave_q = None
    for idx in idxs:
        ec = RingEconomy(N=N, e0=e0, rho0=rho0, sigma=sigma, tau_J=tau_J, dt=0.02)
        # run long enough to see >~1 oscillation period for wave modes
        t, a_q, q = ec.mode_decay(idx, steps=9000)
        nchg, is_wave = classify_mode(a_q)
        modes.append(dict(idx=idx, q=q, sign_changes=nchg, is_wave=bool(is_wave)))
        tag = "WAVE" if is_wave else "diff"
        print(f"    idx={idx:3d}  q={q:.4f}  sign-changes={nchg:2d}  -> {tag}")
        if is_wave and first_wave_q is None:
            first_wave_q = q
    # crossover: the smallest q (longest wavelength) that oscillates should sit near q_pred
    cross_ok = (first_wave_q is not None
                and 0.3 * q_pred <= first_wave_q <= 3.0 * q_pred)
    record("W3 dispersion crossover q* matches 1/(2√(Dτ))", cross_ok,
           f"emergent q*≈{first_wave_q if first_wave_q else float('nan'):.4f} vs "
           f"predicted {q_pred:.4f} (ratio "
           f"{(first_wave_q/q_pred) if first_wave_q else float('nan'):.2f})")
    summary["W3"] = dict(q_pred=q_pred, first_wave_q=first_wave_q, modes=modes)

    # --- persist & verdict --------------------------------------------------
    json.dump(summary, open(os.path.join(OUT, "wave_results.json"), "w"), indent=2)
    n_pass = sum(1 for _, ok in results if ok)
    print("\n" + "=" * 76)
    print(f"SUMMARY: {n_pass}/{len(results)} checks passed   (cached -> results/wave_results.json)")
    for name, ok in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 76)
    return n_pass == len(results)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)

"""
experiments.py — Rung 7: do the field-theory signatures survive a REAL-LLM
microscopic rule? Runs the two signatures + their derived gating conditions against
the FROZEN thresholds in PREREGISTRATION.md. Honest PASS/FAIL, incl. the falsification
clause. Caches every model call (results/cache.sqlite); writes results/real_results.json.

Run:  python3 sim/field/real/experiments.py            (all)
      python3 sim/field/real/experiments.py flocking   (just signature 2)
      python3 sim/field/real/experiments.py wave        (just signature 1)
"""
from __future__ import annotations
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from llm_economy import LLMEconomy

OUT = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)
# pre-registered primary = 0.5b; secondary robustness = 1.5b (set RUNG7_MODEL)
MODEL = os.environ.get("RUNG7_MODEL", "qwen2.5:0.5b-instruct")
MTAG = MODEL.split(":")[1].split("-")[0] if ":" in MODEL else MODEL

# frozen design constants (PREREGISTRATION §2–§3)
TEMPS = [0.2, 0.6, 1.0, 1.4]
SEEDS = [0, 1]
NF, TF, BURNF = 20, 12, 6           # flocking N, T, burn
NW, TW = 40, 18                     # wave N, T


def flocking_sweep(gamma, topology="annealed", temps=TEMPS, seeds=SEEDS):
    """Return {temp: {m, chi}} averaged over seeds. chi = N·Var_t(m) per seed, averaged."""
    out = {}
    for temp in temps:
        ms, chis, prs = [], [], []
        for s in seeds:
            ec = LLMEconomy(N=NF, model=MODEL, temp=temp, J=1.0, gamma=gamma,
                            k_star=0, topology=topology, n_nb=6, seed=s)
            r = ec.run(T=TF, burn=BURNF)
            ms.append(r["m"]); chis.append(r["chi"]); prs.append(r["parse_rate"])
        out[temp] = dict(m=float(np.mean(ms)), chi=float(np.mean(chis)),
                         parse=float(np.mean(prs)))
        print(f"    [{topology} γ={gamma}] temp={temp}: m={out[temp]['m']:.3f} "
              f"chi={out[temp]['chi']:.3f} parse={out[temp]['parse']:.2f}", flush=True)
    return out


def run_flocking(results):
    print("\nSIGNATURE 2 — collective-goal transition (PRIMARY)")
    rec = []
    def R(name, ok, detail):
        rec.append((name, ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    free = flocking_sweep(gamma=0.0, topology="annealed")
    ms = np.array([free[t]["m"] for t in TEMPS])
    chis = np.array([free[t]["chi"] for t in TEMPS])

    # C1 order->disorder
    c1 = free[0.2]["m"] > 0.55 and free[1.4]["m"] < 0.35
    R("C1 order->disorder transition", c1,
      f"m(0.2)={free[0.2]['m']:.3f} (>0.55?) -> m(1.4)={free[1.4]['m']:.3f} (<0.35?)")

    # C2 susceptibility peak (interior, >1.5x endpoints)
    ipk = int(np.argmax(chis))
    interior = 0 < ipk < len(TEMPS) - 1
    c2 = interior and chis[ipk] > 1.5 * max(chis[0], chis[-1])
    R("C2 susceptibility peak (interior)", c2,
      f"chi peaks at temp={TEMPS[ipk]} (chi={chis[ipk]:.3f}) vs ends "
      f"{chis[0]:.3f}/{chis[-1]:.3f}")

    # C3 control = mass
    ctrl = flocking_sweep(gamma=0.6, topology="annealed")
    chis_c = np.array([ctrl[t]["chi"] for t in TEMPS])
    dm_hi = ctrl[1.4]["m"] - free[1.4]["m"]
    c3 = dm_hi >= 0.10 and chis_c.max() < chis.max()
    R("C3 control = mass (rounds the transition)", c3,
      f"m(1.4): {free[1.4]['m']:.3f}(γ=0)->{ctrl[1.4]['m']:.3f}(γ=0.6) Δ={dm_hi:+.3f} (>=0.10?); "
      f"chi_peak {chis.max():.3f}->{chis_c.max():.3f} (suppressed?)")

    # M motility gating (annealed orders more than quenched at low temp)
    quench = flocking_sweep(gamma=0.0, topology="quenched", temps=[0.2])
    dm_mot = free[0.2]["m"] - quench[0.2]["m"]
    M = dm_mot >= 0.10
    R("M motility gating (Mermin-Wagner direction)", M,
      f"m(0.2): annealed={free[0.2]['m']:.3f} - quenched={quench[0.2]['m']:.3f} "
      f"= {dm_mot:+.3f} (>=0.10?)")

    results["flocking"] = dict(free=free, ctrl=ctrl, quench=quench,
                               checks={n: bool(o) for n, o in rec})
    return rec


# --------------------------------------------------------------------------- wave
def wave_run(lag, seeds=SEEDS, k0=0, x0=NW // 2, hw=2, amp=3.0, t0=2, salient=False):
    """Run the ring economy with a localized value-shock; return the per-round,
    seed-averaged adoption profile of k0 (length NW) and the leading-edge distance."""
    profiles_all = []
    for s in seeds:
        ec = LLMEconomy(N=NW, model=MODEL, temp=0.4, J=1.0, topology="ring",
                        ring_k=2, lag=lag, seed=s, salient=salient)
        ec.shock = (k0, x0, hw, amp); ec.shock_t0 = t0
        r = ec.run(T=TW, burn=0, record_profile_k=k0)
        profiles_all.append(r["profiles"])              # (TW, NW)
    prof = np.mean(profiles_all, axis=0)                 # seed-averaged adoption
    # baseline = pre-shock adoption (rounds < t0), subtract to get the perturbation
    base = prof[:t0].mean(axis=0) if t0 > 0 else 0.0
    pert = np.clip(prof - base, 0, None)
    # leading-edge distance from x0: farthest position (ring metric) with adoption>0.5
    dist = np.array([min(abs(i - x0), NW - abs(i - x0)) for i in range(NW)])
    edges, sig2 = [], []
    for t in range(TW):
        on = np.where(pert[t] > 0.5)[0]
        edges.append(float(dist[on].max()) if len(on) else 0.0)
        w = pert[t]; tot = w.sum()
        sig2.append(float((w * dist ** 2).sum() / tot) if tot > 1e-9 else 0.0)
    return dict(profile=prof.tolist(), edge=edges, sig2=sig2, t0=t0)


def _fit_lin_sqrt(t, y):
    if len(t) < 4:
        return -1.0, -1.0
    t = np.asarray(t, float); y = np.asarray(y, float)
    A = np.sum(t * y) / np.sum(t * t); st = np.sqrt(t)
    B = np.sum(st * y) / np.sum(st * st)
    tot = np.sum((y - y.mean()) ** 2) + 1e-12
    r2 = lambda m: 1 - np.sum((y - m) ** 2) / tot
    return r2(A * t), r2(B * st)


def run_wave(results):
    print("\nSIGNATURE 1 — demand wave (SECONDARY)")
    rec = []
    def R(name, ok, detail):
        rec.append((name, ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

    wL = wave_run(lag=3); w0 = wave_run(lag=0)
    t0 = wL["t0"]
    # post-shock window
    tt = np.arange(TW - t0)
    edgeL = np.array(wL["edge"][t0:]); edge0 = np.array(w0["edge"][t0:])
    s2L = np.array(wL["sig2"][t0:]); s20 = np.array(w0["sig2"][t0:])
    print(f"    L=3 leading edge by round: {np.round(edgeL,1).tolist()}")
    print(f"    L=0 leading edge by round: {np.round(edge0,1).tolist()}")

    # W-wave (L=3): edge propagates ∝ t, travels >= 4 sites
    r2lin_L, r2sqrt_L = _fit_lin_sqrt(tt + 1, edgeL)
    wwave = r2lin_L > 0.8 and edgeL.max() >= 4
    R("W-wave (L=3): adoption front propagates ∝ t", wwave,
      f"R²_lin={r2lin_L:.3f} (>0.8?); front travels {edgeL.max():.1f} sites (>=4?)")

    # W-diff (L=0): peak pinned (edge travel small) AND σ² ∝ t fits better than ∝ t²
    A = np.sum(tt * s20) / np.sum(tt * tt + 1e-12)
    B = np.sum(tt ** 2 * s20) / np.sum(tt ** 4 + 1e-12)
    tot = np.sum((s20 - s20.mean()) ** 2) + 1e-12
    r2lin_s2 = 1 - np.sum((s20 - A * tt) ** 2) / tot
    r2quad_s2 = 1 - np.sum((s20 - B * tt ** 2) ** 2) / tot
    wdiff = edge0.max() <= 2 and r2lin_s2 >= r2quad_s2
    R("W-diff (L=0): spreads in place (diffusion)", wdiff,
      f"front travels {edge0.max():.1f} sites (<=2?); σ²∝t R²={r2lin_s2:.3f} vs σ²∝t² R²={r2quad_s2:.3f}")

    # W-gate: inertia gates the wave
    wgate = wwave and wdiff
    R("W-gate: wave gated by reallocation inertia (L>0 wave, L=0 diffusion)", wgate,
      f"L=3 {'wave' if wwave else 'no-wave'}; L=0 {'diffusion' if wdiff else 'not-diffusion'}")

    results["wave"] = dict(L3=wL, L0=w0, checks={n: bool(o) for n, o in rec})
    return rec


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    ok, msg = __import__("llm_economy").health_check()
    if not ok:
        print(f"HEALTH FAIL ({msg}) — is the SSH tunnel up? aborting."); return False
    print("=" * 78)
    print(f"Rung 7 — real-LLM-agent field test ({MODEL}). Thresholds: PREREGISTRATION.md")
    print("=" * 78)
    results, rec = {}, []
    t0 = time.time()
    if which in ("all", "flocking"):
        rec += run_flocking(results)
    if which in ("all", "wave"):
        rec += run_wave(results)
    json.dump(results, open(os.path.join(OUT, f"real_results_{MTAG}.json"), "w"), indent=2)
    n_pass = sum(1 for _, o in rec if o)
    print("\n" + "=" * 78)
    print(f"SUMMARY: {n_pass}/{len(rec)} checks passed  ({time.time()-t0:.0f}s)  "
          f"-> results/real_results.json")
    for n, o in rec:
        print(f"  {'PASS' if o else 'FAIL'}  {n}")
    print("=" * 78)
    return n_pass == len(rec)


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)

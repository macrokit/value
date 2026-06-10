"""
lever1_stage1.py — Maxwell Stage 1: the ‖Vg‖/γ redo with the de-saturated design.

Implements PREREGISTRATION_stage1.md (frozen before this file ran):
  K=16 niches, TENT reward landscape (peak k_g=12, slope ±g), k*=0,
  grid g ∈ {0.25, 0.7, 2.0} × γ ∈ {2, 6, 18}, seeds 0..7,
  direction-test arms at B1 (γ=6,g=0.7) and B2 (γ=18,g=0.7) with δ=0.5.

Same instrument as doc 13 (qwen2.5:1.5b-instruct, symbol-randomisation, temp 0.6,
N=20, T=18, J=1, annealed n_nb=6) — the fix is the design, not the model.

Raw per-run measurements are appended incrementally to results/stage1_raw.json so the
run is restart-safe (every LLM call is also cached in cache.sqlite). The frozen
decision rule is applied separately by analyze_stage1.py (cache-only).

Run (tunnel must be live):
  python3 sim/field/real/lever1_stage1.py

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from llm_economy import LLMEconomy, health_check

MODEL = "qwen2.5:1.5b-instruct"
OUT   = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(OUT, exist_ok=True)
RAW_PATH = os.path.join(OUT, "stage1_raw.json")

# ── frozen design (PREREGISTRATION_stage1.md §1) ─────────────────────────────
K       = 16
K_STAR  = 0
K_G     = 12          # tent peak
J       = 1.0
TEMP    = 0.6
N       = 20
T_WARM  = 6
T_MEAS  = 12
T_TOTAL = T_WARM + T_MEAS
SEEDS   = list(range(8))
N_NB    = 6
POOL    = 8

GS      = [0.25, 0.7, 2.0]
GAMMAS  = [2.0, 6.0, 18.0]
B_DELTA = 0.5
B_POINTS = [("B1", 6.0, 0.7), ("B2", 18.0, 0.7)]


def tent_rewards(g: float) -> np.ndarray:
    """rewards[k] = g·(k_g − |k − k_g|): slope ±g, peak 12g at k=12, 0 at k=0."""
    ks = np.arange(K)
    return g * (K_G - np.abs(ks - K_G))


def load_raw() -> dict:
    if os.path.exists(RAW_PATH):
        with open(RAW_PATH) as f:
            return json.load(f)
    return {}


def save_raw(raw: dict):
    tmp = RAW_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(raw, f, indent=1)
    os.replace(tmp, RAW_PATH)


def run_condition(gamma: float, g: float, seed: int) -> dict:
    """One (γ, g, seed) run. Measurements in TRUE niche space."""
    ec = LLMEconomy(
        N=N, model=MODEL, temp=TEMP, J=J,
        gamma=gamma, k_star=K_STAR,
        topology="annealed", n_nb=N_NB,
        seed=seed, pool=POOL,
        symbol_random=True,        # mandatory bias control
        k=K,
    )
    ec.rewards = tent_rewards(g)

    k_bar_hist, V_hist, above_cnt, tot_cnt = [], [], 0, 0
    for rnd in range(T_TOTAL):
        ec.step(rnd)
        if rnd >= T_WARM:
            k_bar_hist.append(float(np.mean(ec.niche)))
            V_hist.append(float(np.var(ec.niche)))
            above_cnt += int(np.sum(ec.niche > K_G))
            tot_cnt += N

    return {
        "gamma": gamma, "g": g, "seed": seed,
        "k_bar_ss": float(np.mean(k_bar_hist)),
        "V_ss": float(np.mean(V_hist)),
        "residual_ss": float(np.mean(k_bar_hist)) - K_STAR,
        "frac_above_peak": above_cnt / max(tot_cnt, 1),
        "parse_rate": ec.parse_ok / max(ec.parse_tot, 1),
    }


def main():
    ok, msg = health_check()
    if not ok:
        print(f"HEALTH FAIL — tunnel/model not live: {msg}")
        raise SystemExit(1)
    print(f"Health: OK ({msg})", flush=True)

    raw = load_raw()
    t0 = time.time()

    # work list: A grid + B arms (B r0 points are grid conditions, reused)
    work = [("A", gamma, g) for gamma in GAMMAS for g in GS]
    for bid, gamma, g in B_POINTS:
        work.append((f"{bid}_dgamma", gamma + B_DELTA, g))
        work.append((f"{bid}_dg",     gamma,           g - B_DELTA))

    n_total = len(work) * len(SEEDS)
    n_done = 0
    print(f"STAGE-1 RUN: {len(work)} conditions x {len(SEEDS)} seeds "
          f"= {n_total} runs (~{n_total * N * T_TOTAL} calls, cached)", flush=True)

    for tag, gamma, g in work:
        key = f"{tag}|gamma={gamma}|g={g}"
        runs = raw.get(key, [])
        done_seeds = {r["seed"] for r in runs}
        for seed in SEEDS:
            if seed in done_seeds:
                n_done += 1
                continue
            r = run_condition(gamma, g, seed)
            runs.append(r)
            raw[key] = runs
            save_raw(raw)
            n_done += 1
            el = time.time() - t0
            print(f"[{n_done}/{n_total}] {key} seed={seed}: "
                  f"k̄={r['k_bar_ss']:.3f} V={r['V_ss']:.2f} "
                  f"res={r['residual_ss']:.3f} above_peak={r['frac_above_peak']:.2f} "
                  f"parse={r['parse_rate']:.2f}  ({el/60:.1f} min)", flush=True)

    print(f"\nALL RUNS COMPLETE in {(time.time()-t0)/60:.1f} min → {RAW_PATH}", flush=True)


if __name__ == "__main__":
    main()

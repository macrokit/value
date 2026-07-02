"""
stage2b.py — Stage 2, experiment 2B: the ‖Vg‖/γ grid on the frontier instrument.

The Stage-1 frozen design verbatim (PREREGISTRATION.md §3): K=16 tent landscape,
N=20, T=18 (6+12), J=1, symbol-randomisation, g ∈ {0.25,0.7,2.0} × γ ∈ {2,6,18},
seeds 0..7, direction arms B1/B2 with δ=0.5 — driven by claude-opus-4-8 via the
cached, cap-metered API backend. Incremental + restart-safe (results/stage2b_raw.json).

Usage:
  ANTHROPIC_API_KEY=... python3 sim/stage2/stage2b.py

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "field", "real"))
sys.path.insert(0, HERE)
from llm_economy import LLMEconomy                       # noqa: E402
from lever1_stage1 import tent_rewards, K, K_G, K_STAR   # noqa: E402
import api_client                                        # noqa: E402

MODEL = os.environ.get("STAGE2_MODEL", "claude-opus-4-8")
CAP_USD = 160.0
RAW_PATH = os.path.join(api_client.RESULTS, "stage2b_raw.json")

# frozen design (identical to Stage 1)
N, T_WARM, T_MEAS = 20, 6, 12
T_TOTAL = T_WARM + T_MEAS
SEEDS = list(range(8))
J, N_NB = 1.0, 6
POOL = 12          # operational concurrency only (API tier-2); not design
GS = [0.25, 0.7, 2.0]
GAMMAS = [2.0, 6.0, 18.0]
B_DELTA = 0.5
B_POINTS = [("B1", 6.0, 0.7), ("B2", 18.0, 0.7)]


def load_raw():
    if os.path.exists(RAW_PATH):
        with open(RAW_PATH) as f:
            return json.load(f)
    return {}

def save_raw(raw):
    tmp = RAW_PATH + ".tmp"
    with open(tmp, "w") as f:
        json.dump(raw, f, indent=1)
    os.replace(tmp, RAW_PATH)


def run_condition(chat_fn, gamma, g, seed):
    ec = LLMEconomy(N=N, model=MODEL, temp=None, J=J, gamma=gamma, k_star=K_STAR,
                    topology="annealed", n_nb=N_NB, seed=seed, pool=POOL,
                    symbol_random=True, k=K, chat_fn=chat_fn)
    ec.rewards = tent_rewards(g)
    kbar, V, above, tot = [], [], 0, 0
    for rnd in range(T_TOTAL):
        ec.step(rnd)
        if rnd >= T_WARM:
            kbar.append(float(np.mean(ec.niche)))
            V.append(float(np.var(ec.niche)))
            above += int(np.sum(ec.niche > K_G)); tot += N
    return {"gamma": gamma, "g": g, "seed": seed,
            "k_bar_ss": float(np.mean(kbar)), "V_ss": float(np.mean(V)),
            "residual_ss": float(np.mean(kbar)) - K_STAR,
            "frac_above_peak": above / max(tot, 1),
            "parse_rate": ec.parse_ok / max(ec.parse_tot, 1)}


def main():
    ok, msg = api_client.health_check(MODEL, cap_usd=CAP_USD)
    if not ok:
        print(f"HEALTH FAIL ({MODEL}): {msg}")
        raise SystemExit(1)
    print(f"Health OK: {MODEL}  (spent so far ${api_client.spent_usd():.2f})", flush=True)
    chat_fn = api_client.make_chat(MODEL, cap_usd=CAP_USD, max_tokens=200)

    work = [("A", gamma, g) for gamma in GAMMAS for g in GS]
    for bid, gamma, g in B_POINTS:
        work.append((f"{bid}_dgamma", gamma + B_DELTA, g))
        work.append((f"{bid}_dg",     gamma,           g - B_DELTA))

    raw = load_raw()
    n_total, n_done, t0 = len(work) * len(SEEDS), 0, time.time()
    print(f"STAGE-2B: {len(work)} conditions × {len(SEEDS)} seeds = {n_total} runs "
          f"(~{n_total*N*T_TOTAL} calls, cached, cap ${CAP_USD})", flush=True)

    for tag, gamma, g in work:
        key = f"{tag}|gamma={gamma}|g={g}"
        runs = raw.get(key, [])
        done = {r["seed"] for r in runs}
        for seed in SEEDS:
            if seed in done:
                n_done += 1
                continue
            try:
                r = run_condition(chat_fn, gamma, g, seed)
            except api_client.BudgetExceeded as e:
                print(f"BUDGET STOP: {e} — stopping per prereg §5; "
                      f"completed {n_done}/{n_total}", flush=True)
                raise SystemExit(2)
            runs.append(r); raw[key] = runs; save_raw(raw); n_done += 1
            print(f"[{n_done}/{n_total}] {key} seed={seed}: "
                  f"k̄={r['k_bar_ss']:.3f} V={r['V_ss']:.2f} res={r['residual_ss']:.3f} "
                  f"above={r['frac_above_peak']:.2f} parse={r['parse_rate']:.2f} "
                  f"(${api_client.spent_usd():.2f}, {(time.time()-t0)/60:.0f} min)",
                  flush=True)

    print(f"\nALL RUNS COMPLETE in {(time.time()-t0)/60:.1f} min → {RAW_PATH} "
          f"(spent ${api_client.spent_usd():.2f})", flush=True)


if __name__ == "__main__":
    main()

"""
gate.py — Stage 2 responsiveness gate (G-1/G-2/G-3), per PREREGISTRATION-gate.md (frozen).

Drives the EXACT Stage-1/2B niche economy (sim/field/real/llm_economy.LLMEconomy) on a
frontier API model via the cached api_client backend. Applies the frozen pass/fail
thresholds and decision rule mechanically; writes results/gate_results.json.

Usage:
  ANTHROPIC_API_KEY=...  python3 sim/stage2/gate.py --tier debug      # Sonnet, NOT a verdict
  ANTHROPIC_API_KEY=...  python3 sim/stage2/gate.py --tier frontier   # Opus, the verdict
  python3 sim/stage2/gate.py --tier mock                              # offline, no spend

Models (override via env): GATE_FRONTIER_MODEL, GATE_DEBUG_MODEL. The model actually
used is recorded in gate_results.json and docs/19.

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json, argparse
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "field", "real"))
sys.path.insert(0, HERE)
from llm_economy import LLMEconomy            # noqa: E402
from lever1_stage1 import tent_rewards, K, K_G, K_STAR   # noqa: E402  (K=16, K_G=12)
import api_client                              # noqa: E402

# ── frozen gate parameters (PREREGISTRATION-gate.md §2–§3) ───────────────────
N, T_WARM, T_MEAS = 12, 4, 4
T_TOTAL = T_WARM + T_MEAS
SEEDS = [0, 1, 2, 3]
TEMP, J, N_NB = 0.6, 1.0, 6
POOL = 6
LN2 = float(np.log(2))

# frozen thresholds
G1_GAMMA, G1_G = 18.0, 0.0
G1_KBAR_MAX, G1_SEEDS_REQ = 5.5, 3          # k̄ ≤ 5.5 in ≥ 3/4 seeds
G2_GAMMA, G2_G = 0.0, 0.7
G2_KBAR_MIN, G2_SEEDS_REQ = 9.5, 3          # k̄ ≥ 9.5 in ≥ 3/4 seeds
G3_AGENTS = [0, 1, 2]                        # bit index each agent reveals
G3_REPS = 8
G3_INFO_MIN = 0.5 * LN2                      # 0.3466 nats
G3_AGENTS_REQ = 2                            # ≥ 2/3 agents individually

# Current latest IDs as defaults; override via env to whatever the owner's key can
# access. The model actually used is recorded in gate_results.json + docs/19.
DEFAULT_FRONTIER = os.environ.get("GATE_FRONTIER_MODEL", "claude-opus-4-8")
DEFAULT_DEBUG    = os.environ.get("GATE_DEBUG_MODEL", "claude-sonnet-4-6")
HARD_CAP_USD = 30.0


# ── G-1 / G-2: niche-economy responsiveness ──────────────────────────────────
def run_niche_condition(chat_fn, model, gamma, g, seed):
    ec = LLMEconomy(N=N, model=model, temp=TEMP, J=J, gamma=gamma, k_star=K_STAR,
                    topology="annealed", n_nb=N_NB, seed=seed, pool=POOL,
                    symbol_random=True, k=K, chat_fn=chat_fn)
    ec.rewards = tent_rewards(g)
    kbar = []
    for rnd in range(T_TOTAL):
        ec.step(rnd)
        if rnd >= T_WARM:
            kbar.append(float(np.mean(ec.niche)))
    return {"seed": seed, "k_bar_ss": float(np.mean(kbar)),
            "parse_rate": ec.parse_ok / max(ec.parse_tot, 1)}


# ── G-3: perception (belief elicitation) ─────────────────────────────────────
def _elicit_prompt(bit_j, v):
    place = 2 ** bit_j
    return (
        "A hidden number X is drawn uniformly at random from 0 to 7 (each equally "
        "likely). Written in 3 bits, X = 4*b2 + 2*b1 + 1*b0.\n"
        f"You receive one clean observation: bit b{bit_j} (the {place}s place) of X "
        f"is {v}.\n"
        "Give your probability that X equals each value 0..7, using the observation.\n"
        'Respond ONLY as JSON: {"probs": [p0, p1, p2, p3, p4, p5, p6, p7]} '
        "(eight non-negative numbers).")

def _parse_probs(txt):
    try:
        arr = json.loads(txt[txt.index("{"):txt.rindex("}") + 1])["probs"]
        p = np.array([float(x) for x in arr], dtype=float)
        if p.shape != (8,) or not np.all(np.isfinite(p)) or p.sum() <= 0:
            return None
        p = np.clip(p, 0, None)
        return p / p.sum()
    except Exception:
        return None

def _kl_to_uniform(p):
    u = np.full(8, 1 / 8)
    p = np.clip(p, 1e-12, None); p = p / p.sum()
    return float(np.sum(p * np.log(p / u)))

def run_g3(chat_fn, model):
    agents = []
    for j in G3_AGENTS:
        post = {}
        parse_fails = 0
        for v in (0, 1):
            acc = []
            for rep in range(G3_REPS):
                txt = chat_fn(model, TEMP, _elicit_prompt(j, v),
                              seed=0, agent=j, rnd=v * 100 + rep, k=8)
                p = _parse_probs(txt)
                if p is None:
                    parse_fails += 1
                else:
                    acc.append(p)
            post[v] = np.mean(acc, axis=0) if acc else np.full(8, 1 / 8)
        info = 0.5 * _kl_to_uniform(post[0]) + 0.5 * _kl_to_uniform(post[1])
        agents.append({"bit": j, "info_nats": info,
                       "frac_of_channel": info / LN2,
                       "parse_fails": parse_fails,
                       "post0": post[0].tolist(), "post1": post[1].tolist()})
    return agents


# ── verdict (frozen decision rule) ───────────────────────────────────────────
def verdict(g1, g2, g3):
    g1_pass_seeds = sum(1 for r in g1 if r["k_bar_ss"] <= G1_KBAR_MAX)
    g2_pass_seeds = sum(1 for r in g2 if r["k_bar_ss"] >= G2_KBAR_MIN)
    g3_mean = float(np.mean([a["info_nats"] for a in g3]))
    g3_agents_pass = sum(1 for a in g3 if a["info_nats"] >= G3_INFO_MIN)

    g1_ok = g1_pass_seeds >= G1_SEEDS_REQ
    g2_ok = g2_pass_seeds >= G2_SEEDS_REQ
    g3_ok = (g3_mean >= G3_INFO_MIN) and (g3_agents_pass >= G3_AGENTS_REQ)
    gate_pass = g1_ok and g2_ok and g3_ok
    return {
        "G1": {"pass": g1_ok, "pass_seeds": g1_pass_seeds, "req": G1_SEEDS_REQ,
               "k_bar_by_seed": [round(r["k_bar_ss"], 3) for r in g1],
               "threshold": f"k̄ ≤ {G1_KBAR_MAX}"},
        "G2": {"pass": g2_ok, "pass_seeds": g2_pass_seeds, "req": G2_SEEDS_REQ,
               "k_bar_by_seed": [round(r["k_bar_ss"], 3) for r in g2],
               "threshold": f"k̄ ≥ {G2_KBAR_MIN}"},
        "G3": {"pass": g3_ok, "mean_info": round(g3_mean, 4),
               "agents_pass": g3_agents_pass, "req_agents": G3_AGENTS_REQ,
               "info_by_agent": [round(a["info_nats"], 4) for a in g3],
               "threshold": f"Î ≥ {G3_INFO_MIN:.4f} nats (0.5·ln2)"},
        "GATE": "PASS" if gate_pass else "FAIL",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", choices=["mock", "debug", "frontier"], required=True)
    args = ap.parse_args()

    if args.tier == "mock":
        from mock_backend import mock_chat
        chat_fn, model, cap = mock_chat, "mock-model", 0.0
    else:
        model = DEFAULT_DEBUG if args.tier == "debug" else DEFAULT_FRONTIER
        ok, msg = api_client.health_check(model)
        if not ok:
            print(f"HEALTH FAIL ({model}): {msg}")
            raise SystemExit(1)
        print(f"Health OK: {model} ({msg})")
        cap = HARD_CAP_USD
        chat_fn = api_client.make_chat(model, cap_usd=cap, max_tokens=64)

    print(f"\n=== STAGE 2 GATE — tier={args.tier} model={model} ===")
    print("Frozen: PREREGISTRATION-gate.md  (N=12, T=8, S=4, K=16)")

    g1 = [run_niche_condition(chat_fn, model, G1_GAMMA, G1_G, s) for s in SEEDS]
    print(f"G-1 (γ={G1_GAMMA}, g={G1_G}) k̄ by seed: {[round(r['k_bar_ss'],2) for r in g1]}")
    g2 = [run_niche_condition(chat_fn, model, G2_GAMMA, G2_G, s) for s in SEEDS]
    print(f"G-2 (γ={G2_GAMMA}, g={G2_G}) k̄ by seed: {[round(r['k_bar_ss'],2) for r in g2]}")
    g3 = run_g3(chat_fn, model)
    print(f"G-3 info by agent (nats): {[round(a['info_nats'],3) for a in g3]}")

    v = verdict(g1, g2, g3)
    spent = api_client.spent_usd() if args.tier != "mock" else 0.0
    out = {"tier": args.tier, "model": model, "spent_usd": round(spent, 4),
           "verdict": v,
           "raw": {"G1": g1, "G2": g2, "G3": g3},
           "frozen": {"N": N, "T": T_TOTAL, "seeds": SEEDS,
                      "uniform_mean": (K - 1) / 2, "uniform_var": (K**2 - 1) / 12}}
    path = os.path.join(api_client.RESULTS,
                        f"gate_results_{args.tier}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)

    print("\n" + "=" * 60)
    for g in ("G1", "G2", "G3"):
        print(f"  {g}: {'PASS' if v[g]['pass'] else 'FAIL'}  {v[g]}")
    print(f"  GATE VERDICT: {v['GATE']}   (spent ${spent:.2f} / cap ${HARD_CAP_USD})")
    print("=" * 60)
    print(f"→ {path}")


if __name__ == "__main__":
    main()

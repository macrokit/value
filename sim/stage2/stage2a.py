"""
stage2a.py — Stage 2, experiment 2A: capacity region & gap law on frontier agents.

Implements PREREGISTRATION.md §2 as amended by PREREGISTRATION-amendment2.md:
  - belief elicitation, 12 reps/cell, for every coalition of every structure
    (A2.1: coalition-level elicitation defines Ĝ_S; product fusion is a secondary
    diagnostic), analysed by EXACT enumeration over each structure's joint atoms;
  - the live parimutuel market (A2.2: heterogeneous BSC ladder + clones).

Usage:
  python3 sim/stage2/stage2a.py --tier mock       # offline; true-posterior+noise agents
  ANTHROPIC_API_KEY=... python3 sim/stage2/stage2a.py --tier frontier

Outputs results/stage2a_reports.json (raw elicited posteriors + market trajectories).
The frozen bands are applied by analyze_stage2.py (cache-only).

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json, argparse, itertools
import concurrent.futures as cf
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import api_client

RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)
OUT_PATH = os.path.join(RESULTS, "stage2a_reports.json")

MODEL = os.environ.get("STAGE2_MODEL", "claude-opus-4-8")
CAP_USD = 160.0
REPS = 12
POOL = 6
LN2 = float(np.log(2))
RNG = np.random.default_rng(23)


# ─────────────────────────────────────────────────────────────────── structures
def bits(x):
    return (x & 1, (x >> 1) & 1, (x >> 2) & 1)   # (b0, b1, b2)

def _obs_bit(j, v):
    return f"bit b{j} of X is {v}"

def _obs_pair(i, j, vi, vj):
    return f"bit b{i} of X is {vi} and bit b{j} of X is {vj}"

def _obs_noisy(j, v, flip):
    return (f"a noisy sensor for bit b{j} of X (it flips its reading with "
            f"probability {flip:.2f}) reports {v}")

WORLD8 = ("A hidden number X is drawn uniformly at random from 0 to 7 (each equally "
          "likely). Written in 3 bits, X = 4*b2 + 2*b1 + 1*b0.")
WORLD2 = ("A hidden fair coin X is either 0 or 1 (each with probability 1/2).")

def make_structures():
    """Each structure: dict(name, n_states, world_text, m, atoms, obs).
    atoms: list of (prob, x, (y_0..y_{m-1})); obs(a, y) -> observation sentence."""
    S = {}

    # (a) disjoint bits
    atoms = [(1 / 8, x, bits(x)) for x in range(8)]
    S["a_disjoint"] = dict(n=8, world=WORLD8, m=3, atoms=atoms,
                           obs=lambda a, y: _obs_bit(a, y))

    # (b) partial overlap: signals (b0,b1),(b1,b2),(b0,b2) encoded y = vi + 2*vj
    def yb(x):
        b0, b1, b2 = bits(x)
        return (b0 + 2 * b1, b1 + 2 * b2, b0 + 2 * b2)
    PAIRS = [(0, 1), (1, 2), (0, 2)]
    atoms = [(1 / 8, x, yb(x)) for x in range(8)]
    S["b_overlap"] = dict(n=8, world=WORLD8, m=3, atoms=atoms,
                          obs=lambda a, y: _obs_pair(PAIRS[a][0], PAIRS[a][1],
                                                     y & 1, (y >> 1) & 1))

    # (c) clones: agents see (b0, b0, b1)
    atoms = [(1 / 8, x, (bits(x)[0], bits(x)[0], bits(x)[1])) for x in range(8)]
    S["c_clones"] = dict(n=8, world=WORLD8, m=3, atoms=atoms,
                         obs=lambda a, y: _obs_bit(0 if a < 2 else 1, y))

    # (d) noisy: bit j through a 10% flip sensor, independent noise
    atoms = []
    for x in range(8):
        b = bits(x)
        for f in itertools.product((0, 1), repeat=3):
            p = (1 / 8) * np.prod([0.9 if fi == 0 else 0.1 for fi in f])
            atoms.append((float(p), x, tuple(b[j] ^ f[j] for j in range(3))))
    S["d_noisy"] = dict(n=8, world=WORLD8, m=3, atoms=atoms,
                        obs=lambda a, y: _obs_noisy(a, y, 0.10))

    # (e) XOR control on the reduced world X' = one fair bit
    atoms = [(1 / 4, xp, (c, xp ^ c)) for xp in range(2) for c in range(2)]
    def obs_e(a, y):
        if a == 0:
            return (f"an independent fair coin C was flipped (it has no connection "
                    f"to X on its own); C = {y}")
        return (f"you see the value of X XOR C = {y}, where C is an independent "
                f"fair coin whose value you do NOT see")
    # A3.2: neutral composition for coalition prompts (the singleton text for agent 2
    # contradicts a coalition prompt that also shows C)
    def obs_e_coal(a, y):
        if a == 0:
            return f"the independent fair coin C = {y}"
        return f"the value of X XOR C = {y}"
    S["e_xor"] = dict(n=2, world=WORLD2, m=2, atoms=atoms, obs=obs_e,
                      obs_coal=obs_e_coal)
    return S


# ─────────────────────────────────────────────────── exact-enumeration helpers
def coalition_cells(st, Sset):
    """Realisable y_S tuples with P(y_S) > 0. Returns {y_S: prob}."""
    out = {}
    for p, x, ys in st["atoms"]:
        key = tuple(ys[a] for a in Sset)
        out[key] = out.get(key, 0.0) + p
    return out

def exact_I(st, Sset):
    """I(X;Y_S) in nats from the atoms."""
    pxy, px, py = {}, {}, {}
    for p, x, ys in st["atoms"]:
        key = tuple(ys[a] for a in Sset)
        pxy[(x, key)] = pxy.get((x, key), 0.0) + p
        px[x] = px.get(x, 0.0) + p
        py[key] = py.get(key, 0.0) + p
    return float(sum(p * np.log(p / (px[x] * py[k]))
                     for (x, k), p in pxy.items() if p > 0))


# ───────────────────────────────────────────────────────────────── elicitation
def elicit_prompt(st, Sset, y_S):
    lines = [st["world"]]
    obs_fn = st.get("obs_coal", st["obs"]) if len(Sset) > 1 else st["obs"]
    if len(Sset) == 1:
        lines.append(f"You receive one observation: {obs_fn(Sset[0], y_S[0])}.")
    else:
        lines.append("You receive the following observations together:")
        for i, a in enumerate(Sset):
            lines.append(f"  - Observation {i + 1}: {obs_fn(a, y_S[i])}")
    n = st["n"]
    ps = ", ".join(f"p{i}" for i in range(n))
    # A3.2: JSON-first protocol — the object must come first, on its own line
    lines.append(f"Give your probability that X equals each value 0..{n-1}, using "
                 "all observations jointly.")
    lines.append(f'Your reply MUST START with the JSON object on its own first line: '
                 f'{{"probs": [{ps}]}} ({n} non-negative numbers summing to 1). '
                 "Any explanation must come AFTER the JSON, never before.")
    return "\n".join(lines)

RETRY_NUDGE = ('\nIMPORTANT: your previous reply was not machine-parseable. '
               'Reply with the JSON object ONLY — first line, nothing before it.')

def _first_json_obj(txt):
    """First parseable JSON object in txt (JSON-first protocol tolerant of trailing
    prose containing braces)."""
    start = txt.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(txt)):
            if txt[i] == "{":
                depth += 1
            elif txt[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(txt[start:i + 1])
                    except Exception:
                        break
        start = txt.find("{", start + 1)
    return None

def parse_probs(txt, n):
    try:
        obj = _first_json_obj(txt)
        arr = obj["probs"]
        p = np.array([float(v) for v in arr], dtype=float)
        if p.shape != (n,) or not np.all(np.isfinite(p)) or p.sum() <= 0:
            return None
        return (np.clip(p, 0, None) / np.clip(p, 0, None).sum())
    except Exception:
        return None

def true_posterior(st, Sset, y_S):
    num = np.zeros(st["n"])
    for p, x, ys in st["atoms"]:
        if tuple(ys[a] for a in Sset) == tuple(y_S):
            num[x] += p
    return num / num.sum()

def run_elicitation(tier, chat_fn, only=None):
    structures = make_structures()
    reports = {}
    cells = []
    for name, st in structures.items():
        if only is not None and name not in only:
            continue
        for size in range(1, st["m"] + 1):
            for Sset in itertools.combinations(range(st["m"]), size):
                for y_S in sorted(coalition_cells(st, Sset)):
                    cells.append((name, Sset, y_S))
    print(f"2A elicitation: {len(cells)} cells × {REPS} reps = {len(cells)*REPS} calls")

    def do_cell(idx_cell):
        idx, (name, Sset, y_S) = idx_cell
        st = structures[name]
        if tier == "mock":
            tp = true_posterior(st, Sset, y_S)
            # true posterior + mild dirichlet noise, averaged over reps
            ps = [RNG.dirichlet(tp * 40 + 0.5) for _ in range(REPS)]
            good = ps
        else:
            prompt = elicit_prompt(st, Sset, y_S)
            good = []
            for rep in range(REPS):
                txt = chat_fn(MODEL, None, prompt, seed=1, agent=idx, rnd=rep, k=8)
                p = parse_probs(txt, st["n"])
                if p is None:   # A3.2: one pre-stated parse-retry (distinct cached rep)
                    txt = chat_fn(MODEL, None, prompt + RETRY_NUDGE,
                                  seed=1, agent=idx, rnd=rep + 1000, k=8)
                    p = parse_probs(txt, st["n"])
                if p is not None:
                    good.append(p)
        mean_p = np.mean(good, axis=0) if good else np.full(st["n"], 1 / st["n"])
        return (name, str(Sset), str(y_S)), {
            "posterior": mean_p.tolist(), "n_good": len(good), "n_reps": REPS,
            "per_rep_sd": (float(np.mean(np.std(good, axis=0))) if len(good) > 1 else None)}

    with cf.ThreadPoolExecutor(max_workers=POOL) as ex:
        for key, val in ex.map(do_cell, enumerate(cells)):
            reports[f"{key[0]}|{key[1]}|{key[2]}"] = val
            if len(reports) % 25 == 0:
                print(f"  {len(reports)}/{len(cells)} cells "
                      f"(spent ${api_client.spent_usd():.2f})", flush=True)
    return reports


# ─────────────────────────────────────────────────────────────── live market
def market_structures():
    """(L) ladder: b0 clean / 10% / 25%. (C) clones: b0, b0, b1 (clean)."""
    return {
        "L_ladder": dict(world=WORLD8, flips=[0.0, 0.10, 0.25], bits_idx=[0, 0, 0]),
        "C_clones": dict(world=WORLD8, flips=[0.0, 0.0, 0.0], bits_idx=[0, 0, 1]),
    }

def market_prompt(world, sensor_desc, obs_v, wealth, last_odds):
    odds = (", ".join(f"x={i}: {o:.3f}" for i, o in enumerate(last_odds))
            if last_odds is not None else "no previous round")
    return (
        f"{world}\nYou are one of 3 bettors in a repeated parimutuel betting game on X.\n"
        f"Your sensor: {sensor_desc}. Your sensor's reading THIS round: {obs_v}.\n"
        f"Your current wealth share: {wealth:.4f}.\n"
        f"Last round's market odds (total bet fraction on each outcome): {odds}.\n"
        "Each round the whole pool is paid to those who bet on the realised X, "
        "pro-rata. You must bet ALL your wealth, split across the 8 outcomes.\n"
        'Your reply MUST START with the JSON object on its own first line: '
        '{"bets": [f0, f1, f2, f3, f4, f5, f6, f7]} (8 non-negative fractions '
        "summing to 1). Any explanation must come AFTER the JSON, never before.")

def parse_bets(txt):
    try:
        obj = _first_json_obj(txt)
        arr = obj["bets"]
        p = np.array([float(v) for v in arr], dtype=float)
        if p.shape != (8,) or not np.all(np.isfinite(p)) or p.sum() <= 0:
            return None
        return np.clip(p, 0, None) / np.clip(p, 0, None).sum()
    except Exception:
        return None

def sensor_desc(bit_idx, flip):
    if flip == 0:
        return f"a clean reading of bit b{bit_idx} of X (always correct)"
    return (f"a noisy reading of bit b{bit_idx} of X — it flips its reading with "
            f"probability {flip:.2f}")

def run_market(tier, chat_fn, rounds=40, seeds=(0, 1, 2, 3, 4)):
    out = {}
    for name, spec in market_structures().items():
        runs = []
        for seed in seeds:
            rng = np.random.default_rng(1000 + seed)
            w = np.full(3, 1 / 3)
            last_odds = None
            traj = [w.tolist()]
            parse_ok = np.zeros(3, dtype=int)
            parse_tot = np.zeros(3, dtype=int)
            for rnd in range(rounds):
                x = int(rng.integers(0, 8))
                b = bits(x)
                bets = np.zeros((3, 8))
                for a in range(3):
                    j, fl = spec["bits_idx"][a], spec["flips"][a]
                    v = b[j] ^ (1 if rng.random() < fl else 0)
                    if tier == "mock":
                        post = np.array([(1 - fl) if bits(z)[j] == v else fl
                                         for z in range(8)]) if fl > 0 else \
                               np.array([1.0 if bits(z)[j] == v else 0.0
                                         for z in range(8)])
                        bets[a] = post / post.sum()
                        parse_ok[a] += 1; parse_tot[a] += 1
                    else:
                        prompt = market_prompt(spec["world"],
                                               sensor_desc(j, fl), v,
                                               float(w[a]), last_odds)
                        txt = chat_fn(MODEL, None, prompt,
                                      seed=seed, agent=a, rnd=rnd + 500, k=8)
                        p = parse_bets(txt)
                        if p is None:   # A3.2: one pre-stated parse-retry
                            txt = chat_fn(MODEL, None, prompt + RETRY_NUDGE,
                                          seed=seed, agent=a, rnd=rnd + 2500, k=8)
                            p = parse_bets(txt)
                        parse_tot[a] += 1
                        if p is not None:
                            parse_ok[a] += 1
                        bets[a] = p if p is not None else np.full(8, 1 / 8)
                B = w @ bets
                w = w * bets[:, x] / max(B[x], 1e-12)
                w = w / w.sum()
                last_odds = B.tolist()
                traj.append(w.tolist())
            pr = (parse_ok / np.maximum(parse_tot, 1)).tolist()
            runs.append({"seed": seed, "final_wealth": w.tolist(),
                         "traj_every5": traj[::5], "parse_by_agent": pr})
            print(f"  market {name} seed={seed}: final w = "
                  f"{[round(v,3) for v in w]} parse={[round(p,2) for p in pr]} "
                  f"(spent ${api_client.spent_usd():.2f})", flush=True)
        out[name] = runs
    return out


# ──────────────────────────────────────────────────────────────────────── main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", choices=["mock", "frontier"], required=True)
    ap.add_argument("--redo", default=None,
                    help="comma list: structures to re-elicit (e.g. b_overlap,d_noisy,"
                         "e_xor) and/or 'market'. Merges into the existing reports "
                         "file per Amendment 3 (passed components kept).")
    args = ap.parse_args()

    chat_fn = None
    if args.tier == "frontier":
        ok, msg = api_client.health_check(MODEL, cap_usd=CAP_USD)
        if not ok:
            print(f"HEALTH FAIL ({MODEL}): {msg}")
            raise SystemExit(1)
        print(f"Health OK: {MODEL}")
        # A3.2: ceiling 900 (JSON-first protocol; explanation allowed after)
        chat_fn = api_client.make_chat(MODEL, cap_usd=CAP_USD, max_tokens=900)

    print(f"=== STAGE 2A — tier={args.tier} model={MODEL} "
          f"redo={args.redo or '(full)'} ===")
    redo = set(args.redo.split(",")) if args.redo else None

    prev = json.load(open(OUT_PATH)) if (redo and os.path.exists(OUT_PATH)) else None
    only_structs = None if redo is None else {s for s in redo if s != "market"}
    reports = run_elicitation(args.tier, chat_fn, only=only_structs)
    market = (run_market(args.tier, chat_fn)
              if (redo is None or "market" in redo) else prev["market"])
    if prev:
        merged = dict(prev["elicitation"])
        merged.update(reports)          # re-run cells replace; others kept (A3.3)
        reports = merged

    out = {"tier": args.tier, "model": MODEL,
           "spent_usd": round(api_client.spent_usd(), 4) if args.tier != "mock" else 0.0,
           "protocol": "A3.2 (json-first, ceiling 900, parse-retry)" if redo or True else "",
           "redo": args.redo,
           "elicitation": reports, "market": market}
    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=1)
    print(f"→ {OUT_PATH}  (spent ${out['spent_usd']})")


if __name__ == "__main__":
    main()

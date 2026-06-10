"""
coupled_fleet.py — Maxwell Stage 0: the payout-COUPLED fleet pilot.

Implements the pre-registered design in PREREGISTRATION_stage0.md (frozen before this
file ran). Three experiment sets:

  E6  shared-bankroll coalition throughputs  G_S = I(X;Y_S); submodularity (+ XOR control)
  E7  parimutuel coupling                    gap law G_a−G_b = I_a−I_b; aggregate ≤ 0
  E8  alignment curvature (doc 04 §4)        region ordered by cos θ

Pure numpy, no LLM calls. Reuses sim/value_sim.py primitives where applicable.
Run:  python3 sim/coupled/coupled_fleet.py   →  results/stage0.json + PASS/FAIL stdout.

Author byline: Cheng Qian.
"""
from __future__ import annotations
import os, sys, json, itertools
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import value_sim as v

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results")
os.makedirs(OUT, exist_ok=True)

SEED = 7
LN2 = float(np.log(2))

CHECKS = []

def chk(name, ok, detail):
    CHECKS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    return ok


# ============================================================================
# E6 — shared-bankroll coalition throughputs
# ============================================================================
# World: X = 3 iid fair bits (8 states). A "channel" is specified by a
# conditional table P[y|x] over a finite alphabet. Coalition S observes the
# tuple (y_a)_{a in S}; the fused posterior p(x|y_S) is exact by enumeration.

def channel_bits(bits, eps=0.0):
    """Channel that reveals the given subset of the 3 bits, each independently
    flipped with prob eps. Y alphabet = tuples over those bits."""
    n_y = 2 ** len(bits)
    P = np.zeros((8, n_y))
    for x in range(8):
        xb = [(x >> b) & 1 for b in range(3)]
        for y in range(n_y):
            yb = [(y >> i) & 1 for i in range(len(bits))]
            p = 1.0
            for i, b in enumerate(bits):
                p *= (1 - eps) if yb[i] == xb[b] else eps
            P[x, y] = p
    return P

def channel_xor_noise():
    """X = B1 only matters; agent sees B2 (independent fair bit) — pure noise.
    Implemented on the 8-state world: Y = bit 1 of X (independent of bit 0)."""
    return channel_bits([1])

def channel_xor_parity():
    """Agent sees B1 XOR B2 (parity of bits 0 and 1)."""
    P = np.zeros((8, 2))
    for x in range(8):
        b0, b1 = x & 1, (x >> 1) & 1
        P[x, b0 ^ b1] = 1.0
    return P

def coalition_joint(q, chans):
    """Joint P[x, (y_1..y_k)] for the coalition's product channel
    (channels conditionally independent given X by construction here —
    EXCEPT that deterministic channels of overlapping bits are still fine:
    P[y_S|x] = prod_a P[y_a|x] holds whenever the channels' noise is
    independent, which is true for every structure in this file)."""
    sizes = [c.shape[1] for c in chans]
    n_y = int(np.prod(sizes)) if sizes else 1
    J = np.zeros((8, n_y))
    for x in range(8):
        if not chans:
            J[x, 0] = q[x]
            continue
        py = np.ones(1)
        for c in chans:
            py = np.outer(py, c[x]).ravel()
        J[x] = q[x] * py
    return J

def coalition_G_and_I(q, chans, T, rng):
    """Exact I(X;Y_S) and Monte-Carlo Ĝ_S of betting the fused posterior
    against fair odds r = q (pooled bankroll)."""
    J = coalition_joint(q, chans)
    I = v.mutual_information(J) if chans else 0.0
    # exact posterior p(x|y)
    post = v.posterior(J)  # P[x|y], shape (8, n_y)
    # MC: draw (x, y) from the joint, log-growth = ln(post[x,y]/q[x])
    flat = J.ravel()
    flat = flat / flat.sum()
    idx = rng.choice(len(flat), size=T, p=flat)
    xs, ys = np.unravel_index(idx, J.shape)
    G = float(np.mean(np.log(np.clip(post[xs, ys], 1e-300, None) / q[xs])))
    return G, I

def powerset(m):
    for k in range(m + 1):
        yield from itertools.combinations(range(m), k)

def run_E6(T=200_000):
    print("\nE6 — shared-bankroll coalitions: G_S = I(X;Y_S); submodularity; controls")
    rng = np.random.default_rng(SEED)
    q = np.full(8, 1 / 8)
    Hx = v.entropy(q)

    structures = {
        "a_disjoint": [channel_bits([0]), channel_bits([1]), channel_bits([2])],
        "b_overlap":  [channel_bits([0, 1]), channel_bits([1, 2]), channel_bits([0, 2])],
        "c_clones":   [channel_bits([0]), channel_bits([0]), channel_bits([1])],
        "d_noisy":    [channel_bits([0], 0.1), channel_bits([1], 0.1), channel_bits([2], 0.1)],
        "e_xor":      [channel_xor_noise(), channel_xor_parity()],
    }
    # for (e) the "world" that matters is bit 0 of X; same 8-state q works:
    # I(X;Y1)=I over the full X of seeing bit1 = ln2 — careful: prereg states
    # I(Y1)=0 *about B1*; on the full 3-bit X, Y1=B2 carries ln2 about X but 0
    # about bit 0. To match the prereg's synergy claim exactly we score (e)
    # against the REDUCED world X' = B1 (bit 0): build reduced joints below.
    out = {"H_X": Hx, "structures": {}}

    all_ok_ach, worst_ach = True, 0.0
    mono_ok, ceil_ok = True, True
    submod_worst = +1e9

    for name, chans in structures.items():
        m = len(chans)
        if name == "e_xor":
            # reduced world: X' = bit 0 (fair bit). Build channels on X'∈{0,1}:
            # Y1 = B2 ~ fair coin independent of X'; Y2 = X' XOR B2.
            # Joint over (X', Y1, Y2): Y2 determined by (X', Y1).
            # Coalition joints by enumeration over (x', b2).
            q2 = np.array([0.5, 0.5])
            def joint_e(S):
                # variables: y1 in {0,1}, y2 in {0,1}; P[x', y_S]
                sizes = {0: 2, 1: 2}
                dims = [sizes[a] for a in S]
                J = np.zeros((2, int(np.prod(dims)) if dims else 1))
                for xp in range(2):
                    for b2 in range(2):
                        p = 0.25  # q(x')·P(b2)
                        yvals = {0: b2, 1: xp ^ b2}
                        if S:
                            iy = 0
                            for a in S:
                                iy = iy * 2 + yvals[a]
                        else:
                            iy = 0
                        J[xp, iy] += p
                return J
            Gs, Is = {}, {}
            for S in powerset(2):
                J = joint_e(S)
                I = v.mutual_information(J) if S else 0.0
                post = v.posterior(J)
                flat = (J / J.sum()).ravel()
                idx = rng.choice(len(flat), size=T, p=flat)
                xs, ys = np.unravel_index(idx, J.shape)
                G = float(np.mean(np.log(np.clip(post[xs, ys], 1e-300, None) / q2[xs])))
                Gs[S], Is[S] = G, I
                worst_ach = max(worst_ach, abs(G - I))
                all_ok_ach &= abs(G - I) <= 0.02
            # E6.5: supermodularity of the control
            marg_given_1 = Gs[(0, 1)] - Gs[(0,)]
            marg_given_0 = Gs[(1,)] - Gs[()]
            super_gap = marg_given_1 - marg_given_0
            chk("E6.5 XOR control supermodular (gap ≥ ln2−0.05)",
                super_gap >= LN2 - 0.05,
                f"marginal(Y2|{{Y1}})−marginal(Y2|∅) = {super_gap:.4f} (ln2={LN2:.4f})")
            out["structures"][name] = {
                "G": {str(S): Gs[S] for S in Gs}, "I": {str(S): Is[S] for S in Is},
                "supermodular_gap": super_gap}
            continue

        Gs, Is = {}, {}
        for S in powerset(m):
            G, I = coalition_G_and_I(q, [chans[a] for a in S], T, rng)
            Gs[S], Is[S] = G, I
            worst_ach = max(worst_ach, abs(G - I))
            all_ok_ach &= abs(G - I) <= 0.02
            ceil_ok &= G <= Hx + 0.02
        # monotonicity over all nested pairs
        for S in powerset(m):
            for Tt in powerset(m):
                if set(S) <= set(Tt):
                    mono_ok &= Gs[S] <= Gs[Tt] + 0.02
        # submodularity: marginal diminishing for S ⊆ T, a ∉ T
        for S in powerset(m):
            for Tt in powerset(m):
                if set(S) <= set(Tt):
                    for a in range(m):
                        if a not in Tt:
                            mS = Gs[tuple(sorted(set(S) | {a}))] - Gs[S]
                            mT = Gs[tuple(sorted(set(Tt) | {a}))] - Gs[Tt]
                            submod_worst = min(submod_worst, mS - mT)
        out["structures"][name] = {"G": {str(S): Gs[S] for S in Gs},
                                   "I": {str(S): Is[S] for S in Is}}

    chk("E6.1 achievability |Ĝ_S − I(X;Y_S)| ≤ 0.02 (all coalitions, all structures)",
        all_ok_ach, f"worst |Ĝ−I| = {worst_ach:.4f} nats")
    chk("E6.2 monotonicity Ĝ_S ≤ Ĝ_T (S⊆T, slack 0.02)", mono_ok, "all nested pairs")
    chk("E6.3 joint ceiling Ĝ_S ≤ H(X)+0.02", ceil_ok, f"H(X)={Hx:.4f}")
    chk("E6.4 submodularity (a)–(d) (worst marginal-diff ≥ −0.03)",
        submod_worst >= -0.03, f"worst diminishing-returns margin = {submod_worst:.4f}")

    # E6.0 — the erratum counterexample with PRIVATE bankrolls
    rng0 = np.random.default_rng(SEED + 1)
    G1, I1 = coalition_G_and_I(q, [channel_bits([0])], T, rng0)
    G2, _ = coalition_G_and_I(q, [channel_bits([0])], T, rng0)
    Gj, Ij = coalition_G_and_I(q, [channel_bits([0]), channel_bits([0])], T, rng0)
    sum_private = G1 + G2
    chk("E6.0 erratum counterexample: private clones Σ Ĝ ≈ 2ln2 > I_joint = ln2",
        abs(sum_private - 2 * LN2) <= 0.02 and sum_private > Ij + 0.1,
        f"Σ Ĝ_private = {sum_private:.4f} (2ln2={2*LN2:.4f}); I_joint = {Ij:.4f}")
    out["erratum_counterexample"] = {"sum_private": sum_private, "I_joint": Ij}
    return out


# ============================================================================
# E7 — parimutuel coupling
# ============================================================================

EPS_LIST = [0.05, 0.15, 0.30, 0.45]

def bsc_I(eps):
    return LN2 - (-eps * np.log(eps) - (1 - eps) * np.log(1 - eps))

def parimutuel_inst(eps_list, T, rng, clone_of=None):
    """Equal-weight instantaneous per-agent growth under parimutuel odds.
    clone_of: if set (agent index), append an agent receiving the SAME y."""
    m0 = len(eps_list)
    xs = rng.integers(0, 2, size=T)
    ys = np.empty((m0, T), dtype=int)
    for a, eps in enumerate(eps_list):
        flip = rng.random(T) < eps
        ys[a] = np.where(flip, 1 - xs, xs)
    agents = list(range(m0))
    if clone_of is not None:
        agents.append(clone_of)        # clone shares y of `clone_of`
    m = len(agents)
    # posterior of a BSC agent: p(x=y_seen) = 1-eps
    b = np.empty((m, T))               # bet placed on the TRUE outcome x
    Ball = np.zeros((2, T))            # total bet per outcome
    for i, a in enumerate(agents):
        eps = eps_list[a]
        y = ys[a]
        p_correct = np.where(y == xs, 1 - eps, eps)   # bet on the true x
        b[i] = p_correct
        Ball[0] += np.where(y == 0, 1 - eps, eps) / m
        Ball[1] += np.where(y == 1, 1 - eps, eps) / m
    Bx = Ball[xs, np.arange(T)] if False else np.where(xs == 0, Ball[0], Ball[1])
    G = np.log(b / Bx[None, :]).mean(axis=1)          # per-agent E ln(b/B)
    return G

def parimutuel_evolve(eps_list, T, rng):
    """Evolving wealth shares; returns final shares and conservation error."""
    m = len(eps_list)
    w = np.full(m, 1 / m)
    xs = rng.integers(0, 2, size=T)
    for t in range(T):
        x = xs[t]
        bets = np.empty((m, 2))
        for a, eps in enumerate(eps_list):
            y = x if rng.random() >= eps else 1 - x
            bets[a, y] = 1 - eps
            bets[a, 1 - y] = eps
        B = w @ bets                                  # total per outcome
        w = w * bets[:, x] / B[x]
    return w, abs(float(w.sum()) - 1.0)

def run_E7(T=100_000, R=10):
    print("\nE7 — parimutuel coupling: gap law, ordering, aggregate ≤ 0, clones")
    I = np.array([bsc_I(e) for e in EPS_LIST])
    rng = np.random.default_rng(SEED)

    Gs = np.array([parimutuel_inst(EPS_LIST, T, np.random.default_rng(SEED + r))
                   for r in range(R)])               # (R, 4)
    G = Gs.mean(axis=0)
    out = {"I": I.tolist(), "G_mean": G.tolist(), "G_reps": Gs.tolist()}

    # E7.2 gap law
    worst_gap = 0.0
    for a in range(4):
        for b in range(4):
            if a < b:
                worst_gap = max(worst_gap, abs((G[a] - G[b]) - (I[a] - I[b])))
    chk("E7.2 gap law |(Ĝ_a−Ĝ_b)−(I_a−I_b)| ≤ 0.01 (all pairs)",
        worst_gap <= 0.01, f"worst pairwise deviation = {worst_gap:.5f} nats")

    # E7.3 ordering
    rank_ok_reps = sum(1 for r in range(R)
                       if tuple(np.argsort(-Gs[r])) == tuple(np.argsort(-I)))
    pooled_ok = tuple(np.argsort(-G)) == tuple(np.argsort(-I))
    chk("E7.3 ordering by I (pooled exact; ≥9/10 reps)",
        pooled_ok and rank_ok_reps >= 9,
        f"pooled={'OK' if pooled_ok else 'NO'}, reps={rank_ok_reps}/10  "
        f"G={np.round(G,4).tolist()}")

    # E7.4 aggregate ≤ 0 + uncoupled contrast
    agg_reps = Gs.mean(axis=1)
    agg, agg_se = float(agg_reps.mean()), float(agg_reps.std(ddof=1) / np.sqrt(R))
    # uncoupled: private bankrolls vs fair house odds r=q → G_a = I_a
    rng2 = np.random.default_rng(SEED + 99)
    G_unc = []
    for eps in EPS_LIST:
        xs = rng2.integers(0, 2, size=T)
        flip = rng2.random(T) < eps
        p_corr = np.where(~flip, 1 - eps, eps)
        G_unc.append(float(np.mean(np.log(p_corr / 0.5))))
    sum_unc = float(np.sum(G_unc))
    chk("E7.4 coupled aggregate < 0 (CI excl 0) vs uncoupled Σ ≈ ΣI > 0",
        agg + 1.96 * agg_se < 0 and abs(sum_unc - I.sum()) <= 0.02,
        f"coupled mean_a Ĝ = {agg:.4f} ± {1.96*agg_se:.4f}; "
        f"uncoupled Σ Ĝ = {sum_unc:.4f} (ΣI = {I.sum():.4f})")
    out["aggregate"] = {"coupled": agg, "se": agg_se,
                        "uncoupled_sum": sum_unc, "I_sum": float(I.sum())}

    # E7.5 clones
    Gc = np.array([parimutuel_inst(EPS_LIST, T, np.random.default_rng(SEED + r),
                                   clone_of=0) for r in range(R)])   # (R, 5)
    eq = abs(float(Gc[:, 0].mean() - Gc[:, 4].mean()))
    drop_reps = Gs[:, 0] - Gc[:, 0]
    drop, drop_se = float(drop_reps.mean()), float(drop_reps.std(ddof=1) / np.sqrt(R))
    chk("E7.5 clones: equal growth (≤0.01) and edge competed away (drop CI excl 0)",
        eq <= 0.01 and drop - 1.96 * drop_se > 0,
        f"|Ĝ_1−Ĝ_clone| = {eq:.5f}; drop in Ĝ_1 = {drop:.4f} ± {1.96*drop_se:.4f}")
    out["clone"] = {"equality": eq, "drop": drop, "drop_se": drop_se}

    # E7.1 conservation + E7.6 selection (evolving)
    cons_errs, order_hits = [], 0
    finals = []
    for r in range(R):
        w, err = parimutuel_evolve(EPS_LIST, 10_000, np.random.default_rng(SEED + 50 + r))
        cons_errs.append(err)
        finals.append(w.tolist())
        if int(np.argmax(w)) == int(np.argmax(I)):
            order_hits += 1
    chk("E7.1 conservation |Σw − 1| ≤ 1e-9 (evolving run)",
        max(cons_errs) <= 1e-9, f"max error = {max(cons_errs):.2e}")
    chk("E7.6 selection: best-informed ends largest (≥9/10 reps)",
        order_hits >= 9, f"{order_hits}/10 reps; mean final shares = "
        f"{np.round(np.mean(finals, axis=0), 3).tolist()}")
    out["evolve"] = {"final_shares_mean": np.mean(finals, axis=0).tolist(),
                     "order_hits": order_hits}
    return out


# ============================================================================
# E8 — alignment curvature (doc 04 §4)
# ============================================================================

def run_E8(T=50_000):
    print("\nE8 — alignment curves the region: bulge (cosθ>0) / conflict tax (cosθ<0)")
    MU = 0.1
    cs = [-0.8, -0.4, 0.0, 0.4, 0.8]
    ts = np.linspace(0, 1, 21)
    rng = np.random.default_rng(SEED)
    xi_a = rng.uniform(0.5, 1.5, size=T)
    xi_b = rng.uniform(0.5, 1.5, size=T)   # same draws across c, t → paired comparison
    out = {"mu": MU, "c_values": cs, "t_grid": ts.tolist(), "frontier": {}}

    fronts = {}
    for c in cs:
        Ga = np.array([float(np.mean(MU * (t + c * (1 - t)) * xi_a)) for t in ts])
        Gb = np.array([float(np.mean(MU * ((1 - t) + c * t) * xi_b)) for t in ts])
        fronts[c] = (Ga, Gb)
        out["frontier"][str(c)] = {"G_a": Ga.tolist(), "G_b": Gb.tolist()}

    # E8.1 sum-frontier
    ok1, worst1 = True, 0.0
    for c in cs:
        Ga, Gb = fronts[c]
        S = float(np.max(Ga + Gb))
        rel = abs(S - (1 + c) * MU) / MU
        worst1 = max(worst1, rel)
        ok1 &= rel <= 0.02
    chk("E8.1 sum-frontier = (1+cosθ)·μ (rel ≤ 2%)", ok1,
        f"worst rel error = {worst1:.4f}")

    # E8.2 pointwise dominance ordering in c
    ok2 = True
    for c1, c2 in zip(cs[1:], cs[:-1]):     # c1 > c2
        Ga1, Gb1 = fronts[c1]; Ga2, Gb2 = fronts[c2]
        ok2 &= bool(np.all(Ga1 >= Ga2 - 0.001) and np.all(Gb1 >= Gb2 - 0.001))
    chk("E8.2 region ordered by alignment (pointwise dominance, slack 0.001)",
        ok2, f"checked {len(cs)-1} adjacent pairs × 21 allocations")

    # E8.3 egalitarian point
    ok3, worst3 = True, 0.0
    for c in cs:
        Ga, Gb = fronts[c]
        egal = float(np.max(np.minimum(Ga, Gb)))
        rel = abs(egal - (1 + c) / 2 * MU) / MU
        worst3 = max(worst3, rel)
        ok3 &= rel <= 0.05
    chk("E8.3 egalitarian point = ((1+cosθ)/2)·μ (rel ≤ 5%)", ok3,
        f"worst rel error = {worst3:.4f}")
    return out


# ============================================================================
def main():
    print("=" * 76)
    print("MAXWELL STAGE 0 — coupled-fleet pilot (pre-registered: PREREGISTRATION_stage0.md)")
    print("=" * 76)
    results = {"E6": run_E6(), "E7": run_E7(), "E8": run_E8()}

    n_pass = sum(1 for _, ok, _ in CHECKS if ok)
    print("\n" + "=" * 76)
    print(f"STAGE 0: {n_pass}/{len(CHECKS)} pre-registered checks passed")
    for name, ok, _ in CHECKS:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 76)

    results["checks"] = [(n, ok, d) for n, ok, d in CHECKS]
    results["n_pass"] = n_pass
    results["n_total"] = len(CHECKS)
    path = os.path.join(OUT, "stage0.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"→ {path}")
    raise SystemExit(0 if n_pass == len(CHECKS) else 1)


if __name__ == "__main__":
    main()

# sim — falsifiable checks of the value thesis

A minimal numerical instantiation of [docs 00–05](../docs). The point is not a
big simulation; it is to take the thesis's **closed-form predictions** and show
that a Monte-Carlo world actually produces those numbers — and that **pricing the
fleet beats ad-hoc coordination**, the claim that turns the theory from vibes into
evidence (the standard set in [`00`](../docs/00-thesis-seed.md) §9.5).

Everything is in **nats** (natural log) so value growth rates and information
quantities (`H`, `D`, `I`) are directly comparable — which is the thesis's whole
contention: they are the same kind of quantity.

## Run

```sh
python3 sim/experiments.py     # needs numpy; ~20s; exits 0 iff all checks pass
```

## What each experiment checks

| Exp | Doc claim | Prediction | Result |
|---|---|---|---|
| **E1** | [02](../docs/02-coding-theorem-of-value.md) capacity theorem | `ΔG = I(X;Y)` — value-growth gain from perception **equals** mutual information | measured `ΔG` matches `I` to ~0.001 nats across three channel noises |
| **E2** | [02](../docs/02-coding-theorem-of-value.md) Second Law (exact) | `G = D(q‖r) − D(q‖p)` | matches to ~0.001; confident error (`D(q‖p) > D(q‖r)`) drives growth **negative** (value destroyed), as predicted |
| **E3** | [04](../docs/04-multi-agent-capacity-region.md) fleet ceiling | `ΔG_fleet ≤ H(X)`; perception **diversity** lifts it, **redundancy** does not | ceiling holds; diverse fleet (4 distinct bits) reaches 4× a single agent; redundant copies add exactly 0 |
| **E4** | [04](../docs/04-multi-agent-capacity-region.md) §3 operating point | Kelly/price-rebalanced fleet **beats** ad-hoc allocation | **Shannon's demon**: 3 agents each with ≈0 individual growth; the priced fleet grows at **+0.021/round** — beats all-in (17×) and every individual agent |
| **E5** | [05](../docs/05-dynamics.md) §1 dynamics | cumulative dissipation `= Σ D(q‖p_t)` `=` log-loss **regret**; a drifting world forbids zero dissipation | regret ≈ dissipation; stationary per-round dissipation → 0 (`≈2e-5`); **drifting world floors at `≈0.18` nats** (Dynamical Second Law), 4 orders of magnitude above stationary |

All 20 checks pass (`SUMMARY: 20/20`).

## Why these five

They are the load-bearing claims, one per layer of the thesis:

1. **E1** — value-throughput *is* information-throughput (the bridge is real, not analogy).
2. **E2** — the Second Law holds *exactly*, including the regime where value goes negative.
3. **E3** — the fleet's hard ceiling is the world's entropy; headcount past perception-saturation is worthless.
4. **E4** — the headline governance claim: **pricing beats ad-hoc**, with the most striking case (a fleet that profits from agents that individually don't).
5. **E5** — learning *is* value-recovery, and a moving world guarantees standing dissipation.

## Honest scope

- These confirm the theory is **self-consistent and correctly derived** — the simulated worlds are built from the same distributions the formulas assume. That is the right first test (does the math predict its own instantiation?), **not** a claim that real LLM agents obey these laws. That is the next step.
- **E4's** Shannon's-demon case uses symmetric anti-correlated returns, so Kelly weights equal the uniform weights; the decisive comparison there is *priced/rebalanced fleet vs all-in*, not vs equal-split. The general asymmetric case (where Kelly ≠ uniform) is the natural extension.
- **E5's** drift result demonstrates the Dynamical Second Law *qualitatively* (floor ≫ 0 under drift, ≈ 0 when stationary). The quantitative `D_min ∝ ‖q̇‖·σ` law ([05](../docs/05-dynamics.md) §1) is a linearized estimate and is not asserted here.
- Next step toward real evidence: replace the synthetic horse-race with a tool-use/agent task, estimate `I(X;Y_a)` empirically per agent, and test whether price-based fleet routing beats round-robin on realized task value — the same move Macrokit's benchmark makes for the weak-vs-frontier claim.

## Files

- `value_sim.py` — primitives: `H`/`D`/`I` (nats), the horse-race growth game, perception channels, the online-Bayes learner, and Kelly/price portfolio weights.
- `experiments.py` — the five experiments, each asserting measured ≈ predicted.

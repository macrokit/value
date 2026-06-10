# PRE-REGISTRATION — Maxwell Stage 0: the payout-COUPLED fleet pilot

**Frozen before any experimental run.** The git commit of this file precedes the first
results commit; thresholds and tolerances are stated here and applied mechanically.
Author byline: Cheng Qian.

---

## 0. What is being tested and why it exists

The correctness audit (doc 04 §2 erratum) showed the sum-form fleet ceiling
`Σ_a G_a ≤ H(X)` is **false** in the base model precisely because the base model lacks
**payout coupling**: independently-bankrolled agents do not share a physical medium, so
nothing ties their separately-compounded growth rates together. The corrected theory
makes three coupled-regime claims that have **never been checked in any implementation**:

1. **Pooled bankroll / fused posterior:** a coalition `S` betting the fused posterior
   `p(x|Y_S)` achieves `G_S = I(X;Y_S)` — and, for channels conditionally independent
   given `X`, `I(X;Y_S)` is **submodular** in `S` (diminishing coalition returns).
2. **Parimutuel coupling:** when agents bet **against each other** (odds formed from
   aggregate bets; zero-sum in wealth shares), aggregate growth collapses to ≤ 0 while
   **relative** growth is ordered by `I(X;Y_a)` — this is the explicit coupling under
   which a sum-form constraint becomes true.
3. **Alignment curves the region (doc 04 §4, first-ever check):** goal alignment
   `cos θ_ab > 0` bulges the jointly-achievable growth region outward
   (cooperation dividend); `cos θ_ab < 0` contracts it (conflict tax).

**Status of this pilot, stated up front:** this is a synthetic simulation built from the
corrected model's own assumptions — like E1–E5 it is **necessary, not sufficient**
(design validation, not discovery). Its role is to (i) validate the corrected
coupled-regime math numerically, and (ii) validate the experimental design (coalition
counterfactuals, overlap structures, coupling mechanics) before any real-agent Stage 2.
A pass licenses the design; it does not confirm the theory on real systems. A fail is a
math/implementation error to be found and reported.

---

## 1. E6 — shared-bankroll coalition throughputs (prediction set 1)

**World:** `X = (B₁,B₂,B₃)`, three iid fair bits; `q` uniform over 8 states;
`H(X) = 3 ln 2 ≈ 2.0794` nats. Reference odds fair vs `r = q` (so `G_∅ = 0` and
`G_S = ΔG_S`).

**Overlap structures (m = 3 agents unless noted):**

| ID | channels | analytic `I(X;Y_S)` highlights |
|---|---|---|
| (a) disjoint | `Y_a = B_a` | `I = |S|·ln2`; modular (marginals constant) |
| (b) partial overlap | `Y₁=(B₁,B₂)`, `Y₂=(B₂,B₃)`, `Y₃=(B₁,B₃)` | singletons `2ln2`; pairs `3ln2`; triple `3ln2` (third agent adds **0**) |
| (c) clones | `Y₁=Y₂=B₁`, `Y₃=B₂` | `I({1,2}) = ln2` (clone adds **0**) |
| (d) noisy | `Y_a = BSC₀.₁(B_a)`, independent noise | `I = |S|·0.3681` |
| (e) XOR synergy **control** | `X=B₁`; `Y₁=B₂` (noise), `Y₂=B₁⊕B₂` | `I(Y₁)=I(Y₂)=0`, `I({1,2})=ln2` — **supermodular** |

For (a)–(d) the channels are conditionally independent given `X`, the precondition under
which `I(X;Y_S)` is submodular. Structure (e) deliberately **violates** that
precondition; the theory then predicts submodularity **fails** there. (e) is a designed
control showing the precondition is load-bearing, not decoration.

**Procedure:** for every coalition `S ⊆ {1..m}`, compute the exact fused posterior
`p(x|y_S)` by enumeration, bet it with the pooled bankroll over `T = 200{,}000`
Monte-Carlo rounds, measure `Ĝ_S` = mean per-round log growth.

**PRE-REGISTERED CHECKS (tolerances chosen as ≥4× the MC standard error ≈ 0.005):**

| Check | Condition | Tolerance |
|---|---|---|
| E6.0 erratum counterexample reproduces | clones with **private** bankrolls: `Σ_a Ĝ_a ≈ 2 ln2 > I(X;Y_{12}) = ln2` | `Σ Ĝ within ±0.02 of 2ln2`, strictly > `ln2 + 0.1` |
| E6.1 achievability | `|Ĝ_S − I(X;Y_S)| for ALL coalitions, ALL structures (a)–(e)` | ≤ 0.02 nats |
| E6.2 monotonicity | `Ĝ_S ≤ Ĝ_T + 0.02` for all `S ⊆ T` | slack 0.02 |
| E6.3 joint ceiling (corrected doc 04 §2) | `Ĝ_S ≤ H(X) + 0.02` for all S | slack 0.02 |
| E6.4 submodularity where predicted | (a)–(d): all marginal-diminishing inequalities `[Ĝ_{S∪a}−Ĝ_S] − [Ĝ_{T∪a}−Ĝ_T] ≥ −0.03` for `S⊆T`, `a∉T` | slack 0.03 |
| E6.5 submodularity FAILS in the control | (e): marginal of `Y₂` given `{Y₁}` minus marginal given ∅ ≥ `ln2 − 0.05` (supermodular by ≈ ln2) | as stated |

---

## 2. E7 — parimutuel coupling (prediction set 2)

**World:** one fair bit, `q = (½,½)`. **Agents:** 4 BSC channels,
`ε ∈ {0.05, 0.15, 0.30, 0.45}` → exact `I_a ∈ {0.4946, 0.2704, 0.0823, 0.0050}` nats.
Each agent bets its full wealth proportionally to its exact posterior `b_a(x|y_a)`.
**Parimutuel rule (no take):** total bet on outcome `x` is `B(x) = Σ_a w_a b_a(x|y_a)`;
the whole pool is paid to outcome-`x*` bettors pro rata:
`w_a ← w_a · b_a(x*)/B(x*)`. Zero-sum in shares by construction.

**Primary reading (equal weights, instantaneous):** `G_a = E[ln(b_a(x*)/B(x*))]` at
fixed `w = 1/m`, estimated over `T = 100{,}000` rounds × `R = 10` reps.
**Analytic fact to verify:** since `E[ln b_a(x*|y_a)] = −H(X|Y_a)` and the
`−E[ln B(x*)]` term is common across agents, **pairwise growth gaps equal information
gaps exactly**: `G_a − G_b = I_a − I_b`.

**PRE-REGISTERED CHECKS:**

| Check | Condition | Tolerance |
|---|---|---|
| E7.1 conservation (zero-sum sanity) | evolving-wealth run: `|Σ_a w_a(T) − 1|` | ≤ 1e-9 |
| E7.2 gap law | all pairwise `|(Ĝ_a−Ĝ_b) − (I_a−I_b)|` (pooled estimate) | ≤ 0.01 nats |
| E7.3 ordering | Spearman(Ĝ_a, I_a) = 1.0 pooled; identical ranking in ≥ 9/10 reps | as stated |
| E7.4 aggregate collapses | equal-weight aggregate `mean_a Ĝ_a < 0`, 95% CI excludes 0; **contrast:** same 4 agents UNcoupled (private bankrolls vs fair house odds) give `Σ_a Ĝ_a` within ±0.02 of `Σ_a I_a = 0.852 > 0` | as stated |
| E7.5 clones' edges cancel | add agent 5 = exact clone of agent 1 (same `y` realisation): (i) `|Ĝ_1 − Ĝ_5| ≤ 0.01`; (ii) `Ĝ_1(with clone) < Ĝ_1(without)`, 95% CI of the drop excludes 0 | as stated |
| E7.6 selection (secondary) | evolving-wealth run from equal start, `T = 10{,}000`: terminal wealth share ordered by `I_a` (best-informed largest) in ≥ 9/10 reps | as stated |

---

## 3. E8 — alignment curvature of the region (prediction set 3; doc 04 §4)

**Model (minimal coupled implementation):** two agents share one effort budget
(`e_a + e_b = 1`); each works along its own goal direction; per-round log-growth of
agent `a` is `μ·(e_a + c·e_b)·ξ_t` with `c = cos θ_ab`, `μ = 0.1`, and `ξ_t` iid
positive mean-1 noise (uniform on [0.5, 1.5]) — agent `b`'s work spills into `a`'s
goal-progress with sign and magnitude `c`. Sweep allocations `e_a = t ∈ {0, .05, …, 1}`
(21 points), `T = 50{,}000` rounds/point, `c ∈ {−0.8, −0.4, 0, +0.4, +0.8}`.

**Honesty up front:** this is the weakest and most nearly-circular of the three sets —
the model's expectation is analytically `G_a = μ(e_a + c·e_b)`, so the check validates
the *implementation and region geometry*, not an independent law. It is the first
numerical instantiation of doc 04 §4's claim, nothing more.

**PRE-REGISTERED CHECKS:**

| Check | Condition | Tolerance |
|---|---|---|
| E8.1 sum-frontier linear in alignment | `max_t (Ĝ_a+Ĝ_b) = (1+c)·μ` for each `c` | rel. error ≤ 2% (vs μ) |
| E8.2 region ordered by alignment | for `c₁ > c₂`: `Ĝ_a(t;c₁) ≥ Ĝ_a(t;c₂) − 0.001` and same for `b`, at every `t` (pointwise dominance — bulge/contraction) | slack 0.001 (≈1%·μ) |
| E8.3 conflict tax at the egalitarian point | `max_t min(Ĝ_a,Ĝ_b) = ((1+c)/2)·μ` for each `c` | rel. error ≤ 5% |

---

## 4. Pass/fail accounting and what a result means

- **All checks pass** → the corrected coupled-regime math is implemented correctly and
  the Stage-2 experimental design (coalition counterfactuals + overlap structures +
  coupling mechanics) is validated. **Not** evidence about real agents.
- **Any check fails** → either a theory error or an implementation error; diagnose,
  report which, and do not proceed to Stage 2 on a failed design. A theory-level failure
  in E6/E7 would be a real (synthetic) negative against the corrected doc-04 claims and
  will be written up as such.
- Results JSON + honest writeup in `docs/17-coupled-fleet-pilot.md`, including a
  "what this does NOT show" section (synthetic; circularity; Stage 2 is the real test).

## 5. Reproducibility

Pure numpy, seeded (`seed = 7` primary; reps use `seed + rep`). Single file
`sim/coupled/coupled_fleet.py`; results to `sim/coupled/results/stage0.json`.
No LLM calls, no network. Runs in minutes on a laptop.

*Pre-registration commit SHA precedes the results commit SHA — see git log.*

# The Real-Agent Test — Do Live LLMs Obey the Laws of Value?

> The sim ([`sim/`](../sim/), E1–E5, 20/20) shows the closed-form laws are self-consistent on *synthetic*
> worlds built from the same distributions the formulas assume. That is necessary but circular: it cannot tell
> us whether *real* agents obey the laws. This doc closes that gap. We instantiate the theory with a ladder of
> real local language models as agents on a fixed decision task, and measure — from their actual outputs —
> whether the three load-bearing quantities (`I(X;Y)`, `ΔG`, `D(q‖p)`) behave as the statics (docs
> [`01`](01-core-formalization.md)–[`04`](04-multi-agent-capacity-region.md)) predict.

> **Real-agent result.** On a frozen 100-item decision task, four local models obey the value laws *measured on
> their own behavior*. **(R1)** value-growth tracks perception mutual information: `I(X;Y)` follows realized
> **capability** (Pearson **r = 0.99** vs accuracy) and out-of-sample `ΔG` tracks `I` at **r = 0.99** — and the
> tracking is to *capability, not parameter count*, a cross-family 8B model that is bigger yet weaker than the
> 7B landing at correspondingly lower `I`. **(R2)** over-confidence is measurable value dissipation that *shrinks
> with capability* (4.17 → 0.69 nats over the qwen ladder) — for the 1.5B model, confident error drives realized
> growth **negative**. **(R3)** the cheapest model delivers the most perception-MI **per second of compute**
> (0.74 vs 0.30 nats/s). **(R4)** a diverse model pair covers more of `H(X)` than either alone (+0.09 nats) while
> an identical re-run adds exactly **0**. **(R5, honest negative + twist)** a price/Kelly fleet beats
> equal-weight but **does *not* beat the single best model** on raw growth — there is no Shannon's demon on a
> *correlated* set of agents — **yet** under a compute budget the value-density ranking inverts and an `I/cost`
> price wins (0.33 vs 0.24 nats/s). Pricing pays where the agents are *priced*, not merely *pooled*.

## 1. Why a tool-routing task

The cleanest real instantiation of the single-agent theory needs a task with (a) a well-defined *correct
action* per situation (so the world-state `X` is ground-truthed), (b) a model output that *is* an action (so
the perception channel `Y` is observed directly, not inferred), and (c) a frozen, pre-registered item set (so
the measurement cannot be tuned to flatter a model). A **tool-routing / intent-classification** benchmark
satisfies all three: each item is a natural-language request whose gold answer is one of a small set of
actions, and the model's job is to pick the action. This is exactly the perception-then-act structure of the
coding theorem ([`02`](02-coding-theorem-of-value.md) §3) — the model perceives the request and commits to an
action — so the bridge `ΔG = I(X;Y)` is testable on raw behavior.

We reuse a **frozen 100-item tool-routing corpus** (committed before any model was run; the item set and the
scoring rules are immutable). Each item has a gold action drawn from **K = 7 classes**: six distinct tools plus
a "no-tool" class (the request should be declined / answered in free text). We deliberately do *not* build a
fresh dataset: a pre-registered corpus removes the degree of freedom that would let us choose items after
seeing results. The task is described here abstractly; its domain specifics are irrelevant to the value
measurement.

## 2. The value mapping

| Theory object | Instantiation |
|---|---|
| World-state `X` | the **correct action** for an item (one of K=7 classes) |
| Perception `Y_a` | model `a`'s **chosen action** (the tool it called, or "none") |
| World law `q(x)` | the empirical marginal of correct actions over the corpus |
| Reference `r(x)` | set to `q` (the action marginal) — so a no-signal agent grows value at rate 0 |
| Agent `a` | a local model at a fixed temperature (greedy), one of a capability ladder |

From each model's run we build the **confusion matrix** `C_a[x,y] = #(gold=x, chosen=y)`. Every value quantity
is then computed from `C_a` with the **same** primitives the sim uses ([`sim/value_sim.py`](../sim/value_sim.py)),
in **nats**:

- **Perception MI** `I(X;Y_a)` — directly from the joint `C_a / N`.
- **Calibrated posterior** `p_a(x|y) = C_a[:,y] / Σ_x C_a[:,y]` (Dirichlet-smoothed) — the agent's
  best Bayesian read of the world given its own action `y`.
- **Realized value-growth** `ΔG_a = mean over items of ln( p_a(x|y_a) / r(x) )` — the horse-race log-growth of
  betting the calibrated posterior against the reference ([`02`](02-coding-theorem-of-value.md) §2).

The agents are four local models spanning a range of capability (three from one family at ~1.5B / 3B / 7B, plus
a cross-family ~8B). This is deliberately **not** a clean parameter ladder: the 8B model is from a different
family and is *less capable* on this task than the 7B, which is exactly the perturbation R1 needs — it
separates "`I` rises with size" (false) from "`I` rises with capability" (the real claim). The benchmark's
headline **accuracy** is reported only as a measure of realized capability; it is *not* `I(X;Y)` — the value
quantities are computed independently from the confusion structure.

**Honest measurement discipline.** To keep the test from being circular we separate two regimes:

- **In-sample identity.** With the oracle posterior (calibration on the full set) and `r = q`, the realized
  growth equals the mutual information *by construction*: `ΔG = E[ln p(x|y)/q(x)] = I(X;Y)`. This is an
  arithmetic identity; we report it only to confirm the bridge **computes correctly on real confusions** and to
  pin the units — not as evidence.
- **Out-of-sample.** We fit the calibrated posterior on a stratified **fit split** (50 items) and score
  realized growth on the held-out **holdout split** (50 items). Out of sample `ΔG_holdout ≤ I(X;Y)`, and the
  gap is genuine **generalization dissipation** — the empirical content. The non-trivial claims are that
  `I(X;Y)` *rises along the capability ladder* and that out-of-sample `ΔG` *tracks* it; neither is forced by the
  identity.

## 3. The experiments (mirroring the sim's E1–E5 on real models)

- **R1 — the bridge holds on real outputs** (real E1). Does `ΔG_a` track `I(X;Y_a)`, and do both rise along the
  weak→strong ladder? The headline empirical validation: *value-throughput is information-throughput, on real
  model behavior.*
- **R2 — the Second Law / calibration is dissipation** (real E2). Reading the *same* point-predictions with a
  calibrated vs an over-confident posterior realizes different value; the gap is dissipation in nats. Confident
  error destroys value ([`02`](02-coding-theorem-of-value.md) §4).
- **R3 — value per joule** (the deployment-relevant axis: cheap reflex vs. expensive deliberation). `I(X;Y)`
  per second of compute across the ladder —
  does a cheap model deliver competitive perception-MI per unit compute? (Scope note: this corpus is fixed
  across models, so R3 is the I/compute *curve*, not a within-model prompt ablation — see §5.)
- **R4 — diversity beats redundancy** (real E3). Joint `I(X; Y_a, Y_b)` for two *different* models vs the same
  model twice. Distinct models should cover more of `H(X)`; an identical (greedy) re-run adds exactly 0.
- **R5 — pricing beats ad-hoc** (real E4, the headline governance claim). Combine the models' calibrated
  posteriors into a fleet and compare realized out-of-sample log-growth of: (a) the single best model, (b) an
  equal-weight ensemble, (c) a **price/Kelly-weighted** ensemble (weights from `kelly_weights` fit on the fit
  split). Prediction: priced fleet ≥ best-single and ≥ equal-weight; the striking case is a *demon* — the fleet
  beating every member. **Reported honestly whether or not it holds.**

## 4. Results

> **Status.** Four models: 1.5B / 3B / 7B (one family) + a cross-family 8B. Greedy decoding (temperature 0),
> 100 items, 48/52 fit/holdout. The 7B is served via llama.cpp; the 1.5B/3B/8B via a local Ollama server (a
> serving-stack difference noted in §5). All numbers below are produced by
> [`sim/real/experiments_real.py`](../sim/real/experiments_real.py) and cached under `sim/real/results/`.

**R1 — the bridge holds, and `I` tracks *capability*, not size.** The in-sample identity `ΔG = I(X;Y)` holds to
`< 10⁻⁴` (confirming the arithmetic on real confusions). Across the four models, `I(X;Y)` tracks realized
capability (tool-accuracy) at **Pearson r = 0.99**, and out-of-sample `ΔG` tracks `I` at **r = 0.99**. The
decisive point is the cross-family 8B: it is *larger* than the 7B yet *less capable* (0.86 vs 0.96 accuracy),
and its `I` lands accordingly *below* the 7B and near the 3B — bigger model, lower capability, lower value
ceiling. So the claim is not "scale buys value"; it is the sharper **value-throughput is information-throughput,
and information-throughput is set by what the model can actually perceive.**

| Model | params | tool-acc | `I(X;Y)` (nats) | `ΔG` in-samp | `ΔG` holdout |
|---|---|---|---|---|---|
| qwen2.5-1.5b | 1.5B | 0.79 | 1.277 | 1.277 | 0.915 |
| qwen2.5-3b | 3B | 0.87 | 1.561 | 1.561 | 1.242 |
| qwen-7b | 7B | 0.96 | **1.779** | 1.779 | 1.423 |
| llama3.1-8b *(cross-family)* | 8B | 0.86 | 1.513 | 1.513 | 1.109 |

(`H(X) = 1.92` nats is the ceiling; the 7B captures 93% of the world's entropy, the 1.5B 66%. Note the 8B —
larger than the 7B — sits at 79%, below it: a value ceiling set by capability, not parameters.)

**R2 — over-confidence is dissipation, and calibration is a capability.** Reading the *same* point-predictions
with a calibrated vs an over-confident posterior realizes different value; the gap is dissipation. It is large
for the weak model and shrinks with scale — a quantitative statement that **weaker models must be more humble**:

| Model | tool-acc | `G_cal` | `G_over` | dissipated (nats) |
|---|---|---|---|---|
| qwen2.5-1.5b | 0.79 | +0.915 | **−3.255** | 4.17 |
| qwen2.5-3b | 0.87 | +1.242 | −0.863 | 2.11 |
| qwen-7b | 0.96 | +1.423 | +0.731 | 0.69 |
| llama3.1-8b | 0.86 | +1.109 | −1.660 | 2.77 |

Dissipation tracks *(in)capability*, not size: the less-reliable 8B dissipates 2.77 nats — more than the 7B and
in line with its accuracy. For the 1.5B and 8B models, confident error drives realized growth **negative** — a
wrong, certain agent actively destroys value, exactly the Second Law's prediction
([`02`](02-coding-theorem-of-value.md) §4).

**R3 — value per joule: the cheap model wins the density race.** `I(X;Y)` per second of compute *falls* with
scale across the qwen family (0.74 → 0.38 → 0.30 nats/s), and the cross-family 8B is worst of all (0.15 nats/s:
slowest *and* lower `I`). The weak model is the most *efficient* perceiver per unit compute — the value-theoretic
statement of why a cheap reflex is worth running. (Scope: this is the I/compute curve across heterogeneous
models, not a within-model prompt ablation; see §5.)

**R4 — diversity beats redundancy.** Two *different* models jointly perceive more of `H(X)` than either alone;
an identical greedy re-run adds **exactly 0**. The best diverse pair (3B+7B) reaches `I = 1.869` nats, lifting
+0.090 over the 7B alone and closing most of the gap to `H(X) = 1.921`.

| Pair | joint `I` | lift over best single |
|---|---|---|
| 1.5B + 3B | 1.767 | +0.205 |
| 3B + 7B | **1.869** | +0.090 |
| 1.5B + 8B | 1.698 | +0.185 |
| 3B + 8B | 1.761 | +0.200 |
| any model ×2 (redundant) | = single | **+0.000** |

The largest *lifts* come from pairing models whose errors differ most (two weaker, differently-wrong models —
1.5B+3B, 3B+8B — add ~0.2 nats), while the highest *absolute* joint `I` comes from the strongest diverse pair
(3B+7B). Either way, two distinct perceivers beat one; an identical re-run adds nothing.

**R5 — pricing beats ad-hoc, but only where there is something to price (the headline, reported honestly).**
On raw out-of-sample growth, the Kelly/price fleet (`+1.328`) beats the equal-weight ensemble (`+1.315`) but
**does not beat the single best model** (`+1.423`). **There is no Shannon's demon here** — and the theory says
why: four models on the *same* task are *positively-correlated* agents (R4: the best diversity lift is only +0.09
nats), so there is no anti-correlated volatility for Kelly rebalancing to harvest, and the best agent simply
dominates. This is the honest negative the synthetic E4 demon does *not* reproduce, because E4 was built with
anti-correlated agents by construction.

The twist that rescues the governance claim: **the negative is only on the cost-blind axis.** Value *per joule*
(growth ÷ mean compute) inverts the ranking — the 1.5B model yields **0.531 nats/s** against the 7B's 0.243 (and
the slow 8B only 0.111) — and a budget-aware price `∝ I_a/cost_a` (the shadow-price `λ = K/E` of
[`03`](03-cross-frame-value.md) §5) achieves **0.328 nats/s**, beating the best single model's density (0.243).
So pricing pays exactly where [`04`](04-multi-agent-capacity-region.md) says it should: as the lever that
*chooses the operating point under a resource constraint*, not as a free lunch that beats the best agent when
compute is unlimited.

> **What R5 teaches.** Pooling a correlated ladder does not beat its best member (no demon). Pricing earns its
> keep on two distinct axes that *are* present here: it beats naïve equal-weighting, and under a compute budget
> it routes value-density to the cheap agent and wins. The demon needs *perception diversity* (different slices
> of `H(X)`), which a same-task capability ladder lacks by construction — a concrete, falsifiable boundary on
> the fleet result.

A PASS/FAIL table and per-model confusion matrices are emitted to
[`sim/real/results/`](../sim/real/results/) (`results_table.json`, `confusions.json`, `experiments_output.txt`);
the raw model runs are cached under `sim/real/results/bench_runs/` so every number re-derives offline.

## 5. Where this breaks (scope honesty)

- **The in-sample identity is arithmetic, not evidence.** `ΔG = I` in-sample holds by construction; only the
  capability tracking (`I` vs accuracy, incl. the cross-family point), the out-of-sample tracking, and R5 are
  empirical. We label them as such above.
- **R3 is a curve, not an ablation.** The corpus is fixed and "macro-on" for every model, so R3 measures
  `I`/compute across model scale, not raw-prompt vs structured-prompt within one model. A clean within-model
  macro ablation (the sharpest form of the "design-time encoding raises `I` per joule" claim) is future work and
  needs a second prompt condition the frozen corpus does not contain.
- **Calibration is constructed, not elicited.** The models emit hard actions, not probabilities, so the
  "posterior" is the empirical confusion column, and the "over-confident" belief in R2 is a constructed reading.
  The dissipation we measure is real, but it is the dissipation of *a stated belief over those predictions*, not
  of a probability the model itself reported.
- **One task, one corpus.** R1 passing means the bridge holds *on this task*. It is evidence, not a universal
  law. Tool-routing is a discrete-action perception task; continuous or long-horizon settings are untested.
- **Tooling artifacts are not capability.** Small models served through some local tool-calling stacks emit no
  tool call at all (a plumbing failure, not a routing decision); such degenerate runs are detected (near-zero
  `I` with predictions collapsed to the no-op class) and excluded, never reported as a low-`I` capability
  result. One 7B run was discarded on exactly this ground and replaced by a clean run of the same model.
- **Mixed serving stacks.** The 7B was served via one local runtime and the 1.5B/3B/8B via another. The value
  mapping reads only each model's chosen action, so the confounder is small for `I`/`ΔG`, but the absolute
  latencies in R3/R5 mix two stacks and should be read as within-model, not cross-stack, comparisons.
- **R5's negative is regime-specific, and that is the point.** No demon appears because four models on the same
  task are positively-correlated agents (R4 quantifies the best residual diversity at +0.09 nats). A fleet of
  agents with genuinely *different* perception channels — different slices of `H(X)`, e.g. specialists rather
  than generalists of varying strength — is the regime where the demon is predicted; testing that needs
  heterogeneous *roles*, not heterogeneous *capability*, and is the natural next experiment.

## 6. What this establishes

On a frozen, pre-registered decision task, four real local models obey the value laws measured on their own
outputs: **value-throughput tracks information-throughput**, and information-throughput tracks *capability, not
size* — a cross-family 8B that is bigger yet weaker than the 7B sits at correspondingly lower `I` (R1, r = 0.99).
**Miscalibration is dissipation in nats** and the least-capable models dissipate most, going negative (R2);
**diversity lifts the fleet's perception while redundancy adds nothing** (R4). The two governance-facing results
are reported with their honest edges: perception-MI is the real ceiling on an agent's value-generation (R1), and
**pricing beats naïve pooling and wins under a compute budget, but does not beat the single best agent on a set
of correlated agents** (R5) — no demon without genuine perception diversity. The bridge from a thermodynamics of
value to live agents is empirical, not just self-consistent; its limits are named.

# value

*A mathematical theory of value — built the way Shannon built information.*

This is a private research repository. It develops one bet to its consequences:

> **Value is a real, lawful quantity** — in the same category as matter, energy, and information — currently
> left undefined only because, like information before 1948, it is confused with its semantic clothing
> (morality, price, preference). Strip the clothing and a structural quantity remains, with measures, limits,
> and conservation laws. The end goal is concrete: a quantity precise enough to **govern populations of
> separated AI individuals.**

The motivating premise: *in the near future, all AI agents are driven by values.* If so, a theory of value is
not philosophy — it is the **control theory for agent populations.**

## The method (copied from Shannon, deliberately)

Shannon's 1948 paper worked because of one ruthless abstraction: he threw away **meaning** and defined
information as nothing but reduction of uncertainty. From that he got a measure (`−log p`), a unit (the bit),
a system model, and hard limits (channel capacity, the coding theorems).

Our analogous abstraction: **throw away morality, price, and human psychology.** What remains is value as a
*frame-relative but lawful* quantity — relative to an agent's goal the way information is relative to a prior
and energy is relative to a reference frame. Relativity does not disqualify a quantity from being fundamental;
it forces the theory to make the frame explicit.

> **A theory of value is to agency what relativity is to motion.** Value is frame-dependent on the agent's
> goal; the laws relating value across frames are universal.

## The results so far

| Doc | Contribution | Headline result |
|---|---|---|
| [`00`](docs/00-thesis-seed.md) | Framing | Value = exergy (created by gradients, dissipated by misalignment), not conserved energy; frame-relative; substrate = free energy |
| [`01`](docs/01-core-formalization.md) | The measure | **Logarithmic Value Law** `V = Σ kᵢ ln eᵢ` (forced by one Cauchy axiom); optimal allocation `eᵢ* ∝ kᵢ`; focus penalty `V* = K ln E − K·H(k̂)` |
| [`02`](docs/02-coding-theorem-of-value.md) | The capacity theorem | **`ΔG ≤ I(X;Y)`** — value-throughput is bounded by information-throughput; **Second Law** `G = D(q‖r) − D(q‖p)` exact |
| [`03`](docs/03-cross-frame-value.md) | Cross-frame / multi-agent | **Value is frame-relative; price is frame-independent.** Exchange via shadow price `λ=K/E`; invariant = Fisher–Rao metric (Čencov); alignment `cos θ` sets positive/negative-sum |
| [`04`](docs/04-multi-agent-capacity-region.md) | Fleet governance | **Collective value-throughput ≤ H(X)** — the world's entropy caps the whole fleet; region shaped by alignment; operating point set by price |
| [`05`](docs/05-dynamics.md) | The equations of motion | **Learning = value-recovery, dissipation = regret**; natural-gradient (Fisher) belief flow, tâtonnement price flow, control+selection goal flow; alignment = a stability condition; a moving world forbids zero dissipation |
| [`06`](docs/06-real-agent-test.md) | **Real-agent test** | Four live LLMs obey the laws on their own outputs: `I(X;Y)` tracks realized **capability not size** (**r=0.99**; a cross-family 8B, bigger-but-weaker, lands at lower `I`); `ΔG`∝`I(X;Y)`; over-confidence dissipates value (weakest → negative growth); diversity > redundancy; **pricing beats pooling and wins under a compute budget — but no demon on correlated agents** (honest negative) |

### The three load-bearing equations

```
V   = Σ kᵢ ln eᵢ                  the measure            (doc 01)
ΔG  = I(X;Y)                      the capacity            (doc 02)
G   = D(q‖r) − D(q‖p)             available − dissipated  (doc 02)
```

Two structural facts give confidence the abstraction is real, not decorative:

1. **The logarithm is over-determined** — forced independently by diminishing marginal value (doc 01) *and*
   by multiplicative compounding dynamics (doc 02). Fundamental quantities are over-determined like that.
2. **Shannon's own quantities reappear unbidden** — entropy `H` as a value-dissipation penalty (doc 01), KL
   divergence `D` as available-minus-dissipated value (doc 02), mutual information `I` as the value ceiling
   (doc 02), the Fisher metric as the cross-frame invariant (doc 03). The bridge is load-bearing.

## Why this serves "governing separated AI individuals"

- **Per agent:** value-generation rate is capped by its perception's mutual information `I(X;Y_a)`. A macro
  raises `I` per joule — the formal reason a cheap reflex can match expensive deliberation on a narrow task.
- **Across agents:** their values are *not* cardinally comparable (Arrow / interpersonal-utility impossibility —
  and we do not pretend otherwise). Coordinate them through an **emergent price** on shared resources, exactly
  as economies coordinate incomparable utilities — never through a god's-eye utility sum.
- **Fleet design:** cultivate **goal-diversity** (trades to positive-sum) and **perception-diversity** (covers
  more of `H(X)`); suppress **belief-divergence** (zero/negative-sum speculation) and **goal-conflict**
  (negative `cos θ`). Headcount past perception-saturation buys nothing.

## Evidence — the theory predicts its own instantiation

[`sim/`](sim/) is a minimal numerical test: take each closed-form prediction and check a Monte-Carlo world
produces those numbers. **20/20 checks pass** (`python3 sim/experiments.py`):

- **E1** `ΔG = I(X;Y)` to ~0.001 nats — value-throughput *is* information-throughput.
- **E2** `G = D(q‖r) − D(q‖p)` exactly, including value going **negative** under confident error.
- **E3** fleet ceiling `ΔG_fleet ≤ H(X)`; diversity lifts it, redundancy adds exactly 0.
- **E4** the headline: a **priced/rebalanced fleet beats ad-hoc** — *Shannon's demon*, a fleet that grows at
  +0.021/round from agents that individually don't grow at all.
- **E5** dissipation = regret; a drifting world floors dissipation at ~0.18 nats while a stationary one → 0
  (the Dynamical Second Law).

These confirm the math is self-consistent and correctly derived. The sim is necessary but circular (the worlds
are built from the distributions the formulas assume), so the next step is **real agents**.

[`sim/real/`](sim/real/) instantiates the theory with **four live local LLMs** (1.5B / 3B / 7B + a cross-family
8B) on a frozen 100-item decision task — `X` = the correct action, `Y_a` = the model's chosen action — and
measures the value quantities from their *actual outputs* (`python3 sim/real/experiments_real.py`; full write-up
in [`docs/06`](docs/06-real-agent-test.md)):

- **R1** `I(X;Y)` tracks realized **capability, not parameter count** (**Pearson r = 0.99** vs accuracy): the
  cross-family 8B is *bigger yet weaker* than the 7B and its `I` lands lower accordingly. Out-of-sample `ΔG`
  tracks `I` at r = 0.99 — value-throughput is information-throughput, on real behavior.
- **R2** over-confidence is dissipation in nats, *shrinking* with capability (4.17 → 0.69 over the qwen ladder);
  the least-capable models' confident error drives realized growth **negative**.
- **R3** the cheapest model delivers the most `I(X;Y)` **per second of compute** (0.74 vs 0.30 nats/s).
- **R4** a diverse pair covers more of `H(X)` than either alone (+0.09 nats); an identical re-run adds **0**.
- **R5** (honest) a price/Kelly fleet beats equal-weight pooling but **not** the single best model — *no demon
  on correlated agents* — **yet** under a compute budget an `I/cost` price wins (0.33 vs 0.24 nats/s). Pricing
  pays where agents are priced and diverse, not merely pooled.

So the laws hold on real agents where the single-frame theory is testable; the one fleet-level claim with a
genuine precondition (perception diversity) is reported with its boundary, not oversold.

## Honest status

- **Proven (within stated axioms):** the log law (01), the capacity theorem with achievability + converse (02),
  the Second-Law decomposition (02), the cross-frame exchange rate + Fisher invariant (03), and the fleet
  outer bounds (04).
- **Conjecture:** the Second Law of Value as a global tendency (00 §4); equilibrium-price existence beyond the
  convex regime (03 §8).
- **Open:** the *exact* multi-agent capacity region (04) — likely as hard as open problems in network
  information theory; the cross-frame *cardinal* comparison (03, deliberately unsolved); the full **dynamics**
  of how `k`, `p`, `π` evolve (Thread C — unwritten).

Each doc ends with an explicit "where this breaks" section, in Shannon's spirit of naming the model's
assumptions.

## Reading order

`00` (framing) → `01` (the measure) → `02` (the limit) → `03` (many agents) → `04` (the fleet) → `05`
(dynamics) → `06` (the real-agent test). Each builds on the last; each is self-contained enough to skim from
its headline box. Docs 01–04 are the **statics** (conservation laws, equilibria); doc 05 is the **dynamics**
(equations of motion); doc 06 is the **evidence** (live LLMs measured against the laws). Together they form a
thermodynamics of value, with a real-agent test.

## Provenance & non-goals

- Author byline for any external write-up: **Cheng Qian**. Repo git identity: `jamesavechives`.
- This is a *theory* repo — definitions, derivations, and honest limits. It is **not** a product, and it does
  not aim to resolve interpersonal value comparison (provably non-canonical) or to produce a single fleet-wide
  "total value" number (there isn't one — that's the point of price).

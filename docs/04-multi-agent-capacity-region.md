# The Multi-Agent Value Capacity Region

> Threads A + B unified, from [`03-cross-frame-value.md`](03-cross-frame-value.md) §9. Single-agent gave a
> scalar ceiling (`ΔG ≤ I(X;Y)`, [`02`](02-coding-theorem-of-value.md)). Cross-frame gave exchange and
> alignment ([`03`](03-cross-frame-value.md)). This doc asks the governance question: for `m` interacting
> agents sharing **one world** and **one resource pool**, what is the achievable region of joint growth-rate
> vectors `(G_1,…,G_m)`? This is the value analog of Shannon's *capacity region* for multi-user channels — and
> the first result that is a theory of *governing* a fleet, not just measuring one.

**Honesty up front.** The *exact* region is almost certainly as hard as open problems in network information
theory (the general broadcast-channel region is still unsolved after 50 years). What is rigorously available —
and what governance actually needs — is the set of **outer bounds**, the **qualitative shape** the alignment
matrix imposes, and the **structure of the operating point**. We prove those and flag the rest as open.

## 1. The fleet model

`m` agents share:

- one **world** with state `X ∼ q` per round, entropy `H(X)`;
- one **resource pool** `E = Σ_a E_a` (free energy), reallocatable across agents;
- each agent `a` has a **perception channel** `Y_a` (mutual information `I(X;Y_a)` with the world), a **goal
  covector** `k_a`, and a **belief** `p_a` (notation from [`01`](01-core-formalization.md)–[`03`](03-cross-frame-value.md)).

Each agent compounds value at growth rate `G_a` ([`02`](02-coding-theorem-of-value.md)). The **value capacity
region** `𝓡` is the closure of all jointly-achievable `(G_1,…,G_m)`. We characterize `𝓡` by three couplings,
added one at a time.

## 2. Coupling I — the shared world (information outer bound)

The agents perceive the **same** `X` through different channels, so their perceptions are correlated and
*redundant*. By the chain rule and data-processing, for every subset `S ⊆ {1,…,m}`:

$$\sum_{a\in S} G_a \;\le\; I\big(X;\, Y_S\big) \;\le\; H(X),\qquad Y_S := \{Y_a : a\in S\}.$$

The per-agent bound `G_a ≤ I(X;Y_a)` ([`02`](02-coding-theorem-of-value.md)) is the singleton case; the
**sum-rate** bound is the whole-fleet case:

$$\boxed{\,\sum_{a=1}^{m} G_a \;\le\; I(X;\,Y_{1:m}) \;\le\; H(X).\,}$$

> **Fleet Value Ceiling.** No fleet, however large, can compound value faster than the world produces
> resolvable uncertainty `H(X)` per round.

This is the value analog of the **multiple-access sum-rate constraint**: agents are "transmitters," the shared
world/resource is the channel, growth rates are rates, and the region has the polymatroidal subset structure
`Σ_{a∈S} G_a ≤ I(X; Y_S)`. Two immediate governance corollaries:

- **Diminishing returns to headcount.** Once `I(X; Y_{1:m})` saturates toward the available observable
  information (≤ `H(X)`), adding more agents with redundant perception buys **zero** marginal throughput. The
  binding constraint becomes *perception diversity*, not headcount.
- **Perception diversity is the lever.** Fleet throughput grows only as the agents' channels cover *different*
  parts of `H(X)` (small `I(Y_a;Y_b)` given `X`). Redundant clones are dead weight.

## 3. Coupling II — the shared resource (the operating point is a Kelly portfolio)

Growth *rate* is scale-invariant in the compounding regime ([`02`](02-coding-theorem-of-value.md) §1), so the
shared pool does not change any single `G_a` — it sets each agent's **weight** in total fleet value. Measuring
all agents' value in the common price units of [`03`](03-cross-frame-value.md) §5, total fleet value
`W = Σ_a W_a` and

$$\frac{d \log W}{dt} \;=\; \text{(value-weighted average of the } G_a\text{)} \;+\; \text{(rebalancing term)}.$$

Two regimes:

- **Perfectly correlated agents** → put all resource on the max-`G` agent (pure compounding is winner-take-all).
- **Imperfectly correlated agents** (they perceive/bet on different things) → **diversify.** Under
  multiplicative dynamics, spreading resource across imperfectly-correlated agents and rebalancing *raises* the
  time-average growth — the volatility-harvesting / "Shannon's demon" effect, formalized by Kelly portfolios
  and Cover's universal portfolio. The fleet is a **Kelly portfolio over agents.**

The operating point on the frontier is therefore selected by the resource allocation, equivalently by the
**price vector** `π` ([`03`](03-cross-frame-value.md) §5): prices move resource to high-shadow-price agents
(`λ_a = K_a/E_a`) until `λ` equalizes, and the rebalancing term rewards keeping imperfectly-correlated agents
funded rather than collapsing onto one. *Price chooses where on `𝓡` the fleet sits; it does not change `𝓡`.*

## 4. Coupling III — alignment curves the region

Agents act on the *same* world, so one agent's value-producing action is an **externality** on the others,
signed by their alignment `cos θ_{ab} = ⟨k̂_a, k̂_b⟩` ([`03`](03-cross-frame-value.md) §3):

- **Aligned (`cos θ_{ab} > 0`)** — `a`'s progress also advances `b`'s goal (positive externality). Their joint
  achievable growth **exceeds** the sum of solo growths: the region **bulges outward** past the independent box
  `∏_a[0, I(X;Y_a)]`. A *cooperation dividend.*
- **Opposed (`cos θ_{ab} < 0`)** — `a`'s progress destroys `b`'s value (negative externality). They cannot both
  reach their solo maxima: the region **contracts inward**. A *conflict tax*, the Second Law
  ([`00`](00-thesis-seed.md) §4) at fleet scale.
- **Orthogonal (`cos θ_{ab} = 0`)** — independent; the box face is flat.

So the **alignment matrix** `M = [\cos θ_{ab}]` is what *shapes* `𝓡` (curvature of the Pareto frontier),
while §3's price *selects the point on it*. This is the value analog of the difference between **cooperative**
multi-user channels (region expands) and **interference** channels (region shrinks).

## 5. Synthesis — the region and the two governance levers

Collecting the three couplings, the achievable region `𝓡` is bounded by:

1. **per-agent ceilings** `G_a ≤ I(X;Y_a)` (own perception, doc 02);
2. **subset sum-rate** `Σ_{a∈S} G_a ≤ I(X;Y_S) ≤ H(X)` (shared world, §2);
3. **frontier curvature** set by the alignment matrix `M` (shared world action, §4);

and the fleet's **operating point** within `𝓡` is selected by the resource **price** `π`, with a Kelly-portfolio
diversification bonus for imperfectly-correlated agents (shared resource, §3).

This separates governance into two cleanly different acts:

| Lever | What it does | Mechanism |
|---|---|---|
| **Choose the operating point on `𝓡`** | tactical — who gets resource now | price `π` / shadow-price equalization (doc 03 §2); Kelly-diversify across uncorrelated agents |
| **Shape `𝓡` itself** | strategic — what the fleet *can* achieve | set `k_a` to make `cos θ_{ab} ≥ 0` (alignment design); raise & diversify `I(X;Y_a)` (perception design — e.g. macros) |

> **Governing a fleet of AI individuals = shaping its value capacity region (alignment + perception) and then
> pricing resource to the best point on it.**

## 6. The Macrokit connection, at fleet scale

[`02`](02-coding-theorem-of-value.md) §5 showed a macro raises one agent's `I(X;Y_a)` per joule. At fleet
scale the payoff compounds two ways: (i) it pushes each agent toward its per-agent ceiling cheaply, and (ii)
because macros can be authored to cover *different* slices of `H(X)`, a macro library is a direct instrument
for the **perception diversity** that §2 identified as the only thing that lifts the fleet ceiling. "Design a
macro library" = "tile `H(X)` with non-redundant cheap perception channels" = "raise `I(X;Y_{1:m})` toward
`H(X)` at minimum joules." The fleet ceiling and the Macrokit pattern are the same optimization.

## 7. Honest limits

- **The exact region is open.** As in network information theory, the inner/outer bounds here need not meet;
  the true `𝓡` may be strictly inside the cut-set outer bound of §2. We claim the **outer bounds** and the
  **qualitative shape**, not a closed-form capacity region.
- **Stationarity & ergodicity.** Growth rates are long-run averages; the Kelly-portfolio result (§3) assumes a
  stationary, ergodic-enough world. Regime shifts in `q` break the time-average law.
- **Convexity for prices.** The operating-point/price story inherits [`03`](03-cross-frame-value.md) §8: it
  needs the smooth-goal (convex) regime; thresholds/satiation can destroy equilibrium prices.
- **Static frames.** `k_a`, `p_a`, `Y_a` are held fixed. In reality they *evolve* — and the strategic lever of
  §5 (shaping `𝓡` by changing `k` and `I`) is itself a dynamical process this static picture only points at.
- **Alignment as a scalar.** `cos θ_{ab}` is a pairwise, local linearization; genuine multi-way interactions
  (three agents whose pairwise alignments are positive but whose joint action conflicts) are not captured by
  `M` alone.

## 8. What this closes, and the one thread left

**Closed.** The trilogy 01–03 unifies into a fleet theory: a value capacity region bounded by `H(X)`, shaped
by the alignment matrix, with the operating point priced à la Kelly. Governance splits into *shaping the
region* (alignment + perception design) and *pricing the point* (resource allocation). The Macrokit pattern is
revealed as the fleet's perception-design instrument. Every prior result feeds in: the log law (per-agent
scale), the `I(X;Y)` capacity (the bounds), price + alignment (point + shape).

**The one thread left — Thread C, dynamics.** Everything proven across 01–04 is a *steady-state* or
*static-frame* result. The remaining question is the **time evolution**: how do `k` (goals), `p` (beliefs),
and `π` (prices) move? Sub-questions, each with an existing-field anchor:

- *Belief dynamics* — `p_a → q` is learning; rate-of-convergence is a **regret bound** (online learning). By
  [`02`](02-coding-theorem-of-value.md) §4 this is literally the rate of value-recovery from dissipation.
- *Price dynamics* — tâtonnement / market-clearing convergence of `π`; when does the fleet's pricing process
  itself converge, and how much value does it dissipate while searching?
- *Goal dynamics* — how `k_a` is set and drifts; **alignment-as-choosing-`k`** becomes a control problem on the
  shape of `𝓡`. This is where "value alignment" stops being a slogan and becomes a controllable dynamical
  system.

Thread C would give the thesis its *transient* law to sit beside the steady-state laws of 01–04 — the
equations of motion to go with the conservation laws.

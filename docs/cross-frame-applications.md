# The cross-frame / price layer's real-world test bed (research direction)

> A connecting note, not a result. The single-agent laws ([`01`](01-core-formalization.md),
> [`02`](02-coding-theorem-of-value.md)) are now validated in-domain and across task shapes on real LLMs
> ([`06`](06-real-agent-test.md), [`14`](14-bridge-generalization.md)). The **multi-agent cross-frame / price
> layer** ([`03`](03-cross-frame-value.md), [`04`](04-multi-agent-capacity-region.md)) is the part the
> LLM-agent experiments *could not reach* — small-model token bias and underpowering blocked the
> goal-dynamics/coordination tests ([`11`](11-real-agent-field-test.md), [`13`](13-incentive-vs-oversight-real.md)).
> This note identifies a different empirical arena where that layer *can* be tested: **observable value-flow
> across networks of substrates.** It is a candidate test bed, with honest confounds, not a claim.

## Why a second arena, and why this one

The cross-frame results — *value is frame-relative, price is frame-independent*; resource flows down shadow-
price gradients; cross-frame transfer is friction-limited and never lossless — are claims about **populations of
agents exchanging value across frames.** Real small LLMs turned out to be a poor instrument for *that* layer
(they coordinate by focal points, not by spontaneously responding to a value/price field). But there is a
domain where the same structure appears with **fully observable, abundant data and real economic agents**:
systems in which value (and the rights/claims that carry it) moves across multiple substrates/networks, where
every flow, price, and transfer cost is recorded. Ledgered / on-chain value-flow systems are the cleanest such
instance simply because their flow and price data are public — a *data-availability* point, not an endorsement
of any domain.

Crucially, this arena is **not blocked by the small-LLM ceiling** that sank the agent-dynamics tests: the
"agents" are real value-holders, the "frames" are real substrates with differing local valuations, and the
quantities the theory needs (cross-frame value differences, transfer frictions, prices) are *measured, not
elicited from a weak model.*

## The structural correspondence (concepts, not any domain's framing)

An earlier, independent line of the author's work reached the same architecture from a completely different
direction ("value sits between information and physics; substrate-grounded; price compresses beliefs; agency-
coupling; arbitrage/friction limits free creation"). Its applied formalism maps almost one-to-one onto the
cross-frame layer here:

| Cross-frame layer ([`03`](03-cross-frame-value.md)/[`04`](04-multi-agent-capacity-region.md)) | Observable value-flow instantiation |
|---|---|
| value is **frame-relative**; each agent's `V` lives in its own `k`-basis | each substrate assigns a *local* value to the same right/claim |
| **price is frame-independent** — the scalar all frames agree on | the cross-substrate price of a transferable claim |
| transfer is **friction-limited** (non-negative loss; never lossless): transfer only when the gain exceeds the friction | move value `i→j` only when `V_j − V_i > f` (a measurable threshold) |
| resource flows **down shadow-price gradients** until prices equalize ([`04`](04-multi-agent-capacity-region.md) §3) | flows run from lower- to higher-value substrates until arbitrage closes |
| **gains from trade** when frames value channels differently (positive-sum) | coordination surplus captured by moving to a better-aligned substrate |

Two enrichments the applied view suggests for the abstract theory:
- **A friction decomposition.** [`03`](03-cross-frame-value.md) treats transfer friction as a single
  non-negative loss; in practice it is a *sum* of distinguishable components (bridging, compliance, latency,
  conversion, custody). Decomposing the friction term is a faithful, testable refinement of the transfer law.
- **Liquidity / network-effect feedback.** Realized price is the value discounted by a liquidity factor that
  *grows with participation*, creating a positive feedback (more flow → deeper liquidity → higher realized
  price → more flow). The current dynamics ([`05`](05-dynamics.md)) have no such network-effect amplification;
  it is a candidate addition to the price-flow equations.

## A candidate test (pre-registered, honest)

The question the cross-frame layer makes falsifiable in this arena:

> Does observable value flow across substrates obey [`03`](03-cross-frame-value.md)'s predictions —
> **(i)** flows run *down* the cross-substrate value/price gradient; **(ii)** transfer is *friction-gated*
> (a flow occurs only when the value differential exceeds the measured friction, `V_j − V_i > f`); and
> **(iii)** the cross-substrate **price** is the frame-independent coordinate on which otherwise-incomparable
> holders agree?

Design discipline (same as the agent experiments): **pre-register** the predictions and thresholds before
touching data; define the observable proxies (value differential, friction components, price) up front; report
the verdict whichever way it falls. The friction-gated prediction (ii) is the sharpest and most distinctive —
it is the empirical face of "value transfer is never lossless."

## Honest cautions

- **Confounds dominate, and physics-envy is the failure mode here too.** Real value-flow is driven by
  expectations, narrative, regulation, and reflexive feedback — "social processes dominate." A clean gradient-
  descent / friction-gated law may *not* hold; if it doesn't, that is a real, reportable negative, not a reason
  to fit epicycles. Pre-registration is the guard.
- **This is the applied/heuristic cousin, not the rigorous core.** The correspondence is structural; the
  abstract theorems ([`03`](03-cross-frame-value.md)) are rigorous, the applied instantiation is a measurement
  hypothesis. Keep them separate.
- **Convergence ≠ independent validation.** The earlier work reaching the same architecture is a *robustness*
  signal (the intuition survives a change of route), not third-party confirmation — and the two lines *diverge*
  on the substrate (the earlier one explicitly disclaims thermodynamic grounding; here it is a *candidate*
  substrate). The agreement is at the architectural level — value between information and physics, substrate-
  grounded, price-mediated — not on the physics.
- **Keep the framing substrate-agnostic.** The arena is "observable value-flow across networks"; specific
  market/protocol framings are instances, not the theory. Do not let a domain's vocabulary leak into the
  substrate-agnostic core.

## Status

A **research direction**, gated behind the published core. It matters because it is the one empirical arena
that reaches the cross-frame/price layer the LLM-agent tests could not, with real agents and observable data —
a genuinely different shot than the agent experiments, in a domain where the data is abundant and the
quantities are measured rather than elicited. Whether it confirms or falsifies [`03`](03-cross-frame-value.md)'s
flow/friction/price predictions, it would be the first real-world test of the multi-agent half of the theory.

# Cross-Frame / Price Layer on Real-World Value-Flow — the Verdict

> The "upside shot": the one empirical move that might escape the *just-Kelly* critique by testing the
> **multi-agent** half of the theory ([`03`](03-cross-frame-value.md), [`04`](04-multi-agent-capacity-region.md))
> on observable real-world value-flow with *measured* quantities — the layer the LLM-agent tests could not reach
> ([`11`](11-real-agent-field-test.md), [`13`](13-incentive-vs-oversight-real.md)). Pre-registered in
> [`sim/realdata/PREREGISTRATION.md`](../sim/realdata/PREREGISTRATION.md) (frozen + committed before any data).
> **Verdict: (b) CAP — not resolvable on observational data — refined into a precise structural statement of
> *why*, and a roadmap of what would resolve it.** Byline: Cheng Qian.

## 1. What this had to clear

A confirmation only counts if it is **distinctively value** — something Kelly / information theory / decision
theory cannot produce. The cross-frame flow predictions fail that bar by inspection: instantiated in any
money-market they *are* arbitrage, the law of one price, Arrow–Debreu equilibrium, and log-utility shadow
prices (`λ = K/E`). The project's own red-team already concedes this (A4: doc 03 is "GE repainted"; A2: the
free-energy substrate that would distinguish `λ = K/E` from a preference price is "decorative"). So the first
and hardest job was not to find data — it was to **isolate a prediction that diverges from standard theory at
all**, then ask whether *that* one is measurable.

## 2. The one prediction that diverges — and the null it must beat

Exactly one survives the screen (prereg §1): the **multi-agent value capacity-region ceiling** (doc 04 §2), in
its *region* form, not the scalar:

$$\sum_{a\in S} G_a \;\le\; I\!\big(X;\,Y_S\big)\ \ \forall S,\qquad\text{so}\qquad \sum_a G_a \le I(X;Y_{1:m})\le H(X).$$

The distinctive content is **not** "you can't grow faster than `H(X)`" as a slogan — it is (i) the
**all-subsets cut-set shape** (the multiple-access region), and (ii) its corollary that **redundant perception
buys zero marginal collective throughput**: collective growth saturates at `I(X;Y_{1:m})`, which lies *below*
`Σ_a I(X;Y_a)` by the measured redundancy `Σ I(Y_a;Y_b\mid X)`. Standard finance has **no `H(X)`-denominated
collective ceiling and no cut-set region.** This is the prediction the handoff and red-team A7 both name as the
honest candidate for a novel, quantitative claim.

It must beat a named null on the same data (prereg §2): **Grinold breadth** (saturation level a free parameter,
no `H(X)`), **Sharpe's arithmetic** (`Σ G_a ≤ 0`, zero-sum), and the **forecast-aggregation / data-processing**
account (combined resolution `≤ I(X;Y_{1:m})` *by the DPI* — tautologically). P★ beats these **only if the
saturation level equals an *independently measured* `I(X;Y_{1:m})`/`H(X)`** — a number the nulls do not contain
and cannot fit — *and* the equality is non-tautological.

## 3. Why no observational arena can host the test (the vise)

The resolvability criterion (prereg §3) demands all four of: **R1** positive-sum-from-the-world (else
zero-sum, ceiling vacuous); **R2** common-unit per-agent growth *coupled by a conserved resource yet not pooled
into one portfolio*; **R3** an `H(X)`/`I(X;Y_S)` estimated *independently* of the growth data; **R4**
falsifiability (the bound must be *able* to fail). The pre-data screen (prereg §5):

- **Money-markets / cross-venue flow** fail **R2**: either one rebalanced book — and then `d log W/dt ≤
  I(X;Y_{1:m})` is just the single-agent **Cover/Kelly** bound on the aggregate ("just Kelly") — or a closed
  market, and then **N-zero** zero-sum makes the `H(X)` ceiling vacuous. (The flow/price predictions are also
  §0-trivial: arbitrage / LOOP.)
- **On-chain MEV / arbitrage** fails **R1 & R4**: extraction is competed away from counterparties (zero-sum),
  the searchers share one public mempool (redundancy total), and "more searchers ≠ more extraction" is plain
  Bertrand competition — the null predicts it identically. This is literally the *just-arbitrage* trap.
- **Common-pool harvest** (attention, ad-impressions, block rewards, fisheries) fails **R3**: a conservation
  ceiling `Σ ≤ V_total` exists, but `V_total` is a quantity of *resource*, not an *entropy*. Confirming it is
  throughput conservation, not the information ceiling; `H(X)` is not independently estimable.
- **Forecasting / prediction tournaments** — the *only* arena giving jointly-observed `(X, Y_a)`, hence a
  computable `I(X;Y_S)` — fail **R4 (and R2)**: scores are independent per forecaster (no coupling), and the
  combined-forecast bound holds **by the data-processing inequality**. It is a tautology, and the
  forecast-aggregation null predicts the same number. A tie by construction.

**The common reason.** P★'s discriminating content lives in the *coupled-but-separate* multi-agent regime.
Observational data only ever exposes the two degenerate corners — **uncoupled** (the ceiling is simply false /
inapplicable: `Σ_a I(X;Y_a)` can reach `m·H(X)`) or **fully-pooled / closed** (single-agent Kelly, or
zero-sum Sharpe). The intermediate regime where the region bound is *both binding and falsifiable* is exactly
the one that requires **measuring counterfactual sub-coalition throughputs** — which no observational record
contains.

## 4. Verdict — (b) CAP, refined

Per the pre-committed decision rule (prereg §4.3): **no arena passes R1–R4 → verdict (b): not resolvable on
observational data.** Crucially, this is **not** "the data was too noisy." It is structural: the cross-frame /
price layer offers **no observational test that is simultaneously discriminating and resolvable.** Wherever the
distinctive prediction *would* bind, observational value-flow collapses it into Kelly, Sharpe, GE, or arbitrage
(verdict-(a) territory); the only arena that exposes the joint information (forecasting) makes it a
data-processing tautology that the standard null matches exactly.

As instructed, we **do not** retreat to a flow/friction/price prediction to manufacture a number — that is the
trap the whole mission was designed to avoid. No data was downloaded; running a test that can only reconfirm
arbitrage would be physics-envy, not evidence.

## 5. What this *does* establish (it is not nothing)

This sharpens the paper's most dangerous concession. Red-team **A7** ("no novel, surprising, confirmed
prediction") was answered with "we haven't tested the fleet ceiling yet — here's the roadmap." This analysis
upgrades that to a **precise structural claim**:

> The cross-frame / price layer's one distinctively-value prediction — the capacity-region cut-set ceiling —
> is **not falsifiable on observational value-flow data**, because every observable arena realizes one of the
> two degenerate corners (uncoupled → ceiling inapplicable; pooled/closed → Kelly or zero-sum). The prediction
> is testable **only** in a *controlled* setting that can construct and measure sub-coalition throughputs.

That is a real result: it tells the reader exactly where the theory's empirical content does and does not lie,
and it forecloses a tempting class of "we confirmed it in market data" claims as category errors.

## 6. The one route that *would* resolve it (roadmap, not a result)

P★ meets R1–R4 only under a **controlled multi-agent experiment with *measured* signals**:

1. **Construct the coupling.** A fixed shared resource pool and a shared world `X` with *known* `H(X)`
   (a designed task distribution), so the sum-ceiling can bind and `H(X)` is known by construction, not fit
   (satisfies R1, R2-coupling, R3).
2. **Vary perception overlap deliberately.** Assign agents signals `Y_a` with *controlled* redundancy
   `I(Y_a;Y_b\mid X)` — from near-orthogonal to near-clones — so the predicted gap between `I(X;Y_{1:m})` and
   `Σ_a I(X;Y_a)` is swept, not observed once.
3. **Measure each sub-coalition's realized growth** `Σ_{a\in S} G_a` against its own `I(X;Y_S)`, testing the
   *region* (all-subsets), not just the full-fleet scalar (the part that escapes Kelly).
4. **Pre-register P★ vs Grinold-breadth** with the saturation level pinned to the *designed* `H(X)`: P★ wins
   iff the saturation tracks the known `I(X;Y_{1:m})` across the redundancy sweep while the free-parameter null
   needs a different per-condition fit.

This is the **LLM-agent route** — and it is precisely the route that hit the **small-model ceiling** (docs 11,
13): small models coordinate by token/focal-point bias, not by responding to a value field, so they are a poor
instrument for the coupled multi-agent dynamics. So the honest standing of the upside shot is:

- **observational real-world value-flow** cannot host the discriminating test (this doc, §3–4);
- **controlled agent experiments** can host it in principle but need an instrument (agent population) that
  *actually responds to a value/price field* — beyond current small open models.

The upside therefore **survives as a well-specified future experiment**, not as a result available now. It is
gated on a stronger agent instrument (or a non-LLM controlled substrate that demonstrably couples through a
shared resource), with the design above pre-registered.

## 7. Honest limits of *this* verdict

- **A CAP is arena-relative.** "Not resolvable on observational value-flow data" is a claim about the arenas
  screened (prereg §5). A genuinely positive-sum, common-unit, coupled-but-separate system with an
  independently-estimable `H(X)` would reopen the test; we argue such a system is exactly what observational
  records lack, but we cannot prove no such public dataset exists. If one is proposed, it must clear R1–R4
  *before* any run.
- **The screen is structural, not exhaustive.** It rests on the reduction arguments (§3 / prereg §5), not on
  having tried every dataset. Its strength is that the reductions are corners of the *same* region geometry,
  not a list of coincidences.
- **No new claim is added to the core paper.** This is a negative/scoping result. It strengthens the
  limitations and the A7 discussion; it does not license any positive empirical statement about real markets.

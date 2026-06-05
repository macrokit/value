# PRE-REGISTRATION — Cross-frame / price layer, real-data test (the upside shot)

**Frozen before touching any data.** This file fixes, *in advance*: the one prediction of the
cross-frame / price layer (docs [`03`](../../docs/03-cross-frame-value.md),
[`04`](../../docs/04-multi-agent-capacity-region.md)) that **diverges from standard finance / decision
theory**; the **standard-economics null it must beat**; the **resolvability criterion** an arena must meet for
the comparison to be both discriminating *and* testable; and a **pre-committed decision rule** — including the
clause that stops the effort if no arena meets the criterion. Written in the discipline of the prior
pre-registrations (Rung 7/8): thresholds and the falsification/stop clause are committed first; a negative or
a "not testable here" is a real, reportable result; physics-envy (manufacturing empirical flavour) is the
failure mode. Author byline: **Cheng Qian**. This file's commit precedes any analysis or data commit.

---

## 0. The mission, stated as a trap to avoid

The cross-frame / price layer is the one piece of the theory the single-agent bridge (`ΔG = I(X;Y)`) does not
already cover — the part that is distinctively *value* rather than *Kelly*. The upside is an empirical result
**Kelly / information theory / decision theory cannot explain.** The trap, equally explicit: the layer's flow
predictions, instantiated in any money-market, **collapse into textbook economics** —

- "value flows down the value/price gradient" → **arbitrage**;
- "transfer only when `V_j − V_i > f`" → **arbitrage-with-transaction-cost**;
- "price equalizes across venues" → the **law of one price**;
- "a price emerges that coordinates incomparable holders" → **Arrow–Debreu general equilibrium** (and the
  paper's own red-team A4 already concedes doc 03 is "GE repainted");
- "shadow price `λ_a = K_a/E_a`, resource flows low-`λ`→high-`λ`" → **log-utility / Kelly** (the very "just
  Kelly" critique the project is trying to escape; red-team A2 concedes the free-energy substrate is currently
  decorative, so `λ = K/E` cannot be distinguished from a preference-based price on observable data).

Confirming any of those proves **nothing distinctively value**. This pre-registration therefore commits, before
data, to test **only** a prediction that survives this screen — and to **stop** rather than run a test that can
only reconfirm arbitrage / GE / Kelly.

## 1. The single discriminating prediction (frozen)

Of the three candidate predictions in the handoff, two are excluded *a priori* by §0:

- **Price-as-coordinate for incomparable frames** — collapses to general equilibrium (price emerges for any
  exchange economy; "no shared numeraire" is not special — GE produces relative prices regardless). The only
  value-distinctive content is `λ = K/E` (price pinned by a *conserved physical substrate*, not preferences),
  and that is **not measurable** on social data: we cannot put `K_a` (goal scale) or `E_a` (free energy) in
  joules for real holders, so it cannot be distinguished from a preference-based price. **Non-discriminating or
  non-measurable. Excluded.**
- **Friction-gated transfer with a derived functional form** — alone it is arbitrage-with-transaction-cost.
  Discriminating *only* via a specific derived flow magnitude/timing, which the abstract theory does not yet
  pin down sharply enough to beat a tuned transaction-cost model. **Secondary at best. Excluded as a headline.**

The one prediction that genuinely **diverges from Kelly/finance** is the **multi-agent value capacity-region
ceiling** (doc 04 §2), in its *exact, region* form — not the scalar:

> **P★ (frozen).** For `m` agents acting on one shared world `X` and drawing growth from one conserved shared
> resource, the realized joint value-growth-rate vector `(G_1,…,G_m)` lies inside the **polymatroidal region**
> $$\sum_{a\in S} G_a \;\le\; I\!\big(X;\,Y_S\big)\quad\text{for every subset } S\subseteq\{1,\dots,m\},
> \qquad Y_S=\{Y_a:a\in S\},$$
> and in particular the full fleet obeys `Σ_a G_a ≤ I(X;Y_{1:m}) ≤ H(X)`. The **distinctive, non-Kelly
> content is the *all-subsets region shape*** — the multiple-access cut-set structure — and its corollary that
> **redundant perception buys zero marginal collective throughput**: collective growth saturates at
> `I(X;Y_{1:m})`, which sits *below* `Σ_a I(X;Y_a)` by exactly the conditional redundancy
> `Σ` of `I(Y_a;Y_b\mid X)` terms. Standard finance has no `H(X)`-denominated collective ceiling and no
> cut-set region; this is the prediction the handoff and red-team A7 both single out as the honest candidate
> for a *novel, surprising, quantitative* claim.

## 2. The standard-economics null P★ must beat (frozen, explicit)

The result is meaningful **only** if P★ beats, on the *same data*, the standard model. The null is **not**
"no relationship"; it is the strongest off-the-shelf account:

- **N-add (additive capacity / Grinold breadth).** Collective throughput grows with the number of *independent*
  bets; the saturation level is a **free parameter** (effective breadth × IC²), fit to the data — with **no
  reference to an independently-measured `H(X)`.** Grinold's fundamental law already predicts that redundant
  (correlated) signals add little — so *qualitative* sub-additivity is NOT discriminating.
- **N-zero (Sharpe's arithmetic).** In a closed market, aggregate active growth is **zero-sum** before costs,
  negative after: `Σ_a G_a ≤ 0`. Here the `H(X)` ceiling is **vacuous** (never binds; the true ceiling is 0).
- **N-agg (forecast-aggregation / diversity-prediction theorem, Page).** Collective skill = average individual
  skill − diversity; correlation caps the crowd's gain. Information-theoretic when scored by log-loss, the
  combined forecast's resolution `≤ I(X;Y_{1:m})` holds **by the data-processing inequality** — i.e.
  tautologically, predicting the same number P★ does.

**P★ beats the null only if the collective-throughput saturation level equals an *independently measured*
`I(X;Y_{1:m})` / `H(X)` — a quantity the null does not contain and cannot fit — and the equality is
non-tautological (the data-generating process could have violated it).** Anything weaker is a tie, and a tie is
verdict (a)/(b), not the prize.

## 3. Resolvability criterion (frozen) — what an arena MUST provide

P★ is testable-and-discriminating in an arena **iff all four hold**:

- **R1 — Positive-sum-from-the-world.** Agents extract growth from a shared *external uncertain process*, not
  (only) from each other. *(Else N-zero: zero-sum, `H(X)` ceiling vacuous.)*
- **R2 — Coupled-but-not-collapsed common-unit growth.** Per-agent `G_a` are in a common unit and *coupled by a
  conserved shared resource* (so the sum-ceiling can bind), yet **not pooled into one rebalanced portfolio**.
  *(If uncoupled separate pools: `Σ_a G_a = Σ_a I(X;Y_a)` ranges up to `m·H(X)` — the ceiling is simply
  **false/inapplicable**, nothing to confirm. If one rebalanced pool: `d log W/dt ≤ I(X;Y_{1:m})` is the
  single-agent **Cover/Kelly** bound on the aggregate — "just Kelly," not multi-agent.)*
- **R3 — Independently-estimable `H(X)` / `I(X;Y_S)`.** The world entropy and the joint signal information must
  be estimable from a source **disjoint from the realized-growth data** used to compute `G_a`. *(Else the
  ceiling is computed from the same numbers it bounds → circular / tautological → ties N-agg.)*
- **R4 — Falsifiability.** The data-generating process must be *able* to violate the bound, so that holding is
  informative. *(A bound that holds by construction/data-processing is a tautology, not a confirmation.)*

## 4. Pre-committed decision rule (frozen)

1. **Screen arenas against R1–R4 *before* downloading any data** (the screen below, §5). The screen is itself
   the pre-registered analysis: it is judged on the *structure* of each arena, not on fitted results.
2. **If an arena passes R1–R4:** freeze its observable proxies (the per-agent `G_a`, the signals `Y_a`, the
   independent `H(X)` estimator) and PASS/FAIL thresholds *in an addendum to this file*, commit that addendum,
   **then** download + cache data and run P★ vs the null. PASS = P★'s `H(X)`-pinned ceiling fits within CI and
   the null's free-parameter fit is *not* needed (formally: the `H(X)`-constrained model is not rejected and a
   nested likelihood-ratio / out-of-sample test does not prefer the free-saturation null). Report verdict
   (c) discriminating-confirm or (d) falsification.
3. **If no arena passes R1–R4:** report verdict **(b) CAP — not resolvable on observational data**, and
   **stop. Do NOT** weaken P★ to a flow/friction/price prediction merely to have a number to report — that is
   the §0 trap and is forbidden by this pre-registration.

## 5. A priori arena screen (frozen, pre-data) — the vise

Each candidate observational arena fails at least one of R1–R4. This screen is committed before data; it is the
substance of the (b)-CAP verdict if no arena survives.

| Arena | Agents / `G_a` | Fails | Why |
|---|---|---|---|
| **Money-market / cross-venue flow** | traders, returns | **R2** | Either one rebalanced book (→ single-agent Kelly bound, "just Kelly") or a closed market (→ N-zero, ceiling vacuous). And the flow/price predictions are §0-trivial (arbitrage / LOOP). |
| **On-chain MEV / arbitrage extraction** | searcher bots, profit | **R1, R4** | Extracted value is conserved and competed *away from* LPs/traders → zero-sum among searchers (N-zero). Signals = the shared public mempool → `I(X;Y_S)` identical for all `S`, redundancy total → "more searchers ≠ more extraction" is **Bertrand competition / arbitrage**, predicted identically by the null. Literally the §0 trap. |
| **Common-pool harvest** (attention, ad-impressions, block rewards, fisheries) | harvesters, share | **R3** | A conservation ceiling `Σ ≤ V_total` exists, but `V_total` is a quantity of resource (dollars, impressions, biomass), **not** an information entropy. Confirming `Σ ≤ V_total` is mass/throughput conservation, not the `H(X)` ceiling; `H(X)` is not independently estimable. |
| **Forecasting / prediction tournament** (public, e.g. resolved-question sets) | forecasters, log-score gain | **R4 (and R2)** | This is the *only* arena giving jointly-observed `(X, Y_a)`, so `I(X;Y_S)` is computable. But scores are *independent per forecaster* (no shared pool, R2 fails the "coupled" side), and the combined-forecast resolution `≤ I(X;Y_{1:m})` holds **by the data-processing inequality** — a tautology (R4 fails). The null **N-agg predicts the identical number.** Tie by construction. |

**Common structural reason all four fail.** P★'s discriminating content is the *coupled* multi-agent
cut-set region. Observational data offers only the two degenerate corners: **uncoupled** (ceiling false/
inapplicable) or **fully-pooled / closed** (single-agent Kelly, or zero-sum Sharpe). The intermediate
*coupled-but-separate* regime where the region bound is both binding and falsifiable is exactly the regime that
requires **forming and measuring counterfactual sub-coalition throughputs** — which observational records do
not contain. Testing the region shape therefore requires a **controlled multi-agent experiment with measured
signals** (assign agents, vary perception overlap, measure each sub-coalition's realized growth). That is the
LLM-agent route — which already hit the small-model ceiling (docs 11, 13). Hence P★ is **currently not
resolvable with measured real-world quantities.**

## 6. Honesty discipline (frozen)

- **The null is the whole game.** Report P★ vs the named null with CIs, or report that the arena cannot host
  the comparison. No P★ result is reported without its null.
- **Physics-envy guard.** Do not run a tautological or vacuous test to manufacture an empirical number; a
  reasoned "not resolvable here" is the honest result and is *worth more* than a tie dressed as a confirmation.
- **No epicycles.** If a passing arena yields (d) falsification, report it; do not add liquidity/feedback
  enrichments post hoc to rescue P★.
- **Substrate-agnostic core.** Any arena is an *instance*; the theory and the core paper stay general
  (Sacred Rule #1). Cache/snapshot all data if §4.2 is reached.
- **Outcome ledger.** (a) trivial-confirm = reduces to arbitrage/GE/Kelly → worthless; avoid by design.
  (b) CAP = not resolvable / un-estimable `H(X)` → honest "not testable in this arena." (c) discriminating
  confirm = P★ beats the null → the prize. (d) clean falsification = P★ loses to the null → real negative.
  **Only (c) or (d) count as the upside; pursue a design that can deliver them, never one that can only
  deliver (a).**

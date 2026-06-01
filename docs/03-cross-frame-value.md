# Cross-Frame Value — Exchange, Geometry, and Price

> Thread B from [`02-coding-theorem-of-value.md`](02-coding-theorem-of-value.md) §7: define the
> transformation between two agents with different goal-weight/belief bases, and find the invariant beyond the
> shared budget `E`. This is the piece the "govern *separated* AI individuals" goal actually needs — all prior
> results were single-frame.

## 0. The honest starting point: do not try to make value cardinally comparable across agents

The first instinct is to seek a god's-eye value scale on which agent A's and agent B's values are directly
comparable — a "universal util." **No such scale exists, and the impossibility is a theorem, not a gap in our
work.** Interpersonal cardinal comparison of value is not pinned down by preferences (the interpersonal-utility
problem); aggregating ordinal frames into one canonical order is impossible under mild axioms (Arrow). Any
theory that claims to sum incomparable agent-values is smuggling in a value judgment.

So the goal of Thread B is **not** "compare A's value to B's." It is: *find the lawful structure that lets
separated agents coordinate without that comparison.* Real economies do exactly this — they coordinate
billions of incomparable utilities through **prices**, never through a cosmic utility sum. We will recover the
same resolution from the physics of the shared substrate.

What we have that pure preference-economics lacks: every agent spends the **same** resource, free energy `E`
([`00`](00-thesis-seed.md) §3). That shared substrate is what breaks the impasse — not by making values
comparable, but by pinning a price.

## 1. The two axes on which frames differ

Two agents `A`, `B` differ along two independent axes:

- **Goal axis** — the goal-weight covector `k_A` vs `k_B` (what matters). From [`01`](01-core-formalization.md).
- **Belief axis** — the world-model `p_A` vs `p_B` (what is expected). From [`02`](02-coding-theorem-of-value.md).

These produce *qualitatively different* interactions (§6): goal-differences create **gains from trade**
(positive-sum); belief-differences create **speculation** (zero- or negative-sum). Keeping them separate is
essential and is usually conflated in informal "value alignment" talk.

## 2. The scalar part of the transformation — exchange through the substrate

Value is never converted agent-to-agent directly; it is converted *through joules*. From
[`01`](01-core-formalization.md) §4, `V_A^* = K_A \ln E_A − K_A H(\hat k_A)`, so the **marginal value of
resource** (the shadow price of free energy in A's frame) is

$$\lambda_A \;=\; \frac{\partial V_A^*}{\partial E_A} \;=\; \frac{K_A}{E_A}.$$

`λ_A` is denominated in (A-value)/(joule) — it is A's internal-scale-to-substrate conversion factor. Hence the
**cross-frame exchange rate**:

$$\boxed{\,T_{A\to B} \;=\; \frac{\lambda_B}{\lambda_A} \;=\; \frac{K_B/E_B}{K_A/E_A}.\,}$$

This is the value-theory analog of a Lorentz factor / a currency cross-rate: the scalar magnitude of value
*does* transform cleanly between frames, because it passes through the invariant `E`.

### The shadow price equalizes — and that is the emergent price

Transferring `dE` from A to B changes total realized value by `dV = (\lambda_B - \lambda_A)\,dE`. So resource
flows from **low-shadow-price to high-shadow-price** agents, raising total value, until a single `λ*` clears
the fleet:

$$\lambda_A = \lambda_B = \cdots = \lambda^\* \quad\text{at equilibrium.}$$

This is mechanically a **thermodynamic equilibration** — `λ` equalizes across agents like temperature across
bodies in thermal contact, or chemical potential across a membrane. The common value `λ*` is the
**frame-independent price of free energy** — pinned not by any interpersonal comparison but by the
conservation of the shared resource. *This is the first invariant beyond `E` itself: not a quantity of value,
but a price.*

## 3. The directional part — the irreducible inter-frame structure

Factor each frame into scale and direction: `k_A = K_A\,\hat k_A`, with `\hat k_A` on the simplex. The scale
`K_A` fed §2; the **direction** `\hat k_A` is the genuinely frame-specific part that does *not* reduce to `E`.
The natural scalar between two directions is the **alignment**

$$\cos\theta_{AB} \;=\; \langle \hat k_A,\, \hat k_B\rangle_g$$

(inner product in the metric `g` of §4). It governs whether two agents sharing a world create or destroy value:

| `θ_{AB}` | interaction | fleet consequence |
|---|---|---|
| small (aligned) | value-gradients reinforce | **positive-sum** — pool resource |
| `π/2` (orthogonal) | independent goals | no interaction |
| large (opposed) | each agent's progress destroys the other's value | **negative-sum** — the Second Law ([`00`](00-thesis-seed.md) §4) at fleet scale |

The directional part is where *all* multi-agent value creation and destruction lives. It is exactly the part
that has no single-number cross-frame reduction — which is the precise, geometric restatement of §0's
impossibility result.

## 4. The invariant, rigorously — the Fisher–Rao metric (Čencov)

What do *all* frames agree on, whatever their goals? The **geometry of the state space**. The simplex of
world-states (or of resource allocations) carries the **Fisher–Rao metric**, and by **Čencov's theorem** this
is the *unique* Riemannian metric invariant under sufficient statistics (congruent Markov maps). It is
canonical — not a modeling choice.

This makes the relativity analogy exact rather than decorative:

| Relativity | Value |
|---|---|
| spacetime manifold | state simplex |
| Lorentz metric (canonical) | **Fisher–Rao metric (canonical, by Čencov)** |
| observer's time/space split | agent's goal-covector `k_A` |
| invariant spacetime interval | the shared Fisher geometry (+ the price vector, §5) |
| coordinate time (frame-relative) | realized value `V_A` (frame-relative) |

**Value is a covector `k_A` paired with a shared state-velocity `de` in the shared metric:**

$$dV_A \;=\; \langle k_A,\, de\rangle \;=\; \sum_i k_{A,i}\,\frac{de_i}{e_i}.$$

The `1/e_i` is the Fisher/log structure — the metric, not the goal. The geometry is **one**; the goals are
**many** covectors on it. Different agents are different "value coordinates" over a single invariant manifold,
precisely as different observers are different coordinatizations of one spacetime.

## 5. The resolution — price as the frame-independent universal coordinate

Generalize §2 from a single resource to the full channel space. Let the fleet share a supply of
channel-progress; let `π = (π_1,…,π_n)` be a **price vector** over channels. Each agent faces the *same* `π`
but holds its *own* `k_A`, and buys progress on channel `i` where `k_{A,i}/π_i` is largest. Prices adjust
until demand meets supply (a standard Arrow–Debreu equilibrium; existence holds because log-value is concave —
[`01`](01-core-formalization.md)).

At equilibrium:

- each agent's **value `k_A` stays its own** — never compared to anyone else's;
- the **price `π` is shared and objective** — pinned by the resource constraint, agreed by all frames;
- coordination is achieved through `π`, **without** any interpersonal cardinal comparison.

$$\boxed{\text{Value (}k\text{) is frame-relative; price (}\pi\text{) is frame-independent.}}$$

Price is the objective shadow the collective casts — the value-theory analog of the invariant interval, and
the operational answer to "what do all frames agree on." It exists *because* the substrate `E` is conserved
and shared, which is exactly what pure-preference economics lacked and what makes value (here) physical rather
than merely psychological.

## 6. Goal-difference vs belief-difference: trade vs speculation

The two axes of §1 produce opposite-signed interactions — a distinction the price machinery makes sharp:

- **Differing goals (`k_A ≠ k_B`), shared beliefs.** Agents value channels differently *in relative* terms ⇒
  **gains from trade / comparative advantage**: each gives up progress it values less for progress it values
  more, both rise. **Positive-sum.** Value is *created* by goal-diversity. Encourage it.
- **Differing beliefs (`p_A ≠ p_B`), shared goals.** Agents bet against each other on what the world will do ⇒
  **speculation.** Under a common true law `q`, this is **zero-sum in expectation**, and **negative-sum** if
  both models are wrong (each pays the Second-Law dissipation `D(q\|p)` from [`02`](02-coding-theorem-of-value.md) §4).
  Its one redeeming use is **information aggregation** — a prediction market that pools the agents' private
  bits into a sharper collective `p`. Otherwise it is friction to suppress.

**Governance rule:** cultivate goal-diversity (it trades to positive-sum); meter belief-disagreement (let it
aggregate information, but do not let agents burn shared resource speculating against each other).

## 7. Application — governing a fleet of separated AI individuals

The cross-frame machinery yields a concrete control surface:

1. **Run an internal price vector `π` over shared resources/channels.** It coordinates agents with
   *incomparable* values — no need to (and no way to) put them on one util scale. This is how to manage
   "separated" individuals without a central utility function.
2. **Equalize shadow prices `λ_a`** by routing free energy from low-`λ` to high-`λ` agents — the value analog
   of pressure equalization; raises total realized value monotonically.
3. **Track the alignment matrix `\cos θ_{ab}`.** Co-locate aligned agents (pool); separate opposed agents
   (their coexistence dissipates value); exploit orthogonal/complementary agents via trade.
4. **Separate the two frictions.** Goal-conflict (negative `\cos θ`) is structural — fix by re-aiming `k` or
   separating agents. Belief-conflict (`p_a ≠ p_b`) is informational — fix by sharing information until models
   converge, or harvest it once via a prediction market, then stop.

## 8. Honest limits

- **We did not solve interpersonal cardinal comparison — by design.** §0's impossibility stands; we route
  around it via price. Anyone wanting a single fleet-wide "total value" number is asking for something that
  provably is not canonical. Price-based coordination is the honest most we can offer.
- **Equilibrium prices need convexity.** The threshold/satiation/risk-seeking non-convexities of
  [`01`](01-core-formalization.md) §6 break price existence (classic Arrow–Debreu failure). Smooth-goal regime
  only.
- **The geometry is cleanest locally.** Fisher–Rao is canonical but curved; the "angle `θ`" picture is exact
  near a reference state and approximate globally.
- **`λ_A = K_A/E_A` assumed the single-frame optimum.** Out of equilibrium, or with coupled budgets, `λ` is a
  local linearization, not a global constant.

## 9. What B closed and opened

**Closed.** The cross-frame transformation exists: scalar magnitude transforms through the substrate
(`T_{A→B} = λ_B/λ_A`); the invariant is the Fisher–Rao geometry (Čencov) plus the emergent price vector;
coordination of incomparable frames is achieved by price, not by an impossible cardinal sum. The relativity
analogy is now exact (shared canonical manifold, frame-dependent covectors). Goal-diversity is positive-sum
(trade); belief-divergence is zero/negative-sum (speculation).

**Open — the real prize (A + B): the multi-agent capacity region.** Single-agent: value-throughput
`≤ I(X;Y)` ([`02`](02-coding-theorem-of-value.md)). Multi-agent with prices and alignment (this doc): what is
the **achievable region of joint growth rates** for `m` interacting agents sharing one world and one resource
pool? Shannon has a capacity *region* for broadcast/multiple-access channels; the value analog — the Pareto
frontier of fleet growth as a function of the alignment matrix and the price vector — is the unification of
all three docs and the actual theory of *governing* (not just measuring) a population of AI individuals.

Secondary open thread: **dynamics** ([`02`](02-coding-theorem-of-value.md) §7, Thread C) — how `k`, `p`, and
`π` evolve in time; alignment-as-learning; a value-flavored regret bound for the price-finding (tâtonnement)
process.

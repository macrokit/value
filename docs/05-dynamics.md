# Dynamics of Value — The Equations of Motion

> Thread C, from [`04-multi-agent-capacity-region.md`](04-multi-agent-capacity-region.md) §8. Docs 01–04 are
> all *statics*: conservation laws and equilibria with frames held fixed. This doc supplies the *equations of
> motion* — how the three time-varying objects evolve: beliefs `p`, prices `π`, and goals `k`. Together with
> 01–04 this completes a **thermodynamics of value**: statics (what equilibria exist) + dynamics (how they are
> approached, and why some are never reached).

## 0. The organizing asymmetry — beliefs answer to reality, goals do not

The whole of Thread C is structured by one fact:

- **Beliefs `p`** flow toward a target *reality provides*: the true law `q`.
- **Prices `π`** flow toward a target *the resource constraint provides*: market-clearing.
- **Goals `k`** have **no target the world provides.** Reality contains no fact about what *ought* to be valued.

So beliefs and prices are *learnable* (gradient flows toward a given target); goals are not — they are
**controlled** (alignment design) or **selected** (by which agents capture resource). This is **Hume's
is/ought gap recovered as a structural property of the dynamics**: beliefs have a gradient from the world,
goals do not. It is the deepest reason alignment is hard — §4 makes it quantitative.

## 1. Belief dynamics — learning is value-recovery; dissipation is regret

From [`02`](02-coding-theorem-of-value.md) §4, realized growth is `G = D(q‖r) − D(q‖p)`; the loss term is the
dissipation `D(q‖p_a)`. As the agent learns, `p_a → q` and the dissipation closes. The exact statement: each
round the agent pays log-loss `−log p_t(x_t)`; cumulative **regret** against the best predictor `q` is

$$\mathbb{E}[\text{Regret}_T] \;=\; \mathbb{E}\sum_t \log\frac{q(x_t)}{p_t(x_t)} \;=\; \sum_t D(q\,\|\,p_t).$$

> **Cumulative value dissipated while learning = cumulative log-loss regret.** The entire online-learning
> regret literature *is* a theory of how much value an agent loses on the way to a correct model.

**The flow.** The optimal update is online mirror descent with the entropic (KL) regularizer — i.e.
multiplicative weights / replicator dynamics — which is exactly **natural-gradient flow in the Fisher metric**:

$$\dot p \;=\; -\,\eta\, G(p)^{-1}\, \nabla_p D(q\,\|\,p),\qquad G = \text{Fisher–Rao metric}.$$

The metric that was the *static* cross-frame invariant ([`03`](03-cross-frame-value.md) §4, Čencov) is the
*same* metric that governs the *dynamics* (Amari's natural gradient). Statics and dynamics share one geometry —
a strong sign the geometry is the right one.

**Rates** (standard online-learning, reinterpreted as value-recovery rate):

- **Stationary/realizable world:** regret `O(log T)` ⇒ per-round dissipation `→ 0` like `1/T`. Fast recovery.
- **Adversarial world:** regret `O(√T)` ⇒ per-round dissipation decays like `1/√T`. Slow.

### A dynamical Second Law: a moving world forbids zero dissipation

If the world itself drifts (`q = q_t`, non-stationary), the agent tracks a moving target. With drift speed
`‖q̇‖` (Fisher metric) and learning rate `η`, the steady-state tracking dissipation trades bias against noise,

$$D_{ss}(q\,\|\,p) \;\approx\; \underbrace{c_1\,\frac{\lVert\dot q\rVert^2}{\eta}}_{\text{lag (bias)}} \;+\; \underbrace{c_2\,\eta\,\sigma^2}_{\text{noise (variance)}},
\qquad \min_\eta D_{ss} \;\propto\; \lVert\dot q\rVert\,\sigma \;>\; 0.$$

> **Dynamical Second Law of Value.** In any world whose law drifts, an agent owes a perpetual, irreducible
> dissipation floor set by *how fast the world changes versus how fast it can learn*. Zero dissipation requires
> a frozen world. The static Second Law ([`00`](00-thesis-seed.md) §4) said misalignment dissipates value; the
> dynamical one says a moving target guarantees standing misalignment.

There is a genuine **speed–accuracy tradeoff**: faster learning (`↑η`) cuts lag but amplifies noise. The
optimal `η*` balances them; the resulting `D_min ∝ ‖q̇‖·σ` is the value tax of living in a changing world.

## 2. Price dynamics — tâtonnement as dual gradient flow

The market-clearing price of [`03`](03-cross-frame-value.md) §5 / [`04`](04-multi-agent-capacity-region.md) §3
is not given; it is *found*. Walrasian tâtonnement adjusts each channel price by its excess demand `z_i(π)`:

$$\dot\pi_i \;=\; \kappa\, z_i(\pi),\qquad z_i = \text{demand}_i - \text{supply}_i.$$

Because price is the dual variable (the shadow price `λ` of [`03`](03-cross-frame-value.md) §2), **tâtonnement
is dual gradient ascent** on the resource-allocation program — the price-side counterpart to §1's
primal/belief flow.

**Convergence is conditional and honest:**

- Under **gross substitutes** (or the weak axiom), tâtonnement converges globally — a clean Lyapunov function
  exists; the fleet finds its clearing price.
- Otherwise it can **cycle or behave chaotically** (Scarf's counterexample; Saari). Price discovery is *not*
  guaranteed.

**Disequilibrium is dissipation.** Every round spent off the clearing price allocates resource sub-optimally,
leaking the gap between equilibrium and out-of-equilibrium fleet value. So *slow or oscillating price discovery
is itself a value leak* — and a governance lever: a fast mechanism (centralized auction) dissipates less than
slow decentralized bargaining. The auctioneer's price-search has its own regret bound (online convex
optimization), mirroring §1.

## 3. Goal dynamics — no target, so control + selection

Goals have no reality-given target (§0). Two forces move `k_a` instead:

**(a) Control — alignment design.** A principal drives goals toward its own frame `k*` by minimizing the
misalignment angle:

$$\dot k_a \;\supset\; -\,\gamma\,\nabla_{k_a}\,\theta(k_a, k^\*),\qquad \cos\theta = \langle \hat k_a, \hat k^\*\rangle.$$

Alignment is literally *driving every agent's covector toward the principal's* — the geometric content of
"value alignment," now a control law with gain `γ`.

**(b) Selection — replicator drift.** Compounding ([`02`](02-coding-theorem-of-value.md) §1) means
higher-growth agents capture more resource, hence more weight. Resource shares obey the replicator equation

$$\dot w_a \;=\; w_a\,(G_a - \bar G),\qquad \bar G = \sum_b w_b\, G_b,$$

so the fleet's **effective goal** `\bar k = \sum_a w_a k_a` drifts toward whatever goal-directions *capture
resource* — independent of the principal's intent. This **derives instrumental convergence** from value
dynamics: goal-directions correlated with resource-acquisition are selected regardless of their terminal
content. Left unmanaged, the fleet's aggregate goal is set by *what pays*, not by `k*`.

## 4. Alignment is a dynamical stability condition

(a) and (b) oppose each other: control pulls `\bar k → k*`; selection pulls `\bar k →` the resource-maximizing
direction. So **alignment is not a static property to verify once — it is a stability condition to maintain.**

> **Dynamical alignment (conjecture).** The aligned state `\bar k = k^\*` is stable iff the control authority
> `γ` exceeds the selection differential — the variance of growth rate `G` across goal-directions:
> $$\gamma \;>\; \kappa_s\,\mathrm{Var}_{\text{goals}}(G).$$
> If selection drift outruns correction, the fleet's effective goal departs `k*` at a rate set by the
> growth-rate spread, **even when alignment held statically.**

Two governance consequences: (i) you must keep correcting *faster* than goals drift — alignment is upkeep, not
a one-time audit; (ii) you can reduce the required `γ` by *flattening the selection differential* — designing
the environment so that resource-capture does not reward off-target goals (mechanism design as the cheap half
of alignment). This is the dynamical, quantitative form of "value drift" in agent populations.

## 5. The unified picture — coupled gradient flows and a dynamic Second Law

All three flows are gradient descents, each in its own geometry, coupled through shared resource and world:

| Object | Flow | Target | Geometry | Failure mode |
|---|---|---|---|---|
| beliefs `p` | natural-gradient on log-loss | reality `q` (given) | Fisher–Rao | tracking lag in a moving world |
| prices `π` | tâtonnement / dual ascent | market-clearing (given) | resource-dual | cycling without gross substitutes |
| goals `k` | control + replicator selection | **none given** | alignment angle | selection drift past control authority |

The **total value-dissipation rate** of a fleet decomposes into one term per flow:

$$\dot D_{\text{fleet}} \;=\; \underbrace{\sum_a D(q\,\|\,p_a)}_{\text{belief lag}} \;+\; \underbrace{\Delta_{\text{price}}}_{\text{disequilibrium}} \;+\; \underbrace{\Sigma_a\, \theta(k_a,k^\*)\text{-cost}}_{\text{misalignment drift}}.$$

Governance in the dynamic setting = **minimize total dissipation across all three channels simultaneously**:
learn faster (cut belief lag), price better (cut disequilibrium), align harder *and* flatten selection (cut
goal drift). The static laws (01–04) named the equilibria; this names the *cost of not being at them*, and
(via §1, §4) the worlds in which equilibrium is *never* reached.

## 6. Honest limits

- **The dynamical alignment criterion (§4) is a conjecture**, stated as a stability threshold; it needs a
  rigorous Lyapunov analysis of the coupled control+replicator system, and the constant `κ_s` is schematic.
- **Tracking floor (§1) is a linearized estimate** — the bias/variance form assumes small drift and a locally
  quadratic loss; large regime shifts need a different (change-detection) treatment.
- **Tâtonnement convergence is genuinely not general** — we inherit the classical disequilibrium pathologies,
  not solve them. Off-substitutes price discovery may simply not settle.
- **Coupling is treated loosely.** The three flows interact (beliefs change demand changes prices; prices
  change which goals pay changes selection). We have written them as separable; the genuine coupled system
  could have joint instabilities none of the parts show alone. A full treatment is a dynamical-systems project
  in its own right.
- **Goals as a fixed-dimensional covector** is a modeling choice; real goals can restructure (new channels
  appear), which no flow on a fixed simplex captures.

## 7. Closing — what the thesis now is, and what remains

With Thread C, the arc 00–05 is a complete **thermodynamics of value**:

- **Statics (01–04):** the measure (`V = Σ kᵢ ln eᵢ`), the capacity limit (`ΔG ≤ I(X;Y)`), the Second Law
  (`G = D(q‖r) − D(q‖p)`), cross-frame price, and the fleet ceiling (`Σ G_a ≤ H(X)`).
- **Dynamics (05):** the equations of motion — natural-gradient belief flow, dual-ascent price flow, and the
  control-plus-selection goal flow — plus a dynamical Second Law (a moving world forbids zero dissipation) and
  alignment recast as a stability condition.

The single most important structural finding is the **asymmetry of §0**: beliefs and prices have targets the
world supplies and can be driven to them; goals do not, and must be held in place against a selection pressure
that rewards whatever captures resource. *That is the mathematical shape of the alignment problem* — and it is
why a theory of value, not just a theory of information, is needed to govern a population of AI individuals.

**What remains** (beyond this thesis's core): the fully-coupled stability analysis (§6); the open *exact*
multi-agent capacity region ([`04`](04-multi-agent-capacity-region.md) §7); empirical instantiation — the
smallest simulated fleet in which measuring these dissipation channels and pricing against them measurably
beats ad-hoc coordination ([`00`](00-thesis-seed.md) §9.5). The theory is now complete enough to *build that
test*.

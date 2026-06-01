# The Coding Theorem of Value

> Thread A from [`01-core-formalization.md`](01-core-formalization.md) §8: push the Kelly connection to a
> growth-rate limit and obtain the closest thing to a Shannon **channel-capacity theorem** for value. The
> static log law of [`01`](01-core-formalization.md) gave one allocation result; this gives the *rate* law —
> how fast value can be created under uncertainty, and what hard ceiling bounds it.

## 1. The repeated value game (compounding regime)

In [`01`](01-core-formalization.md) the budget `E` was fixed. Here it **compounds**: value realized this
round becomes resource next round (an agent that achieves its goal earns more compute, trust, or budget). This
is the regime that matters for a long-lived agent.

Each round `t`:

- the world settles into a state `s ∈ S` (the goal-relevant situation), drawn `s ∼ q` (the *true* law);
- the agent splits its budget into fractions `b = (b₁,…,bₙ)`, `bᵢ ≥ 0`, `Σ bᵢ = 1`, across `n` channels;
- channel `i` returns a multiplier `oᵢ(s) ≥ 0` per unit committed when the world is in state `s`
  (goal-progress per unit resource); resource on a channel that does not pay is dissipated.

Budget update: `E_{t+1} = E_t · Σᵢ bᵢ oᵢ(s_t)`. Hence

$$\log E_T = \log E_0 + \sum_{t} \log\!\Big(\sum_i b_i\, o_i(s_t)\Big),$$

and the long-run **value growth rate** (per round) is

$$\boxed{\,G(b) = \mathbb{E}_{s\sim q}\Big[\log \sum_i b_i\, o_i(s)\Big].\,}$$

`G(b)` is concave in `b` (log of a linear form), so maximizing it is a well-posed convex program — the
**value-Kelly** allocation `b* = argmax G(b)`.

### Why the log is forced *again*

[`01`](01-core-formalization.md) derived the log from diminishing marginal value (axiom A3). Here the log
reappears from a *different* premise: the time-average growth rate of a **multiplicative** process is the
expected log of its multiplier (Peters, ergodicity economics — the log is the time-average, not a utility
quirk). The logarithm of value is therefore **over-determined** — two independent routes, psychology and
dynamics, force the same form. Over-determination is exactly the robustness signature of a fundamental
quantity.

## 2. Value growth = informational advantage

Take the canonical "horse-race" structure (Kelly's fair-odds case): the states are the channels (`n = |S|`),
committing to channel `i` pays only if state `i` occurs, and returns are set against a **reference belief**
`r` over states: `oᵢ = 1/rᵢ`. (`r` is the market / prior / baseline expectation.) Then

$$G(b) = \sum_s q_s \log\frac{b_s}{r_s}.$$

Maximizing over the simplex (Gibbs' inequality): the optimum is **to commit proportional to your model of the
world**, `b_s = p_s`, where `p` is the agent's belief about `q`. With a *correct* model (`p = q`):

$$\boxed{\,G^{*} = \sum_s q_s \log\frac{q_s}{r_s} = D(q\,\|\,r).\,}$$

**Maximal value growth equals the KL divergence of the agent's (correct) model from the baseline.** An agent
whose model is the baseline (`p = r`) grows value at rate **zero**. *Value creation is informational edge over
the prevailing expectation* — nothing more, nothing less. This is the precise form of
[`00`](00-thesis-seed.md) §5's "value created by gradients": the gradient is `D(q\|r)`.

## 3. The capacity theorem — value-throughput ≤ information-throughput

Now equip the agent with a **perception channel**: a signal `Y`, correlated with the world-state `X`, that it
observes before allocating. Optimal play is Bayesian — bet the posterior, `b_s = p(s \mid y)`. The growth rate
*with* perception:

$$G_Y = \sum_{x,y} p(x,y)\,\log\frac{p(x\mid y)}{r(x)}.$$

The **gain** over acting on the prior alone (`G_0 = D(p_X \| r)`):

$$\boxed{\,\Delta G = G_Y - G_0 = \sum_{x,y} p(x,y)\,\log\frac{p(x\mid y)}{p(x)} = I(X;Y).\,}$$

> **Coding Theorem of Value.** The incremental rate at which an agent can compound value, by perceiving the
> world through a channel `Y`, is at most the mutual information `I(X;Y)` between the world-state and the
> perception — and this bound is **achieved** by Bayes-optimal proportional allocation.

It has the full structure of a Shannon coding theorem:

- **Achievability.** Betting the posterior `b_s = p(s\mid y)` attains `ΔG = I(X;Y)`.
- **Converse.** No allocation does better: any `b ≠ p(\cdot\mid y)` loses exactly `D(p(\cdot\mid y)\,\|\,b)`
  per round (Gibbs), so `I(X;Y)` is an upper bound.

The slogan from [`00`](00-thesis-seed.md) §5 is now a theorem: **an agent cannot create value faster than it
can perceive the world. Value-throughput is bounded by information-throughput.** Perception capacity is the
hard ceiling on value-generation rate — the value analog of channel capacity `C`.

## 4. The Second Law of Value, made exact

Drop the assumption that the agent's model is correct. Let `q` be reality, `p` the agent's model, `r` the
baseline. The agent bets `b_s = p_s` but the world is drawn from `q`. Then

$$G_{\text{actual}} = \sum_s q_s \log\frac{p_s}{r_s}
   = \underbrace{D(q\,\|\,r)}_{\text{available potential}} \;-\; \underbrace{D(q\,\|\,p)}_{\text{dissipation: model error}}.$$

Read it term by term:

- **`D(q‖r)`** — the value a *perfectly-informed* agent could extract (the exergy of the situation; the gap
  between reality and the baseline).
- **`−D(q‖p)`** — value **dissipated** by the agent's misalignment with reality. Zero iff `p = q`.

This is [`00`](00-thesis-seed.md) §4's **Second Law of Value** made quantitative: *realized value = available
potential − dissipation from model error*, every term in nats. Three consequences:

1. **Misalignment is measurable dissipation.** Confident error (`D(q‖p) > D(q‖r)`) drives growth **negative** —
   a wrong, certain agent actively destroys value. Calibrated humility is value-preserving.
2. **Learning is value-recovery.** `D(q‖p)` is exactly the cross-entropy excess that supervised/predictive
   training minimizes. So **the ML training objective IS the minimization of value dissipation.** Training an
   agent and conserving value are the same operation viewed from two fields.
3. **Alignment is a value law, not only an ethics norm.** Reducing `D(q‖p)` — making the agent's model match
   the world — is mechanically identical to reducing wasted value. This is the cleanest bridge yet from the
   thesis to AI alignment.

## 5. Consequences for governing AI individuals

- **Each agent's value-generation rate is capped by `I(X;Y_a)`** — the mutual information of *its* perception
  channel. A weak model with a noisy channel has low `I`, hence a low value ceiling, no matter its effort.
- **This is the formal reason the Macrokit pattern produces value.** A precompiled macro hands the agent the
  goal-relevant bits directly, raising effective `I(X;Y)` *per joule* of compute — it lifts value-throughput
  without raising the deliberation cost. "Move reasoning to design-time" = "raise the perception channel's
  mutual information cheaply." The coding theorem is *why* cheap reflexes can match expensive deliberation on
  narrow tasks: on a narrow task the macro's `I` can equal the strong model's at a fraction of the joules.
- **Fleet governance = waterfilling perception bandwidth.** Total growth `Σ_a G_a`; raise it by routing
  scarce perception/information to the agents where its marginal value (goal-stakes × leverage) is highest,
  and by driving every agent's `D(q‖p_a)` down (keep models calibrated). Both are now optimization targets
  with units, not slogans.

## 6. Boundary conditions — where the theorem's assumptions bite

In Shannon's spirit of naming what the model assumes:

- **Compounding is required.** The clean rate law needs value reinvested as resource (multiplicative dynamics).
  For one-shot, non-reinvested value, use the static law of [`01`](01-core-formalization.md) instead.
- **The KL form needs the horse-race structure.** General returns `oᵢ(s)` give a concave program with no
  closed form; `G* = D(q‖r)` is the clean special case (mutually-exclusive channels, fair returns). The
  *bound* `ΔG ≤ I(X;Y)` is more robust but tightest in this structure.
- **Stationarity / ergodicity.** Growth rates are long-run averages; under non-stationary `q` (drifting world)
  the time-average and ensemble-average diverge and the limit must be handled carefully.
- **No-leverage, no-ruin.** Betting fractions sum to ≤ 1 (no borrowed resource). Leverage reintroduces ruin
  risk that the log objective is precisely designed to avoid — but only without leverage.

## 7. What threads A has now closed and opened

**Closed:** the value analog of channel capacity exists and is proven — `ΔG ≤ I(X;Y)`, achievable, with a
converse. Value-throughput is bounded by information-throughput; misalignment is quantified dissipation;
learning is value-recovery. The thesis now has *two* hard theorems (the log law, the coding theorem) and a
quantitative Second Law.

**Open (next):**

- **Cross-frame transformation (the hard one).** Everything here is single-frame: one agent's `q, p, r, k`.
  Fleet-level value still needs the transformation law between two agents' goal-weight/belief bases and the
  invariant beyond `E`. Thread B.
- **Dynamics of the model `p` and goal-weights `k`.** §4 says learning reduces `D(q‖p)`; a dynamical theory of
  *how fast* (a value-flavored learning-rate / regret bound) would connect this to online learning and give a
  transient law to sit beside the steady-state one. Thread C.
- **Multi-agent capacity region.** Shannon has a multi-user capacity *region* (broadcast, MAC). The value
  analog — the achievable region of joint growth rates for interacting agents sharing a world — is the
  natural unification of A and B, and the real prize for governance.

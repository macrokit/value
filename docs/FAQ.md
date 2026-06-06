# FAQ — common objections, answered honestly

Short answers to the questions readers ask first. The discipline here is the same as the rest of the
project: concede what is conceded, claim only what is earned. Each answer links to where the full treatment
lives.

---

## "What is value's nature — and is it value that *drives* a human or an AI agent to decide?"

**Value's nature: a relation, not a substance.** Strip the semantic clothing and value is the rate at which an
agent converts a scarce resource into progress toward a goal, relative to a frame the goal fixes. Three faces:
its **currency is substance** (free energy / exergy — what's spent), its **structure is information**
(organized by `H, D, I`), and its **frame is the goal** (what gives it direction). That is the precise sense of
"value sits between substance and information": *value is information given a direction by a goal, paid for in
substrate.* Remove the goal and there is no value — only energy and bits.

Three consequences, stated with the honesty the rest of this project uses:
- **It is relational, not fundamental.** Energy exists with no observer; information needs only a distribution;
  value needs an *agent with a goal*. It is a *derived*, frame-relative quantity — real and lawful (the same
  *type* of thing as information), **not** a newly-discovered fundamental substance.
- **It is not conserved.** Value is created by an agent aligned with its world and destroyed by miscalibration
  (the Second Law of value, [`02`](02-coding-theorem-of-value.md)). Non-conservation is part of its nature.
- **Its reference is agent-supplied** — the is/ought asymmetry ([`05`](05-dynamics.md) §0): the world pins a
  Hamiltonian (substance) and a source distribution (information), but it does *not* pin the goal.

**Does value drive decisions?** Only in two honest senses — not as a literal cause.
- *As a model — yes, almost tautologically:* any agent that chooses consistently can be *described* as
  maximizing something. But that is a lens we impose, not an engine we find — and you **cannot** uniquely
  recover an agent's value function from its behavior (Armstrong & Mindermann, 2018). There is no fact of the
  matter about *the one value* driving it.
- *For humans — no, not cleanly:* real decisions come from habit, emotion, social context, and conflicting,
  time-inconsistent drives. "Value" is a useful first-order story and an after-the-fact reconstruction, not the
  mechanism.
- *For today's AI — no, literally:* an LLM agent completes patterns shaped by training; it is not running a
  value function at decision time.
- *For engineered/future AI — this is the project's bet, and it is **prescriptive**, not descriptive:* *if* we
  build agents around explicit goal/value representations, *then* value is the right quantity to route, align,
  and govern them with.

So: **value does not drive decisions the way force drives motion (world-given, deterministic); it *organizes
and governs* them as a frame the agent — or its designer — supplies.** The reason is value's one distinctive
feature: its reference is unpinned. Because the goal is agent-supplied and not readable from behavior, value
can only be the *lens* that makes decisions legible and the *control quantity* used to steer agent populations —
which is exactly why this project's defensible contribution is a governance lens, not a discovered mechanism.

---

## "Isn't value just a price, or a number? Why do you need a mathematical theory at all?"

A price *is* a number — but it is value seen from **one frame: the market's**, not value itself. This is
exactly Shannon's situation in 1948: information looked like "just the message," already concrete, until he
showed the lawful quantity (bits) was hiding underneath the meaning. Price is the analogue of the message.

The theory's central distinction ([`03`](03-cross-frame-value.md)): **value is frame-relative** (it depends on
an agent's goal `k`); **price is frame-independent** (the one scalar all traders agree on at equilibrium, the
shadow price `λ = K/E`). Price is what value *collapses to* in a market — an emergent coordination signal, not
the underlying quantity.

So the math is necessary precisely where a price cannot reach:

- **Agents with no market.** An agent classifying intents or triaging tasks creates value but produces no
  price. The measure `ΔG` / `I(X;Y)` ([`02`](02-coding-theorem-of-value.md)) is defined from outputs and the
  world — no market required.
- **Limits, not points.** A price is one equilibrium number. The theory gives the *ceiling* on value an agent
  can generate (`ΔG ≤ I(X;Y)`), the *dissipation* it wastes (`D(q‖p)`), and the *fleet cap* (`Σ G_a ≤ H(X)`,
  [`04`](04-multi-agent-capacity-region.md)). A number can't carry laws; a theory can.

**Honest boundary:** the math is *not* necessary everywhere. For trading goods between humans in a market,
price already suffices and standard economics has it. And where a market exists, the cross-frame flow
predictions reduce to arbitrage / law-of-one-price / general equilibrium ([`15`](15-cross-frame-realdata.md)) —
there the equations add no edge. The theory earns its keep only where it tells you something a price cannot:
ceilings, dissipation, and the is/ought asymmetry ([`07`](07-alignment-stability.md)).

---

## "Can it estimate the price of things that don't currently have one?"

Yes for one meaning of "price," no for the other.

- **✅ Internal / shadow prices — yes.** For things with no market, the theory assigns a principled valuation
  *relative to a stated goal*: the shadow price of the budget `λ = K/E` ([`01`](01-core-formalization.md)), and
  the value-per-cost of each agent `I_a / cost_a` ([`04`](04-multi-agent-capacity-region.md)). This is exactly
  what the **value-meter** ([`tools/value-meter/`](../tools/value-meter/)) does: take agents with no prices,
  return a defensible price for each, and decide where to spend a budget. Pricing the unpriced *within a frame
  you choose* is a core use.
- **❌ External market price — no.** A market price is frame-independent *because the market makes it so* — it
  is the equilibrium of many frames plus supply, liquidity, and expectations. You cannot conjure it from one
  agent's value function; you need the actual market. And where the market exists, the theory reproduces
  general equilibrium and adds no pricing edge. For a genuinely unpriced external good, no frame-free "true
  price" even exists — interpersonal value comparison is provably non-canonical (Arrow).

**Precise statement:** it gives a *frame-relative valuation* and an *internal shadow price* for the unpriced —
useful for allocating resources inside agent systems — but it does not discover the objective external price,
which by definition only exists once a market produces it.

---

## "Can value be stored and transferred like money?"

The storable, transferable thing is **price and resource** — *not value itself*, and the difference is the
reason money exists.

Value in this theory is **exergy** (available useful work), not conserved energy ([`00`](00-thesis-seed.md)).
So unlike money it is:

1. **Not conserved — it dissipates.** The Second Law of Value: realized value = available potential −
   dissipation (`G = D(q‖r) − D(q‖p)`), and a moving world floors dissipation above zero
   ([`02`](02-coding-theorem-of-value.md), [`05`](05-dynamics.md)). Value leaks; a dollar doesn't.
2. **Frame-relative — no single magnitude to move.** The same item is worth different amounts to agents with
   different goals; there is no one number to transfer ([`03`](03-cross-frame-value.md)).
3. **Lossy to transfer.** Cross-frame transfer is friction-limited and never lossless: move `i→j` only when
   `V_j − V_i > f`, with `f > 0` ([`03`](03-cross-frame-value.md)).

**Money is the transferable shadow of value, not value itself.** Because value is frame-relative and lossy to
move, a frame-independent, conserved, storable token (money, or the shadow price `λ`) is invented to *stand in
for* value during exchange. The physics analogy is energy: you can store it in a battery and send it down a
wire, but the *useful* part (exergy) degrades on every store and round-trip. So you can store the **substrate**
(free energy, compute, a budget `E`) — but it is exergy, it dissipates, not a frozen stock; and you
**transfer via price**, because raw value cannot cross frames intact. This is why the theory coordinates agents
through a *price on shared resources* rather than by moving value between them.

---

## "Isn't this just generalized Kelly with new terminology?"

At the single-agent core, **yes — and the project concedes it up front** (README; `docs/related-work.md`). The
capacity theorem `ΔG ≤ I(X;Y)` and the fleet's Kelly-portfolio operating point are Kelly/Cover results re-read
for an arbitrary scarce resource. None of the underlying mechanisms is individually new.

What is added — and what Kelly does not cover — is their **unification under one substrate-grounded quantity**,
the **cross-frame / price layer** ([`03`](03-cross-frame-value.md)), the **fleet ceiling**
([`04`](04-multi-agent-capacity-region.md)), and the **is/ought asymmetry** — beliefs have a target the world
supplies, goals do not — from which alignment emerges as a control-stability condition
([`07`](07-alignment-stability.md)). The full prior-art comparison and contribution statement are in
[`docs/related-work.md`](related-work.md).

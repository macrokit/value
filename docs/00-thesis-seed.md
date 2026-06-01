# A Mathematical Theory of Value — Thesis Seed

> Working title. Deliberately echoes Shannon, *A Mathematical Theory of Communication* (1948).
> This is a private thinking document. Nothing here is settled; everything is a claim to be sharpened or killed.

## 0. The claim

Value is not merely a human verdict laid on top of the world. It is a **real, lawful quantity** — in the
same category as matter, energy, and information — in that it *measurably shapes how the physical world
evolves* (it determines where agents spend their scarce resources). It has been left undefined because, like
information before Shannon, it has been confused with its semantic clothing (morality, price, preference).
The task is to strip that clothing and find the structural quantity underneath.

The payoff we are aiming at: a quantity precise enough to **govern a population of separated AI individuals** —
to measure, route, transfer, and conserve-or-dissipate value across many agents.

## 1. The method we are copying from Shannon

Shannon did not define information. He defined a **measure** of it, after one ruthless abstraction:

> "The semantic aspects of communication are irrelevant to the engineering problem."

He threw away **meaning**. What remained — reduction of uncertainty over a set of possibilities — gave him:

| Shannon got | from |
|---|---|
| a measure: information content `−log p` | axioms (continuity, monotonicity, additivity over independent events) |
| a unit: the **bit** | the choice of log base 2 |
| a system model | source → encoder → **channel (+noise)** → decoder → destination |
| fundamental limits | channel capacity; source-coding & noisy-channel-coding theorems |

**Our analogous ruthless abstraction:** throw away **morality, price, and human psychology.** They are to
value what *meaning* was to information — the loaded semantic layer. What remains is structural.

## 2. The central tension — and why it is the breakthrough, not the bug

Objection: matter/energy/information are objective; value is agent-relative — a thing has value only *to
someone*. So value can't be fundamental.

Rebuttal: **information is relative too** — to a prior distribution. **Energy is relative** — to a reference
frame. Relativity does not disqualify a quantity from being fundamental; it forces the theory to make the
*frame* explicit.

> **A theory of value is to agency what relativity is to motion.**
> Value is frame-dependent on the agent's goal — but the laws relating value across frames are universal.

Value is therefore *not subjective (arbitrary)* but *frame-relative (lawful, measured from a stated origin:
the agent's goal)*. The thesis is, in large part, the search for the **transformation laws between
agent-frames** and the **invariant** all frames agree on.

## 3. The invariant and the unit

The anchor that makes value physical rather than arbitrary: **free energy (exergy)** — the universal scarce
resource any agent must spend to do work. Money, reward, and utility are proxies for *a claim on free energy
/ labor*.

- **Unit of value:** the agent's irreplaceable resource — joules, or its computational proxy (compute, time).
- **Definition (candidate):** `V(x | A)` = the quantity of free energy agent `A` would rationally spend to
  move the world toward state `x`. Frame-relative in *direction*; invariant in *substrate*.
- Price, utility, RL reward, willingness-to-pay are all **projections** of this onto various measuring sticks.

## 4. Value is exergy, not conserved energy (a correction to the first instinct)

Total energy is *conserved*. Value is **not**. Value behaves like **free energy / exergy**:

- it is **created** by gradients (positive-sum interactions), and
- it is **irreversibly destroyed** by dissipation — waste, conflict, misalignment, duplication.

**Second Law of Value (conjecture):** in a closed multi-agent system with no new gradients, realizable value
dissipates toward equilibrium unless work is spent to maintain it. (The "heat death of motivation.")

This law is the spine of the governance application: left alone, a fleet of agents *loses* value.

## 5. The channel/coding picture (the most load-bearing borrowed structure)

Map Shannon's communication system onto value production:

| Shannon | Value analog |
|---|---|
| message source | an agent's goal |
| channel | the agent's capacity to convert resources into goal-progress |
| **channel capacity** | **value throughput** — max rate an agent turns free energy into realized value |
| noise | misalignment, model error, environmental stochasticity (intended − realized value) |
| **source coding** (efficient codes) | **compiling a recurring value-producing workflow into a short policy** |
| optimal code / short codeword | a reusable, precompiled routine for a frequent value-flow |

This is where the theory becomes operational rather than poetic: governing many agents = a **rate–distortion
problem**. Produce the most realized value per joule, accepting bounded distortion (imperfect goal-attainment),
by encoding frequent value-flows into cheap channels.

## 6. Axioms (first sketch — to be made rigorous or discarded)

For value measure `V(· | A)` relative to agent `A` with goal `G`:

1. **Relativity.** Value is always `V(x | A)`; there is no frameless value. (cf. prior in information, frame in energy.)
2. **Ordering.** `V` induces a (partial) preference order over outcomes.
3. **Substrate grounding.** `V` is denominated in `A`'s scarce resource (free energy / compute / time); this is the cross-frame invariant.
4. **Composition.** Value of combined outcomes composes under a defined operation (likely sub-additive — diminishing returns — not simple sum).
5. **Transfer with dissipation.** Value can be transferred between agents, but transfer incurs friction (a non-negative loss); never lossless. (Distinguishes value from conserved quantities.)
6. **Creation by gradient.** Value can be created where agent-frames are *complementary* (positive-sum); destroyed where they conflict.

## 7. Application — governing separated AI individuals

- An AI individual = **an agent-frame** carrying its own value field (its goal).
- Coordination = **aligning frames** so their value-gradients compose rather than cancel.
- Value as transferable token ⇒ agents **trade work**; measure each one's *marginal contribution* to a shared objective (Shapley-style value accounting).
- **Value throughput** per agent ⇒ route each unit of value-production to the cheapest agent that can carry it (rate–distortion routing).
- **Second Law of Value** names the no-supervision failure mode: drift, duplication, conflict ⇒ value dissipates. Governance = supply gradients + cut dissipative friction.

## 8. Honest objections / where the analogy breaks

- **No clean noiseless reference.** Shannon's source has a well-defined alphabet and distribution. An agent's
  goal is often ill-specified and changes over time — the "source" is non-stationary. This is the hardest gap.
- **Inter-frame comparison is unsolved.** Energy in different frames relates by clean transformations; we do
  not yet have the "Lorentz transformation" for value across two agents with incommensurable goals. Without it,
  cross-agent value accounting may be only ordinal, not cardinal.
- **Measurement.** Information is measurable because probabilities are estimable. Estimating `V` requires
  estimating an agent's goal and its resource-spend counterfactually — much harder to observe.
- **Risk of circularity.** "Value = what an agent spends resources to get" can collapse into revealed
  preference (tautology). The theory earns its keep only if it *predicts* spend, sets *limits*, or yields
  *conservation/dissipation laws* that revealed preference cannot.

## 9. Open questions (the research program)

1. State the value measure axiomatically (à la Shannon's Appendix 2) and prove what functional form they force.
2. Is there a value analog of the **coding theorems** — a provable bound on value-per-joule for a given agent capacity?
3. Formalize the **Second Law of Value**: what is the entropy-analog whose increase = value dissipation?
4. Find the **cross-frame invariant** rigorously. Is free energy enough, or is a richer invariant needed?
5. Build the smallest **toy multi-agent system** where value-accounting measurably outperforms ad-hoc coordination.

---

*Next:* pick one thread from §9 and go deep. The likeliest first win is §1–§3 formalized into a single
clean definition + one provable limit — the minimal "Shannon Section 1" of value.

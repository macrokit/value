# The Wave / Field Theory of Value — results

> **Standalone summary of the speculative frontier thread.** A population of
> goal-directed agents admits a *statistical field theory* — value as a field, demand
> as a wave, alignment as a phase transition — the way flocks, fluids, and spins do.
> This folder collects the result of asking, with the project's honesty rule, whether
> that is **real physics or a seductive analogy.**
>
> **Status (2026-06-02): honest-positive, conditional.** The field equations now
> *derive* from the agent dynamics, and both signatures *emerge* from a toy agent
> economy. What remains unproven is the one thing that would make it science rather
> than internal consistency: a measurement on a **real** agent population or market.
> Until then this is suggestive + derived, **not** validated — and it stays out of the
> core preprint (Zenodo concept DOI 10.5281/zenodo.20487041; latest published record v3).
>
> Canonical sources (this is a digest of them):
> [`docs/08-field-theory-of-value.md`](../docs/08-field-theory-of-value.md) (construction),
> [`docs/10-field-theory-derivation.md`](../docs/10-field-theory-derivation.md) (derivation, Thrust A),
> [`sim/field/dynamic/`](../sim/field/dynamic/) (emergent simulation, Thrust B).

---

## 0. First, the question everyone asks: which is the wave, and which is the field?

"Field" and "wave" are not two names for one thing. **Field** is the *category* — a
quantity defined continuously over the population. **Wave** is a *behavior* — what a
disturbance does when it propagates at finite speed. So:

| object | role | what it is |
|---|---|---|
| **demand** (desire `ρ`) | source + carrier of the disturbance | a demand shock **is the wave** |
| **price** `π` | the medium | the field the demand-wave travels *through* |
| **value** `v` | extracted density | a field — but the *dissipated* one, not what waves |
| **goals** `n` | order parameter | the *other* field — its alignment **phase-transitions**, it doesn't wave |

**One-liner:** *value is a field; demand is what waves across it; the collective goal
is what freezes (phase-transitions) within it.* The owner's intuition "value is an
intelligence wave" is the poetic version; the rigorous version is "**demand** is the
wave, **price** is the medium, **value** is the field-density the passing wave
realizes." That refinement is a sharpening, not a contradiction.

There are really **two sectors**, and each contributes one phenomenon:

1. **Economic sector** (resource–price–demand) → the **wave** (telegrapher).
2. **Goal sector** (the director field `n`) → the **phase transition** (flocking).
   It has slow waves too — the Goldstone modes (§3) — but its headline is ordering.

---

## 1. Thrust A — the field equations DERIVE (not posited)

The earlier construction (doc 08) wrote the telegrapher and Toner–Tu equations down
*by analogy* with active matter, and admitted every coupling constant was a free
parameter. Coarse-graining the discrete value dynamics
([`docs/04`](../docs/04-multi-agent-capacity-region.md),
[`docs/05`](../docs/05-dynamics.md)) shows both forms actually **fall out** of the
agent rules — Maxwell, not metaphor (full work in
[`docs/10`](../docs/10-field-theory-derivation.md)).

### 1a. The demand wave (telegrapher equation)

Two conservation-grade facts — substrate conservation `∂ₜe + ∇·Jₑ = 0` and a local
price–resource response `δe = C δπ` — plus **one** constitutive choice for the
resource current decide everything:

- **instantaneous** reallocation (`Jₑ = −σ∇π`) ⇒ pure **diffusion**, no wave;
- **relaxational** reallocation (the current eases toward its target over a finite
  time — Maxwell–Cattaneo / transmission-line) ⇒ the **telegrapher equation**.

The two coupled first-order relations (price ↔ resource current, like voltage ↔
current on a transmission line) combine to

$$\frac{L}{R}\,\partial_t^2\pi + \partial_t\pi = \frac{1}{RC}\,\nabla^2\pi,
\qquad \tau=\frac{L}{R},\;\; D=\frac{1}{RC},\;\; v=\frac{1}{\sqrt{LC}}.$$

So doc 08's three free constants become three **agent-economic** quantities:

| field constant | = agent quantity | meaning |
|---|---|---|
| storage elasticity `C` | `∂e/∂π` | resource held per unit price (inventory/supply response) |
| dissipative resistance `R` | `~ 1/κ` | value-leak per unit flow (disequilibrium dissipation) |
| reallocation inertia `L` | `~ 1/η` | how sluggishly budget is redirected |

and the **crossover** (the central falsifiable prediction) is
`q* = 1/(2√(Dτ)) = ½√(RC)`: short-scale demand shocks propagate as waves, society-wide
ones diffuse.

> **The condition that decides it: `L > 0`.** The wave exists *iff* resource
> reallocation carries inertia. If agents reallocate instantly, `τ→0`, `v→∞`, and the
> theory predicts only diffusion. This replaces a *posit* with a *measurable
> condition*.

### 1b. The collective goal (Toner–Tu) + control = a mass

The goal update — agents imitating the goals of **resource-capturing** neighbours
(replicator-weighted), under control toward a principal goal and idiosyncratic noise —
**is a Vicsek alignment interaction**. Its continuum limit is therefore Toner–Tu by
the established Bertin–Droz–Grégoire route, with

$$\Gamma \propto J_{\text{align}}\,\rho\,r^2 \quad(\text{imitation rate}\times\text{density}\times\text{range}^2),
\qquad J \propto J_{\text{align}}\,\rho \;(\text{Frank stiffness}).$$

The control term coarse-grains to an external field on the director — formally a
**symmetry-breaking mass** `m² ∝ γ`. This *derives* doc 08 §6's is/ought claim:

> **Goals are Goldstone (massless) only when uncontrolled (γ=0). Alignment design is
> literally the addition of a mass term.** Beliefs are pinned by reality (an exogenous
> mass); goals have no world-given field, so absent control they are exactly soft.

### 1c. The honest ledger

**Derives:** the telegrapher form (τ,D,v from C,R,L); the Toner–Tu form (Γ,J,β from
imitation/density/range/replicator); control = mass. **Stays assumed (now explicit and
falsifiable):** reallocation inertia `L>0` (else the wave is pure diffusion);
**local, rotationally-symmetric, motile** imitation (else the gradient expansion /
spontaneous ordering fails); the linear truncation (full nonlinear Toner–Tu needs the
complete Boltzmann–Ginzburg–Landau machinery). The honest gap **moved** — from "are
these the right equations?" to "do real agent networks meet these conditions?"

---

## 2. Thrust B — both signatures EMERGE in a toy value economy (7/7)

[`sim/field/dynamic/`](../sim/field/dynamic/) runs **microscopic agents only** — each
with a local rule referencing its neighbours. **No telegrapher or Toner–Tu equation is
integrated anywhere.** The question is whether the macroscopic field shows the
predicted behaviour as an *emergent* property. It does.
(Run: `python3 sim/field/dynamic/run_all.py`.)

### 2a. Demand wave — `RingEconomy`, 4/4 PASS

Agents ship resource toward value (up the price gradient) but adjust their outflow
toward the desired rate only *partway each step* — a finite flow lag `τ_J` (the
microscopic realization of reallocation inertia `L`). Resource is exactly conserved.

| check | prediction | measured | verdict |
|---|---|---|---|
| **W1a** wave regime | shock **peak propagates** ∝ t at √(D/τ) | peak speed 2.46 (pred 2.50), travels 30 sites | **PASS** |
| **W1b** diffusion regime | peak **pinned**, bulk σ² ∝ t | peak travels 0 sites; σ²∝t R²=1.00 | **PASS** |
| **W2** speed scaling | v ∝ 1/√τ_J | ratio const to ~9% across τ_J ∈ {4,8,16,32} | **PASS** |
| **W3** dispersion crossover | q* ≈ 1/(2√(Dτ)) | emergent q*≈0.031 vs pred 0.025 (within 26%) | **PASS** |

The wave–diffusion split is exactly the inertia condition of §1a: with a flow lag the
disturbance *propagates*; without it, it *spreads in place*.

### 2b. Collective-goal transition — `FlockEconomy`, 3/3 PASS

Motile agents imitate resource-weighted neighbour goals; resource follows a replicator
payoff (alignment is a positive-sum dividend), so the imitation weights **evolve** —
this is a value economy, not plain Vicsek.

| check | prediction | measured | verdict |
|---|---|---|---|
| **C1** order→disorder | m collapses as noise η rises | m: 0.73 → 0.05 across the η sweep | **PASS** |
| **C2** susceptibility peak | χ peaks at η_c (continuous transition) | χ_peak = 17.0 at η_c ≈ 0.15, vs ends 3.9 / 0.3 | **PASS** |
| **C3** control = mass | γ>0 rounds the transition | m(high η): 0.05→0.17; χ_peak: 17.0→0.43 | **PASS** |

**Two sub-findings that confirm Thrust A's conditions:**

- **Motility is necessary.** On a *fixed* lattice the goal field is a 2D XY model with
  scalar noise — Mermin–Wagner forbids ordering, and we observed exactly that (no order
  at any noise). Spontaneous collective goals require agents that *move* (Toner–Tu's
  mechanism). This is itself a finding, and it sharpens doc 08 §5.
- **Control is measurably a mass.** Turning on `γ` rounds the transition — the
  simulated signature of the §6 mass term — confirming §1b from the micro-rules up.

---

## 3. What it adds up to, and what it does not

**Two independent routes — analytic coarse-graining (A) and microscopic simulation
(B) — reach the same field equations.** The telegrapher wave and the Toner–Tu
transition are the continuum limit of an agent value-economy, with coupling constants
that are functions of agent-level quantities, under explicit conditions (inertia;
motile, local, symmetric imitation) that are themselves confirmed as *necessary* by
the simulation.

**What is NOT yet earned** (doc 08 §9): any of this on **real** agents. Both routes are
internal — the simulation is toy agents, the derivation is on paper. The decisive,
still-open gate is a **measured dispersion crossover or flocking transition in a real
agent population or market**. A standalone speculative preprint (byline Cheng Qian) is
earnable only *after* such a real-data signature exists — not before.

**The prize, if it survives the real-data test** (doc 08 §8): a **phase diagram of
collective intelligence** — regimes of coherent shared purpose vs incoherent drift,
mapped against alignment coupling, noise, and resource coupling, with measurable
transitions. That is what "study intelligence as physics" would concretely mean: an
order parameter and a phase diagram you can measure.

---

## 4. Map of the thread

| rung | artifact | status |
|---|---|---|
| belief: "value is an intelligence wave" | — | ✅ |
| formal construction | [`docs/08`](../docs/08-field-theory-of-value.md) | ✅ |
| continuum has the phenomenology (PDEs integrated) | [`sim/field/field_experiments.py`](../sim/field/field_experiments.py) | ✅ 5/5 |
| order-parameter foundations on real agents (static) | [`sim/field/v2_geometry.py`](../sim/field/v2_geometry.py) | ✅ |
| **A: field equations DERIVE** | [`docs/10`](../docs/10-field-theory-derivation.md) | ✅ |
| **B: signatures EMERGE in a toy economy** | [`sim/field/dynamic/`](../sim/field/dynamic/) | ✅ 7/7 |
| **real-data test** (the one gate left) | — | ⏳ open |

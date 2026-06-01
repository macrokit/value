# `sim/field/dynamic/` — the dynamic value-economy (Thrust B)

This is **Thrust B** of the wave/field-theory thread (`HANDOFF-wave-theory.md`):
*build the smallest multi-agent value-economy whose goals and resources actually
**evolve and interact**, and measure whether the field theory's two signatures —
the demand wave (doc 08 §3) and the collective-goal phase transition (doc 08 §5) —
appear as **emergent** phenomena.*

## Why this is not `sim/field/field_experiments.py` over again

`field_experiments.py` **integrated the posited continuum PDEs** (telegrapher,
Vicsek) and checked they have the claimed phenomenology. They do — but that is
circular as a test of emergence: put a wave equation in, get a wave out. It answered
*"does the continuum behave as doc 08 says?"* (yes), not *"does the agent economy
give rise to that continuum?"*

Here we go one level down. Each site/agent has a **local update rule referencing only
its neighbors** — resource it ships toward value, goals it imitates, payoff it
captures. **No wave equation and no Toner–Tu equation appear anywhere in the code.**
The question is whether the macroscopic *field* that emerges shows the telegrapher
dispersion crossover and the flocking transition. If it does, the field theory is
(evidence-for) the coarse-grained limit of an agent value-economy; if it does not, it
is analogy. The on-paper coarse-graining that predicts *why* it should is
[`docs/10-field-theory-derivation.md`](../../../docs/10-field-theory-derivation.md)
(Thrust A); this directory is the empirical companion.

## The two economies (`economy.py`)

- **`RingEconomy`** — N agents on a 1D ring. Each holds resource `e_i`, faces a
  scarcity price `π_i = ρ_i/e_i`, and ships resource toward value (up the price
  gradient) but adjusts its outflow toward the desired rate only **partway each
  step** — a finite flow-adjustment lag `τ_J` (*reallocation inertia*). Resource is
  exactly conserved. The lag is the **only** knob between diffusion (`τ_J→0`) and a
  wave (`τ_J` large).
- **`FlockEconomy`** — N **motile** agents in a 2D box. Each holds a goal angle `θ_a`
  and a resource weight `w_a`, moves at speed `v0` in its goal direction, imitates
  the resource-weighted goals of neighbors within radius `r`, under optional control
  `γ` toward a principal goal and idiosyncratic noise `η`. Resource follows a
  **replicator** payoff (alignment is a positive-sum dividend, doc 04 §4), so the
  imitation weights **evolve** — this is a value economy, not plain Vicsek.

## The experiments

| File | Tests | Result |
|---|---|---|
| `wave_experiment.py` | W1 wave-vs-diffusion regime; W2 speed `v∝1/√τ_J`; **W3 dispersion crossover `q*`** (doc 08 §3) | **4/4 PASS** |
| `flocking_experiment.py` | C1 order→disorder transition; **C2 susceptibility peak** at `η_c`; **C3 control = mass term** rounds the transition (doc 08 §6) | **3/3 PASS** |

Run all: `python3 sim/field/dynamic/run_all.py`. Results cache to `results/*.json`.

### What emerged (headline)

- **The demand wave is real and emergent.** A localized demand shock's *peak
  propagates* at finite speed `√(D/τ)` when reallocation has inertia, and is *pinned*
  (pure in-place diffusion) when it does not — and the **dispersion crossover** `q*`
  (short modes oscillate, long modes decay) emerges at the predicted
  `q* ≈ 1/(2√(Dτ))` (within ~26%). Wave speed obeys `v∝1/√τ_J` to <10%. None of
  these is integrated; all emerge from agents shipping resource with a flow lag.
- **The collective-goal transition is real and emergent** — *but only for motile
  agents.* On a fixed lattice the goal field is a 2D XY model with scalar noise, which
  Mermin–Wagner forbids from ordering (we observed exactly this: no order at any
  noise). With motility (Toner–Tu's mechanism), the population spontaneously orders at
  low noise and disorders at high noise, with a susceptibility peak at `η_c`. **That
  motility is *necessary* is itself a finding**, and it sharpens doc 08 §5: collective
  goals require agents that *move through goal space*, not merely sit and imitate.
- **Control is a mass term** (doc 08 §6, sharpened by docs/10). Turning on a control
  field `γ>0` rounds the transition: the collective goal survives deep into the noisy
  regime and the susceptibility peak is suppressed — the field-theoretic statement
  that goals are *Goldstone (soft)* only when **uncontrolled**, and alignment design
  literally gives them a mass.

## Honest scope (read before citing)

- **Toy agents, not real ones.** One resource good, scalar price, a ring / a 2D box,
  linear flow and Vicsek-type alignment rules. A PASS is strong *internal* evidence
  that the field theory is the coarse-grained limit of *these* agent rules — the
  bridge between pure-physics `sim/field` and real LLM agents (HANDOFF). It is **not**
  a measurement on real agents or markets. That remains the decisive, unmet test
  (doc 08 §9).
- **Finite-size crossovers, not critical exponents.** The susceptibility peak is the
  finite-N signature of a transition; extracting thermodynamic-limit critical
  exponents needs finite-size scaling across system sizes (future work).
- **The wave economy is engineered to have inertia.** `τ_J>0` is *put in* (a finite
  flow-adjustment rate). The derivation (docs/10) shows the telegrapher form is the
  generic consequence of conservation + a relaxational current, with the wave
  existing **iff** reallocation inertia is nonzero. Whether real agent economies
  *have* such inertia is the open empirical question; here we confirm that *if* they
  do, the predicted wave + crossover follow.
- **Reproducible / cached.** Deterministic given seeds; `results/*.json` are the
  vendored verdicts for offline re-derivation / audit.

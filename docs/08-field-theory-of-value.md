# Toward a Field Theory of Value (speculative)

> The frontier extension of the thesis: take the *discrete* multi-agent theory ([`03`](03-cross-frame-value.md),
> [`04`](04-multi-agent-capacity-region.md), [`05`](05-dynamics.md)) to a **continuum**, so that value becomes
> a **field** over a population of agents, demand-shocks become **waves**, alignment becomes **interference**,
> and the spontaneous coordination of goals becomes a **phase transition**. The ambition is to *study
> intelligence the way we study physics* — as fields, symmetries, and collective phenomena.
>
> **Honesty first.** This is a research program, not a result. What is *rigorous* here is the borrowed
> physics — the equations below are standard (telegrapher's equation, Frank elastic energy, Goldstone's
> theorem, Toner–Tu active hydrodynamics). What is *speculative* is the **mapping** of value/economics onto
> them. The whole document is a construction motivated by analogy plus one real anchor (active matter); §9 is
> blunt about what would make it science rather than physics-envy.

## 0. The one anchor that keeps this honest: active matter

There is already a mature physics of *many goal-directed agents that align with their neighbors*: **active
matter** — the Vicsek model and its continuum limit, the **Toner–Tu equations**, which describe flocks, swarms,
and self-propelled particles as a hydrodynamic field theory with an orientational order parameter. Active
matter already has: an alignment order parameter, spontaneous symmetry breaking (the flocking transition),
density waves, dissipation, and dispersion relations. **A field theory of value is active matter plus an
economic sector** (resource + price), plus the is/ought source asymmetry of [`05`](05-dynamics.md). That
lineage is what makes "value is a wave" a physics statement rather than a metaphor — we are not inventing the
field theory of aligned agents; we are extending one that works.

## 1. From agents to fields

Replace the discrete agent index `a` with a continuous position `x` in a base space `M` (a social/network
space), evolving in time `t`. The discrete objects become fields:

| Discrete ([`03`](03-cross-frame-value.md)–[`05`](05-dynamics.md)) | Continuum field over `M` |
|---|---|
| goal covector `k_a` (the frame) | **goal-director field** `n(x,t)`, a unit vector — the *order parameter* |
| resource/budget `E_a` | **resource density** `e(x,t)` (the conserved substrate) |
| shadow price `λ_a=K_a/E_a` | **price field** `π(x,t)` — the carrier/potential |
| desire/demand | **desire density** `ρ(x,t)` — the source term |
| value `V_a=Σk_i\ln e_i` | **value density** `v(x,t)` — what is extracted, not conserved |

The order parameter is `n` (where goals point), exactly as in a flock or a nematic. Alignment between two
regions is `n(x)\cdot n(x')`; its sign is the constructive/destructive **interference** of desires.

## 2. Three structural inputs, read off the discrete theory

1. **Misalignment is gradient energy.** In [`03`](03-cross-frame-value.md), alignment `cos θ` set positive- vs
   negative-sum. In the field, that becomes the **Frank elastic energy** of the director field,
   `F_{\text{align}} = \tfrac{J}{2}\int_M |\nabla n|^2\,dx`. Smoothly aligned goals store no energy; gradients
   (disagreement between neighbors) store energy that can propagate or dissipate. *Misalignment is literally
   curvature in the goal field.*
2. **Price is the carrier.** In [`03`](03-cross-frame-value.md), resource flows down shadow-price gradients
   until `λ` equalizes (a thermodynamic equilibration). In the field, this is a transport law:
   resource current `J_e = -D\,\nabla\pi`. Price is the potential whose gradients move the substrate.
3. **Value is exergy, so the theory is dissipative.** The Second Law ([`02`](02-coding-theorem-of-value.md))
   says value is created and destroyed, not conserved. A field theory of value therefore *cannot* be a clean
   conservative (Hamiltonian) field theory — it is necessarily an **open / non-equilibrium / active** one, with
   a dissipation term. This is not a defect; it is the same reason active matter is non-equilibrium physics.

## 3. The wave equation, and where waves actually come from

Combine resource transport (`∂_t e = -\nabla\!\cdot J_e = D\nabla^2\pi`) with the market relation that price
responds to scarcity and demand, **with a response lag** `τ` (agents update beliefs/prices with delay —
[`05`](05-dynamics.md)). Expanding the lag to second order yields, for the demand/price disturbance `φ`, the
**telegrapher's equation**:

$$\boxed{\;\tau\,\partial_t^2 \varphi \;+\; \partial_t \varphi \;=\; v^2\,\nabla^2\varphi \;+\; \text{source}(\rho)\;,\qquad v=\sqrt{D/\tau}.\;}$$

This is exactly the "driven, dissipative wave" of the informal picture, now an equation with a name. Its
character depends on a single ratio:

- **Overdamped regime** (lag small, `\tau` → 0): reduces to the **diffusion** equation `∂_t φ = v^2τ\nabla^2φ`
  — demand-shocks spread and damp, no oscillation.
- **Underdamped regime** (lag large): genuine **waves** — demand-shocks propagate at speed `v=\sqrt{D/τ}` (a
  "speed of value") and oscillate as they damp.

**Dispersion relation** (`\varphi \sim e^{i(q\cdot x-\omega t)}`): `\tau\omega^2 + i\omega - v^2 q^2 = 0`, so
$$\omega(q) = \frac{-i \pm \sqrt{4\tau v^2 q^2 - 1}}{2\tau}.$$
There is a **crossover wavenumber** `q^\* = 1/(2v\sqrt{\tau})`: short-wavelength (local) demand-shocks
propagate as waves; long-wavelength (society-wide) ones diffuse and damp. *This is the central falsifiable
prediction — a real demand-propagation experiment on a network should show this crossover, or the field
picture is wrong.*

This is the formal content of "an individual's desire creates a wave in society": a localized source `\rho`
in the telegrapher's equation radiates a damped wave through the price field, at speed `\sqrt{D/\tau}`.

## 4. The order-parameter sector: alignment as collective dynamics

The goal-director field obeys active-matter (Toner–Tu-like) dynamics — relaxation toward local alignment plus
advection plus noise:

$$\partial_t n + (u\!\cdot\!\nabla)n = \Gamma\big(\nabla^2 n - (n\!\cdot\!\nabla^2 n)\,n\big) \;+\; \beta\,\Pi_n\nabla\pi \;+\; \boldsymbol\eta,$$

where `\Gamma` relaxes goals toward neighbors (the alignment coupling), `\beta\,\Pi_n\nabla\pi` re-aims goals
toward where value/price is high (agents chase value, projected orthogonal to `n` to keep `|n|=1`), and
`\boldsymbol\eta` is the noise of individual idiosyncrasy. This is the field version of "agents adjust their
goals under control + selection" ([`05`](05-dynamics.md) §3; [`07`](07-alignment-stability.md)).

## 5. The exciting prediction: collective goals are a phase transition

When the alignment coupling `\Gamma` beats the noise `\boldsymbol\eta`, the director field **spontaneously
orders**: a population of scattered desires condenses into a *coherent collective goal*. This is a genuine
**phase transition** — the flocking / order–disorder transition of active matter — and it is the field-theory
account of movements, manias, paradigm shifts, fashions, and bubbles: society *condensing* onto a shared
direction of value.

Two consequences carry real predictive content:
- **Criticality.** Near the transition, correlation lengths diverge and fluctuations become scale-free —
  predicting **power-law demand cascades** (virality, fat-tailed adoption) as a critical phenomenon, not an
  accident.
- **Hysteresis / metastability.** First-order versions predict that collective goals, once formed, resist
  dissolving (lock-in) — the value analog of supercooling.

## 6. The is/ought asymmetry as a mass spectrum (the deepest restatement)

[`05`](05-dynamics.md) §0 found that beliefs have a world-given target and goals do not. In field language this
is a statement about the **mass spectrum of the two fields**:

- The **belief field** is *explicitly pinned* to reality `q` — an external source acts as a symmetry-breaking
  field, i.e. a **mass term**. Beliefs are **massive**: pull them and they spring back to truth.
- The **goal field** has a continuous symmetry (rotations in goal space) that is *spontaneously* broken when
  the population aligns — with no external field pinning the direction. By **Goldstone's theorem**, the broken
  symmetry produces **gapless (massless) modes**: long-wavelength re-orientations of the collective goal that
  cost vanishing energy.

$$\boxed{\;\text{Beliefs are massive (pinned by reality). Goals are Goldstone (massless, free to swing).}\;}$$

The slow, society-wide **value-waves** we experience as cultural and ideological drift *are the Goldstone modes
of the goal field* — and they are soft precisely *because* goals have no world-given target. Hume's is/ought
gap becomes: the belief field has a mass, the goal field does not. This is the single most striking thing the
field picture buys, and it is a precise, structural claim.

## 7. What is conserved, and what is not

The truly conserved object is the **substrate** (resource/free energy): a continuity equation
`∂_t e + \nabla\!\cdot J_e = 0` in a closed system. **Value** is the part *extracted along goal-gradients* — a
source/sink term, created where `n` aligns with resource flow and dissipated where it does not. The Lagrangian
(action) formulation works only for the conservative sector; the dissipation (the Second Law) is
**non-Lagrangian** — it needs a Rayleigh dissipation function or an open-system (non-Hermitian) treatment.
*Restating: a field theory of value is irreducibly a theory of active, driven matter — there is no Hamiltonian
for it, and that is forced by the Second Law of Value, not a modeling shortcut.*

## 8. "Intelligence as physics" — what the program actually claims

Stated carefully, the claim is not that minds are literally fields, but that **populations of goal-directed
agents admit a statistical field theory** the same way populations of spins, molecules, or birds do. Its
observables are collective: order parameters (alignment), waves (demand propagation with a dispersion
relation), phase transitions (collective-goal formation), critical exponents (cascade statistics), and a
characteristic asymmetry (massive beliefs, massless goals). Intelligence-at-scale would then have a *phase
diagram* — regimes of coherent collective purpose vs. incoherent individual drift, with measurable transitions
between them. That is what it would mean to study intelligence as we study physics: not metaphor, but order
parameters and dispersion relations you can measure.

## 9. Where this breaks — the honest guard against physics-envy

The history of "physics of society" is littered with equations mapped onto social systems that did not obey
them. This program is worth nothing until it earns the analogy:

- **Locality and symmetry are assumed, not established.** Field theory needs local interactions and a real
  symmetry group. Social/agent networks are long-range, heterogeneous, and may have *no* clean symmetry — in
  which case the field reduction is invalid and only the discrete theory survives.
- **The mappings are constructions, not derivations.** The telegrapher's equation, Frank energy, and Toner–Tu
  dynamics are rigorous; *that value/price/desire obey them* is a hypothesis. Each coupling constant
  (`D, τ, J, Γ, β`) is presently a free parameter, not measured.
- **The decisive test is a measured dispersion relation or a measured transition.** The program becomes science
  the day someone measures, in a real agent population or market, either the §3 crossover `q^\*` (waves at
  short scale, diffusion at long scale) or the §5 flocking transition with its critical exponents. Absent that,
  this is a suggestive structure, explicitly labelled as such.
- **No empirical content yet.** Unlike [`06`](06-real-agent-test.md), nothing here has been tested. It is the
  *most* speculative document in the repository and should be read as the research frontier, not a claim.

## 10. Roadmap

This is the long-horizon extension, gated behind the nearer empirical work ([`06`](06-real-agent-test.md)
scale-up). The tractable first steps, in order:

1. ✅ **Simulate it — DONE** ([`sim/field/`](../sim/field/), 5/5). The lattice limit *does* have the claimed
   phenomenology: a demand-shock spreads ballistically (`σ²∝t²`, a wave) at large lag and diffusively (`σ²∝t`)
   at small lag, with wave speed obeying the telegrapher law `v∝1/√τ` to 1%; and a population of goal-directors
   undergoes the Vicsek order→disorder phase transition (`m`: 0.99→0.03). This clears the first gate — *does the
   continuum even have the phenomenology?* — yes. It is an internal-consistency check, **not** evidence about
   real agents (next steps remain).
1b. ✅ **First real-data touch — DONE** ([`sim/field/v2_geometry.py`](../sim/field/v2_geometry.py)). The
   field theory's *order-parameter assumption* holds on a real 10-agent population: across 3 domains, strong
   positive cross-agent alignment (correlation 0.32–0.51) and a dominant shared-competence axis (`λ₁/Σλ`
   0.41–0.51), **tens of σ above the independence null** (z = 32–51). Real agents have the low-dimensional
   alignment geometry the field assumes — and this *static* geometry explains the v1/v2 R5 result (the
   population is deep in the constructive-interference/aligned regime, so there is little anti-correlated
   diversity for pooling/pricing to harvest). **Scope: supports the foundations; NOT a test of the wave (§3)
   or the transition (§5)** — those need evolving goals, which static classification lacks.

2. **Pin the couplings** to the discrete theory by coarse-graining (derive `D, τ, J, Γ` from agent-level
   `E, λ, k`-dynamics rather than positing them).
3. **Find one real system** with measurable demand-propagation (a market microstructure, an information
   cascade on a network) and test for the dispersion crossover.
4. Only then: the analytic field theory (renormalization, the phase diagram, the critical exponents).

The prize, if it survives: a **phase diagram of collective intelligence** — and the field-theoretic statement
that *the soft modes of shared purpose exist because goals, unlike beliefs, answer to nothing outside
themselves.*

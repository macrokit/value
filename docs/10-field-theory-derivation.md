# Deriving the Field Theory from the Agent Dynamics (the coarse-graining)

> The decisive step for [`08`](08-field-theory-of-value.md). Doc 08 *posits* the
> telegrapher equation (demand wave, §3) and the Toner–Tu dynamics (goal alignment,
> §4–5) **by analogy** with active matter, and openly flags (§9) that "the mappings
> are constructions, not derivations" and that every coupling constant `D, τ, J, Γ, β`
> "is presently a free parameter, not measured." This document does the work doc 08
> §10.2 deferred: **coarse-grain the discrete value dynamics of
> [`04`](04-multi-agent-capacity-region.md)–[`05`](05-dynamics.md) into a continuum
> field theory and ask whether the telegrapher and Toner–Tu forms *fall out* — and if
> so, with what coefficients expressed in agent-level quantities.**
>
> **Honesty frame (the load-bearing rule of this thread).** The test is Maxwell vs
> metaphor: a derivation, not a re-decoration. The honest outcomes were (HANDOFF):
> (1) it derives → upgrade doc 08 from analogy to consequence; (2) it derives only
> under extra assumptions → say exactly which; (3) it does not derive → relabel doc 08
> as analogy and say so. **The finding is outcome (2): both forms derive, but each
> rests on one explicit, falsifiable structural assumption** — reallocation *inertia*
> for the wave, and *motile, locally-symmetric* goal imitation for the transition.
> Naming those assumptions precisely is the advance: doc 08's free parameters become
> functions of agent quantities, and its caveats become *conditions you can measure*.

## 1. What "derive" has to mean here

A field theory is *derived* from an agent model when a controlled coarse-graining
(continuum limit + gradient expansion) of the microscopic update rules yields the
field equations, with transport coefficients given as functions of microscopic
parameters — the standard set by **Bertin–Droz–Grégoire** (PRE 2006; J. Phys. A
2009), who obtained the Toner–Tu hydrodynamics for Vicsek with explicit coefficients
from a Boltzmann treatment. Anything weaker — "the equations look alike" — is analogy.

We coarse-grain the three discrete flows of [`05`](05-dynamics.md): price/tâtonnement
(§2 there), resource transport ([`04`](04-multi-agent-capacity-region.md) §3), and
goal control+replicator (§3 there). The substrate is conserved; value is not
([`02`](02-coding-theorem-of-value.md)) — so the result must be an open/active field
theory, never a Hamiltonian one (doc 08 §7). It is.

## 2. The resource–price sector ⇒ the telegrapher equation

### 2.1 Two conservation-grade facts, then one constitutive choice

Pass from the agent index `a` to a continuous coordinate `x` on the network. Two
fields survive the limit: the **resource density** `e(x,t)` (the conserved substrate)
and the **price** `π(x,t)` (its dual potential, [`03`](03-cross-frame-value.md) §5).
Two facts are not negotiable:

1. **Substrate conservation** (closed system, `Σ_a E_a` fixed):
   $$\partial_t e + \nabla\!\cdot J_e = 0.$$
2. **Local price–resource response.** Price is a function of local scarcity; to
   linear order about a uniform state, `δe = C\,δπ` with a **storage elasticity**
   `C ≡ \partial e/\partial π` (how much resource the population holds per unit price —
   an inventory/supply response). For the scarcity price `π=ρ/e` used in the
   simulation, `C = -e_0^2/\rho_0` in magnitude; sign conventions are fixed below so
   transport is stable.

The physics is entirely in the **third** ingredient — the constitutive law for the
current `J_e`. Two closures are possible, and they are the whole story:

- **Instantaneous (Darcy/Fick):** `J_e = -\sigma_c\,\nabla\pi`. Substituting gives
  `\partial_t e = \sigma_c\nabla^2\pi`, i.e. with the local closure a pure **diffusion
  equation**. No wave. This is doc 08 §3's overdamped regime — and it is what you get
  if resource reallocation is *instantaneous*.
- **Relaxational (Maxwell–Cattaneo):** the current does **not** snap to its Darcy
  value; it relaxes toward it over a finite time `τ_J`, because agents redirect budget
  with a delay (finite learning/adjustment rate, [`05`](05-dynamics.md) §1's tracking
  lag):
  $$\tau_J\,\partial_t J_e + J_e = -\sigma_c\,\nabla\pi.$$
  This single change — first studied by Cattaneo precisely to stop diffusion's
  unphysical infinite signal speed — turns the parabolic diffusion equation into a
  hyperbolic wave equation.

### 2.2 The telegrapher equation is the generic consequence (transmission-line route)

The cleanest derivation needs no slaving of `π` to `e`. Write the two conserved-grade
relations as two coupled first-order PDEs — exactly the **telegrapher's equations** of
a transmission line, with `π ↔` voltage and `J_e ↔` current:

$$C\,\partial_t \pi = -\nabla\!\cdot J_e ,\qquad\qquad L\,\partial_t J_e = -\nabla\pi - R\,J_e .$$

Reading the second equation as economics: the resource current is **driven** by price
gradients (`-\nabla\pi`), **damped** by a dissipative resistance `R` (the Second-Law
value-leak of out-of-equilibrium flow, [`05`](05-dynamics.md) §2; `R\sim1/\kappa`,
slow tâtonnement = high friction), and carries **inertia** `L` (the finite response
time of reallocation; `L=0` ⇒ the instantaneous Darcy law `J_e=-\nabla\pi/R`).
Eliminating `J_e` (take `\partial_t` of the first, substitute the second) gives, for
the price disturbance,

$$\boxed{\;\frac{L}{R}\,\partial_t^2 \pi \;+\; \partial_t \pi \;=\; \frac{1}{RC}\,\nabla^2\pi\;}$$

which is **exactly the telegrapher equation of doc 08 §3**, `τ\,\partial_t^2\varphi +
\partial_t\varphi = D\,\nabla^2\varphi`, under the identification

$$\boxed{\;\tau = \frac{L}{R},\qquad D = \frac{1}{RC},\qquad v = \sqrt{\frac{D}{\tau}} = \frac{1}{\sqrt{LC}}.\;}$$

So doc 08's three free constants are **not independent posits**. They are three
agent-economic quantities:

| Field constant | = agent-economic quantity | meaning |
|---|---|---|
| storage elasticity `C` | `\partial e/\partial\pi` | resource held per unit price (inventory/supply response) |
| dissipative resistance `R` | `\sim 1/\kappa` (tâtonnement rate) | value-leak per unit flow (disequilibrium dissipation, doc 05 §2) |
| reallocation inertia `L` | `\propto` agent response time (`\sim 1/\eta`, doc 05 §1) | how sluggishly budget is redirected |

and the **speed of value** `v = 1/\sqrt{LC}` is the transmission-line speed — fast when
reallocation is light (`L` small) and inventories are thin (`C` small).

The same result follows from the Maxwell–Cattaneo closure (§2.1) with `τ=τ_J`,
`D=σ_c/C`; the transmission-line route is preferred only because it assumes less.

### 2.3 The crossover, and the one condition the wave needs

Doc 08 §3's dispersion relation `τ\omega^2 + i\omega - Dq^2 = 0` and its **crossover
wavenumber** now read, in agent terms,

$$q^\* = \frac{1}{2\sqrt{D\tau}} = \frac{1}{2}\sqrt{RC}\,,\qquad \ell^\* = \frac{1}{q^\*} = \frac{2}{\sqrt{RC}}.$$

Short-wavelength (local) demand shocks propagate as damped waves; long-wavelength
(society-wide) shocks diffuse — exactly doc 08's central falsifiable prediction, now
with `q^\*` a function of the dissipation and storage of the economy.

**The load-bearing condition is `L>0`.** If reallocation is inertia-free (`L→0`),
then `τ→0`, `v→∞`, and the telegrapher equation collapses to pure diffusion: *no
wave.* Thus "demand is a wave" is **not** unconditional — it holds **iff resource
reallocation carries inertia**. This replaces doc 08's *posited* `τ` with a *derived,
measurable condition*: find one agent economy with a finite reallocation response
time and the wave (with its crossover) must be there; show reallocation is effectively
instantaneous and the field theory itself predicts only diffusion. That is a sharper,
more honest claim than doc 08 made.

## 3. The goal sector ⇒ Toner–Tu (and control = a mass term)

### 3.1 The discrete goal update is a Vicsek alignment interaction

[`05`](05-dynamics.md) §3 gives the goal director `k_a` (unit vector; angle `θ_a`)
two forces: **control** toward a principal frame `k^\*` (gain `γ`), and
**replicator selection** — resource-capturing agents' goals spread
(`\dot w_a = w_a(G_a-\bar G)`). Make "spread" concrete as local, resource-weighted
**imitation** (an agent re-aims toward the goals of high-resource neighbors), add
idiosyncratic noise `η`, and the microscopic update is

$$\theta_a \leftarrow \arg\Big(\underbrace{\textstyle\sum_{b\sim a} w_b\,e^{i\theta_b}}_{\text{replicator-weighted imitation}} \;+\; \underbrace{\gamma\,e^{i\theta^\*}}_{\text{control}}\Big) \;+\; \eta\,\xi_a .$$

The imitation term **is a Vicsek alignment interaction** — neighbours pull a director
toward their (resource-weighted) mean orientation. That is the exact microscopic
input Bertin–Droz–Grégoire coarse-grain. So the goal sector is not *like* active
matter; under local imitation it *is* an active-matter alignment model, and its
continuum limit is obtained by the established route — no new physics required.

### 3.2 What the coarse-graining yields

Coarse-graining the director field `n(x,t)=(\cos\theta,\sin\theta)` (Vicsek →
Boltzmann–Ginzburg–Landau → Toner–Tu) returns precisely doc 08 §4's equation, with
the coefficients now read off the agent rules:

- **Alignment relaxation `Γ`** (the `Γ\nabla^2 n` Frank-elastic term): from the
  discrete imitation Laplacian, `Γ \propto J_{\text{align}}\,\rho\,r^2` — imitation
  rate × local density × interaction range². The **Frank stiffness** `J` of doc 08 §2
  (`F_{\text{align}}=\tfrac{J}{2}\!\int|\nabla n|^2`) is `J\propto J_{\text{align}}\rho`:
  misalignment-as-curvature, with a stiffness set by how strongly and densely agents
  copy.
- **Value-chasing `β`** (the `β\,\Pi_n\nabla\pi` term, goals re-aim toward high
  price): from the replicator sensitivity `\partial G/\partial\pi` — how strongly
  resource-capture (hence goal weight) responds to price. The coupling to §2's
  price field is the replicator, made continuum.
- **Noise temperature**: the idiosyncrasy variance `η`, which sets the order–disorder
  (flocking) transition of doc 08 §5.

### 3.3 Control is a symmetry-breaking mass — sharpening the is/ought claim (doc 08 §6)

The control term `\gamma\,e^{i\theta^\*}` coarse-grains to an **external field**
`h=\gamma\,n^\*` acting on the director — formally a **symmetry-breaking mass** in the
Ginzburg–Landau free energy `\tfrac12 m^2\,|n-n^\*|^2` with `m^2\propto\gamma`. This
*derives and sharpens* doc 08 §6's "beliefs massive, goals Goldstone":

$$\boxed{\;\text{Goals are Goldstone (massless) }only\text{ when uncontrolled }(\gamma=0).\ \text{Alignment design is literally a mass term }m^2\propto\gamma.\;}$$

Beliefs are pinned by reality (an *exogenous* field — a mass set by the world,
[`05`](05-dynamics.md) §0). Goals have **no** world-given field, so absent control
they are exactly Goldstone — soft, free to drift (the cultural value-waves of doc 08
§6). Control supplies the missing field by hand; that is *why* alignment is upkeep
(doc 05 §4) and *why* an uncontrolled population's collective goal is set by what pays.
The mass spectrum is not decoration — it is the field-theoretic statement of the
is/ought gap, and the coarse-graining produces it.

## 4. The honest ledger — what derives, what stays assumed

**Derives (form + coefficient map):**
- The **telegrapher equation** is the generic continuum limit of substrate
  conservation + a relaxational resource current; `τ,D,v` are functions of `C,R,L`
  (§2.2). Not a posit.
- The **Toner–Tu / Frank-elastic** goal dynamics follow from local replicator-weighted
  imitation by the Bertin–Droz–Grégoire route; `Γ,J,β` are functions of imitation
  rate, density, range, and replicator sensitivity (§3.2). Not a posit.
- **Control = mass** is derived, not assumed, and it grounds the §6 mass spectrum
  (§3.3).

**Stays assumed (the conditions, now explicit and falsifiable):**
- **Inertia `L>0`** for the wave. With instantaneous reallocation the theory predicts
  *only* diffusion. (Falsifiable: measure the reallocation response time.)
- **Motility / locality / approximate rotational symmetry** for the transition. The
  Vicsek→Toner–Tu route assumes *local* imitation and a rotational symmetry in goal
  space (broken by control). Real agent networks may be **long-range** and
  **asymmetric**, in which case the gradient expansion is invalid and only the
  discrete theory ([`04`](04-multi-agent-capacity-region.md)–[`05`](05-dynamics.md))
  survives — doc 08 §9's standing caveat, here pinned to the exact assumption that
  would break. Empirically, spontaneous ordering further **requires motility**
  (Mermin–Wagner forbids it on a fixed lattice — see §5).
- **Linear/Ginzburg–Landau truncation.** We obtain the linear (telegrapher,
  Frank-elastic) forms cleanly; the full nonlinear Toner–Tu structure (the `|n|^2`
  pressure, the convective `λ(n\!\cdot\!\nabla)n`) needs the complete
  Boltzmann–Ginzburg–Landau machinery, which we cite (BDG) but do not carry through.
- **The interesting regime is not guaranteed.** The derivation fixes the *form* and
  the *parameter map*, not which regime a given economy sits in (wave vs diffusion,
  ordered vs disordered). That is set by the agent-level numbers, and is the empirical
  question.

## 5. Empirical companion: the emergent signatures (Thrust B)

The coarse-graining is on paper; [`sim/field/dynamic/`](../sim/field/dynamic/) is its
empirical check. There, **toy agents with only the microscopic rules above** (resource
shipped toward value with a flow lag; goals imitating resource-capturing neighbours)
were run, and the macroscopic field measured — *no telegrapher or Toner–Tu equation is
integrated anywhere*. The derived predictions appeared as **emergent** phenomena:

- **Demand wave (W1–W3, 4/4).** A demand shock's peak *propagates* at `√(D/τ)` when
  reallocation has inertia and is *pinned* (pure diffusion) when it does not; the
  speed scales `v∝1/√τ_J` (<10%); and the **dispersion crossover** emerges at the
  predicted `q^\*≈1/(2\sqrt{D\tau})` (within ~26%). This is §2 confirmed from the
  micro-rules up.
- **Collective-goal transition (C1–C3, 3/3).** A motile value economy spontaneously
  orders at low noise and disorders at high noise, with a susceptibility peak at
  `η_c`; on a *fixed* lattice it never orders (Mermin–Wagner), confirming §4's motility
  condition; and a control field `γ>0` **rounds** the transition (collective goal
  survives noise, susceptibility peak suppressed) — §3.3's mass term, measured.

So the form derived here is also the form that *emerges* from an agent economy obeying
the micro-rules — two independent routes (analytic coarse-graining, micro-simulation)
to the same field equations. Neither is yet a measurement on **real** agents/markets,
which remains the decisive open test (doc 08 §9).

## 6. Verdict and what to change in doc 08

**Verdict.** Doc 08 should be relabelled from *"value-flavoured active matter
(analogy)"* to *"the continuum limit of the value dynamics — telegrapher + Toner–Tu —
under explicit, falsifiable locality/symmetry/inertia/motility assumptions."* It is
Maxwell with stated boundary conditions, not metaphor: the field equations are
derived, the coupling constants are functions of agent quantities, and the standing
caveats (doc 08 §9) are now sharpened into *conditions you can measure* rather than
hand-waves. What is **not** yet earned is the empirical step on real systems; that gate
(doc 08 §9, §10.3) is unchanged.

Concretely, doc 08 §3/§4 should cite this document for the coefficient map, §6 should
note that the goal mass is `m^2\propto\gamma` (control), and §9's "the mappings are
constructions, not derivations" should be amended to "the mappings are derivations
*conditional on* `L>0` (wave) and local-symmetric motile imitation (transition); those
conditions, not the equations, are what remains to be checked on real systems." The
status box (§10) gains rung 2 (**pin the couplings — done, this doc**) and the Thrust-B
emergent confirmation.

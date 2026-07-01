# Kelly-Orthogonality — a sim that *exhibits* an orthogonality and *isolates* a question

> **Scope, first, because it is the whole point.** This is a synthetic sim that **exhibits** an orthogonality
> and **isolates** an empirical question — it is **not** evidence that the effect is real in nature. It assumes
> nature's agent-coupling has a particular (aligned-multiplicative) form; whether real agents couple that way is
> exactly the instrument-blocked question it sharpens, not one it answers. Same standing as the other empirical
> writeups ([`15`](15-cross-frame-realdata.md), [`18`](18-residual-scaling-redo.md)): **necessary-not-sufficient.**
> Stage-2 prep, not a result. Byline: Cheng Qian.
>
> Sim: [`sim/coupled/kelly_orthogonal.py`](../sim/coupled/kelly_orthogonal.py) (seeded, pure numpy, reuses
> [`value_sim.py`](../sim/value_sim.py)); numbers in
> [`results/kelly_orthogonal.json`](../sim/coupled/results/kelly_orthogonal.json). **7/7 checks pass.**

## 1. What this had to clear, and what E8 left open

The standing directive ([`ROADMAP.md`](ROADMAP.md) "Strategic lens"; every external review): a confirmation
counts only if it is **distinctively value** — something Kelly / information theory / decision theory cannot
produce. The single-agent bridge `ΔG = I(X;Y)` ([`02`](02-coding-theorem-of-value.md)) fails that bar; it is
Kelly's home turf. The distinctively-value claim is that goal-**alignment** `cos θ` curves the multi-agent
growth region ([`04`](04-multi-agent-capacity-region.md) §4).

Stage-0's E8 ([`17`](17-coupled-fleet-pilot.md)) confirmed the *algebra* of that frontier — it posits
`G_a = μ(t + cos θ·(1−t))` and checks the sum is `(1+cos θ)·μ`. That is "write the formula, check the formula."
It has **no Kelly null**, so it cannot make the load-bearing point: that *nothing Kelly can see moves with
`cos θ`*. This doc supplies the null and reports what it shows — and, just as carefully, what it does not.

## 2. The construction

Two agents `A, B` share a world. Each round, each agent's gross return is a product of two factors:

$$R_a(t) \;=\; \underbrace{R^{\text{perc}}_a(t)}_{\text{what Kelly sees}}\;\times\;\underbrace{R^{\text{world}}_a(t)}_{\text{what Kelly cannot see}}.$$

- **Perception factor** `R^{perc}_a` — a binary-symmetric horse race: `X ∼ Bern(½)`, agent observes `Y_a` through
  a BSC with flip `eps_a`, bets the Bayes posterior against fair odds. By construction `E[ln R^{perc}_a] =
  I(X;Y_a)` — the *entire* single-agent/Kelly content, held **identical** across every alignment condition
  (same channels, same seeds).
- **World factor** `R^{world}_a` — goal-space is 2-D; agent `a` has unit goal vector `k̂_a` and pushes the shared
  world along *its own* goal. Its world log-growth is `κ⟨k̂_a, Δm⟩` with `Δm = ρ Σ_b k̂_b`, so `a` benefits from
  `b`'s push in proportion to `⟨k̂_a, k̂_b⟩ = cos θ_ab` — a pure externality. We set `k̂_A=(1,0)`,
  `k̂_B=(cos θ, sin θ)` and sweep `cos θ ∈ [−0.8, 0.8]`.

**The Kelly null (the strongest fair null).** Run each agent *alone*, record its realized return stream, and let
a Kelly/Cover investor form the best rebalanced portfolio over the two streams. That is *everything* portfolio
theory can extract — each agent's marginal return law and their correlation, as exogenous assets. The isolated
streams do not depend on `cos θ`, so **the Kelly-null growth is a constant in `cos θ`.**

## 3. Part 1 — the genuine increment is the null, not the dividend (K1–K5)

| `cos θ` | `G_coupled` | `G_null` | dividend |
|---:|---:|---:|---:|
| −0.8 | 0.317 | 0.477 | **−0.160** |
| −0.4 | 0.397 | 0.477 | −0.080 |
|  0.0 | 0.477 | 0.477 | 0.000 |
| +0.4 | 0.557 | 0.477 | +0.080 |
| +0.8 | 0.637 | 0.477 | **+0.160** |

**The one durable result.** Realized fleet growth swings **~0.32 nats** across the sweep, while the
Kelly-over-isolated-streams null is **dead constant** (`G_null = 0.477`) and `I(X;Y_a)` never moves. Quantified
in K5: `Var(G_coupled)` is explained `R² = 1.000` by `cos θ`, and `0` by the information variables `(I_A, I_B,
G_null)`, which are constants. The docs *assert* "value-throughput is invisible to information beyond `I(X;Y)`";
this **exhibits** it — there is a concrete model where a goal-geometry quantity moves realized growth and no
information-theoretic variable has any purchase on it. **The contribution is exhibition, not discovery.**

**Concession — the dividend's *existence* is analytic, not an MC finding.** K3's residual is `1.4e-16` (machine
epsilon). With this coupling form the world factor `exp(κρ(1+cos θ))` factors straight out of the log-portfolio,
so "dividend `= κρ·cos θ`" is algebra. The Monte-Carlo in Part 1 is almost decorative. What is *not* baked in —
and is the load-bearing claim — is K2: the null's **invariance**. Portfolio theory takes returns as exogenous
data, so it *structurally* has no variable that can move with alignment, whatever the coupling's magnitude.

## 4. Part 2 — the substantive half: a conflict tax with no portfolio analog (K6–K7)

Make effort **costly**: each agent picks `ρ_a` to maximize its own per-round growth
`g_a = I_a + κρ_a + κ cos θ·ρ_b − (c/2)ρ_a²`. Measured by compounding Monte-Carlo:

| `cos θ` | Nash − isolation | cooperative − Nash |
|---:|---:|---:|
| −0.8 | **−0.064** | 0.026 |
| −0.4 | −0.032 | 0.006 |
|  0.0 | 0.000 | 0.000 |
| +0.4 | +0.032 | 0.006 |
| +0.8 | +0.064 | 0.026 |

- **K6 conflict tax** — `Nash − isolation = (2κ²/c)·cos θ`: a fleet of *optimizing* agents grows **slower than
  two isolated agents** for `cos θ < 0`.
- **K7 free-riding gap** — `cooperative − Nash = (κ²/c)·cos²θ ≥ 0`: a public-good under-provision.

**Why this is the substantive half.** Both are properties of an *equilibrium of agents choosing actions*.
Portfolio theory has no actions, hence no equilibrium, hence **cannot represent** agents whose coordination (or
conflict) changes the realized returns. Part 1 says "Kelly can't see the variable"; Part 2 says "Kelly can't
even represent the phenomenon."

**Caveat, owned.** The coupling here is **linear**, so the best-response effort is a *dominant* strategy
(`ρ* = κ/c`, independent of `cos θ` and of the other agent): there is no escalation. The tax is the **sign of
the cross-term**, not an arms race. A nonlinear / contested coupling (a Tullock-style contest) would make effort
*escalate* with misalignment and produce genuine rent dissipation — but that is still an **assumed coupling
form**, adds no evidence about real agents, and sits below the gate in value. *Future option, deliberately not
built here.* (One line, not a claim.)

## 5. An open question — flagged for a priority check, NOT claimed as novelty

It is tempting to name a "novel seam": *an information-theoretic perception ceiling `I(X;Y_a)` bounding a
goal-alignment-curved, game-theoretic growth region is non-standard in either parent field.* **This is
un-audited and is written here as an open question, not a contribution.** It is at real risk of being
anticipated by **information-constrained / bounded-rationality game theory**, **evolutionary game theory**, and
**informational general equilibrium** — each of which couples informational limits to strategic interaction in
ways this construction may simply re-instantiate. Per the project's concession discipline (the six-pass audit),
a claim like this earns the word "novel" only *after* a deep-research priority pass clears those literatures.
Until then it is a flag, not a flag-planting. **Priority check owed before any external framing of this as new.**

**First concrete entries for that priority pass (do not skip):**
- **van Merwijk, Carey & Everitt, *A Complete Criterion for Value of Information in Soluble Influence Diagrams*
  (arXiv:2202.11629, 2022).** The "value of information" (VoI) lineage is the direct ancestor of doc 02's
  *value-of-perception* claim: VoI is the expected gain to a goal-directed agent from observing a variable.
  This paper gives the *complete graphical* criterion for *when* VoI ≠ 0 (qualitative, general-utility,
  single-agent / multi-decision). Our `ΔG = I(X;Y)` is the *quantitative* law in the **log-utility / compounding**
  slice (classical VoI = mutual information only there — Kelly 1956), so it is **not** anticipated quantitatively
  — but the *framing* is squarely in this tradition and must be cited as such, the way is/ought was conceded to
  Armstrong & Mindermann and the side-info bound to Barron–Cover. (NB: Everitt endorsed the arXiv submission and
  is the Stage-2 collaboration target — this is common ground, not a priority threat.)
- **Multi-Agent Influence Diagrams (MAIDs; Koller–Milch; Hammond, Fox, Everitt et al.)** — the *game-theoretic*
  extension of the above, coupling informational structure to strategic interaction. This is the literature
  **most likely to anticipate the §5 "seam"** (info structure bounding a strategic, alignment-shaped outcome).
  Clear MAIDs (and informational-GE / info-constrained game theory) before claiming the seam is new.
- **Jing Chen, *An entropy theory of value* (Structural Change and Economic Dynamics, 2018); Galbraith & Chen,
  *Entropy Economics* (2024); Georgescu-Roegen (1971).** *This is prior art for the FOUNDATIONAL layer, not the
  §5 seam — recorded here and folded into [`related-work.md`](related-work.md) "Entropy theories of value".*
  Chen independently and earlier makes our doc-00/01 core moves: value = `−log(scarcity)` = Shannon entropy,
  derived from additivity axioms; "an entropy theory of value is inevitably an information theory of value";
  thermodynamic low-entropy grounding; value-of-information ≈ mutual information. **Must-cite** in any public
  framing — a value paper titled *A Mathematical Theory of Value* that omits it reads as a novelty overclaim to
  the physics.soc-ph / ecological-economics audience. NOT in Chen's line (our departures): compounding/Kelly
  growth-rate, the `ΔG=I(X;Y)` capacity theorem with converse, the `G=D(q‖r)−D(q‖p)` Second Law, and the entire
  multi-agent price/alignment/fleet/dynamics layer. Net: it *sharpens* the standing verdict that originality
  rests on the multi-agent layer, and closes a real gap (Chen was absent from related-work.md).

## 6. What it does NOT show

- **It assumes the coupling form.** The whole effect rides on real agents' value-streams coupling through an
  aligned-multiplicative term `κ⟨k̂_a, Δm⟩`. Real LLM fleets or markets may not. The sim does not close that gap
  — it **isolates** it, consistent with the convergence finding and [`15`](15-cross-frame-realdata.md) /
  [`18`](18-residual-scaling-redo.md): the distinctively-value claim remains testable only via a controlled
  multi-agent experiment with capable agents.
- **Part 1 is near-analytic** (§3) — its load-bearing claim is the null's invariance, not the dividend.
- **Two agents, 2-D goals, pairwise `cos θ`.** Genuine multi-way interactions are out of scope
  ([`04`](04-multi-agent-capacity-region.md) §7).

## 7. The compounding hook — a sharper target for the Stage 2 grid

The one thing that makes this compound rather than sit isolated: it hands the coupled-regime experiment a
**sharpened, pre-registerable signal and null.**

- **Signal.** The slope of the fleet-growth dividend in `cos θ`, measured at **fixed `I(X;Y_a)`** (perception
  channels clamped identical across alignment conditions). A non-zero slope at fixed `I` is the distinctively-
  value observable.
- **Null.** The Kelly/Cover portfolio growth over the agents' **isolated** return streams — constant in `cos θ`
  by construction. The experiment confirms value-content only if realized coupled growth *departs* from this
  null in a way that tracks `cos θ`.

> **Forward-pointer (for the Stage 2 *grid* pre-registration, to be frozen after the gate passes —
> [`ROADMAP.md`](ROADMAP.md) ⊕ The Maxwell program):** adopt this **`cos θ`-slope-at-fixed-`I` signal** and the
> **Kelly-isolated null** as the grid's primary endpoint. It converts "does alignment add value beyond
> information?" into a single clamped-`I`, varied-`cos θ` contrast with a pre-registered null that no
> information-theoretic account can move.

## Run

```sh
python3 sim/coupled/kelly_orthogonal.py     # ~10s; exits 0 iff all 7 checks pass
```

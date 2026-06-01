# sim/field — does the field theory (doc 08) have its claimed phenomenology?

The first concrete step of [`docs/08`](../../docs/08-field-theory-of-value.md) §10: simulate the continuum
limit and check whether its two headline predictions actually emerge. **5/5 checks pass**
(`python3 sim/field/field_experiments.py`, ~2s).

| Check | doc 08 | Prediction | Result |
|---|---|---|---|
| **F1a** | §3 | large lag `τ` → demand-shock spreads **ballistically**, `σ²(t) ∝ t²` (a wave) | PASS — `R²_quad=0.97 > R²_lin`; front speed `2.44` vs predicted `√(D/τ)=2.50` |
| **F1b** | §3 | small `τ` → spreads **diffusively**, `σ²(t) ∝ t` | PASS — `R²_lin=1.00 > R²_quad` |
| **F1c** | §3 | wave speed obeys the telegrapher law `v ∝ 1/√τ` | PASS — measured/`√(D/τ)` constant to **1%** across `τ∈{4,8,16,32}` |
| **F2 (transition)** | §5 | goal-directors undergo an **order→disorder phase transition** with noise | PASS — order parameter `m`: `0.99 → 0.03` |
| **F2 (collapse)** | §5 | the collective goal collapses monotonically as noise rises | PASS — `Δm=0.96` across the sweep |

So the "value is an intelligence wave" intuition is, at minimum, **internally coherent**: a population of
agents with local resource-transport + response-lag *does* carry demand as a damped wave with the predicted
speed law, and a population of goal-directors *does* condense into a collective goal as a genuine phase
transition.

## What this is — and is NOT (honest scope, per doc 08 §9)

- **F1** simulates the *coarse-grained field dynamics* (the telegrapher equation derived in doc 08 §3). It
  therefore tests whether the predicted **scaling laws** hold (ballistic-vs-diffusive crossover; `v∝1/√τ`) —
  which is non-trivial and could have failed — **not** whether real agents behave this way. It is an
  internal-consistency check of the construction, like the synthetic `sim/` for the core theory.
- **F2** is the real **Vicsek model** (self-propelled particles; its continuum limit is the Toner–Tu theory
  doc 08 is built on). It moves because a *static* 2D lattice is the XY model, which by Mermin–Wagner does not
  order — flocks order only because they move. F2 thus confirms our goal field **is** an active-matter order
  parameter, by reproducing known active-matter physics (expected, and the point).
- **Neither is empirical evidence about real agent populations or markets.** Doc 08 §9 names the decisive test:
  a *measured* dispersion crossover or flocking transition in a real system. That remains undone. This
  simulation only clears the first gate — *does the continuum limit even have the phenomenology?* — and the
  answer is yes.

## Real-data foundations check — `v2_geometry.py`

The first time the field theory touches *real* data. The field theory models an agent population as an
**order-parameter field** (goals/competences that align, with a dominant collective direction). This check asks
one honest, limited question of the 30 v2 caches (10 models × 3 domains): **does a real agent population sit in
the field theory's *ordered* (aligned) phase?** Run: `python3 sim/field/v2_geometry.py`.

| Domain | mean cross-agent correlation (vs independent null) | top eigenvalue fraction `λ₁/Σλ` (vs null) |
|---|---|---|
| intent | **+0.51** vs +0.00 — **z = +51** | **0.51** vs 0.21 — z = +43 |
| mcqa | **+0.34** vs −0.00 — **z = +36** | **0.41** vs 0.13 — z = +51 |
| topic | **+0.32** vs +0.00 — **z = +32** | **0.41** vs 0.14 — z = +50 |

**Reading:** across all three domains the population is strongly **ordered** — a dominant shared competence
axis and strong positive cross-agent correlation, *tens of standard deviations* above what independent agents
at the same accuracies would show. So real agents **do** have the low-dimensional alignment geometry the field
theory's order parameter assumes. Bonus: this *static* geometry **explains** the v1/v2 R5 result (no Shannon's
demon) — a positively-aligned population is deep in the constructive-interference regime, so pooling/pricing has
little anti-correlated diversity to harvest. The geometry predicts the dynamics.

**Honest scope:** this supports the order-parameter *assumption* on real agents. It is **not** a test of the
wave dynamics (doc 08 §3) or the phase transition (§5) — those need agents whose goals *evolve* over time, which
v2 (static classification) does not have. Suggestive of the foundations, not validation of the field theory.
The decisive test (a *measured* dispersion crossover or flocking transition in a dynamic agent system) remains
open.

## Files

- `field_experiments.py` — F1 (telegrapher demand-wave: `simulate_front` for speed, `simulate_spread` for the
  ballistic/diffusive second-moment discriminator) and F2 (`vicsek_order`, self-propelled flock). numpy only.
- `v2_geometry.py` — the real-data order-parameter foundations check above (reads `sim/real/v2/results/raw/`).

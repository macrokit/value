# The ‖Vg‖/γ Redo — Maxwell Stage 1 (de-saturated design): CAP again, and the small-model thread closes

> **Maxwell program, Stage 1.** The redo that [`13`](13-incentive-vs-oversight-real.md)
> §5 named: same instrument (qwen2.5:1.5b, symbol-randomised, China-Mac fleet), the
> design fixed per doc 13's own postmortem — K=16 **tent** landscape (interior peak
> decoupling gradient strength from boundary runaway), an 8×-per-axis grid
> g ∈ {0.25, 0.7, 2.0} × γ ∈ {2, 6, 18}, 8 seeds, direction-test δ = 0.5 (10×).
>
> Pre-registered in [`sim/field/real/PREREGISTRATION_stage1.md`](../sim/field/real/PREREGISTRATION_stage1.md)
> (frozen before any run; SHA precedes this results commit).
>
> **Result, stated plainly: SCALING = CAP (again — but for the mirror-image reason),
> DIRECTION = FALSIFIED by the letter of the frozen rule, with the trigger pathway
> disclosed as non-response rather than oversight-beats-incentive.** The substantive
> finding is sharper than either verdict: **at K=16 the real agents do not respond to
> the reward landscape at all** — the population sits at uniform scatter in every one
> of 9 conditions spanning 8× in each knob. Doc 13's design saturated; this design
> dissolved responsiveness. Two independent designs, two CAPs, and every measured
> trend across both has g-exponent ≈ 0. **The small-local-model thread closes here**
> (§5); the residual-scaling question moves to Stage 2's frontier-agent instrument.

## 0. The system

104 runs (9 grid conditions + 4 direction arms, × 8 seeds), N=20 agents, T=18 rounds,
J=1.0, temp 0.6, annealed n_nb=6, per-agent symbol-randomisation (mandatory bias
control), structured output, **parse rate = 1.00 in all 104 runs**. ~37k cached LLM
calls (~9.8 h). Landscape: `rewards[k] = g·(12 − |k−12|)` (slope ±g, peak 12g at
k_g=12, zero at the target k*=0); control γ as a bonus at k*. All measurements in
true-niche space. Raw: [`results/stage1_raw.json`](../sim/field/real/results/stage1_raw.json);
frozen-rule analysis: [`analyze_stage1.py`](../sim/field/real/analyze_stage1.py) →
[`results/stage1_redo.json`](../sim/field/real/results/stage1_redo.json).

## 1. The grid, and what the regime rule found

| γ | g | residual (±seed std) | V_ss | k̄ | above-peak | V·g/γ | regime |
|---|---|---|---|---|---|---|---|
| 2 | 0.25 | 8.59 ± 0.85 | 16.3 | 8.6 | 0.21 | 2.03 | excluded (iii) |
| 2 | 0.70 | 8.69 ± 1.33 | 15.4 | 8.7 | 0.24 | 5.39 | excluded (iii) |
| 2 | 2.00 | 8.87 ± 0.99 | 14.5 | 8.9 | 0.23 | 14.5 | excluded (iii) |
| 6 | 0.25 | 7.66 ± 1.08 | 19.8 | 7.7 | 0.18 | 0.82 | **in-regime** |
| 6 | 0.70 | 8.16 ± 1.81 | 16.4 | 8.2 | 0.22 | 1.91 | excluded (iii) |
| 6 | 2.00 | 8.36 ± 1.40 | 18.3 | 8.4 | 0.24 | 6.09 | excluded (iii) |
| 18 | 0.25 | 7.62 ± 1.53 | 20.0 | 7.6 | 0.22 | 0.28 | excluded (iii) |
| 18 | 0.70 | 7.03 ± 1.44 | 24.5 | 7.0 | 0.21 | 0.95 | excluded (iii) |
| 18 | 2.00 | 9.20 ± 1.42 | 16.4 | 9.2 | 0.32 | 1.82 | excluded (iii) |

**8/9 conditions fail the regime rule on clause (iii)** (above-peak fraction > 0.20)
→ only 1 in-regime condition → the pre-registered minimum (≥6 conditions, ≥4× span)
is unreachable → **SCALING = CAP ("insufficient in-regime span")** by the frozen rule.

**Honest disclosure of what clause (iii) actually detected.** The clause was designed
to catch *pile-up at the reward peak* (saturation). It fired for the opposite reason:
a **uniform-scatter** population on K=16 has `P(k > 12) = 3/16 = 0.188`, and the
measured fractions (0.18–0.32) sit at exactly that value — the population never *left*
uniform scatter. The exclusions are mechanically correct (the linearized Price-drift
derivation indeed does not describe a non-responding population) but the named reason
differs from the anticipated one, and we say so.

## 2. The substantive finding: no response, affirmatively demonstrated

The CAP is not a default — the prereg's anti-default clause demands the deviation be
affirmatively shown noise/non-estimable, and it is:

- **Residuals are flat at the uniform mean.** Grand mean 8.24 (uniform k̄ = 7.5),
  range 7.0–9.2 across a grid spanning **8× in g and 9× in γ**. `R_across ≈ 0` vs
  `3σ_in = 3.24`: the across-condition signal is *zero* against the seed noise.
- **Dispersion is the uniform value.** Grand mean V_ss = 17.9 (uniform = 21.25); no
  condition collapses (min 14.5) — nothing concentrates, not even under γ=18, a
  control bonus 18× the teamwork dividend.
- **Exploratory free fit on all 9 conditions** (labelled exploratory — these are the
  conditions the frozen rule excludes; shown descriptively):
  `residual ∝ g^{+0.049} γ^{−0.045}` (R² = 0.52) — exponents ≈ **(0, 0)** against the
  theorem's (+1, −1). The same g-exponent ≈ 0 that doc 13's mean trend showed (−0.01),
  now joined by a γ-exponent ≈ 0.

Doc 13 and this run fail in mirror image: there, `g ≤ 0.2` saturation made the
gradient *too weak to matter*; here, agents at K=16 *cannot read the landscape at
all*. Rung 8 demonstrated γ-response at K=8 (order parameter 0.18 → 0.51 under a
field); at K=16, with 16 enumerated reward lines in the prompt, that response
dissolves — a 1.5b instrument-capability ceiling, not a property of the law being
tested.

## 3. Direction verdict — FALSIFIED by the frozen rule's letter, disclosed in full

| Point | r0 | raise-γ arm | lower-g arm | eff_γ | eff_g | ratio | floor |
|---|---|---|---|---|---|---|---|
| B1 (γ=6, g=0.7) | 8.16 | 8.78 | 7.59 | **−1.24** | +1.14 | −0.92 | 0.54 |
| B2 (γ=18, g=0.7) | 7.03 | 7.59 | 7.58 | **−1.12** | −1.10 | 0.99 | 0.54 |

The frozen rule (§4 of the prereg): B1's arm signals (0.62, 0.57) exceed the floor
(0.54) → "resolvable"; eff_g/eff_γ = −0.92 < 1 → **DIRECTION-FALSIFIED**. The theorem
predicted eff_g/eff_γ ≈ +4.3 at B1. We keep this verdict as the verdict-of-record —
the same discipline by which doc 13 refused to switch from its committed raw-σ
convention when an SEM reading would have *flattered* a different outcome; the rule
binds symmetrically when it goes against comfort.

**Full disclosure of the trigger pathway (committed-rule honesty, doc-13 style):**

1. **The sign pattern is non-response, not oversight-beats-incentive.** eff_γ < 0 at
   *both* points — raising the control bonus *increased* measured misalignment, which
   no control-theoretic reading supports; and at B2 *both* levers "hurt." On a flat,
   noisy baseline, ±0.6 swings in 8-seed means (seed std 1.0–1.9, SEM 0.36–0.68) are
   unremarkable. The physically coherent reading is the same unresponsiveness as §2.
2. **The floor is fragile.** σ_in comes from the *single* in-regime condition (std
   1.08); the floor 0.54 = σ_in·√(2/8). An SEM-of-difference reading (SE ≈ 0.5–0.9
   per arm) would call **all four** arm signals unresolvable → INCONCLUSIVE. We
   disclose that reading and do not adopt it post-hoc.
3. Net: the governance direction ("reducing g beats raising γ") is **falsified on this
   instrument** in the rule's terms, and the *content* of that falsification is that
   **neither lever moves the population at all** — which is also why the scaling is
   CAP. The two verdicts are one phenomenon.

## 4. Net status of the alignment-stability theorem (precise, cumulative)

- **Toy (doc 12):** confirmed as self-consistency (R² = 0.999) — necessary, not
  discovery.
- **Real attempt 1 (doc 13, K=8 linear):** CAP — saturation forced a g-window below
  the noise floor; mean trend leaned negative (g-exp ≈ 0).
- **Real attempt 2 (this, K=16 tent):** CAP on scaling — population non-responsive;
  direction FALSIFIED per the frozen rule via the non-response pathway; exploratory
  exponents (+0.05, −0.05) vs theorem (+1, −1).
- **Cumulative:** the theorem remains **unvalidated on real agents**, and every
  measured trend across two independent designs is consistent with *residual
  independent of g* — but neither run cleared its own pre-registered bar for a clean
  falsification, and we do not claim one. What is now established about the
  *instrument*: small local models cannot be placed in the theorem's linear-response
  regime — K=8 saturates the gradient; K=16 dissolves the response.

## 5. Decision: close the small-model thread; the question moves to Stage 2

Doc 13's decision rule said: "CAP again → report what would de-CAP it or close the
thread." Both, explicitly:

**What would de-CAP it** (named for completeness, not pursued at this scale):
1. A **pre-registered responsiveness gate** run *before* any scaling grid: a γ-only
   sanity condition that must move k̄ by a stated margin (e.g. ≥ 2 niches below
   uniform within T rounds). If the gate fails, the instrument is declared incapable
   and the grid does not run — a cheap abort that both doc-13 designs lacked.
2. An instrument whose agents demonstrably read the landscape: smaller K with the
   tent (K=8–12 keeps the prompt within the 1.5b attention budget — though K=8
   re-tightens the saturation window), salient-mode prompting, or **stronger agents**.

**Why we close rather than iterate:** a third small-model attempt would have to
thread a needle that two designs have now bracketed from both sides (K=8: saturation;
K=16: non-response), with no evidence the needle's eye exists at 1.5b — and escalating
model size *within this thread* is exactly the instrument-fishing the standing
guardrails prohibit. The honest move is the one the Maxwell program already provides:
**Stage 2's frontier-agent coupled economy** is the next and proper instrument for the
residual-scaling question — capable agents, payout coupling (design validated in
[`17`](17-coupled-fleet-pilot.md)), its own pre-registration including the
responsiveness gate above, its own budget, and owner sign-off. Until then the v5
paper's decisive-prediction paragraph stands as printed: the `‖Vg‖/γ` half remains
**instrument-blocked** — now with the small-LLM instrument class affirmatively
exhausted rather than merely suspected insufficient.

## 6. Honest limits of this test itself

- **Toy scale**: N=20, T=18, 1.5b, uniform resource weights, temperature-as-noise —
  all doc-13 §6 limits carry over.
- **The K=16 design is implicated, not exonerated**: we cannot distinguish "the law
  is false for these agents" from "these agents cannot express any law at K=16."
  That is precisely why CAP, not falsification, is the scaling verdict.
- **The single in-regime condition** makes σ_in (hence the direction floor and the
  signal gate) fragile — disclosed in §3; both alternative readings stated.
- **Clause (iii) ambiguity**: the regime rule could not distinguish peak pile-up from
  uniform scatter (both put >20% above k_g). A future rule should test uniformity
  directly (e.g. V_ss within a band of V_unif AND k̄ within a band of (K−1)/2 ⇒
  non-responsive, a distinct named outcome).
- **Reproducible**: every call cached (`results/cache.sqlite`); analysis cache-only;
  pre-registration → instrument → results commits in provable order.

*Author byline: Cheng Qian. Pre-registration (frozen) and instrument commits precede
this results commit — see git log.*

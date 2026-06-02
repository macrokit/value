# PRE-REGISTRATION ADDENDUM — Lever-1 three-outcome decision rule

**Committed before any curve-fitting or interpretation of the grid.** Status at the
time of writing: the detached run has logged 4 of 6 Prediction-A grid points to
`results/lever1_run.log`; **no fit has been performed, no V·g/γ regression run, no
outcome chosen.** This addendum freezes the rule that maps the completed grid to one of
three outcomes, so the falsification-vs-CAP call cannot be made post-hoc after seeing
fits. It refines (does not relax) the falsification/CAP definitions of
`PREREGISTRATION_lever1.md` §0. Author byline: Cheng Qian.

---

## 0. Why this addendum

The base pre-registration (§0) defined only two non-confirming buckets: F-A (a narrow
"directionally wrong AND R²<0.50" falsification) and CAP ("high variance, no monotone
dependence — not testable"). That collapses a real third case: **the residual may be
systematic and lawful but follow a *different* law than V·g/γ.** That is a *clean
falsification of the precise theorem*, not "not testable." Defaulting such a result to
CAP would understate a genuine negative. This addendum separates the three.

---

## 1. The three outcomes (mutually exclusive; the scaling test resolves to exactly one)

Over the completed 6-condition grid (γ∈{0.5,1,2} × g∈{0.1,0.2}, 3 seeds each), with
`residual_ss`, `V_ss` measured per `PREREGISTRATION_lever1.md` §1:

**Outcome 1 — CONFIRM (residual ∝ V·g/γ).**
The primary law L0: `residual = C·(V·g/γ)` passes the base §2 thresholds —
log-log slope α ∈ [0.60, 1.60] **and** R² ≥ 0.70 **and** mean ratio ∈ [0.50, 2.00].
→ The theorem's scaling law holds on real agents.

**Outcome 2 — CLEAN FALSIFICATION (systematic, but ≠ V·g/γ).**
L0 fails its thresholds, **but the deviation is SYSTEMATIC** by the §2 discriminator
below — some alternative law fits cleanly, or the free-exponent fit returns stable
exponents inconsistent with V·g/γ. → The precise `‖Vg‖/γ` scaling is a toy artifact;
real agents follow a different (or g-independent) lawful relation. **Report as a real
negative — NOT "not testable."**

**Outcome 3 — CAP (not testable at this scale).**
L0 fails **and** the deviation is NOISE / non-estimable by the §2 discriminator — no
candidate law fits, within-condition seed scatter swamps the across-condition signal,
or V_ss is not cleanly estimable. → Neither confirmation nor falsification. Report CAP;
**do NOT escalate model size to fish.**

> **Anti-default rule:** CAP (outcome 3) requires *affirmatively demonstrating* the
> deviation is noise/non-estimable. "L0 failed" alone is **not** sufficient for CAP —
> it must first be checked against outcome 2.

---

## 2. The 2-vs-3 discriminator (systematic vs noise) — committed

Run all of the following on the completed grid, then apply the decision gate.

**(a) Candidate law family (fit each; record R² and, where applicable, exponents):**
- L0: `residual = C·V·g/γ`        (the theorem)
- L1: `residual = C·g/γ`          (drop V)
- L2: `residual = C·V·g`          (drop 1/γ)
- L3: `residual = C/γ`            (γ-only; g-independent)
- L4: `residual = C·V·gᵖ·γᵠ`      (free exponents p, q)
- Lpow: `residual = C·gᵖ·γᵠ`      (free power law, V folded into C)
- Lnull: `residual = C`           (constant)

**(b) Noise vs signal:**
- σ_in := median over conditions of the seed-level std of `residual_ss`.
- R_across := max−min of condition-mean `residual_ss` across the 6 conditions.
- V-estimability: CV_V := median over conditions of (seed-std(V_ss)/mean(V_ss)); and
  the across-condition range of V_ss. V is "not cleanly estimable" if CV_V > 0.5 or V_ss
  barely varies while it should (saturation).

**(c) Stability:** for the best-fitting non-null law, leave-one-condition-out — refit on
5 conditions, check the exponents/structure are stable (Δp, Δq < 0.5 and sign-stable).

**Decision gate (apply in order):**
1. If L0 passes §2 base thresholds → **Outcome 1**.
2. Else if `best-alternative-law R² ≥ 0.70` **AND** `R_across > 3·σ_in` (signal exceeds
   noise) **AND** the best law is leave-one-out stable **AND** V is estimable
   (CV_V ≤ 0.5) → **Outcome 2** (systematic, different law — falsification). Name the
   law that fits and how its exponents differ from (V¹g¹γ⁻¹).
3. Else → **Outcome 3** (CAP). State which gate failed (no law ≥0.70 R², or signal≤noise,
   or unstable, or V non-estimable).

---

## 3. The DIRECTION test — separable, reported independently of the scaling outcome

The exact scaling law and the governance *direction* are **separable**: "reducing g
beats raising γ" can hold even if `residual ≠ V·g/γ` exactly, and can fail even if some
law holds. From the B cases (`PREREGISTRATION_lever1.md` §3) at (γ=1,g=0.1) and
(γ=2,g=0.1), with `eff_g`, `eff_γ` as defined there:

- **DIRECTION-CONFIRMED:** eff_g/eff_γ > 1 at both B points (reducing g lowers residual
  more than raising γ per unit) — the governance claim survives on real agents.
- **DIRECTION-FALSIFIED:** eff_g/eff_γ < 1 at (γ=1,g=0.1) where theory predicts ~5
  (base §3 F-B trigger) — oversight matches/beats incentive design; governance claim
  falsified.
- **DIRECTION-INCONCLUSIVE:** |eff_g − eff_γ| within seed noise (the δ-perturbation
  signal is below the seed-level std of residual_ss) — the perturbation is too small to
  resolve at this scale. State this explicitly.

This verdict is reported **regardless** of the scaling outcome (1/2/3), and the two are
kept distinct in docs/13.

---

## 4. What docs/13 must contain

1. The scaling outcome resolved to **exactly one** of {1 confirm, 2 falsification, 3 CAP},
   with the §2 discriminator values shown (all candidate-law R²s, σ_in, R_across, CV_V,
   leave-one-out stability) — so the reader can audit the 2-vs-3 call.
2. The direction verdict resolved to **exactly one** of {confirmed, falsified,
   inconclusive}, with eff_g, eff_γ, and the seed-noise floor shown.
3. Both kept separate; no rounding a falsification up to a confirmation nor down to CAP,
   and no defaulting to CAP without passing the anti-default gate of §1.

*Addendum commit SHA precedes the results commit SHA — see git log.*

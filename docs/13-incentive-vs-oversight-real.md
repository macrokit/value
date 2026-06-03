# Incentive Design vs Oversight on Real LLM Agents — the Discovery Shot

> **LEVER 1, real-agent rung.** The toy (doc 12) confirmed `residual = V·g/γ` as a
> self-consistency check (R²=0.999) in a simulation built from the theorem's own
> dynamics — necessary, not a discovery. This document is the discovery attempt: does
> the alignment-stability theorem (doc 07 §3) describe **real bias-controlled LLM
> agents** whose decision dynamics are *not* derived from the theorem?
>
> Pre-registered in [`sim/field/real/PREREGISTRATION_lever1.md`](../sim/field/real/PREREGISTRATION_lever1.md)
> and the three-outcome decision rule in
> [`PREREGISTRATION_lever1_analysis_addendum.md`](../sim/field/real/PREREGISTRATION_lever1_analysis_addendum.md)
> (both committed before fitting; SHAs precede the results commit).
>
> **Result, stated plainly: SCALING = CAP (not cleanly testable at this scale);
> DIRECTION = INCONCLUSIVE.** Neither a confirmation of `V·g/γ` nor a clean
> falsification of it on real agents. The discovery shot did **not** land. The honest,
> disciplined accounting — including a real tension the pre-committed rule resolves
> toward CAP — is below.

## 0. The system

`N=20` agents, `K=8` niches on a target line (`k*=0`), `qwen2.5:1.5b-instruct`,
temp=0.6, `J=1.0` alignment dividend, annealed `n_nb=6`, `T=18` (warm 6 + meas 12),
3 seeds. **Per-agent symbol-randomisation** (the rung-8 confound control): each agent
sees niches under its own fixed label permutation, so collective token bias cancels;
all physics (`k̄`, `V`, rewards, control) is measured in true-niche space. Reward
gradient `rewards[k] = g·k` (off-target pays); control `γ` rewards `k*=0`. Noise = the
LLM's own sampling temperature (no externally-imposed alignment noise — guardrail
carried over verbatim from rung-8). **Parse rate = 1.00 across all conditions** — the
agents play the game. Every call cached (auditable, offline-reproducible).

This rung is licensed by rung-8's clean negative: rung-8 killed *flocking* (irrelevant
to Lever 1) but validated the two ingredients Lever 1 needs — real agents respond to a
reward-gradient `g` (adoption ~0.7 under a salient shock) and to control `γ` (external
field lifts order 0.18→0.51). The prerequisites are present; this rung tests the law.

---

## 1. Prediction A — the scaling law `residual = V·g/γ`

**Grid (pre-registered):** γ ∈ {0.5, 1.0, 2.0} × g ∈ {0.1, 0.2}, 3 seeds each. The
narrow `g ≤ 0.2` window is a **pre-stated design constraint** (prereg §1): with K=8 and
a linear gradient, `g > γ/7` saturates niche 7, so a g-strong regime is not reachable
without leaving the non-saturated regime.

| γ | g | residual (k̄−k*) | V_ss | predicted V·g/γ | ratio |
|---|---|---|---|---|---|
| 0.5 | 0.1 | 4.322 ± 0.162 | 6.130 | 1.226 | 3.53 |
| 0.5 | 0.2 | 4.129 ± 0.702 | 5.723 | 2.289 | 1.90 |
| 1.0 | 0.1 | 3.399 ± 0.881 | 6.084 | 0.608 | 5.59 |
| 1.0 | 0.2 | 3.372 ± 0.413 | 6.083 | 1.217 | 2.98 |
| 2.0 | 0.1 | 3.110 ± 0.648 | 6.618 | 0.331 | 9.33 |
| 2.0 | 0.2 | 2.857 ± 0.465 | 6.282 | 0.628 | 4.55 |

**Pre-registered checks:**

| Check | Threshold | Result |
|---|---|---|
| A1 log-log slope ∈ [0.60,1.60], R²≥0.70 | | **FAIL** — slope 0.176, R² 0.559 |
| A2 mean ratio ∈ [0.50, 2.00] | | **FAIL** — mean 4.65, std 2.39 |
| A3 residual ↓ as γ↑ (≥1/2 g-slices) | | **PASS** — monotone in both slices |

`V·g/γ` is **not** confirmed: the predicted residual (0.33–2.29) is the wrong magnitude
*and* the wrong shape (it should rise steeply with g; the measured residual barely moves
with g). A1/A2 fail decisively. A3 passes — residual *does* fall with γ — but that alone
is the weakest directional check.

---

## 2. The committed three-outcome discriminator (scaling)

Per the addendum, "A1 failed" is **not** sufficient for CAP — it must first be tested
against outcome 2 (systematic-but-different law). Running the frozen §2 discriminator
([`analyze_lever1.py`](../sim/field/real/analyze_lever1.py), cache-only):

**Candidate-law fits (R² on the 6 condition means, log space):**

| Law | R² | fitted exponents |
|---|---|---|
| L0 `V·g/γ` (theorem, fixed) | **−11.7** | V¹ g¹ γ⁻¹ |
| L1 `g/γ` (fixed) | −13.7 | g¹ γ⁻¹ |
| L2 `V·g` (fixed) | −6.1 | V¹ g¹ |
| L3 `1/γ` (g-independent, fixed) | −7.4 | γ⁻¹ |
| **L4 `V·gᵖγᵠ` (free p,q)** | **+0.989** | **g^−0.01 γ^−0.31** |
| Lpow `gᵖγᵠ` (free, no V) | +0.966 | g^−0.07 γ^−0.25 |
| Lpow3 `Vʳgᵖγᵠ` (free all) | +0.985 | V^1.23 g^0.01 γ^−0.33 |

**The mean trend is systematic and points away from the theorem.** A free power law fits
the condition means at R²=0.99 and is leave-one-out stable (g-exp spread 0.08, γ-exp
spread 0.04, sign-stable). But its **g-exponent is ≈ 0** (−0.01) and its γ-exponent is
**≈ −0.31** — not the theorem's (g:+1, γ:−1). Read at face value, the clean mean-trend
says *residual is essentially independent of g and weakly decreasing in γ* — a
**directional contradiction** of `V·g/γ`, whose entire content is that `g` drives
misalignment.

**Why the verdict is nonetheless CAP, not falsification.** The frozen 2-vs-3 gate
requires the deviation be systematic *above the noise floor*: `R_across > 3·σ_in`, where
`σ_in` is the median within-condition **seed std** of residual. Here:

| quantity | value | gate |
|---|---|---|
| σ_in (median seed std of residual) | 0.556 | — |
| R_across (across-condition range) | 1.465 | — |
| **signal/noise R_across/σ_in** | **2.63** | **need > 3 → FAIL** |
| CV_V (seed CV of V) | 0.110 | ≤0.5 → V estimable ✓ |
| L-best alternative R² | 0.989 | ≥0.70 ✓ |
| leave-one-out stable | yes | ✓ |

Three of the four §2 gates pass (clean alt-law fit, stable, V estimable) — **but the raw
per-seed signal-to-noise is 2.63, below the pre-committed 3× bar.** By the frozen rule
this is **Outcome 3 — CAP, not cleanly testable at this scale.**

> **Honest disclosure of the marginal call.** An SEM-based reading (condition means have
> SEM ≈ σ_in/√3 ≈ 0.32, giving signal/noise ≈ 4.5 > 3) *would* cross into Outcome 2
> (clean falsification). We committed to **raw seed std**, not SEM, in the addendum, and
> it yields 2.63 < 3 → CAP. We report CAP and **do not** switch to the SEM reading
> post-hoc to claim a falsification — that latitude is exactly what the pre-registration
> exists to remove. The defensible statement is: *the mean trend leans toward falsifying
> `V·g/γ` (g-independence), but the per-seed noise does not clear our own pre-stated bar,
> so it is not yet a clean falsification — it is underpowered.*

**Why CAP is also the physically honest reading (not just a threshold technicality).**
The fleet sits near-uniformly scattered (V_ss ≈ 6.0–6.6 vs uniform-over-{0..7} variance
5.25) with mean k̄ ≈ 2.9–4.3 (uniform mean 3.5), weakly pulled toward k*=0 by γ. In the
`g ≤ 0.2` window that K=8 saturation forces, the *entire* reward-gradient spread is only
`g·7 = 0.7–1.4` — comparable to the J=1 dividend and below the temperature noise. So the
agents barely respond to `g` here **because the testable g-window is too weak**, not
(provably) because the theorem's g-dependence is false. That is the definition of "not
cleanly testable at this scale/design." Resolving it needs a system where `g` can be
made strong without saturation (more niches / continuous goal space) **and** more seeds
to shrink σ_in — not a bigger model. **We did not escalate past 1.5b (no fishing).**

---

## 3. Prediction B — the governance direction (separable)

The exact scaling law and the governance *direction* ("does reducing g beat raising γ?")
are separable. B perturbs each in-zone operating point by δ=0.05 and compares
`eff_g = Δresidual/Δ(−g)` to `eff_γ = Δresidual/Δγ`.

Noise floor on a difference of two 3-seed means: `σ_in·√(2/3) ≈ 0.454`.

| Point | raise-γ signal \|Δres\| | lower-g signal \|Δres\| | resolvable? |
|---|---|---|---|
| B1 (γ=1, g=0.1) | 0.393 (eff_γ=−7.86) — below floor | 0.974 (eff_g=+19.47) — above floor | **No** (γ-arm below floor) |
| B2 (γ=2, g=0.1) | 0.006 (eff_γ=+0.11) — below floor | 0.106 (eff_g=+2.11) — below floor | **No** |

Three of four δ=0.05 perturbations — including **both** `eff_γ`-defining raise-γ signals
— fall below the noise floor. `eff_γ` even flips sign between B1 (−7.86) and B2 (+0.11):
the same quantity, noise-dominated. By the committed §3 rule (CONFIRMED needs *both*
points fully resolvable with incentive winning at both; FALSIFIED needs B1 resolvable
with oversight winning), the verdict is:

**DIRECTION = INCONCLUSIVE** (0/2 B points fully resolvable; δ=0.05 perturbations mostly
below the seed-noise floor).

> The single resolvable perturbation (B1 lower-g, eff_g=+19.5) is *weakly suggestive*
> that reducing g helps — but one of four resolvable arms cannot carry a verdict, and the
> committed rule correctly returns INCONCLUSIVE. A larger δ or more seeds is the fix.

The pre-registered runner's headline ("PARTIALLY CONFIRMED, 3/6") is **superseded** by
this discriminator: A3, B2, and B_mono are noise-contaminated passes (A3 is the weakest
check; B2/B_mono are mechanical given a noise-flipped eff_γ). The authoritative reading
is CAP (scaling) + INCONCLUSIVE (direction).

---

## 4. Net status carried forward (precise)

- **Scaling law `residual = V·g/γ` on real agents:** **CAP — not cleanly testable at
  this scale/design.** The condition-mean trend is systematic and leans *against* the
  law (g-exponent ≈ 0, i.e. residual ~independent of g), but (i) raw per-seed
  signal/noise (2.63) does not clear the pre-committed 3× bar, and (ii) the K=8
  saturation constraint forced a g-window too weak for agents to respond to — so the
  g-independence is confounded with "g too weak to matter here." Underpowered, not
  refuted; and not confirmed.
- **Governance direction (reduce-g vs raise-γ):** **INCONCLUSIVE** — the δ=0.05
  perturbations are below the seed-noise floor; the one resolvable arm weakly favours
  incentive design but cannot decide.
- **Neither a validated positive nor a clean theory-refutation on real agents.** The
  discovery shot did not land at this scale.

This does **not** promote the alignment-stability theorem from "confirmed in a toy built
from its own dynamics" (doc 12) to "confirmed on real agents." Doc 07's status is
unchanged: a derived theorem, self-consistent in simulation, **not yet validated on real
agent populations** — and now with a concrete, named reason the first real-agent attempt
was inconclusive (weak-g design window + high per-seed variance at N=20, 3 seeds).

## 5. The concrete next instrument (named, not fished)

A clean real-agent test of `V·g/γ` requires, and is gated on, a **fresh
pre-registration** with:
1. **A goal space where `g` can be strong without saturation** — continuous goals or
   K≫8 niches, so the reward-gradient can be varied over a wide range while staying in
   the non-dominated regime. (K=8 is the binding limit here.)
2. **More seeds (≥8–10) and/or larger N** to shrink σ_in until `R_across > 3·σ_in` is
   achievable — i.e. enough power to resolve the 2-vs-3 question that this run could not.
3. **A larger δ** for the direction perturbations (δ=0.05 was below the noise floor).
4. **Same bias control** (symbol-randomisation) and **same no-fishing rule** (no model
   escalation; the instrument is the design, not the model size).

Only with that instrument can the systematic-but-underpowered mean-trend seen here
(which leans toward falsifying `V·g/γ`) be resolved into a clean Outcome 1 / 2 / 3.

## 6. Honest limits of this test itself

- **Toy scale.** N=20, K=8, T=18, 1.5b. Not thermodynamic-limit, not a market.
- **Weak-g window.** K=8 saturation capped g ≤ 0.2; the gradient spread (≤1.4) is
  comparable to the J=1 dividend and below temperature noise. This is the dominant
  reason the scaling is not testable here, and it is a *design* limit (pre-stated), not
  a property of real agents in general.
- **High per-seed variance.** σ_in ≈ 0.56 on residuals ~3–4; 3 seeds give SEM ≈ 0.32.
  The frozen raw-std gate (2.63 < 3) lands on CAP; the SEM reading would not — disclosed
  in §2, resolved conservatively toward CAP by the committed rule.
- **Temperature ≠ OU noise.** As in rung 7, LLM sampling temperature perturbs the
  *response*, not the *perception* of payoffs; the V-maintaining noise is not the toy's σ.
- **Uniform resource weights.** V uses w=1/N; the theorem's V is wealth-weighted. No
  resource-accumulation mechanism here, so the two coincide only under equal payoff.
- **Reproducible.** All calls cached (`results/cache.sqlite`); pre-registered verdicts in
  `results/lever1_real.json`; the committed-discriminator analysis in
  `results/lever1_analysis.json`; per-seed grid in §1.

*Author byline: Cheng Qian. Pre-registration + addendum commit SHAs precede this
results commit — see git log.*

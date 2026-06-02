# PRE-REGISTRATION — Lever-1 real-agent test: residual = ‖Vg‖/γ on real LLMs

**Frozen before any experimental run.** Git commit of this file precedes the first
data collection. Thresholds, falsification criteria, and scope limits are stated here.
Author byline: Cheng Qian.

---

## 0. What is being tested and what would falsify it

The alignment-stability theorem (doc 07 §3) predicts that the fleet's residual
misalignment at the mean-field fixed point is

    ‖k̄* − k*‖ = ‖Vg‖ / γ                   ...(★)

where `k̄ = Σ_a w_a k_a` (wealth-weighted fleet goal), `V = Cov_a(k_a)` (goal
dispersion), `g = ∇_k G` (reward gradient), `γ` = control gain.

**The toy (doc 12) confirmed (★) as a self-consistency check (R²=0.999) in a
simulation built from the theorem's own dynamics.** That is a necessary first gate,
not a discovery. The discovery requires showing (★) on real LLM agents whose
decision dynamics are NOT derived from the theorem — agents that respond to rewards
and control signals for their own LLM-internal reasons.

**Rung-8 validation (real prerequisite check, bias-controlled):** two ingredients
of (★) are present on real 1.5b agents with per-agent symbol-randomisation:
  - agents respond to reward-gradient g: localized reward → adoption rate ~0.7
  - agents respond to control γ: external field lifts collective order m: 0.18 → 0.51

Flocking (spontaneous ordering without control) was NOT present — clean negative —
but Lever 1 does not need it. The bias-controlled harness is validated and reused.

**Falsification (frozen):**

  F-A: Prediction A fails — ratio residual/(V·g/γ) is directionally WRONG
       (lower γ gives lower or equal residual, OR lower g gives higher or equal
       residual) AND R² < 0.50. This is a quantitative falsification.
  F-B: Prediction B fails — at (γ=1, g=0.1), eff_g < eff_γ. The theorem predicts
       incentive design should WIN clearly here (endogenous-V theory: ratio ≈ 5).
       If oversight beats or matches incentive design at this clearly-in-zone point,
       the governance implication is falsified on real agents at this scale.
  CAP (not falsification): If the ratio variance is very high (std/mean > 1.0
       across conditions) and no monotone dependence on V·g/γ is detectable, the
       result is "not cleanly testable at this scale/design" — neither confirmation
       nor falsification. Report this honestly; do NOT escalate model size to fish.

An honest negative or "not testable" result is real output; it will be reported
in docs/13-incentive-vs-oversight-real.md with the same discipline as Rung 7.

---

## 1. System design (frozen)

**N = 20 LLM agents** in a shared niche economy. `K = 8` niches, target `k* = 0`.
Model: `qwen2.5:1.5b-instruct` (same as Rung 8; primary). Temperature = 0.6 (Rung 8
showed graded, coherent reward-following at this temperature). `T = 18` rounds
(`T_warm = 6`, `T_meas = 12`). Seeds `{0, 1, 2}` (3 seeds per condition).

**Instrument: per-agent symbol-randomisation (rung-8 guardrail, mandatory).**
Each agent sees niches under its own fixed random permutation of labels {0,..,7}.
Physics (goals, rewards, control) are measured in TRUE niche space. Token bias
cancels at the population level. This is the validated confound control from Rung 8.

**Reward structure:**
- Base gradient: `rewards[k] = g × k`  for `k ∈ {0,..,7}` (linear, off-target pays)
- Control: `γ` bonus at niche `k*=0` (via the existing LLMEconomy `gamma` parameter)
- Alignment dividend: `J = 1.0` (Rung-8 default; maintains goal diversity)
- Topology: annealed, `n_nb = 6` (mean-field; same as Rung-8 C1/C2 tests)

**Measurements (in TRUE niche space, after symbol-randomisation):**
- `k̄_t = (1/N) Σ_a k_a(t)` — fleet mean niche (linear scale)
- `V_t = (1/N) Σ_a (k_a(t) − k̄_t)²` — goal dispersion (uniform resource weights)
- `k̄_ss = mean over t ∈ [T_warm, T)` (averaged over T_meas rounds and seeds)
- `V_ss = mean over t ∈ [T_warm, T)` (averaged likewise)
- `residual_ss = k̄_ss − k*` (signed; should be positive for g > 0, k* = 0)
- `predicted_ss = V_ss × g / γ` (theorem prediction)

**Design scope and saturation note (pre-stated):**
With K=8 niches and a linear gradient `g × k`, the maximum gradient effect is
`g × 7` at niche 7. For g > γ / 7, niche 7 strictly dominates even the control-bonus
niche, and agents may saturate toward niche 7 (k̄ → 7, V → 0). The test is designed
to remain in the non-saturated regime by keeping g small (≤ 0.2) and γ ≥ 0.5. The
`oversight-wins` B-regime (γ < 2g by the endogenous-V account) requires g > γ/2 ≥ 0.25,
which enters the saturation regime in this K=8 system — **not testable at this scale
and design without a broader niche range.** This is a pre-stated design limitation,
not a post-hoc excuse.

---

## 2. Prediction A — quantitative match: residual_ss ≈ V_ss · g / γ

**Grid:** γ ∈ {0.5, 1.0, 2.0} × g ∈ {0.1, 0.2} — 6 conditions, 3 seeds each.

Rationale for scales: g = 0.1 → max gradient effect R_7 = 0.7, comparable to γ = 0.5–2.0.
g = 0.2 → max R_7 = 1.4. Both keep the non-dominated control regime.
γ ∈ {0.5, 1.0, 2.0} spans the 4× range the toy used (§2 of doc 12) but at smaller values
due to the K=8 niche range.

**PRE-REGISTERED THRESHOLDS (real-agent tolerances, deliberately loose):**

| Check | Condition | Threshold | Rationale |
|---|---|---|---|
| A1 proportionality | log-log OLS of residual_ss ~ V_ss·g/γ | slope ∈ [0.60, 1.60], R² ≥ 0.70 | Real-agent noise; N=20, 3 seeds |
| A2 ratio | mean(residual_ss / (V_ss·g/γ)) | ∈ [0.50, 2.00] | Discrete K=8 niches, non-OU dynamics |
| A3 direction | residual_ss decreases as γ increases (fixed g) | monotone for ≥ 2/3 γ-pairs | Weakest directional test |

If R² < 0.50 AND no monotone dependence on V·g/γ — report CAP: "not cleanly testable
at this scale." If R² < 0.70 BUT monotone dependence holds — report directional
confirmation only (not quantitative). If slope or mean ratio outside threshold but
monotone — report partial confirmation with explicit scope.

---

## 3. Prediction B — marginal efficiency: incentive-wins zone (γ ≫ 2g)

**Two operating points, both firmly in the incentive-wins zone:**

| ID | γ | g | Endogenous-V theory ratio eff_g/eff_γ | Zone |
|---|---|---|---|---|
| B1 | 1.0 | 0.1 | γ/(2g) = 5.0 | Incentive wins |
| B2 | 2.0 | 0.1 | γ/(2g) = 10.0 | Incentive wins (stronger) |

Perturbation: δ = 0.05. Seeds: {0, 1, 2}. Signed-residual version:
  `eff_γ = (r0 − r(γ+δ, g)) / δ`
  `eff_g = (r0 − r(γ, g−δ)) / δ`

**PRE-REGISTERED THRESHOLDS:**

| Check | Condition | Threshold |
|---|---|---|
| B1 incentive wins | (γ=1.0, g=0.1): eff_g/eff_γ | > 1.0 |
| B2 incentive wins | (γ=2.0, g=0.1): eff_g/eff_γ | > 1.0 |
| B_mono | ratio(B2) ≥ ratio(B1) | weakly monotone |

**Oversight-wins zone NOT TESTED** (see §1 saturation note). Explicitly pre-stated.

**Falsification trigger for B:** if eff_g / eff_γ < 1 at (γ=1, g=0.1) — where the
endogenous-V theory predicts a ratio of ~5 — the governance implication is falsified.

---

## 4. Honest limits (stated before any run)

1. **Discrete goals.** Real agents choose from K=8 niches (integers), not a continuous
   ℝ. The mean k̄ is continuous but the individual goals are not. The linearized ODE
   that underpins (★) is an approximation on the discrete lattice.
2. **Uniform resource weights.** V is computed with w_a = 1/N (equal resources).
   The theorem uses wealth-weighted V; without a resource-accumulation mechanism,
   the two coincide only if all agents have equal accumulated payoff.
3. **J=1 alignment dividend.** The coordination pressure from J=1 may alter
   V_ss relative to the OU baseline. This is analogous to the endogenous-V finding
   in the toy — the actual V_ss is measured, not assumed.
4. **Small N and T.** N=20, T_meas=12, 3 seeds → effective sample size ≈ 720
   per condition. k̄_ss has std ≈ sqrt(V/720) ≈ 0.08–0.10. For small predicted
   residuals (g=0.1, γ=2.0: predicted ≈ 0.26), the SNR is ~2–3. Marginal.
5. **Temperature as noise knob.** LLM sampling temperature is not OU noise.
   It affects the model's *response* to perceived payoffs, not the *perception*
   of payoffs. The "noise" that maintains V is not the same as σ in the toy.
6. **No V evolution mechanism.** The toy had explicit noise σ driving V;
   here V is maintained by LLM stochasticity. The mapping V_toy ↔ V_real is
   approximate.
7. **Not a market.** N=20 toy-scale. No real stakes. The result is about whether
   the theorem describes SMALL LLM AGENT POPULATIONS, not real-world systems.

---

## 5. Cache and reproducibility

Every LLM call is cached in `results/cache.sqlite` by
`(model, temp, seed, agent, round, prompt)`. Runs with the same parameters are fully
deterministic given the cache. Results written to `results/lever1_real.json`.
All calls use `qwen2.5:1.5b-instruct` via the China-Mac Ollama tunnel
(`ssh -f -N -L 11434:localhost:11434 blueidea@MacBook-Pro.local`).

*Pre-registration commit SHA precedes results commit SHA — see git log.*

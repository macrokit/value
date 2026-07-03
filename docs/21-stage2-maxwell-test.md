# The Maxwell Test on Frontier Agents — Stage 2: half the displacement current is CONFIRMED; the other half finds no domain

> **Maxwell program, Stage 2** — the experiment the v5 paper names as its continuation
> gate. Pre-registered chain, every link committed before the results it governs:
> grid prereg `4c0a7a1` → A2 `c79f8fe` → instrument `2b2c010` → A3 `9d685f8` →
> 2A results `f8b902d` → this. Instrument: `claude-opus-4-8` (gate-proven, docs/19),
> 104 grid runs + full elicitation + live markets, **parse = 1.000 in all 104 runs**,
> total metered spend **$138.76 of the $160 cap** (gate + debug + 2A + 2B inclusive).
>
> **Verdicts, stated plainly (frozen rules applied mechanically):**
> **Prediction (i) — the coupled capacity region: CONFIRMED within its frozen bands
> on real frontier agents** (P1 gap law, P2 submodularity, P2e synergy control, P3
> ceiling all PASS; P4a selection PASS; P4b clone equality is a real, disclosed miss
> on a supporting check). This is the first real-agent confirmation of a
> distinctively-coupled-regime prediction of the unified theory.
> **Prediction (ii) — the ‖Vg‖/γ residual scaling: P5 = CAP** ("insufficient
> in-regime span: **0 of 9** conditions") — by a **third, new mechanism**: frontier
> populations hold **no dispersion** (V → 0 everywhere). **P6 = INCONCLUSIVE** by the
> frozen floor rule. The formal whole-experiment outcome under §4's letter is
> therefore **outcome 3 (CAP)** — rule 1 requires P5 — with the split above reported
> exactly as it fell.

## 0. The system and its provenance

The frozen designs of `sim/stage2/PREREGISTRATION.md` + amendments 1–3 (each
committed before the runs it governs; A1 = provider rejects temperature; A2 = two
internal spec inconsistencies fixed blind; A3 = protocol faults caught by the frozen
§5 gates, traced in the cache, corrected, and re-run **scoped to the faulted
components only** — passed data was never re-rolled). Every call cached and
cap-metered. Mid-run the 2B grid was migrated from the local machine to a cloud host
(owner hardware shutdown): the SQLite call cache replayed all completed runs at zero
cost — the restart-safety design carried a live experiment across machines. A ~3-run
overlap window during the handover was double-sampled; the remote data is the data
of record (disclosed; the overlapping local partials were discarded).

## 1. Prediction (i) — the coupled capacity region on real agents: CONFIRMED

| Check | Frozen band | Result | |
|---|---|---|---|
| **P1 gap law** `Ĝ_a − Ĝ_b = Î_a − Î_b` (parimutuel, all pairs, 4 structures) | ≤ 0.05 nats | worst **0.0457** | **PASS** |
| **P2 submodularity** of coalition value (a)–(d) | margins ≥ −0.03 | worst **−0.019** | **PASS** |
| **P2e XOR synergy control** — submodularity must FAIL | gap ≥ ln2/2 = 0.347 | **0.621** | **PASS** |
| **P3 joint ceiling** `Ĝ_S ≤ H(X)` | slack 0.02 | worst overage **−0.000** | **PASS** |
| **P4a wealth selection** (live market, BSC ladder) | ordered by `Î` in ≥ 4/5 | **4/5**, clean sensor absorbs the pool | **PASS** |
| **P4b clone equality** (live market) | gap ≤ 10% in ≥ 4/5 | 2/4 scoreable (+1 nan seed) | **FAIL** (real, supporting) |

Read together: on real frontier agents, **relative growth under market coupling
equals claimed information difference to within 46 millinats**; coalition value shows
the predicted diminishing returns; and the designed control — a channel pair whose
individual signals are worthless but jointly worth one bit — flips coalition value to
supermodular almost exactly as the theory requires (0.62 of the ideal ln 2, achieved
by the agents *reasoning out the XOR*). The joint ceiling holds exactly. In the live
market, the best-informed agent absorbs essentially the entire pool (Kelly selection
at its sharpest). None of these is predicted by Kelly portfolios, classical control,
or welfare economics taken separately — this is the coupled-regime structure the
unification claimed, measured on real agents.

**The honest misses in (i):** P4b — clones (identical signals) diverge in terminal
wealth (gaps 1.0/0.5/0/0): at provider-default sampling temperature with fully-sharp
all-in bets, a single divergent-sample round is absorbing. One seed was unscoreable
(no bettor on the realised outcome → undefined pool — a harness edge case,
disclosed). Protocol history: the first 2A pass had genuine instrument faults (36%
market parse; a self-contradictory control prompt); the frozen gates caught them, A3
scoped the re-run, and the corrected protocol achieved parse 1.00. Secondary
diagnostic as pre-registered: naive-Bayes product fusion tracks coalition-level
value imperfectly (max dev 0.466 — elicited joint posteriors are not the product of
elicited singletons even where conditional independence holds) and returns ~0 for
the synergy pair — the independence precondition is load-bearing at the fusion
level, exactly as amended.

## 2. Prediction (ii) — ‖Vg‖/γ: no linear-response regime exists (third mechanism)

The frozen grid, all 9 conditions, 8 seeds each:

| γ | g | residual (±seed std) | V_ss | verdict of the regime rule |
|---|---|---|---|---|
| 2 | 0.25 | 10.22 ± 4.74 | 0.46 | excluded (V collapsed; at peak) |
| 2 | 0.70 | 11.94 ± 1.51 | 0.56 | excluded (V collapsed; at peak) |
| 2 | 2.00 | 12.04 ± 1.59 | 0.70 | excluded (V collapsed; at peak) |
| 6 | 0.25 | **0.000 ± 0.000** | 0.00 | excluded (V collapsed; residual ≤ 0) |
| 6 | 0.70 | 10.59 ± 4.45 | 0.96 | excluded (V collapsed; at peak) |
| 6 | 2.00 | 11.92 ± 1.52 | 0.73 | excluded (V collapsed; at peak) |
| 18 | 0.25 | **0.000 ± 0.000** | 0.00 | excluded (V collapsed; residual ≤ 0) |
| 18 | 0.70 | **0.000 ± 0.000** | 0.00 | excluded (V collapsed; residual ≤ 0) |
| 18 | 2.00 | 10.56 ± 4.39 | 1.41 | excluded (V collapsed; at peak) |

**P5 = CAP ("insufficient in-regime span: 0/9").** Across all 72 grid runs the
maximum dispersion was **V = 4.85** (median **0.00**) against the frozen floor 5.31
and the uniform reference 21.25. No condition triggered the uniformity
(non-response) clause either: this is not Stage 1's failure. The population
*always* concentrates: on the target when control dominates (γ exceeds the peak
payout 12g — three conditions at exactly 0.000 ± 0.000 across all 8 seeds), on or
near the peak when incentive dominates, and **bistably** (seed-by-seed corner
selection, e.g. per-seed residuals `[9.9, 13.0, 13.0, 12.0, 14.6, 0.3, 9.9, 12.0]`)
when the two attractors are comparable. Within-seed clusters sit 1–3 niches off the
exact peak (9.9 / 13 / 14.6) — the pre-stated J-granularity systematic, seed-persistent.

**The three-instrument bracket is now complete.** The theorem's mean-field regime
requires noise-maintained dispersion (`V ≫ 0` sustained under selection and control):
- 1.5B, K=8 (doc 13): **saturation** — gradient window below the noise floor;
- 1.5B, K=16 (doc 18): **non-response** — V ≈ uniform, no attractor felt;
- **frontier (this)**: **concentration** — V → 0, pure attractor competition;
  response to (g, γ) is a **step function** across the reward-dominance boundary
  (`γ ⋛ 12g`), not a power law in the levers.

Too noisy to respond, or too decisive to disperse — no tested real LLM population
holds the intermediate dispersion the derivation assumes. The `‖Vg‖/γ` law remains
**neither confirmed nor falsified on real agents** (with V→0 the theorem's own
prediction degenerates to 0 and the observed corner residuals live outside its
stated linear-response domain); what the program has now established is sharper:
**the domain of the mean-field dynamical layer appears to be empty for real
LLM-agent populations at every capability level tested.**

**P6 = INCONCLUSIVE** by the frozen rule — with zero in-regime conditions the noise
floor `σ_in·√(2/8)` is undefined, so no arm is formally "resolvable" (the rule's
letter; disclosed). The exploratory reading is dramatic and direction-consistent:
at B1, lowering g by 0.5 flipped the population from the peak corner to **perfect
alignment in 8/8 seeds** (10.59 → 0.000 — the incentive lever crossed the dominance
boundary), while raising γ by 0.5 did nothing (10.59 → 12.08, bistability noise).
Incentive design didn't marginally beat oversight; it **switched the attractor**.
Reported as exploratory only.

## 3. What this does to the continuation gate

The v5 paper's printed rule: *predictions pass → the unification earns the stronger
word; fail or remain unresolvable → the distinctively-unified layer retires.* The
result splits the displacement current exactly down its seam:

- **The static/coupled half (prediction i) passed** its frozen bands on real capable
  agents. The gap law, conditional submodularity with its synergy control, the joint
  ceiling, and Kelly selection are now measured properties of a real coupled
  LLM-agent economy — the unification's distinctive coupled-regime structure held
  where it was tested.
- **The dynamical half (prediction ii) remains unresolvable on a proven-capable
  instrument** — and the reason is now attributable to the theory, not the
  instrument: the mean-field layer's standing assumption (noise-maintained goal
  dispersion) has no realisation in any tested LLM population. Three CAPs by three
  distinct mechanisms bracket the assumption from all sides. Unless a future,
  pre-registered design *creates* sustained dispersion (explicit exploration
  incentives, heterogeneous objectives — at which point one is testing a modified
  theory and should say so), the honest status of `‖Vg‖/γ` as a real-agent law is:
  **domain not found; retire the claim to its toy/mathematical scope** (doc 12's
  self-consistency, doc 07's derivation) and update the paper's decisive-prediction
  paragraph accordingly in the next version — the (i)-confirmed / (ii)-domain-empty
  split stated in full.

## 4. Honest limits

- **Single model family and provider**; one frontier tier. Replication elsewhere is
  open. Elicited beliefs are unincentivised statements; the live market partially
  covers the acting-vs-stating gap at small scale.
- **P4b is a real miss** of a supporting prediction, with a named mechanism
  (sampling variance + absorbing all-in dynamics) and one harness-undefined seed.
- **Protocol history in full view:** three amendments after the freeze, every one
  committed before the runs it governed, every one forced by a provider constraint,
  an internal inconsistency, or a gate-caught fault — the record is in the chain,
  and pre-registered vs exploratory is separated throughout this document.
- **The P6 floor is definitionally tied to in-regime σ**, which a zero-in-regime
  grid leaves undefined — a prereg drafting gap, disclosed rather than papered over.
- **Migration**: one machine handover mid-grid (cache-replayed, ~3 runs
  double-sampled, remote data of record).
- 2B inherits the standing toy-scale caveats (N=20, T=18, uniform resource weights,
  prompt-γ calibration absorbed into the fit constant).

## 5. Verdict of record

**Formal outcome (frozen §4 rule, applied in order): outcome 3 — CAP**, named gate
"P5 insufficient in-regime span (0/9; dispersion collapse)". Within that:
**P1, P2, P2e, P3, P4a PASS their frozen bands — prediction (i) is confirmed within
scope on real frontier agents**; P4b fails (supporting, disclosed); P5 CAP by the
dispersion-collapse mechanism; P6 formally inconclusive with the attractor-switching
exploratory reading stated as such. Total program spend for the entire Stage 2
including the gate: **$138.76 metered** (< the $160 cap; ≈ the calibrated real
prices). All numbers re-derive offline from `sim/stage2/results/` (cached,
auditable); the analyzer applies the frozen bands mechanically
(`sim/stage2/analyze_stage2.py`).

*Author byline: Cheng Qian. The pre-registration chain (grid prereg, amendments 1–3,
2A results) provably precedes this results commit — see git log.*

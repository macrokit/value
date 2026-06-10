# The v2 Empirical Scale-Up — From Demonstration Toward Validation

> [`06`](06-real-agent-test.md) tested the value laws on **one task, four models** — a demonstration, not a
> validation (an external review scored its rigor 6.5/10). This doc scales that test along the three axes that
> were binding: **(A) one task → three domains**, **(B) four models → a ten-model cross-family ladder** (so R1
> is a regression, not four points), and **(C) the homogeneous fleet R5 → a heterogeneous, cost-constrained
> fleet raced against a *strong* hand-tuned router.** Everything was **pre-registered before any model ran**
> ([`sim/real/v2/PREREGISTRATION.md`](../sim/real/v2/PREREGISTRATION.md), committed frozen; v1's "pre-registered"
> was an overclaim we corrected — here the word is earned). Results are reported against that frozen document,
> negatives included.

> **v2 result (10 models × 3 domains, 240 items each, 95% CIs).** The bridge **generalizes**: pooled across 30
> model×domain points, `I(X;Y)` tracks realized capability at **Spearman ρ = 0.977** (CI [0.916, 0.996]) and
> out-of-sample `ΔG` tracks `I` with **slope 0.935** (CI [0.915, 0.954]). The Second Law **generalizes**:
> over-confidence dissipates value in **every** domain, driving the weakest models sharply **negative**. The
> fleet ceiling holds (`Σ`-throughput ≤ `H(X)`) and diverse specialists beat redundancy in every domain. The
> **headline, scoped honestly:** a value-price router (`∝ I_a/cost_a`) **beats the naive baselines**
> (round-robin, equal-weight) on all cost metrics — so the governance claim is non-empty. On the pre-registered
> **primary cost (tokens)** it **ties** the strong cost-blind hand-tuned router (token cost is ~uniform, so
> cost-aware routing reduces to quality-first). A **post-hoc sensitivity analysis** on two cost proxies that *do*
> express the compute gradient — wall latency and a hardware-**independent** active-params×tokens (∝ FLOPs) — finds
> value-price **beats the cost-blind router on both** (FLOP-proxy Δ = +7.45, CI [6.33, 8.48]): the cost-aware win
> is **robust across cost metrics**, not metric-shopping. Against a *cost-aware* engineer (accuracy/cost) it is
> edged out under latency but **exactly ties** under the principled FLOP proxy — it **matches, never beats** it.
> The theory's contribution is thus precise: it **derives cost-aware routing from first principles**, dominating
> cost-blind allocation and recovering a cost-aware heuristic — principled measurement, not outperformance.

## 1. Method (what changed from v1)

**Output protocol.** v2 uses **plain text-label output**, not the tool-call API that produced v1's plumbing
artifacts. Every model on the ladder runs every domain; a response that parses to no valid label is a distinct
`?` error class (counted as an error, never silently dropped). This also lets us re-include Mistral (its v1
exclusion was a tool-call incompatibility that does not apply to text output).

**Domains (Axis A).** Three public, abstractly-described tasks, each with the v1 structure (ground-truth label
over `K` classes; the model's text output *is* its label):

| Domain | K | Source | n |
|---|---|---|---|
| intent routing | 6 | CLINC150, a confusable assistant-router slice | 240 |
| multiple-choice QA | 4 | MMLU-style, mixed subjects (A/B/C/D) | 240 |
| topic classification | 4 | AG News (world/sports/business/sci-tech) | 240 |

**Ladder (Axis B).** Ten models across **five families** and ~0.5B→8B: Qwen2.5 (0.5/1.5/3/7B), Llama (3.2-1B,
3.2-3B, 3.1-8B), Gemma2-2B, Phi-3.5, Mistral-7B. Capability proxy = per-(model, domain) accuracy. (One model,
Phi-3.5, threw HTTP-500s mid-run from a concurrent-load OOM on the 16 GB host; diagnosed in isolation as a
*serving* failure, fixed by evicting each model between batches, the partial artifact cleared and re-run — **not**
recorded as low capability. A text-output degraded-model guard, >50% unparseable ⇒ excluded as plumbing, was in
place; nothing tripped it post-fix, max unparse rate 6%.)

**Statistics (Axis D).** Calibrated posteriors and all routing weights are fit on a seeded 50/50 fit split and
scored out-of-sample on the holdout. Point estimates carry **95% CIs** (2000-sample bootstrap). All quantities
in nats via [`sim/value_sim.py`](../sim/value_sim.py); all model outputs cached so every number re-derives
offline.

> **Statistical corrections (2026-06-07, after external review).** Two issues were flagged and fixed.
> **(a) Clustering.** The 30 pooled points are 10 models × 3 domains — clustered by model — and the original
> bootstrap resampled them i.i.d., which is anti-conservative (effective n ≈ 10). The harness now also reports
> a **cluster bootstrap by model**; re-run on the cached data, the conclusions are unchanged: R1a pooled ρ =
> 0.977 with clustered CI **[0.943, 0.995]**, R1b slope = 0.935 with clustered CI **[0.914, 0.956]** — both
> still clear their registered thresholds. **(b) Threshold disclosure.** The code's original pass condition
> added an unregistered `CI-low > 0.5` check alongside the registered `ρ > 0.8`; the registered criterion alone
> now decides the verdict and the extra check is reported as the unregistered diagnostic it is (it passes
> either way here, but the deviation should have been disclosed).

## 2. R1-v2 — the capacity bridge generalizes  ✅ PASS

Across all 30 model×domain points, mutual information tracks realized capability, and out-of-sample value-growth
tracks mutual information:

- **Pooled Spearman(`I`, accuracy) = 0.977**, 95% CI [0.916, 0.996] (threshold > 0.8). Per-domain ρ = **0.842**
  (intent), **0.952** (mcqa), **0.988** (topic) — all clear the > 0.6 per-domain bar.
- **Slope of `ΔG_holdout` on `I` = 0.935**, 95% CI [0.915, 0.954] — excludes 0, and is ≈ 1, i.e. realized
  out-of-sample value-growth *is* perceived mutual information.

The cross-family points sharpen the v1 reframe ("`I` tracks capability, not parameter count"): Phi-3.5 is strong
on MMLU (acc 0.53 → `I` 0.19) but weak on topic (0.30 → 0.09); Llama-3.1-8B is the reverse (topic 0.80 → 0.82).
Size does not predict `I`; *capability on the task* does.

## 3. R2-v2 — the Second Law generalizes  ✅ PASS

Reading the same predictions with a calibrated vs an over-confident posterior, realized value drops in **every**
domain (minimum dissipation: intent +0.42, mcqa +5.91, topic +3.53 nats). The effect is dramatic in the
low-`I` domains: a weak model that is *confidently* wrong on MMLU or topic drives realized growth strongly
**negative** (e.g. −11 nats on MMLU, −14 on topic) — confident error is catastrophic value destruction, exactly
the prediction of [`02`](02-coding-theorem-of-value.md) §4, now shown across three task shapes.

## 4. Fleet-R5 — the heterogeneous, cost-constrained headline

The fleet is **specialized by domain competence** (different models lead on different domains), so on a mixed
360-query holdout stream their per-item errors are far less correlated (mean pairwise error-agreement **0.750**)
than v1's same-task generalists. Under a compute budget we race six routing policies on realized
**value per unit cost**, with two pre-registered cost units (tokens primary; latency secondary):

| Policy | value / 1k tok *(primary)* | value / 10s latency | value / compute *(params×tok, ∝FLOPs)* |
|---|---|---|---|
| equal-weight pool | +0.57 | +1.94 | +0.16 |
| round-robin | +5.01 | +17.08 | +1.36 |
| best-single | +6.18 | +13.30 | +0.88 |
| hand-tuned (best accuracy/domain, **cost-blind**) | +6.67 | +15.54 | +1.15 |
| **value-price** (`∝ I_a/cost_a`) | **+6.67** | **+21.85** | **+8.61** |
| hand-tuned cost-aware (best accuracy/cost) | +6.67 | +43.78 | +8.61 |

**Required win — PASS (all metrics).** value-price beats round-robin (tokens Δ = +1.66 CI [1.03, 2.25]; latency
Δ = +4.81 CI [1.88, 7.79]; compute Δ = +7.25 CI [6.07, 8.29]) and equal-weight (all CIs exclude 0). The
governance claim is **non-empty**: pricing strictly beats naive allocation, out-of-sample.

**Strong win vs the cost-blind hand-tuned adversary — primary tie, robust on real cost gradients.**
- **Primary (tokens) — tie.** Δ = 0.0000: token cost varies only ~1.2× across the ladder, so `I_a/cost_a` ranks
  models the same as `I_a`, which (R1) ranks them as accuracy does — value-price and the quality-first hand-tuned
  router pick the *identical* model in every domain. When compute is nearly free per token, cost-aware pricing
  correctly reduces to quality-first. A **FAIL** of the strict strong-win threshold, recorded as a tie, not
  rounded up.
- **Sensitivity analysis (post-hoc, cache-only, *not* pre-registered).** A token budget cannot express the real
  cost gradient. We re-score on two cost proxies that do, *without re-running any model*: wall **latency**
  (5–6×, hardware-dependent) and **active-params × tokens** (∝ FLOPs ∝ energy; ~16×; hardware-*independent* — the
  principled compute cost, which answers any "you picked the metric that won" objection). value-price beats the
  cost-blind router on **both**: latency Δ = +6.42 CI [3.92, 9.22]; **compute Δ = +7.45 CI [6.33, 8.48]**. The
  cost-aware win is therefore **robust across cost metrics**, not an artifact of one.

**Relationship to a cost-aware engineer (honest, and it improves under the principled proxy).** A hand-tuned
router that *itself* prices cost (best accuracy/cost) edges out value-price under **latency** (+43.8 vs +21.8) —
but under the principled **FLOP** proxy value-price **exactly ties** it (Δ = 0.0000): `I_a/compute` and
`accuracy_a/compute` select the same model, because `I` tracks accuracy (R1). So value-price **matches** the
cost-aware engineer under the hardware-independent metric and never beats it. The contribution is precise:
`I_a/cost_a` pricing **derives cost-aware routing from first principles** — it dominates *cost-blind* allocation
robustly, and *recovers* (matches, does not outperform) a cost-aware heuristic. Pricing's value is cost-awareness
itself, obtained as a law rather than hand-built.

**Ceiling & diversity — PASS.** All pairwise joint `I(X; Y_a, Y_b) ≤ H(X)` (the data-processing bound holds
empirically in every domain), and the best diverse specialist pair lifts joint `I` over the best single model in
every domain (+0.095 intent, +0.132 mcqa, +0.134 topic), approaching `H(X)`.

## 5. Scorecard against the frozen pre-registration

| Pre-registered check | Verdict |
|---|---|
| **R1-v2** ρ(`I`, acc) > 0.8 pooled + per-domain; `ΔG~I` slope CI excludes 0 | **PASS** (ρ = 0.977; slope 0.935) |
| **R2-v2** over-confidence dissipation > 0 in every domain | **PASS** |
| **Fleet-R5 required** value-price > round-robin AND equal-weight | **PASS** (all three cost metrics) |
| **Fleet-R5 strong** value-price > cost-blind hand-tuned | **primary (tokens): tie (FAIL)** · sensitivity (latency + FLOPs): **PASS, robust** — reported honestly |
| **Ceiling** `Σ`-throughput ≤ `H(X)`; diverse > redundant | **PASS** |

The publication gate (prereg §4: R1-v2 ∧ R2-v2 ∧ Fleet-R5-required all PASS) is **met**.

## 6. Where this breaks (scope honesty)

- **Tokens are a weak compute-cost proxy here.** Same prompt + one-token answer ⇒ token counts vary only ~1.2×
  across a 0.5B→8B ladder, so a *token* budget cannot express the real cost gradient and cost-aware routing
  collapses to quality-first (the primary tie). The meaningful budget is compute, not tokens.
- **The cost-aware win is a post-hoc sensitivity analysis, and robust.** It was *not* pre-registered: we re-score
  cache-only on two cost proxies that express the compute gradient — wall latency (hardware-dependent) and
  active-params × tokens (∝ FLOPs, hardware-*independent*) — and value-price beats the cost-blind router on
  **both** (CIs exclude 0). Reporting two metrics, one principled and hardware-independent, is what defuses the
  "you picked the metric that won" objection; we still lead with the pre-registered token tie.
- **Latency had to be load-corrected.** The OOM fix (evicting models between batches) injected one-time
  model-*load* time into the first call of each batch; the mean would be biased unevenly (bigger models load
  slower). We use **median** per-call latency (load-robust) — a disclosed measurement-artifact correction, not a
  goalpost move. The FLOP proxy (params × tokens) has no such issue (counts only), and carries the same verdict.
- **The win is bounded, and we do not overstate it.** value-price beats *cost-blind* hand-tuning and **matches**
  (ties under the principled FLOP proxy, is edged out under raw latency) a *cost-aware* hand-tuned heuristic — it
  never **outperforms** the cost-aware engineer. The claim is "pricing = cost-awareness derived from first
  principles," not "pricing beats every engineer."
- **Calibration is constructed,** as in v1 (models emit hard labels, not probabilities); the R2 dissipation is
  that of a stated belief over those predictions.
- **Three domains, ten models** is materially stronger than v1's one-and-four, but still narrow versus the space
  of tasks and models; the laws are shown to generalize *here*, not proven universal.

## 7. What this establishes

The v1 result was a demonstration; v2 is evidence of **generalization**. The capacity bridge (`ΔG ∝ I(X;Y)`) and
the Second Law (over-confidence = dissipation) hold across three task shapes and a ten-model cross-family ladder,
as pre-registered regressions with confidence intervals. The governance claim is validated as **non-empty**:
priced routing beats naive allocation out-of-sample. And the headline fleet result is reported with its exact
scope — pricing's edge is **cost-awareness under a compute budget**, dominating cost-blind allocation, bounded by
a cost-aware engineer. That boundary is the result, not a disappointment: a theory that says precisely where its
advantage lies is the one worth governing agents with.

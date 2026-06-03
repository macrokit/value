# Is `ΔG = I(X;Y)` a LAW Across Task Shapes? — the Cross-Shape Generalization Test

> **LEVER 2.** v2 (`docs/09`) generalized the capacity bridge `ΔG ∝ I(X;Y)` across **3
> domains × 10 models** — but all three domains were the same task *shape*: pick-a-label
> classification. This rung tests whether the *same* relationship holds across
> qualitatively different task **shapes**, using only **discrete-gold** generative/agentic
> tasks so the exact confusion-matrix `I` machinery applies (no soft embedding-MI;
> open-ended generation deferred as the hard frontier).
>
> Pre-registered in [`sim/real/shapes/PREREGISTRATION_lever2.md`](../sim/real/shapes/PREREGISTRATION_lever2.md)
> (frozen before any run; SHA precedes results). Reuses v2's exact pipeline.
>
> **Result (final at the pre-registered ≥6-model minimum; 8-model extension blocked by
> hardware — §5): the out-of-sample bridge `ΔG ~ I` generalizes across all three new
> shapes and is consistent with classification** — pooled slope **0.956**,
> cross-shape-with-classification slope **0.953** (≈ v2's 0.935), ρ **0.924**.
> `I`-tracks-capability holds cleanly for **reasoning** and **sequential/agentic** shapes;
> for **code** it is **underpowered** (compressed capability spread at ≤3B), not a clean
> break. **11/12 frozen checks pass.** The strict full-LAW verdict (every shape passes
> *both* checks) is **not met**: code's `I`-vs-capability sub-check is underpowered, and
> the pre-registered remedy (adding the 7B/8B models to widen code's range) **could not be
> run** — those models stall on the 16 GB China-Mac host at 512-token CoT (§5). Reported
> honestly as a strong-generalization-with-one-underpowered-sub-check, not forced.

## 0. System (identical pipeline to v2)

For each (model, shape): discrete gold `X`, model's discretised outcome `Y`, `I(X;Y)`
from the confusion matrix (nats); capability = accuracy; **out-of-sample** `ΔG_holdout` =
mean `ln p(x|y)/r(x)` with `p(x|y)` calibrated on a seeded 50/50 fit split, `r = q`
(empirical marginal). Same `confusion`/`calib`/`per_item_value`/bootstrap as
`sim/real/v2/experiments_v2.py`. Three new shapes, each a genuinely different task shape
with discrete gold:

| shape | task | free-form output | discrete gold | K |
|---|---|---|---|---|
| **reason** | GSM8K | chain-of-thought → integer | gold answer mod 4 | 4 |
| **seqstate** | synthetic register-machine rollout | step-by-step trace → final state | exact final value mod 6 | 6 |
| **code** | MBPP | a Python function | sandbox-executed output, hash mod 4 | 4 |

8-model ladder pre-registered (0.5B→8B, 3 families); **this report covers the 6 completed
models** (qwen0.5b, llama1b, qwen1.5b, gemma2b, qwen3b, llama3b — the pre-registered ≥6
minimum); qwen7b + llama8b **could not be run** on the available host (§5). Code executed in a restricted
sandbox on the China Mac (off the main Mac); 5 s timeout, blocked imports. Parse/exec
rates within the ≤50% degraded guard for every point.

## 1. Per-shape results (L2-a Spearman(I,acc)>0.70 ; L2-b out-of-sample slope(ΔG~I) CI excl 0)

### reason (GSM8K) — PASS / PASS
| model | acc | I | ΔG_hold |
|---|---|---|---|
| qwen0.5b | 0.66 | 0.340 | 0.316 |
| llama1b | 0.66 | 0.330 | 0.181 |
| gemma2b | 0.73 | 0.456 | 0.288 |
| qwen1.5b | 0.79 | 0.608 | 0.453 |
| llama3b | 0.85 | 0.733 | 0.617 |
| qwen3b | 0.91 | 0.887 | 0.750 |

L2-a Spearman(I,acc) = **0.943** CI[0.657,1.000] ✓ · L2-b slope(ΔG~I) = **0.936**
CI[0.571,1.113] ✓ · info-floor: I≈0.559 ≫ 3×null(0.027) ✓.

### seqstate (sequential/agentic rollout) — PASS / PASS
| model | acc | I | ΔG_hold |
|---|---|---|---|
| llama1b | 0.45 | 0.374 | 0.107 |
| qwen0.5b | 0.46 | 0.329 | 0.141 |
| gemma2b | 0.67 | 0.781 | 0.615 |
| qwen3b | 0.88 | 1.339 | 1.164 |
| llama3b | 0.93 | 1.563 | 1.343 |
| qwen1.5b | 0.94 | 1.555 | 1.379 |

L2-a Spearman = **0.886** CI[0.429,1.000] ✓ · L2-b slope = **1.023** CI[0.942,1.088] ✓ ·
info-floor: I≈0.990 ≫ 3×null(0.094) ✓. The widest `I` range of the three shapes (0.33→1.56
nats) — the synthetic difficulty produced a clean capability spread, as intended.

### code (MBPP) — FAIL (L2-a, underpowered) / PASS (L2-b)
| model | acc | I | ΔG_hold |
|---|---|---|---|
| llama1b | 0.35 | 0.258 | 0.132 |
| qwen0.5b | 0.38 | 0.231 | 0.090 |
| gemma2b | 0.42 | 0.315 | 0.160 |
| qwen1.5b | 0.42 | 0.282 | 0.152 |
| qwen3b | 0.45 | 0.257 | 0.134 |
| llama3b | 0.47 | 0.294 | 0.229 |

L2-a Spearman = **0.429** CI**[−0.429, 1.000]** ✗ · L2-b slope = **1.133** CI[0.392,2.468]
✓ · info-floor: I≈0.273 > 3×null(0.066) ✓.

**The L2-a miss is underpowered, not a break.** The 6 small models cluster at code-acc
0.35–0.47 (range 0.115, just above the CAP floor) — a compressed capability spread on
MBPP at ≤3B. The Spearman CI [−0.43, 1.0] spans almost the whole range: the rank
correlation is *noise-dominated/inconclusive*, not a confident "I fails to track
capability." Crucially, the **bridge itself** (out-of-sample `ΔG ~ I`, L2-b) **passes** for
code — `ΔG` tracks `I`. This is the regime the pre-registration's CAP clause anticipated
(no clean capability spread ⇒ Spearman undefined/noisy), and exactly what the 8-model
extension (qwen7b, llama8b — far stronger coders) should resolve by widening the range.

## 2. Pooled and cross-shape (the law claim)

- **L2-c pooled across all 3 new shapes (n=18):** slope(ΔG~I) = **0.956** CI[0.920, 1.001]
  ✓ — within [0.5,1.5] and CI excludes 0. The out-of-sample bridge holds when reasoning,
  sequential, and code points are pooled.
- **L2-d cross-shape including v2's 3 classification domains (n=42):** Spearman(I,acc) =
  **0.924** CI[0.825, 0.967] ✓ ; slope(ΔG~I) = **0.953** CI[0.925, 0.979] ✓. The bridge
  is one relationship across **four task shapes** (classification, reasoning, sequential,
  code), with a slope statistically indistinguishable from v2's classification-only 0.935.

This is the core finding: **the out-of-sample `ΔG ~ I` law is not a property of
classification — it holds, with the same ≈1 slope, across reasoning, sequential decision,
and code shapes, and pooled with classification.**

## 3. Verdict against the frozen thresholds (11/12)

| check | reason | seqstate | code | pooled / cross |
|---|---|---|---|---|
| L2-a Spearman(I,acc)>0.70 | ✓ 0.943 | ✓ 0.886 | ✗ 0.429 (underpowered) | — |
| L2-b slope(ΔG~I) CI excl 0 | ✓ 0.936 | ✓ 1.023 | ✓ 1.133 | — |
| L2-e info-floor I>3×null | ✓ | ✓ | ✓ | — |
| L2-c pooled-new slope∈[0.5,1.5] | — | — | — | ✓ 0.956 |
| L2-d cross-shape ρ>0.80 & slope CI excl 0 | — | — | — | ✓ ρ0.924, slope0.953 |

**Pre-registered LAW verdict (strict):** requires L2-a *and* L2-b for **every** shape +
L2-c + L2-d. Code's L2-a fails ⇒ the **strict** full-LAW verdict is **not met at the
6-model minimum**. **Honest reading:** the bridge (`ΔG ~ I`) generalizes across all three
new shapes (every L2-b passes) and is consistent with classification (L2-d); `I`-tracks-
capability is confirmed for reasoning and sequential and **underpowered (CAP-like), not
broken,** for code. This is a **strong generalization with one inconclusive sub-check**,
not a clean "law for all shapes" and not a "shape-specific break." The 8-model extension
is the pre-registered path to resolve code's L2-a.

## 4. Honest scope

- **In-sample `ΔG = I` is definitional** (oracle posterior); the empirical content is the
  **out-of-sample** `ΔG_holdout ~ I` tracking (L2-b/c/d), which is what passes here.
- **Discretisation** (mod 4 / mod 6 / hash mod 4) sets the `I` *scale*; the **slope** and
  **rank** claims are scale-invariant, and the absolute `I` is not over-interpreted.
- **seqstate is synthetic** (exact gold, controllable difficulty) — a clean substitute for
  the sequential-decision shape, not scraped agent traces; live tool-use is not tested.
- **code uses real sandboxed execution** (rigorous, not a soft estimate); its capability
  spread at ≤3B is compressed, which is why L2-a is underpowered there.
- **Open-ended generation (continuous-MI) is deferred** as the hard frontier (prereg §6) —
  not claimed here.
- **6 of 8 models** (the pre-registered minimum); see §5.

## 5. 8-model extension — attempted, blocked by hardware (honest infrastructure limit)

The full pre-registered ladder adds **qwen2.5:7b** and **llama3.1:8b** — both materially
stronger, especially on MBPP, and the pre-registered path to widen code's capability range
and resolve its underpowered L2-a. **They could not be run at usable throughput.** On the
16 GB China-Mac host, qwen2.5:7b with 512-token chain-of-thought **stalled**: ~40 of 150
items over the multi-hour window, 0 progress across a 10-minute observation, the process
blocked at 0 % CPU (RAM-pressure / swap thrashing — the same 7B+-on-16 GB ceiling v2
documented for phi3.5). Throughput was effectively zero; an 8-model run would take days, if
it completed at all.

Per this thread's no-fishing / honest-limits discipline, we do **not** force inadequate
hardware, and we do **not** reduce `num_predict` or swap models for the big two (that would
be a post-hoc design change making them non-comparable to the 6). The result is therefore
**finalized at the pre-registered ≥6-model minimum** (which the pre-registration explicitly
permits: "analysis requires ≥6 actually run per shape"). The partial qwen7b run (<142 items)
is auto-excluded by the analysis and left in the cache for audit.

**Consequence for the verdict, stated plainly:** the strict full-LAW verdict (every shape
passes both L2-a and L2-b) is **not met**, because code's L2-a is underpowered and the
remedy was unrunnable here. What *is* established stands on its own and is strong: the
out-of-sample `ΔG ~ I` bridge generalizes across reasoning, sequential, and code shapes
(every L2-b passes), pooled (slope 0.956) and cross-shape with classification (ρ 0.924,
slope 0.953 ≈ v2's 0.935); `I`-tracks-capability is confirmed for two of three new shapes.

**To actually complete the test** (future, on adequate hardware): re-run the *frozen*
8-model design on a host that can serve 7B–8B at 512-token CoT (≥32–48 GB, or a faster
fleet), then `execute_code.py` + `analyze_shapes.py` cache-only. If code's L2-a then clears
0.70, the strict cross-shape LAW verdict is met → prepare a Zenodo v3 (bridge promoted from
demonstration to law), owner sign-off gated. If it remains < 0.70 with a *tight* CI, that is
a real **shape-specific** finding (capability-tracking weaker for code), reported as such.
Neither can be claimed from the current underpowered code L2-a.

*Author byline: Cheng Qian. Pre-registration + analysis-addendum SHAs precede the results
commit. All numbers re-derive offline from `sim/real/shapes/results/` + the v2 cache.*

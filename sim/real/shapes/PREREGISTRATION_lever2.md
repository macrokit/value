# PRE-REGISTRATION — Lever 2: is `ΔG = I(X;Y)` a LAW across task *shapes*?

**Committed before any model is run for this rung.** Frozen: domains/shapes, models,
mappings, statistics, and pass/fail thresholds are fixed here in advance. The git commit
of this file precedes the first `sim/real/shapes/results/` commit (the audit trail).
Results are reported honestly in `docs/14-bridge-generalization.md`, FAILs and a *break*
(holds for classification, fails for a new shape) included. Author byline: **Cheng Qian**.
Everything described abstractly; no private/proprietary content.

---

## 0. The question and what would make / break the law

v1 tested the capacity bridge `ΔG ∝ I(X;Y)` on 1 task; **v2** generalized it across **3
domains × 10 models** (`docs/09`): pooled Spearman(I, accuracy) = 0.977, out-of-sample
slope(ΔG ~ I) = 0.935. **The standing critique: all three v2 domains were the same task
*shape* — pick-a-label classification.** Lever 2 tests whether the same relationship
holds across qualitatively different task **shapes**.

**The design rule that keeps `I` rigorous (no physics-envy):** test only shapes whose
**ground truth is discrete**, so the *exact* confusion-matrix `I` machinery of v1/v2
applies (no embedding/kNN MI estimation). `X` = discrete gold, `Y` = the model's
discretised outcome, `I(X;Y)` from the confusion matrix — **computed, not estimated.**
Truly open-ended generation (continuous-MI) is the **hard frontier** and is explicitly
**deferred** (§6), not faked with a soft estimate.

**CLAIM (to confirm or falsify):** across all tested shapes — **per-shape AND pooled** —
(i) `I` tracks capability and (ii) out-of-sample `ΔG` tracks `I` with slope CI excluding
0, the *same* relationship as classification ⇒ the bridge is a **law**, not a
classification demonstration.

**Honesty (locked, as in v2):** in-sample `ΔG = I` is **definitional** (the oracle
posterior). The empirical content is (a) the **out-of-sample** `ΔG_holdout ~ I` tracking
and (b) the **cross-shape generalisation**. A *break* — the bridge holds for some shapes
and fails for another — is a **real, informative result** ("the bridge is shape-specific"),
reported as such, never hidden.

---

## 1. Mapping (identical pipeline to v2 — this is the point)

For every shape, each item has a **discrete gold class** `X ∈ {0..K-1}` and the model
produces a free-form output that is parsed/executed to a **discrete outcome**
`Y ∈ {0..K-1} ∪ {?}` (`?` = unparseable/erroring, a distinct honest error column, never
dropped). The raw artifact for each (model, shape) is the **same schema as v2**:
`{id: {gold, pred, text, prompt_tokens, eval_tokens, total_ns}}`. Therefore the v2
analysis code (`sim/real/v2/experiments_v2.py`: `confusion`, `calib`, `per_item_value`,
R1a/R1b, R2) is **reused unchanged**:

- `q(x)` = empirical marginal of gold classes; reference `r = q` (no-signal agent grows
  at rate 0; in-sample `ΔG = I` holds for the oracle posterior — definitional).
- `I(X;Y)` = `mutual_information(confusion)` in nats.
- capability proxy = per-(model, shape) **accuracy** (fraction with `pred == gold`).
- **out-of-sample** `ΔG_holdout`: calibrate the posterior `p(x|y)` on a seeded 50/50
  **fit** split (Laplace α=0.5), score per-item value `ln(p(x|y)/r(x))` on the **holdout**.
- Seeded stratified fit/holdout split; 95% bootstrap CIs (2000 resamples), exactly as v2.

**Finite-sample `I` bias (disclosed control).** New shapes use modest `K` (below) and
n≈100–150 ⇒ a confusion matrix comparable in sampling to v2's K=4 domains. We additionally
report, per point, a **permutation-null `I`** (mean `I` over 20 label-shuffles of `Y`) as
the bias floor, and require **signal `I` > 3 × null `I`** for a point to count as carrying
information (else flagged). This is a rigor add-on beyond v2; it does not change the v2
pipeline, only annotates it.

---

## 2. The three shapes (discrete gold; genuinely different task shapes)

| ID | shape | source | free-form output | discrete gold `X` | `Y` (parsed/executed) | K | target n |
|----|-------|--------|------------------|-------------------|----------------------|---|----------|
| **reason** | free-form reasoning → number | GSM8K (openai/gsm8k, test) | chain-of-thought, then a number | `gold_answer mod 4` | `extracted_final_int mod 4`, else `?` | 4 | 150 |
| **seqstate** | sequential/agentic rollout → final state | **synthetic** register-machine (pre-registered generator §2.2) | step-by-step trace, then a final state | exact final register value `mod K` | parsed final state `mod K`, else `?` | 6 | 150 |
| **code** | code generation → executed output | MBPP (google-research-datasets/mbpp, test) | a free-form Python function | `hash(repr(gold_output)) mod K` | `hash(repr(model_code_output)) mod K`, else `?`/`ERR` | 4 | 96 |

**Why these are different *shapes*, not new domains of the same shape:** classification is
*pick one of K shown labels from a single input*. **reason** requires multi-line free
arithmetic reasoning before a number is produced (the label is not shown; it is
*computed*). **seqstate** requires tracking state across N sequential operations to a final
discrete endpoint (a sequential-decision rollout — the "agentic / multi-step → final
action" shape; tools are simulated inline, no live tool calls). **code** requires
producing a *program* whose *executed behaviour* (not its text) determines the discrete
outcome. In all three the discrete gold is exact and `I` is computed from a confusion
matrix — the rigour of classification with a genuinely different task shape.

### 2.1 reason (GSM8K) — frozen
- Items: first `n=150` test items whose gold answer (after `####`) is a **non-negative
  integer** (non-integer/zero-rare items filtered; filter is pre-registered & logged).
- `X = gold mod 4`, `Y = (final integer parsed from the model's output) mod 4` or `?`.
  Parse rule: the **last** integer in the output (CoT then answer); pre-registered, frozen.
- Prompt: "Solve the problem. Think step by step, then end with `#### <integer>`." Greedy
  (temp 0), `num_predict = 512` (room for CoT).
- mod-4 is **solve-gated** (the residue is not guessable from the problem surface; a wrong
  answer gives a ~uniform residue ⇒ noise), and matches v2's K=4 for comparability.

### 2.2 seqstate (synthetic sequential rollout) — frozen generator
- A register starts at `s0 ∈ {0..K-1}`; `L` operations are applied, each
  `+a`, `-a`, or `×a` (mod K), `a ∈ {1..K-1}`, drawn by a **seeded** RNG (seed 7).
  `K = 6`, `L = 5` steps. Gold `X` = the exact final register value (computed by the
  harness, mod K). This is a deterministic multi-step rollout to a discrete endpoint.
- The model is shown `s0` and the `L` operations and asked to **apply them one at a time,
  showing each intermediate value, then output `#### <final value>`**. `Y` = parsed final
  value mod K, or `?`. Greedy, `num_predict = 512`.
- n=150 items, seeded. Difficulty (`L=5`, `×` mod K) is set so the ladder spans accuracy
  (weak models lose track; strong models hold state) — verified only AFTER the run; if all
  models score ≈ chance or ≈ perfect (no capability spread), the shape is **uninformative**
  and reported as such (a pre-stated failure mode, not tuned away).
- **Synthetic is deliberate:** the gold is *exact* (more rigorous than scraped labels),
  and difficulty is controllable. Disclosed as synthetic in `docs/14`.

### 2.3 code (MBPP) — frozen, with sandbox; defer-if-infeasible
- Items: first `n=96` test items with a parseable first `assert` of the form
  `assert f(args) == <literal>` (so a gold output literal exists). Filter pre-registered.
- The model is prompted to write the function (free-form code). Its code is executed in a
  **sandbox** (separate `python3` subprocess, **5 s timeout, no network, no shell**, run
  on the China Mac via the same tunnel host to isolate from the main Mac; `__import__`
  of `os`/`sys`/`subprocess`/`socket` blocked in the exec globals) on the assert's input.
- `gold_output` = the literal RHS of the first assert; `X = hash_modK(repr(gold_output))`.
  `Y = hash_modK(repr(model_output))` if it runs, else `?` (no compile / exception /
  timeout). `K = 4`, `hash_modK = (sha256(repr) as int) mod K` — deterministic, type-
  agnostic, near-uniform; a *correct* program reproduces the gold output ⇒ same class.
- **Heaviest shape (execution).** It is rigorous (real execution, not a soft estimate), so
  it is worth attempting. If the sandbox proves unsafe or flaky at this scale, **code is
  DEFERRED with a stated reason** (not faked, not soft-estimated) and the law is reported
  on the shapes that completed — explicitly scoped.

---

## 3. Model ladder (frozen)

A capability-spanning subset of the v2 ladder (generative outputs are slower; a smaller
ladder is justified by cost and still gives ≥6 points per shape for the per-shape
Spearman). Pre-registered tags (Ollama, China-Mac fleet), ~0.5B→8B, 3 families:

`qwen2.5:0.5b-instruct`, `llama3.2:1b`, `qwen2.5:1.5b-instruct`, `gemma2:2b`,
`qwen2.5:3b-instruct`, `llama3.2:3b`, `qwen2.5:7b-instruct`, `llama3.1:8b` — **8 models**.

A model absent at run time is skipped + logged; analysis requires ≥ 6 actually run per
shape. A run with **> 50% `?` (unparseable)** is excluded as plumbing/degradation (not
recorded as low capability), exactly as v2's degraded-model guard — logged.

---

## 4. Pre-registered thresholds (frozen)

Let a "point" be one (model, shape) pair with measured (accuracy, `I`, `ΔG_holdout`).

| ID | check | threshold to PASS |
|----|-------|-------------------|
| **L2-a** per-shape capability tracking | for **each** completed shape: Spearman(`I`, accuracy) across its models | ρ > 0.70 |
| **L2-b** per-shape out-of-sample bridge | for **each** completed shape: slope(`ΔG_holdout` ~ `I`) bootstrap 95% CI | excludes 0 (positive) |
| **L2-c** pooled bridge across shapes | pooled over ALL completed-new-shape points: slope(`ΔG_holdout` ~ `I`) 95% CI | excludes 0 (positive) AND slope ∈ [0.5, 1.5] |
| **L2-d** cross-shape consistency w/ classification | pool new shapes **+ v2's 3 classification domains** (recomputed, same pipeline): pooled Spearman(`I`, acc) and slope(ΔG~I) | ρ > 0.80 AND slope CI excludes 0 |
| **L2-e** info-floor sanity | every counted point has signal `I` > 3 × permutation-null `I` | ≥ 90% of points pass; points failing are flagged, not counted |

**LAW verdict (pre-committed):** the bridge is reported as a **law across shapes** iff
**L2-a, L2-b for every completed shape, AND L2-c, AND L2-d** all PASS (with ≥ 2 new shapes
completed besides classification). 

**BREAK verdict:** if L2-a/L2-b PASS for some shapes but FAIL for ≥1 shape, report
**"the bridge is shape-specific,"** naming which shape breaks it and the likely reason
(e.g., `I` saturates, no capability spread, parsing confound). This is a real result.

**CAP / inconclusive:** if a shape yields no capability spread across the ladder (all
models ≈ chance or ≈ ceiling) so Spearman/slope are undefined or noise-dominated, that
shape is reported **inconclusive — uninformative at this scale**, not as a pass or fail.
Do **not** escalate model size or hand-tune difficulty post-hoc to manufacture a spread.

---

## 5. Statistics & reproducibility (frozen)

- Spearman via rank-correlation; slope via OLS `ΔG_holdout ~ I`; 95% CIs by 2000-sample
  bootstrap over points (same `boot_ci`/`spearman`/`slope` as `experiments_v2.py`).
- Seeded stratified 50/50 fit/holdout per shape (seed 7); ΔG scored on holdout only.
- Every model call cached (`results/raw/{model}__{shape}.json`); every code execution
  cached by `(model, item, code_hash)`. All numbers re-derive offline from cache.
- v2 classification points (L2-d) recomputed from the existing `sim/real/v2/results/raw/`
  cache with the identical pipeline — no re-running v2 models.

---

## 6. The deferred frontier (stated now, not after seeing results)

**Truly open-ended generation** (free-form text with no discrete gold — summarisation,
essays, dialogue) requires **continuous / embedding-based MI estimation** (kNN, MINE),
which is the genuine hard frontier and the place a "law" could be manufactured by a soft
estimate. It is **explicitly out of scope for this rung** and deferred to a future,
separately-pre-registered test with a rigorous MI estimator and its own validation. We do
**not** claim the law for open-ended generation here, and we say so.

## 7. Honest limits (stated before any run)

- **Discretisation choices** (`mod 4`, `mod K`, `hash mod K`) define the label space; they
  are pre-registered and frozen, but a different discretisation would give a different `I`
  *scale*. The **slope** (ΔG~I) and the **rank** tracking are the claims, and both are
  invariant to the `I` scale; the absolute `I` value is not over-interpreted.
- **Smaller n and ladder than v2** (cost of generative outputs). Enough for a regression
  with CIs, not a high-precision estimate. Disclosed.
- **seqstate is synthetic** (exact gold, controllable difficulty) — a clean *substitute*
  of the sequential-decision shape, not scraped agent traces; live tool-use is not tested.
- **code uses execution** of small-model code in a sandbox; if unsafe/flaky it is deferred.
- **Not a proof of universality.** Two–three new shapes + classification is materially
  broader than "one shape," but still a finite slice of task space. The law is shown to
  generalise *across these shapes*, not proven for all tasks.

*Pre-registration commit SHA precedes the results commit SHA — see git log.*

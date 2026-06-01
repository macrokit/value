# PRE-REGISTRATION — v2 empirical scale-up of the value theory

**Committed before any v2 model was run.** This document fixes the domains, models, metrics, routing
policies, statistical procedure, and pass/fail thresholds *in advance*. It is **frozen**: once committed it is
not edited. Results are reported against it honestly in `docs/09-v2-empirics.md`, including any FAILs. (v1
called itself "pre-registered" after the fact; this file exists so the word is earned. The git commit
timestamp of this file, preceding the first `sim/real/v2/results/` commit, is the audit trail.)

Author byline for any resulting publication: **Cheng Qian**. Everything here is described abstractly; no
private/proprietary domain content.

---

## 0. The question and the prior result

v1 measured the value laws on **1 task, 4 models** — a demonstration, not a validation (external review: rigor
6.5/10). v2 attacks three weaknesses: **(A)** one task → ≥3 domains; **(B)** 4 models → a ≥8-model
cross-family ladder (R1 as a regression, not 4 points); **(C)** the homogeneous R5 (which could only show
pricing > pooling, not pricing > best-single) → a **heterogeneous, cost-constrained fleet** raced against a
**strong hand-tuned router**. (C) is the headline and the gate for the governance/killer-app claim.

The **R5 framing rule is locked and pre-committed**: pricing is a *scoping theorem* — it is predicted to
dominate ad-hoc allocation only under **cost constraints OR imperfect agent correlation**. We never report
"pricing beats ad-hoc" unqualified.

---

## 1. Design (fixed in advance)

### 1.1 Mapping (unchanged from v1)
For every domain: world-state `X` = the ground-truth correct action/label of an item over `K` classes;
signal `Y_a` = model `a`'s chosen label; `q(x)` = empirical marginal of correct labels; reference `r = q`
(so a no-signal agent grows value at rate 0 and the in-sample identity `ΔG = I(X;Y)` holds for the oracle
posterior). All quantities computed in **nats** with `sim/value_sim.py`
(`mutual_information`, `kl`, `entropy`, `portfolio_growth`, `kelly_weights`).

### 1.2 Output protocol (fixes the v1 tool-call artifact)
All v2 domains use **plain text-label output** (the model emits a label token; we parse it), NOT the Ollama
tool-call API. This (a) lets every model on the ladder participate in every domain, and (b) removes the
tool-call plumbing failure that forced mistral's exclusion in v1. A response that parses to no valid label is
recorded as a distinct `?` class (an honest error column), never silently dropped. Greedy decoding
(temperature 0) for the main runs.

### 1.3 Domains (≥3 required; these three are the pre-registered set)
| ID | Domain | K | Source (public, abstract) | Target n |
|----|--------|---|---------------------------|----------|
| D1 | intent routing | 6 | CLINC150 (clinc/oos-eval), a confusable assistant-router slice | 240 |
| D2 | multiple-choice QA | 4 | MMLU-style MCQA, mixed subjects (A/B/C/D) | 240 |
| D3 | topic classification | 4 | AG News (World/Sports/Business/Sci-Tech) | 240 |
| D4 (optional) | sentiment | 2–3 | a public sentiment set | 200 |
Each domain: balanced where possible; a seeded stratified **fit/holdout split (50/50)**. Corpora of 200–300
items/domain (≥3× v1's per-task size). If a source is unreachable, a documented clean substitute of the same
task *shape* may be used; the substitution is logged in `docs/09`.

### 1.4 Model ladder (≥8 required, across ≥3 families)
Pre-registered target (Ollama tags), spanning ~0.5B→9B and the Qwen / Llama / Gemma / Phi families:
`qwen2.5:0.5b-instruct`, `qwen2.5:1.5b-instruct`, `qwen2.5:3b-instruct`, `qwen2.5:7b-instruct`,
`llama3.2:1b-instruct`, `llama3.2:3b-instruct`, `llama3.1:8b`, `gemma2:2b`, `phi3.5` (3.8B). Target **9 models**.
- `mistral:7b` MAY be included in v2 because v2 uses text output (its v1 tool-call incompatibility does not
  apply); if included it is flagged as text-only and never as evidence about tool-calling.
- A model that fails to pull/load on the 16 GB host is **excluded and logged**; the analysis requires
  **≥8 models actually run**. Capability proxy = per-model per-domain **accuracy** (not `I` — accuracy is the
  independent capability axis R1 is tested against).

### 1.5 Cost model (for the budgeted fleet, Axis C)
`cost_a` = **mean total tokens per call** (Ollama `prompt_eval_count + eval_count`), measured per model
(secondary: mean latency seconds). Frozen choice: tokens are the primary budget unit.

### 1.6 Statistical procedure (Axis D)
- **Seeds:** ≥3 seeds vary the fit/holdout split and any stochastic routing. Point estimates are accompanied by
  **95% confidence intervals** (bootstrap over items, ≥1000 resamples, and/or across seeds — whichever is
  reported is stated).
- **Out-of-sample discipline:** calibrated posteriors and all routing weights are fit on the **fit** split and
  scored on the **holdout** split. The in-sample `ΔG = I` identity is reported only to confirm units, and is
  labeled non-evidential.
- All model outputs cached to JSON; every number re-derivable offline from cache.

---

## 2. Experiments and PRE-REGISTERED pass/fail thresholds

These thresholds are verbatim binding. A result that misses a threshold is reported as a **FAIL** with analysis.

### R1-v2 — the bridge generalizes (capacity)
Pooled across **≥3 domains and ≥8 models**:
- **(R1a)** `I(X;Y)` vs realized capability (accuracy) has **Spearman ρ > 0.8** (report ρ with a 95% CI).
- **(R1b)** out-of-sample `ΔG` tracks `I`: the regression slope of `ΔG_holdout` on `I` has a **95% CI that
  excludes 0** (and is positive).
- **PASS** = both hold pooled, AND R1a holds within each domain individually (per-domain ρ > 0.6, a weaker
  per-domain bar acknowledging smaller n). **FAIL** ⇒ the core bridge does not generalize.

### R2-v2 — the Second Law generalizes (dissipation)
- Constructing an over-confident posterior from the same predictions, realized growth drops:
  **dissipation `G_cal − G_over > 0` in every domain.** The least-capable models may go **negative** under
  over-confidence (reported, not required).
- **PASS** = dissipation > 0 in every domain. **FAIL** ⇒ the Second Law is domain-specific.

### Fleet-R5 — the heterogeneous, cost-constrained headline
Build a **specialist** fleet (low cross-agent error correlation — verified to be **lower than v1's mean
pairwise error-agreement**) over a mixed multi-domain query stream under a **fixed token budget**. Compare
**realized task-value per unit budget** of these routing policies:
1. **round-robin** (naive),
2. **equal-weight pooling** (query all, average posteriors),
3. **best-single** (the one model with highest fit accuracy overall),
4. **value-price routing** — per query, route to the model maximizing **`I_a(domain)/cost_a`** (the
   shadow-price `λ=K/E` rule, doc 03 §2; per-domain `I` fit on the fit split),
5. **hand-tuned router (the strong adversary)** — per query, route to the model with the **highest fit-split
   accuracy in that query's domain** (a domain-aware, quality-first router a competent engineer would build;
   cost-blind by construction).

Pre-registered verdicts (report ALL, with CIs):
- **(R5-required)** value-price **beats round-robin AND equal-weight** on value-per-budget (CI of the
  difference excludes 0). This is *required* to keep the governance claim non-empty. **A loss to round-robin
  falsifies the governance claim** and is reported as such.
- **(R5-strong)** value-price **beats the hand-tuned baseline** on value-per-budget. This is the *strong* win
  (the theory's cost-aware router beats a smart cost-blind engineer under budget). Reported PASS/FAIL honestly;
  a tie/loss here is an honest, publishable result (it would mean `I/cost` pricing ≈ a hand-tuned heuristic),
  **not** a mission failure.
- Secondary: also report a *cost-aware* hand-tuned variant (route by best fit **accuracy/cost** per domain) as
  an even-stronger adversary; report whether value-price ties it.

### Ceiling & diversity (R4 at scale)
- **`Σ_a G_a ≤ H(X)`** holds (it is a bound; it must never break — a break indicates a measurement bug).
- Joint `I(X; Y_a, Y_b)` for **diverse specialists > redundant** (same-model / same-domain) pairs; diverse
  specialists approach `H(X)` better than generalists. PASS = both hold.

---

## 3. What would change our mind (falsifiers, stated up front)
- R1-v2 FAIL (ρ ≤ 0.8 pooled, or slope CI includes 0) ⇒ the capacity bridge is task-specific, not a law.
- R2-v2 FAIL in any domain ⇒ the Second Law decomposition is not general.
- Fleet-R5 value-price **loses to round-robin** ⇒ the governance/pricing claim is empty; we retract it.
- `Σ_a G_a > H(X)` beyond CI ⇒ a measurement/implementation bug to be found before any other claim stands.

## 4. Publication gate
IF (and only if) R1-v2 PASS, R2-v2 PASS, and Fleet-R5-required PASS hold, a Zenodo **"New version"** of the
preprint (concept DOI 10.5281/zenodo.20487041) is *prepared* with the strengthened empirics. Publishing
requires explicit owner sign-off; the deposit is done in-browser up to — and stopping at — the Publish button.
Negative results are written up regardless and do not gate on owner sign-off to be *recorded* in `docs/09`.

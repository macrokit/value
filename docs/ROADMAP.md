# Roadmap — open directions (status as of 2026-06-04)

A single view of what's open, so the threads aren't scattered. Ordered by readiness. The published core
(Zenodo, concept DOI `10.5281/zenodo.20487041`) stands on its own; everything here is *forward* work.

## Strategic lens (the prioritization rule)
External review converges on one directive: *the decisive move is not more equations or broader Kelly-style
validation, but an empirical result that **Kelly / information theory / decision theory cannot explain.*** That
sorts the work sharply:
- The **single-agent bridge** (`ΔG = I(X;Y)`, the cross-shape law) is **Kelly's home turf** — strengthening it
  (more shapes, more models) raises rigor but does **not** escape the "generalized Kelly with new terminology"
  critique, and does not earn the word "value."
- What is **distinctively *value*** — and the only thing that escapes that critique, settles the naming battle,
  and lifts the impact tier — is the **multi-agent + dynamics layer**: cross-frame/price coordination, the
  fleet ceiling, and the is/ought / alignment-as-control results. *None* of these are single-agent Kelly.
**Therefore: prioritize the multi-agent / dynamics empirics (below) over any further single-agent/bridge work.**
The cross-frame/price **real-data test is the highest-leverage shot** precisely because it tests the part Kelly
does not cover, with measured (not weak-model-elicited) quantities.

## Near-term (in flight / logistics)
- [x] **Publish v3 — DONE (live 2026-06-03):** `zenodo.org/records/20530824` (Version v3, under concept DOI
  `10.5281/zenodo.20487041`; v1/v2 preserved). The cross-shape generalization ([`14`](14-bridge-generalization.md))
  + two-route derivation hardening ([`01`](01-core-formalization.md)); `n=42` reconciled; PDF md5 `1fb3a85e…`.
  **This is now the canonical link** for citation/dissemination.
- [ ] **v3-completeness (optional):** close the code **capability-ranking** sub-check (currently 11/12 —
  underpowered, ρ=0.429). Needs a **≥32 GB host** to run 7B/8B coders without the 16 GB RAM thrash; would turn
  11/12 → 12/12. Not a blocker for v3; would let a later version drop the caveat.
- [ ] **Dissemination (the real "reach" lever):** the published record has ~0 views — that is a *distribution*
  problem, not a versioning one. Move: post the is/ought-as-control note (drafted, `drafts/`) to the relevant
  audience + an arXiv cross-listing + sharing. This is what converts the record into readers; another version
  does not.
- [x] **v4 paper revision — PUBLISHED (2026-06-06):** record `zenodo.org/records/20572360`; folds the priority
  concessions into the paper. Superseded by the v5 candidate below.
- [x] **v5 paper revision — PUBLISHED (2026-06-10):** `zenodo.org/records/20621815`, title now carries the
  subtitle, description = the v5 abstract verbatim, md5 `11ab30c5…` verified live. **Dissemination is
  UNBLOCKED.** Original entry:** The
  sixth (correctness) pass found the sum-form fleet ceiling **false**; v4 carries it in the abstract and §fleet.
  `paper/main.tex` now: corrects the abstract + fleet section (pooled/fused ceiling, explicit erratum +
  counterexample, sum-form only under payout coupling); cites **Barron & Cover 1988** as the primary source for
  the side-information bound (+ Blackwell 1953, Sims 2003, Ortega & Braun 2013); reframes the contribution list
  ("pooled-fleet ceiling … both corollaries of Kelly–Cover, claimed as such"). `main.pdf` rebuilt
  (md5 `11ab30c51e7d22b6ed7b41bb82707ea2` (after the 🟡 folds + subtitle + decisive-prediction paragraph)), citations resolve. **Remaining (owner-gated):** publish Zenodo
  **v5** (new version under the concept DOI), then resync `drafts/arxiv-metadata.md` to the v5 abstract. v4 has
  ~0 views — zero cost to supersede; do this BEFORE any posting (the predicted top comment is "the fleet
  ceiling is wrong," and v5 removes it).
- [x] **Priority / novelty check — DONE (2026-06-06):** deep-research pass against the nearest neighbors. Verdict:
  components anticipated (result 1(ii) ← ergodicity economics; result 2 ← Kelly/info-rate, Moffett–Eckford 2021,
  Touchette–Lloyd 2000; **result 3 ← Still, Sivak, Bell & Crooks 2012 "thermodynamics of prediction" — the one
  genuine priority threat**), **synthesis + result 5 (is/ought-as-control) appear novel** (nearest neighbor,
  active inference, makes the *opposite* move). `related-work.md` patched to cite the flagged neighbors.
- [x] **Close the two open priority gaps — second pass DONE (2026-06-06).** Verdicts:
  **(A-iii)** Fisher–Rao as cross-frame invariant = **Čencov's uniqueness theorem restated** (Campbell 1986; Lê
  2017; Bauer–Bruveris–Michor 2016) — the theory's *weakest* novelty claim; `related-work.md` now concedes it as
  an application, not a new result. **(A-frame-split)** value-relative-vs-price-invariant: **no clear prior**
  (nearest, Lin 2026 "Financial Relativity," does the *inverse*); economics dimension (Hayek/Arrow) still
  untested. **(A-fleet ceiling `Σ G_a ≤ H(X)`)**: **no clear prior** — single-agent Kelly conservation doesn't
  aggregate; held as plausibly-novel. **(B, result 5)**: **no clear prior** — only an *agenda* paper (Perrier
  2025) exists, no formal stability condition / residual; `related-work.md` now positions doc 07 as supplying
  what that agenda calls for. **(C)** no unified "mathematical/thermodynamic theory of value" framing found.
- [x] **Third pass on result-5 residual — DONE (2026-06-06); verdict SHIFTED, be honest about it.** The deeper
  search found real prior art the first two passes missed, so result 5 splits:
  **Part 1 (is/ought asymmetry):** the *value-side* (goals can't be read off behavior) is **anticipated** —
  **Armstrong & Mindermann (2018)** prove it as a No-Free-Lunch result and *explicitly call it Hume's is/ought
  gap formalized*; Spizzirri (2026) restates it. Our surviving Part-1 novelty is only the *two-sided*
  belief-vs-goal dynamical framing (+ the `D(q‖r)` belief target) — **presentational, contestable.**
  **Part 2 (alignment-as-control-stability, `γ > λ_max`, `‖Vg‖/γ`):** **no clear prior found** — the genuine
  surviving novelty. Closest analogs: Perrier 2025 (agenda only), Goertzel 2024 (contraction fixed-point, no
  eigenvalue criterion), Powers PCT (`1/(1+G)` but vs *exogenous* disturbance, not goal-drift Jacobian).
  `related-work.md` rewritten to concede Part 1's value-side and claim only Part 2. **Net: result 5's headline
  novelty narrows from "the is/ought asymmetry" to "the control-stability theorem."**
- [x] **Fourth pass (cybernetics + classical control) — DONE (2026-06-06); result 5 / Part 2 fully demoted.**
  Blunt verdict: the alignment-layer **control result is elementary classical control**, not new theory.
  **(a)** `γ > λ_max` = textbook high-gain / root-locus stabilization of an unstable pole. **(b)** the `‖Vg‖/γ`
  residual = the classic steady-state **velocity error `e_ss = 1/K_v`** (a drifting goal is a ramp reference) —
  a near-exact textbook match (Ogata; Åström & Murray; Franklin–Powell–Emami-Naeini; internal-model principle,
  Francis & Wonham 1976). Cybernetics (Conant–Ashby, requisite variety) = **dead end**, does not anticipate.
  **The only contribution of the alignment layer is the APPLICATION/mapping** (goal-drift-under-selection as
  ramp-tracking → incentive-beats-oversight ordering). `related-work.md` + the contribution statement rewritten
  to concede this; dissemination drafts cite Ogata/Åström–Murray to front-run the controls reviewer.
- [ ] **(Optional) Only genuine-departure left to probe.** Whether the goal-drift Jacobian `∂(Vg)/∂k̄` is
  state-dependent / non-LTI / has multi-dimensional eigenvalue coupling that the scalar LTI textbook results do
  **not** cover — the one place a *mathematical* (not merely applied) novelty for Part 2 could survive. Not
  currently claimed. Probe only if a stronger control-theoretic claim is ever wanted.

### ⊕ Sixth pass — the CORRECTNESS audit (external review, 2026-06-07): fleet ceiling was FALSE
A Fable-5 external-style review did what the five priority passes never did — checked **truth**, not just
priority — and found **one outright error in a headline result**, verified line-by-line before acting:
- **🔴 The sum-form Fleet Value Ceiling (`Σ_a G_a ≤ H(X)`, doc 04 §2) was false as stated.** Counterexample:
  two agents with identical perfect channels, each on its own bankroll, each achieve `G_a = H(X)` → sum
  `2H(X)`. The chain rule bounds *joint* information, not sums of independently-compounded growth rates; the
  MAC analogy fails (no shared medium). The sim's E3 always tested the *joint* version, never the false sum.
  **Fixed everywhere** (doc 04 erratum + corrected Joint Fleet Ceiling `G_fleet ≤ I(X;Y_{1:m}) ≤ H(X)` for a
  pooled/fused fleet — a corollary of doc 02, claimed as such; README, repo+site FAQ, paper → v5 candidate).
  **Lesson recorded: a novelty pass answers "did someone publish this?", not "is it true?"** Pass 2's
  "plausibly-novel" verdict on the sum-form ceiling found no prior because the claim was wrong.
- **🟠 Doc 03 §0/§2 self-contradiction (verified):** λ-equalization maximizes the *unweighted sum* `Σ V_a` —
  the equal-Negishi-weight planner — exactly the interpersonal comparison §0 forbids; not invariant under
  per-agent rescaling; gameable via self-declared `K_a` (mechanism design is the missing, now-acknowledged
  prior art). Honest caveat added to doc 03 §2 + honest limits.
- **🟠 Doc 03 vs 05 flow laws (verified):** λ-routing vs replicator selection govern the same quantity and
  generically disagree; reconciled as two *institutions* (governed reallocation vs ungoverned compounding) in
  both docs; doc 07 lives in the selection regime.
- **🟡 Empirics hygiene (verified + fixed):** pooled CIs now also cluster-bootstrapped by model — conclusions
  unchanged (R1a clustered CI [0.943,0.995]; R1b [0.914,0.956]); the unregistered `lo>0.5` pass-condition is
  disclosed; **Barron & Cover (1988)** (+ Blackwell 1953, Sims 2003, Ortega & Braun 2013) now cited as the
  primary source for the side-information growth bound.

### ⊕ Priority-check program — final tally (four passes, 2026-06-06; CORRECTED by the sixth pass, 2026-06-07)
Across four adversarial deep-research passes, the honest verdict on *A Mathematical Theory of Value*:
**components anticipated, synthesis novel, and three specific over-claims caught and conceded** —
(1) Fisher–Rao cross-frame invariant = Čencov restated; (2) is/ought value-side = Armstrong & Mindermann 2018;
(3) the alignment control result = elementary classical control (novelty is the application); and — added by
the sixth pass — (4) **the sum-form fleet ceiling was not novel but FALSE**; the corrected pooled-fleet version
is a Kelly–Cover corollary. **Surviving distinctively-novel claims (post-correction):** the *synthesis* itself,
the value/price *frame split*, the *focus penalty* `V* = K ln E − K·H(k̂)` (flagged by external review as the
most original interpretive move), the *governance mapping* (goal-drift as ramp-tracking →
incentive-beats-oversight), and the **concession discipline itself**. The single-agent core remains, by the
paper's own statement, generalized Kelly (primary source for the side-information bound: Barron & Cover 1988).
Net: the work's defensible contribution is **unification + honest scoping**, not a stack of new theorems —
which is exactly what the paper claims, now verified the hard way across six passes (five priority + one
correctness).

## Research directions (gated behind the published core)
- [x] **Cross-frame / price layer — real-data test → STRUCTURAL CAP** ([`15`](15-cross-frame-realdata.md),
  pre-reg `f3bc720`, verdict `81780fc`; branch `claude/goofy-hawking-2c1df2` — merge to main). Worked to a frozen
  pre-registration and stopped honestly (the charter's "say so and stop"): **the cross-frame layer has no
  observational test that is both discriminating and resolvable.** The flow/friction/price predictions are
  arbitrage / law-of-one-price / GE-repainted (trivial). The only divergent-from-Kelly prediction — the cut-set
  ceiling `Σ_{a∈S} G_a ≤ I(X;Y_S) ≤ H(X)` — lives in the *coupled-but-separate* multi-agent regime that
  observational data never exposes (only the degenerate uncoupled / fully-pooled corners; forecasting makes it a
  data-processing tautology). Sharpens the project's own adversarial-review concern from "untested" to a precise structural claim, and specifies
  the **only resolving route: a controlled multi-agent experiment with counterfactual sub-coalition throughputs
  + varied perception overlap.** That is the LLM-agent route — gated on a **stronger agent instrument** than
  small LLMs (the ceiling that sank Lever 1).

### ⊕ Convergence finding (the clarified state of the whole program)
Every escape-Kelly route is now mapped and they **all converge on one gate**: the distinctively-*value* claim is
testable *in principle* only via a **controlled multi-agent experiment** (counterfactual coalition throughputs,
varied perception overlap) with **agents capable enough to play the value game** — and *neither observational
data (degenerate corners) nor small LLMs (capability ceiling) can deliver it.* So: single-agent bridge = Kelly's
turf; governance (Lever 1) = small-LLM CAP; wave theory = real-agent negative; cross-frame = structural CAP.
**"Great" is now precisely specified and currently blocked on a stronger-agent instrument** — revisit the one
controlled-multi-agent experiment when such an instrument exists. No current move delivers the upside.

### ⊕ Goal-maintenance-cost pre-check — verdict ANTICIPATED, thread closed (2026-06-06)
Doc [`16`](16-the-disanalogy.md) §4 flagged one open candidate in the disanalogy region: an *irreducible exergy
floor on maintaining an agent-supplied, world-unpinned goal/frame against a drifting world* — distinct from the
belief-side tracking floor already conceded to Still et al. 2012. A focused fifth priority pass (same adversarial
method) **breaks it**: the floor is **housekeeping heat** (drift-independent cost of maintaining any
detailed-balance-violating steady state; Speck & Seifert 2005, *J. Phys. A* 38, L581) plus **excess heat** (the
drift-scaled transition cost; Hatano & Sasa 2001, *PRL* 86, 3463). Decisive discriminator fails: both results are
explicitly **setpoint-origin-agnostic** — they price maintaining *any* steady state "regardless of how the
nonequilibrium condition is established" / "regardless of the physical origin," so an *agent-chosen* reference
costs the same to hold as a world-given one and opens no thermodynamic gap. The only goal-specific feature (no
predictive-information discount, Still 2012, when there is no world target) is a **corollary of the already-conceded
is/ought asymmetry** (Armstrong & Mindermann 2018), not a new dissipation law. **Outcome:** the disanalogy yields
no new *law* (it remains the right place to *look* — it locates where the distinctively-value subject matter lives,
doc 16 §3); the distinctively-value contribution stays the *synthesis* + fleet ceiling + value/price frame split +
governance mapping. Thread closed; no `docs/17` written.
- [ ] **Wave / field theory — gate not cleared** (docs [`08`](08-field-theory-of-value.md),
  [`11`](11-real-agent-field-test.md)). Derived + toy-emergent, but real small-LLM agents coordinate by
  *Schelling focal points*, not spontaneous flocking. Options (no model-escalation fishing): a motile,
  focal-point-free re-test under fresh pre-registration; OR write up the honest negative as a standalone note;
  OR retire the gate. Earnable standalone preprint *only* on a clean guardrail-respecting positive.
- [ ] **Incentive-design-beats-oversight — real-agent verdict** (docs [`12`](12-incentive-vs-oversight.md),
  [`13`](13-incentive-vs-oversight-real.md)). Confirmed in the toy (`residual = V·g/γ`, R²=0.999); real-agent
  test was **CAP / underpowered** (design saturated `g ≤ 0.2` below the noise floor). A properly-powered redo
  needs a *de-saturated design* (continuous/large-K goal space, larger δ, more seeds) — the fix is the design,
  not bigger models. Likely outcome leans negative (mean trend had g-exponent ≈ 0); pursue only for a
  definitive verdict, not a rescue.
- [ ] **Axiom-3 deeper defense (optional theory).** Now *demoted* (the log is over-determined by the
  compounding route, so scale-invariance is no longer load-bearing) — so lower priority. A first-principles
  argument for why value has no privileged scale would still harden the foundation.

### ⊕ The Maxwell program — concrete path to the continuation gate (2026-06-10)
The v5 paper names the decisive prediction (the "displacement-current candidate"): for a **coupled** fleet,
(i) the capacity-region structure on jointly-achievable growth vectors under varied perception overlap, and
(ii) the `‖Vg‖/γ` residual scaling on real populations. The path, cheapest-first — and note the correctness
audit *clarified* the experiment: the sum-form was false precisely because the base model lacked coupling, so
the experiment must **implement the payout coupling explicitly** (shared bankroll or parimutuel) and measure
the region. Standing guardrails apply at every stage: pre-register before any run; report negatives as
verdicts; no instrument-fishing for positives.
- [ ] **Stage 0 — synthetic pilot of the COUPLED fleet (cheap, runnable now).** Extend `sim/` with an explicit
  payout-coupled fleet (one shared bankroll betting fused posteriors; and/or parimutuel odds), vary perception
  overlap, measure counterfactual sub-coalition throughputs, and check the predicted region structure. This
  validates the *experimental design* and the corrected theory's coupled-regime predictions before any real
  agents — and is the first test of prediction (i) in any form.
- [ ] **Stage 1 — the `‖Vg‖/γ` redo (feasible NOW — design-blocked, not instrument-blocked).** Doc 13's own
  verdict says the fix is the *design*, not bigger models: de-saturated continuous/large-K goal space, larger
  `δ`, more seeds. Expected lean-negative (g-exponent ≈ 0 last time) — run it for a **definitive verdict**: a
  clean negative honestly retires half the displacement current per the paper's own continuation-gate language
  (itself a publishable, decision-grade result); a positive is half the discovery.
- [ ] **Stage 2 — the real Maxwell test (the stronger-agent instrument now exists commercially).** The
  convergence finding's blocker was "agents capable enough to play the value game" — small local models failed.
  Frontier-model agents via API plausibly clear that bar today. The experiment: a payout-coupled multi-agent
  economy (Stage-0 design), counterfactual sub-coalition throughputs, varied perception overlap, frontier
  agents, **pre-registered before the first token**. Real costs (API spend, careful design) — budget and
  pre-registration first. Decision rule is already printed in the paper: predictions pass → the unification
  earns the stronger word; fail/CAP → the distinctively-unified layer retires, and the cleanly-falsified
  program is itself the contribution.

### ⊕ Two future-directions from the GPT-5.5 review (2026-06-07) — captured, not yet acted on
An external review independently converged on the audited position (it reached "this is a theory of
goal-directed agency, not value" and "the frame split is the most original part" on its own). It surfaced two
ideas worth keeping:
- [x] **Reframe the scope/pitch — ACTIONED in v5 (2026-06-07):** the paper now carries the subtitle *"a
  synthesis on goal-directed agency under resource constraints"* and a stated **decisive prediction /
  continuation gate** (Maxwell-test paragraph in the Discussion: coupled-fleet capacity region + `‖Vg‖/γ`
  scaling, instrument-blocked). Original direction:**"a mathematical theory of goal-directed agency under resource constraints."**
  Strategic, not a rename of the artifact: lead the *positioning* (and possibly the title) with this rather than
  "theory of value." It is more defensible and more publishable, and it matches the honest scoping
  (`docs/FAQ.md`: value is relational, requires a goal-having agent). Weigh for the dissemination framing.
- [ ] **Candidate alternative grounding: value ≈ increase in *attainable futures* (option value), not exergy.**
  The reviewer's one substantive technical criticism: a theorem / proof / standard has value not proportional to
  joules spent but to the reachable state-space it opens; exergy is the most vulnerable anchor. **Honest caveat:
  "increase in attainable futures" is essentially *empowerment* (mutual information between actions and reachable
  futures; Klyubin/Polani — already flagged as a known neighbor in pass 2).** So this is a reframing of the
  *substrate*, not an escape from anticipation — but it may be a more defensible grounding than exergy for
  non-physical value. Probe only as a deliberate foundational revision; pre-check against empowerment/option-value
  first (same discipline as the goal-floor pre-check).
- *(Note: the review's enthusiasm for the is/ought asymmetry and the alignment dynamical system as novel is
  behind this audit — both are conceded in v4 (A&M 2018; classical control). Do NOT re-inflate them on the
  strength of the review.)*

## Standing discipline (applies to every item above)
Pre-register before fitting; keep pre-registered vs exploratory strictly separate; report negatives as results;
no instrument-fishing (no escalating model size / forcing hardware to manufacture a positive); the publish gate
is owner-only; keep the core paper substrate-agnostic and clean. The credibility of the whole program rests on
these — they are why the *good* result is worth more than a hollow *great*.

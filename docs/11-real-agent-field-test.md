# The Real-Agent Field Test (Rung 7) — an honest negative, and what it isolates

> The decisive gate for the wave/field theory of value (doc 08): do the demand wave
> (§3) and the collective-goal transition (§5) survive when the microscopic rule is a
> **real small LLM** choosing each agent's strategy, rather than a hand-coded equation?
> Pre-registered in [`sim/field/real/PREREGISTRATION.md`](../sim/field/real/PREREGISTRATION.md)
> (thresholds frozen, falsification clause up front, v2 discipline); harness +
> cached runs in [`sim/field/real/`](../sim/field/real/).
>
> **Result, stated plainly: the pre-registered tests are a NEGATIVE.** Neither
> signature appeared under its frozen thresholds. But the negative does **not** cleanly
> refute the field theory, because a confound specific to *LLM agents* — intrinsic
> **token bias** plus a **weak noise knob** — sits between the theory and the
> measurement. This document separates, precisely, (a) what the pre-registered tests
> returned, (b) what exploratory follow-ups suggest, and (c) what is confound vs. signal.
> Per the honesty rule of this thread, a negative is a real finding; we neither
> rationalize it away nor inflate it into a refutation.

## 0. The system (recap)

`N` agents, each holding one of `K=8` niches (a goal director on a circle; order
parameter `m=|⟨e^{iθ}⟩|`). Each round, **`qwen2.5:0.5b-instruct` (pre-registered) /
`qwen2.5:1.5b-instruct` (secondary)** chooses each agent's next niche from its payoff
history and a tally of its neighbours' niches. The economy rewards coordinating with
neighbours (alignment dividend = the coupling); a value-shock bumps one niche's reward
(for the wave); a control field `γ` rewards a principal niche (the mass term). **LLM
sampling temperature is the noise knob.** Every call is cached (12.7k calls; sqlite).
Random baseline for `m` at `N=20, K=8` is `≈ 0.20`.

---

## 1. Signature 2 — collective-goal transition: PRE-REGISTERED NEGATIVE

### 1.1 The frozen verdict (both models: 0/4)

| check | threshold | 0.5b | 1.5b |
|---|---|---|---|
| **C1** order→disorder | `m(0.2)>0.55` & `m(1.4)<0.35` | 0.656 → **0.466** ✗ | 0.938 → **0.783** ✗ |
| **C2** interior χ peak | interior max `>1.5×` ends | peak at 1.0 but only 1.13× ✗ | χ rises to the **boundary** (1.4) ✗ |
| **C3** control = mass | `γ>0` raises `m(1.4)` ≥0.10 & suppresses χ-peak | Δm=**−0.082**, χ-peak ↑ ✗ | Δm=**−0.041**, χ-peak ↑ ✗ |
| **M** motility gating | `m(0.2)`: annealed − quenched ≥0.10 | +0.062 ✗ | +0.035 ✗ |

**The predicted order→disorder transition did not appear within the pre-registered
noise range (temp ≤ 1.4) for either model.** In both, `m` declines with noise but never
reaches a disordered phase; the susceptibility never shows a clean interior peak;
control did not round the transition (it slightly *destabilised* it); and motility
barely mattered (the quenched ring ordered nearly as much as the annealed mean field).
By the frozen falsification clause this is outcome **F-flat**: the signature is not
present as specified.

### 1.2 Exploratory characterisation (post-hoc — NOT a pre-registered pass)

The two models fail for *opposite* reasons, which is itself informative:

- **0.5b is too incoherent to order cleanly.** A diagnostic probe (unanimous-neighbour
  prompt) shows it follows the visible majority only **30%** at temp 0.2 and **~15%**
  (≈ the random `1/8`) at temp ≥ 1.0. Its apparent low-temp "order" (`m≈0.66`) is
  substantially **token bias**, not coordination: with a neutral prompt (no neighbours,
  no rewards) the 0.5b output concentrates on niches 0 and 6 so strongly that the
  empirical `m=0.51` at temp 1.0 — as high as the "ordered" phase. Extending the sweep
  to temp 3.5 (exploratory), `m` plateaus at **~0.42**, never reaching the random `0.20`.
- **1.5b is too *coherent* to disorder.** It follows the majority **100% / 85% / 65% /
  50%** at temp 0.2 / 1.0 / 2.0 / 3.5 — a clean, temperature-graded coupling, exactly
  the noise knob the transition needs. Low-temp order is strong and real (`m=0.94`).
  But extending the sweep (exploratory): `m` = 0.94, 0.89, 0.78, 0.73, 0.78, 0.73,
  **0.70** at temp 0.2→4.5 — it **plateaus around 0.70 and never collapses** to the
  disordered phase. There is a shallow **interior χ bump at temp ≈ 2.0** (χ=0.112), but
  with no order→disorder collapse this is at most a **soft crossover, not a clean
  transition.**

So even exploratorily, **no clean transition was located** at either scale. The 1.5b
interior χ bump is suggestive but does not meet the bar to claim a transition (see §1.3).

### 1.3 The symmetric caveat (do not collapse it to one cause)

"No disordered phase; consensus self-sustaining" has **two candidate explanations we
cannot yet distinguish**, and honesty requires holding both:

1. **Real consensus stickiness** that genuinely contradicts the flocking prediction —
   an LLM-agent value economy condenses onto a shared goal that noise does not dissolve.
2. **The noise knob is the wrong kind of noise.** LLM sampling temperature perturbs
   *token sampling* but the neighbour majority is **always fully visible in the prompt**,
   so temperature never *hides or corrupts the alignment signal* the way Vicsek
   alignment-noise does. Vicsek's `η` randomises the *perceived neighbour direction*;
   our temperature only randomises the *response* to a perfectly-perceived majority.
   A model that follows a visible majority even 50% of the time (1.5b at temp 3.5) will
   sustain consensus regardless — so the absence of a transition may be an artifact of
   the knob, not of the physics.

We report the negative as it stands (the pre-registered transition did not appear) and
flag (2) explicitly **without** using it to explain the negative away. **Cleaner
follow-up (exploratory, future):** an alignment-noise knob that randomly resamples or
corrupts a fraction of each agent's neighbour signal (a faithful discrete Vicsek `η`),
rather than LLM temperature. If a transition appears under *that* knob, (2) is
implicated; if it still does not, (1) is supported.

### 1.4 What it would take to claim the transition is real (not done here)

A legitimate positive claim for 1.5b would require **all** of: (a) a clean **interior**
χ maximum (not a boundary rise or a shallow bump over a still-ordered `m`); (b) the
**control-rounding** test passing (`γ>0` rounds the peak — doc 08 §6); and (c) a
**fresh pre-registration** at the corrected noise definition/range, followed by a clean
confirming run. Exploratory *locating* of structure is not validation. We have none of
(a)–(c). Status: **pre-registered negative; exploratory shows at most a soft crossover.**

---

## 2. Signature 1 — demand wave: PRE-REGISTERED CONFOUNDED → exploratory pending

### 2.1 The frozen verdict (0.5b): inconclusive by confound

The pre-registered wave (0.5b, shock on niche `k0=0`) returned **0/3** — but the
leading-edge perturbation was **identically zero** at every round in *both* lag
conditions. The cause is a confound, not a clean null: **niche 0 is the 0.5b model's
single most-favoured token** (§1.2). Many agents sit on niche 0 at baseline from token
bias, so the localized reward-shock on niche 0 produces no detectable perturbation above
that background. The pre-registered wave is therefore **inconclusive (confounded)**, not
a clean negative.

### 2.2 Exploratory re-tests (1.5b, salient reward, bias-controlled) — also confounded, and why

Per the reward-salience check (below), we re-ran the wave at **1.5b** with the reward
**foregrounded** in the prompt and the shock on a **non-favoured** niche — changing
both model and prompt, so these are **exploratory**, not the pre-registered test:

- **Shock niche 3 (1.5b-*favoured*):** the locus adopts the rewarded niche (→0.9), but
  the leading edge jumps to the far boundary (17 sites) **instantly in both L=3 and
  L=0** — agents everywhere adopt niche 3 from token bias, so there is no localized
  propagating front to measure.
- **Shock niche 7 (1.5b-*disfavoured*):** the locus **does not adopt** the rewarded
  niche even with a salient `+5` bonus (stays ≈0.1); far-field stays 0. The shock does
  not take at all.

**The deeper finding (the genuine obstruction): token bias dominates the value-response.**
A localized value-shock cannot create a clean propagating demand wave, because the niche
choice is gated by intrinsic token priors, not the reward: a bias-*favoured* shock niche
is adopted everywhere (no localization), a bias-*disfavoured* one is not adopted even
when explicitly rewarded. The apparent "reward-following" we saw for niche 3 (0.75–0.90,
§3) was **confounded with token preference** — niche 3 is a token the model already
likes. When the reward points at a disliked token, it is ignored.

### 2.3 Status

**Pre-registered 0.5b wave = inconclusive (confounded by bias-niche shock). 1.5b salient
re-tests = exploratory, and also confounded by niche-specific token bias in both
directions.** A clean wave test requires a bias-controlled design (a shock that is not
itself a token-prior signal) **and its own fresh pre-registration** before any positive
could be claimed — same rule as the transition (§1.4). Not done here.

---

## 3. The cross-cutting finding: token bias is the real obstacle

The honest headline of Rung 7 is not "the field theory is true/false on real agents" —
it is that a **methodological obstacle specific to LLM agents** stands between the two:

> **A small LLM's strategy choice is dominated by intrinsic, context-insensitive token
> priors.** These priors (i) **confound the order parameter** — apparent collective
> "order" is partly the model emitting its favourite niche tokens, not value-driven
> coordination (neutral-context `m` reaches 0.51 at 0.5b, 0.40 at 1.5b, with no
> neighbours and no rewards at all); and (ii) **gate the value-response** — explicit
> rewards are followed only when they happen to coincide with a token the model already
> prefers (niche 3: followed; niche 7: ignored despite a `+5` bonus).

This is scale-dependent in *capability* (1.5b coordinates and grades with temperature
far better than 0.5b) but **not eliminated** by scale (1.5b still has strong niche
priors). It means studying LLM-agent populations as value-field systems needs
**bias-controlled instruments** — symbol-randomised niches, an alignment-noise knob that
corrupts perception rather than sampling, larger/more-instructable models — before the
field-theoretic observables (`m`, χ, dispersion) can be read cleanly. That is a
prerequisite the pre-registration did not anticipate, and it is the concrete next step.

## 4. Net status carried forward (precise)

- **Collective-goal transition:** **pre-registered NEGATIVE** (both 0.5b and 1.5b; not
  present at temp ≤ 1.4). Exploratory high-temp shows at most a **soft crossover** (1.5b
  interior χ bump at temp≈2, but `m` never collapses), **not** a clean transition.
  Symmetric caveat: real consensus-stickiness vs. LLM-temperature-as-poor-Vicsek-noise —
  **undistinguished**; cleaner alignment-noise knob is the exploratory follow-up.
- **Demand wave:** **pre-registered INCONCLUSIVE** (0.5b shock fell on the model's
  favourite token). Exploratory 1.5b salient re-tests **also confounded** by
  niche-specific token bias. **Exploratory-pending**, needs a bias-controlled design +
  fresh pre-registration.
- **Neither signature is a validated positive; neither is a clean theory-refutation.**
  The binding obstacle is LLM token bias, not (yet) the physics.

## 5. Consequence for doc 08 and the thread

Rung 7 does **not** clear the real-agent gate, and it does not earn the standalone
speculative preprint (which required the signatures to emerge *with* their derived
gating conditions on real agents — they did not). doc 08 §9's "no empirical content yet
on real agents" stands, now sharpened: a first real-agent attempt was made and returned
a **pre-registered negative (transition) and an inconclusive-confounded result (wave)**,
with the obstacle identified as LLM token bias + a weak noise knob. The honest status of
the field theory is unchanged from after Rung 6: **derived (doc 10) and emergent in a
toy economy (sim/field/dynamic), but not validated on real agents** — and now with a
concrete, named reason the first real-agent test was inconclusive, and a concrete next
instrument (bias-controlled niches + alignment-noise knob) to try.

## 6. Honest limits of this test itself

- **Toy scale** (`N=20–40`, `K=8`, `T≤18`, 0.5b/1.5b). Not thermodynamic-limit; no
  finite-size scaling. A capable, less-biased model at larger `N` might behave
  differently — but per the no-instrument-fishing rule we did **not** escalate past
  1.5b to chase a cleaner peak; 1.5b is a valid instrument showing a real, graded signal.
- **`temp` conflates** sampling stochasticity with reasoning perturbation, and (the §1.3
  point) is not a faithful alignment-noise. This is a design limitation, stated, not a
  result.
- **Susceptibility = time-variance of `m`** over the measured rounds at fixed params (a
  finite-system proxy), seed-averaged over only 2 seeds — noisy. The exploratory χ
  structures are suggestive, not decisive.
- **Reproducible:** all model calls cached (`sim/field/real/results/cache.sqlite`);
  pre-registered verdicts in `real_results_*.json`; exploratory runs in
  `exploratory_*.json`, each labelled exploratory in-file.

# PRE-REGISTRATION — Rung 8, the bias-controlled real-agent field test

**Frozen before any Rung-8 run.** Rung 7 ([`../../docs/11-real-agent-field-test.md`](../../docs/11-real-agent-field-test.md))
returned a pre-registered negative (transition) and an inconclusive-confounded result
(wave), with the obstacle identified as **LLM token bias**: small models emit favourite
niche-*tokens* regardless of value, inflating the order parameter and masking the
value-response. Rung 8 controls that *instrument artifact* and re-runs the test — under
a locked guardrail. Author byline: Cheng Qian. This file's commit precedes any results.

---

## 0. THE LOCKED GUARDRAIL (control the confound, do NOT impose the conclusion)

The point of the real-agent test is: *do the field signatures survive when the
microscopic rule is a real LLM's actual value-behaviour?* There is a sharp line between
removing an **instrument artifact** (legitimate) and **engineering the Vicsek structure
the theory predicts** (self-fulfilling — at the limit it is just `sim/field/dynamic`
with an irrelevant LLM wrapper). This pre-registration commits to the legitimate side:

- **(a) Symbol-randomise niche labels — DONE in the design.** Each agent sees the niches
  under its own *private random label permutation*. The model's preference for a *token*
  (e.g. the digit "3") then maps to a **different true niche for each agent**, so the
  collective token bias cancels — while coordination ("match the majority label you
  see") and reward-reading ("pick the label shown as paying more") are **still processed
  by the model**. This removes the tokenisation artifact, not the value-reasoning.
- **(b) Externally corrupting perceived neighbours — FORBIDDEN in this test.** We do NOT
  hard-substitute the LLM's decision or inject Vicsek alignment-noise by replacing what
  the model sees. The **noise is the LLM's own sampling stochasticity** (temperature);
  the alignment/reward signals are presented faithfully (only relabelled) and the model
  does the actual choosing. (A (b)-style externally-corrupted-neighbour knob may be run
  ONLY later as an explicitly-labelled *toy-limit control*, never as this test.)
- **(c) Bias-controlled shock — DONE in the design.** The wave shock rewards a *true*
  niche, presented in each agent's private label space, so the rewarded niche is not
  itself a fixed token-prior signal.

**Valid Rung-8 real-agent test = (a) + (c) + the LLM still making the real value-decision,
with its own temperature as the only noise.** If the signatures appear under these
conditions → genuine. If not → clean negative.

**THE CAP (frozen).** If this carefully-scoped (a)+(c) test is *also* inconclusive, the
honest verdict is **"the field signatures are not testable with current small LLMs as
agents"** — we STOP. We do **not** escalate to bigger models to fish for a positive.
Rung 7's finding ("small-LLM value-response is dominated by token priors; the physics
question is masked by the instrument") is a keeper regardless. Only a clean,
guardrail-respecting positive earns the standalone preprint.

---

## 1. System (unchanged from Rung 7 except symbol-randomisation)

`N` agents, `K=8` true niches on a circle; order parameter `m=|⟨e^{iθ_true}⟩|` computed
on **true** niches. Payoffs, the alignment dividend, the value-shock, and the control
field `γ` all act in **true-niche space** (the physics is unchanged). The ONLY change:
each agent `a` has a fixed private permutation `π_a`; everything shown to the model
(neighbour tally, per-niche rewards, the agent's own history) is in `a`'s label space,
and the model's chosen label is mapped back to a true niche via `π_a^{-1}`. The model
cannot tell the labels are permuted — coordination and reward-reading are unaffected;
only the *coupling between the model's token prior and a fixed true niche* is broken.

**Model.** `qwen2.5:1.5b-instruct` is the **primary** instrument for Rung 8. Rationale
(not escalation-fishing): Rung 7 established that `0.5b` cannot coordinate at all
(follows a clear majority only ~30%), so it cannot *play* the value game — testing the
*theory* requires a model that can at least coordinate, and 1.5b is the smallest such on
the fleet. `0.5b` is reported only as a capability-floor reference, never as the test.
Per the CAP, we do **not** go beyond 1.5b.

**Noise knob** = LLM sampling temperature (the model's own stochasticity). The Rung-7
caveat stands and is acknowledged, not engineered around: temperature randomises the
*response* to a perceived majority, not the *perception* itself.

Caching, parsing (structured-output JSON), annealed/quenched topology, switching-lag `L`
(reallocation inertia), and the control field `γ` are all as in Rung 7.

---

## 2. Pilot gate (instrument check; run BEFORE §3–§4)

`N=16`, `T=14`, annealed, `γ=0`, symbol-randomised. Proceed only if **all** hold (else
debug, record changes — the pilot is an instrument check, not a hypothesis test):
- **P-parse:** ≥ 90% of outputs parse to a valid label.
- **P-bias-controlled:** neutral-context (no neighbours, no rewards) true-niche
  `m ≤ 0.30` — i.e. symbol-randomisation has pulled the collective token bias down to
  ~random (Rung 7 saw 0.40–0.51 *without* the control). This confirms (a) works.
- **P-coordination:** `m(temp=0.2) − m(temp=2.0) > 0.15` — real coordination still
  produces order at low temp and degrades at high temp (the model still plays the game).

---

## 3. Signature 2 — collective-goal transition (PRIMARY)

1.5b, annealed, `J=1.0`, `γ=0`, symbol-randomised, no shock. Sweep
`temp ∈ {0.2, 0.6, 1.0, 1.4, 2.0, 2.8}` (range widened vs Rung 7, frozen now that we
know `η_c` is high). `N=20`, `T=14`, measure last 7 rounds, `seeds ∈ {0,1}`.
`χ(temp)=N·Var_t(m)`, seed-averaged. Random baseline `m ≈ 0.20`.

| ID | prediction | FROZEN threshold |
|---|---|---|
| **C1** order→disorder | `m` collapses as temp rises | `m(0.2) > 0.55` AND `m(2.8) < 0.35` |
| **C2** susceptibility peak | interior `χ` maximum | interior max, `χ_peak > 1.5 ·` max(endpoint χ's) |
| **C3** control = mass | `γ=0.6` (toward a true `k*`) rounds it | `m(2.8)` rises `≥0.10` vs `γ=0` AND `χ_peak(γ=0.6) < χ_peak(γ=0)` |
| **M** motility gating | annealed orders more than quenched | `m(0.2, annealed) − m(0.2, quenched) ≥ 0.10` |

## 4. Signature 1 — demand wave (SECONDARY)

Ring `N=40`, ring-neighbours `±2`, `J=1.0`, `temp=0.4`, symbol-randomised. At `t0=2`
inject a value-shock on **true** niche `k0` (reward `+5`) for agents within `±2` of
ring-locus `x0=N/2`, presented in each agent's label space (bias-controlled per (c)).
Track adoption of `k0` (true) as a perturbation about baseline; peak position + `σ²`.
Conditions `L ∈ {0,3}`, `T=18`, `seeds ∈ {0,1}`.

| ID | prediction | FROZEN threshold |
|---|---|---|
| **W-wave** (`L=3`) | adoption front **propagates** | peak position `∝ t`, `R²_lin > 0.8`, travels `≥ 4` sites |
| **W-diff** (`L=0`) | spreads **in place** | peak travels `≤ 2` sites AND `σ² ∝ t` beats `∝ t²` |
| **W-gate** | wave gated by inertia | W-wave at `L=3` AND W-diff at `L=0` |

---

## 5. Falsification & outcomes (frozen)

- **Clean positive** (earns the standalone preprint, owner sign-off): C1+C2 pass AND
  (C3 or M) behaves as predicted, under the bias-controlled (a)+(c) design. For the
  wave: W-gate passes. Then the signatures survive a real LLM's value-behaviour with the
  artifact removed → genuine.
- **Clean negative:** with token bias controlled, `m` still does not collapse / no χ
  peak / wave never propagates (or propagates without inertia gating) → the field
  signatures do **not** describe a real-LLM value economy. Relabel doc 08 accordingly.
- **Inconclusive → THE CAP:** if symbol-randomisation also degrades coordination so far
  that no clean signal of either kind is measurable (e.g. pilot P-coordination barely
  holds, `m` low and flat), the honest verdict is **"not testable with current small
  LLMs as agents."** Stop; do not escalate past 1.5b.

Pre-registered (§2–§4) and any exploratory follow-ups are kept strictly separate in the
write-up, as in Rung 7.

## 6. Honest limits (stated now)

- Symbol-randomisation removes the *token→fixed-niche* coupling; it does **not** remove
  any residual *positional* or *ordinal* prior (e.g. a tendency to pick the first listed
  option). If such a residual exists it adds per-agent quenched noise (disorder), so it
  biases against a false positive — acceptable.
- Same toy scale, susceptibility-as-time-variance proxy, 2 seeds, and `temp`-as-noise
  caveats as Rung 7 (`docs/11` §6). Unchanged.
- The per-agent permutation is fixed for a run (quenched): each agent has a constant
  personal label map, so its token prior points at one random true niche all run — these
  cancel across agents in `m` but add a small static disorder, again biasing against a
  false positive.

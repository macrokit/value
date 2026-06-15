# PRE-REGISTRATION — Stage 2 responsiveness gate (frontier-agent)

**Frozen before any run.** The git commit of this file precedes the first results
commit; thresholds, model, protocol, and the decision rule are stated here and applied
mechanically. Author byline: Cheng Qian.

This is the **gate only** — the cheap pre-test that frontier agents engage the coupled
value dynamics at all, before any spend on the full Stage 2 grid (P1–P6 of
`drafts/stage2-proposal.md`, OUT OF SCOPE here). It exists because two pre-registered
small-model attempts (`docs/13`, `docs/18`) died on exactly this failure: the agents
never responded to the incentive (`g`) or control (`γ`) levers — the K=16 population
never left uniform scatter, even at `γ = 18`. The gate answers, for ≈ $10, whether a
capable instrument clears that bar.

---

## 0. What is being tested

Three sign-level sanity checks on whether frontier LLM agents, placed in the exact
Stage-1/2B niche-economy protocol, **respond to the levers the theory's dynamics
require**:

- **G-1 control sanity** — raising the control gain `γ` pulls the population goal
  toward the target `k* = 0` (correct sign).
- **G-2 incentive sanity** — a reward gradient `g` toward an off-target peak pulls the
  population goal toward that peak (correct sign).
- **G-3 perception sanity** — agents condition their stated beliefs on their
  perception signal (use the signal, not the prior).

The gate is **coarse by design**: it tests *engagement with correct sign above a low
bar*, not the quantitative scaling laws (P5/P6) or the capacity-region structure
(P1–P4). A capable agent should clear these bars comfortably; the small-model
instrument cleared none.

**This is deliberately a smaller instrument than the full grid** (N, T, seeds reduced
— §2), because a sign-and-engagement question needs far less power than a scaling
exponent, and the gate is self-funded under a hard cap (§5). The reduction is
pre-stated here, not a post-hoc economy.

---

## 1. Model and provider (frozen)

- **Frontier (the verdict run):** Anthropic Claude **Opus-class** (the owner's top
  available model), via the Anthropic API with the owner's key. The exact model ID is
  recorded in the results writeup (`docs/19-stage2-gate.md`) and in the results JSON.
- **Debug (not a verdict):** Anthropic Claude **Sonnet-class**, used only to shake out
  parsing/protocol bugs before the frontier run. Debug numbers are reported as debug,
  never as the gate verdict.
- Temperature **0.6** (carried from the Stage-1 design). Every call cached
  (`sim/stage2/results/gate_cache.sqlite`, keyed by model/temp/seed/agent/round/prompt)
  — deterministic given the cache, offline-auditable, restart-safe.

## 2. Protocol and frozen scale

**Harness:** the exact Stage-1/2B niche economy (`sim/field/real/llm_economy.py`,
`LLMEconomy`), ported to the API via a cached chat backend with the same cache
contract. **All Stage-1 design invariants carried verbatim:** K = 16 niches, target
`k* = 0`, tent reward landscape `rewards[k] = g·(12 − |k − 12|)` (slope ±g, interior
peak at `k_g = 12`), control `γ` as a bonus at `k*`, **per-agent symbol-randomisation
ON** (mandatory bias control; physics measured in true-niche space), annealed topology
with `n_nb = 6`, coordination dividend `J = 1`, structured JSON output, parse-rate
gate ≥ 0.90.

**Frozen scale (reduced for the gate, pre-stated):** `N = 12` agents, `T = 8` rounds
(4 warm + 4 measured), `S = 4` seeds {0,1,2,3}. Measurements in true-niche space:
`k̄_ss` = mean over measured rounds and seeds of the population-mean niche; `V_ss` =
mean population variance. Uniform-scatter reference for K = 16: mean `(K−1)/2 = 7.5`,
variance `(K²−1)/12 = 21.25`.

**G-3 elicitation protocol:** disjoint structure — 3 agents, agent `j` perceives bit
`j ∈ {0,1,2}` of the 3-bit world state `X` (uniform over 8 states, `I(X;Y_j) = ln 2`).
For each agent and each signal value `v ∈ {0,1}`, elicit a posterior over the 8 states
(JSON, 8 non-negative floats, renormalised mechanically), `R = 8` repeats averaged.
Realised information `Î_j = Σ_v P(v)·KL(p̂_j(·|v) ‖ uniform)` with `P(v) = ½`
(perfect conditioning ⇒ `Î_j = ln 2`).

## 3. Pre-registered pass/fail thresholds (frozen)

| Gate | Condition (frozen) | Pass criterion |
|---|---|---|
| **G-1 control sanity** | `γ = 18, g = 0` (control only, strong lever) | `k̄_ss ≤ 5.5` (≥ 2 niches below the uniform mean 7.5) in **≥ 3/4 seeds** |
| **G-2 incentive sanity** | `γ = 0, g = 0.7` (gradient only, peak at k_g=12) | `k̄_ss ≥ 9.5` (≥ 2 niches above the uniform mean 7.5) in **≥ 3/4 seeds** |
| **G-3 perception sanity** | disjoint elicitation, 3 agents | mean `Î_j ≥ 0.5·ln 2 (= 0.347 nats)` across agents **AND** `Î_j ≥ 0.5·ln 2` for **≥ 2/3** agents |

Rationale for the bars: each is a low, sign-level threshold (a 2-niche shift, half the
channel's information) — chosen so a genuinely responsive agent clears it easily while
a non-responding population (the doc-13/18 outcome: `k̄ ≈ 7.5`, `Î ≈ 0`) fails
unambiguously. The strong levers (`γ = 18`, the full tent gradient) are the correct
test of *engagement*: "can the agent respond at all to a strong push," not "how
precisely does it scale" (that is the grid's job).

## 4. Decision rule (frozen; both outcomes are results)

- **GATE PASS** — **all three** of G-1, G-2, G-3 pass their criteria above. → The
  frontier instrument engages the coupled dynamics with correct signs. The instrument
  is proven; **STOP and report.** The full grid (P1–P6) is a **separate owner go**
  (freeze the grid pre-registration, then run) — NOT part of this charter.
- **GATE FAIL** — any of the three fails. → The frontier instrument does not engage
  the dynamics either; report it as the informative verdict it is (it would retire the
  small-instrument *and* current-frontier route for this protocol, publishable as a
  clean negative). **Name** what would de-CAP it (richer elicitation protocol, larger
  context, different agent scaffolding) — but do **NOT** instrument-fish by tweaking
  thresholds, levers, or scale until it passes. The frozen thresholds bind.

Per-test results are reported with their numbers regardless of outcome; pre-registered
vs any exploratory observation is kept strictly separate.

## 5. Budget (computed) and hard cap

Calls: G-1 `12×8×4 = 384`, G-2 `384`, G-3 `3×2×8 = 48` → **816 frontier calls**
(plus an equal debug pass on Sonnet-class). Token model ≈ 470 in / 50 out per
niche-economy turn, ≈ 430 in / 90 out per elicitation. At list prices:

| Tier | $/M in · out | Gate cost |
|---|---|---|
| Debug (Sonnet-class) | 3 · 15 | ≈ **$1.8** |
| Frontier (Opus-class) | 15 · 75 | ≈ **$8.9** |

**Hard cap: $30 total** (gate + debug + retries). Reaching the cap = stop and report
whatever ran. Frontier sub-cap ≈ $14; debug sub-cap ≈ $9 (per the charter).

## 6. Honest scope and limits (pre-stated)

- **Gate, not grid.** A pass means only that the instrument *can* produce signal; it
  is not evidence for any Stage 2 prediction (P1–P6). A fail does not falsify the
  theory — it bounds the instrument, exactly as docs 13/18 did for small models.
- **Reduced scale.** N=12, T=8, S=4 is powered for a sign question, not a scaling
  regression; this is why the gate cannot and does not report exponents.
- **Single provider/model family.** "Frontier" here = the owner's available Claude
  Opus-class model; a fail is a statement about *this* instrument, and the de-CAP path
  includes other model families.
- **Temperature ≠ OU noise** and **uniform resource weights** — the standing Stage-1
  caveats (`docs/18` §6) carry over.

*Pre-registration commit SHA precedes the results commit SHA — see git log.*

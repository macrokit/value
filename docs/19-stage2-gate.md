# The Stage 2 Responsiveness Gate — GATE PASS: the frontier instrument is proven

> **Maxwell program, Stage 2 pre-test.** The cheap, pre-registered gate that
> [`18`](18-residual-scaling-redo.md) §5 made mandatory before any further spend on the
> `‖Vg‖/γ` question: do the agents engage the coupled value dynamics *at all*? Two
> small-model attempts ([`13`](13-incentive-vs-oversight-real.md), doc 18) died on
> exactly this — their populations never responded to either lever.
>
> Pre-registered in [`sim/stage2/PREREGISTRATION-gate.md`](../sim/stage2/PREREGISTRATION-gate.md)
> (frozen; commit precedes all runs) + one pre-run amendment
> ([`PREREGISTRATION-gate-amendment1.md`](../sim/stage2/PREREGISTRATION-gate-amendment1.md):
> temperature omitted — the frozen models reject the parameter; committed before any
> gate run).
>
> **Verdict: GATE PASS — 3/3 checks, 4/4 seeds each, decisively.** The capability bar
> that closed the small-model era is cleared by a frontier agent. Per the frozen
> decision rule this run **stops here**: the instrument is proven; the full Stage 2
> grid (P1–P6) is a separate, owner-gated go with its own frozen pre-registration.
> Total spend: **$8.76** of the $30 cap.

## 0. The system

The exact Stage-1 niche economy (`llm_economy.LLMEconomy`: K=16 tent landscape,
per-agent symbol-randomisation, J=1, annealed n_nb=6), gate-sized per the frozen
prereg (N=12, T=8 = 4 warm + 4 measured, seeds {0..3}), driven over the Anthropic API
by a cached backend (`sim/stage2/api_client.py`; every call cached; spend metered
against a hard cap before each call). **Verdict model: `claude-opus-4-8`** (frontier).
Debug tier `claude-sonnet-5` (protocol shakeout only, reported as debug). Temperature
omitted per Amendment 1.

## 1. Results against the frozen thresholds

| Gate | Condition | Threshold | Opus 4.8 (verdict) | |
|---|---|---|---|---|
| **G-1 control sanity** | γ=18, g=0 | `k̄_ss ≤ 5.5` in ≥3/4 seeds | k̄ = **0.0, 0.0, 0.0, 0.0** (4/4) | **PASS** |
| **G-2 incentive sanity** | γ=0, g=0.7 | `k̄_ss ≥ 9.5` in ≥3/4 seeds | k̄ = **13.0, 13.0, 13.0, 12.0** (4/4) | **PASS** |
| **G-3 perception sanity** | disjoint elicitation | mean `Î ≥ 0.347`, ≥2/3 agents | Î = **0.693, 0.693, 0.693** = ln 2 exactly (3/3) | **PASS** |

**GATE = PASS.** Parse rate 1.00 on every G-1/G-2 run (niche protocol). The responses
are not marginal: under control the entire population sits *on the target niche*;
under the gradient it sits *on the reward peak*; and the elicited posteriors average
to **exact Bayes** — each agent extracts the full ln 2 of its channel.

## 2. The capability bar, before and after

The same protocol, the same levers, the same bias control:

| Check | qwen2.5-1.5b (docs 13/18) | Sonnet 5 (debug) | **Opus 4.8 (verdict)** |
|---|---|---|---|
| G-1: γ=18 control | k̄ ≈ 7.5 (uniform scatter — no response) | 0.0 | **0.0** |
| G-2: gradient | no response (exponent ≈ 0) | 12–13 | **12–13** |
| G-3: perception | Î ≈ 0 | ln 2 exact | **ln 2 exact** |

The small-model era's binding constraint — "agents capable enough to play the value
game" — is decisively cleared. The doc-18 de-CAP prescription (responsiveness gate +
capable agents) is validated on both counts: the gate caught nothing this time because
there was nothing to catch, and it would have failed the 1.5b instrument outright.

## 3. Honest notes (disclosed, none affecting the verdict)

- **Debug earned its keep.** The first debug pass exposed a truncation bug
  (`max_tokens=64` cut prefaced JSON; one G-3 cell lost 15/16 reps and fell back to
  uniform, landing exactly on the threshold). Fixed (ceilings 200/400 — a cap, not a
  purchase), cache keys made truncation-aware, and the tier re-run clean **before**
  the frontier verdict. This is precisely the mid-tier-shakeout the charter
  prescribed.
- **G-3 parse fails at the verdict tier:** 11/48 elicitation outputs were unparseable
  even at 400 tokens (verbose reasoning prefaces); the surviving ≥9 reps per cell
  average to exact Bayes. G-1/G-2 parsing was perfect. For the grid, the elicitation
  protocol should either raise the ceiling again or instruct terser output — a
  protocol note, not a capability question.
- **The k̄ = 13 texture.** In 3/4 G-2 seeds both models settle at niche 13, one past
  the reward peak (12): the J=1 coordination bonus (up to 1.0) exceeds the 0.7 reward
  gap between adjacent niches, so an off-peak cluster is a stable coordination
  equilibrium. Irrelevant to the gate (threshold 9.5) but directly relevant to grid
  design: at the grid's g values, J-vs-g interplay is part of what the theory's V·g
  drift term must survive — worth a stated note in the grid pre-registration.
- **Amendment 1** (temperature omitted) was forced by the provider, committed blind to
  outcomes, before any run; the noise default (1.0 > 0.6) is the harder-to-pass
  direction.
- **Two transient infra items** during debug, both operational: an HTTP-529 overload
  crash (fixed with exponential backoff; runs resume from cache) and a health-check
  mini-cap misfire (fixed to use the shared cap).

## 4. Budget (audited from the metered cache)

| Tier | Model | Calls | Tokens in/out | Cost (list) |
|---|---|---|---|---|
| Debug (×2 passes: bug + fix) | claude-sonnet-5 | 1,634 | 632k / 22k | $2.23 |
| **Frontier verdict** | claude-opus-4-8 | 817 | 315k / 24k | $6.53 |
| **Total** | | 2,451 | 947k / 46k | **$8.76 / $30 cap** |

## 5. What this does and does not license

- **Licensed:** the full Stage 2 grid (P1–P6 of the proposal) now has a proven
  instrument — the one thing that blocked every prior real-agent attempt. Per the
  frozen rule, **this charter stops here**; the grid is a separate owner go, gated on
  freezing `sim/stage2/PREREGISTRATION.md` (§2–§4 of the proposal + the J-vs-g and
  elicitation-protocol notes above) before its first call.
- **Not licensed:** any claim about the theory. The gate tests *engagement*, not the
  predictions. G-3's exact-Bayes posteriors are encouraging texture for the gap-law
  test and nothing more; P1–P6 remain genuinely uncertain, and a negative will be
  published per the standing rule.

*Author byline: Cheng Qian. Pre-registration (`a159ca9`) and Amendment 1 (`4a8c376`)
commits precede this results commit — see git log. All numbers re-derive from
`sim/stage2/results/` (cached, offline-auditable).*

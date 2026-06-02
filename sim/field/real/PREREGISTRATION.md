# PRE-REGISTRATION — Rung 7, the real-agent field test

**Frozen before any experimental run.** This file fixes the design, the measurements,
and the PASS/FAIL thresholds for the decisive test of the wave/field theory of value
(doc 08) on **real LLM agents**. It is written in the same discipline as the v2
pre-registration: thresholds are committed *first*, the falsification criterion is
stated up front, and a negative result is a real, publishable finding (the honesty
rule of this thread — physics-envy is the failure mode).

Git commit of this file precedes the commit of any results. Author byline: Cheng Qian.

---

## 0. The claim under test, and what would falsify it

Thrust A ([`docs/10`](../../../docs/10-field-theory-derivation.md)) **derived** the
telegrapher wave and the Toner–Tu transition from the *discrete* value dynamics, under
two gating conditions (reallocation **inertia** for the wave; **motility** for the
transition, with control as a **mass**). Thrust B
([`sim/field/dynamic/`](../dynamic/)) showed both **emerge** from a *toy* agent economy
whose update rule is a hand-coded replicator. **Rung 7 replaces the hand-coded rule
with a real small LLM** choosing each agent's strategy each round, and asks: *do the
wave and the transition survive — with their derived gating conditions — when the
microscopic rule is emergent model behaviour rather than an equation?*

**This is the on-target test** (AI-agent populations are the theory's claimed domain),
deliberately chosen over found market/social data (which is stretch-analogy and the
graveyard of sociophysics — Castellano et al.). Found data is at most secondary,
caveated corroboration, never the primary test.

**Falsification (frozen).** Any of the following ⇒ the field theory does **not**
describe real agent populations; we report the negative and relabel doc 08 §3/§5 from
"derived + emergent" to "suggestive analogy that fails on real agents":
- **F-flat:** the collective-goal order parameter `m` does **not** collapse across the
  noise sweep (no order→disorder), or there is **no interior susceptibility peak**.
- **F-nogate-motility:** ordering does **not** require motility (quenched low-D orders
  as well as annealed), i.e. the derived Mermin–Wagner gating is absent.
- **F-diffusiononly:** an injected value-shock **never** propagates (pure diffusion at
  all reallocation lags) — no wave at all.
- **F-nogate-inertia:** a wave appears **even at zero reallocation lag** (propagation
  is not gated by inertia), i.e. the derived telegrapher condition is absent.
- **F-unparseable:** real-LLM outputs cannot be made to yield valid strategy choices at
  ≥90% parse rate (the agents can't play the game) — then the test is inconclusive, not
  negative, and we report that honestly.

A PASS requires the signatures to emerge **with** their derived gating conditions
behaving as predicted — not merely the signatures alone.

---

## 1. The system (frozen)

`N` LLM agents in a shared niche-economy over `T` discrete rounds.

- **Niches.** `K = 8` niches arranged on a circle; niche `k` has angle `θ_k = 2πk/K`.
  An agent's current niche is its **goal director**. The collective-goal **order
  parameter** is `m = |(1/N) Σ_a e^{iθ_{k_a}}| ∈ [0,1]` (1 = all agents on one niche /
  aligned, 0 = uniformly scattered).
- **The microscopic rule = a real LLM.** Each round, **each agent's next niche is
  chosen by `qwen2.5:0.5b-instruct`** (China-Mac Ollama fleet) given a prompt
  containing: the `K` niches and their current rewards; the agent's own recent
  choices+payoffs; and its neighbours' most recent choices+payoffs. The model outputs a
  single integer `0..K-1`. **No replicator equation, no alignment formula** governs the
  choice — only the model's reading of payoffs and neighbours. (Robustness re-run on
  `qwen2.5:1.5b-instruct` if time permits; pre-registered as secondary.)
- **Payoff (what the economy rewards), computed by the harness, shown to the LLM:**
  `payoff_a = J · (fraction of a's neighbours on the same niche as a)   [alignment dividend, the coupling]`
  `         + R_{k_a}                                                   [niche base reward; the value-shock bumps one R_k]`
  `         + γ · 1[k_a = k*]                                           [optional control field toward principal niche k*; the mass term]`
  Alignment dividend `J=1.0` fixed. Coordinating with neighbours pays — the ordering
  pressure. Noise is **not** added by hand; it is the **LLM sampling temperature**.
- **Noise knob = LLM sampling temperature** `temp`. Low temp → the model reliably picks
  the payoff-maximising (coordinate-with-neighbours) niche → order. High temp → noisy
  choices → disorder. This is the field theory's `η`.
- **Topology / motility.** Two regimes, frozen:
  - **annealed ("motile"):** each round each agent sees a *fresh random sample* of
    `n_nb = 6` other agents — effective re-linking, the high-connectivity / mean-field
    limit that *can* order. Used for the primary transition test.
  - **quenched ("fixed"):** each agent sees fixed ring-adjacent neighbours (`±3`,
    low-dimensional, quenched). Used for the motility-gating contrast (Mermin–Wagner
    expects this to *resist* ordering).
- **Reallocation inertia (for the wave) = a switching commitment lag `L`.** An agent
  that changed niche must keep it for `L` rounds before changing again (momentum in
  reallocation). `L=0` = free switching (the inertia-free limit, diffusion expected);
  `L>0` = momentum (wave expected). This is the emergent analogue of the toy's flow lag
  `τ_J`.
- **Caching.** Every model call is cached by `sha256(model, temp, prompt, agent_id,
  round, seed)` so runs are re-runnable offline and the verdict is auditable. The seed
  + id + round in the key make each call a distinct, reproducible stochastic draw.

---

## 2. Signature 2 — collective-goal transition (PRIMARY; cheaper, run first)

Annealed topology, `J=1.0`, `γ=0`, no value-shock (uniform niche rewards `R_k=0`).
Sweep `temp ∈ {0.2, 0.6, 1.0, 1.4}`. `N=20`, `T=12`, measure on the last 6 rounds;
average over `seeds ∈ {0,1}`. Susceptibility `χ(temp) = N · Var_t(m)` (time-variance of
the order parameter over the measured rounds, averaged over seeds).

| ID | prediction | FROZEN threshold to PASS |
|---|---|---|
| **C1** order→disorder | `m` collapses as `temp` rises | `m(0.2) > 0.55` AND `m(1.4) < 0.35` |
| **C2** susceptibility peak | `χ(temp)` peaks at an interior `temp_c` | interior max, `χ_peak > 1.5 ·` max(endpoint χ's) |
| **C3** control = mass | `γ>0` rounds the transition | with `γ=0.6` toward `k*`: `m(1.4)` rises by `≥0.10` vs `γ=0`, AND `χ_peak(γ=0.6) < χ_peak(γ=0)` |
| **M** motility gating | ordering needs motility (annealed) | `m(0.2, annealed) − m(0.2, quenched) ≥ 0.10` |

## 3. Signature 1 — demand wave (SECONDARY)

Ring of `N=40`, ring neighbours `±2`, `J=1.0`, `γ=0`, `temp=0.4` (low, to track a clean
front). At round `t0=2` inject a value-shock: niche `k0=0` gets reward `R_{k0}=3.0` for
agents within `±2` of ring-locus `x0=N/2` (a localized "this niche is suddenly
valuable here"). Track, per round, the ring profile of *adoption of `k0`* (fraction of
agents at each ring position on niche `k0`), as a perturbation about baseline; record
its **peak position** (does the adoption front travel?) and **second moment `σ²`**.
Conditions: lag `L ∈ {0, 3}`. `T=18`, `seeds ∈ {0,1}`.

| ID | prediction | FROZEN threshold to PASS |
|---|---|---|
| **W-wave** (`L=3`) | adoption front **propagates** | peak position `∝ t` with `R²_lin > 0.8` AND peak travels `≥ 4` ring-sites over the window |
| **W-diff** (`L=0`) | spreads **in place** (diffusion) | peak travels `≤ 2` sites (pinned) AND `σ² ∝ t` fits better than `∝ t²` |
| **W-gate** (inertia) | wave **gated by inertia** | W-wave holds at `L=3` AND W-diff holds at `L=0` |

---

## 4. Pilot gate (cheap; run BEFORE §2–§3)

`N=12`, `T=8`, annealed, `γ=0`, two temps `{0.2, 1.4}`, one seed. Proceed to the full
runs **only if** both hold; otherwise debug prompts/parsing first and record what was
changed (the pilot is not a hypothesis test, it is an instrument check):
- **P-parse:** `≥ 90%` of LLM outputs parse to a valid niche `0..K-1`.
- **P-signal:** `m(0.2) − m(1.4) > 0.10` (real LLM choices show *some* temp-dependent
  ordering — enough to justify the full sweep).

## 5. Scope and honest limits (stated now, not after seeing results)

- **Toy-scale, real-rule.** `N∼20–40`, `K=8`, `T∼12–18`, a 0.5B model. This upgrades
  the *microscopic rule* from equation to real model; it does **not** claim
  thermodynamic-limit critical exponents (that needs finite-size scaling across `N`,
  out of scope here) nor a real *market*. A PASS means: *the field-theoretic signatures
  and their derived gating conditions survive a real-LLM microscopic rule at toy scale.*
- **Susceptibility = time-variance of `m`** at fixed params (a finite-system proxy for
  the fluctuation peak), averaged over seeds — not an ensemble heat-capacity. Pre-
  registered as such.
- **Motility = re-linking (annealed neighbours)**, the network analogue of Vicsek
  motion; "quenched" = fixed ring. Mermin–Wagner is asymptotic, so the gating test is
  **directional** (annealed orders more than quenched), not a claim about the `N→∞`
  limit. Pre-registered as directional.
- **`temp` as `η`** conflates sampling stochasticity with any temperature-induced shift
  in the model's reasoning. We treat `temp` purely as the noise knob and do not claim
  it is a thermodynamic temperature.
- **Only if the signatures emerge WITH their gating conditions** is the standalone
  speculative preprint (byline Cheng Qian, separate from the core paper) earned — and
  only with owner sign-off. A partial or negative result is written up honestly in
  `docs/11-real-agent-field-test.md` and the thread is relabelled accordingly.

# PRE-REGISTRATION — Stage 2: the decisive coupled-fleet test on frontier agents

**Frozen before any experimental run.** The git commit of this file precedes the first
results commit; predictions, bands, protocols, budget cap, and the decision rule are
stated here and applied mechanically. Author byline: Cheng Qian.

**Lineage.** This freezes §2–§4 of `drafts/stage2-proposal.md`, amended by the gate
findings of [`docs/19`](../../docs/19-stage2-gate.md). Prior chain: the synthetic
coupled-regime pilot passed 15/15 ([`docs/17`](../../docs/17-coupled-fleet-pilot.md));
two small-model attempts CAP'd on agent non-response
([`docs/13`](../../docs/13-incentive-vs-oversight-real.md),
[`docs/18`](../../docs/18-residual-scaling-redo.md)); the pre-registered
responsiveness gate then **passed 3/3 on the frontier instrument**
(prereg `a159ca9` → amendment `4a8c376` → results `0759c4b`) — the owner has funded
and authorised the full grid. This is the test the v5 paper names as its
continuation gate (Discussion, *The decisive prediction*).

**Expectation, stated honestly:** genuinely uncertain. The synthetic pilot validated
only the math and the design. The small-model trends leaned against prediction (ii)
but never engaged the dynamics; the gate proves the frontier instrument engages them.
Pass or fail, the result is published with equal prominence.

---

## 1. Instrument (frozen)

- **Model (all verdict runs): `claude-opus-4-8`** via the Anthropic API (owner-funded).
  Debug/protocol shakeout may use `claude-sonnet-5`; debug numbers are never verdicts.
- **Amendment-1 carryover:** `temperature` omitted (the models reject the parameter);
  noise = the model's own sampling.
- **Backend:** `sim/stage2/api_client.py` — every call cached
  (`results/gate_cache.sqlite`), deterministic given the cache, restart-safe; spend
  metered per call against the hard cap (§6) with pre-call abort.
- **max_tokens ceilings** (caps, not purchases): niche-economy turns 200; belief
  elicitation 600 with a terser-output instruction (gate lesson: 11/48 elicitations
  exceeded 400 via verbose prefaces).

## 2. Experiment 2A — capacity region & gap law (prediction i)

**World:** `X = (b₂,b₁,b₀)`, three iid fair bits (8 states, uniform `q`);
`H(X) = 3 ln 2 ≈ 2.0794` nats. Reference odds fair vs `r = q`.

**Perception structures** (ported from the validated pilot; channel `I` exact by design):

| ID | agents & signals | notes |
|---|---|---|
| (a) disjoint | 3 agents; agent `j` sees bit `b_j` | `I = ln2` each |
| (b) overlap | 3 agents; see `(b₀,b₁)`, `(b₁,b₂)`, `(b₀,b₂)` | pairs saturate `3ln2` |
| (c) clones | agents 1,2 both see `b₀`; agent 3 sees `b₁` | clone adds 0 |
| (d) noisy | 3 agents; agent `j` sees `b_j` through a stated 10%-flip sensor | `I = 0.3681` each |
| (e) XOR control | reduced world `X' = b₀`; agent 1 sees an independent fair bit `c`; agent 2 sees `b₀⊕c` | `I = 0` each; joint `ln2` |

**Belief elicitation (primary protocol):** for each structure × agent × signal value,
the agent gets the world rules, its channel description (including sensor noise where
applicable), and its observed signal; it returns a probability vector over the world
states (JSON floats; renormalised mechanically; **12 repeats per cell averaged**;
parse-failed repeats dropped and counted; a cell with < 6 surviving repeats fails the
protocol gate and is reported).

**Analysis (exact enumeration, no MC noise):** with reported posteriors `p̂_a(x|y)`:
- `Î_a = Σ_y P(y) · KL(p̂_a(·|y) ‖ q)` — realized information of agent `a`'s reports.
- **Coalitions:** naive-Bayes product fusion
  `p̂_S(x|y_S) ∝ q(x) · Π_{a∈S} [p̂_a(x|y_a)/q(x)]`;
  `Ĝ_S = Σ_{x,y_S} P(x,y_S) · ln(p̂_S(x|y_S)/q(x))` over the exact joint.
- **Parimutuel (equal weights):** `Ĝ_a = Σ P(x,y_all) · ln(b_a(x)/B(x))` with
  `b_a = p̂_a`, `B = (1/m)Σ_a b_a`.

**Live-market run (secondary, dynamic):** structures (a) and (c); 3 agents each;
**40 rounds × 5 seeds**; each round every agent sees its signal, its wealth, and last
round's market odds, and outputs its bet allocation (JSON floats over the 8 states;
renormalised); parimutuel wealth update, zero-sum in shares, no take.

## 3. Experiment 2B — residual scaling ‖Vg‖/γ (prediction ii)

**Identical frozen design to Stage 1** (comparability deliberate): K = 16 niches,
`k* = 0`, tent landscape `rewards[k] = g·(12 − |k−12|)`, γ bonus at `k*`, N = 20,
T = 18 (6 warm + 12 measured), J = 1, annealed `n_nb = 6`, per-agent
symbol-randomisation ON, grid **g ∈ {0.25, 0.7, 2.0} × γ ∈ {2, 6, 18}**, seeds
{0..7}, direction arms at B1 (γ=6, g=0.7) and B2 (γ=18, g=0.7) with δ = 0.5
(arms: γ+δ and g−δ; r0 reused from the grid).

**Regime rule:** the Stage-1 rule verbatim (V_ss ≥ 5.31; k̄_ss ≤ 10; agent-rounds
above the peak ≤ 0.20; parse ≥ 0.90; residual > 0) **plus the doc-18 uniformity
clause** — a condition with `V_ss` within ±25% of 21.25 **and** `k̄_ss` within ±1 of
7.5 is named "non-responsive", a distinct outcome from saturation. Regression needs
≥ 6 in-regime conditions spanning ≥ 4× in `V·g/γ`, else the scaling verdict is
CAP("insufficient in-regime span").

**Known systematic, pre-stated (gate finding):** with J = 1 and the grid's g values,
coordination can lock the population one niche off a reward optimum (adjacent-niche
reward gaps < J) — a ±1-niche granularity on `k̄_ss`. The frozen bands below already
tolerate a constant offset (free-exponent fit; C unconstrained); we pre-state this as
an honest limit rather than altering any threshold.

## 4. Pre-registered predictions and bands (frozen)

**Prediction (i) — 2A:**

| ID | Prediction | Band |
|---|---|---|
| **P1 gap law** | parimutuel `Ĝ_a − Ĝ_b = Î_a − Î_b`, all pairs, structures (a)–(d) | worst pairwise deviation ≤ **0.05 nats** |
| **P2 submodularity** | `Ĝ_S` diminishing-returns for (a)–(d); **supermodular** in (e) | margins ≥ **−0.03**; (e) gap ≥ **ln2/2** |
| **P3 joint ceiling** | `Ĝ_S ≤ H(X)` all coalitions, all structures | slack **0.02** |
| **P4 selection (live market)** | terminal wealth ordered by `Î_a`; clones' terminal wealth equal | ordering in ≥ **4/5 seeds** per structure; clone gap ≤ 10% of mean share |

**Prediction (ii) — 2B:** the Stage-1 frozen conventions verbatim:

| ID | Prediction | Band |
|---|---|---|
| **P5 exponents** | `residual ∝ g^p γ^q`, theorem (p,q) = (+1,−1) | free log-log fit on in-regime condition means: `p ∈ [0.6,1.4]`, `q ∈ [−1.4,−0.6]`, `R² ≥ 0.70`; seed-bootstrap 95% CIs (2000 resamples); signal gate `R_across > 3σ_in` (raw seed-std); mean ratio vs `V·g/γ` ∈ [0.33, 3.0] |
| **P6 direction** | incentive beats oversight in the incentive zone | `eff_g/eff_γ > 1` at B1 and B2, all four arm signals above the noise floor `σ_in·√(2/8)` |

**Decision rule (as printed in the v5 paper; applied mechanically, in order):**

1. **PASS** — P1–P3 pass and P5 passes (P4/P6 reported as supporting): the
   unification predicts coupled-regime structure none of its components predicts, on
   real capable agents — it earns the stronger word.
2. **CLEAN NEGATIVE** — the instrument engages (gate already passed; 2B conditions
   not majority non-responsive) but P1/P2/P5 fail their bands with the deviation
   systematic by the Stage-1 addendum discriminator (alternative-law fit R² ≥ 0.70,
   `R_across > 3σ_in`, leave-one-out stable, anti-default clause): the
   distinctively-unified layer of the theory **retires**, published with the same
   prominence a positive would receive. P1-specific: a worst-pair deviation > 0.05
   with per-cell elicitation SE < 0.02 (from repeat scatter) is a clean miss;
   larger SE → protocol-CAP.
3. **CAP** — otherwise (named gate: non-estimable elicitation, insufficient in-regime
   span, majority non-responsive conditions, or budget stop). State what would
   de-CAP.

Scaling (P5) and direction (P6) verdicts are reported separately, as in Stage 1.
Pre-registered vs exploratory is strictly separated throughout.

## 5. Protocol gates (cheap aborts, pre-stated)

- **Parse gate:** any 2B condition with parse < 0.90 is excluded (Stage-1 rule);
  if > 2 of 9 grid conditions fail parsing, stop and report (instrument fault).
- **Elicitation gate:** any 2A cell with < 6/12 surviving repeats → that structure is
  protocol-CAP'd (reported, not fitted).
- **Budget stop (§6):** reaching the cap = stop; whatever is complete is analysed and
  published; incomplete parts reported as budget-stopped.

## 6. Budget (computed at current real prices) and hard cap

Gate audit calibration: the gate's 817 Opus calls billed ≈ $3.7 total-month vs $6.5
on the conservative meter — real Opus 4.8 pricing ≈ **$5/M in, $25/M out** (the
meter's price table is updated to these; it remains the enforcement instrument).

| Component | Calls | Est. tokens in/out | Est. cost (Opus @ 5/25) |
|---|---|---|---|
| 2A elicitation (5 structures, ≤4 signal values × ≤3 agents × 12 reps) | ~1,100 | 0.5M / 0.15M | ≈ $6 |
| 2A live market (2 × 3 agents × 40 rounds × 5 seeds) | 1,200 | 0.7M / 0.12M | ≈ $7 |
| 2B grid (9 × 8 × 20 × 18) | 25,920 | 11.7M / 1.3M | ≈ $91 |
| 2B direction arms (4 × 8 × 360) | 11,520 | 5.2M / 0.6M | ≈ $41 |
| **Total** | ≈ 39,700 | ≈ 18.1M / 2.2M | **≈ $145** |

**Hard cap: $160 on the meter** (pre-call abort). Order of spend: 2A first (cheap,
independent), then 2B grid, then arms — so a budget stop preserves the most complete
publishable unit. Runtime estimate ≈ 4–6 h (pool 6, restart-safe).

## 7. Honest limits (pre-stated)

- **Single model family/provider.** All verdict runs on one frontier model; results
  are statements about *this* instrument class. Replication on another family is
  future work.
- **Elicited beliefs ≠ incentivised beliefs.** 2A's primary protocol asks for stated
  posteriors; agents are not paid for calibration. The live market (P4) partially
  covers the acting-vs-reporting gap at small scale.
- **Fusion rule is naive-Bayes** — exact for (a)–(d) by conditional independence,
  and deliberately *wrong* for (e); that asymmetry is the P2 control's point.
- **2B inherits Stage-1 caveats** (uniform resource weights; toy scale; prompt-γ ↔
  theorem-γ calibration absorbed into C) plus the ±1-niche coordination granularity
  (§3).
- **Elicitation repeats share no seed variation** (temperature fixed at provider
  default); repeat scatter is sampling noise only.

*Pre-registration commit SHA precedes the results commit SHA — see git log.*

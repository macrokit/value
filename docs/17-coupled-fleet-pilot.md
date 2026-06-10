# The Coupled Fleet, Measured — Maxwell Stage 0 (synthetic pilot)

> **Maxwell program, Stage 0** (`docs/ROADMAP.md` ⊕ The Maxwell program). The
> correctness audit ([`04`](04-multi-agent-capacity-region.md) §2 erratum) showed the
> sum-form fleet ceiling was false **because the base model lacked payout coupling** —
> so the correction itself defines the experiment: implement the coupling explicitly
> and measure the region. This pilot is that implementation, synthetic-first.
>
> Pre-registered in [`sim/coupled/PREREGISTRATION_stage0.md`](../sim/coupled/PREREGISTRATION_stage0.md)
> (committed before any run; SHA precedes this results commit).
>
> **Result: 15/15 pre-registered checks pass** — the corrected coupled-regime
> predictions hold in an explicit implementation, the erratum's counterexample
> reproduces numerically, and the designed control (where the theory predicts its own
> precondition must break) breaks exactly as predicted. **Status: necessary, not
> sufficient** — this validates the corrected math and the Stage-2 experimental design,
> not the theory on real agents (§5).

## 0. The system

Pure numpy ([`sim/coupled/coupled_fleet.py`](../sim/coupled/coupled_fleet.py)), seeded,
no model calls; every number re-derivable offline from
[`results/stage0.json`](../sim/coupled/results/stage0.json). Three experiment sets, one
per coupled-regime claim.

## 1. E6 — shared bankroll: coalition value is fused information (6/6)

One pooled bankroll bets the fused posterior `p(x|Y_S)` for every coalition
`S ⊆ {1..m}`, in a 3-bit world (`H(X) = 2.079` nats), across five designed overlap
structures: disjoint bits, partial overlap, clones, noisy (BSC 0.1), and an XOR-synergy
control.

| Check | Prediction | Measured |
|---|---|---|
| E6.0 | **erratum counterexample**: private-bankroll clones `Σ_a G_a = 2ln2 > I(X;Y₁₂) = ln2` | `Σ Ĝ = 1.3863` vs `I = 0.6931` ✓ |
| E6.1 | `Ĝ_S = I(X;Y_S)` for **all** coalitions, all structures | worst `|Ĝ−I| = 0.0026` nats ✓ |
| E6.2 | monotone in `S` | all nested pairs ✓ |
| E6.3 | corrected joint ceiling `Ĝ_S ≤ H(X)` | all coalitions ✓ |
| E6.4 | **submodular** (diminishing coalition returns) where channels are cond.-independent given `X` | worst margin `−0.0029` (= MC noise) ✓ |
| E6.5 | submodularity **fails** in the XOR control (precondition violated) | supermodular gap `= 0.6931 = ln2` exactly ✓ |

Read together: the un-coupled model *violates* the sum form exactly as the erratum says
(E6.0), while the **pooled** fleet obeys the corrected ceiling and the submodular
coalition structure (E6.1–E6.4) — and the submodularity precondition (conditional
independence given the world) is load-bearing, not decorative: build a synergistic
channel pair and coalition value turns supermodular by exactly `ln2` (E6.5). Two agents
individually worthless (`I = 0` each) are jointly worth one full bit — coalition
synergy is real where perception channels are entangled.

## 2. E7 — parimutuel coupling: the regime where a sum-form is true (6/6)

Agents bet **against each other**: odds form from aggregate bets
(`B(x) = Σ_a w_a b_a(x)`), the pool pays winners pro rata — zero-sum in wealth shares.
Four BSC agents, `ε ∈ {0.05, 0.15, 0.30, 0.45}`, `I_a ∈ {0.495, 0.270, 0.082, 0.005}`.

| Check | Prediction | Measured |
|---|---|---|
| E7.1 | wealth shares conserved exactly | error `0.0` (machine precision) ✓ |
| E7.2 | **gap law** `G_a − G_b = I_a − I_b` (the common market term cancels) | worst pairwise deviation `0.0016` nats ✓ |
| E7.3 | growth ordered by `I_a` | exact ordering, 10/10 reps ✓ |
| E7.4 | **aggregate collapses**: `mean_a G_a < 0` coupled, vs `Σ G_a = ΣI_a = 0.852 > 0` uncoupled | coupled `−0.0888 ± 0.0001`; uncoupled `0.857` ✓ |
| E7.5 | clones' edges cancel (equal growth; edge competed away) | `|Ĝ₁−Ĝ_clone| < 10⁻⁵`; drop `0.061 ± 0.0002` ✓ |
| E7.6 | wealth selection: best-informed agent absorbs the pool | 10/10 reps; mean final share **1.000** ✓ |

Three structural points worth naming:

- **The gap law is the cleanest coupled-regime prediction in the pilot.** Under
  parimutuel coupling, *relative* growth is purely informational —
  `G_a − G_b = I_a − I_b`, with everything about the market common-mode and cancelled.
  Measured to 1.6 millinats. This is a sharp, quantitative, *coupled-regime* analog of
  the single-agent capacity theorem, and a direct Stage-2 target.
- **The coupling is what makes a sum-form constraint true.** The same four agents whose
  private-bankroll growths sum to `+0.85` nats/round sum to `−0.09` under parimutuel
  coupling — aggregate value creation in a zero-sum payout structure collapses to ≤ 0
  (Jensen), exactly the assumption-scoped statement the corrected doc 04 §2 makes.
- **Selection is total, and it is the efficient-market mechanism in miniature.** The
  evolving-wealth run concentrates the entire pool onto the best-informed agent (E7.6);
  as its share → 1 the market odds → its beliefs and every edge (including its own)
  vanishes. Value-as-relative-information is self-extinguishing under this coupling —
  the market "learns" by transferring wealth to whoever perceives best.

## 3. E8 — alignment curves the region (3/3; first numerical check of doc 04 §4)

Two agents share one effort budget; each works along its own goal; work spills into the
other's goal-progress with sign `cos θ_ab`. Sweep `cos θ ∈ {−0.8 … +0.8}` × 21
allocations.

| Check | Prediction | Measured |
|---|---|---|
| E8.1 | sum-frontier `= (1+cosθ)·μ` | worst rel. error 0.2% ✓ |
| E8.2 | region pointwise-ordered by alignment (bulge / conflict tax) | all pairs, all allocations ✓ |
| E8.3 | egalitarian point `= ((1+cosθ)/2)·μ` | worst rel. error 0.04% ✓ |

The cooperation dividend and conflict tax of doc 04 §4 — region bulges outward for
aligned goals, contracts for opposed ones — hold quantitatively in a concrete coupled
implementation. **This is the weakest of the three sets** (the model's expectation is
analytic, so the check validates implementation and geometry rather than an independent
law); it is included because §4's claim had never been instantiated at all.

## 4. What this validates for Stage 2

The Stage-2 design (real frontier agents in a payout-coupled economy) needs exactly the
machinery exercised here, and all of it now has a validated synthetic reference:

1. **Counterfactual coalition throughputs** (run every `S`, compare to fused `I`) — E6.
2. **Designed overlap structures** (disjoint / partial / clone / noisy / synergistic) —
   E6, with the submodularity-vs-synergy contrast as the discriminating probe.
3. **Parimutuel mechanics** with exact conservation and the gap-law readout — E7. The
   gap law in particular gives Stage 2 a *quantitative* target that does not require
   absolute calibration (the market common-mode cancels).
4. **Region-shape probes** under varied alignment — E8.

## 5. What this does NOT show (read before citing)

- **It is synthetic and largely circular.** The worlds, channels, and payout rules are
  built from the corrected model's own assumptions; agents bet exact Bayes posteriors.
  Like E1–E5, passing is *necessary* for the theory and the implementation to be
  coherent — it is **not evidence the theory describes any real system**. The
  real-agent test is Stage 2, which is gated on its own pre-registration and budget.
- **No learning, no goals-in-motion, no strategic behaviour.** Agents are fixed
  posterior-bettors; nobody distorts bets to manipulate parimutuel odds (real agents
  might — strategic bet-shading is a known wrinkle of real parimutuel markets and is
  absent here by construction).
- **E8 is nearly definitional** (§3) — treat it as an implementation check of doc 04
  §4's geometry, not a discovery.
- **The exact capacity region remains open** (doc 04 §7). The pilot measures
  achievability points and outer-bound compliance for specific structures; it does not
  characterize `𝓡` in general.
- **Finite-precision caveat**: tolerances (0.01–0.03 nats) are 4× MC standard error at
  the registered T; sub-tolerance deviations from the exact laws are not resolvable
  here and were not claimed.

## 6. Verdict

**15/15 pre-registered checks pass** ([`stage0.json`](../sim/coupled/results/stage0.json)).
The corrected coupled-regime mathematics of doc 04 §2 — fused-coalition achievability,
the joint ceiling, conditional submodularity (and its designed failure), the
parimutuel sum-collapse, and the relative-growth gap law — are all confirmed in an
explicit payout-coupled implementation, and the experimental design for the real-agent
Maxwell test (Stage 2) is validated. The next rung on this thread is **Stage 1** (the
`‖Vg‖/γ` redo with a de-saturated design — see
[`13`](13-incentive-vs-oversight-real.md) §5), and then Stage 2 itself, both gated on
their own pre-registrations.

*Author byline: Cheng Qian. Pre-registration commit SHA precedes this results commit —
see git log. All numbers re-derive from `sim/coupled/coupled_fleet.py` (seeded, offline).*

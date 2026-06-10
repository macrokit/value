# Alignment as a Stability Condition — the Coupled-Flow Theorem

> Promotes the conjecture of [`05-dynamics.md`](05-dynamics.md) §4 to a result. Doc 05 said *alignment is a
> dynamical stability condition, not a static property*, and guessed a threshold. Here we set up the coupled
> control + selection dynamics, solve the mean-field fixed point in closed form, and get a sharp stability
> criterion **and** a formula for the residual misalignment the conjecture did not have. This is the Tier-2
> theoretical result flagged in `STRATEGY.md` §2 — the one most relevant to AI alignment.

## 1. The coupled system

A fleet of `m` agents. Agent `a` has a **goal vector** `k_a` in goal-space and a **resource share** `w_a ≥ 0`,
`Σ_a w_a = 1`. The principal has a target goal `k*`. The object of interest is the fleet's **effective goal**

$$\bar k \;=\; \sum_a w_a\, k_a .$$

Two forces act ([`05`](05-dynamics.md) §3):

- **Control (alignment design).** Each goal is pulled toward the target with gain `γ > 0`:
  $$\dot k_a\big|_{\text{ctrl}} = -\,\gamma\,(k_a - k^\*).$$
- **Selection (replicator).** Compounding ([`02`](02-coding-theorem-of-value.md) §1) reweights toward
  higher-growth agents:
  $$\dot w_a = w_a\,(G_a - \bar G),\qquad \bar G = \sum_b w_b G_b,$$
  where `G_a = G(k_a)` is the environment's growth rate for goal `k_a`.

The environment's reward landscape over goals is summarized, to first order around the operating point, by its
**growth gradient** `g := ∇_k G` — the direction in goal-space along which deviating from `k*` *increases*
resource capture. `g = 0` means the environment rewards exactly the target goal; `g ≠ 0` means resource capture
pulls goals off-target.

## 2. Mean-field dynamics of the effective goal

The selection term's effect on `\bar k` is given exactly by **Price's equation**: the rate of change of a
population mean under selection is the covariance between the trait and fitness,

$$\dot{\bar k}\big|_{\text{sel}} \;=\; \mathrm{Cov}_a\!\big(k_a,\, G_a\big) \;=\; \sum_a w_a (k_a-\bar k)(G_a-\bar G).$$

Linearizing growth about the mean, `G_a \approx \bar G + g^\top (k_a - \bar k)`, the covariance becomes

$$\dot{\bar k}\big|_{\text{sel}} \;=\; V g,\qquad V := \mathrm{Cov}_a(k_a) \text{ (the goal-dispersion matrix)}.$$

Adding control, the effective goal obeys

$$\boxed{\,\dot{\bar k} \;=\; -\,\gamma\,(\bar k - k^\*) \;+\; V g.\,}$$

Control restores toward `k*`; selection drives along `Vg` — the goal-dispersion projected onto the reward
gradient. Two opposed flows, exactly as [`05`](05-dynamics.md) §4 described, now with explicit terms.

## 3. The fixed point and the stability criterion

**Residual misalignment.** Setting `\dot{\bar k} = 0`:

$$\boxed{\,\bar k^\* \;=\; k^\* \;+\; \gamma^{-1}\,V g,\qquad \big\lVert \bar k^\* - k^\* \big\rVert \;=\; \gamma^{-1}\,\lVert V g\rVert.\,}$$

The fleet does **not** in general settle at the target. It settles a distance `‖Vg‖/γ` away — *goal-dispersion
times reward-pull, divided by control gain*. Perfect alignment (`\bar k^\* = k^\*`) holds **iff** `Vg = 0`,
i.e. iff either the environment rewards exactly the target (`g = 0`), or there is no goal diversity to select
among (`V = 0`), or control is infinite (`γ → ∞`).

**Stability.** Allowing the reward landscape to depend on the fleet's position, the aligned fixed point is
**locally stable iff**

$$\boxed{\,\gamma \;>\; \lambda_{\max}\!\Big(\tfrac{\partial (V g)}{\partial \bar k}\Big),\,}$$

the control gain must exceed the largest eigenvalue of the *sensitivity of the selection drift to the fleet's
own position*. If drifting off-target makes the off-target pull *stronger* (`∂(Vg)/∂\bar k > 0`, a positive
feedback), then below a critical `γ` the aligned state is unstable and the fleet **runs away** — misalignment
amplification. Above it, control dominates and alignment is maintained, up to the residual of §3.

This is the conjecture of [`05`](05-dynamics.md) §4 made precise. There the threshold was "control gain >
growth-rate variance across goals"; note the growth-rate variance is `g^\top V g` (the variance of
`G_a \approx g^\top(k_a-\bar k)`), the scalar contraction of the same `V` and `g` that appear here — so the
vector criterion above *refines* the scalar conjecture and adds the residual-misalignment formula it lacked.

## 4. Governance consequences — incentive design beats brute-force control

The residual `‖Vg‖/γ` exposes three levers, of sharply different cost:

1. **Raise `γ`** (correct more often / more strongly). Direct, but costly and unbounded — you are perpetually
   fighting a drift you never remove. Halving misalignment means doubling control effort forever.
2. **Shrink `V`** (reduce goal diversity). Cheap, but it destroys the very diversity that lifts the fleet's
   value ceiling ([`04`](04-multi-agent-capacity-region.md) §2) and its adaptability. A bad trade in general.
3. **Drive `g → 0`** (design the environment so resource capture does *not* reward off-target goals). This
   removes the drift *at its source*: if `g = 0`, the residual is zero **for any `γ` and any `V`** — alignment
   is maintained with negligible control while diversity (hence adaptability and ceiling) is preserved for free.

> **The cheap half of alignment is incentive design, not control.** Reducing `g` — aligning what *pays* with
> what is *wanted* — is strictly more efficient than raising `γ`, because it eliminates the selection drift
> rather than perpetually opposing it. Brute-force oversight (high `γ`) is the expensive fallback for the
> residual `g` you cannot design away.

This is the actionable form of the is/ought asymmetry ([`05`](05-dynamics.md) §0): because goals have no
world-given target, they are governed by *what pays* (selection, via `g`) and *what is imposed* (control, via
`γ`). Alignment engineering is the joint design of both — and the theorem says to spend first on `g`.

## 5. Honest limits

- **Mean-field.** §2 uses Price's equation on population means and ignores finite-population fluctuations; a
  small fleet can drift stochastically even when the mean-field fixed point is stable.
- **Linearized landscape.** `G_a ≈ \bar G + g^\top(k_a-\bar k)` is first-order; strongly curved reward
  landscapes (multiple basins, thresholds) need a global treatment and can have several stable misaligned
  fixed points.
- **Quasi-static `V`.** Selection also *reshapes* `V` (it concentrates weight on winners, shrinking dispersion)
  while control and any exploration term replenish it. A full result needs a joint Lyapunov analysis of the
  coupled `(\bar k, V)` system; we have treated `V` as slowly varying.
- **`g` taken as given.** We treat the environment's reward gradient as exogenous; in a closed multi-agent
  world the agents *are* each other's environment, so `g` is endogenous — the genuinely coupled, and harder,
  case.

## 6. What this adds to the thesis

The result aimed squarely at alignment — with its status stated honestly (per the priority audit, the control
mathematics here is *classical*: the threshold is high-gain stabilization, the residual is the textbook
velocity error; the contribution is the **mapping** of goal-drift-under-selection onto that machinery, not a
new control theorem). It turns "keep agents aligned" from a slogan into a control law with a measurable
threshold (`γ > λ_max(∂(Vg)/∂\bar k)`), a closed-form residual (`‖Vg‖/γ`), and a clear prescription (design
`g → 0` before spending on `γ`). **Technical note (2026-06-07, after external review):** for a *non-normal*
Jacobian the precise asymptotic criterion is the **spectral abscissa** (largest *real part* of the eigenvalues
of the linearized flow), and non-normality permits *transient* misalignment growth even when the fixed point is
asymptotically stable — read the eigenvalue threshold as the spectral-abscissa condition in general. Together
with the real-agent test this is the natural core of the paper: *statics* (the measure, capacity, pooled-fleet
ceiling) + *one sharp dynamical mapping* (alignment stability) + *evidence* (sim + real agents).

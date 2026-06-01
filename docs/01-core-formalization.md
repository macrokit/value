# Core Formalization — The Logarithmic Value Law

> Thread A from [`00-thesis-seed.md`](00-thesis-seed.md) §9.1: state the axioms tightly and derive what
> functional form they force. This is the "Shannon Section 1" of value — one clean definition and one
> provable result.

## Motivating premise (why this matters now)

**In the near future, all AI agents are driven by values.** If that is true, a theory of value is not
philosophy — it is the *control theory for agent populations*. To route, align, and govern many separated AI
individuals we need value to be a measured quantity with laws, not a verdict. Everything below is built to
that end.

## 1. The object being measured

Shannon measures a **probability distribution** `p = (p₁,…,pₙ)` over possible messages. We measure the
structurally-parallel object on the value side:

> An agent `A` holds a finite, scarce **resource budget** `E` (free energy, or its proxy: compute, time).
> It commits that budget across `n` **goal-channels** as an allocation `e = (e₁,…,eₙ)`, `eᵢ ≥ 0`, `Σeᵢ = E`.

Same simplex geometry as Shannon's `p`; different semantics. `eᵢ` is *resource committed to channel i*, not
probability of message i.

Each channel carries a **goal-weight** `kᵢ ≥ 0`: how much advancing channel `i` serves agent `A`'s goal, per
unit of effective progress. The vector `k = (k₁,…,kₙ)` **is the agent-frame** — change the agent, change `k`.
The budget `E` is frame-independent (the cross-frame invariant of [`00`](00-thesis-seed.md) §3); `k` is what
varies between agents.

## 2. Axioms for a per-channel value function `vᵢ(eᵢ)`

We want `V(e) = Σᵢ vᵢ(eᵢ)` (separability across independent goal-channels — Axiom S below). For each `vᵢ`:

- **(A1) Continuity.** `vᵢ` is continuous on `e > 0`.
- **(A2) Monotonicity.** `vᵢ` is non-decreasing: committing more resource toward a goal-relevant channel
  never reduces value.
- **(S) Separability.** Value over independent goal-channels adds: `V(e) = Σᵢ vᵢ(eᵢ)`.
- **(A3) Scale-invariant proportional increment.** *The value added by a proportional increase in resource
  is the same regardless of the current level:*
  $$v_i(\lambda e) - v_i(e) = \varphi_i(\lambda)\quad\text{for all } e>0,\ \lambda>0,$$
  with `φᵢ` independent of `e`.

A3 is the load-bearing axiom and it is not arbitrary: it is the precise statement of **diminishing marginal
value** — the most robust empirical regularity about value (Bernoulli 1738 on wealth; Weber–Fechner on
stimulus response; Gossen's first law). It is also exactly the place where value departs from energy: energy
is linear in amount, value is scale-relative.

## 3. The theorem

**Claim.** Any `vᵢ` satisfying (A1)–(A3) has the form `vᵢ(eᵢ) = kᵢ ln eᵢ + cᵢ` with `kᵢ ≥ 0`.

**Proof.** Put `g(x) := vᵢ(eˣ)`. A3 with `e = eˣ`, `λ = eʸ` gives
`g(x+y) − g(x) = φᵢ(eʸ) =: ψ(y)`, independent of `x`. Setting `x = 0`: `ψ(y) = g(y) − g(0)`. Substitute:
$$g(x+y) = g(x) + g(y) - g(0).$$
Let `h(x) := g(x) − g(0)`; then `h(x+y) = h(x) + h(y)` — Cauchy's equation. With continuity (A1), `h(x) = kᵢx`.
Hence `g(x) = kᵢx + g(0)`, i.e. `vᵢ(eᵢ) = kᵢ ln eᵢ + cᵢ`. Monotonicity (A2) forces `kᵢ ≥ 0`. ∎

**The Logarithmic Value Law.**
$$\boxed{\,V(e) = \sum_i k_i \ln e_i + \text{const}\,}$$

### Why this is value, not entropy in disguise

It shares Shannon's logarithm but is a genuinely different quantity:

| | Shannon entropy `H(p) = −Σ pᵢ ln pᵢ` | Logarithmic value `V(e) = Σ kᵢ ln eᵢ` |
|---|---|---|
| variable | probability `pᵢ` (what we don't know) | resource committed `eᵢ` (what we spend) |
| log arises from | additivity over independent events | diminishing marginal value (A3) |
| directionality | none — symmetric in outcomes | carried by `kᵢ` (a goal, a sign, a target) |
| sign of the `Σ … ln …` term | `−` | `+` |

The log is the same skeleton reached by two different routes — which is *why* entropy reappears below as a
natural by-product rather than a coincidence.

## 4. Optimal allocation and the focus penalty

Maximize `V(e) = Σ kᵢ ln eᵢ` subject to the budget `Σ eᵢ = E`. Lagrange: `kᵢ/eᵢ = μ`, so

$$e_i^* = E\,\frac{k_i}{K},\qquad K := \sum_j k_j.$$

**Optimal resource allocation is proportional to goal-weight** — *value-proportional betting.* This is exactly
**Kelly's criterion** (J. L. Kelly, 1956), and the lineage is not a coincidence: Kelly was Shannon's Bell Labs
colleague and derived proportional betting *directly from Shannon's channel capacity* ("A New Interpretation
of Information Rate"). The historical bridge from information to value already exists; the Logarithmic Value
Law generalizes it from gambling returns to arbitrary goal-pursuit.

Substituting `e*` back:

$$V^* = \sum_i k_i \ln\!\Big(\frac{E k_i}{K}\Big) = K\ln E + \sum_i k_i \ln\frac{k_i}{K}
   = \boxed{\,K\ln E \;-\; K\,H(\hat k)\,}$$

where `k̂ = k/K` is the normalized goal-weight vector and `H(k̂) = −Σ k̂ᵢ ln k̂ᵢ` is its **Shannon entropy**.

Read the result:

- **`K ln E`** — realizable value grows with the log of resource, scaled by total goal-stakes `K`.
- **`− K·H(k̂)`** — the **focus penalty**: the more an agent's goals are *spread out* (high entropy), the less
  value it extracts from the same resource. A focused agent (low goal-entropy) realizes strictly more value.

Shannon entropy thus emerges **as a dissipation term** — not as the value itself. This is the Second Law of
Value ([`00`](00-thesis-seed.md) §4) in microcosm: dispersion wastes value.

## 5. Consequences for governing AI individuals

1. **Give each agent a focused goal.** The focus penalty `−K·H(k̂)` is paid per-agent. Diffuse mandates are
   not just bad management — they are *quantified* value dissipation.
2. **Allocate resource proportional to goal-weight** (`eᵢ* ∝ kᵢ`), not equally and not winner-take-all. Both
   uniform and all-in allocations are provably sub-optimal under the log law.
3. **Value is comparable within a frame, cardinal up to the constant `cᵢ`.** Across frames (different `k`),
   only the shared invariant `E` is directly comparable — cross-agent value accounting is the open problem
   ([`00`](00-thesis-seed.md) §8), and this formalization sharpens *why*: two agents' `V`s live in different
   `k`-bases.
4. **A fleet has an aggregate `V* = Σ_a K_a ln E_a − Σ_a K_a H(k̂_a)`.** Governance = maximize the first sum
   (route resource to high-stakes agents) while minimizing the second (keep each agent focused).

## 6. Boundary conditions — where the log law does not hold

Stated plainly, in Shannon's spirit of naming the model's assumptions:

- **Threshold / all-or-nothing goals.** When value is a step (you need *exactly* `X` to clear a bar — a
  surgery, a quorum, a launch), value is not concave and A3 fails near the threshold. The log law is the
  *smooth-goal* regime.
- **Satiation.** Real value often *caps* rather than growing unboundedly as `ln E → ∞`. A bounded variant
  (e.g. `kᵢ(1 − e^{−eᵢ/sᵢ})`) may be needed; A3 then holds only below satiation.
- **Risk-seeking / convex regions.** Gambles, status races, and winner-take-all dynamics produce locally
  convex value; the concavity that A3 encodes is violated.
- **Non-stationary goals.** `k` drifts as the agent learns or the world changes. The static derivation is a
  snapshot; the dynamic theory (how `k` evolves) is unwritten.

## 7. What this bought us (against the tautology objection)

[`00`](00-thesis-seed.md) §8 warned the theory must do something revealed preference cannot. The log law does:

- it **predicts** allocation (`eᵢ* ∝ kᵢ`) from a single axiom,
- it **sets a limit** (`V* = K ln E − K·H(k̂)` bounds extractable value), and
- it makes **Shannon entropy reappear as a dissipation term** — a structural bridge revealed preference has no
  reason to produce.

## 8. Next threads

- **§9.2 (the coding theorem of value).** Push the Kelly connection to a *growth-rate* limit: under
  uncertainty, the max long-run growth rate of value is bounded by an information-rate term. This is the
  closest thing to a Shannon capacity theorem for value, and Kelly already did the gambling case — generalize it.
- **Cross-frame transformation.** Define the map between two agents' `k`-bases and find what (beyond `E`) is
  invariant. Without it, fleet-level value is only ordinal.
- **Dynamics of `k`.** How goal-weights are learned, drift, and are deliberately set (alignment as choosing `k`).

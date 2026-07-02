# AMENDMENT 2 to PREREGISTRATION.md — 2A protocol corrections (committed BEFORE any run)

**Status at the time of writing:** zero experiment-2A or 2B calls have been made (the
only spend to date is the gate, docs/19). Both corrections below fix internal
inconsistencies in the frozen §2/§4 discovered while implementing the harness; both
are committed blind to any outcome, preserving the prereg-precedes-results order.
Author byline: Cheng Qian.

## A2.1 — Coalition throughputs are defined by COALITION-LEVEL elicitation

§2 froze naive-Bayes product fusion of individual reports as *the* coalition rule
while §4's P2 band requires the XOR control (e) to be supermodular by ≥ ln2/2. These
are mathematically incompatible: in (e) each agent's true individual posterior is
uniform (I = 0), and a product of uniforms is uniform — product fusion yields
`Ĝ_{12} = 0` for *perfect* agents, making the frozen band unsatisfiable by design.
The pilot (docs/17) in fact defined coalition value by the **fused posterior
`p(x|Y_S)`**, which for elicited agents ports as:

> **Corrected primary rule:** for every coalition `S`, elicit the posterior from an
> agent instance shown **all of `S`'s signals together** (same 12-repeat protocol;
> one cell per realisable signal-tuple). `Ĝ_S` is computed from these
> coalition-level reports by exact enumeration.

Naive-Bayes product fusion of individual reports is **retained as a pre-registered
secondary diagnostic**: it should track the coalition-level `Ĝ_S` for structures
(a)–(d) (conditional independence holds) and **fail in (e)** — showing the
independence precondition is load-bearing at the fusion level. P2's frozen bands are
unchanged and now well-defined (they bind the coalition-level `Ĝ_S`).

## A2.2 — Live-market structures corrected to a heterogeneous ladder + clones

§2 froze the live market on structures (a) and (c); in both, all agents have equal
channel information (ln 2), making P4's "terminal wealth ordered by `Î_a`"
**degenerate** (no ordering exists to confirm). Corrected structures, porting the
pilot's E7 BSC ladder:

> **(L) ladder:** 3 agents, all observing bit `b₀` — agent 1 clean, agent 2 through
> a stated 10%-flip sensor, agent 3 through a stated 25%-flip sensor
> (`I = 0.693 > 0.368 > 0.131` — strictly ordered).
> **(C) clones:** unchanged from §2 (two clean-`b₀` clones + one `b₁` agent), for
> the clone-equality half of P4.

P4's frozen bands are unchanged: ordering by `Î_a` in ≥ 4/5 seeds **on (L)**; clone
terminal-wealth gap ≤ 10% of mean share **on (C)**.

## Cost note

A2.1 raises the elicitation call count (coalition cells for all `S`, ~1,500 calls
total vs ~1,100): revised 2A estimate ≈ $12–15. The §6 hard cap ($160) and spend
order are unchanged.

*Amendment commit SHA precedes the first 2A/2B results commit — see git log.*

# Roadmap — open directions (status as of 2026-06-04)

A single view of what's open, so the threads aren't scattered. Ordered by readiness. The published core
(Zenodo, concept DOI `10.5281/zenodo.20487041`) stands on its own; everything here is *forward* work.

## Near-term (in flight / logistics)
- [ ] **Publish v3** — the cross-shape generalization ([`14`](14-bridge-generalization.md)) + the two-route
  derivation hardening ([`01`](01-core-formalization.md)). *Blocker:* reconcile the cross-shape `n=42` line in
  the paper's §Cross-shape (make the point count reconstructable), final proof. Then owner-gated Zenodo
  "New version". Draft prepared in `paper/ZENODO.md`.
- [ ] **v3-completeness (optional):** close the code **capability-ranking** sub-check (currently 11/12 —
  underpowered, ρ=0.429). Needs a **≥32 GB host** to run 7B/8B coders without the 16 GB RAM thrash; would turn
  11/12 → 12/12. Not a blocker for v3; would let a later version drop the caveat.
- [ ] **Dissemination (the real "reach" lever):** the published record has ~0 views — that is a *distribution*
  problem, not a versioning one. Move: post the is/ought-as-control note (drafted, `drafts/`) to the relevant
  audience + an arXiv cross-listing + sharing. This is what converts the record into readers; another version
  does not.

## Research directions (gated behind the published core)
- [ ] **Cross-frame / price layer — real-data test** ([`cross-frame-applications`](cross-frame-applications.md)).
  The *one empirical arena that reaches the multi-agent half* of the theory (docs [`03`](03-cross-frame-value.md)/
  [`04`](04-multi-agent-capacity-region.md)) — which the LLM-agent tests could not, because here the quantities
  are *measured, not elicited from a weak model*. Pre-registered test: does observable value flow across
  substrates obey doc 03 — (i) flows down the value/price gradient, (ii) friction-gated transfer
  (`V_j − V_i > f`), (iii) price as the frame-independent coordinate? Honest confound: social processes
  dominate; physics-envy is the failure mode — pre-register and report either way. *This is the most valuable
  next empirical shot* (real agents, abundant data, the untested multi-agent layer).
- [ ] **Wave / field theory — gate not cleared** (docs [`08`](08-field-theory-of-value.md),
  [`11`](11-real-agent-field-test.md)). Derived + toy-emergent, but real small-LLM agents coordinate by
  *Schelling focal points*, not spontaneous flocking. Options (no model-escalation fishing): a motile,
  focal-point-free re-test under fresh pre-registration; OR write up the honest negative as a standalone note;
  OR retire the gate. Earnable standalone preprint *only* on a clean guardrail-respecting positive.
- [ ] **Incentive-design-beats-oversight — real-agent verdict** (docs [`12`](12-incentive-vs-oversight.md),
  [`13`](13-incentive-vs-oversight-real.md)). Confirmed in the toy (`residual = V·g/γ`, R²=0.999); real-agent
  test was **CAP / underpowered** (design saturated `g ≤ 0.2` below the noise floor). A properly-powered redo
  needs a *de-saturated design* (continuous/large-K goal space, larger δ, more seeds) — the fix is the design,
  not bigger models. Likely outcome leans negative (mean trend had g-exponent ≈ 0); pursue only for a
  definitive verdict, not a rescue.
- [ ] **Axiom-3 deeper defense (optional theory).** Now *demoted* (the log is over-determined by the
  compounding route, so scale-invariance is no longer load-bearing) — so lower priority. A first-principles
  argument for why value has no privileged scale would still harden the foundation.

## Standing discipline (applies to every item above)
Pre-register before fitting; keep pre-registered vs exploratory strictly separate; report negatives as results;
no instrument-fishing (no escalating model size / forcing hardware to manufacture a positive); the publish gate
is owner-only; keep the core paper substrate-agnostic and clean. The credibility of the whole program rests on
these — they are why the *good* result is worth more than a hollow *great*.

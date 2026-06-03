# Zenodo deposition metadata — v3 NEW VERSION (DRAFT — do not upload without sign-off)

Draft metadata for depositing the updated `main.pdf` as **a new version of the existing Zenodo record**.
**Nothing here is published.** Release is gated on explicit owner sign-off (handoff rule).

## ⚠️ This is a NEW VERSION, not a new record

- **Concept DOI (cite-always, resolves to latest):** `10.5281/zenodo.20487041`
- **New version DOI:** minted automatically by Zenodo when the new version is published — do **not** create a
  fresh deposition.
- **Workflow:** open the existing record's Zenodo page → **"New version"** → replace `main.pdf` → bump the
  version field → paste the updated description/notes below → **save as draft** → stop. Publishing is the
  owner's call.
- Older versions (v1/v2) remain permanently resolvable under their own version DOIs; the concept DOI moves to v3.

## Fields (Zenodo web form)

| Field | Value |
|---|---|
| **Upload type** | Publication → **Preprint** |
| **Title** | A Mathematical Theory of Value |
| **Authors / Creators** | Qian, Cheng |
| **Affiliation** | *(leave blank — owner default)* |
| **ORCID** | *(none — leave blank)* |
| **Publication date** | 2026-06-03 |
| **Version** | **v3** |
| **License** | **CC-BY-4.0** (unchanged — owner default). |
| **Keywords** | value; theory of value; information theory; Kelly criterion; mutual information; log-optimal growth; multi-agent systems; AI agents; agent coordination; AI alignment; mechanism design; free energy; reinforcement learning; ergodicity economics; task generalization |
| **Description** | (abstract below) |
| **Notes** | Source and reproducible experiments are maintained in a private repository; available on request. |

## Version notes (paste into the "new version" changelog / notes box)

> **v3 changes (empirical strengthening + derivation hardening; no change to the core claims).**
> (1) *Cross-shape generalization.* A new pre-registered test shows the out-of-sample value bridge
> ΔG ~ I(X;Y) is shape-invariant: it holds across four qualitatively different task shapes — classification,
> reasoning (GSM8K), sequential decision, and code (MBPP), all with discrete gold so I is computed exactly
> (not estimated) — with a pooled slope (0.953, n=42) statistically indistinguishable from the
> classification-only value (0.935). This promotes the bridge from a demonstration toward a law. The single
> underpowered sub-check (capability-ranking on the code shape, where ≤3B models cluster in code-accuracy and
> the stronger-model remedy was hardware-blocked) is reported honestly in Limits as a power limitation, not a
> shape-specific break — the code bridge slope itself passes.
> (2) *Logarithm derivation.* The logarithmic measure V = Σ kᵢ ln eᵢ is now presented as forced by two
> independent routes that share no premises — a static scale-invariance/Cauchy argument and a dynamic
> compounding/ergodicity argument — rather than resting on scale invariance alone.

## Description (plain text for the Zenodo abstract box)

> We propose that value — the quantity that goal-directed agents create, destroy, and exchange — is a lawful
> structural quantity, in the same category as information, once stripped of its semantic clothing (morality,
> price, psychology). Following the method of Shannon (1948), we make one ruthless abstraction: value is the
> rate at which an agent converts a physical resource into goal-progress, relative to a frame fixed by the
> agent's goal. A scale-invariance axiom forces a logarithmic measure of value, V = Σ kᵢ ln eᵢ, via a Cauchy
> functional equation; the compounding dynamics of a reinvested resource force the same form independently via
> an ergodicity argument — two routes with no shared premises. From the compounding dynamics we derive a coding
> theorem of value: the rate at which an agent can create value through a perception channel Y of the world X is
> bounded by the mutual information, ΔG ≤ I(X;Y), achieved by Bayes-proportional allocation; and realized value
> decomposes exactly as available potential minus dissipation, G = D(q‖r) − D(q‖p), identifying misalignment
> with measurable waste. For populations we show value is frame-relative while price is frame-independent, that
> the collective value throughput of a fleet is capped by the world's entropy, Σ Gₐ ≤ H(X), and that the
> fleet's operating point is a Kelly portfolio over agents selected by an emergent price. A dynamical layer
> gives the equations of motion and an is/ought asymmetry — beliefs have a target the world supplies, goals do
> not — from which alignment emerges as a control-stability condition with a closed-form residual misalignment.
> We test the single-frame laws on live language models in a pre-registered scale-up across three task domains
> and a ten-model, five-family ladder, and further show the out-of-sample bridge ΔG ~ I(X;Y) is shape-invariant:
> pooled across four qualitatively different task shapes — classification, reasoning (GSM8K), sequential
> decision, and code (MBPP), all with discrete gold so I is computed, not estimated — the slope (0.953) is
> statistically indistinguishable from the classification-only value, promoting the bridge from a demonstration
> toward a law. Over-confidence is measurable dissipation in every domain; the fleet-pricing claim is reported
> with its honest boundary. The laws hold in the smooth, concave regime. None of the underlying mechanisms is
> individually new; the contribution is their unification under one substrate-grounded quantity, and the
> is/ought asymmetry that follows.

## Machine-readable metadata (zenodo.json — for the API, if used)

```json
{
  "metadata": {
    "upload_type": "publication",
    "publication_type": "preprint",
    "title": "A Mathematical Theory of Value",
    "creators": [
      { "name": "Qian, Cheng" }
    ],
    "publication_date": "2026-06-03",
    "language": "eng",
    "version": "v3",
    "conceptdoi": "10.5281/zenodo.20487041",
    "license": "cc-by-4.0",
    "keywords": [
      "value", "theory of value", "information theory", "Kelly criterion",
      "mutual information", "log-optimal growth", "multi-agent systems",
      "AI agents", "agent coordination", "AI alignment", "mechanism design",
      "free energy", "reinforcement learning", "ergodicity economics",
      "task generalization"
    ],
    "description": "See the plain-text description in ZENODO.md (paste into the Zenodo abstract box)."
  }
}
```

## Pre-upload checklist

- [ ] **Publish gate:** explicit owner sign-off (required before any outward release).
- [ ] Use **"New version"** on concept DOI `10.5281/zenodo.20487041` — do NOT mint a new record.
- [x] Decisions resolved (owner defaults): affiliation blank, ORCID blank, license CC-BY-4.0, version v3.
- [x] `main.pdf` rebuilt with the cross-shape subsection (§ Cross-shape generalization) and updated abstract.
- [x] Leakage check clean (no private-project / proprietary-domain specifics).
- [ ] Final read of `main.pdf` end-to-end (last proofing pass before upload).
- [ ] Confirm the version notes + description above match the final PDF abstract.
- [ ] After publish: the version DOI is permanent and the record immutable except for new versions — proof first.

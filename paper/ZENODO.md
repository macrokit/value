# Zenodo deposition metadata (DRAFT — do not upload without sign-off)

Draft metadata for depositing `main.pdf` as a Zenodo preprint. **Nothing here is published.** Two fields need
your decision before upload — flagged with ⚠️.

## Fields (Zenodo web form)

| Field | Value |
|---|---|
| **Upload type** | Publication → **Preprint** |
| **Title** | A Mathematical Theory of Value |
| **Authors / Creators** | Qian, Cheng |
| ⚠️ **Affiliation** | *(blank, or "Independent researcher" — confirm)* |
| ⚠️ **ORCID** | *(none on file — add if you have one, else leave blank)* |
| **Publication date** | 2026 |
| **Language** | English (eng) |
| **Version** | v1 |
| ⚠️ **License** | **CC-BY-4.0** (proposed — standard for a preprint; lets others cite/build with attribution. Note: this is the *paper's* license; differs from Macrokit code's Apache-2.0. Confirm.) |
| **Keywords** | value; theory of value; information theory; Kelly criterion; mutual information; log-optimal growth; multi-agent systems; AI agents; agent coordination; AI alignment; mechanism design; free energy; reinforcement learning; ergodicity economics |
| **Description** | (abstract below) |
| **Notes** | Source and reproducible experiments are maintained in a private repository; available on request. |

## Description (plain text for the Zenodo abstract box)

> We propose that value — the quantity that goal-directed agents create, destroy, and exchange — is a lawful
> structural quantity, in the same category as information, once stripped of its semantic clothing (morality,
> price, psychology). Following the method of Shannon (1948), we make one ruthless abstraction: value is the
> rate at which an agent converts a scarce resource into goal-progress, relative to a frame fixed by the
> agent's goal. From a single scale-invariance axiom we derive a logarithmic measure of value, V = Σ kᵢ ln eᵢ.
> From the compounding dynamics of a reinvested resource we derive a coding theorem of value: the rate at which
> an agent can create value through a perception channel Y of the world X is bounded by the mutual information,
> ΔG ≤ I(X;Y), achieved by Bayes-proportional allocation; and realized value decomposes exactly as available
> potential minus dissipation, G = D(q‖r) − D(q‖p), identifying misalignment with measurable waste. For
> populations we show value is frame-relative while price is frame-independent, that the collective value
> throughput of a fleet is capped by the world's entropy, Σ Gₐ ≤ H(X), and that the fleet's operating point is
> a Kelly portfolio over agents selected by an emergent price. A dynamical layer gives the equations of motion
> and an is/ought asymmetry — beliefs have a target the world supplies, goals do not — from which alignment
> emerges as a control-stability condition with a closed-form residual misalignment. We test the single-frame
> laws on live language models across four local models on a frozen decision task: perception mutual
> information tracks realized capability rather than parameter count, out-of-sample value-growth tracks I(X;Y),
> over-confidence is measurable dissipation, and diversity beats redundancy; the fleet-pricing claim is
> reported with its honest boundary. The laws hold in the smooth, concave regime. None of the underlying
> mechanisms is individually new; the contribution is their unification under one substrate-grounded quantity,
> and the is/ought asymmetry that follows.

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
    "publication_date": "2026-06-01",
    "language": "eng",
    "version": "v1",
    "license": "cc-by-4.0",
    "keywords": [
      "value", "theory of value", "information theory", "Kelly criterion",
      "mutual information", "log-optimal growth", "multi-agent systems",
      "AI agents", "agent coordination", "AI alignment", "mechanism design",
      "free energy", "reinforcement learning", "ergodicity economics"
    ],
    "description": "See ZENODO.md for the full abstract (paste the plain-text description there)."
  }
}
```

## Pre-upload checklist

- [ ] **Publish gate:** explicit owner sign-off (the handoff requires confirming before any outward release).
- [ ] Decide ⚠️ affiliation, ⚠️ ORCID, ⚠️ license (CC-BY-4.0 proposed).
- [ ] Final read of `main.pdf` end-to-end (the red-team fixes are in; this is a last proofing pass).
- [ ] Confirm the paper names no Macrokit/AutoStore specifics (Sacred Rule #1) — leakage check already clean.
- [ ] Reserve a DOI in Zenodo (draft deposition) before publishing, if you want the DOI in any announcement.
- [ ] After publish: the DOI is permanent and the record is immutable except for new versions — so proof first.

# Building the Stage 2 standalone paper

One source, two builds, controlled by a single toggle in `main.tex`:

```latex
\newif\ifanon
\anontrue        %  <- this line is the toggle
```

| Build | Command | Output | Byline | Header | Code pointer | Acks |
|---|---|---|---|---|---|---|
| **Anonymous** (TMLR review, default) | `./build.sh` | `main.pdf` | "Anonymous authors" | "Under review as submission to TMLR" | anonymized supplement ZIP (no external host) | suppressed |
| **De-anonymized** (preprint / arXiv) | `./build.sh preprint` | `main-preprint.pdf` | Cheng Qian, Independent Researcher | none | `github.com/macrokit/value` | shown |

`main.pdf` is the **anonymous submission artifact** — it is what you upload to
OpenReview. Running `tectonic main.tex` (or `./build.sh`) always reproduces it.
The de-anonymized preprint is one line away: `./build.sh preprint` flips the
toggle into a generated `main-preprint.tex` and builds `main-preprint.pdf`, so
the two versions can never drift.

## Anonymized supplementary material (for OpenReview)

TMLR allows an anonymized supplement up to 100 MB. Build it with:

```
./make-supplement.sh      # -> stage2-supplement-anon.zip (~5.5 MB)
```

It packages a tracked-only snapshot of `sim/stage2` (pre-registrations, runners,
analyzer, raw results, per-call cache) with the `Author byline: Cheng Qian.`
headers stripped to `Anonymous`, plus a reviewer README, and **hard-fails if any
identifying string or email-shaped token survives** (text files and the binary
cache are both scanned).

**This ZIP is the SOLE blind code-delivery vehicle.** The anonymous.4open.science
mirror was abandoned: its current UI has no file-content redaction field (it only
masks the repo URL/owner), so the many "Cheng Qian" bylines throughout the repo
would remain in plain text and deanonymize the submission (owner-confirmed on the
live form, 2026-07-03). The anonymous build therefore names no external host and
points reviewers only at this attached supplement. The per-call cache
(`gate_cache.sqlite`, 19.9 MB uncompressed) is included **inside** the ZIP, so the
"every response auditable" claim resolves to a file a blind reviewer can open.
Final size ~5.5 MB (well under the 100 MB cap).

## Requirements
- [`tectonic`](https://tectonic-typesetting.github.io/) (`brew install tectonic`).
  Self-contained: fetches its own packages, no MacTeX needed. First run needs
  network; later runs are offline.

## Before submitting (anonymization checklist — all automated by the toggle)
- [x] Byline suppressed; `\author{}` block ignored by the anonymous style.
- [x] PDF `/Author` and `/Keywords` metadata forced empty (`\hypersetup`).
- [x] Repository URL removed from the anon build; §7 points at the anonymized
      supplement ZIP, no external host named. Preprint build keeps the GitHub URL.
- [x] Acknowledgments (self-funding) suppressed.
- [x] First-person "companion / our synthesis" framing neutralized to third person.
- [x] Self-citation kept: the synthesis `(Qian, 2026)` is cited in third person and
      listed by name in the references — standard, permitted double-blind practice
      (owner decision, 2026-07-03).

## Generated / ignored files
`main-preprint.tex`, `main-preprint.pdf`, and tectonic intermediates
(`*.aux`, `*.bbl`, `*.log`, `*.out`, `*.blg`) are build products — git-ignored,
never edit `main-preprint.tex` by hand (it is overwritten on every preprint build).

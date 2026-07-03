# Building the Stage 2 standalone paper

One source, two builds, controlled by a single toggle in `main.tex`:

```latex
\newif\ifanon
\anontrue        %  <- this line is the toggle
```

| Build | Command | Output | Byline | Header | Repo link | Acks |
|---|---|---|---|---|---|---|
| **Anonymous** (TMLR review, default) | `./build.sh` | `main.pdf` | "Anonymous authors" | "Under review as submission to TMLR" | `anonymous.4open.science` | suppressed |
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
identifying string survives** (text files and the binary cache are both scanned).
Reviewers get code delivery **both** ways (owner decision): this ZIP as a
self-contained backup, and the `anonymous.4open.science` mirror for browsing.

## Requirements
- [`tectonic`](https://tectonic-typesetting.github.io/) (`brew install tectonic`).
  Self-contained: fetches its own packages, no MacTeX needed. First run needs
  network; later runs are offline.

## Before submitting (anonymization checklist — all automated by the toggle)
- [x] Byline suppressed; `\author{}` block ignored by the anonymous style.
- [x] PDF `/Author` and `/Keywords` metadata forced empty (`\hypersetup`).
- [x] Identifying repository URL replaced by the anonymized mirror macro `\repolink`.
- [x] Acknowledgments (self-funding) suppressed.
- [x] First-person "companion / our synthesis" framing neutralized to third person.
- [ ] **Set the real anonymized-mirror URL**: replace the `value-XXXX` placeholder
      in `\repolink` (anon branch) with the actual `anonymous.4open.science` link
      once the mirror is created. (Owner decision — see the session report.)
- [ ] Residual self-citation: the synthesis `(Qian, 2026)` is cited in third
      person and listed by name in the references. This is standard, permitted
      double-blind practice; it is the one item that is an owner judgment call
      (keep as-is vs. redact the reference). See the session report.

## Generated / ignored files
`main-preprint.tex`, `main-preprint.pdf`, and tectonic intermediates
(`*.aux`, `*.bbl`, `*.log`, `*.out`, `*.blg`) are build products — git-ignored,
never edit `main-preprint.tex` by hand (it is overwritten on every preprint build).

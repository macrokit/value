# paper — *A Mathematical Theory of Value*

Shannon-style preprint, single author **Cheng Qian**. Source: `main.tex` (+ `refs.bib`).

## Build

```sh
tectonic main.tex      # single self-contained binary; runs bibtex + multiple passes
# or: pdflatex main && bibtex main && pdflatex main && pdflatex main
```

Output: `main.pdf`.

## Contents

Lifts the derivations and results from [`../docs/`](../docs/) and the experiments from
[`../sim/`](../sim/): the log-law (doc 01) and capacity-theorem (doc 02) proofs are in the appendices; the
multi-agent/price layer is docs 03–04; dynamics + alignment-stability are docs 05/07; Part IV is the sim
(E1–E5) plus the real-agent test (R1–R5, doc 06). Related work is `../docs/related-work.md`.

The experimental task is described **abstractly** (a frozen 100-item tool-routing benchmark); no
application-specific or product details appear in the paper.

## Status

Draft. **Not published.** The real-agent ladder is 1.5B/3B/7B; an 8B rung extends Table 1 when its run lands.
Confirm with the author before any outward publication (Zenodo or otherwise).

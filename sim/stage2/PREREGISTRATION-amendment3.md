# AMENDMENT 3 to PREREGISTRATION.md — protocol-fault re-runs (committed BEFORE the re-run)

**Status at the time of writing:** the first 2A pass is complete; **no 2B call has been
made.** The §5 protocol gates fired on parts of 2A, and a cache audit traced each
firing to an instrument fault (details below, all reproducible from the cached raw
outputs). This amendment (i) fixes an analyzer bug so the §5 gates are *enforced* as
frozen, (ii) states the protocol corrections, and (iii) scopes the re-run to the
protocol-CAP'd components ONLY — data that passed cleanly under the original protocol
is kept as verdict data and is not re-collected. Author byline: Cheng Qian.

## A3.1 — Analyzer conformance (bug fix toward the frozen text)

`analyze_stage2.py` recorded elicitation-gate failures (`n_good < 6/12`) but did not
exclude the affected structures from the P1/P2/P3 verdicts, contrary to §5
("protocol-CAP'd — reported, not fitted"). Fixed: any structure containing a
gate-failed cell is excluded from the frozen-band verdicts for the pass in which it
failed, and listed as protocol-CAP'd. (This is what turned (b)/(d) parse fallbacks
into a spurious −ln2 "submodularity violation" in the first-pass printout; with the
gate enforced, that check simply doesn't fit those structures.)

## A3.2 — Protocol corrections (traced faults, fixed for the re-run)

1. **Market output protocol** (first pass: **36%** of bet outputs parseable — the
   agents reason at provider-default temperature past the 600-token ceiling before
   emitting JSON; 64% uniform fallbacks mechanically produced the observed wealth
   dynamics): instruction changed to demand the JSON object FIRST on its own line
   (any explanation after it is ignored by the parser), ceiling raised to 900, and
   **one pre-stated parse-retry per call** (a distinct cached rep asking for
   format-only compliance). Per-agent parse rates are recorded in the output this
   time; a market run with overall parse < 0.90 remains protocol-CAP (the §5 spirit,
   now stated explicitly for the market).
2. **Structure-(e) coalition prompt self-contradiction** (my drafting fault): agent
   2's singleton observation text says "C … you do NOT see", which is false when
   composed into a coalition prompt that also shows C. Coalition prompts now compose
   observations neutrally ("Observation 1: C = v₁. Observation 2: X XOR C = v₂.");
   singleton prompts unchanged. The first-pass (e) posteriors (hedged toward the
   right XOR answer but ~uniform in one cell) are disclosed as contaminated by the
   contradiction, not evidence either way.
3. **Elicitation instruction** for the re-run cells: same JSON-first form as (1),
   ceiling 900. ((b)'s singleton cells and one (d) cell fell under 6/12 survivors on
   the original form.)

## A3.3 — Scope of the re-run (anti-fishing symmetry)

- **Re-collected under the corrected protocol:** all elicitation cells of structures
  **(b), (d), (e)**, and the **entire live market** (both structures, all seeds).
- **Kept as verdict data (NOT re-collected):** structures **(a), (c)** elicitation —
  they passed the gates cleanly under the original protocol. Passed components are
  not re-rolled, in either direction.
- P1/P2/P3 verdicts are then computed per the frozen bands over the full structure
  set (original (a),(c) + re-run (b),(d),(e)); P4 from the re-run market.
- Estimated re-run cost ≈ $16 (≈1,900 calls); the §6 hard cap ($160 on the meter) is
  unchanged and now binding-tight — if the cap stops 2B mid-way, the frozen spend
  order (§6) preserves the grid over the arms, and the budget stop is reported as
  such per §5.

*Amendment commit SHA precedes the re-run and all 2B results — see git log.*

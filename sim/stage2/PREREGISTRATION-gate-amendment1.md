# AMENDMENT 1 to PREREGISTRATION-gate.md — temperature (committed BEFORE any gate run)

**Status at the time of writing:** no gate run (debug or frontier) has been executed;
the only API calls made so far are model-ID health probes (~40 tokens total). This
amendment is forced by an instrument constraint discovered in those probes, and is
committed before any data collection, preserving the prereg-precedes-results order.

**The constraint.** The frozen models (Claude Opus 4.8 frontier; Sonnet 5 debug)
**reject an explicit `temperature` parameter** — the API returns
`invalid_request_error: "temperature is deprecated for this model"` for any value
other than omission (provider default = 1.0). The frozen §1 clause "Temperature 0.6"
is therefore unsatisfiable on the frozen instrument.

**The amendment (minimal, stated):** the `temperature` field is **omitted** (provider
default). The design's intent is unchanged — the noise source remains the model's own
sampling, exactly as in Stages 0–1 ("noise = the LLM's own sampling temperature", the
standing guardrail). No threshold, lever, scale, or decision-rule clause of the
pre-registration references the temperature value; G-1/G-2/G-3 pass/fail criteria are
untouched.

**Why this is not fishing:** the change is forced by the provider, made blind to any
gate outcome (no run has occurred), moves the noise knob in the *harder-to-pass*
direction if anything (default 1.0 = more sampling noise than 0.6), and is committed
ahead of results with this rationale.

Model IDs confirmed by health probe and recorded: `claude-opus-4-8` (frontier verdict),
`claude-sonnet-5` (debug only).

*Author byline: Cheng Qian. This amendment's commit SHA precedes the first gate-run
results commit — see git log.*

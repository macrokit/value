# Agent Value-Meter

Measure **any agent's value profile** on a task — grounded in a published
information-theoretic theory of value ([preprint](https://zenodo.org/records/20530824)).

Give it an agent's recorded outputs versus ground truth (and, optionally, per-item
cost), and it returns — all in **nats** — how much value the agent *can* generate on
this task, how much it *actually* generates out-of-sample, how much it *dissipates*
to miscalibration, and how much value it buys *per unit of compute*. Every number
ships with a null or a confidence interval, and the honesty caveats are printed in
the output, not buried.

It is **model-agnostic**: the core takes plain records, so it runs on *any* agent's
recorded outputs — no model, inference engine, or framework dependency. The
information-theoretic primitives (`entropy`, `kl`, `mutual_information`) are reused
from the project's `sim/value_sim.py`, not reinvented.

> **Author byline: Cheng Qian.**

---

## What it measures

| # | Quantity | Meaning | Honesty flag |
|---|----------|---------|--------------|
| 1 | **I(X;Y)** | the **value ceiling** — mutual information between gold `X` and the agent's choice `Y`, from the confusion matrix | reported vs a **permutation null** (above-chance, not raw); also `H(X)` and **saturation** `I/H(X)` |
| 2 | **ΔG** | the realized **value-generation rate** | two numbers: **in-sample = I** is an *arithmetic identity* (definitional, no empirical weight); the **out-of-sample** number (calibrate on a fit split, score on a holdout) is the empirical one, with a **bootstrap CI** |
| 3 | **D(q‖p)** | **dissipation** — value lost to miscalibration (the Second-Law term) | uses the agent's **stated** belief if `prob` is supplied, else a **constructed** over-confident belief (clearly labelled — *not* a probability the model reported) |
| 4 | **value / compute** | `I / tokens` (**primary**, load-free) and `I / median-latency` (**secondary**) | median latency is load-robust; tokens are the primary cost because they are unaffected by host load |

### The caveats are the instrument

The meter **measures**; it does not declare an agent "good" or "bad", and it makes no
benchmark-beating claim. Every run prints:

- **Task-relative.** `I`, `ΔG`, and dissipation are measured against *this* task's
  gold. It is a per-`(agent, task)` profile, **not** a universal agent score.
- **In-sample `ΔG = I` is definitional** (an arithmetic identity used only to confirm
  units). The empirical content is the **out-of-sample** `ΔG` and its CI.
- **Dissipation is of a stated *or constructed* belief** — and the output says which.
  The constructed belief is not necessarily one the model reported.
- **Intervals, not point estimates.** Read the permutation null and the bootstrap CI.
- **Single-agent scope only.** This measures the *validated* single-agent layer. It
  does **not** do multi-agent coordination or governance (that layer is unvalidated
  and out of scope).

---

## Install / requirements

Pure Python + NumPy. No network, no model calls. Run it from this directory so the
generic input form resolves the adapter:

```sh
cd tools/value-meter
python3 -m value_meter <input.json>            # human-readable profile
python3 -m value_meter <input.json> --json     # machine-readable JSON
```

---

## Input format (run it on *your* agent)

The portable format is a **list of records**. Each record needs `gold` and `pred`;
everything else is optional:

```json
{
  "classes": ["a", "b", "c"],
  "records": [
    {"gold": "a", "pred": "a", "prob": {"a": 0.7, "b": 0.15, "c": 0.15},
     "cost_tokens": 62, "cost_latency": 0.41},
    {"gold": "b", "pred": "c", "cost_tokens": 58, "cost_latency": 0.39}
  ]
}
```

| field | required | meaning |
|-------|----------|---------|
| `gold` | ✓ | the correct action/label (any string/number) |
| `pred` | ✓ | the agent's chosen action/label. If your agent silently *fails* (truncation, refusal, format collapse), emit a distinct token like `"?"` rather than a wrong label — the meter reports `degraded_rate` and warns when it is high, so plumbing failures aren't scored as low capability |
| `prob` | optional | the agent's **stated belief** over the classes (a `{class: p}` dict or a list aligned to `classes`). If present, dissipation uses the agent's own probabilities |
| `cost_tokens` | optional | total tokens for the item (enables `I / tokens`) |
| `cost_latency` | optional | wall-clock seconds for the item (enables `I / median-latency`) |

`classes` is optional (inferred from the golds if omitted). A bare JSON list of
records also works.

**To run it on your own agent:** log, for each task item, the correct answer and your
agent's answer (plus tokens/latency if you have them), dump them in the format above,
and run `python3 -m value_meter your_run.json`. That's it — there is no model
dependency. The profile tells you the task's information ceiling, how much of it your
agent realizes out-of-sample, what it wastes to over-confidence, and its value-per-token.

You can also call the core directly:

```python
from value_meter import value_profile, Record, format_profile
recs = [Record(gold="a", pred="a", cost_tokens=60), Record(gold="b", pred="c", cost_tokens=58)]
prof = value_profile(recs)          # ValueProfile dataclass; prof.to_dict() for JSON
print(format_profile(prof))
```

It also reads this project's cached harness runs directly
(`sim/real/v2/results/raw/<model>__<domain>.json`,
`sim/real/shapes/results/raw/<model>__<shape>.json`) — that's the self-test below.

---

## Worked examples (on the cached runs)

### 1. A weak model already near the ceiling — `qwen0.5b` on intent classification

```
python3 -m value_meter ../../sim/real/v2/results/raw/qwen0.5b__intent.json
```
```
  1) VALUE CEILING  I(X;Y)
       I = 1.4166 nats  (2.0437 bits)   [ABOVE chance]
       permutation null: mean 0.0549, p95 0.0837 nats   (perm p = 0.002)
       saturation I/H(X) = 0.791
  2) ΔG   in-sample = 1.4166  [= I, definitional]   out-of-sample = 1.3077  CI [1.169, 1.432]
  4) I / tokens = 9.3601 nats / 1k tokens   (mean 151 tok/item)
```
A 0.5B model reaches **79% of the task's world-entropy** on a confusable intent
router — and does it at ~150 tokens/item. The out-of-sample `ΔG` (1.31 nats) is the
honest, empirical number; the in-sample `ΔG = I` is flagged as a definitional identity.
*(This reproduces the paper's published `I` and `ΔG_hold` for this point exactly.)*

### 2. A capable model on a hard sequential task — `llama3b` on seqstate

```
python3 -m value_meter ../../sim/real/shapes/results/raw/llama3b__seqstate.json
```
```
  1) I = 1.5629 nats (2.2548 bits)   saturation I/H(X) = 0.872
  2) ΔG out-of-sample = 1.3427 nats   CI [1.165, 1.492]
  3) DISSIPATION = 1.4107 nats   (constructed over-confident belief)
  4) I / tokens = 4.7363 nats/1k tok   ·   I / latency = 0.1828 nats/s (median 8.5s)
```
The widest-information shape in the suite: `llama3b` extracts **1.56 nats** of a
1.79-nat ceiling on a register-machine rollout. Note the **dissipation of 1.41 nats** —
an over-confident bettor on these same predictions would throw away most of the
realized value; calibration is doing real work. The compute cost is high (~330
tok/item, 8.5s median latency), so its **value-per-token is ~3× lower** than the tiny
intent model above — exactly the kind of trade-off the meter surfaces.

### 3. Your own agent with a stated belief — `examples/toy_agent_with_belief.json`

```
python3 -m value_meter examples/toy_agent_with_belief.json
```
```
  1) I = 0.3796 nats   saturation I/H(X) = 0.346
  2) ΔG out-of-sample = 0.4536 nats   CI [0.335, 0.564]
  3) DISSIPATION = 0.0092 nats   (stated (agent prob) — the agent's OWN reported probability)
```
Because this synthetic agent supplies a `prob` vector, dissipation is measured against
its **own stated belief** (`D(p*‖q)` vs the calibrated optimum) and is labelled as such
— a near-calibrated agent wastes almost nothing. Saturation 0.35 says there is plenty
of headroom on this task: more capability *could* add value (the agent is far from the
ceiling), unlike example 1 where saturation 0.79 means it is already close.

---

## Self-test (the acceptance criterion)

```sh
python3 test_reproduces_paper.py
```

Runs the meter on the project's cached v2 (classification) and Lever-2 (task-shape)
runs and **asserts it reproduces the published numbers** — every per-`(model, domain)`
`I` and out-of-sample `ΔG_holdout`, and the pooled / per-shape `Spearman(I, accuracy)`
and `slope(ΔG ~ I)`:

- v2 pooled: `ρ = 0.977`, `slope = 0.935` (30 model×domain points, exact `I`/`ΔG`).
- shapes: reason `ρ=0.943, slope=0.936` · seqstate `ρ=0.886, slope=1.023` ·
  code `ρ=0.429, slope=1.133` (18 points, exact `I`/`ΔG`).

If it reproduces the paper's figures from the same cache, the instrument is correct.
All 48 cached points reproduce to floating-point tolerance.

---

## Relationship to the theory

This is the most direct *use* of the value theory: the quantities it reports are the
ones validated in the preprint and in
[`docs/14-bridge-generalization.md`](../../docs/14-bridge-generalization.md) — the
out-of-sample bridge `ΔG ~ I(X;Y)` holding across classification, reasoning,
sequential, and code task shapes. The meter packages that validated single-agent
machinery into a reusable instrument with the same honesty discipline as the paper.

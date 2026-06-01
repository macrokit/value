# sim/real — the real-agent test (R1–R5)

Where [`sim/`](../) checks the value laws on *synthetic* worlds (E1–E5), this checks them on **live local
LLMs**. We take a frozen 100-item tool-routing benchmark, treat each model as an agent, and measure the value
quantities (`I(X;Y)`, `ΔG`, `D(q‖p)`) from the models' *actual outputs* — reusing
[`sim/value_sim.py`](../value_sim.py), in nats. Full write-up + results discussion:
[`docs/06-real-agent-test.md`](../../docs/06-real-agent-test.md).

## The mapping

| Theory object | Instantiation |
|---|---|
| World-state `X` | the correct action for an item (K=7 classes: 6 tools + a "no-op" class) |
| Perception `Y_a` | model `a`'s chosen action |
| `q(x)` | empirical marginal of correct actions |
| `r(x)` | set to `q` (so a no-signal agent grows value at 0; the oracle identity `ΔG=I` holds) |
| agent `a` | a local model, greedy decoding; a weak→strong capability ladder |

## Files

- **`bench_data.py`** — loads the frozen corpus + cached model runs and maps them to the value framework.
  Run-discovery is naming-robust (matches rungs by header), **excludes mistral** (a tool-call incompatibility,
  not a capability result), drops **partial** (≠100-task) runs, and rejects **plumbing artifacts** (a run that
  collapses to ~all "no-op" with near-zero `I` — a serving crash, not behavior), keeping the best run per rung.
- **`experiments_real.py`** — computes R1–R5 and writes deliverables to `results/`.
- **`watch_runs.py`** — polls for new ladder runs (used while reusing a parallel benchmarking session's output).
- **`results/`** — `confusions.json` (per-model confusion matrices), `results_table.json` (PASS/FAIL),
  `experiments_output.txt` (full printed run), and `bench_runs/` (the cached raw model runs, so every number
  re-derives offline with no network or model calls).

## Run

```sh
python3 sim/real/experiments_real.py     # prints R1–R5 + PASS/FAIL, rewrites results/
python3 sim/real/bench_data.py           # just the discovered ladder + accuracies
```

No models are called — everything reads the cached runs in `results/bench_runs/`.

## The experiments

| | Claim | Mirrors |
|---|---|---|
| **R1** | `ΔG_a` tracks `I(X;Y_a)`; both rise with model scale | E1 (capacity) |
| **R2** | over-confidence on the same predictions dissipates value (nats) | E2 (Second Law) |
| **R3** | `I(X;Y)` per second of compute across the ladder | doc 02 §5 (I per joule) |
| **R4** | a diverse pair's joint `I` > best single; a redundant re-run adds 0 | E3 (fleet ceiling) |
| **R5** | price/Kelly fleet vs best-single / equal, out-of-sample (+ a compute-budget view) | E4 (pricing) |

## Honest notes

- The in-sample `ΔG = I` is an **arithmetic identity** (oracle posterior + `r = q`); only the ladder
  monotonicity, the out-of-sample tracking, and R5 are empirical. See `docs/06` §2.
- **R5 is an honest negative on the raw-growth axis** (no Shannon's demon): a same-task capability ladder gives
  positively-correlated agents, so Kelly rebalancing has no volatility to harvest and the best agent dominates.
  Pricing still beats equal-weight, and wins under a compute budget. The demon needs *perception diversity*,
  which a scale ladder lacks by construction.
- An 8B rung will extend the ladder when its run lands; it does not change any conclusion.

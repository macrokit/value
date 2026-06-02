# `sim/field/real/` — the real-LLM-agent field test (Rung 7)

The decisive real-agent gate for the wave/field theory of value: replace the toy's
hand-coded replicator rule ([`../dynamic/`](../dynamic/)) with a **real small LLM**
choosing each agent's niche each round, and ask whether the demand wave (doc 08 §3) and
the collective-goal transition (doc 08 §5) survive — *with* their derived gating
conditions (doc 10).

**Read [`PREREGISTRATION.md`](PREREGISTRATION.md) first** (thresholds frozen before any
run; falsification clause up front). The honest write-up is
[`../../../docs/11-real-agent-field-test.md`](../../../docs/11-real-agent-field-test.md).

## Result (one line)

**Pre-registered NEGATIVE (transition) + INCONCLUSIVE-confounded (wave).** Neither
signature emerged under its frozen thresholds. The binding obstacle is **LLM token
bias** (small models pick favourite niche-tokens regardless of value) plus a **weak
noise knob** (sampling temperature is not faithful Vicsek alignment-noise). Neither a
validated positive nor a clean theory-refutation — see docs/11 for the precise,
separated status.

## Files

| file | what |
|---|---|
| `PREREGISTRATION.md` | frozen design + thresholds + falsification clause |
| `llm_economy.py` | the economy: agents choose niches via a cached LLM call; ring (wave) + annealed/quenched (flocking); switching-lag = reallocation inertia; control field; salient-reward mode |
| `experiments.py` | runs the pre-registered checks vs frozen thresholds; `RUNG7_MODEL` env selects the model; writes `results/real_results_<tag>.json` |
| `results/cache.sqlite` | every model call, keyed by (model,temp,seed,agent,round,prompt) — deterministic & re-runnable. **Local-only (gitignored, regenerable via the tunnel);** the committed audit trail is the `results/*.json` verdicts |
| `results/real_results_{0.5b,1.5b}.json` | the **pre-registered** verdicts |
| `results/exploratory_*.json` | **post-hoc** exploratory runs (high-temp extensions; salient-reward wave re-tests) — each is NOT a pre-registered pass |

## Run

```sh
ssh -f -N -L 11434:localhost:11434 blueidea@MacBook-Pro.local   # tunnel to the China-Mac Ollama fleet
python3 sim/field/real/llm_economy.py                            # health check
python3 sim/field/real/experiments.py flocking                  # signature 2 (0.5b, pre-registered)
python3 sim/field/real/experiments.py wave                      # signature 1 (0.5b, pre-registered)
RUNG7_MODEL=qwen2.5:1.5b-instruct python3 sim/field/real/experiments.py flocking   # secondary
```

## Honest scope

Toy-scale (`N=20–40`, `K=8`, `T≤18`, qwen2.5 0.5b/1.5b). This upgrades the *microscopic
rule* from equation to real model; it is **not** a market, not thermodynamic-limit, not
finite-size-scaled. We did **not** escalate past 1.5b (no instrument-fishing). The
exploratory runs locate structure but cannot be reported as pre-registered passes; a
clean positive on either signature would require a **fresh pre-registration** with a
bias-controlled design (symbol-randomised niches; an alignment-noise knob that corrupts
perceived neighbours rather than token sampling) and a confirming run. That is the
concrete next instrument — see docs/11 §3.

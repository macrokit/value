# Data sources & attribution

The real-agent experiments ([`sim/real/`](sim/real/)) evaluate local LLMs on small, frozen
slices of established public benchmarks. The committed run data under `sim/real/*/results/`
contains two kinds of file:

- **`results/raw/*.json`** — *this project's own measurement outputs*: per-item model
  prediction (`pred`), gold label (`gold`), token counts and timing. These are original
  measurements produced here, not redistributed corpus text.
- **`results/data/*.json`** — the *frozen evaluation slices* (the input items + labels) used
  so the runs are reproducible. These contain small subsets of the source benchmarks below,
  redistributed for reproducibility under each source's terms, with attribution.

Only small evaluation subsets (≈100–240 items per domain) are included. Each slice can be
regenerated from its upstream source via the harness (`sim/real/v2/datasets.py`,
`sim/real/shapes/datasets_shapes.py`).

| Domain (in this repo) | Source benchmark | Upstream | License |
|---|---|---|---|
| `intent` (assistant-router intents) | **CLINC150 / OOS-Eval** | [github.com/clinc/oos-eval](https://github.com/clinc/oos-eval) | CC BY 3.0 |
| `mcqa` (multiple-choice QA) | **MMLU** | [huggingface.co/datasets/cais/mmlu](https://huggingface.co/datasets/cais/mmlu) | MIT |
| `topic` (news topic) | **AG News** | [huggingface.co/datasets/fancyzhx/ag_news](https://huggingface.co/datasets/fancyzhx/ag_news) | Academic/research use (Zhang, Zhao & LeCun, 2015) |
| `reason` (grade-school math) | **GSM8K** | [huggingface.co/datasets/openai/gsm8k](https://huggingface.co/datasets/openai/gsm8k) | MIT |
| `code` (program synthesis) | **MBPP** | [huggingface.co/datasets/google-research-datasets/mbpp](https://huggingface.co/datasets/google-research-datasets/mbpp) | CC BY 4.0 |
| `seqstate` (sequential decision) | *synthetic* (this project) | — | original, no upstream |

## Citations

- **CLINC150 / OOS-Eval** — Larson et al., *An Evaluation Dataset for Intent Classification
  and Out-of-Scope Prediction*, EMNLP 2019.
- **MMLU** — Hendrycks et al., *Measuring Massive Multitask Language Understanding*, ICLR 2021.
- **AG News** — Zhang, Zhao & LeCun, *Character-level Convolutional Networks for Text
  Classification*, NeurIPS 2015.
- **GSM8K** — Cobbe et al., *Training Verifiers to Solve Math Word Problems*, 2021.
- **MBPP** — Austin et al., *Program Synthesis with Large Language Models*, 2021.

All trademarks and dataset rights remain with their respective owners. If you are a rights
holder and would prefer a slice not be redistributed here, open an issue and it will be
removed (the harness can always regenerate it from source).

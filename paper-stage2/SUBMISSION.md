# OpenReview submission metadata (TMLR) — anonymous

Paste-ready text for the OpenReview submission form. All fields are author-free
(the abstract/keywords carry no identity). Title matches the PDF exactly.

## Title
Information Limits and Attractor Dynamics in Economies of Frontier LLM Agents: A Pre-Registered Test

## TL;DR (optional field, one sentence)
A $139, fully pre-registered experiment on frontier LLM agents confirms an information-theoretic capacity region for market-coupled agent economies (relative growth = relative claimed information to 46 millinats), while finding that no tested LLM population realizes the smooth mean-field regime — they behave as discrete attractor systems.

## Abstract
We report a pre-registered, two-part experiment on small economies of frontier language-model agents (Claude Opus 4.8), testing two quantitative predictions about coupled multi-agent systems: an information-theoretic capacity region for wealth growth under market coupling, and a mean-field residual-scaling law for population misalignment under incentive and control levers. All predictions, acceptance bands, and decision rules were frozen in a public git chain before any run; every reported number re-derives mechanically from cached model outputs; the entire experiment cost $138.76 in metered API spend and is re-runnable at zero cost from the cache.

The whole-experiment verdict of record, under the frozen rule applied mechanically, is cannot-answer-pass (CAP): the rule conditions the overall outcome on the residual-scaling test, and no tested population entered that law's required regime. Within this verdict the two parts split sharply, and we report the split exactly as it fell.

Result 1 (prediction (i), confirmed within its scope): in parimutuel-coupled economies, relative growth equals relative claimed information — the gap law G_a - G_b = I_a - I_b holds to a worst-case 46 millinats (pre-registered band: 50) across four perception structures; coalition value is submodular exactly where channels are conditionally independent, and a designed XOR synergy control flips it supermodular by 0.62 >= ln2/2 nats, with agents reasoning out the joint bit; the joint growth ceiling G_S <= H(X) binds exactly; and the best-informed agent absorbs essentially the whole wealth pool in 4/5 market seeds. One supporting check — equal terminal wealth for information clones — failed its band and is disclosed with its mechanism.

Result 2 (prediction (ii), domain not found): in all 72 population runs, goal dispersion collapsed (V -> 0; maximum 4.85 against a frozen floor of 5.31), leaving zero of nine grid conditions in-regime for the scaling fit; the population's response to the two levers was a step function across the dominance boundary (gamma vs 12g) rather than a smooth response, and cells near the boundary were bistable with seed-selected outcomes. Together with two prior small-model arms (gradient saturation; non-response), no tested LLM population at any capability level realizes the noise-maintained-dispersion regime that smooth mean-field models assume; we retire the law to its mathematical scope — retired, not falsified. Near-rational LLM populations behaved as discrete attractor systems — locally near-deterministic, globally seed-sensitive — which suggests that population-level interventions on such systems switch attractors or do nothing, rather than acting marginally. We release the full protocol, pre-registration chain, call cache, and analysis code.

> Note: the abstract above is plain-text with ASCII math for form safety. OpenReview
> renders `$...$` MathJax if you prefer, e.g. `$\hat G_a-\hat G_b=\hat I_a-\hat I_b$`,
> `$\ge \ln 2/2$`, `$\hat G_S\le H(X)$`, `$V\to 0$`, `$\gamma\gtrless 12g$`.

## Keywords (comma-separated)
large language model agents, multi-agent systems, pre-registration, information theory, growth-optimal (Kelly) betting, capacity region, prediction markets, mean-field models, attractor dynamics, AI safety

## Certifications / metadata reminders (OpenReview form)
- Submission is anonymized (PDF + supplementary ZIP both). ✓
- Declare: no human subjects/IRB; funding = none (self-funded — declared in metadata,
  NOT in the anonymous PDF); competing interests = none. Conflicts: list any advisor/
  co-author/institution domains for the COI checker.
- Supplementary material: `stage2-supplement-anon.zip` (built by `make-supplement.sh`).

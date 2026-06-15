"""
mock_backend.py — deterministic offline chat_fn for testing the gate pipeline with
ZERO API spend. Not used for any verdict; exists only to shake out parsing/wiring and
the verdict logic before the owner's key is spent.

MOCK_MODE=responsive (default): a rational greedy agent — picks the label with the
highest stated reward (+ a small teamwork pull); on elicitation, concentrates mass on
states consistent with the observed bit. Should drive the gate to PASS.
MOCK_MODE=uniform: a non-responding agent (random niche; uniform posterior) — should
drive the gate to FAIL, reproducing the doc-13/18 small-model failure mode.
"""
from __future__ import annotations
import os, re, json
import numpy as np

MODE = os.environ.get("MOCK_MODE", "responsive")


def _rng(seed, agent, rnd):
    return np.random.default_rng((int(seed) * 100003 + int(agent) * 131 + int(rnd)) % (2**32))


def mock_chat(model, temp, prompt, seed, agent, rnd, k=8):
    # ---- elicitation prompt (G-3) ----
    if '"probs"' in prompt:
        m = re.search(r"bit b(\d+).*?is (\d+)", prompt, re.S)
        if MODE == "uniform" or not m:
            return json.dumps({"probs": [1 / 8] * 8})
        j, v = int(m.group(1)), int(m.group(2))
        p = np.array([1.0 if ((x >> j) & 1) == v else 0.0 for x in range(8)])
        p = p / p.sum()
        # a touch of noise so it's not a perfect oracle
        p = 0.9 * p + 0.1 / 8
        return json.dumps({"probs": (p / p.sum()).round(4).tolist()})

    # ---- niche-economy prompt (G-1/G-2) ----
    rng = _rng(seed, agent, rnd)
    if MODE == "uniform":
        return json.dumps({"niche": int(rng.integers(0, k))})
    # parse the reward line (label space)
    rewards = np.zeros(k)
    for line in prompt.splitlines():
        if line.lower().startswith("niche rewards this round"):
            for lbl, val in re.findall(r"niche (\d+): (-?\d+\.?\d*)", line):
                if int(lbl) < k:
                    rewards[int(lbl)] = float(val)
    # parse neighbour tally for a light teamwork pull
    nbr = np.zeros(k)
    for line in prompt.splitlines():
        if "neighbour" in line.lower():
            for lbl, cnt in re.findall(r"niche (\d+): (\d+) neighbour", line):
                if int(lbl) < k:
                    nbr[int(lbl)] = int(cnt)
    score = rewards + 1.0 * nbr / max(nbr.sum(), 1)   # J=1 teamwork pull, normalised
    choice = int(np.argmax(score + 1e-6 * rng.standard_normal(k)))
    return json.dumps({"niche": choice})

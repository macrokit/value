"""
value_meter — measure any agent's *value profile* on a task (nats).

The most direct way to *use* the value theory (preprint: doi.org/10.5281/zenodo.20487041):
give it an agent's recorded outputs vs ground truth and it returns a principled,
information-theoretic profile of how much value the agent generates, how much it
dissipates, and how much value it buys per unit of compute — with nulls, CIs, and
the honesty caveats baked into the output.

Model-agnostic by design. The core takes plain records

    Record(gold, pred [, prob] [, cost_tokens] [, cost_latency])

so it works on *any* agent's recorded outputs — no model, inference, or framework
dependency. The information-theoretic primitives (entropy / KL / mutual information)
are imported from the project's `sim/value_sim.py`, NOT reimplemented here.

What it computes (all in nats; bits shown alongside for I):
  1. I(X;Y)      — the value ceiling (mutual information of gold X vs chosen Y),
                   reported against a permutation/independence null (above-chance,
                   not raw).
  2. ΔG          — realized value-generation rate, as TWO clearly-labelled numbers:
                     • in-sample  = I  (an arithmetic identity — definitional, no
                       empirical weight; used only to confirm units), and
                     • out-of-sample (calibrate the posterior on a fit split, score
                       on a holdout) — the EMPIRICAL number, with a bootstrap CI.
  3. D(q‖p)      — dissipation: value lost to miscalibration. If `prob` is supplied
                   we use the agent's STATED belief; otherwise we CONSTRUCT a belief
                   from the confusion matrix and report the dissipation of *that*
                   stated belief (flagged explicitly — it is not a probability the
                   model reported).
  4. value/compute — I / mean_tokens (PRIMARY, load-free) and I / median_latency
                   (SECONDARY; median is load-robust — the Lever-1 lesson).
  5. H(X) + saturation I/H(X) — the task's world-entropy and how close the agent is
                   to the ceiling (saturation → more compute can't add value).

Honesty is the brand. Every profile carries its caveats (in-sample = definitional;
dissipation = a stated/constructed belief; CIs not bare point estimates; the profile
is TASK-RELATIVE; and the scope is the validated SINGLE-AGENT layer only — no
multi-agent coordination/governance).

Author byline: Cheng Qian.
"""
from __future__ import annotations

import math
import os
import random
import sys
from dataclasses import dataclass, field, asdict
from typing import Any, Optional, Sequence

import numpy as np

# --- reuse the project's information-theoretic primitives (do NOT reimplement) ---
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", ".."))
for _p in (os.path.join(_REPO, "sim"), _REPO):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import value_sim as _v  # entropy, kl, mutual_information  (nats)

LN2 = math.log(2.0)


# ===========================================================================
# Records — the model-agnostic input
# ===========================================================================
@dataclass
class Record:
    """One scored item of an agent's run.

    gold          : the correct action/label (any hashable).
    pred          : the agent's chosen action/label (any hashable). A model that
                    silently degrades should emit a distinct "unparseable" token
                    (e.g. "?") as `pred` rather than a wrong label — see
                    `degraded_rate` in the profile.
    prob          : OPTIONAL stated belief — a probability over the gold class set.
                    Either a dict {class: p} or a sequence aligned to `classes`.
                    If given, dissipation uses the agent's OWN stated belief.
    cost_tokens   : OPTIONAL total tokens spent on this item (prompt+completion).
    cost_latency  : OPTIONAL wall-clock seconds for this item.
    """
    gold: Any
    pred: Any
    prob: Optional[Any] = None
    cost_tokens: Optional[float] = None
    cost_latency: Optional[float] = None


# ===========================================================================
# The value profile — the output
# ===========================================================================
@dataclass
class ValueProfile:
    # task shape
    n: int
    n_classes: int
    classes: list
    H_X_nats: float                     # world-entropy of the gold marginal
    degraded_rate: float                # fraction of preds that are unparseable tokens

    # 1. value ceiling
    I_nats: float
    I_bits: float
    I_null_mean_nats: float             # mean I under label-permutation (chance floor)
    I_null_p95_nats: float
    I_perm_p_value: float               # P(I_perm >= I_observed)
    I_above_chance: bool                # I > 3 * null mean (the info-floor test)
    saturation: float                   # I / H(X)  — closeness to the ceiling

    # 2. realized value-generation rate
    dG_in_sample_nats: float            # == I (arithmetic identity; DEFINITIONAL)
    dG_out_of_sample_nats: float        # EMPIRICAL: calibrate on fit, score on holdout
    dG_oos_ci_nats: tuple               # bootstrap 95% CI over holdout items
    split_frac: float
    split_seed: int
    n_holdout: int

    # 3. dissipation (Second Law term)
    dissipation_nats: float
    dissipation_belief: str             # "stated (agent prob)" | "constructed (over-confident)"
    dissipation_note: str

    # 4. value per compute
    I_per_1k_tokens: Optional[float]    # PRIMARY (load-free)
    mean_tokens: Optional[float]
    I_per_sec_median_latency: Optional[float]   # SECONDARY (median = load-robust)
    median_latency_s: Optional[float]

    # honesty
    caveats: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["dG_oos_ci_nats"] = list(self.dG_oos_ci_nats)
        return d


# ===========================================================================
# internals — confusion / calibration / split / per-item value
# (mirrors sim/real/v2/experiments_v2.py so the numbers reproduce exactly)
# ===========================================================================
UNPARSED_TOKENS = ("?", "__CODE__", None, "")


def _coerce(records: Sequence) -> list:
    out = []
    for r in records:
        if hasattr(r, "gold") and hasattr(r, "pred"):   # duck-typed Record
            # rebuild to this module's Record (guards the `python -m` double-import,
            # where the adapter's Record is a distinct class object)
            out.append(Record(gold=r.gold, pred=r.pred,
                              prob=getattr(r, "prob", None),
                              cost_tokens=getattr(r, "cost_tokens", None),
                              cost_latency=getattr(r, "cost_latency", None)))
        elif isinstance(r, dict):
            out.append(Record(**{k: r.get(k) for k in
                                 ("gold", "pred", "prob", "cost_tokens", "cost_latency")}))
        else:  # (gold, pred) tuple
            out.append(Record(*r))
    return out


def _class_sets(recs: list, classes: Optional[list]):
    """X = gold class set (sorted, stable); Y = X plus any extra pred-only labels
    (e.g. the unparseable token), so degraded output is a column, not a wrong row."""
    if classes is None:
        classes = sorted({r.gold for r in recs}, key=lambda c: (str(type(c)), c))
    extra = [p for p in sorted({r.pred for r in recs}, key=lambda c: str(c))
             if p not in classes]
    ylab = list(classes) + extra
    return list(classes), ylab


def _confusion(recs, classes, ylab, ids=None):
    idx = {c: i for i, c in enumerate(classes)}
    yidx = {y: i for i, y in enumerate(ylab)}
    C = np.zeros((len(classes), len(ylab)))
    for i, r in enumerate(recs):
        if ids is not None and i not in ids:
            continue
        if r.gold not in idx or r.pred not in yidx:
            continue
        C[idx[r.gold], yidx[r.pred]] += 1
    return C


def _calib(C_fit, alpha=0.5):
    """Laplace-smoothed posterior p(x|y) from a fit-split confusion matrix."""
    P = C_fit + alpha
    return P / P.sum(axis=0, keepdims=True)


def _marginal(recs, classes):
    idx = {c: i for i, c in enumerate(classes)}
    c = np.zeros(len(classes))
    for r in recs:
        if r.gold in idx:
            c[idx[r.gold]] += 1
    return c / c.sum()


def _stratified_split(recs, classes, seed, frac):
    """Seeded, gold-stratified fit/holdout split over record indices.
    Matches sim/real/v2/experiments_v2.split (sorted ids, Random(seed).shuffle,
    k = round(len*frac))."""
    by = {c: [] for c in classes}
    for i, r in enumerate(recs):
        if r.gold in by:
            by[r.gold].append(i)
    rng = random.Random(seed)
    fit, hold = [], []
    for c in classes:
        ids = sorted(by[c])
        rng.shuffle(ids)
        k = int(round(len(ids) * frac))
        fit += ids[:k]
        hold += ids[k:]
    return set(fit), set(hold)


def _per_item_values(recs, post, classes, ylab, ids, r):
    """ln p(x_gold | y_pred) / r(x_gold) per holdout item (the realized value)."""
    idx = {c: i for i, c in enumerate(classes)}
    yidx = {y: i for i, y in enumerate(ylab)}
    vals = []
    for i, rec in enumerate(recs):
        if i not in ids or rec.gold not in idx or rec.pred not in yidx:
            continue
        x = idx[rec.gold]
        y = yidx[rec.pred]
        vals.append(float(np.log(post[x, y] / r[x])))
    return vals


def _prob_vector(rec, classes):
    """Normalize a record's stated belief into an aligned probability vector, or None."""
    if rec.prob is None:
        return None
    if isinstance(rec.prob, dict):
        vec = np.array([float(rec.prob.get(c, 0.0)) for c in classes], dtype=float)
    else:
        vec = np.asarray(rec.prob, dtype=float)
        if len(vec) != len(classes):
            return None
    s = vec.sum()
    if s <= 0:
        return None
    return vec / s


# ===========================================================================
# the public API
# ===========================================================================
def value_profile(records: Sequence,
                  classes: Optional[list] = None,
                  split: float = 0.5,
                  seed: int = 7,
                  n_boot: int = 2000,
                  n_perm: int = 500) -> ValueProfile:
    """Compute the full value profile for one (agent, task) run.

    records : a sequence of Record (or dicts / (gold,pred) tuples).
    classes : optional explicit gold class set (else inferred, sorted).
    split   : holdout fraction is (1 - split fit); `split` is the FIT fraction
              (default 0.5 — calibrate on half, score on the other half).
    seed    : split seed (7 reproduces the paper's published per-model numbers).
    """
    recs = _coerce(records)
    if not recs:
        raise ValueError("value_profile: no records given.")
    rng = np.random.default_rng(seed)
    classes, ylab = _class_sets(recs, classes)
    n = len(recs)

    # --- task shape -------------------------------------------------------
    r = _marginal(recs, classes)
    H_X = _v.entropy(r)
    degraded = float(np.mean([rec.pred in UNPARSED_TOKENS for rec in recs]))

    # --- 1. value ceiling I(X;Y) + permutation null -----------------------
    C = _confusion(recs, classes, ylab)
    I = _v.mutual_information(C)
    I_bits = I / LN2
    golds = [c for c in (rec.gold for rec in recs) if c in classes]
    preds = [rec.pred for rec in recs if rec.gold in classes]
    idx = {c: i for i, c in enumerate(classes)}
    yidx = {y: i for i, y in enumerate(ylab)}
    g_arr = np.array([idx[g] for g in golds])
    p_arr = np.array([yidx[p] for p in preds])
    null_Is = np.empty(n_perm)
    for k in range(n_perm):
        sp = rng.permutation(p_arr)
        Cp = np.zeros((len(classes), len(ylab)))
        np.add.at(Cp, (g_arr, sp), 1.0)
        null_Is[k] = _v.mutual_information(Cp)
    null_mean = float(null_Is.mean())
    null_p95 = float(np.percentile(null_Is, 95))
    perm_p = float((np.sum(null_Is >= I) + 1) / (n_perm + 1))
    above_chance = bool(I > 3.0 * max(null_mean, 1e-12))
    saturation = float(I / H_X) if H_X > 0 else float("nan")

    # --- 2. ΔG in-sample (= I, definitional) and out-of-sample (empirical) -
    fit, hold = _stratified_split(recs, classes, seed, split)
    post = _calib(_confusion(recs, classes, ylab, fit))
    hold_vals = _per_item_values(recs, post, classes, ylab, hold, r)
    dG_oos = float(np.mean(hold_vals)) if hold_vals else float("nan")
    # bootstrap CI over holdout items
    if len(hold_vals) >= 2:
        hv = np.asarray(hold_vals)
        boots = np.array([hv[rng.integers(0, len(hv), len(hv))].mean()
                          for _ in range(n_boot)])
        ci = (float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5)))
    else:
        ci = (float("nan"), float("nan"))
    dG_in = I  # arithmetic identity (oracle posterior over the full sample)

    # --- 3. dissipation D(q‖p) -------------------------------------------
    dissipation, belief_kind, belief_note = _dissipation(recs, classes, ylab, fit, hold, r)

    # --- 4. value per compute --------------------------------------------
    toks = [rec.cost_tokens for rec in recs if rec.cost_tokens is not None]
    lats = [rec.cost_latency for rec in recs if rec.cost_latency is not None]
    mean_tokens = float(np.mean(toks)) if toks else None
    median_lat = float(np.median(lats)) if lats else None       # median: load-robust
    I_per_1k = (I / mean_tokens * 1000.0) if mean_tokens else None
    I_per_sec = (I / median_lat) if median_lat else None

    caveats = [
        "TASK-RELATIVE: I, ΔG, dissipation are measured against THIS task's gold; "
        "they are a per-(agent, task) profile, not a universal agent score.",
        "in-sample ΔG = I is an arithmetic IDENTITY (definitional, no empirical "
        "weight); the empirical content is the OUT-OF-SAMPLE ΔG and its CI.",
        f"dissipation is computed against a {belief_kind} belief — {belief_note}",
        "all figures carry a null or a bootstrap CI; read the intervals, not the "
        "bare point estimates.",
        "SCOPE: this is the validated SINGLE-AGENT layer only. It does NOT measure "
        "multi-agent coordination/governance (that layer is unvalidated — out of scope).",
    ]
    if degraded > 0.5:
        caveats.insert(0, f"WARNING: {degraded:.0%} of preds are unparseable — this "
                          "likely reflects plumbing degradation (truncation/refusal), "
                          "NOT capability; the I/ΔG numbers are not trustworthy.")

    return ValueProfile(
        n=n, n_classes=len(classes), classes=list(classes),
        H_X_nats=H_X, degraded_rate=degraded,
        I_nats=I, I_bits=I_bits, I_null_mean_nats=null_mean, I_null_p95_nats=null_p95,
        I_perm_p_value=perm_p, I_above_chance=above_chance, saturation=saturation,
        dG_in_sample_nats=dG_in, dG_out_of_sample_nats=dG_oos, dG_oos_ci_nats=ci,
        split_frac=split, split_seed=seed, n_holdout=len(hold_vals),
        dissipation_nats=dissipation, dissipation_belief=belief_kind,
        dissipation_note=belief_note,
        I_per_1k_tokens=I_per_1k, mean_tokens=mean_tokens,
        I_per_sec_median_latency=I_per_sec, median_latency_s=median_lat,
        caveats=caveats,
    )


def _dissipation(recs, classes, ylab, fit, hold, r):
    """Second-Law dissipation term, in nats.

    Two modes, always labelled:
      • STATED  (some record carries `prob`): per holdout item, the world-conditional
        optimum is p*(x|y) (calibrated on the fit split); the agent bets its stated
        belief q. The value it dissipates vs a perfectly-calibrated bettor is
        D(p* ‖ q), averaged over holdout items.
      • CONSTRUCTED (no prob): we contrast a CALIBRATED belief with an OVER-CONFIDENT
        one (argmax → p=1) built from the same confusion matrix, and report the value
        the over-confident belief dissipates (ΔG_cal − ΔG_over ≥ 0). This is the
        miscalibration cost of a belief the model did NOT necessarily report.
    """
    idx = {c: i for i, c in enumerate(classes)}
    yidx = {y: i for i, y in enumerate(ylab)}
    have_prob = any(rec.prob is not None for rec in recs)
    post_cal = _calib(_confusion(recs, classes, ylab, fit))

    if have_prob:
        diss = []
        for i, rec in enumerate(recs):
            if i not in hold or rec.gold not in idx or rec.pred not in yidx:
                continue
            q = _prob_vector(rec, classes)
            if q is None:
                continue
            y = yidx[rec.pred]
            pstar = post_cal[:len(classes), y]
            pstar = pstar / pstar.sum()
            diss.append(_v.kl(pstar, q))
        d = float(np.mean(diss)) if diss else float("nan")
        return d, "stated (agent prob)", (
            "the agent's OWN reported probability; D(p*‖q) vs the calibrated optimum.")

    # constructed over-confident belief
    C_fit = _confusion(recs, classes, ylab, fit)
    post_over = np.full((len(classes), len(ylab)), 1e-9)
    for y in range(len(ylab)):
        post_over[np.argmax(C_fit[:, y]), y] = 1.0
    post_over /= post_over.sum(axis=0, keepdims=True)
    gc = _per_item_values(recs, post_cal, classes, ylab, hold, r)
    go = _per_item_values(recs, post_over, classes, ylab, hold, r)
    d = float(np.mean(gc) - np.mean(go)) if gc and go else float("nan")
    return d, "constructed (over-confident)", (
        "a CONSTRUCTED argmax/over-confident belief, NOT a probability the model "
        "reported; the gap ΔG_calibrated − ΔG_overconfident it would dissipate.")


# ===========================================================================
# human-readable rendering
# ===========================================================================
def format_profile(p: ValueProfile, title: str = "") -> str:
    L = []
    bar = "=" * 72
    L.append(bar)
    L.append(f"  VALUE PROFILE{('  —  ' + title) if title else ''}")
    L.append(bar)
    L.append(f"  task: n={p.n} items, K={p.n_classes} classes, "
             f"H(X)={p.H_X_nats:.3f} nats ({p.H_X_nats/LN2:.3f} bits)")
    if p.degraded_rate:
        L.append(f"        degraded/unparseable preds: {p.degraded_rate:.1%}")
    L.append("")
    L.append("  1) VALUE CEILING  I(X;Y)")
    chance = "ABOVE chance" if p.I_above_chance else "NOT above chance (≈ null!)"
    L.append(f"       I = {p.I_nats:.4f} nats  ({p.I_bits:.4f} bits)   [{chance}]")
    L.append(f"       permutation null: mean {p.I_null_mean_nats:.4f}, "
             f"p95 {p.I_null_p95_nats:.4f} nats   (perm p = {p.I_perm_p_value:.3g})")
    L.append(f"       saturation I/H(X) = {p.saturation:.3f}  "
             f"(→1 means more compute can't add value)")
    L.append("")
    L.append("  2) REALIZED VALUE-GENERATION RATE  ΔG")
    L.append(f"       in-sample      = {p.dG_in_sample_nats:.4f} nats   "
             f"[= I — arithmetic IDENTITY, definitional only]")
    lo, hi = p.dG_oos_ci_nats
    L.append(f"       out-of-sample  = {p.dG_out_of_sample_nats:.4f} nats   "
             f"95% CI [{lo:.4f}, {hi:.4f}]   <- the EMPIRICAL number")
    L.append(f"       (calibrate on {p.split_frac:.0%} fit split, score on "
             f"{p.n_holdout} holdout items; seed {p.split_seed})")
    L.append("")
    L.append("  3) DISSIPATION  D(q‖p)   (Second-Law term: value lost to miscalibration)")
    L.append(f"       dissipation = {p.dissipation_nats:.4f} nats")
    L.append(f"       belief: {p.dissipation_belief} — {p.dissipation_note}")
    L.append("")
    L.append("  4) VALUE PER COMPUTE")
    if p.I_per_1k_tokens is not None:
        L.append(f"       I / tokens   = {p.I_per_1k_tokens:.4f} nats / 1k tokens   "
                 f"(PRIMARY, load-free; mean {p.mean_tokens:.0f} tok/item)")
    else:
        L.append("       I / tokens   = n/a (no cost_tokens supplied)")
    if p.I_per_sec_median_latency is not None:
        L.append(f"       I / latency  = {p.I_per_sec_median_latency:.4f} nats / s   "
                 f"(SECONDARY, median {p.median_latency_s:.3f}s — load-robust)")
    else:
        L.append("       I / latency  = n/a (no cost_latency supplied)")
    L.append("")
    L.append("  CAVEATS (read these — honesty is the instrument):")
    for c in p.caveats:
        L.append(f"     • {c}")
    L.append(bar)
    return "\n".join(L)


# ===========================================================================
# CLI
# ===========================================================================
def _main(argv=None):
    import argparse
    import json
    from adapters import load_records, describe_source

    ap = argparse.ArgumentParser(
        prog="value_meter",
        description="Measure an agent's value profile on a task (nats). "
                    "Reuses the value theory's I/ΔG/dissipation machinery.")
    ap.add_argument("input", help="a records JSON, or a project run JSON "
                                  "(sim/real/v2 or sim/real/shapes). See adapters.py.")
    ap.add_argument("--split", type=float, default=0.5,
                    help="fit fraction (calibration split); default 0.5.")
    ap.add_argument("--seed", type=int, default=7,
                    help="split seed; 7 reproduces the paper's per-model numbers.")
    ap.add_argument("--data", default=None,
                    help="optional dataset JSON (project adapter) giving the gold "
                         "class set + canonical split.")
    ap.add_argument("--json", action="store_true",
                    help="emit the profile as machine-readable JSON.")
    args = ap.parse_args(argv)

    records, classes = load_records(args.input, data_path=args.data)
    prof = value_profile(records, classes=classes, split=args.split, seed=args.seed)
    if args.json:
        print(json.dumps(prof.to_dict(), indent=2))
    else:
        print(format_profile(prof, title=describe_source(args.input)))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())

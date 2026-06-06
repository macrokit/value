"""
adapters.py — turn inputs into value_meter Records.

Two input families are supported so the meter runs both on YOUR agent and on this
project's cached runs (the latter is also the self-test, test_reproduces_paper.py):

  A. Generic records JSON — the portable format. Either
        {"records": [{"gold": "...", "pred": "...", "cost_tokens": 42, ...}, ...],
         "classes": ["...", ...]}          # classes optional
     or just a bare list  [{"gold":..., "pred":...}, ...].
     Optional per-record fields: prob, cost_tokens, cost_latency.

  B. Project run JSON — the existing harness output
        sim/real/v2/results/raw/<model>__<domain>.json
        sim/real/shapes/results/raw/<model>__<shape>.json
     a dict { "<id>": {"gold","pred","prompt_tokens","eval_tokens","total_ns",...} }.
     For these, pass the matching dataset (data/<domain>.json) via --data, or let the
     adapter auto-locate it next to the run, so the gold CLASS SET and canonical
     ordering match the paper exactly (records are emitted in id order 0..n-1).

`prob` (stated belief) is honored from generic records; project runs don't carry a
stated probability vector, so the meter falls back to the constructed-belief
dissipation (clearly labelled in the output).
"""
from __future__ import annotations

import json
import os
import re

from value_meter import Record


# --------------------------------------------------------------------------
def _is_project_run(obj) -> bool:
    """A project run is a dict keyed by stringy ids whose values have gold+pred and
    the harness cost fields."""
    if not isinstance(obj, dict):
        return False
    vals = list(obj.values())
    if not vals or not isinstance(vals[0], dict):
        return False
    v0 = vals[0]
    return ("gold" in v0 and "pred" in v0
            and ("total_ns" in v0 or "eval_tokens" in v0 or "prompt_tokens" in v0))


def _find_data_for_run(run_path: str):
    """Given .../results/raw/<model>__<domain>.json, locate .../results/data/<domain>.json."""
    base = os.path.basename(run_path)
    m = re.match(r".+__(.+)\.json$", base)
    if not m:
        return None
    domain = m.group(1)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(run_path)), "data")
    cand = os.path.join(data_dir, f"{domain}.json")
    return cand if os.path.exists(cand) else None


def _records_from_project_run(run: dict, data_path: str | None):
    """Emit Records in id order 0..n-1 so the seeded split reproduces the paper.
    Cost: tokens = prompt_tokens + eval_tokens; latency = total_ns / 1e9 (seconds)."""
    classes = None
    order = None
    if data_path and os.path.exists(data_path):
        data = json.load(open(data_path))
        classes = data.get("classes")
        # canonical id order from the dataset
        order = [str(it["id"]) for it in sorted(data["items"], key=lambda x: x["id"])]
    if order is None:
        order = sorted(run.keys(), key=lambda s: int(s))

    recs = []
    for sid in order:
        o = run.get(sid)
        if o is None:
            continue
        toks = (o.get("prompt_tokens") or 0) + (o.get("eval_tokens") or 0)
        ns = o.get("total_ns")
        recs.append(Record(
            gold=o["gold"], pred=o["pred"],
            cost_tokens=(toks or None),
            cost_latency=(ns / 1e9 if ns else None),
        ))
    return recs, classes


def load_records(path: str, data_path: str | None = None):
    """Load (records, classes) from either input family. `classes` may be None
    (then value_meter infers the gold class set)."""
    obj = json.load(open(path))

    if _is_project_run(obj):
        dp = data_path or _find_data_for_run(path)
        return _records_from_project_run(obj, dp)

    # generic records JSON
    if isinstance(obj, dict) and "records" in obj:
        rows = obj["records"]
        classes = obj.get("classes")
    elif isinstance(obj, list):
        rows = obj
        classes = None
    else:
        raise ValueError(
            f"{path}: unrecognized input. Expected a project run dict, a "
            f'{{"records": [...]}} object, or a bare list of records.')
    recs = [Record(
        gold=r["gold"], pred=r["pred"],
        prob=r.get("prob"),
        cost_tokens=r.get("cost_tokens"),
        cost_latency=r.get("cost_latency"),
    ) for r in rows]
    return recs, classes


def describe_source(path: str) -> str:
    base = os.path.basename(path)
    m = re.match(r"(.+)__(.+)\.json$", base)
    if m:
        return f"{m.group(1)} on {m.group(2)}"
    return base

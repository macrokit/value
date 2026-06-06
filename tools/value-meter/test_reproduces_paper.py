"""
test_reproduces_paper.py — the ACCEPTANCE CRITERION for the value-meter.

Runs the model-agnostic value-meter on the project's CACHED runs and asserts it
reproduces the published numbers:

  • v2 / classification  (sim/real/v2/results/r1_points.json):
       per (model, domain) I(X;Y) and out-of-sample ΔG_holdout, and the pooled
       Spearman(I, accuracy) and slope(ΔG ~ I) the paper reports (ρ=0.977, slope=0.935).

  • Lever-2 / task shapes (sim/real/shapes/results/lever2_analysis.json):
       per (model, shape) I and ΔG_holdout, and per-shape Spearman / slope
       (reason ρ=0.943 slope=0.936 · seqstate ρ=0.886 slope=1.023 · code ρ=0.429 slope=1.133).

If the meter reproduces the paper's figures from the same cache, the instrument is
correct. The meter is model-agnostic; here the project-JSON adapter feeds it the
cached runs exactly as the original harness saw them (records in id order, same gold
class set, same seed-7 stratified split).

Run:  python3 test_reproduces_paper.py        (plain asserts; exit 0 = PASS)
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
V2 = os.path.join(REPO, "sim", "real", "v2", "results")
SHAPES = os.path.join(REPO, "sim", "real", "shapes", "results")

sys.path.insert(0, HERE)
from value_meter import value_profile          # noqa: E402
from adapters import load_records              # noqa: E402

TOL = 1e-6          # I and ΔG are deterministic given the seed → tight tolerance


def _spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])


def _slope(x, y):
    return float(np.polyfit(np.asarray(x, float), np.asarray(y, float), 1)[0])


def _profile_for(run_path, data_path):
    records, classes = load_records(run_path, data_path=data_path)
    # n_perm/n_boot small here: the asserted quantities (I, ΔG point estimates) are
    # independent of the null/bootstrap, which only feed the CI/floor reporting.
    return value_profile(records, classes=classes, split=0.5, seed=7,
                         n_perm=50, n_boot=200)


def _check(label, got, want, tol=TOL):
    ok = abs(got - want) <= tol
    flag = "ok  " if ok else "FAIL"
    print(f"   [{flag}] {label}: got {got:.6f}  want {want:.6f}  (Δ={got-want:+.2e})")
    assert ok, f"{label}: {got} != {want} (Δ={got-want})"


# ===========================================================================
def test_v2_classification():
    print("\n── v2 / classification (r1_points.json) ──────────────────────────")
    pts = json.load(open(os.path.join(V2, "r1_points.json")))
    accs, Is, dGs = [], [], []
    for p in pts:
        run = os.path.join(V2, "raw", f"{p['model']}__{p['domain']}.json")
        data = os.path.join(V2, "data", f"{p['domain']}.json")
        prof = _profile_for(run, data)
        _check(f"{p['model']:9s}/{p['domain']:7s} I", prof.I_nats, p["I"])
        _check(f"{p['model']:9s}/{p['domain']:7s} ΔG", prof.dG_out_of_sample_nats, p["dG_hold"])
        # accuracy for the pooled rank/slope checks
        acc = sum(1 for r in load_records(run, data_path=data)[0] if r.gold == r.pred) / prof.n
        accs.append(acc); Is.append(prof.I_nats); dGs.append(prof.dG_out_of_sample_nats)
    rho = _spearman(accs, Is); slope = _slope(Is, dGs)
    print(f"   pooled Spearman(I,acc) = {rho:.3f}  (paper 0.977)")
    print(f"   pooled slope(ΔG~I)     = {slope:.3f}  (paper 0.935)")
    assert abs(rho - 0.977) < 0.01, rho
    assert abs(slope - 0.935) < 0.01, slope


def test_shapes():
    print("\n── Lever-2 / task shapes (lever2_analysis.json) ──────────────────")
    analysis = json.load(open(os.path.join(SHAPES, "lever2_analysis.json")))
    want_rho = {"reason": 0.942857, "seqstate": 0.885714, "code": 0.428571}
    want_slope = {"reason": 0.936031, "seqstate": 1.022740, "code": 1.132539}
    for shape, blk in analysis["shapes"].items():
        if blk.get("status") != "complete":
            continue
        accs, Is, dGs = [], [], []
        for row in blk["points"]:
            model, acc, I_pub, dG_pub = row[0], row[1], row[2], row[3]
            run = os.path.join(SHAPES, "raw", f"{model}__{shape}.json")
            data = os.path.join(SHAPES, "data", f"{shape}.json")
            prof = _profile_for(run, data)
            _check(f"{model:9s}/{shape:8s} I", prof.I_nats, I_pub)
            _check(f"{model:9s}/{shape:8s} ΔG", prof.dG_out_of_sample_nats, dG_pub)
            accs.append(acc); Is.append(prof.I_nats); dGs.append(prof.dG_out_of_sample_nats)
        rho = _spearman(accs, Is); slope = _slope(Is, dGs)
        print(f"   {shape:8s}: Spearman(I,acc)={rho:.3f} (paper {want_rho[shape]:.3f}) · "
              f"slope(ΔG~I)={slope:.3f} (paper {want_slope[shape]:.3f})")
        assert abs(rho - want_rho[shape]) < 0.01, (shape, rho)
        assert abs(slope - want_slope[shape]) < 0.01, (shape, slope)


def main():
    print("=" * 70)
    print("VALUE-METER SELF-TEST — reproduce the published paper numbers from cache")
    print("=" * 70)
    test_v2_classification()
    test_shapes()
    print("\n" + "=" * 70)
    print("ALL CHECKS PASS — the value-meter reproduces the paper's I, ΔG, ρ, slope.")
    print("=" * 70)


if __name__ == "__main__":
    main()

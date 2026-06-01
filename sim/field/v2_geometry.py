"""
v2_geometry.py — a FOUNDATIONS CHECK for the field theory of value (docs/08),
using real data: the 30 v2 caches (10 models x 3 domains, 240 items each).

The field theory (doc 08) models a population of agents as an order-parameter field:
goals/competences that ALIGN, with a collective direction (the flocking order
parameter). This script asks one honest, limited question of REAL agents:

    Does a real agent population sit in the field theory's *ordered* (aligned)
    phase — i.e. is there a dominant shared "competence axis" (one big principal
    component, strong positive cross-agent correlation), far above what
    independent agents at the same accuracies would show?

HONEST SCOPE (read this):
  * This is a STATIC geometry check of the field theory's ORDER-PARAMETER
    ASSUMPTION on real agents. It is NOT a test of the wave dynamics (doc 08 §3)
    or the phase transition (§5) — those need agents whose goals EVOLVE over time,
    which v2 does not have. Suggestive of foundations, not decisive.
  * "Alignment" here = cross-agent agreement structure on which items each model
    gets right (a shared difficulty/competence axis), the empirical stand-in for
    the doc-08 goal-director order parameter.

Run:  python3 sim/field/v2_geometry.py   (reads sim/real/v2/results/raw/*.json)
"""
from __future__ import annotations
import json, glob, os
import numpy as np

RAW = os.path.join(os.path.dirname(__file__), "..", "real", "v2", "results", "raw")
DOMAINS = ["intent", "mcqa", "topic"]
rng = np.random.default_rng(0)


def load_correctness(domain):
    """Return (model_names, C) where C[a,i] = 1 if model a got item i right."""
    files = sorted(glob.glob(os.path.join(RAW, f"*__{domain}.json")))
    names, rows = [], []
    for f in files:
        d = json.load(open(f))
        idx = sorted(d.keys(), key=int)
        correct = [1.0 if d[i].get("pred") == d[i].get("gold") else 0.0 for i in idx]
        names.append(os.path.basename(f).split("__")[0])
        rows.append(correct)
    return names, np.array(rows)            # (n_models, n_items)


def order_metrics(C):
    """Mean off-diagonal cross-agent correlation, and top-eigenvalue fraction
    (λ1/Σλ) of the agent covariance — both order-parameter proxies."""
    A = C.shape[0]
    var = C.var(axis=1)
    ok = var > 1e-9                          # drop agents with no variance (all right/wrong)
    Cv = C[ok]
    R = np.corrcoef(Cv)
    off = R[np.triu_indices_from(R, k=1)]
    mean_corr = float(np.nanmean(off))
    cov = np.cov(Cv)                         # agents as variables
    eig = np.linalg.eigvalsh(cov)
    eig = eig[eig > 0][::-1]
    top_frac = float(eig[0] / eig.sum()) if len(eig) else float("nan")
    return mean_corr, top_frac, int(ok.sum())


def independence_null(C, reps=400):
    """Null: each agent independently correct at its own accuracy (permute each
    agent's items separately -> destroys cross-agent structure, keeps accuracy)."""
    mc, tf = [], []
    for _ in range(reps):
        Cn = np.array([rng.permutation(row) for row in C])
        m, t, _ = order_metrics(Cn)
        mc.append(m); tf.append(t)
    return np.array(mc), np.array(tf)


def main():
    print("=" * 74)
    print("v2_geometry — does a REAL agent population sit in the field theory's")
    print("ordered (aligned) phase?  (foundations check, doc 08 — static, not dynamics)")
    print("=" * 74)
    rows = []
    for dom in DOMAINS:
        names, C = load_correctness(dom)
        mean_corr, top_frac, n_eff = order_metrics(C)
        null_mc, null_tf = independence_null(C)
        # how far above the independence null (one-sided percentile / z)
        z_corr = (mean_corr - null_mc.mean()) / (null_mc.std() + 1e-9)
        z_tf = (top_frac - null_tf.mean()) / (null_tf.std() + 1e-9)
        rows.append((dom, len(names), n_eff, mean_corr, null_mc.mean(),
                     top_frac, null_tf.mean(), z_corr, z_tf))
        print(f"\n[{dom}]  {len(names)} models, {C.shape[1]} items "
              f"(accuracy spread {C.mean(1).min():.2f}-{C.mean(1).max():.2f})")
        print(f"  mean cross-agent correlation : {mean_corr:+.3f}   "
              f"(independent null {null_mc.mean():+.3f} ± {null_mc.std():.3f};  z={z_corr:+.1f})")
        print(f"  top-eigenvalue fraction λ1/Σλ: {top_frac:.3f}   "
              f"(independent null {null_tf.mean():.3f} ± {null_tf.std():.3f};  z={z_tf:+.1f})")

    # verdict
    aligned = all(r[7] > 3 and r[5] > 1.8 * r[6] for r in rows)   # z>3 AND λ1 well above null
    print("\n" + "=" * 74)
    print("FOUNDATIONS-CHECK READING (honest, limited):")
    if aligned:
        print("  • Across all 3 domains the population is strongly ORDERED: a dominant shared")
        print("    competence axis (λ1 fraction far above the independence null) and strong")
        print("    positive cross-agent correlation (z ≫ 3). Real agents DO have the")
        print("    low-dimensional alignment geometry the field theory's order parameter assumes.")
        print("  • This also explains v1/v2 R5 (no Shannon's demon): a positively-aligned")
        print("    population is deep in the constructive-interference regime, so pooling/pricing")
        print("    has little anti-correlated diversity to harvest. The static geometry predicts")
        print("    the dynamic result.")
    else:
        print("  • The ordered-phase signature is NOT uniform across domains — the field")
        print("    theory's order-parameter assumption is only partially supported here.")
    print("\n  SCOPE: static order-parameter geometry only. NOT a test of the wave dynamics")
    print("  (§3) or the phase transition (§5) — those need evolving goals v2 lacks. Suggestive")
    print("  of the foundations, not validation of the field theory.")
    print("=" * 74)


if __name__ == "__main__":
    main()

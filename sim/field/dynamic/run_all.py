"""
run_all.py — run both Thrust-B dynamic-economy experiments and report a combined
verdict. See README.md for honest scope.

Run:  python3 sim/field/dynamic/run_all.py
"""
from __future__ import annotations
import wave_experiment
import flocking_experiment


def main():
    wave_ok = wave_experiment.main()
    flock_ok = flocking_experiment.main()
    print("\n" + "#" * 76)
    print("THRUST B COMBINED VERDICT (emergent dynamics of a toy value economy)")
    print(f"  demand-wave / dispersion crossover (doc 08 §3): {'PASS' if wave_ok else 'FAIL'}")
    print(f"  collective-goal flocking transition (doc 08 §5–6): {'PASS' if flock_ok else 'FAIL'}")
    print("#" * 76)
    return wave_ok and flock_ok


if __name__ == "__main__":
    raise SystemExit(0 if main() else 1)

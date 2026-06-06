#!/usr/bin/env bash
# build.sh — assemble the value-meter web demo's static assets.
#
# The page runs the REAL value_meter.py in-browser via Pyodide, so there is no
# reimplementation: this script copies the actual Python source into public/py/
# (single source of truth — re-run on every deploy) and generates small, real
# example record sets from the cached harness runs so the live demo reproduces
# the paper's published numbers.
#
# Run from anywhere:  tools/value-meter/web/build.sh
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
PUB="$HERE/public"

echo "==> copy real Python source -> public/py/ (single source of truth)"
cp "$REPO/sim/value_sim.py"              "$PUB/py/value_sim.py"
cp "$REPO/tools/value-meter/value_meter.py" "$PUB/py/value_meter.py"

echo "==> generate real example record sets from the cached runs"
python3 "$HERE/gen_examples.py" "$REPO" "$PUB/examples"

echo "==> done. Serve locally with:  (cd $PUB && python3 -m http.server 8080)"

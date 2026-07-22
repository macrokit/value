#!/usr/bin/env bash
# Build the Stage 2 standalone paper. Requires `tectonic` (self-contained LaTeX).
#
#   ./build.sh            # anonymous TMLR review build -> main.pdf   (default)
#   ./build.sh anon       # same as above
#   ./build.sh preprint   # de-anonymized preprint      -> main-preprint.pdf
#   ./build.sh both       # both
#
# The two builds share ONE source (main.tex); the mode is a single toggle
# (\anontrue near the top). The preprint build is produced by flipping that
# one line into a generated main-preprint.tex, so the two can never drift.
set -euo pipefail
cd "$(dirname "$0")"

build_anon() {
  tectonic main.tex
  echo "-> main.pdf (anonymous, double-blind review build)"
}
build_preprint() {
  sed 's/^\\anontrue/\\anonfalse/' main.tex > main-preprint.tex
  tectonic main-preprint.tex
  echo "-> main-preprint.pdf (de-anonymized preprint)"
}

case "${1:-anon}" in
  anon)     build_anon ;;
  preprint) build_preprint ;;
  both)     build_anon; build_preprint ;;
  *) echo "usage: $0 [anon|preprint|both]" >&2; exit 1 ;;
esac

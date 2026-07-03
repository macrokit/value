#!/usr/bin/env bash
# Build the ANONYMIZED supplementary ZIP for TMLR (OpenReview, <=100MB).
# Packages a tracked-only snapshot of sim/stage2 (pre-registrations, amendments,
# runners, analyzer, raw results, and the per-call SQLite cache), with the
# "Author byline: Cheng Qian." header lines stripped to "Anonymous". Hard-fails
# if any identifying string survives. Regenerate anytime; output is git-ignored.
#
#   ./make-supplement.sh
#
# Output: paper-stage2/stage2-supplement-anon.zip
set -euo pipefail
cd "$(dirname "$0")/.."                      # repo root
STAGE="$(mktemp -d)"
OUT="paper-stage2/stage2-supplement-anon.zip"
# Identity vectors actually present in sim/stage2 (author byline + repo org), plus
# a generic address-shaped catch-all so no private email can slip in un-named.
DENY='Cheng Qian|macrokit'
EMAIL='[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}'

# 1. tracked-only snapshot (no .git, no untracked junk, no .DS_Store)
git archive HEAD sim/stage2 | tar -x -C "$STAGE"

# 2. anonymize the byline header in every text file
find "$STAGE/sim/stage2" -type f \( -name '*.md' -o -name '*.py' -o -name '*.sh' \) \
  -exec perl -0pi -e 's/Cheng Qian/Anonymous/g' {} +

# 3. drop a top-level README pointing reviewers at the reproduction command
cat > "$STAGE/sim/stage2/README-SUPPLEMENT.txt" <<'TXT'
Anonymized supplementary material for the TMLR submission
"Information Limits and Attractor Dynamics in Economies of Frontier LLM Agents".

Contents (self-contained; no external identity):
  PREREGISTRATION*.md   frozen pre-registrations + amendments 1-3
  gate.py stage2a.py stage2b.py   experiment runners
  analyze_stage2.py     the mechanical frozen-band analyzer
  api_client.py mock_backend.py   cached provider backend + mock backend
  results/*.json        raw outputs + the frozen analysis of record
  results/gate_cache.sqlite   the per-call cache (every model response, auditable)

Reproduce every number in the paper offline, deterministically, at zero cost:
  python3 sim/stage2/analyze_stage2.py

The commit-chain hashes cited in the paper are file-level references; their
temporal ordering is verifiable in the version-controlled repository, linked
upon de-anonymization.
TXT

# 4. verify NO identifying string survives (text files + binary cache)
if grep -rIlE "$DENY" "$STAGE/sim/stage2" 2>/dev/null; then
  echo "REFUSING: identifying string survived in a text file (above)." >&2; exit 1
fi
if grep -rIlE "$EMAIL" "$STAGE/sim/stage2" 2>/dev/null; then
  echo "REFUSING: an email address survived in a text file (above)." >&2; exit 1
fi
if strings "$STAGE/sim/stage2/results/gate_cache.sqlite" 2>/dev/null | grep -qiE "$DENY|$EMAIL"; then
  echo "REFUSING: identifying string or email in the cache." >&2; exit 1
fi

# 5. zip (stored paths rooted at sim/stage2/)
rm -f "$OUT"
( cd "$STAGE" && zip -qr - sim/stage2 ) > "$OUT"
rm -rf "$STAGE"
echo "-> $OUT ($(du -h "$OUT" | cut -f1)); anonymization verified."

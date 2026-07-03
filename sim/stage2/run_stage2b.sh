#!/bin/zsh
# run_stage2b.sh — supervisor for the 2B grid: relaunches the restart-safe runner
# on silent death. Operational only; no design change.
cd "$(dirname "$0")/../.."
source .env.stage2
attempt=0
while true; do
  python3 sim/stage2/stage2b.py && break
  code=$?
  if [ $code -eq 2 ]; then
    echo "[supervisor] BUDGET STOP (exit 2) — stopping per prereg ($(date))"
    exit 2
  fi
  attempt=$((attempt+1))
  if [ $attempt -ge 30 ]; then
    echo "[supervisor] giving up after $attempt attempts ($(date))"
    exit 1
  fi
  echo "[supervisor] runner exited $code — retry $attempt in 45s ($(date))"
  sleep 45
done
echo "[supervisor] STAGE-2B COMPLETE ($(date))"

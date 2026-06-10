#!/bin/zsh
# run_stage1.sh — supervisor for the Stage-1 run: auto-heals the ssh tunnel and
# relaunches the (restart-safe) runner on crash. Operational only; no design change.
cd "$(dirname "$0")"
attempt=0
while true; do
  # ensure tunnel
  if ! curl -s -m 5 http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "[supervisor] tunnel down — re-establishing ($(date))"
    pkill -f "ssh.*11434:localhost:11434" 2>/dev/null
    sleep 2
    ssh -o ConnectTimeout=10 -o BatchMode=yes -o ExitOnForwardFailure=yes \
        -o ServerAliveInterval=30 -o ServerAliveCountMax=4 \
        -f -N -L 11434:localhost:11434 blueidea@MacBook-Pro.local
    sleep 3
    # ensure remote ollama is up
    if ! curl -s -m 5 http://localhost:11434/api/tags >/dev/null 2>&1; then
      ssh -o ConnectTimeout=10 -o BatchMode=yes blueidea@MacBook-Pro.local \
        'pgrep -f "ollama serve" >/dev/null || (OLLAMA_NUM_PARALLEL=8 OLLAMA_KEEP_ALIVE=-1 nohup /opt/homebrew/bin/ollama serve > /tmp/ollama.log 2>&1 &); sleep 3'
      sleep 2
    fi
  fi
  python3 lever1_stage1.py && break
  attempt=$((attempt+1))
  if [ $attempt -ge 40 ]; then
    echo "[supervisor] giving up after $attempt attempts ($(date))"
    exit 1
  fi
  echo "[supervisor] runner exited nonzero — retry $attempt in 60s ($(date))"
  sleep 60
done
echo "[supervisor] STAGE-1 RUN COMPLETE ($(date))"

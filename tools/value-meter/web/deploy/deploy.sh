#!/usr/bin/env bash
# Deploy value.macrokit.dev — the value project + Agent Value-Meter live demo.
#
# A STATIC, client-only site: the page runs the real value_meter.py in-browser
# via Pyodide, so there is no app server and no secrets on the box. Mirrors
# studio/deploy/deploy.sh. Steps: (re)build the static assets (copy the real
# Python source + regenerate the example record sets), rsync public/, install
# the nginx vhost, reload nginx.
#
# Override connection via env: MACROKIT_SSH_KEY, MACROKIT_SSH_HOST.
#
# PREREQUISITES (one-time, owner):
#   1. DNS: an A record  value.macrokit.dev -> 3.95.41.84
#   2. TLS: on the box,  sudo certbot --nginx -d value.macrokit.dev
#      (run after the vhost is first installed, or use the HTTP-01 challenge path).

set -euo pipefail

SSH_KEY="${MACROKIT_SSH_KEY:-/Users/jameswalstonn/Desktop/servers/us/helpswap.pem}"
SSH_HOST="${MACROKIT_SSH_HOST:-ubuntu@3.95.41.84}"
REMOTE_ROOT="${MACROKIT_REMOTE_ROOT:-/macrokit/value-site}"
HERE="$(cd "$(dirname "$0")/.." && pwd)"          # .../tools/value-meter/web

if [[ ! -f "$SSH_KEY" ]]; then
  echo "SSH key not found at $SSH_KEY" >&2; exit 1
fi

echo "==> (re)build static assets (copy real Python source + regen examples)"
bash "$HERE/build.sh"

echo "==> ensure remote root exists"
ssh -i "$SSH_KEY" -o ServerAliveInterval=30 "$SSH_HOST" \
  "sudo mkdir -p $REMOTE_ROOT/public $REMOTE_ROOT/deploy/nginx && sudo chown -R \$USER $REMOTE_ROOT"

echo "==> rsync public/ -> $SSH_HOST:$REMOTE_ROOT/public/"
rsync -avz --delete \
  -e "ssh -i $SSH_KEY -o ServerAliveInterval=30" \
  "$HERE/public/" "$SSH_HOST:$REMOTE_ROOT/public/"

echo "==> rsync nginx vhost"
rsync -avz \
  -e "ssh -i $SSH_KEY -o ServerAliveInterval=30" \
  "$HERE/deploy/nginx/" "$SSH_HOST:$REMOTE_ROOT/deploy/nginx/"

echo "==> install vhost + reload nginx"
ssh -i "$SSH_KEY" -o ServerAliveInterval=30 "$SSH_HOST" bash <<'REMOTE'
set -euo pipefail
sudo ln -sf /macrokit/value-site/deploy/nginx/value.macrokit.dev.conf /etc/nginx/sites-available/value.macrokit.dev
sudo ln -sf /etc/nginx/sites-available/value.macrokit.dev /etc/nginx/sites-enabled/value.macrokit.dev
sudo nginx -t
sudo systemctl reload nginx
REMOTE

echo "==> done -> https://value.macrokit.dev"

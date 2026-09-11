#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MODEL="${MODEL:-}"
CONTEXT="${CONTEXT:-4096}"
PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
THREADS="${THREADS:-}"
LLAMA_DIR="${LLAMA_DIR:-$HOME/llama.cpp}"

if [ -z "$MODEL" ]; then
  echo "ERROR: MODEL is required."
  exit 1
fi

if [ ! -f "$MODEL" ]; then
  echo "ERROR: model not found: $MODEL"
  exit 1
fi

SERVER="$LLAMA_DIR/build/bin/llama-server"
if [ ! -x "$SERVER" ]; then
  echo "ERROR: llama-server not found. Build llama.cpp first."
  exit 1
fi

ARGS=(-m "$MODEL" -c "$CONTEXT" --host "$HOST" --port "$PORT")
if [ -n "$THREADS" ]; then
  ARGS+=(-t "$THREADS")
fi

echo "=== ORBI Edge Mesh — Local llama-server ==="
echo "WARNING: Phase 0 is LAN-only. Do not expose this port to the public Internet."
echo "Host: $HOST"
echo "Port: $PORT"
echo "Model: $MODEL"
echo
echo "Local addresses:"
ip -br addr 2>/dev/null || ip addr || true
echo

exec "$SERVER" "${ARGS[@]}"

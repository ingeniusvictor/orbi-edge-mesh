#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MODEL="${MODEL:-}"
CONTEXT="${CONTEXT:-4096}"
THREADS="${THREADS:-}"
PROMPT="${PROMPT:-Responde en una sola frase: ¿qué es ORBI Edge Mesh?}"
LLAMA_DIR="${LLAMA_DIR:-$HOME/llama.cpp}"

if [ -z "$MODEL" ]; then
  echo "ERROR: MODEL is required."
  echo "Example:"
  echo "  MODEL=~/models/model.gguf ./run_smoke_test.sh"
  exit 1
fi

if [ ! -f "$MODEL" ]; then
  echo "ERROR: model not found: $MODEL"
  exit 1
fi

CLI="$LLAMA_DIR/build/bin/llama-cli"
if [ ! -x "$CLI" ]; then
  echo "ERROR: llama-cli not found. Build llama.cpp first."
  exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
LOG_DIR="$HOME/orbi-edge-runs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/smoke-$STAMP.log"

ARGS=(-m "$MODEL" -c "$CONTEXT" -p "$PROMPT")
if [ -n "$THREADS" ]; then
  ARGS+=(-t "$THREADS")
fi

echo "=== ORBI Edge Mesh — Smoke Test ===" | tee "$LOG"
echo "Model: $MODEL" | tee -a "$LOG"
echo "Context: $CONTEXT" | tee -a "$LOG"
echo "Threads: ${THREADS:-auto}" | tee -a "$LOG"
echo "llama.cpp commit: $(cd "$LLAMA_DIR" && git rev-parse HEAD)" | tee -a "$LOG"
echo "Started: $(date -Iseconds 2>/dev/null || date)" | tee -a "$LOG"
echo | tee -a "$LOG"

"$CLI" "${ARGS[@]}" 2>&1 | tee -a "$LOG"

echo | tee -a "$LOG"
echo "Finished: $(date -Iseconds 2>/dev/null || date)" | tee -a "$LOG"
echo "Log: $LOG"

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
MODEL="${MODEL:-$HOME/models/Qwen3-1.7B-Q4_K_M.gguf}"
THREADS="${THREADS:-4}"
CONTEXT="${CONTEXT:-4096}"
PROMPT="${PROMPT:-Responde en español y en una sola frase: ¿qué es una red local de inteligencia artificial?}"

if [[ ! -f "$MODEL" ]]; then
  echo "ERROR: model not found: $MODEL" >&2
  echo "Run scripts/android/download_node01_phase0_model.sh first." >&2
  exit 2
fi

MODEL="$MODEL" THREADS="$THREADS" CONTEXT="$CONTEXT" PROMPT="$PROMPT" \
  bash "$ROOT_DIR/scripts/android/run_smoke_test.sh"

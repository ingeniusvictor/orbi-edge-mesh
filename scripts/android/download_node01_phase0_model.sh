#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

MODEL_DIR="${MODEL_DIR:-$HOME/models}"
MODEL_FILE="${MODEL_FILE:-Qwen3-1.7B-Q4_K_M.gguf}"
MODEL_URL="${MODEL_URL:-https://huggingface.co/ggml-org/Qwen3-1.7B-GGUF/resolve/main/Qwen3-1.7B-Q4_K_M.gguf?download=true}"
OUT="$MODEL_DIR/$MODEL_FILE"

mkdir -p "$MODEL_DIR"

echo "=== ORBI Edge Mesh — Node-01 Phase 0 model ==="
echo "Target: $OUT"
echo "Source: ggml-org/Qwen3-1.7B-GGUF / Q4_K_M"
echo

if [[ -f "$OUT" ]]; then
  echo "Model already exists:"
  ls -lh "$OUT"
  echo "Delete or rename it manually if a clean re-download is required."
  exit 0
fi

echo "Checking available storage..."
df -h "$MODEL_DIR" || true
echo

echo "Downloading with resume support..."
curl -L --fail --retry 3 --retry-delay 3 --continue-at - \
  --output "$OUT.part" "$MODEL_URL"

mv "$OUT.part" "$OUT"

echo
echo "Download complete."
ls -lh "$OUT"

if command -v sha256sum >/dev/null 2>&1; then
  echo "Local SHA-256:"
  sha256sum "$OUT"
fi

echo
echo "Model path:"
echo "$OUT"

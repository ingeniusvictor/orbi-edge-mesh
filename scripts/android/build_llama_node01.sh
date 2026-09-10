#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

LLAMA_DIR="${LLAMA_DIR:-$HOME/llama.cpp}"
JOBS="${JOBS:-2}"

if [ ! -d "$LLAMA_DIR/.git" ]; then
  echo "ERROR: llama.cpp repository not found at $LLAMA_DIR"
  exit 1
fi

cd "$LLAMA_DIR"

echo "=== ORBI Edge Mesh — llama.cpp Build ==="
echo "Directory: $LLAMA_DIR"
echo "Jobs: $JOBS"
echo "Commit: $(git rev-parse HEAD)"

cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j"$JOBS"

echo
echo "=== Produced binaries ==="
ls -lh build/bin/llama-cli build/bin/llama-server 2>/dev/null || true

echo
echo "=== Version checks ==="
./build/bin/llama-cli --version || true
./build/bin/llama-server --version || true

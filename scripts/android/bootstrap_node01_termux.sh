#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "=== ORBI Edge Mesh — Node-01 Bootstrap ==="
echo "This script is intended for Termux on Android."
echo "No root is required."

if ! command -v pkg >/dev/null 2>&1; then
  echo "ERROR: pkg not found. Run this inside Termux."
  exit 1
fi

echo
echo "[1/6] Updating Termux packages..."
pkg update -y
pkg upgrade -y

echo
echo "[2/6] Installing build/runtime dependencies..."
pkg install -y git cmake clang make python curl wget libandroid-spawn

echo
echo "[3/6] Preparing directories..."
mkdir -p "$HOME/models"
mkdir -p "$HOME/orbi-edge-baselines"
mkdir -p "$HOME/orbi-edge-runs"

echo
echo "[4/6] Capturing quick device identity..."
{
  echo "manufacturer=$(getprop ro.product.manufacturer 2>/dev/null || true)"
  echo "model=$(getprop ro.product.model 2>/dev/null || true)"
  echo "device=$(getprop ro.product.device 2>/dev/null || true)"
  echo "android=$(getprop ro.build.version.release 2>/dev/null || true)"
  echo "sdk=$(getprop ro.build.version.sdk 2>/dev/null || true)"
  echo "abi=$(getprop ro.product.cpu.abi 2>/dev/null || true)"
  echo "hardware=$(getprop ro.hardware 2>/dev/null || true)"
} | tee "$HOME/orbi-edge-runs/node01-identity.txt"

echo
echo "[5/6] Cloning/updating llama.cpp..."
if [ -d "$HOME/llama.cpp/.git" ]; then
  cd "$HOME/llama.cpp"
  git fetch --all --tags
  git status --short
  echo "Existing llama.cpp checkout preserved. No automatic reset performed."
else
  git clone https://github.com/ggml-org/llama.cpp.git "$HOME/llama.cpp"
fi

cd "$HOME/llama.cpp"
git rev-parse HEAD | tee "$HOME/orbi-edge-runs/llama-cpp-commit.txt"

echo
echo "[6/6] Bootstrap complete."
echo
echo "Next:"
echo "  1) capture full baseline"
echo "  2) build llama.cpp"
echo "  3) place a small GGUF model in ~/models"
echo "  4) run smoke test"

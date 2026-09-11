#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT_DIR="$HOME/orbi-edge-evidence/node01-$STAMP"

mkdir -p "$OUT_DIR"

copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [[ -e "$src" ]]; then
    cp -R "$src" "$dst"
  fi
}

echo "Collecting Node-01 evidence into $OUT_DIR"

copy_if_exists "$HOME/orbi-edge-baselines" "$OUT_DIR/baselines"
copy_if_exists "$HOME/orbi-edge-runs" "$OUT_DIR/runs"
copy_if_exists "$HOME/orbi-edge-watchdog" "$OUT_DIR/watchdog"

{
  echo "timestamp=$(date -Iseconds)"
  echo "repo=$ROOT_DIR"
  echo "branch=$(git -C "$ROOT_DIR" branch --show-current 2>/dev/null || true)"
  echo "repo_commit=$(git -C "$ROOT_DIR" rev-parse HEAD 2>/dev/null || true)"
  echo "llama_commit=$(git -C "$HOME/llama.cpp" rev-parse HEAD 2>/dev/null || true)"
  echo "model_files:"
  find "$HOME/models" -maxdepth 1 -type f -printf '%f %s bytes\n' 2>/dev/null || true
} > "$OUT_DIR/manifest.txt"

if command -v termux-info >/dev/null 2>&1; then
  termux-info > "$OUT_DIR/termux-info.txt" 2>&1 || true
fi

dumpsys battery > "$OUT_DIR/battery.txt" 2>&1 || true
cat /proc/meminfo > "$OUT_DIR/meminfo.txt" 2>&1 || true
df -h > "$OUT_DIR/storage.txt" 2>&1 || true

echo
echo "Evidence package prepared locally:"
echo "$OUT_DIR"
echo
echo "Review it before sharing or committing anything."

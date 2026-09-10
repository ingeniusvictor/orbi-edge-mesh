#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"

echo "=== ORBI Edge Mesh — Node-01 Headless Start ==="

if command -v termux-wake-lock >/dev/null 2>&1; then
  echo "[1/3] Acquiring Termux wake lock..."
  termux-wake-lock
else
  echo "WARNING: termux-wake-lock not available."
  echo "The node may suspend when the screen turns off."
fi

echo "[2/3] Starting local AI server..."
echo "Display may now be turned off after server startup."
echo "Use stop_headless_node01.sh to release the wake lock."
echo

echo "[3/3] Delegating to start_local_server.sh..."
exec bash "$ROOT_DIR/scripts/android/start_local_server.sh"

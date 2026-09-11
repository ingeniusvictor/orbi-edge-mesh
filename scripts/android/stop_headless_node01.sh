#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "=== ORBI Edge Mesh — Node-01 Headless Stop ==="

if command -v termux-wake-unlock >/dev/null 2>&1; then
  termux-wake-unlock
  echo "Wake lock released."
else
  echo "termux-wake-unlock not available."
fi

echo "If llama-server is still running, stop that process separately."

#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
STATE_DIR="${STATE_DIR:-$HOME/orbi-edge-watchdog}"
RESTART_FILE="$STATE_DIR/restart_count"
mkdir -p "$STATE_DIR"
printf '0\n' > "$RESTART_FILE"
echo "ORBI Node watchdog restart budget reset to 0."

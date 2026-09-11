#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

CHECK_INTERVAL="${CHECK_INTERVAL:-30}"
MAX_RESTARTS="${MAX_RESTARTS:-3}"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8080}"
STATE_DIR="${STATE_DIR:-$HOME/orbi-edge-watchdog}"
LOG_FILE="$STATE_DIR/watchdog.log"
RESTART_FILE="$STATE_DIR/restart_count"

mkdir -p "$STATE_DIR"
touch "$LOG_FILE"

log() {
  printf '%s %s\n' "$(date -Iseconds)" "$*" | tee -a "$LOG_FILE"
}

restart_count=0
if [[ -f "$RESTART_FILE" ]]; then
  restart_count="$(cat "$RESTART_FILE" 2>/dev/null || echo 0)"
fi

is_process_alive() { pgrep -f "llama-server" >/dev/null 2>&1; }
is_api_reachable() { curl --silent --fail --max-time 5 "http://$HOST:$PORT/v1/models" >/dev/null 2>&1; }

policy_allows_restart() {
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  if python "$SCRIPT_DIR/check_recovery_policy.py" >>"$LOG_FILE" 2>&1; then
    log "[POLICY PASS] recovery authorized"
    return 0
  fi
  log "[POLICY BLOCK] recovery denied by thermal/power policy"
  return 1
}

restart_service() {
  if ! policy_allows_restart; then
    log "[HOLD] service remains down until policy allows recovery"
    return 2
  fi
  if (( restart_count >= MAX_RESTARTS )); then
    log "[QUARANTINE] restart budget exhausted: $restart_count/$MAX_RESTARTS"
    return 1
  fi
  restart_count=$((restart_count + 1))
  printf '%s\n' "$restart_count" > "$RESTART_FILE"
  log "[RESTART] attempt $restart_count/$MAX_RESTARTS"
  pkill -f "llama-server" >/dev/null 2>&1 || true
  sleep 2
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  nohup bash "$SCRIPT_DIR/start_headless_node01.sh" >>"$STATE_DIR/server.log" 2>&1 &
  sleep 10
  if is_api_reachable; then
    log "[RECOVERY PASS] API reachable after restart"
    return 0
  fi
  log "[RECOVERY FAIL] API still unreachable"
  return 1
}

log "[WATCHDOG START] interval=${CHECK_INTERVAL}s max_restarts=$MAX_RESTARTS"
while true; do
  if is_process_alive && is_api_reachable; then
    log "[HEALTHY] process=up api=up"
  elif is_process_alive; then
    log "[FAULT] process=up api=down"
    restart_service || true
  else
    log "[FAULT] process=down api=down"
    restart_service || true
  fi
  if (( restart_count >= MAX_RESTARTS )); then
    log "[WATCHDOG STOP] automatic restart budget exhausted"
    exit 2
  fi
  sleep "$CHECK_INTERVAL"
done

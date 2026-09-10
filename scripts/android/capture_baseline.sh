#!/data/data/com.termux/files/usr/bin/bash
set -u

OUT_DIR="${1:-$HOME/orbi-edge-baselines}"
mkdir -p "$OUT_DIR"
STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="$OUT_DIR/node-baseline-$STAMP.txt"

section() {
  printf "\n===== %s =====\n" "$1" >> "$OUT"
}

safe() {
  "$@" >> "$OUT" 2>&1 || true
}

printf "ORBI Edge Mesh — Android Node Baseline\n" > "$OUT"
printf "Captured: %s\n" "$(date -Iseconds 2>/dev/null || date)" >> "$OUT"

section "Identity"
safe getprop ro.product.manufacturer
safe getprop ro.product.model
safe getprop ro.product.device
safe getprop ro.build.version.release
safe getprop ro.build.version.sdk
safe getprop ro.product.cpu.abi
safe getprop ro.hardware

section "Kernel"
safe uname -a

section "CPU"
safe sh -c 'cat /proc/cpuinfo'

section "Memory"
safe sh -c 'cat /proc/meminfo'
safe free -h

section "Storage"
safe df -h
safe sh -c 'du -sh "$HOME" 2>/dev/null'

section "Battery"
safe dumpsys battery

section "Thermal"
if [ -d /sys/class/thermal ]; then
  safe sh -c 'for z in /sys/class/thermal/thermal_zone*; do [ -d "$z" ] || continue; printf "%s " "$z"; cat "$z/type" 2>/dev/null; cat "$z/temp" 2>/dev/null; done'
else
  printf "Thermal sysfs not visible\n" >> "$OUT"
fi

section "Termux"
safe termux-info

section "Network"
safe ip addr
safe ip route

section "Notes"
printf "Record Android Memory Extension state manually in the benchmark sheet.\n" >> "$OUT"
printf "Do not infer physical RAM from marketing/virtual-memory totals.\n" >> "$OUT"

printf "%s\n" "$OUT"

# ORBI Edge Mesh — Node-01 Bring-Up Runbook

Device: POCO X7 Pro 5G
Role: Primary experimental node
Phase: 0 hardware validation

## Goal

Bring Node-01 from a normal Android phone to a reproducible local ORBI AI node.

## Safety constraints

- no root
- no bootloader changes
- no public port forwarding
- no permanent system modifications
- keep the phone on a trusted LAN
- stop tests if thermal behavior looks abnormal
- do not perform heavy sustained inference while fast charging

## Step 1 — Install and open Termux

Use a current trusted Termux distribution.

Then keep Android battery optimization permissive enough for the test session.

## Step 2 — Clone ORBI Edge Mesh

```bash
pkg update
pkg install git -y
cd ~
git clone https://github.com/ingeniusvictor/orbi-edge-mesh.git
cd orbi-edge-mesh
git checkout feature/phase-0-foundation
```

## Step 3 — Bootstrap Node-01

```bash
bash scripts/android/bootstrap_node01_termux.sh
```

## Step 4 — Capture baseline

```bash
bash scripts/android/capture_baseline.sh
```

Manually record Android Memory Extension state because Android may not expose it reliably through shell APIs.

## Step 5 — Build llama.cpp

```bash
bash scripts/android/build_llama_node01.sh
```

Do not increase build parallelism aggressively on the first run.

## Step 6 — Verify binaries

Expected binaries include:

```text
llama-cli
llama-server
```

## Step 7 — Add first small GGUF model

Use a small 1B–3B Q4-class model for the first smoke test.

Store it under:

```text
~/models/
```

Do not start Phase 0 with a 7B/14B/30B model.

## Step 8 — Offline smoke test

Example:

```bash
MODEL=~/models/<model>.gguf \
THREADS=4 \
CONTEXT=4096 \
bash scripts/android/run_smoke_test.sh
```

Then temporarily disable Internet connectivity while keeping the local test path valid and repeat one inference.

## Step 9 — Start headless server

```bash
MODEL=~/models/<model>.gguf \
THREADS=4 \
CONTEXT=4096 \
PORT=8080 \
bash scripts/android/start_headless_node01.sh
```

## Step 10 — Find Node-01 LAN IP

```bash
ip addr
ip route
```

Record the Wi-Fi IPv4 address.

## Step 11 — PC validation

From the PC repository checkout:

```bash
python scripts/pc/test_llama_server.py --host <POCO_IP>
```

PASS requires `/v1/models` and `/v1/chat/completions` to respond.

## Step 12 — Screen-off certification

Start the PC probe:

```bash
python scripts/pc/headless_probe.py --host <POCO_IP>
```

Then turn the POCO display off and leave it off for the full test.

## Step 13 — Watchdog recovery

Only after the normal headless test passes:

```bash
bash scripts/android/reset_watchdog_budget.sh
bash scripts/android/watchdog_node01.sh
```

Use the dedicated recovery experiment before enabling any unattended watchdog behavior.

## Step 14 — Collect evidence

Run:

```bash
bash scripts/android/package_node01_evidence.sh
```

Do not commit raw evidence logs automatically.

## Exit

Node-01 Phase 0 hardware validation is materially complete when the Phase 0 exit checklist is satisfied.

# Node-01 — Exact Execution Sequence

This is the shortest supported path from a clean Termux install to the first ORBI Edge Mesh local inference.

## Step 1 — Get the ORBI scripts onto the phone

Preferred developer path:

```bash
cd ~
git clone https://github.com/ingeniusvictor/orbi-edge-mesh.git
cd orbi-edge-mesh
git checkout feature/phase-0-foundation
```

If the repository becomes private later, authenticate using a safe GitHub method supported by the user. Do not store credentials in scripts.

## Step 2 — Bootstrap Termux

```bash
cd ~/orbi-edge-mesh
bash scripts/android/bootstrap_node01_termux.sh
```

Expected:
- package installation succeeds;
- ~/models exists;
- ~/llama.cpp exists;
- exact llama.cpp commit SHA is written to ~/orbi-edge-runs/llama-cpp-commit.txt.

## Step 3 — Capture full baseline

```bash
bash scripts/android/capture_baseline.sh
```

Preserve the output path printed by the script.

Also record manually:
- Xiaomi Memory Extension enabled/disabled;
- configured virtual-memory amount.

## Step 4 — Build llama.cpp

```bash
bash scripts/android/build_llama_node01.sh
```

Default build parallelism is deliberately conservative at 2 jobs.

Expected:
- build/bin/llama-cli
- build/bin/llama-server

## Step 5 — Place first model

Put one small GGUF model under:

```text
~/models/
```

Phase 0 first-model policy:
- ~1B–3B parameter class
- Q4-class quantization preferred
- known chat/instruct model
- no 30B/35B testing yet

Before running:

```bash
ls -lh ~/models
```

Record exact filename and size.

## Step 6 — First smoke test

```bash
cd ~/orbi-edge-mesh
MODEL="$HOME/models/<exact-file>.gguf" \
bash scripts/android/run_smoke_test.sh
```

The generated log will be stored under:

```text
~/orbi-edge-runs/
```

## Step 7 — Offline verification

After the model has been downloaded/copied and the runtime built:
- disable mobile data;
- disable external Internet access if practical while keeping local Wi-Fi if needed;
- repeat the smoke test.

The inference result should not require cloud access.

## Step 8 — Start LAN server

```bash
MODEL="$HOME/models/<exact-file>.gguf" \
bash scripts/android/start_local_server.sh
```

Phase 0 rule:
- trusted LAN only;
- no router port forwarding;
- no public exposure.

## Step 9 — PC connectivity test

Find the phone's Wi-Fi IPv4 address from the server output or Android Wi-Fi settings.

Then from the PC test the local endpoint using the API exposed by the installed llama-server build.

Record:
- phone IP;
- port;
- request latency;
- result;
- whether the request completed fully locally.

## Step 10 — Evidence

For P0-B certification, preserve:
- baseline text file;
- llama.cpp commit SHA;
- build/version output;
- exact model filename;
- smoke-test log;
- screenshots only when useful;
- any thermal anomaly or Android process termination.

Do not merge Phase 0 foundation merely because the scripts exist. The branch is certified only after real Node-01 evidence is collected.

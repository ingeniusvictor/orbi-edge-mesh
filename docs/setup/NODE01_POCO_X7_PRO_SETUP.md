# Node-01 Setup — POCO X7 Pro

## Scope

Prepare the POCO X7 Pro as the first ORBI Edge Node using a fully reversible, non-root path.

## Official Phase 0 runtime path

Primary path: **Termux + llama.cpp CLI/server on Android**.

This follows the current llama.cpp Android guidance, which explicitly documents building the CLI under Termux without root.

## Safety constraints

- Do not unlock the bootloader.
- Do not root the phone.
- Do not flash a custom ROM.
- Do not alter partitions.
- Do not enable permanent high-load background execution yet.
- Do not combine sustained maximum inference load with fast charging during first thermal tests.
- Keep the first model small enough that failure is unlikely to destabilize the phone.

## P0-B1 — Install Termux

Preferred sources:
- official Termux project / F-Droid
- Google Play only if using the currently supported experimental build

After installation, open Termux and run:

```bash
pkg update
pkg upgrade -y
pkg install git cmake clang make python curl wget libandroid-spawn -y
```

Record:

```bash
uname -a
getprop ro.product.manufacturer
getprop ro.product.model
getprop ro.product.device
getprop ro.build.version.release
getprop ro.build.version.sdk
getprop ro.product.cpu.abi
getprop ro.hardware
```

## P0-B2 — Capture baseline

From the repository tooling, run the baseline script or manually capture equivalent fields.

Desired baseline:
- Android version
- ABI
- kernel
- physical memory visible to Termux
- storage available to Termux
- CPU information
- battery state
- battery temperature if exposed
- thermal-zone visibility
- memory-extension state recorded manually from Android settings

The baseline must be captured **before** installing or loading a large model.

## P0-B3 — Clone llama.cpp

```bash
cd ~
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
git rev-parse HEAD
```

The exact commit SHA must be stored in every benchmark record.

## P0-B4 — Build llama.cpp

Start with the standard Termux/CMake path:

```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j2
```

Why `-j2` initially:
- minimizes uncontrolled thermal spikes during first compilation;
- gives us a conservative reproducible baseline;
- can be increased later after thermal behavior is understood.

Verify:

```bash
./build/bin/llama-cli --version
./build/bin/llama-server --version
```

If one executable is not produced, record the result rather than improvising a different build configuration.

## P0-B5 — Storage policy

For first tests, keep model files inside the Termux home directory:

```text
~/models/
```

Create it with:

```bash
mkdir -p ~/models
```

This follows the llama.cpp Android guidance to use the Termux/private filesystem rather than Android shared storage for model execution.

## P0-B6 — First model policy

Do not start with 30B/35B.

Initial class:
- approximately 1B–3B
- GGUF
- Q4-class quantization preferred for the first smoke test

Exact model selection is recorded separately so it can be changed without rewriting this setup procedure.

## P0-B7 — First CLI smoke test

Example shape:

```bash
cd ~/llama.cpp
./build/bin/llama-cli \
  -m ~/models/<model>.gguf \
  -c 4096 \
  -p "Responde en una frase: ¿qué es ORBI Edge Mesh?"
```

Start with context size 4096 unless the selected model requires a smaller safe value.

Pass criteria:
- binary launches;
- model loads;
- prompt returns coherent text;
- no crash;
- model can infer with external internet disabled after the file is already present.

## P0-B8 — First local API

After CLI success:

```bash
./build/bin/llama-server \
  -m ~/models/<model>.gguf \
  -c 4096 \
  --host 0.0.0.0 \
  --port 8080
```

Security rule for Phase 0:
- use only on the trusted local LAN;
- do not expose port 8080 to the public Internet;
- do not configure router port forwarding.

From the PC, verify the server using the POCO's local Wi-Fi address.

## P0-B9 — Exit criteria

P0-B is complete when:
- device baseline is stored;
- llama.cpp commit is recorded;
- CLI builds and launches;
- llama-server builds and launches;
- selected small GGUF model is present;
- first local prompt completes.

P0-C begins only after these conditions are met.

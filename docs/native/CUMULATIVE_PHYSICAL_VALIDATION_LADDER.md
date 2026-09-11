# Cumulative Native Physical Validation Ladder

## Why this ladder exists

The native research branches are cumulative. We do not need to install a different APK for every gate.

A sufficiently recent cumulative APK can validate N0 through N9 sequentially, provided each lower gate is still checked and recorded independently.

This reduces APK churn without weakening certification.

## Rule

Compile success never closes a physical gate.

A later cumulative APK may certify an earlier gate only when the exact acceptance evidence for that earlier gate is observed on Node-01.

## Recommended first physical candidate

Use the newest cumulative Android build whose CI is fully green.

Before installation record:

- branch;
- commit;
- app version;
- APK SHA-256;
- Android version;
- Node-01 battery;
- whether the previous Termux llama-server is stopped.

Termux may remain installed as a diagnostic/reference environment, but it must not provide inference for native certification.

## Gate sequence

### N0 — Android/JNI foundation

Confirm:

- app installs;
- app launches without crash;
- device identity is correct;
- ABI is arm64-v8a;
- `JNI BRIDGE READY` appears.

### N1 — Android-native telemetry

Compare app values with Android UI where practical:

- battery;
- charging;
- RAM class;
- storage;
- Wi-Fi/network;
- Android thermal category if exposed.

Unknown/unavailable values are acceptable only when represented explicitly as UNKNOWN rather than fabricated.

### N2 — llama.cpp native link

Confirm the app displays llama.cpp system information from the JNI call.

This proves the packaged native library is callable on the physical POCO.

### N3 — GGUF import

Select the exact Qwen3 1.7B Q4_K_M GGUF.

Require:

- file import completes;
- SHA-256 MATCH;
- app remains responsive;
- invalid-file path will later be tested safely with a small non-model file.

### N4 — first APK-owned inference

Load Qwen with the reference settings:

- context 4096;
- threads 4.

Run the built-in Spanish prompt.

Require a coherent completion.

Then disable Internet connectivity and repeat.

Native inference must continue without a Termux inference process.

### N5 — local API

Start the local API and confirm from Windows:

- `/health`;
- `/node`;
- `/v1/models`.

After N9 is present in the cumulative build, unsigned chat requests are expected to be rejected. Use the paired signed client for privileged chat inference.

### N6 — screen-off/headless parity

Start the headless service and use the signed native probe.

Formal target:

- 7/7 reachability checks;
- 5-minute interval;
- about 30 minutes total;
- signed real inference at check 5;
- screen off after check 1;
- service remains alive;
- no abnormal thermal behavior.

### N7 — bounded supervisor

With the model desired and the headless service active:

- trigger the controlled model-runtime failure;
- observe supervisor detection;
- observe bounded recovery;
- verify restart count;
- verify inference becomes usable again.

Do not induce repeated failures beyond what is required to verify the 3-attempt bound.

### N8 — resource guard

Verify normal cool/battery-healthy operation reports ALLOW.

Do not intentionally overheat the phone.

BLOCK/DEGRADE edge conditions should be validated primarily by unit/simulation tests plus naturally occurring observations.

### N9 — explicit pairing

Generate a pairing token.

Record the node ID separately.

Validate:

- unsigned chat rejected;
- signed chat accepted;
- replay rejected;
- wrong node ID rejected;
- token rotation/revocation invalidates old credentials.

Do not commit pairing secrets to Git.

## Signed N6 probe

On Windows, after pairing:

```powershell
$env:ORBI_PAIRING_TOKEN="<token shown on Node-01>"

python scripts/pc/native_headless_probe.py `
  --host 192.168.1.7 `
  --node-id "<Node-01 ID>"

Remove-Item Env:\ORBI_PAIRING_TOKEN
```

## N10 and beyond

N10 requires the same native node behavior on all three permanent Android devices and therefore cannot be certified from Node-01 alone.

R1/R2/R3 remain post-N10 research tracks.

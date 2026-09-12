# ORBI Edge Node Native Alpha — Node-01 Validation Runbook

Status: PREPARED — PHYSICAL EXECUTION REQUIRED

## Purpose

Use one consolidated APK to validate the native N0-N9 stack on the POCO X7 Pro without installing a different APK for every gate.

This runbook does not replace individual acceptance criteria. It collects reproducible evidence efficiently.

## Build identity

Expected version: `0.10.0-native-alpha`.

The exact APK SHA-256 must be recorded from CI before installation.

## Before installation

Keep the existing Termux Phase 0 environment intact as a recovery/reference path.

Do not run the Termux llama-server on port 8080 while validating the APK local API, otherwise the results would be ambiguous.

## Stage A — N0/N1/N2 preflight

Install and launch the Native Alpha APK.

Record a screenshot containing build version, POCO identity, Android version, arm64-v8a, `JNI BRIDGE READY`, llama.cpp system information, native telemetry and N8 resource-policy state.

Expected readiness: N0 READY, N1 READY, N2 READY. N3+ may still show WAIT.

## Stage B — N3 model import

Select the existing `Qwen3-1.7B-Q4_K_M.gguf`.

Expected SHA-256:

`d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5`

Expected result: `SHA-256 MATCH`.

The APK copies the model into its own private model directory.

## Stage C — N4 native inference

Press `Load Qwen into native runtime`, then run the in-app inference test.

Record response, approximate latency, battery, Android thermal category and whether the app remained stable.

Termux must not provide inference during this test.

## Stage D — N9 pairing

Generate a pairing token and record the Node ID plus the token privately for the PC test.

Do not place the token in GitHub, public screenshots or evidence JSON.

## Stage E — N5 local API

Start the local API or the headless service.

From Windows:

```powershell
python .\scripts\pc\native_alpha_probe.py --host 192.168.1.7 --mode preflight
```

Use the actual IPv4 displayed by the APK if it has changed.

Expected: `/health`, `/node`, `/diagnostics` and `/v1/models` PASS.

## Stage F — N9 signed API validation

```powershell
$env:ORBI_PAIRING_TOKEN="<private token from the POCO>"

python .\scripts\pc\native_alpha_probe.py `
  --host 192.168.1.7 `
  --node-id "<node id from the POCO>" `
  --mode full

Remove-Item Env:\ORBI_PAIRING_TOKEN
```

The full probe requires unsigned chat -> HTTP 401, signed chat -> HTTP 200, exact replay -> HTTP 401 `replay_detected`, and evidence JSON without the pairing secret.

## Stage G — N6 screen-off headless parity

With model loaded, pairing active, foreground service started and Windows able to reach the APK, repeat the established 30-minute headless protocol:

- 7 reachability checks;
- approximately 5-minute spacing;
- real signed inference after at least 20 minutes;
- display off after the first check;
- no interaction with the phone until completion.

Record battery start/end, Android thermal status, manual physical temperature observation, Android warnings and foreground notification survival.

## Stage H — N7 bounded recovery

Only while N8 policy reports `ALLOW`: keep the headless service active, use `Simulate model runtime failure`, observe supervisor state, require a bounded reload, then run another signed chat request.

Maximum configured automatic attempts: 3.

## Stage I — N8 resource guard

Do not deliberately overheat the phone. Thermal blocking/degrade transitions can be supported by automated tests and natural observations.

## Certification rule

A green build means software preparation.

A physical gate is only PASS after real Node-01 evidence is recorded.

Termux becomes optional for normal ORBI Edge Node operation only after native headless parity is physically demonstrated.

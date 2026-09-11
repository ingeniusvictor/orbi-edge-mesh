# Node-01 Native APK — Physical Install and First-Pass Runbook

This runbook begins only after the cumulative APK candidate is fully green in CI.

## 1. Record the candidate

Before installation, record branch, Git commit, APK SHA-256, signing-certificate digest, app version and current Node-01 battery percentage.

Do not use an APK whose source commit, checksum or signer is unknown.

The cumulative CI workflow preserves a research debug signing key through the GitHub Actions cache. After RC1 is installed, later research APKs intended as in-place upgrades should present the same signing-certificate digest. If the signer changes unexpectedly, stop and investigate instead of uninstalling the working node automatically.

## 2. Preserve the Phase 0 reference

Termux may remain installed because it is still useful for diagnostics.

Before N4 native-inference certification, stop any Termux llama-server or llama-cli inference process so there is no ambiguity about which runtime produced the response.

## 3. Install

Use either Android's package installer or ADB.

For manual installation, grant install-unknown-apps only to the file/browser source used for this test. There is no need to disable Android security globally.

For ADB:

```powershell
adb devices
adb install -r app-debug.apk
```

If Android reports a signing-key mismatch with an earlier research build, uninstall only the ORBI Edge Node research app and install the new candidate again. Do not uninstall Termux or delete the original GGUF.

## 4. First launch — N0/N1/N2

Before importing a model, capture a screenshot showing ORBI Edge Node, app version, source commit, manufacturer/model/device, Android/API level, arm64-v8a, CPU logical processors, JNI BRIDGE READY, llama.cpp system information, and RAM/storage/battery/network/thermal values.

Do not mark a value correct merely because it is present. Compare battery/storage/device identity with Android where practical.

## 5. N3 model import

The proven GGUF currently lives inside Termux private storage, which the Android document picker cannot normally browse directly.

Before the first native import, expose a **copy** in shared Downloads from a second Termux session:

```bash
termux-setup-storage
cp ~/models/Qwen3-1.7B-Q4_K_M.gguf ~/storage/downloads/
sha256sum ~/storage/downloads/Qwen3-1.7B-Q4_K_M.gguf
```

Android may ask Termux for shared-storage permission the first time `termux-setup-storage` is used.

Do not delete the proven Termux reference copy yet.

Then use the ORBI Edge Node system document picker and select the shared Downloads copy:

`Qwen3-1.7B-Q4_K_M.gguf`

Expected SHA-256:

`d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5`

Require `SHA-256 MATCH` before model loading.

The original source file is not deleted.

## 6. N4 first native inference

Load with context 4096 and threads 4.

Run the built-in Spanish prompt and record the complete response, wall-clock inference metrics shown by the APK, battery before/after, thermal category and physical feel.

Then stop Internet connectivity while retaining the local test state and repeat local inference.

No Termux inference process may be running.

## 7. N5/N9 network certification

Generate a pairing token in the APK and separately record the Node ID.

On the Windows PC:

```powershell
$env:ORBI_PAIRING_TOKEN="<token>"

python scripts/pc/native_node01_certify.py `
  --host 192.168.1.7 `
  --node-id "<node-id>"

Remove-Item Env:\ORBI_PAIRING_TOKEN
```

The evidence JSON intentionally excludes the pairing secret.

## 8. N6 headless test

With Qwen loaded and the foreground node service running:

```powershell
$env:ORBI_PAIRING_TOKEN="<token>"

python scripts/pc/native_headless_probe.py `
  --host 192.168.1.7 `
  --node-id "<node-id>"
```

After check 1/7, turn the POCO display off and do not reopen the app.

Formal target: 7/7 reachability checks, signed inference at check 5, about 30 minutes total, display remains off, no abnormal heat, service remains alive.

## 9. N7 fault recovery

Only after N6 passes, use the controlled runtime-failure button, observe supervisor detection, require bounded recovery and confirm inference returns.

## 10. N8 resource policy

Normal cool operation should produce a sensible resource decision.

Do not intentionally overheat the phone to test a thermal BLOCK. Edge cases are validated by automated tests and natural observations.

## 11. Evidence discipline

Physical certification closes only the gates actually observed.

A cumulative APK being newer than a gate does not automatically certify that gate.

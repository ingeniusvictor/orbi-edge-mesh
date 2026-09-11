# N0 — Node-01 Physical Validation

Status: WAITING FOR CI APK

## Objective

Validate the first ORBI Edge Node native APK on the real POCO X7 Pro.

N0 is not complete from CI alone. Physical hardware evidence is mandatory.

## Preconditions

- N0 GitHub Actions build is green.
- Debug APK artifact exists.
- Node-01 is the POCO X7 Pro used for the Phase 0 reference tests.
- No Termux process is required by the APK.

## Installation paths

### Preferred: ADB from Windows

After enabling Android Developer Options and USB debugging:

```powershell
adb devices
adb install -r app-debug.apk
```

### Manual fallback

Copy the APK to the POCO and install it using Android's package installer after explicitly authorizing installation from the chosen file source.

Do not disable platform security globally.

## Physical checks

Launch ORBI Edge Node and record exactly what appears.

Expected:

- app title: ORBI Edge Node
- build: 0.1.0-n0
- device: POCO model reported by Android
- Android: installed Android release
- ABI: arm64-v8a
- Native runtime: JNI BRIDGE READY
- AI runtime: NOT LOADED

## PASS criteria

- install succeeds;
- launch succeeds;
- no crash;
- device identity is plausible/correct;
- JNI bridge reports READY;
- app remains open for at least 5 minutes;
- screen rotation/background/foreground cycle does not immediately crash;
- disabling Wi-Fi does not prevent the N0 screen from working.

## FAIL evidence

If a failure occurs, record:

- screenshot/photo;
- exact Android message;
- whether install or launch failed;
- Logcat excerpt if available;
- app version;
- APK source commit.

## Certification

Only after this physical PASS may Issue #21 be closed and N1 implementation begin.

# ORBI Edge Node Native — Current Research Status

Status date: 2026-09-11

## Proven physically before native track

Phase 0 Termux reference on Node-01:

- Qwen3 1.7B Q4_K_M local inference: PASS
- offline inference: PASS
- trusted-LAN serving: PASS
- Windows-to-phone chat completion: PASS
- 30-minute screen-off/headless test: 7/7 PASS
- post-20-minute headless inference: PASS

Termux is now the reference/diagnostic baseline rather than the intended final runtime.

## Native implementation state

| Gate | Implementation | CI/build | Physical certification |
|---|---|---|---|
| N0 APK + JNI | implemented | PASS | pending Node-01 |
| N1 Android telemetry | implemented | PASS | pending Node-01 |
| N2 pinned llama.cpp | implemented | PASS | pending Node-01 |
| N3 GGUF import/hash | implemented | PASS | pending Node-01 |
| N4 APK-owned inference | implemented | PASS after C++ API fix | pending Node-01 |
| N5 local API | implemented | PASS | pending Node-01 |
| N6 foreground headless service | implemented | PASS | pending Node-01 |
| N7 bounded supervisor | implemented | PASS | pending fault injection |
| N8 resource guard | implemented | PASS | pending Node-01 observation |
| N9 local signed pairing | implemented | PASS at previous head; latest cumulative rebuild pending | pending pairing tests |
| N10 three-node manager | implemented | manager tests PASS at previous head; cumulative rebuild pending | pending Node-01/02/03 |
| R1 role-aware routing | prepared | manager tests PASS at previous head; cumulative rebuild pending | post-N10 |
| R2 storage-aware placement | prepared | tests staged | post-N10 |
| R3 distributed feasibility gate | prepared | tests staged | post-N10 measurements |

## Current cumulative candidate

Branch:

`feature/native-r3-distributed-feasibility`

Version:

`0.12.0-r3-research`

The cumulative build embeds its Git commit in `BuildConfig.GIT_SHA` and displays the short source commit in the app.

## Critical claim boundary

Only the Phase 0 Termux behaviors above are physically certified today.

Native N0-N9 features are implemented and progressively CI-tested, but they remain physically uncertified until the cumulative APK is installed and exercised on the POCO X7 Pro.

N10/R1/R2/R3 require later multi-node measurements and must not be described as already demonstrated.

# ORBI Edge Node Native — Architecture v0.1

## Objective

Replace the operational role currently provided by Termux with an ORBI-owned Android runtime while preserving the proven Phase 0 behavior as a reference baseline.

## Layering

```text
UI / Operator Surface
        |
Application Orchestration
        |
+-------------------------------+
| Device Profiler               |
| Model Manager                 |
| Inference Manager             |
| Node Supervisor               |
| Local API                     |
| Trust / Pairing               |
| Mesh Agent                    |
+-------------------------------+
        |
Kotlin Native Boundary
        |
JNI
        |
+-------------------------------+
| ORBI Native Runtime           |
| llama.cpp (from N2 onward)    |
| future whisper.cpp adapters   |
+-------------------------------+
        |
Android / Linux kernel / SoC
```

## Design rules

1. Kotlin owns Android lifecycle and policy integration.
2. C/C++ owns performance-critical inference runtime integration.
3. JNI remains intentionally narrow.
4. UI never calls native inference primitives directly.
5. model state is explicit: absent / discovered / validated / loaded / error.
6. runtime state is explicit: stopped / starting / ready / busy / protected / error.
7. unavailable telemetry is represented as unavailable, never guessed.
8. headless operation must use Android-supported lifecycle mechanisms.
9. no public network exposure is assumed.
10. resource protection wins over availability.

## JNI boundary

The native bridge should expose coarse operations rather than hundreds of llama.cpp internals.

Target direction:

```text
nativeRuntimeVersion()
nativeCreate(config)
nativeLoadModel(path, config)
nativeGenerate(request)
nativeUnloadModel()
nativeDestroy()
```

Exact APIs are frozen only per implementation gate.

## Threading

- UI thread must never perform model loading or inference.
- native work runs through dedicated coroutine/executor boundaries.
- cancellation and teardown must be explicit.
- N0 has no inference threads.

## Failure philosophy

A native error must become a bounded application state, not an application crash whenever safely possible.

Examples:

- missing model -> MODEL_NOT_FOUND
- invalid GGUF -> MODEL_INVALID
- load OOM -> MODEL_LOAD_FAILED
- thermal protection -> PROTECTED
- native bridge failure -> NATIVE_ERROR

## Security posture

N0-N4 are single-node research stages.

When LAN serving begins in N5:
- trusted LAN only;
- no router port forwarding;
- no public exposure;
- explicit security warning.

Privileged mesh trust begins in N9.

## Termux relationship

Termux remains the diagnostic/reference implementation until native parity is certified at N6.

It is not deleted because it provides:
- comparison measurements;
- recovery access;
- low-level diagnostics;
- a known-good inference baseline.

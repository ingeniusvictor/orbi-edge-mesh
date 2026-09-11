# N2 llama.cpp Android Preparation

Status: COMPILE-ONLY RESEARCH PREP

This branch prepares Android-native linkage against the same llama.cpp revision already proven in the Node-01 Termux reference path.

## Pinned upstream

- repository: ggml-org/llama.cpp
- commit: df03399b885831b2a1603b3abb0d8c156808e363
- Phase 0 observed build: 0.4.0-dev / b10902-df03399b8

## Purpose

N2 does not load a GGUF model yet.

It proves:

1. Android NDK can compile the pinned llama.cpp library for arm64-v8a.
2. ORBI's C++ JNI library can link to llama.cpp.
3. Kotlin can call an ORBI JNI function that in turn calls llama.cpp.
4. No Termux runtime dependency is required.

## JNI smoke

The N2 preview exposes llama.cpp system information through:

`NativeBridge.llamaSystemInfo()`

This is intentionally a narrow proof of linkage.

## Build policy

The CMake integration disables unrelated llama.cpp tools, tests, examples, server, OpenSSL and subprocess support.

The upstream revision is pinned rather than following HEAD.

## Certification

A green CI build is only a compile/link gate.

Physical N2 certification will still require launching the APK on Node-01 after N0/N1 hardware validation.

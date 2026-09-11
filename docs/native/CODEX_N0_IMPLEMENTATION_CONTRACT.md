# Codex Implementation Contract — N0 Native Foundation

Status: FROZEN FOR IMPLEMENTATION

## Mission

Build the smallest real Android-native ORBI Edge Node foundation that can be compiled into an arm64 APK and installed on Node-01.

This is a research foundation. Do not optimize for commercial polish.

## Allowed scope

- `android/edge-node-native/**`
- N0-specific documentation and tests
- build fixes required to make N0 compile

## Required architecture

- Kotlin
- Jetpack Compose
- Android NDK
- CMake
- one minimal JNI bridge
- arm64-v8a only for N0
- package: `com.orbi.edgenode`

## Required screen

Display:

- ORBI Edge Node
- app version
- Android device model
- Android version
- ABI
- native bridge status

## Native requirement

N0 does NOT integrate llama.cpp yet.

It MUST prove that the APK can load an ORBI-owned native C++ library through JNI and return a deterministic status string.

Expected native status:

`JNI BRIDGE READY`

## Runtime constraints

- no Termux dependency
- no root dependency
- no cloud runtime dependency
- no analytics
- no login/account
- no model download
- no inference
- no local HTTP server
- no mesh logic

## Acceptance gates

1. Gradle configuration resolves.
2. `:app:assembleDebug` passes.
3. arm64-v8a APK is produced.
4. APK installs on Node-01.
5. App launches without crash.
6. Device identity is visible.
7. Native bridge reports `JNI BRIDGE READY`.
8. App performs no required network operation at runtime.

## Stop conditions

Do not continue into N1 or N2 merely because N0 compiles.

N0 is complete only after physical installation evidence from Node-01.

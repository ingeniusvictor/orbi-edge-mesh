# ORBI Edge Node Native

Research implementation of an Android-native ORBI Edge Node.

## N0 scope

N0 proves:

- a real Android app can be built;
- the app can identify the device;
- an ORBI-owned C++ shared library can be loaded through JNI;
- the runtime does not depend on Termux.

N0 intentionally does not include llama.cpp or model inference.

## Build

From this directory with Android SDK/NDK installed:

```bash
gradle :app:assembleDebug
```

Expected APK:

`app/build/outputs/apk/debug/app-debug.apk`

## Expected Node-01 screen

- ORBI Edge Node
- research build version
- POCO device model
- Android version
- arm64-v8a
- Native runtime: JNI BRIDGE READY
- AI runtime: NOT LOADED

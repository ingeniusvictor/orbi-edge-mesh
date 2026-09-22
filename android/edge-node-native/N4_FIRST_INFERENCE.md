# N4 First Native Inference Research Preview

This branch contains the first end-to-end APK-owned inference path.

## Intended physical sequence

1. select the exact Qwen3 1.7B Q4_K_M GGUF;
2. copy it into app-private storage;
3. verify SHA-256;
4. load it through ORBI JNI into the pinned llama.cpp runtime;
5. create a 4096-token context using 4 CPU threads;
6. generate a short Spanish response;
7. unload the model cleanly.

## Important

This branch is compile-preparation only until tested on the POCO X7 Pro.

A green GitHub Actions build proves:
- Kotlin/C++ API agreement;
- llama.cpp API compatibility at compile/link time;
- arm64 packaging.

It does NOT prove:
- Android runtime model load;
- memory behavior;
- generation quality;
- thermal behavior;
- offline inference.

Those require Node-01.

# N3 Model Import Research Preview

This preview extends the compile-only N2 llama.cpp link with an Android-native GGUF import path.

## Behavior

- opens Android's system document picker;
- copies the selected file into app-private model storage;
- computes SHA-256 while copying;
- accepts only the exact Node-01 reference Qwen3 1.7B Q4_K_M hash;
- deletes the partial file on validation failure;
- does not load the model into llama.cpp yet.

## Reference hash

`d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5`

## Security / integrity intent

The file picker grants user-selected access only. The app does not request broad storage access.

## Gate

N3 is not certified until:
- N2 has passed on hardware;
- the exact GGUF is selected on Node-01;
- hash validation passes;
- the app-private copy is confirmed;
- invalid-file behavior is physically tested.

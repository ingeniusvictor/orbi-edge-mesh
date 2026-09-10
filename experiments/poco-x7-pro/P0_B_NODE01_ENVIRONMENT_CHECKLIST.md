# P0-B — Node-01 Environment Checklist

Device: POCO X7 Pro  
Role: Node-01  
Status: READY FOR EXECUTION

## Pre-flight

- [ ] Battery above 40%
- [ ] Phone case removed for first thermal characterization if convenient
- [ ] Fast charging disconnected during sustained inference
- [ ] At least 15 GB free storage
- [ ] Stable Wi-Fi available
- [ ] Android Memory Extension setting recorded
- [ ] No root / bootloader modifications planned

## Environment

- [ ] Termux installed
- [ ] Packages updated
- [ ] git installed
- [ ] cmake installed
- [ ] clang installed
- [ ] libandroid-spawn installed
- [ ] baseline script executed
- [ ] baseline artifact preserved

## Runtime

- [ ] llama.cpp cloned
- [ ] llama.cpp commit SHA recorded
- [ ] Release build configured
- [ ] llama-cli produced
- [ ] llama-server produced
- [ ] llama-cli version recorded

## Model

- [ ] ~/models created
- [ ] first GGUF downloaded/copied
- [ ] model filename recorded
- [ ] quantization recorded
- [ ] file size recorded

## Smoke test

- [ ] CLI model load succeeds
- [ ] first prompt completes
- [ ] coherent answer returned
- [ ] internet-disabled inference verified
- [ ] no crash
- [ ] no unsafe thermal behavior observed

## Completion

P0-B result:

- [ ] PASS
- [ ] PASS WITH LIMITATIONS
- [ ] FAIL

Evidence location:

```text
TBD
```

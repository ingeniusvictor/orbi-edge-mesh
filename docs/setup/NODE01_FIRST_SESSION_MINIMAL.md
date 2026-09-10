# Node-01 — First Session Minimal Path

If time is limited, do only this:

```bash
pkg update
pkg install git -y
cd ~
git clone https://github.com/ingeniusvictor/orbi-edge-mesh.git
cd orbi-edge-mesh
git checkout feature/phase-0-foundation
bash scripts/android/bootstrap_node01_termux.sh
bash scripts/android/capture_baseline.sh
bash scripts/android/build_llama_node01.sh
```

Stop there if needed.

That first session is still useful because it certifies the Android toolchain and captures the exact device baseline without requiring a model download yet.

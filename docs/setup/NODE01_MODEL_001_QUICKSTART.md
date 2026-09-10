# Node-01 Model 001 — Quickstart

After llama.cpp builds successfully:

```bash
cd ~/orbi-edge-mesh
git checkout feature/phase-0-foundation
git pull

bash scripts/android/download_node01_phase0_model.sh
bash scripts/android/run_node01_phase0_model.sh
```

After the first successful run, repeat the inference with Internet access disabled to prove local execution.

Do not optimize threads, context or larger models yet. First capture a clean baseline.

# ORBI Edge Mesh

Private, local-first AI infrastructure built from reused Android devices.

## Phase 0 — Foundation & Baseline

Initial objective: certify one Android device as a reproducible local AI node before building multi-device orchestration.

### Initial hardware

- Node-01: POCO X7 Pro — 12 GB physical RAM / 512 GB storage — principal experimental node.
- Node-02: Xiaomi 11T Pro — 8 GB physical RAM / 256 GB storage — secondary compute node.
- Node-03: Xiaomi Mi 10T Lite — 6 GB physical RAM / 256 GB storage — auxiliary services node.

Combined physical resources are distributed, not unified: 26 GB RAM and approximately 1 TB of storage across three devices.

## First milestone

POCO X7 Pro -> local model -> local API -> Wi-Fi client -> reproducible benchmark.

No root, no bootloader unlock, no cloud dependency, and no hardware purchases are required for the first milestone.

## Architecture direction

ORBI Edge Mesh will evolve through:

1. Android Node Agent
2. Hardware Profiler
3. Thermal Protection Layer
4. Power Manager
5. Local OpenAI-compatible API
6. Device Discovery
7. Scheduler / Router
8. Model Storage Manager
9. Dashboard
10. Later research: MoE expert streaming and distributed inference

## Project principles

- Local-first and privacy-first.
- Reuse existing hardware before buying dedicated servers.
- Benchmark before optimizing.
- Keep physical RAM, virtual memory, and storage metrics separate.
- Prefer reversible, non-root experimentation on daily-use devices.
- Treat large-model streaming as a later research phase, not the starting point.

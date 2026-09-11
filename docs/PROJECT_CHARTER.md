# ORBI Edge Mesh — Project Charter

## Mission

Build useful private AI infrastructure from Android hardware that is already available, delaying dedicated server purchases until real workloads justify them.

## MVP thesis

A heterogeneous group of reused phones can provide useful local AI capacity when each device is treated as an independently measurable node and coordinated through software.

## First proof

One POCO X7 Pro runs a local model and responds to requests from a PC over the local network.

## First mesh proof

Three different Android devices discover/register with ORBI and local AI tasks can be routed between them without cloud inference.

## Constraints

- near-zero hardware spend for initial phases
- local-first operation
- no requirement for cellular service
- no assumption that distributed RAM is unified RAM
- no assumption that virtual RAM equals physical RAM
- benchmark every meaningful performance claim
- protect batteries and device thermals
- preserve reversibility on daily-use devices

## Initial node roles

- Node-01: POCO X7 Pro — main LLM / experiments
- Node-02: Xiaomi 11T Pro — secondary LLM / fallback
- Node-03: Mi 10T Lite — speech, embeddings, lightweight services
- Node-00: Xiaomi 14 Ultra — optional reference benchmark only

## Long-term product concepts

Possible future forms:
- ORBI Edge Software
- ORBI Edge Box
- ORBI Edge Rack

These are product hypotheses, not Phase 0 deliverables.

# EDGE-ECC-P2 — AgentShield Repository Baseline

Status: REPORT-ONLY / BASELINE PENDING FIRST EXECUTION

## Purpose

Create a fresh ORBI Edge Mesh security baseline for the Native Alpha line.

This phase does **not** inherit any accepted finding from:

- ORBI Creative Studio;
- ORBI PVMetrics;
- L.U.M.I.A.;
- ORBI News;
- ORBI Agent Engineering Kit.

## Pinning

AgentShield:

- package: `ecc-agentshield@1.6.0`
- commit: `b0891303bdcd6037376a94263d45cfd2ff3dfb98`

GitHub actions are pinned to immutable SHAs.

## Report-only guarantees

- `contents: read`;
- checkout credentials not persisted;
- `fail-on-findings: false`;
- `fail-on-supply-chain: false`;
- no automatic fixes;
- offline supply-chain lookup;
- verified evidence pack;
- retained SARIF/baseline artifact.

## Edge-specific review priorities

Classify findings especially around:

- pairing tokens / HMAC secrets;
- request signing / replay protection;
- LAN API exposure;
- Android intent/service configuration;
- JNI/native library loading;
- subprocess / shell / PC-side validation scripts;
- local model paths and imported files;
- capability manifests;
- resource policy bypass;
- model placement / transfer tooling;
- GitHub Actions and dependency supply chain.

## Evidence boundary

A clean scanner does not prove:

- physical node trust;
- pairing correctness;
- transport encryption;
- model integrity on device;
- native model load/inference;
- LAN isolation;
- headless reliability;
- thermal/power behavior;
- distributed execution.

## Exit criteria

P2 passes only when:

1. AgentShield completes successfully;
2. evidence pack verification passes;
3. supply-chain status is recorded;
4. every finding class is inspected;
5. any accepted false positive is justified from Edge evidence;
6. Edge ECC PR Gate remains GREEN;
7. no runtime/product behavior changes.

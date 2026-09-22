# EDGE-ECC-P2 — AgentShield Repository Baseline

Status: REPORT-ONLY / BASELINE CLASSIFIED

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

## First-run evidence

Run: `35736298537`

Result:

- score: **100 / 100**;
- grade: **A**;
- findings: **0**;
- unique finding classes: **0**;
- supply chain: **CLEAN**;
- evidence-pack verification: **PASSED**;
- evidence-pack digest: `sha256:0ef2730141a44cbf8f172ee1799dc9be84ab6c0ae84e42b81caa005fdea8c728`;
- artifact ID: `10698241187`;
- artifact digest: `sha256:c1e4a630b4f40c15192056348834c045669b942a0674bc622ceb87aeb41f45bf`.

Classification:

`BASELINE_CLEAN — NO_ACCEPTED_FINDING_CLASSES`

Any future AgentShield finding on Edge Mesh is therefore a **new finding class until explicitly reviewed**.

No repository-specific exception is required by P2.

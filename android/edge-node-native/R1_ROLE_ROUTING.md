# R1 Heterogeneous Service / Role Routing

## Research objective

Move beyond "all phones are interchangeable chat nodes."

Each ORBI Edge Node advertises only services it has actually validated. The mesh manager then selects nodes by:

1. requested service;
2. requested model;
3. trust / pairing;
4. model residency;
5. resource policy;
6. battery-aware tie-break;
7. deterministic fallback.

## Current validated service shape

The present APK advertises only:

`CHAT`

with the reference model:

`qwen3-1.7b-q4_k_m-node01`

No ASR/TTS/embedding capability is advertised yet because those native runtimes have not been physically validated.

## Future service vocabulary

Prepared research vocabulary:

- CHAT
- ASR
- TTS
- EMBEDDING
- UTILITY

A node MUST NOT advertise a role merely because its hardware might be capable of it.

## Manager usage

```powershell
python manager/native_mesh_manager.py `
  --config config/native-mesh.example.json `
  --service CHAT `
  --model-id qwen3-1.7b-q4_k_m-node01 `
  --prompt "Responde solo: ORBI ROLE ROUTING OK"
```

## Selection rule

A node is ineligible when any of the following is true:

- unreachable;
- unpaired;
- resource BLOCK;
- requested service absent;
- requested model absent;
- required model not loaded.

ALLOW is preferred over DEGRADE.

Within equivalent policy state, higher battery is preferred as the current deterministic research tie-break.

## Why this matters

This is the first architectural step toward a genuinely heterogeneous reused-phone AI fabric:

- a stronger phone may host CHAT;
- another node may later host ASR;
- another may host TTS or lightweight utility models;
- the mesh manager routes work by capability rather than by hard-coded device identity.

This still does not imply unified RAM or distributed tensor execution.

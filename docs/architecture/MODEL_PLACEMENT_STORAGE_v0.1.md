# ORBI Edge Mesh — Model Placement & Storage v0.1

## Goal

Decide where model files should live without treating distributed phone storage as one shared filesystem.

## Core rule

```text
distributed storage != unified storage
```

Each phone owns its own local storage.

The manager may know:
- which node has a model;
- how large the model is;
- how much free storage remains;
- whether a replica exists elsewhere.

It must not pretend that Node-01 storage is directly available to Node-02.

## Placement factors

Initial Phase 0 placement considers:

- model already present;
- free storage;
- projected free storage after placement;
- minimum free-space reserve;
- physical RAM as a secondary tie-break signal.

## Storage reserve

Initial policy keeps at least the larger of:

```text
8 GB
or
10% of total device storage
```

free after planned model placement.

These values are experimental and will be calibrated.

## Model roles

```text
primary
fallback
specialized
replica
```

## Residency classes

```text
hot
warm
cold
```

Example target:

```text
Node-01 / POCO
qwen-main → primary / hot

Node-02 / 11T Pro
qwen-light → fallback / warm

Node-03 / Mi 10T Lite
whisper-small → specialized / warm
kokoro-es → specialized / cold
```

## Future evolution

Later versions may include:
- checksums
- versioning
- quantization variants
- download/copy plans
- deduplication
- model eviction
- storage wear considerations
- measured load time
- replica policy

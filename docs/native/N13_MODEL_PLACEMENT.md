# N13 Heterogeneous Native Model Placement Planner

## Purpose

N13 plans where a complete model should live across independent Android nodes.

It does not transfer files and it does not combine RAM.

## Inputs

The planner consumes saved N12 capability manifests containing:

- node ID;
- available storage;
- physical memory total;
- current resource-policy action;
- model IDs already available on the node.

## Rules

1. BLOCK/UNKNOWN resource states are excluded from new placement.
2. If the requested model already exists on an eligible node, keep it there.
3. Otherwise require enough storage for the model plus a free-space reserve.
4. Prefer the candidate with the greatest projected free-storage headroom.
5. Use physical RAM as a secondary signal in the inherited placement helper.

The default reserve remains the Phase 0 provisional 8 GiB storage reserve and is configurable.

## Important

The planner produces only a recommendation.

`binary_transfer_performed` is always false.

Automatic model copying/downloading is deliberately outside N13.

## Example

```powershell
python manager/native_placement_planner.py `
  --input config/native-capability-manifests.example.json `
  --model-id qwen3-1.7b-q4_k_m-node01 `
  --model-size-bytes <actual-gguf-size>
```

Use actual measured model size rather than a marketing/rounded estimate.

## Physical PASS

N13 can only be physically validated after N12 manifests are collected from real nodes and the planner recommendation is checked against their actual storage/RAM state.

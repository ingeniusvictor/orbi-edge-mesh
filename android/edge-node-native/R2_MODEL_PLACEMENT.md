# R2 Storage-Aware Model Placement

## Research objective

Allow ORBI to decide where a model could reside across independent Android nodes without pretending their storage is one filesystem.

R2 is advisory only.

The planner never:

- deletes a model;
- transfers a model;
- moves user files;
- modifies Android storage;
- treats distributed storage as unified.

## Inputs

Each node reports:

- total/available storage;
- total/available memory;
- battery;
- Android thermal/resource policy;
- supported services;
- loaded model IDs;
- pairing/reachability state.

The initial catalog contains only the physically proven Qwen3 1.7B Q4_K_M reference model.

## Provisional reserve policy

After a proposed model placement, ORBI requires that free storage remain at least:

`max(8 GiB, 10% of total node storage)`

This is a conservative research policy, not a universal Android requirement.

## Planner behavior

Candidates are rejected when:

- unreachable;
- unpaired;
- resource policy is BLOCK;
- requested service is unsupported;
- storage metrics are unavailable;
- projected free storage would violate the reserve.

Already-resident models are preferred before proposing a new copy.

## Example

```powershell
python manager/native_model_placement.py `
  --config config/native-mesh.example.json `
  --catalog models/native-model-catalog.example.json `
  --model-id qwen3-1.7b-q4_k_m-node01 `
  --replicas 2
```

## PASS

R2 physical certification requires:

1. `/node` reports credible storage values on Node-01/02/03;
2. planner produces deterministic proposals;
3. reserve policy is respected;
4. blocked nodes are excluded;
5. no automatic destructive action occurs;
6. the user remains in control of actual model import/transfer.

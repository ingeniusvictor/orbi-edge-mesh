# N10 Native Multi-Node Coordination — First Research Shape

## Scope

N10 intentionally does **not** merge phone RAM, storage or tensor memory.

Each Android device remains an independent ORBI Edge Node.

The first native mesh manager performs whole-workload routing:

```text
                  ORBI Native Mesh Manager
                         |
          +--------------+--------------+
          |              |              |
       Node-01         Node-02        Node-03
       Android         Android        Android
       own RAM         own RAM        own RAM
       own model       own model      own model
```

## Manager inputs

A local JSON config contains node name, LAN host/port, node ID, and the environment-variable name holding the pairing token.

Secrets are **not** stored in the JSON config.

## Discovery / observation

For each configured node the manager reads `/node` and `/v1/models`.

It verifies reported node identity when available and records reachability, model-loaded state, the model IDs actually advertised by that node, pairing state, resource policy action, battery and thermal category.

A node that says `model_loaded=true` but does not advertise a usable model ID is not eligible.

## Initial routing

Only nodes that are reachable, paired, model-loaded, advertise at least one model, and are in ALLOW or DEGRADE state are eligible.

Preference:

1. ALLOW before DEGRADE;
2. higher reported battery within the same policy state;
3. stable node name as deterministic final tie-break.

For a selected node, the manager sends the first model ID actually advertised by that node through `/v1/models`. It does not synthesize or hard-code a Node-01 model identity.

If the first eligible node fails during the signed request, the manager attempts the next eligible node.

This is whole-request fallback, **not distributed inference**.

## Example

```powershell
$env:ORBI_NODE01_TOKEN="<node-01-token>"
$env:ORBI_NODE02_TOKEN="<node-02-token>"
$env:ORBI_NODE03_TOKEN="<node-03-token>"

python manager/native_mesh_manager.py `
  --config config/native-mesh.example.json `
  --prompt "Responde solo: ORBI MESH OK"
```

Use `--status-only` first during physical admission. The status output intentionally omits token environment-variable names and never emits token values.

## N10 physical PASS

With all three permanent devices:

1. each native APK starts independently;
2. each node has a unique node ID and pairing secret;
3. manager observes all three;
4. each routing candidate advertises its actually loaded model;
5. a whole chat workload routes to an eligible node using that node's advertised model ID;
6. stopping the selected node causes fallback to another eligible node;
7. blocked/resource-protected nodes are skipped;
8. no cloud inference is used;
9. no claim is made that the distributed physical RAM is unified.

A two-node rehearsal is useful evidence but does **not** close N10; final PASS still requires the three-node acceptance gate.

## Future research beyond N10

Only after this is stable should ORBI study automatic model placement, specialized speech/TTS nodes, network-cost-aware scheduling, distributed experts, and tensor/shard execution across phones.

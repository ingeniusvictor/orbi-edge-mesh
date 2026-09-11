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

It verifies reported node identity when available and records reachability, model-loaded state, pairing state, resource policy action, battery and thermal category.

## Initial routing

Only nodes that are reachable, paired, model-loaded, and in ALLOW or DEGRADE state are eligible.

Preference:

1. ALLOW before DEGRADE;
2. higher reported battery within the same policy state;
3. stable node name as deterministic final tie-break.

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

## N10 physical PASS

With all three permanent devices:

1. each native APK starts independently;
2. each node has a unique node ID and pairing secret;
3. manager observes all three;
4. a whole chat workload routes to an eligible node;
5. stopping the selected node causes fallback to another eligible node;
6. blocked/resource-protected nodes are skipped;
7. no cloud inference is used;
8. no claim is made that the distributed physical RAM is unified.

## Future research beyond N10

Only after this is stable should ORBI study automatic model placement, specialized speech/TTS nodes, network-cost-aware scheduling, distributed experts, and tensor/shard execution across phones.

# N12 Capability Manifest and Workload-Aware Routing

## Goal

A node must describe what it can actually execute before the mesh manager assigns work to it.

## Endpoint

`GET /capabilities`

The initial manifest contains:

- schema and protocol version;
- stable node ID;
- build version;
- device model and ABI;
- physical/available memory from Android;
- total/available app storage;
- capability strings;
- model IDs available in app-private storage;
- model IDs currently loaded;
- current resource-policy action;
- headless support;
- signed-control requirement;
- NSD service type;
- explicit `unified_ram: false`.

## Initial capability strings

- `node.health`
- `node.diagnostics`
- `node.headless`
- `node.signed-control`
- `text.generate` when llama.cpp is linked
- model availability/load markers when applicable

## Manager behavior

The native mesh manager now accepts:

`--capability <capability-name>`

Default:

`text.generate`

A node is eligible only when it is reachable, paired, model-loaded, resource-eligible, and advertises the requested capability.

## Scope

This is capability-aware whole-workload routing.

It does not create shared RAM, tensor sharding, KV migration or distributed model execution.

## Physical PASS

With multiple real nodes, intentionally request a capability that one node lacks and verify the manager skips it while selecting a compatible node.

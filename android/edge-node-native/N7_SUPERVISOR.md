# N7 Bounded Native Supervisor

## Objective

Detect loss of the desired local model runtime and attempt bounded recovery inside the APK-owned service.

## Model

The app persists:

- validated model path;
- desired model-loaded state;
- context size;
- thread count.

The headless service runs an `EdgeNodeSupervisor` every 15 seconds.

If:
- the model is desired;
- the model is no longer loaded;
- a validated model path exists;
- recovery is authorized;
- the restart limit is not exhausted;

then the supervisor attempts to reload the model.

## Bound

Maximum automatic restart attempts per supervisor lifecycle: **3**.

After repeated failure the node enters a local quarantine state and stops retrying.

There is no unbounded restart loop.

## N7 recovery gate

N7 uses an explicit temporary controlled-research allow gate.

It is intentionally replaced by Android-native thermal/power policy in N8 before autonomous recovery is considered safe for longer unattended operation.

## Fault injection

The N7 preview includes a supervised test button that unloads the model while leaving the desired-state flag true.

Expected sequence:

```text
MODEL LOADED
   ↓
fault injection: unload
   ↓
supervisor detects model absent
   ↓
recovery authorization
   ↓
reload attempt
   ↓
MODEL LOADED
```

## PASS

Physical N7 certification requires:

- model loaded normally;
- headless service active;
- fault injected deliberately;
- supervisor detects the loss;
- one bounded reload succeeds;
- local API returns to usable inference;
- restart count is visible;
- repeated forced failures cannot cause an infinite loop.

## Safety

Do not run fault injection while the device is hot or at critically low battery.

N8 adds the resource authorization gate.

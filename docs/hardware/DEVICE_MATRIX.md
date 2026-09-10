# Device Matrix

## Known initial devices

| Node | Device | Physical RAM | Storage | Role | Notes |
|---|---|---:|---:|---|---|
| Node-01 | POCO X7 Pro 5G | 12 GB | 512 GB | Principal experimental LLM node | Daily-use device; non-root and reversible changes only |
| Node-02 | Xiaomi 11T Pro | 8 GB | 256 GB | Secondary compute node | Snapdragon platform useful for architecture comparison |
| Node-03 | Xiaomi Mi 10T Lite 5G | 6 GB | 256 GB | Auxiliary services | Wi-Fi-only operation is sufficient for ORBI Edge Mesh |
| Node-00 | Xiaomi 14 Ultra | 16 GB | 512 GB | Reference benchmark only | Not a permanent node unless explicitly authorized |

## Aggregate available permanent-node resources

- Physical RAM: 26 GB distributed
- Storage: approximately 1,024 GB distributed
- Three independent SoCs
- Three mobile GPUs
- Three independent battery-backed devices

These values are distributed resources. ORBI must not present them as one unified 26 GB RAM machine or one unified 1 TB filesystem.

## Profiling fields to capture

Each node profile should eventually contain:

```yaml
node_id:
device_name:
android_version:
soc:
cpu:
gpu:
npu:
physical_ram_mb:
memory_extension_enabled:
memory_extension_mb:
storage_total_mb:
storage_free_mb:
storage_type:
battery_percent:
charging:
battery_temperature_c:
thermal_state:
wifi_link:
runtime:
runtime_version:
models:
last_benchmark:
```

## Memory-extension policy

Android/Xiaomi memory extension uses storage-backed virtual memory and is not physical RAM.

Phase 0 should benchmark at least:
- memory extension OFF
- memory extension ON, where available

Metrics:
- time to first token
- tokens per second
- peak memory
- storage I/O
- temperature
- stability

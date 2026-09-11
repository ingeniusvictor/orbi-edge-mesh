# ORBI Edge Node Native — Research Roadmap

## Proven reference baseline

Phase 0 / Termux has already proven on Node-01:

- local Qwen3 1.7B Q4_K_M inference;
- offline inference;
- llama-server over trusted LAN;
- PC-to-phone inference;
- 30-minute screen-off operation;
- post-20-minute inference while screen off;
- 7/7 headless reachability checks.

The native track must reproduce these capabilities progressively without depending on Termux.

## Native gates

| Gate | Goal | Exit condition |
|---|---|---|
| N0 | Android foundation | APK builds, installs, opens, JNI bridge works |
| N1 | Hardware profiler | native app reports device/RAM/storage/battery/network/thermal signals |
| N2 | llama.cpp JNI | llama.cpp library builds and is callable from Kotlin |
| N3 | GGUF model manager | existing Qwen GGUF is selected, validated and loadable |
| N4 | Native inference | first Qwen completion occurs entirely inside APK |
| N5 | Local API | PC can call health/models/chat endpoints on Node-01 |
| N6 | Headless parity | 30-minute screen-off test passes without Termux |
| N7 | Supervisor | runtime failure is detected and bounded recovery works |
| N8 | Resource guard | thermal/power policy can block/reduce/recover work |
| N9 | Trust | explicit pairing protects privileged mesh actions |
| N10 | Multi-node | Node-01, Node-02 and Node-03 coordinate local workloads |

## Research tracks after N10

Only after autonomous native nodes are stable:

- heterogeneous scheduling;
- specialized model residency;
- automatic workload migration;
- storage-aware placement;
- distributed expert experiments;
- distributed model/shard experiments;
- network-cost-aware inference research.

These are research goals, not promised product features.

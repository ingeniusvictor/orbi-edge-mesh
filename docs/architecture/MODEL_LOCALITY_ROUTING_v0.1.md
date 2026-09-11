# ORBI Edge Mesh — Model Locality Routing v0.1

## Goal

Route work to the node that already has the required model/service locally whenever possible.

## Why locality matters

On a phone mesh, transferring or repeatedly loading large models is expensive in:
- time;
- storage I/O;
- battery;
- heat;
- network bandwidth.

Therefore ORBI should prefer a node where the requested model is already loaded or immediately ready.

## Locality states

```text
loaded   → best
ready    → available
cold     → present but not loaded
disabled → unavailable by policy/config
missing  → unavailable
```

## Request dimensions

The scheduler can route by:

```text
service_type
model_id
family
```

Examples:

```text
service=llm, model_id=qwen-main
→ Node-01

service=speech_to_text, family=whisper
→ Node-03

service=text_to_speech, family=kokoro
→ Node-03
```

## Routing precedence

For eligible nodes:

1. model locality state;
2. runtime health;
3. thermal/power policy;
4. consecutive failures;
5. temperature;
6. deterministic node_id tie-break.

## Design consequence

ORBI nodes can specialize.

Example target layout:

```text
Node-01 / POCO X7 Pro
- primary Qwen
- optional Whisper fallback

Node-02 / Xiaomi 11T Pro
- lighter Qwen
- fallback LLM

Node-03 / Mi 10T Lite
- Whisper
- Kokoro
- embeddings
```

This specialization is a hypothesis until measured on real hardware.

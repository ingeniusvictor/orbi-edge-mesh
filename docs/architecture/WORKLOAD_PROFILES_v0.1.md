# ORBI Edge Mesh — Workload Profiles v0.1

## Goal

Stop treating all AI requests as equivalent.

ORBI Edge Mesh should route based on workload characteristics, not only generic service availability.

## Initial workload classes

```text
chat_short
generation_long
embedding
speech_to_text
text_to_speech
```

## Why this matters

A short assistant turn and a long generation can have different priorities.

Example:

```text
chat_short
→ latency matters more

generation_long
→ sustained thermal behavior matters more

speech_to_text
→ specialized speech node preferred

text_to_speech
→ low-latency voice node preferred
```

## Deterministic classifier

Phase 0 uses explicit rules.

For LLM:

```text
requested_output_tokens <= 512
→ chat_short

requested_output_tokens > 512
→ generation_long
```

This is intentionally simple.

## Model tags

Services can advertise tags such as:

```text
fast-chat
long-generation
embedding
stt
tts
```

A preferred tag can improve routing rank.

## Safety ordering

Workload preferences never bypass:

- thermal blocks
- battery blocks
- runtime availability

## Future evolution

Later classification may include:
- input size
- context length
- audio duration
- required quality tier
- deadline/latency SLO
- memory requirement
- expected energy cost

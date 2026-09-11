# Benchmarks

All performance claims for ORBI Edge Mesh must be backed by a stored benchmark record.

## Record format

Use one Markdown or JSON record per run.

Suggested ID:

`YYYYMMDD-node-model-runtime-runNN`

## Required fields

- date/time
- node ID
- device
- Android version
- physical RAM
- memory extension state
- runtime and version/commit
- model filename
- model family
- parameter class
- quantization
- file size
- context size
- thread count
- prompt
- prompt tokens
- generated tokens
- time to first token
- prompt processing speed
- generation speed
- peak RAM if observable
- initial/max/final temperature if observable
- battery initial/final
- charging state
- duration
- errors
- result

Do not compare runs if major parameters differ without explicitly noting the difference.

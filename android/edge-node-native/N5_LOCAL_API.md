# N5 Trusted-LAN Local API Research Preview

## Goal

Expose the APK-owned local model runtime to another device on the same trusted Wi-Fi/Ethernet network.

## Endpoints

- `GET /health`
- `GET /node`
- `GET /v1/models`
- `POST /v1/chat/completions`

## Security posture

N5 is deliberately limited to research on a trusted LAN.

The server:
- refuses to start unless Android reports Wi-Fi or Ethernet as the active transport;
- has no public-cloud dependency;
- is never intended to be router-port-forwarded;
- does not emit permissive CORS headers;
- limits request bodies to 64 KiB;
- has no authentication yet.

Explicit cryptographic pairing belongs to N9. Until then this server is a supervised lab interface only.

## Compatibility target

The chat endpoint uses an OpenAI-like request/response shape sufficient for the same Windows/PowerShell test used during Phase 0.

## Physical gate

N5 passes only when a PC on the same LAN can:

1. reach `/health`;
2. read `/v1/models`;
3. submit UTF-8 JSON containing Spanish text;
4. receive a real Qwen completion produced inside the APK.

No Termux inference process may participate in that test.

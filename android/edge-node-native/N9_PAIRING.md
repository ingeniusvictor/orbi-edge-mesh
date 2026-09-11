# N9 Explicit Pairing and Signed Local Control

## Why

Being connected to the same Wi-Fi is not sufficient authorization for privileged ORBI actions.

N9 introduces explicit local trust for chat inference.

## Node identity

Each ORBI Edge Node creates a persistent random node ID in app-private storage.

## Pairing secret

The app can generate/rotate a 32-byte random pairing secret encoded with URL-safe Base64.

For the research build the token is shown after generation/rotation so it can be copied into the trusted manager environment.

Do not publish or commit this token.

## Signed request

The current privileged endpoint is `POST /v1/chat/completions`.

Required headers:

- `X-ORBI-Node-ID`
- `X-ORBI-Timestamp` — epoch milliseconds
- `X-ORBI-Nonce`
- `X-ORBI-Signature`

Canonical payload:

```text
ORBI-AUTH-V1
<node-id>
<METHOD>
<path>
<timestamp-ms>
<nonce>
<body-sha256>
```

Signature: `HMAC-SHA256(pairing-secret, canonical-payload)`.

## Replay protection

- request clock window: ±120 seconds;
- nonce replay cache: 5 minutes;
- repeated nonce is rejected.

## Revocation

Revoking pairing removes the active secret and clears the replay cache.

Previously signed privileged requests then fail.

## PC test

In Windows PowerShell:

```powershell
$env:ORBI_PAIRING_TOKEN="<token shown by the POCO>"

python scripts/pc/orbi_signed_chat.py `
  --host 192.168.1.7 `
  --node-id "<node id shown by the POCO>"

Remove-Item Env:\ORBI_PAIRING_TOKEN
```

The token is intentionally read from an environment variable instead of a command-line parameter so it is less likely to remain in shell history.

## Security boundary

N9 provides local request authentication and integrity. It is **not transport encryption**.

For this research stage:

- use only a trusted local network;
- do not port-forward the node;
- do not expose port 8080 to the public Internet.

Future research may add TLS/mTLS or a Noise-style encrypted local control channel.

## Physical PASS

- unsigned chat request -> rejected;
- correctly signed paired request -> accepted;
- same nonce replay -> rejected;
- wrong node ID -> rejected;
- rotated/revoked secret invalidates the old manager credential.

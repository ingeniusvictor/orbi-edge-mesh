#!/usr/bin/env python3
"""Send an HMAC-signed chat request to a paired ORBI Edge Node."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def decode_token(token: str) -> bytes:
    padding = "=" * (-len(token) % 4)
    return base64.urlsafe_b64decode(token + padding)


def body_sha256(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def canonical_payload(node_id, method, path, timestamp_ms, nonce, body_hash):
    return "\n".join([
        "ORBI-AUTH-V1",
        node_id,
        method.upper(),
        path,
        str(timestamp_ms),
        nonce,
        body_hash.lower(),
    ])


def sign(secret: bytes, canonical: str) -> str:
    return hmac.new(secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--node-id", required=True)
    parser.add_argument(
        "--prompt",
        default="Responde en español y en una sola frase: ¿qué es ORBI Edge Mesh?",
    )
    parser.add_argument("--max-tokens", type=int, default=96)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    token = os.environ.get("ORBI_PAIRING_TOKEN")
    if not token:
        print(
            "ERROR: set ORBI_PAIRING_TOKEN in the environment; "
            "do not pass the pairing secret on the command line.",
            file=sys.stderr,
        )
        return 2

    try:
        secret = decode_token(token)
    except Exception as exc:
        print(f"ERROR: invalid ORBI_PAIRING_TOKEN: {exc}", file=sys.stderr)
        return 2

    if len(secret) != 32:
        print(
            f"ERROR: pairing token decoded to {len(secret)} bytes; expected 32.",
            file=sys.stderr,
        )
        return 2

    path = "/v1/chat/completions"
    url = f"http://{args.host}:{args.port}{path}"

    payload = {
        "model": "qwen3-1.7b-q4_k_m-node01",
        "messages": [{"role": "user", "content": args.prompt}],
        "max_tokens": max(1, min(args.max_tokens, 256)),
        "stream": False,
    }

    body = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    timestamp_ms = int(time.time() * 1000)
    nonce = secrets.token_hex(16)
    digest = body_sha256(body)
    canonical = canonical_payload(
        args.node_id,
        "POST",
        path,
        timestamp_ms,
        nonce,
        digest,
    )
    signature = sign(secret, canonical)

    request = Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "X-ORBI-Node-ID": args.node_id,
            "X-ORBI-Timestamp": str(timestamp_ms),
            "X-ORBI-Nonce": nonce,
            "X-ORBI-Signature": signature,
        },
    )

    try:
        with urlopen(request, timeout=args.timeout) as response:
            parsed = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP {exc.code}: {error_body}", file=sys.stderr)
        return 1
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(parsed, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

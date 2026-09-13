#!/usr/bin/env python3
"""Send the exact same signed ORBI request twice to validate replay protection."""

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


def sign(secret: bytes, canonical: str) -> str:
    return hmac.new(secret, canonical.encode("utf-8"), hashlib.sha256).hexdigest()


def send(url: str, body: bytes, headers: dict[str, str], timeout: float) -> tuple[int, str]:
    request = Request(url, data=body, method="POST", headers=headers)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--node-id", required=True)
    parser.add_argument("--timeout", type=float, default=120.0)
    args = parser.parse_args()

    token = os.environ.get("ORBI_PAIRING_TOKEN")
    if not token:
        print("ERROR: ORBI_PAIRING_TOKEN is not set.", file=sys.stderr)
        return 2

    secret = decode_token(token)
    if len(secret) != 32:
        print("ERROR: pairing token must decode to 32 bytes.", file=sys.stderr)
        return 2

    path = "/v1/chat/completions"
    url = f"http://{args.host}:{args.port}{path}"

    payload = {
        "model": "qwen3-1.7b-q4_k_m-node01",
        "messages": [{"role": "user", "content": "Responde solo: REPLAY TEST OK"}],
        "max_tokens": 8,
        "stream": False,
    }
    body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")

    timestamp_ms = int(time.time() * 1000)
    nonce = secrets.token_hex(16)
    digest = hashlib.sha256(body).hexdigest()
    canonical = "\n".join([
        "ORBI-AUTH-V1",
        args.node_id,
        "POST",
        path,
        str(timestamp_ms),
        nonce,
        digest,
    ])
    signature = sign(secret, canonical)

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-ORBI-Node-ID": args.node_id,
        "X-ORBI-Timestamp": str(timestamp_ms),
        "X-ORBI-Nonce": nonce,
        "X-ORBI-Signature": signature,
    }

    first_status, first_body = send(url, body, headers, args.timeout)
    print("FIRST:", first_status, first_body)

    second_status, second_body = send(url, body, headers, args.timeout)
    print("SECOND:", second_status, second_body)

    if first_status == 200 and second_status == 401 and "replay_detected" in second_body:
        print("PASS: replay protection rejected the exact same signed request.")
        return 0

    print("FAIL: replay acceptance criteria not met.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

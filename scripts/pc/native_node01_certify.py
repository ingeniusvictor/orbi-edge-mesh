#!/usr/bin/env python3
"""Automate non-destructive Node-01 native certification checks over trusted LAN."""

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
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def decode_token(token: str) -> bytes:
    padding = "=" * (-len(token) % 4)
    secret = base64.urlsafe_b64decode(token + padding)
    if len(secret) != 32:
        raise ValueError(
            f"pairing token decoded to {len(secret)} bytes; expected 32"
        )
    return secret


def request_json(
    request: Request | str,
    timeout: float,
) -> tuple[int, dict[str, Any]]:
    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        status = exc.code
        body = exc.read().decode("utf-8", errors="replace")

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        parsed = {"raw": body}

    return status, parsed


def chat_body(
    model_id: str,
    prompt: str,
    max_tokens: int = 64,
) -> bytes:
    return json.dumps(
        {
            "model": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "max_tokens": max(1, min(max_tokens, 256)),
            "stream": False,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def signed_headers(
    *,
    secret: bytes,
    node_id: str,
    method: str,
    path: str,
    body: bytes,
    timestamp_ms: int,
    nonce: str,
) -> dict[str, str]:
    body_hash = hashlib.sha256(body).hexdigest()
    canonical = "\n".join(
        [
            "ORBI-AUTH-V1",
            node_id,
            method.upper(),
            path,
            str(timestamp_ms),
            nonce,
            body_hash,
        ]
    )
    signature = hmac.new(
        secret,
        canonical.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    return {
        "Content-Type": "application/json; charset=utf-8",
        "X-ORBI-Node-ID": node_id,
        "X-ORBI-Timestamp": str(timestamp_ms),
        "X-ORBI-Nonce": nonce,
        "X-ORBI-Signature": signature,
    }


def signed_chat_request(
    *,
    base_url: str,
    node_id: str,
    secret: bytes,
    model_id: str,
    prompt: str,
    timestamp_ms: int | None = None,
    nonce: str | None = None,
) -> tuple[Request, int, str]:
    path = "/v1/chat/completions"
    body = chat_body(model_id, prompt)
    ts = timestamp_ms if timestamp_ms is not None else int(time.time() * 1000)
    actual_nonce = nonce or secrets.token_hex(16)
    headers = signed_headers(
        secret=secret,
        node_id=node_id,
        method="POST",
        path=path,
        body=body,
        timestamp_ms=ts,
        nonce=actual_nonce,
    )
    return (
        Request(
            base_url + path,
            data=body,
            method="POST",
            headers=headers,
        ),
        ts,
        actual_nonce,
    )


def unsigned_chat_request(
    *,
    base_url: str,
    model_id: str,
    prompt: str,
) -> Request:
    return Request(
        base_url + "/v1/chat/completions",
        data=chat_body(model_id, prompt),
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
        },
    )


def check(
    name: str,
    passed: bool,
    evidence: dict[str, Any],
) -> dict[str, Any]:
    return {
        "name": name,
        "pass": bool(passed),
        "evidence": evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--node-id", required=True)
    parser.add_argument(
        "--model-id",
        default="qwen3-1.7b-q4_k_m-node01",
    )
    parser.add_argument(
        "--prompt",
        default="Responde solo: ORBI NATIVE CERTIFICATION OK",
    )
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("node01-native-certification.json"),
    )
    args = parser.parse_args()

    token = os.environ.get("ORBI_PAIRING_TOKEN")
    if not token:
        print(
            "ERROR: set ORBI_PAIRING_TOKEN in the environment.",
            file=sys.stderr,
        )
        return 2

    try:
        secret = decode_token(token)
    except Exception as exc:
        print(f"ERROR: invalid ORBI_PAIRING_TOKEN: {exc}", file=sys.stderr)
        return 2

    base_url = f"http://{args.host}:{args.port}"
    results: list[dict[str, Any]] = []

    try:
        health_status, health = request_json(
            base_url + "/health",
            args.timeout,
        )
        results.append(
            check(
                "health",
                health_status == 200 and health.get("status") == "ok",
                {
                    "status": health_status,
                    "body": health,
                },
            )
        )

        node_status, node = request_json(
            base_url + "/node",
            args.timeout,
        )
        results.append(
            check(
                "node_identity",
                (
                    node_status == 200
                    and node.get("node_id") == args.node_id
                    and node.get("abi") == "arm64-v8a"
                ),
                {
                    "status": node_status,
                    "body": node,
                },
            )
        )

        models_status, models = request_json(
            base_url + "/v1/models",
            args.timeout,
        )
        model_ids = [
            str(item.get("id"))
            for item in models.get("data", [])
            if isinstance(item, dict) and item.get("id")
        ]
        results.append(
            check(
                "model_visible",
                (
                    models_status == 200
                    and args.model_id in model_ids
                ),
                {
                    "status": models_status,
                    "model_ids": model_ids,
                },
            )
        )

        unsigned_status, unsigned_body = request_json(
            unsigned_chat_request(
                base_url=base_url,
                model_id=args.model_id,
                prompt=args.prompt,
            ),
            args.timeout,
        )
        unsigned_code = (
            unsigned_body.get("error", {}).get("code")
            if isinstance(unsigned_body.get("error"), dict)
            else None
        )
        results.append(
            check(
                "unsigned_chat_rejected",
                unsigned_status == 401,
                {
                    "status": unsigned_status,
                    "error_code": unsigned_code,
                },
            )
        )

        signed_request, ts, nonce = signed_chat_request(
            base_url=base_url,
            node_id=args.node_id,
            secret=secret,
            model_id=args.model_id,
            prompt=args.prompt,
        )
        signed_status, signed_body = request_json(
            signed_request,
            args.timeout,
        )
        content = (
            signed_body.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            if isinstance(signed_body.get("choices"), list)
            and signed_body.get("choices")
            else ""
        )
        results.append(
            check(
                "signed_chat_accepted",
                signed_status == 200 and bool(content),
                {
                    "status": signed_status,
                    "content": content,
                },
            )
        )

        replay_request, _, _ = signed_chat_request(
            base_url=base_url,
            node_id=args.node_id,
            secret=secret,
            model_id=args.model_id,
            prompt=args.prompt,
            timestamp_ms=ts,
            nonce=nonce,
        )
        replay_status, replay_body = request_json(
            replay_request,
            args.timeout,
        )
        replay_code = (
            replay_body.get("error", {}).get("code")
            if isinstance(replay_body.get("error"), dict)
            else None
        )
        results.append(
            check(
                "replay_rejected",
                (
                    replay_status == 401
                    and replay_code == "replay_detected"
                ),
                {
                    "status": replay_status,
                    "error_code": replay_code,
                },
            )
        )

        wrong_node = args.node_id + "-wrong"
        wrong_request, _, _ = signed_chat_request(
            base_url=base_url,
            node_id=wrong_node,
            secret=secret,
            model_id=args.model_id,
            prompt=args.prompt,
        )
        wrong_status, wrong_body = request_json(
            wrong_request,
            args.timeout,
        )
        wrong_code = (
            wrong_body.get("error", {}).get("code")
            if isinstance(wrong_body.get("error"), dict)
            else None
        )
        results.append(
            check(
                "wrong_node_rejected",
                (
                    wrong_status == 401
                    and wrong_code == "wrong_node"
                ),
                {
                    "status": wrong_status,
                    "error_code": wrong_code,
                },
            )
        )

    except (
        HTTPError,
        URLError,
        TimeoutError,
        OSError,
        json.JSONDecodeError,
    ) as exc:
        results.append(
            check(
                "transport",
                False,
                {
                    "error": f"{type(exc).__name__}: {exc}",
                },
            )
        )

    passed = sum(1 for item in results if item["pass"])
    failed = len(results) - passed

    evidence = {
        "schema_version": "0.1",
        "generated_at": now_iso(),
        "target": base_url,
        "node_id": args.node_id,
        "model_id": args.model_id,
        "checks": results,
        "pass_count": passed,
        "fail_count": failed,
        "overall_pass": failed == 0,
        "secret_included": False,
        "manual_checks_remaining": [
            "token rotation invalidates prior credential",
            "token revocation invalidates prior credential",
            "offline inference",
            "battery and thermal observations",
            "screen-off headless duration",
        ],
    }

    args.output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for item in results:
        state = "PASS" if item["pass"] else "FAIL"
        print(f"[{state}] {item['name']}")

    print(
        f"Evidence: {args.output} | PASS={passed} FAIL={failed}"
    )

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

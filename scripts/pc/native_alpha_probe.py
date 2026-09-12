#!/usr/bin/env python3
"""Physical validation probe for the consolidated ORBI Edge Node Native Alpha APK."""

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
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class Check:
    name: str
    passed: bool
    detail: str
    status_code: int | None = None
    elapsed_s: float | None = None


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def decode_token(token: str) -> bytes:
    padding = "=" * (-len(token) % 4)
    raw = base64.urlsafe_b64decode(token + padding)
    if len(raw) != 32:
        raise ValueError(f"pairing token decodes to {len(raw)} bytes; expected 32")
    return raw


def canonical(
    node_id: str,
    method: str,
    path: str,
    timestamp_ms: int,
    nonce: str,
    body: bytes,
) -> str:
    body_hash = hashlib.sha256(body).hexdigest()
    return "\n".join([
        "ORBI-AUTH-V1",
        node_id,
        method.upper(),
        path,
        str(timestamp_ms),
        nonce,
        body_hash,
    ])


def signed_headers(
    secret: bytes,
    node_id: str,
    method: str,
    path: str,
    body: bytes,
    *,
    timestamp_ms: int | None = None,
    nonce: str | None = None,
) -> dict[str, str]:
    timestamp_ms = timestamp_ms if timestamp_ms is not None else int(time.time() * 1000)
    nonce = nonce or secrets.token_hex(16)
    payload = canonical(node_id, method, path, timestamp_ms, nonce, body)
    signature = hmac.new(
        secret,
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {
        "Content-Type": "application/json; charset=utf-8",
        "X-ORBI-Node-ID": node_id,
        "X-ORBI-Timestamp": str(timestamp_ms),
        "X-ORBI-Nonce": nonce,
        "X-ORBI-Signature": signature,
    }


def request_json(
    method: str,
    url: str,
    timeout: float,
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, Any], float]:
    request = Request(
        url,
        data=body,
        method=method,
        headers=headers or {},
    )
    started = time.perf_counter()
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, payload, time.perf_counter() - started
    except HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return exc.code, payload, time.perf_counter() - started


def chat_body(prompt: str, max_tokens: int = 64) -> bytes:
    return json.dumps(
        {
            "model": "qwen3-1.7b-q4_k_m-node01",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "stream": False,
        },
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def add_check(
    checks: list[Check],
    name: str,
    expected: bool,
    detail: str,
    status_code: int | None = None,
    elapsed_s: float | None = None,
) -> None:
    checks.append(
        Check(
            name=name,
            passed=expected,
            detail=detail,
            status_code=status_code,
            elapsed_s=round(elapsed_s, 3) if elapsed_s is not None else None,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--node-id")
    parser.add_argument("--mode", choices=["preflight", "full"], default="preflight")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    base = f"http://{args.host}:{args.port}"
    checks: list[Check] = []
    captured: dict[str, Any] = {}

    for path, name in [
        ("/health", "health"),
        ("/node", "node"),
        ("/diagnostics", "diagnostics"),
        ("/v1/models", "models"),
    ]:
        try:
            code, payload, elapsed = request_json("GET", base + path, args.timeout)
            captured[name] = payload
            add_check(
                checks,
                name=f"GET {path}",
                expected=code == 200,
                detail=f"HTTP {code}",
                status_code=code,
                elapsed_s=elapsed,
            )
        except (URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
            add_check(
                checks,
                name=f"GET {path}",
                expected=False,
                detail=f"{type(exc).__name__}: {exc}",
            )

    node = captured.get("node", {})
    diagnostics = captured.get("diagnostics", {})
    reported_node_id = node.get("node_id") or diagnostics.get("node_id")

    if args.node_id and reported_node_id:
        add_check(
            checks,
            "node identity matches expected",
            str(reported_node_id) == args.node_id,
            f"reported={reported_node_id}",
        )

    if args.mode == "full":
        token_text = os.environ.get("ORBI_PAIRING_TOKEN")
        if not token_text:
            add_check(
                checks,
                "pairing token available",
                False,
                "ORBI_PAIRING_TOKEN is not set",
            )
        elif not args.node_id:
            add_check(
                checks,
                "expected node ID supplied",
                False,
                "--node-id is required in full mode",
            )
        else:
            try:
                secret = decode_token(token_text)
                add_check(checks, "pairing token format", True, "32-byte secret decoded")

                body = chat_body("Responde solo: ORBI NATIVE ALPHA OK", 64)
                path = "/v1/chat/completions"

                unsigned_code, unsigned_payload, unsigned_elapsed = request_json(
                    "POST",
                    base + path,
                    max(args.timeout, 90.0),
                    body=body,
                    headers={"Content-Type": "application/json; charset=utf-8"},
                )
                captured["unsigned_chat"] = unsigned_payload
                add_check(
                    checks,
                    "unsigned privileged chat rejected",
                    unsigned_code == 401,
                    f"HTTP {unsigned_code}",
                    unsigned_code,
                    unsigned_elapsed,
                )

                fixed_timestamp = int(time.time() * 1000)
                fixed_nonce = secrets.token_hex(16)
                headers = signed_headers(
                    secret,
                    args.node_id,
                    "POST",
                    path,
                    body,
                    timestamp_ms=fixed_timestamp,
                    nonce=fixed_nonce,
                )

                signed_code, signed_payload, signed_elapsed = request_json(
                    "POST",
                    base + path,
                    max(args.timeout, 120.0),
                    body=body,
                    headers=headers,
                )
                captured["signed_chat"] = signed_payload
                add_check(
                    checks,
                    "signed paired chat accepted",
                    signed_code == 200,
                    f"HTTP {signed_code}",
                    signed_code,
                    signed_elapsed,
                )

                replay_code, replay_payload, replay_elapsed = request_json(
                    "POST",
                    base + path,
                    max(args.timeout, 90.0),
                    body=body,
                    headers=headers,
                )
                captured["replay_chat"] = replay_payload
                replay_error = replay_payload.get("error", {})
                replay_code_name = (
                    replay_error.get("code")
                    if isinstance(replay_error, dict)
                    else None
                )
                add_check(
                    checks,
                    "replayed signed request rejected",
                    replay_code == 401 and replay_code_name == "replay_detected",
                    f"HTTP {replay_code}, error={replay_code_name}",
                    replay_code,
                    replay_elapsed,
                )
            except Exception as exc:
                add_check(
                    checks,
                    "full signed validation",
                    False,
                    f"{type(exc).__name__}: {exc}",
                )

    evidence = {
        "schema_version": "0.1",
        "test": "ORBI Edge Node Native Alpha Validation",
        "mode": args.mode,
        "started_at": now_iso(),
        "target": {
            "host": args.host,
            "port": args.port,
            "expected_node_id": args.node_id,
        },
        "checks": [asdict(check) for check in checks],
        "captured": captured,
        "secret_material_recorded": False,
    }

    passed = sum(1 for check in checks if check.passed)
    failed = len(checks) - passed
    evidence["summary"] = {
        "pass": passed,
        "fail": failed,
        "result": "PASS" if failed == 0 else "FAIL",
    }

    output = args.output
    if output is None:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output = Path(f"native-alpha-evidence-{stamp}.json")

    output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    for check in checks:
        prefix = "PASS" if check.passed else "FAIL"
        print(f"[{prefix}] {check.name}: {check.detail}")

    print(f"Evidence: {output}")
    print(f"PASS={passed} FAIL={failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

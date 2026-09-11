#!/usr/bin/env python3
"""30-minute native ORBI headless probe with N9 signed inference."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from orbi_signed_chat import (
    body_sha256,
    canonical_payload,
    decode_token,
    sign,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat()


def get_health(base_url: str, timeout: float) -> dict:
    started = time.monotonic()
    with urlopen(base_url + "/health", timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return {
        "ok": response.status == 200 and payload.get("status") == "ok",
        "status_code": response.status,
        "elapsed_s": round(time.monotonic() - started, 3),
        "payload": payload,
    }


def signed_chat(
    base_url: str,
    node_id: str,
    token: str,
    model_id: str,
    prompt: str,
    timeout: float,
) -> dict:
    secret = decode_token(token)
    if len(secret) != 32:
        raise ValueError(
            f"pairing token decoded to {len(secret)} bytes; expected 32"
        )

    path = "/v1/chat/completions"
    payload = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 96,
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
        node_id,
        "POST",
        path,
        timestamp_ms,
        nonce,
        digest,
    )
    signature = sign(secret, canonical)

    request = Request(
        base_url + path,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "X-ORBI-Node-ID": node_id,
            "X-ORBI-Timestamp": str(timestamp_ms),
            "X-ORBI-Nonce": nonce,
            "X-ORBI-Signature": signature,
        },
    )

    started = time.monotonic()
    with urlopen(request, timeout=timeout) as response:
        parsed = json.loads(response.read().decode("utf-8"))

    content = (
        parsed.get("choices", [{}])[0]
        .get("message", {})
        .get("content", "")
    )

    return {
        "ok": response.status == 200 and bool(content),
        "status_code": response.status,
        "elapsed_s": round(time.monotonic() - started, 3),
        "content": content,
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
    parser.add_argument("--interval-seconds", type=int, default=300)
    parser.add_argument("--checks", type=int, default=7)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("node01-native-headless-probe.json"),
    )
    parser.add_argument(
        "--prompt",
        default="Responde solo: ORBI NATIVE HEADLESS OK",
    )
    args = parser.parse_args()

    if args.checks < 5:
        print("ERROR: checks must be >= 5 for the post-20-minute gate.", file=sys.stderr)
        return 2
    if args.interval_seconds < 1:
        print("ERROR: interval-seconds must be >= 1.", file=sys.stderr)
        return 2

    token = os.environ.get("ORBI_PAIRING_TOKEN")
    if not token:
        print(
            "ERROR: set ORBI_PAIRING_TOKEN in the environment.",
            file=sys.stderr,
        )
        return 2

    base_url = f"http://{args.host}:{args.port}"
    evidence = {
        "schema_version": "0.1",
        "target": base_url,
        "node_id": args.node_id,
        "model_id": args.model_id,
        "started_at": now_iso(),
        "interval_seconds": args.interval_seconds,
        "checks_requested": args.checks,
        "health_checks": [],
        "inference_gate": None,
    }

    print("=== ORBI Edge Node Native Headless Probe ===")
    print(f"Target: {base_url}")
    print(f"Node ID: {args.node_id}")
    print(f"Checks: {args.checks}")
    print(f"Interval: {args.interval_seconds} seconds")
    print(
        "Expected duration: "
        f"{((args.checks - 1) * args.interval_seconds) / 60:.1f} minutes"
    )
    print()

    for index in range(1, args.checks + 1):
        timestamp = now_iso()
        try:
            result = get_health(base_url, args.timeout)
            result.update({
                "check": index,
                "timestamp": timestamp,
            })
        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ) as exc:
            result = {
                "check": index,
                "timestamp": timestamp,
                "ok": False,
                "error": f"{type(exc).__name__}: {exc}",
            }

        evidence["health_checks"].append(result)
        state = "PASS" if result.get("ok") else "FAIL"
        elapsed = result.get("elapsed_s", "?")
        print(
            f"[{state}] check={index}/{args.checks} "
            f"time={timestamp} elapsed={elapsed}s"
        )

        if index == 5:
            print()
            print("[INFERENCE GATE] signed native chat completion...")
            try:
                inference = signed_chat(
                    base_url=base_url,
                    node_id=args.node_id,
                    token=token,
                    model_id=args.model_id,
                    prompt=args.prompt,
                    timeout=args.timeout,
                )
            except (
                HTTPError,
                URLError,
                TimeoutError,
                OSError,
                ValueError,
                json.JSONDecodeError,
            ) as exc:
                inference = {
                    "ok": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }

            evidence["inference_gate"] = inference
            inf_state = "PASS" if inference.get("ok") else "FAIL"
            print(
                f"[INFERENCE {inf_state}] "
                f"elapsed={inference.get('elapsed_s', '?')}s"
            )
            if inference.get("content"):
                print(f"answer={inference['content']}")
            print()

        if index < args.checks:
            time.sleep(args.interval_seconds)

    evidence["finished_at"] = now_iso()
    evidence["pass_count"] = sum(
        1 for item in evidence["health_checks"]
        if item.get("ok")
    )
    evidence["fail_count"] = (
        len(evidence["health_checks"]) - evidence["pass_count"]
    )
    evidence["overall_pass"] = (
        evidence["fail_count"] == 0
        and bool(
            evidence.get("inference_gate")
            and evidence["inference_gate"].get("ok")
        )
    )

    args.output.write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print()
    print(f"Evidence written to: {args.output}")
    print(
        f"PASS={evidence['pass_count']} "
        f"FAIL={evidence['fail_count']} "
        f"INFERENCE={'PASS' if evidence.get('inference_gate', {}).get('ok') else 'FAIL'}"
    )

    return 0 if evidence["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

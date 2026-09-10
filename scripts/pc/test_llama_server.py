#!/usr/bin/env python3
"""Minimal ORBI Edge Mesh LAN test against llama-server.

Uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def get_json(url: str, timeout: float) -> tuple[int, object, float]:
    started = time.perf_counter()
    req = Request(url, method="GET")
    with urlopen(req, timeout=timeout) as response:
        body = response.read()
        elapsed = time.perf_counter() - started
        return response.status, json.loads(body.decode("utf-8")), elapsed


def post_json(url: str, payload: dict, timeout: float) -> tuple[int, object, float]:
    data = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urlopen(req, timeout=timeout) as response:
        body = response.read()
        elapsed = time.perf_counter() - started
        return response.status, json.loads(body.decode("utf-8")), elapsed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, help="Phone IPv4 address, e.g. 192.168.1.50")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument(
        "--prompt",
        default="Responde en una frase: ¿qué es ORBI Edge Mesh?",
    )
    args = parser.parse_args()

    base = f"http://{args.host}:{args.port}"
    print(f"ORBI Edge Mesh LAN Test -> {base}")

    try:
        status, models, elapsed = get_json(f"{base}/v1/models", args.timeout)
        print(f"[PASS] GET /v1/models -> HTTP {status} in {elapsed:.3f}s")
        print(json.dumps(models, ensure_ascii=False, indent=2))

        model_id = "local-model"
        if isinstance(models, dict):
            data = models.get("data")
            if isinstance(data, list) and data and isinstance(data[0], dict):
                model_id = str(data[0].get("id") or model_id)

        payload = {
            "model": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": args.prompt,
                }
            ],
            "stream": False,
            "temperature": 0.2
        }

        status, completion, elapsed = post_json(
            f"{base}/v1/chat/completions",
            payload,
            args.timeout,
        )
        print(f"[PASS] POST /v1/chat/completions -> HTTP {status} in {elapsed:.3f}s")
        print(json.dumps(completion, ensure_ascii=False, indent=2))
        return 0

    except HTTPError as exc:
        print(f"[FAIL] HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        try:
            print(exc.read().decode("utf-8", errors="replace"), file=sys.stderr)
        except Exception:
            pass
        return 2
    except URLError as exc:
        print(f"[FAIL] Network error: {exc.reason}", file=sys.stderr)
        return 3
    except TimeoutError:
        print("[FAIL] Request timed out", file=sys.stderr)
        return 4
    except Exception as exc:
        print(f"[FAIL] {type(exc).__name__}: {exc}", file=sys.stderr)
        return 5


if __name__ == "__main__":
    raise SystemExit(main())

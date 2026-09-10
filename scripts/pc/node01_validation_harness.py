#!/usr/bin/env python3
"""ORBI Edge Mesh — Node-01 Phase 0 validation harness."""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class CheckResult:
    name: str
    ok: bool
    elapsed_s: float
    detail: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_json(url: str, timeout: float) -> tuple[dict, float]:
    started = time.perf_counter()
    with urlopen(url, timeout=timeout) as response:
        body = response.read()
        elapsed = time.perf_counter() - started
        return json.loads(body.decode("utf-8")), elapsed


def post_json(url: str, payload: dict, timeout: float) -> tuple[dict, float]:
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    started = time.perf_counter()
    with urlopen(req, timeout=timeout) as response:
        raw = response.read()
        elapsed = time.perf_counter() - started
        return json.loads(raw.decode("utf-8")), elapsed


def run_check(name, fn) -> CheckResult:
    started = time.perf_counter()
    try:
        detail, elapsed = fn()
        return CheckResult(name, True, elapsed, detail)
    except (HTTPError, URLError, TimeoutError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        elapsed = time.perf_counter() - started
        return CheckResult(name, False, elapsed, f"{type(exc).__name__}: {exc}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--model", default="qwen3-1.7b-q4_k_m")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--prompt", default="Responde solo con la palabra ORBI.")
    parser.add_argument("--output", default="runtime/validation/node01-validation.json")
    args = parser.parse_args()

    base = f"http://{args.host}:{args.port}"
    results: list[CheckResult] = []

    results.append(run_check("models_endpoint", lambda: (
        json.dumps(get_json(base + "/v1/models", args.timeout)[0], ensure_ascii=False)[:300],
        get_json(base + "/v1/models", args.timeout)[1],
    )))

    def inference():
        payload = {
            "model": args.model,
            "messages": [{"role": "user", "content": args.prompt}],
            "stream": False,
            "temperature": 0.0,
        }
        response, elapsed = post_json(
            base + "/v1/chat/completions",
            payload,
            args.timeout,
        )
        choices = response.get("choices") or []
        if not choices:
            raise RuntimeError("response has no choices")
        content = str(choices[0].get("message", {}).get("content", "")).strip()
        if not content:
            raise RuntimeError("empty assistant response")
        return content[:300], elapsed

    results.append(run_check("chat_completion", inference))

    passed = sum(1 for result in results if result.ok)
    overall = passed == len(results)

    payload = {
        "schema_version": "0.1",
        "timestamp": now_iso(),
        "node_id": "node-01",
        "target": base,
        "model": args.model,
        "overall": "PASS" if overall else "FAIL",
        "checks": [asdict(result) for result in results],
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    for result in results:
        state = "PASS" if result.ok else "FAIL"
        print(f"[{state}] {result.name} elapsed={result.elapsed_s:.3f}s {result.detail}")

    print(f"[RESULT] {payload['overall']}")
    print(f"[EVIDENCE] {out}")
    return 0 if overall else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Periodic LAN probe for ORBI screen-off certification."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen


def probe(base: str, timeout: float) -> tuple[bool, str]:
    url = base.rstrip("/") + "/v1/models"
    req = Request(url, method="GET")
    started = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as response:
            elapsed = time.perf_counter() - started
            body = response.read().decode("utf-8", errors="replace")
            return True, f"HTTP {response.status} {elapsed:.3f}s {body[:200]}"
    except (URLError, HTTPError, TimeoutError) as exc:
        elapsed = time.perf_counter() - started
        return False, f"{type(exc).__name__} after {elapsed:.3f}s: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--interval", type=float, default=300.0)
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--timeout", type=float, default=10.0)
    args = parser.parse_args()

    base = f"http://{args.host}:{args.port}"
    failures = 0

    print(f"ORBI headless probe -> {base}")
    print(f"interval={args.interval}s count={args.count}")

    for i in range(1, args.count + 1):
        ok, detail = probe(base, args.timeout)
        stamp = datetime.now().isoformat(timespec="seconds")
        state = "PASS" if ok else "FAIL"
        print(f"[{stamp}] [{state}] probe {i}/{args.count}: {detail}")
        if not ok:
            failures += 1

        if i < args.count:
            time.sleep(args.interval)

    print(json.dumps({
        "probes": args.count,
        "failures": failures,
        "result": "PASS" if failures == 0 else "FAIL",
    }))
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())

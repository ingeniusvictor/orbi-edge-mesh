#!/usr/bin/env python3
"""Observe availability during a watchdog recovery experiment."""
from __future__ import annotations
import argparse
import time
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--count", type=int, default=24)
    args = parser.parse_args()
    url = f"http://{args.host}:{args.port}/v1/models"
    failures = 0
    recovered = False
    seen_failure = False
    for i in range(1, args.count + 1):
        stamp = datetime.now().isoformat(timespec="seconds")
        try:
            started = time.perf_counter()
            with urlopen(url, timeout=3.0) as response:
                response.read()
            elapsed = time.perf_counter() - started
            print(f"[{stamp}] PASS {i}/{args.count} {elapsed:.3f}s")
            if seen_failure:
                recovered = True
        except (HTTPError, URLError, TimeoutError) as exc:
            failures += 1
            seen_failure = True
            print(f"[{stamp}] FAIL {i}/{args.count}: {type(exc).__name__}: {exc}")
        if i < args.count:
            time.sleep(args.interval)
    print(f"summary failures={failures} seen_failure={seen_failure} recovered={recovered}")
    return 0 if (not seen_failure or recovered) else 2

if __name__ == "__main__":
    raise SystemExit(main())

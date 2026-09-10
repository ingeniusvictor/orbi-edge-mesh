#!/usr/bin/env python3
"""Print ORBI Edge Mesh observability summary."""

from __future__ import annotations

import argparse
import json

from observability.metrics import summarize_by_node
from observability.store import JsonlEventStore


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--store",
        default="runtime/observability/execution-events.jsonl",
    )
    args = parser.parse_args()

    store = JsonlEventStore(args.store)
    summary = summarize_by_node(store.read_all())
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

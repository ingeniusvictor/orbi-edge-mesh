#!/usr/bin/env python3
"""Phase 0 discovery source.

This is intentionally static/config-driven. It establishes the discovery
interface before mDNS/UDP discovery is introduced.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_node_urls(path: str) -> list[str]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    urls = payload.get("nodes", [])
    if not isinstance(urls, list):
        raise ValueError("'nodes' must be a list")
    return [str(url).rstrip("/") for url in urls]

#!/usr/bin/env python3
"""Heartbeat helpers for ORBI Edge Mesh."""

from __future__ import annotations

import json
from urllib.request import urlopen


def fetch_capability(base_url: str, timeout: float = 3.0) -> dict:
    url = base_url.rstrip("/") + "/orbi/v1/node"
    with urlopen(url, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status {response.status}")
        return json.loads(response.read().decode("utf-8"))

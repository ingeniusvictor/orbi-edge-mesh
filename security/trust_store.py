#!/usr/bin/env python3
"""Minimal local trust store."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any

class TrustStore:
    def __init__(self, path: str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": "0.1", "nodes": {}}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, payload: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    def pair_node(self, *, node_id: str, fingerprint: str, secret: str) -> None:
        payload = self.load()
        payload.setdefault("nodes", {})[node_id] = {"fingerprint": fingerprint, "secret": secret, "trusted": True}
        self.save(payload)

    def revoke_node(self, node_id: str) -> None:
        payload = self.load()
        node = payload.setdefault("nodes", {}).get(node_id)
        if node is not None:
            node["trusted"] = False
        self.save(payload)

    def get_secret(self, node_id: str) -> str | None:
        payload = self.load()
        node = payload.get("nodes", {}).get(node_id)
        if not node or node.get("trusted") is not True:
            return None
        secret = node.get("secret")
        return str(secret) if secret else None

#!/usr/bin/env python3
"""Replay protection helpers."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class NonceCache:
    ttl_seconds: float = 120.0
    _seen: dict[str, datetime] = field(default_factory=dict)

    def _purge(self) -> None:
        now = datetime.now(timezone.utc)
        stale = [nonce for nonce, seen_at in self._seen.items() if (now - seen_at).total_seconds() > self.ttl_seconds]
        for nonce in stale:
            self._seen.pop(nonce, None)

    def accept(self, nonce: str) -> bool:
        self._purge()
        if nonce in self._seen:
            return False
        self._seen[nonce] = datetime.now(timezone.utc)
        return True

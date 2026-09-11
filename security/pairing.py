#!/usr/bin/env python3
"""Local pairing primitives for ORBI Edge Mesh."""

from __future__ import annotations
import hashlib
import hmac
import secrets
from dataclasses import dataclass

@dataclass(frozen=True)
class PairingSecret:
    node_id: str
    token: str
    fingerprint: str

def generate_pairing_secret(node_id: str, token_bytes: int = 32) -> PairingSecret:
    token = secrets.token_urlsafe(token_bytes)
    fingerprint = hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]
    return PairingSecret(node_id=node_id, token=token, fingerprint=fingerprint)

def verify_token(candidate: str, expected: str) -> bool:
    return hmac.compare_digest(candidate.encode("utf-8"), expected.encode("utf-8"))

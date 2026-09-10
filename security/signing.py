#!/usr/bin/env python3
"""HMAC request signing for local ORBI control-plane calls."""

from __future__ import annotations
import hashlib
import hmac

def canonical_message(*, method: str, path: str, timestamp: str, nonce: str, body: bytes) -> bytes:
    digest = hashlib.sha256(body).hexdigest()
    return "\n".join([method.upper(), path, timestamp, nonce, digest]).encode("utf-8")

def sign_request(*, secret: str, method: str, path: str, timestamp: str, nonce: str, body: bytes) -> str:
    message = canonical_message(method=method, path=path, timestamp=timestamp, nonce=nonce, body=body)
    return hmac.new(secret.encode("utf-8"), message, hashlib.sha256).hexdigest()

def verify_signature(*, secret: str, provided_signature: str, method: str, path: str, timestamp: str, nonce: str, body: bytes) -> bool:
    expected = sign_request(secret=secret, method=method, path=path, timestamp=timestamp, nonce=nonce, body=body)
    return hmac.compare_digest(provided_signature, expected)

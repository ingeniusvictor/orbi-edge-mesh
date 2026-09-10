#!/usr/bin/env python3
"""Generate a local ORBI pairing token."""

from __future__ import annotations
import argparse
import json
from security.pairing import generate_pairing_secret

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", required=True)
    args = parser.parse_args()
    secret = generate_pairing_secret(args.node_id)
    print(json.dumps({"node_id": secret.node_id, "token": secret.token, "fingerprint": secret.fingerprint}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

import base64
import hashlib
import hmac
import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "pc" / "orbi_signed_chat.py"
spec = importlib.util.spec_from_file_location("orbi_signed_chat", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class SignedChatTests(unittest.TestCase):
    def test_urlsafe_token_without_padding_decodes(self):
        raw = bytes(range(32))
        token = base64.urlsafe_b64encode(raw).decode().rstrip("=")
        self.assertEqual(raw, mod.decode_token(token))

    def test_canonical_signature_matches_reference_hmac(self):
        secret = bytes(range(32))
        body = b'{"hello":"orbi"}'
        digest = hashlib.sha256(body).hexdigest()
        canonical = mod.canonical_payload(
            "node-01",
            "POST",
            "/v1/chat/completions",
            123456789,
            "0123456789abcdef",
            digest,
        )

        expected = hmac.new(
            secret,
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        self.assertEqual(expected, mod.sign(secret, canonical))


if __name__ == "__main__":
    unittest.main()

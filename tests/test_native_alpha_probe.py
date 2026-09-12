import base64
import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "pc" / "native_alpha_probe.py"
spec = importlib.util.spec_from_file_location("native_alpha_probe", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class NativeAlphaProbeTests(unittest.TestCase):
    def test_signed_headers_are_stable_for_fixed_inputs(self):
        secret = bytes(range(32))
        body = mod.chat_body("hola", 12)
        first = mod.signed_headers(
            secret,
            "node-01",
            "POST",
            "/v1/chat/completions",
            body,
            timestamp_ms=123456789,
            nonce="0123456789abcdef",
        )
        second = mod.signed_headers(
            secret,
            "node-01",
            "POST",
            "/v1/chat/completions",
            body,
            timestamp_ms=123456789,
            nonce="0123456789abcdef",
        )
        self.assertEqual(first, second)
        self.assertEqual(64, len(first["X-ORBI-Signature"]))

    def test_decode_urlsafe_token(self):
        raw = bytes(range(32))
        token = base64.urlsafe_b64encode(raw).decode().rstrip("=")
        self.assertEqual(raw, mod.decode_token(token))


if __name__ == "__main__":
    unittest.main()

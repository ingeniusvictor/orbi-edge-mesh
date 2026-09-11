import tempfile
import unittest

from security.pairing import generate_pairing_secret, verify_token
from security.replay import NonceCache
from security.signing import sign_request, verify_signature
from security.trust_store import TrustStore


class PairingTests(unittest.TestCase):
    def test_generated_token_verifies(self):
        secret = generate_pairing_secret('node-01')
        self.assertTrue(verify_token(secret.token, secret.token))
        self.assertFalse(verify_token('wrong', secret.token))

    def test_signature_roundtrip(self):
        body = b'hello'
        signature = sign_request(
            secret='abc123',
            method='POST',
            path='/orbi/v1/control',
            timestamp='2026-09-10T19:00:00Z',
            nonce='n-1',
            body=body,
        )
        self.assertTrue(verify_signature(
            secret='abc123',
            provided_signature=signature,
            method='POST',
            path='/orbi/v1/control',
            timestamp='2026-09-10T19:00:00Z',
            nonce='n-1',
            body=body,
        ))

    def test_replay_nonce_rejected(self):
        cache = NonceCache(ttl_seconds=60)
        self.assertTrue(cache.accept('nonce-1'))
        self.assertFalse(cache.accept('nonce-1'))

    def test_trust_store_pair_and_revoke(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TrustStore(f'{tmp}/trust.json')
            store.pair_node(node_id='node-01', fingerprint='abcd', secret='secret')
            self.assertEqual(store.get_secret('node-01'), 'secret')
            store.revoke_node('node-01')
            self.assertIsNone(store.get_secret('node-01'))


if __name__ == '__main__':
    unittest.main()

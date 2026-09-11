package com.orbi.edgenode

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class OrbiAuthTest {
    @Test
    fun signaturesAreDeterministicAndVerifiedConstantTime() {
        val secret = ByteArray(32) { it.toByte() }
        val bodyHash = OrbiAuth.bodySha256("{\"hello\":\"orbi\"}".toByteArray())
        val canonical = OrbiAuth.canonicalPayload(
            nodeId = "node-01",
            method = "POST",
            path = "/v1/chat/completions",
            timestampMs = 123456789L,
            nonce = "0123456789abcdef",
            bodySha256 = bodyHash,
        )

        val first = OrbiAuth.sign(secret, canonical)
        val second = OrbiAuth.sign(secret, canonical)

        assertTrue(OrbiAuth.constantTimeEquals(first, second))
        assertFalse(OrbiAuth.constantTimeEquals(first, "0".repeat(64)))
    }
}

package com.orbi.edgenode

import java.security.MessageDigest
import javax.crypto.Mac
import javax.crypto.spec.SecretKeySpec

object OrbiAuth {
    fun bodySha256(body: ByteArray): String =
        MessageDigest.getInstance("SHA-256")
            .digest(body)
            .joinToString("") { "%02x".format(it) }

    fun canonicalPayload(
        nodeId: String,
        method: String,
        path: String,
        timestampMs: Long,
        nonce: String,
        bodySha256: String,
    ): String = listOf(
        "ORBI-AUTH-V1",
        nodeId,
        method.uppercase(),
        path,
        timestampMs.toString(),
        nonce,
        bodySha256.lowercase(),
    ).joinToString("\n")

    fun sign(
        secret: ByteArray,
        canonicalPayload: String,
    ): String {
        val mac = Mac.getInstance("HmacSHA256")
        mac.init(SecretKeySpec(secret, "HmacSHA256"))
        return mac.doFinal(canonicalPayload.toByteArray(Charsets.UTF_8))
            .joinToString("") { "%02x".format(it) }
    }

    fun constantTimeEquals(
        expectedHex: String,
        actualHex: String,
    ): Boolean {
        val expected = expectedHex.lowercase().toByteArray(Charsets.US_ASCII)
        val actual = actualHex.lowercase().toByteArray(Charsets.US_ASCII)
        return MessageDigest.isEqual(expected, actual)
    }
}

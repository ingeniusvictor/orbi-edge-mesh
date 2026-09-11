package com.orbi.edgenode

import android.content.Context
import java.security.SecureRandom
import java.util.Base64
import java.util.UUID

class PairingManager(
    context: Context,
) {
    private val prefs = context.applicationContext.getSharedPreferences(
        "orbi_edge_node_trust",
        Context.MODE_PRIVATE,
    )

    private val nonceLock = Any()
    private val usedNonces = linkedMapOf<String, Long>()

    val nodeId: String
        get() {
            val existing = prefs.getString(KEY_NODE_ID, null)
            if (!existing.isNullOrBlank()) return existing

            val created = UUID.randomUUID().toString()
            prefs.edit().putString(KEY_NODE_ID, created).commit()
            return created
        }

    fun hasPairingSecret(): Boolean =
        !prefs.getString(KEY_PAIRING_SECRET, null).isNullOrBlank()

    fun currentPairingToken(): String? =
        prefs.getString(KEY_PAIRING_SECRET, null)

    fun rotatePairingToken(): String {
        val secret = ByteArray(32)
        SecureRandom().nextBytes(secret)

        val token = Base64.getUrlEncoder()
            .withoutPadding()
            .encodeToString(secret)

        prefs.edit()
            .putString(KEY_PAIRING_SECRET, token)
            .apply()

        synchronized(nonceLock) {
            usedNonces.clear()
        }

        return token
    }

    fun revokePairing() {
        prefs.edit().remove(KEY_PAIRING_SECRET).apply()
        synchronized(nonceLock) {
            usedNonces.clear()
        }
    }

    fun verify(
        method: String,
        path: String,
        body: ByteArray,
        headers: Map<String, String>,
        nowMs: Long = System.currentTimeMillis(),
    ): AuthVerification {
        val token = currentPairingToken()
            ?: return denied("not_paired", "Node has no active pairing secret.")

        val targetNode = headers["x-orbi-node-id"]
            ?: return denied("missing_node_id", "X-ORBI-Node-ID is required.")

        if (targetNode != nodeId) {
            return denied("wrong_node", "Signed request targets a different node.")
        }

        val timestampRaw = headers["x-orbi-timestamp"]
            ?: return denied("missing_timestamp", "X-ORBI-Timestamp is required.")
        val timestamp = timestampRaw.toLongOrNull()
            ?: return denied("invalid_timestamp", "Timestamp must be epoch milliseconds.")

        if (kotlin.math.abs(nowMs - timestamp) > MAX_CLOCK_SKEW_MS) {
            return denied("stale_request", "Signed request is outside the accepted clock window.")
        }

        val nonce = headers["x-orbi-nonce"]
            ?.takeIf { it.length in 16..128 }
            ?: return denied("invalid_nonce", "X-ORBI-Nonce is missing or invalid.")

        val signature = headers["x-orbi-signature"]
            ?.takeIf { it.length == 64 }
            ?: return denied("invalid_signature", "X-ORBI-Signature is missing or invalid.")

        synchronized(nonceLock) {
            pruneNonces(nowMs)
            if (usedNonces.containsKey(nonce)) {
                return denied("replay_detected", "Nonce has already been used.")
            }
        }

        val secret = try {
            Base64.getUrlDecoder().decode(token)
        } catch (_: Throwable) {
            return denied("trust_store_error", "Stored pairing secret is invalid.")
        }

        val bodyHash = OrbiAuth.bodySha256(body)
        val canonical = OrbiAuth.canonicalPayload(
            nodeId = nodeId,
            method = method,
            path = path,
            timestampMs = timestamp,
            nonce = nonce,
            bodySha256 = bodyHash,
        )
        val expected = OrbiAuth.sign(secret, canonical)

        if (!OrbiAuth.constantTimeEquals(expected, signature)) {
            return denied("signature_mismatch", "HMAC signature verification failed.")
        }

        synchronized(nonceLock) {
            usedNonces[nonce] = nowMs
            pruneNonces(nowMs)
        }

        return AuthVerification(
            allowed = true,
            code = "authorized",
            message = "Signed paired request accepted.",
        )
    }

    private fun pruneNonces(nowMs: Long) {
        val iterator = usedNonces.entries.iterator()
        while (iterator.hasNext()) {
            val entry = iterator.next()
            if (nowMs - entry.value > NONCE_RETENTION_MS) {
                iterator.remove()
            }
        }

        while (usedNonces.size > MAX_NONCES) {
            val first = usedNonces.entries.firstOrNull() ?: break
            usedNonces.remove(first.key)
        }
    }

    private fun denied(
        code: String,
        message: String,
    ) = AuthVerification(
        allowed = false,
        code = code,
        message = message,
    )

    companion object {
        private const val KEY_NODE_ID = "node_id"
        private const val KEY_PAIRING_SECRET = "pairing_secret"

        private const val MAX_CLOCK_SKEW_MS = 120_000L
        private const val NONCE_RETENTION_MS = 5 * 60_000L
        private const val MAX_NONCES = 1_000
    }
}

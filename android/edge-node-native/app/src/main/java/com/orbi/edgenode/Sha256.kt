package com.orbi.edgenode

import java.io.InputStream
import java.security.MessageDigest

object Sha256 {
    fun digest(input: InputStream): String {
        val md = MessageDigest.getInstance("SHA-256")
        val buffer = ByteArray(DEFAULT_BUFFER_SIZE)

        while (true) {
            val read = input.read(buffer)
            if (read < 0) break
            if (read > 0) md.update(buffer, 0, read)
        }

        return md.digest().joinToString("") { "%02x".format(it) }
    }
}

package com.orbi.edgenode

import org.junit.Assert.assertEquals
import org.junit.Test
import java.io.ByteArrayInputStream

class Sha256Test {
    @Test
    fun hashesKnownPayload() {
        val input = ByteArrayInputStream("ORBI".toByteArray())
        assertEquals(
            "4e963f8d2a6ce4bf656a57374419d3e37f3ebde9acd32242977152fc6893ad09",
            Sha256.digest(input),
        )
    }
}

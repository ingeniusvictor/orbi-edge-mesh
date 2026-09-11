package com.orbi.edgenode

import org.junit.Assert.assertEquals
import org.junit.Test
import java.io.ByteArrayInputStream

class Sha256Test {
    @Test
    fun hashesKnownPayload() {
        val input = ByteArrayInputStream("ORBI".toByteArray())
        assertEquals(
            "d8c76c9888b28be2ef30a0fdd704ec435aa6955e854e4cb95f6010370d41d597",
            Sha256.digest(input),
        )
    }
}

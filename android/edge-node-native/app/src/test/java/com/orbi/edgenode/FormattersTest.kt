package com.orbi.edgenode

import org.junit.Assert.assertEquals
import org.junit.Test

class FormattersTest {
    @Test
    fun nullBytesAreUnknown() {
        assertEquals("UNKNOWN", Formatters.bytes(null))
    }

    @Test
    fun gibibytesAreFormatted() {
        assertEquals("1.00 GiB", Formatters.bytes(1024L * 1024L * 1024L))
    }

    @Test
    fun nullableBooleanIsExplicit() {
        assertEquals("YES", Formatters.bool(true))
        assertEquals("NO", Formatters.bool(false))
        assertEquals("UNKNOWN", Formatters.bool(null))
    }
}

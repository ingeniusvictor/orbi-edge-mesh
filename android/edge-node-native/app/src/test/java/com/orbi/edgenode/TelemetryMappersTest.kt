package com.orbi.edgenode

import android.os.BatteryManager
import android.os.PowerManager
import org.junit.Assert.assertEquals
import org.junit.Test

class TelemetryMappersTest {
    @Test
    fun batteryPlugMapsUsb() {
        assertEquals(
            "USB",
            TelemetryMappers.batterySource(BatteryManager.BATTERY_PLUGGED_USB),
        )
    }

    @Test
    fun thermalCriticalIsExplicit() {
        assertEquals(
            "CRITICAL",
            TelemetryMappers.thermalStatus(PowerManager.THERMAL_STATUS_CRITICAL),
        )
    }

    @Test
    fun nullTelemetryStaysUnknown() {
        assertEquals(null, TelemetryMappers.thermalStatus(null))
        assertEquals(null, TelemetryMappers.batterySource(null))
    }
}

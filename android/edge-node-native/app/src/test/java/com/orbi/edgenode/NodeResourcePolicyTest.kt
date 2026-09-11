package com.orbi.edgenode

import org.junit.Assert.assertEquals
import org.junit.Test

class NodeResourcePolicyTest {
    private fun health(
        battery: Int? = 80,
        charging: Boolean? = false,
        thermal: String? = "NONE",
    ) = NodeHealthSnapshot(
        memory = MemorySnapshot(null, null, null),
        storage = StorageSnapshot(null, null),
        battery = BatterySnapshot(battery, charging, null),
        network = NetworkSnapshot(null, emptyList(), emptyList()),
        thermal = ThermalSnapshot(thermal, null),
    )

    @Test
    fun healthySignalsAllow() {
        assertEquals(
            ResourceAction.ALLOW,
            NodeResourcePolicy.evaluate(health()).action,
        )
    }

    @Test
    fun severeThermalBlocks() {
        assertEquals(
            ResourceAction.BLOCK,
            NodeResourcePolicy.evaluate(health(thermal = "SEVERE")).action,
        )
    }

    @Test
    fun criticalLowBatteryBlocks() {
        assertEquals(
            ResourceAction.BLOCK,
            NodeResourcePolicy.evaluate(
                health(battery = 8, charging = false)
            ).action,
        )
    }

    @Test
    fun moderateThermalDegrades() {
        assertEquals(
            ResourceAction.DEGRADE,
            NodeResourcePolicy.evaluate(
                health(thermal = "MODERATE")
            ).action,
        )
    }

    @Test
    fun lowBatteryDegrades() {
        assertEquals(
            ResourceAction.DEGRADE,
            NodeResourcePolicy.evaluate(
                health(battery = 18, charging = false)
            ).action,
        )
    }

    @Test
    fun missingSafetyTelemetryBlocks() {
        assertEquals(
            ResourceAction.BLOCK,
            NodeResourcePolicy.evaluate(
                health(battery = null, charging = null, thermal = null)
            ).action,
        )
    }
}

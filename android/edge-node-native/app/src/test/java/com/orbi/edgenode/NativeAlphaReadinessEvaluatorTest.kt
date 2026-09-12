package com.orbi.edgenode

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class NativeAlphaReadinessEvaluatorTest {
    private val telemetry = NodeHealthSnapshot(
        memory = MemorySnapshot(
            totalBytes = 12L,
            availableBytes = 6L,
            lowMemory = false,
        ),
        storage = StorageSnapshot(
            totalBytes = 512L,
            availableBytes = 200L,
        ),
        battery = BatterySnapshot(
            percent = 80,
            charging = false,
            source = "NOT_PLUGGED",
        ),
        network = NetworkSnapshot(
            connected = true,
            transports = listOf("WIFI"),
            addresses = listOf("192.168.1.7"),
        ),
        thermal = ThermalSnapshot(
            status = "NONE",
            rawStatus = 0,
        ),
    )

    @Test
    fun missingModelPathDoesNotClaimN3Readiness() {
        val result = NativeAlphaReadinessEvaluator.evaluate(
            telemetry = telemetry,
            nativeStatus = "JNI BRIDGE READY",
            llamaSystemInfo = "llama linked",
            modelPath = null,
            apiRunning = false,
            supervisor = SupervisorSnapshot(false, 0, false, "NOT STARTED"),
            resourceDecision = ResourceDecision(
                ResourceAction.ALLOW,
                "ok",
            ),
            paired = false,
        )

        assertTrue(result.n0Bridge)
        assertTrue(result.n1Telemetry)
        assertTrue(result.n2LlamaLink)
        assertFalse(result.n3ModelImported)
        assertFalse(result.n5ApiRunning)
        assertFalse(result.n9Paired)
    }
}

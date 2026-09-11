package com.orbi.edgenode

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val snapshot = DeviceProfiler.snapshot()
        val nativeStatus = NativeBridge.status()
        val telemetry = NodeTelemetryProvider(applicationContext).snapshot()

        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    NodeStatusScreen(snapshot, nativeStatus, telemetry)
                }
            }
        }
    }
}

@Composable
private fun NodeStatusScreen(
    snapshot: DeviceSnapshot,
    nativeStatus: String,
    telemetry: NodeHealthSnapshot,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        Text(
            text = "ORBI Edge Node",
            style = MaterialTheme.typography.headlineMedium,
        )

        Text("Research build: ${BuildConfig.VERSION_NAME}")
        Text("Manufacturer: ${snapshot.manufacturer}")
        Text("Device: ${snapshot.model} (${snapshot.device})")
        Text("Android: ${snapshot.androidVersion} / API ${snapshot.apiLevel}")
        Text("ABI: ${snapshot.abi}")
        Text("CPU logical processors: ${snapshot.availableProcessors}")
        Text("Native runtime: $nativeStatus")
        Text("AI runtime: NOT LOADED")

        HorizontalDivider()
        Text("Native telemetry preview", style = MaterialTheme.typography.titleMedium)

        Text("RAM total: ${Formatters.bytes(telemetry.memory.totalBytes)}")
        Text("RAM available: ${Formatters.bytes(telemetry.memory.availableBytes)}")
        Text("Low-memory flag: ${Formatters.bool(telemetry.memory.lowMemory)}")

        Text("Storage total: ${Formatters.bytes(telemetry.storage.totalBytes)}")
        Text("Storage available: ${Formatters.bytes(telemetry.storage.availableBytes)}")

        Text("Battery: ${Formatters.percent(telemetry.battery.percent)}")
        Text("Charging: ${Formatters.bool(telemetry.battery.charging)}")
        Text("Charge source: ${telemetry.battery.source ?: "UNKNOWN"}")

        Text("Network connected: ${Formatters.bool(telemetry.network.connected)}")
        Text("Transports: ${Formatters.list(telemetry.network.transports)}")
        Text("Addresses: ${Formatters.list(telemetry.network.addresses)}")

        Text("Android thermal status: ${telemetry.thermal.status ?: "UNKNOWN"}")
        Text("Thermal raw status: ${telemetry.thermal.rawStatus?.toString() ?: "UNKNOWN"}")

        Text(
            "N1 telemetry is experimental until physically validated on Node-01.",
            style = MaterialTheme.typography.bodySmall,
        )
    }
}

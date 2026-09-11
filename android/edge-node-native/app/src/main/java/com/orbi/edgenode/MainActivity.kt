package com.orbi.edgenode

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val snapshot = DeviceProfiler.snapshot()
        val nativeStatus = NativeBridge.status()
        val llamaSystemInfo = NativeBridge.llamaSystemInfo()
        val telemetry = NodeTelemetryProvider(applicationContext).snapshot()

        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    NodeStatusScreen(snapshot, nativeStatus, llamaSystemInfo, telemetry)
                }
            }
        }
    }
}

@Composable
private fun NodeStatusScreen(
    snapshot: DeviceSnapshot,
    nativeStatus: String,
    llamaSystemInfo: String,
    telemetry: NodeHealthSnapshot,
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var modelStatus by remember { mutableStateOf("NOT IMPORTED") }

    val picker = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument(),
    ) { uri ->
        if (uri == null) {
            modelStatus = "SELECTION CANCELLED"
        } else {
            modelStatus = "IMPORTING + VERIFYING SHA-256..."
            scope.launch {
                val result = withContext(Dispatchers.IO) {
                    ModelImporter(context.applicationContext)
                        .importFromUri(uri, ReferenceModels.qwen3Node01)
                }

                modelStatus = when (result) {
                    is ModelImportResult.Success ->
                        "VALIDATED: ${result.bytes} bytes | SHA-256 MATCH"
                    is ModelImportResult.Failure ->
                        "${result.code}: ${result.message}"
                }
            }
        }
    }

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
        Text("Device: ${snapshot.model}")
        Text("Android: ${snapshot.androidVersion}")
        Text("ABI: ${snapshot.abi}")
        Text("Native runtime: $nativeStatus")
        Text("llama.cpp link: READY")
        Text("llama.cpp info: $llamaSystemInfo")
        Text("AI model runtime: NOT LOADED")

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

        HorizontalDivider()
        Text("Reference model", style = MaterialTheme.typography.titleMedium)
        Text(ReferenceModels.qwen3Node01.displayName)
        Text("Expected file: ${ReferenceModels.qwen3Node01.fileName}")
        Text("Import state: $modelStatus")

        Button(
            onClick = { picker.launch(arrayOf("*/*")) },
        ) {
            Text("Select and validate GGUF")
        }

        Text(
            "Research preview: N0/N1/N2/N3 gates remain physically uncertified until tested on Node-01.",
            style = MaterialTheme.typography.bodySmall,
        )
    }
}

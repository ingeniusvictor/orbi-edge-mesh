package com.orbi.edgenode

import android.content.Intent
import android.os.Build
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
    remember {
        EdgeNodeRuntime.initialize(context.applicationContext)
        Unit
    }

    var serviceStatus by remember { mutableStateOf("STOPPED") }
    var apiStatus by remember { mutableStateOf("STOPPED") }
    var modelStatus by remember { mutableStateOf("NOT IMPORTED") }
    var modelPath by remember { mutableStateOf<String?>(null) }
    var runtimeStatus by remember { mutableStateOf("MODEL NOT LOADED") }
    var inferenceStatus by remember { mutableStateOf("NOT RUN") }
    var responseText by remember { mutableStateOf("") }

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

                when (result) {
                    is ModelImportResult.Success -> {
                        modelPath = result.filePath
                        modelStatus = "VALIDATED: ${result.bytes} bytes | SHA-256 MATCH"
                    }
                    is ModelImportResult.Failure -> {
                        modelPath = null
                        modelStatus = "${result.code}: ${result.message}"
                    }
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
        Text("Runtime state: $runtimeStatus")
        Text("Inference state: $inferenceStatus")

        Button(
            onClick = { picker.launch(arrayOf("*/*")) },
        ) {
            Text("1. Select and validate GGUF")
        }

        Button(
            enabled = modelPath != null,
            onClick = {
                val path = modelPath ?: return@Button
                runtimeStatus = "LOADING MODEL..."
                scope.launch {
                    runtimeStatus = withContext(Dispatchers.IO) {
                        NativeBridge.loadModel(
                            modelPath = path,
                            contextSize = 4096,
                            threads = 4,
                        )
                    }
                }
            },
        ) {
            Text("2. Load Qwen into native runtime")
        }

        Button(
            enabled = modelPath != null,
            onClick = {
                inferenceStatus = "GENERATING..."
                responseText = ""
                scope.launch {
                    val response = withContext(Dispatchers.IO) {
                        NativeBridge.generate(
                            prompt = "Responde en español y en una sola frase: ¿qué es una red local de inteligencia artificial?",
                            maxTokens = 96,
                        )
                    }
                    responseText = response
                    inferenceStatus = if (response.startsWith("ERROR:")) {
                        "FAIL"
                    } else {
                        "PASS / REVIEW RESPONSE"
                    }
                }
            },
        ) {
            Text("3. Run native inference test")
        }

        Button(
            onClick = {
                scope.launch {
                    runtimeStatus = withContext(Dispatchers.IO) {
                        NativeBridge.unloadModel()
                    }
                }
            },
        ) {
            Text("Unload model")
        }

        HorizontalDivider()
        Text("Trusted-LAN API", style = MaterialTheme.typography.titleMedium)
        Text("API state: $apiStatus")
        Text(
            "Endpoint candidate: " +
                (telemetry.network.addresses.firstOrNull { !it.contains(":") }
                    ?.let { "http://$it:8080" }
                    ?: "IPv4 unavailable")
        )
        Text(
            "Research warning: LAN-only, no public Internet exposure, no port forwarding.",
            style = MaterialTheme.typography.bodySmall,
        )

        Button(
            onClick = { apiStatus = EdgeNodeRuntime.startApi() },
        ) {
            Text("Start local API")
        }

        Button(
            onClick = { apiStatus = EdgeNodeRuntime.stopApi() },
        ) {
            Text("Stop local API")
        }

        HorizontalDivider()
        Text("Headless service", style = MaterialTheme.typography.titleMedium)
        Text("Service state: $serviceStatus")
        Text(
            "The foreground service owns a PARTIAL_WAKE_LOCK and keeps the research node eligible to run with the display off.",
            style = MaterialTheme.typography.bodySmall,
        )

        Button(
            onClick = {
                val intent = Intent(context, EdgeNodeService::class.java)
                    .setAction(EdgeNodeService.ACTION_START)
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    context.startForegroundService(intent)
                } else {
                    context.startService(intent)
                }
                serviceStatus = "START REQUESTED"
            },
        ) {
            Text("Start headless node service")
        }

        Button(
            onClick = {
                context.stopService(Intent(context, EdgeNodeService::class.java))
                serviceStatus = "STOP REQUESTED"
                apiStatus = "STOPPED BY SERVICE"
            },
        ) {
            Text("Stop headless node service")
        }

        if (responseText.isNotBlank()) {
            HorizontalDivider()
            Text("Native Qwen response", style = MaterialTheme.typography.titleMedium)
            Text(responseText)
        }

        Text(
            "N6 is a headless research preview. 30-minute screen-off parity remains physically uncertified until tested on Node-01.",
            style = MaterialTheme.typography.bodySmall,
        )
    }
}

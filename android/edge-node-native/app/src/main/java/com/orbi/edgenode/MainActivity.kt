package com.orbi.edgenode

import android.Manifest
import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        if (
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU &&
            checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) {
            requestPermissions(
                arrayOf(Manifest.permission.POST_NOTIFICATIONS),
                REQUEST_NOTIFICATIONS_CODE,
            )
        }

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

    companion object {
        private const val REQUEST_NOTIFICATIONS_CODE = 6002
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
    val configStore = remember {
        EdgeNodeRuntime.initialize(context.applicationContext)
        NodeConfigStore(context.applicationContext)
    }
    val pairingManager = remember {
        PairingManager(context.applicationContext)
    }

    var currentTelemetry by remember { mutableStateOf(telemetry) }
    var modelLoaded by remember { mutableStateOf(NativeBridge.isModelLoaded()) }
    var supervisorSnapshot by remember { mutableStateOf(SupervisorMonitor.current) }
    var resourceDecision by remember {
        mutableStateOf(NodeResourcePolicy.evaluate(currentTelemetry))
    }

    LaunchedEffect(Unit) {
        while (true) {
            currentTelemetry = NodeTelemetryProvider(
                context.applicationContext
            ).snapshot()
            modelLoaded = NativeBridge.isModelLoaded()
            supervisorSnapshot = SupervisorMonitor.current
            resourceDecision = NodeResourcePolicy.evaluate(currentTelemetry)
            delay(1_000)
        }
    }

    var pairingToken by remember { mutableStateOf<String?>(null) }
    var pairingCopyStatus by remember { mutableStateOf("NOT COPIED") }
    var pairingStatus by remember {
        mutableStateOf(
            if (pairingManager.hasPairingSecret()) "PAIRED" else "NOT PAIRED"
        )
    }

    var serviceStatus by remember { mutableStateOf("STOPPED") }
    var apiStatus by remember { mutableStateOf("STOPPED") }
    var modelPath by remember { mutableStateOf(configStore.modelPath()) }
    var modelStatus by remember {
        mutableStateOf(
            if (modelPath != null) "PERSISTED VERIFIED IMPORT" else "NOT IMPORTED"
        )
    }
    var runtimeStatus by remember {
        mutableStateOf(if (modelLoaded) "MODEL LOADED" else "MODEL NOT LOADED")
    }
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
                        configStore.setValidatedModelPath(result.filePath)
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

    val readiness = NativeAlphaReadinessEvaluator.evaluate(
        telemetry = currentTelemetry,
        nativeStatus = nativeStatus,
        llamaSystemInfo = llamaSystemInfo,
        modelPath = modelPath,
        modelLoaded = modelLoaded,
        apiRunning = EdgeNodeRuntime.isApiRunning(),
        supervisor = supervisorSnapshot,
        resourceDecision = resourceDecision,
        paired = pairingManager.hasPairingSecret(),
    )

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
        Text("Native Alpha readiness", style = MaterialTheme.typography.titleMedium)
        Text("READINESS ≠ PHYSICAL PASS", style = MaterialTheme.typography.bodySmall)
        Text("N0 JNI bridge: ${if (readiness.n0Bridge) "READY" else "WAIT"}")
        Text("N1 telemetry: ${if (readiness.n1Telemetry) "READY" else "WAIT"}")
        Text("N2 llama.cpp link: ${if (readiness.n2LlamaLink) "READY" else "WAIT"}")
        Text("N3 verified model import: ${if (readiness.n3ModelImported) "READY" else "WAIT"}")
        Text("N4 model loaded: ${if (readiness.n4ModelLoaded) "READY" else "WAIT"}")
        Text("N5 local API: ${if (readiness.n5ApiRunning) "READY" else "WAIT"}")
        Text("N6 headless service evidence: ${if (readiness.n6HeadlessServiceEvidence) "READY" else "WAIT"}")
        Text("N7 bounded supervisor: ${if (readiness.n7SupervisorRunning) "READY" else "WAIT"}")
        Text("N8 resource policy: ${readiness.n8ResourceAction}")
        Text("N9 paired trust: ${if (readiness.n9Paired) "READY" else "WAIT"}")

        HorizontalDivider()
        Text("Native telemetry preview", style = MaterialTheme.typography.titleMedium)

        Text("RAM total: ${Formatters.bytes(currentTelemetry.memory.totalBytes)}")
        Text("RAM available: ${Formatters.bytes(currentTelemetry.memory.availableBytes)}")
        Text("Low-memory flag: ${Formatters.bool(currentTelemetry.memory.lowMemory)}")

        Text("Storage total: ${Formatters.bytes(currentTelemetry.storage.totalBytes)}")
        Text("Storage available: ${Formatters.bytes(currentTelemetry.storage.availableBytes)}")

        Text("Battery: ${Formatters.percent(currentTelemetry.battery.percent)}")
        Text("Charging: ${Formatters.bool(currentTelemetry.battery.charging)}")
        Text("Charge source: ${currentTelemetry.battery.source ?: "UNKNOWN"}")

        Text("Network connected: ${Formatters.bool(currentTelemetry.network.connected)}")
        Text("Transports: ${Formatters.list(currentTelemetry.network.transports)}")
        Text("Addresses: ${Formatters.list(currentTelemetry.network.addresses)}")

        Text("Android thermal status: ${currentTelemetry.thermal.status ?: "UNKNOWN"}")
        Text("Thermal raw status: ${currentTelemetry.thermal.rawStatus?.toString() ?: "UNKNOWN"}")

        HorizontalDivider()
        Text("Resource guard", style = MaterialTheme.typography.titleMedium)
        Text("Policy action: ${resourceDecision.action}")
        Text("Policy reason: ${resourceDecision.reason}")
        Text(
            "N8 uses Android thermal categories and battery state. It does not invent Celsius values when Android does not expose them.",
            style = MaterialTheme.typography.bodySmall,
        )

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
                val decision = NodeResourcePolicy.evaluate(
                    NodeTelemetryProvider(context.applicationContext).snapshot()
                )
                resourceDecision = decision
                if (decision.action == ResourceAction.BLOCK) {
                    runtimeStatus = "POLICY BLOCKED: ${decision.reason}"
                    return@Button
                }
                runtimeStatus = "LOADING MODEL..."
                scope.launch {
                    val result = withContext(Dispatchers.IO) {
                        NativeBridge.loadModel(
                            modelPath = path,
                            contextSize = 4096,
                            threads = 4,
                        )
                    }
                    runtimeStatus = result
                    modelLoaded = result == "MODEL LOADED"
                    if (modelLoaded) {
                        configStore.setValidatedModelPath(path)
                        configStore.setRuntimeConfig(4096, 4)
                        configStore.setDesiredModelLoaded(true)
                    }
                }
            },
        ) {
            Text("2. Load Qwen into native runtime")
        }

        Button(
            enabled = modelPath != null && modelLoaded,
            onClick = {
                val decision = NodeResourcePolicy.evaluate(
                    NodeTelemetryProvider(context.applicationContext).snapshot()
                )
                resourceDecision = decision
                if (decision.action == ResourceAction.BLOCK) {
                    inferenceStatus = "POLICY BLOCKED"
                    responseText = decision.reason
                    return@Button
                }

                inferenceStatus = "GENERATING..."
                responseText = ""
                val maxTokens = if (decision.action == ResourceAction.DEGRADE) 48 else 96
                scope.launch {
                    val response = withContext(Dispatchers.IO) {
                        NativeBridge.generate(
                            prompt = "Responde en español y en una sola frase: ¿qué es una red local de inteligencia artificial?",
                            maxTokens = maxTokens,
                        )
                    }
                    responseText = response
                    modelLoaded = NativeBridge.isModelLoaded()
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
                    configStore.setDesiredModelLoaded(false)
                    runtimeStatus = withContext(Dispatchers.IO) {
                        NativeBridge.unloadModel()
                    }
                    modelLoaded = false
                }
            },
        ) {
            Text("Unload model")
        }

        HorizontalDivider()
        Text("Local trust / pairing", style = MaterialTheme.typography.titleMedium)
        Text("Node ID: ${pairingManager.nodeId}")
        Text("Pairing state: $pairingStatus")
        Text(
            "The pairing token is a local research secret. Share it only with the trusted ORBI manager that should control this node.",
            style = MaterialTheme.typography.bodySmall,
        )

        if (!pairingToken.isNullOrBlank()) {
            SelectionContainer {
                Text("Pairing token: $pairingToken")
            }
            Button(
                onClick = {
                    val token = pairingToken ?: return@Button
                    val clipboard = context.getSystemService(Context.CLIPBOARD_SERVICE)
                        as ClipboardManager
                    clipboard.setPrimaryClip(
                        ClipData.newPlainText("ORBI pairing token", token)
                    )
                    pairingCopyStatus = "COPIED TO CLIPBOARD"
                    Toast.makeText(
                        context,
                        "Pairing token copied",
                        Toast.LENGTH_SHORT,
                    ).show()
                },
            ) {
                Text("Copy pairing token")
            }
            Text(
                "Copy state: $pairingCopyStatus",
                style = MaterialTheme.typography.bodySmall,
            )
        }

        Button(
            onClick = {
                pairingToken = pairingManager.rotatePairingToken()
                pairingCopyStatus = "NOT COPIED"
                pairingStatus = "PAIRED"
            },
        ) {
            Text(
                if (pairingManager.hasPairingSecret()) {
                    "Rotate pairing token"
                } else {
                    "Generate pairing token"
                }
            )
        }

        Button(
            enabled = pairingManager.hasPairingSecret(),
            onClick = {
                pairingManager.revokePairing()
                pairingToken = null
                pairingCopyStatus = "NOT COPIED"
                pairingStatus = "REVOKED / NOT PAIRED"
            },
        ) {
            Text("Revoke pairing")
        }

        HorizontalDivider()
        Text("Trusted-LAN API", style = MaterialTheme.typography.titleMedium)
        Text("API state: $apiStatus")
        Text(
            "Endpoint candidate: " +
                (currentTelemetry.network.addresses.firstOrNull { !it.contains(":") }
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
                configStore.setDesiredModelLoaded(false)
                context.stopService(Intent(context, EdgeNodeService::class.java))
                serviceStatus = "STOP REQUESTED"
                apiStatus = "STOPPED BY SERVICE"
            },
        ) {
            Text("Stop headless node service")
        }

        HorizontalDivider()
        Text("Bounded supervisor", style = MaterialTheme.typography.titleMedium)
        Text("Running: ${supervisorSnapshot.running}")
        Text("Restart attempts: ${supervisorSnapshot.restartAttempts}/3")
        Text("Quarantined: ${supervisorSnapshot.quarantined}")
        Text("Last action: ${supervisorSnapshot.lastAction}")

        Button(
            enabled = configStore.desiredModelLoaded() && resourceDecision.action == ResourceAction.ALLOW,
            onClick = {
                runtimeStatus = NativeBridge.unloadModel()
                inferenceStatus = "SIMULATED RUNTIME LOSS; SUPERVISOR SHOULD RECOVER"
            },
        ) {
            Text("Simulate model runtime failure")
        }

        if (responseText.isNotBlank()) {
            HorizontalDivider()
            Text("Native Qwen response", style = MaterialTheme.typography.titleMedium)
            Text(responseText)
        }

        Text(
            "Native Alpha consolidates N0-N9 readiness in one APK. No gate is physically certified until its Node-01 acceptance evidence is recorded.",
            style = MaterialTheme.typography.bodySmall,
        )
    }
}

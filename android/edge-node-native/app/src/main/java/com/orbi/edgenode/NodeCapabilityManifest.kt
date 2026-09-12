package com.orbi.edgenode

import android.content.Context
import java.io.File

data class NodeCapabilityManifest(
    val schemaVersion: String,
    val protocolVersion: String,
    val nodeId: String,
    val buildVersion: String,
    val deviceModel: String,
    val abi: String,
    val memoryTotalBytes: Long?,
    val memoryAvailableBytes: Long?,
    val storageTotalBytes: Long?,
    val storageAvailableBytes: Long?,
    val capabilities: List<String>,
    val availableModelIds: List<String>,
    val loadedModelIds: List<String>,
    val resourceAction: String,
    val headlessSupported: Boolean,
    val signedControlRequired: Boolean,
    val discoveryServiceType: String,
)

class NodeCapabilityProvider(
    private val context: Context,
) {
    fun snapshot(): NodeCapabilityManifest {
        val device = DeviceProfiler.snapshot()
        val health = NodeTelemetryProvider(context).snapshot()
        val policy = NodeResourcePolicy.evaluate(health)
        val pairing = PairingManager(context)
        val config = NodeConfigStore(context)
        val modelPath = config.modelPath()

        val referenceAvailable = modelPath
            ?.let(::File)
            ?.let { it.exists() && it.isFile && it.length() > 0L }
            ?: false

        val availableModels = buildList {
            if (referenceAvailable) add(ReferenceModels.qwen3Node01.id)
        }

        val loadedModels = buildList {
            if (NativeBridge.isModelLoaded()) {
                add(ReferenceModels.qwen3Node01.id)
            }
        }

        val capabilities = buildList {
            add("node.health")
            add("node.diagnostics")
            add("node.headless")
            add("node.signed-control")

            if (
                !NativeBridge.llamaSystemInfo().startsWith("LLAMA NOT AVAILABLE") &&
                !NativeBridge.llamaSystemInfo().startsWith("LLAMA LINK ERROR")
            ) {
                add("text.generate")
            }

            if (referenceAvailable) {
                add("model.qwen3-1.7b.available")
            }

            if (NativeBridge.isModelLoaded()) {
                add("model.qwen3-1.7b.loaded")
            }
        }

        return NodeCapabilityManifest(
            schemaVersion = "0.1",
            protocolVersion = "1",
            nodeId = pairing.nodeId,
            buildVersion = BuildConfig.VERSION_NAME,
            deviceModel = device.model,
            abi = device.abi,
            memoryTotalBytes = health.memory.totalBytes,
            memoryAvailableBytes = health.memory.availableBytes,
            storageTotalBytes = health.storage.totalBytes,
            storageAvailableBytes = health.storage.availableBytes,
            capabilities = capabilities,
            availableModelIds = availableModels,
            loadedModelIds = loadedModels,
            resourceAction = policy.action.name,
            headlessSupported = true,
            signedControlRequired = true,
            discoveryServiceType = NsdAdvertiser.SERVICE_TYPE,
        )
    }
}

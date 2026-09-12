package com.orbi.edgenode

import java.io.File

data class NativeAlphaReadiness(
    val n0Bridge: Boolean,
    val n1Telemetry: Boolean,
    val n2LlamaLink: Boolean,
    val n3ModelImported: Boolean,
    val n4ModelLoaded: Boolean,
    val n5ApiRunning: Boolean,
    val n6HeadlessServiceEvidence: Boolean,
    val n7SupervisorRunning: Boolean,
    val n8ResourceAction: ResourceAction,
    val n9Paired: Boolean,
)

object NativeAlphaReadinessEvaluator {
    fun evaluate(
        telemetry: NodeHealthSnapshot,
        nativeStatus: String,
        llamaSystemInfo: String,
        modelPath: String?,
        modelLoaded: Boolean,
        apiRunning: Boolean,
        supervisor: SupervisorSnapshot,
        resourceDecision: ResourceDecision,
        paired: Boolean,
    ): NativeAlphaReadiness {
        val modelImported = modelPath
            ?.let(::File)
            ?.let { it.exists() && it.isFile && it.length() > 0L }
            ?: false

        val telemetryReady =
            telemetry.memory.totalBytes != null &&
            telemetry.memory.availableBytes != null &&
            telemetry.storage.totalBytes != null &&
            telemetry.battery.percent != null

        return NativeAlphaReadiness(
            n0Bridge = nativeStatus == "JNI BRIDGE READY",
            n1Telemetry = telemetryReady,
            n2LlamaLink =
                !llamaSystemInfo.startsWith("LLAMA NOT AVAILABLE") &&
                !llamaSystemInfo.startsWith("LLAMA LINK ERROR"),
            n3ModelImported = modelImported,
            n4ModelLoaded = modelLoaded,
            n5ApiRunning = apiRunning,
            n6HeadlessServiceEvidence = supervisor.running,
            n7SupervisorRunning = supervisor.running,
            n8ResourceAction = resourceDecision.action,
            n9Paired = paired,
        )
    }
}

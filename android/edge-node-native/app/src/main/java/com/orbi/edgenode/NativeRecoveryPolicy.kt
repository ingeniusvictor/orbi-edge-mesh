package com.orbi.edgenode

import android.content.Context

class NativeRecoveryPolicy(
    context: Context,
) : RecoveryGate {
    private val provider = NodeTelemetryProvider(context.applicationContext)

    override fun evaluate(): RecoveryAuthorization {
        val health = provider.snapshot()
        val decision = NodeResourcePolicy.evaluate(health)

        return if (decision.action == ResourceAction.ALLOW) {
            RecoveryAuthorization(
                allowed = true,
                reason = "resource policy ALLOW: ${decision.reason}",
            )
        } else {
            RecoveryAuthorization(
                allowed = false,
                reason = "resource policy ${decision.action}: ${decision.reason}",
            )
        }
    }
}

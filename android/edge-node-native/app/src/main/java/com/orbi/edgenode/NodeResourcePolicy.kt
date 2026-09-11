package com.orbi.edgenode

enum class ResourceAction {
    ALLOW,
    DEGRADE,
    BLOCK,
}

data class ResourceDecision(
    val action: ResourceAction,
    val reason: String,
)

object NodeResourcePolicy {
    fun evaluate(health: NodeHealthSnapshot): ResourceDecision {
        val thermal = health.thermal.status
        val battery = health.battery.percent
        val charging = health.battery.charging

        if (thermal in setOf("SEVERE", "CRITICAL", "EMERGENCY", "SHUTDOWN")) {
            return ResourceDecision(
                action = ResourceAction.BLOCK,
                reason = "Android thermal status is $thermal.",
            )
        }

        if (battery != null && battery <= 10 && charging != true) {
            return ResourceDecision(
                action = ResourceAction.BLOCK,
                reason = "Battery is $battery% and device is not confirmed charging.",
            )
        }

        if (thermal == null && battery == null) {
            return ResourceDecision(
                action = ResourceAction.BLOCK,
                reason = "Both thermal and battery safety telemetry are unavailable.",
            )
        }

        if (thermal == "MODERATE") {
            return ResourceDecision(
                action = ResourceAction.DEGRADE,
                reason = "Android thermal status is MODERATE.",
            )
        }

        if (battery != null && battery <= 20 && charging != true) {
            return ResourceDecision(
                action = ResourceAction.DEGRADE,
                reason = "Battery is $battery% and device is not confirmed charging.",
            )
        }

        val partial = buildList {
            if (thermal == null) add("thermal unavailable")
            if (battery == null) add("battery unavailable")
        }

        return ResourceDecision(
            action = ResourceAction.ALLOW,
            reason = if (partial.isEmpty()) {
                "Observed Android resource signals are within the N8 research policy."
            } else {
                "Allowed with partial telemetry: ${partial.joinToString(", ")}."
            },
        )
    }
}

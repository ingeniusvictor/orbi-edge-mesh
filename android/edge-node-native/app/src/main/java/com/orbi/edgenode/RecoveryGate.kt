package com.orbi.edgenode

data class RecoveryAuthorization(
    val allowed: Boolean,
    val reason: String,
)

fun interface RecoveryGate {
    fun evaluate(): RecoveryAuthorization
}

class AllowForN7ResearchGate : RecoveryGate {
    override fun evaluate(): RecoveryAuthorization =
        RecoveryAuthorization(
            allowed = true,
            reason = "N7 controlled research gate; N8 resource policy not yet active.",
        )
}

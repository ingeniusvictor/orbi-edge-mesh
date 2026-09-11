package com.orbi.edgenode

data class SupervisorSnapshot(
    val running: Boolean,
    val restartAttempts: Int,
    val quarantined: Boolean,
    val lastAction: String,
)

object SupervisorMonitor {
    @Volatile
    var current: SupervisorSnapshot = SupervisorSnapshot(
        running = false,
        restartAttempts = 0,
        quarantined = false,
        lastAction = "NOT STARTED",
    )
        private set

    fun publish(snapshot: SupervisorSnapshot) {
        current = snapshot
    }
}

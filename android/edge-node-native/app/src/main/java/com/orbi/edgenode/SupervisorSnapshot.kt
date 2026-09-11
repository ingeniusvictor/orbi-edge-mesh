package com.orbi.edgenode

data class SupervisorSnapshot(
    val running: Boolean,
    val restartAttempts: Int,
    val quarantined: Boolean,
    val lastAction: String,
)

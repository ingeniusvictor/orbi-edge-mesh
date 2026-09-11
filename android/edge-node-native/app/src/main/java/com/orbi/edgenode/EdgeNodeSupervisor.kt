package com.orbi.edgenode

import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.TimeUnit

class EdgeNodeSupervisor(
    private val store: NodeConfigStore,
    private val recoveryGate: RecoveryGate,
    private val intervalSeconds: Long = 15L,
    private val maxRestartAttempts: Int = 3,
) {
    @Volatile
    private var executor: ScheduledExecutorService? = null

    @Volatile
    private var restartAttempts = 0

    @Volatile
    private var quarantined = false

    @Volatile
    private var lastAction = "NOT STARTED"

    @Synchronized
    fun start() {
        if (executor != null) return

        val created = Executors.newSingleThreadScheduledExecutor { runnable ->
            Thread(runnable, "orbi-node-supervisor").apply {
                isDaemon = true
            }
        }

        executor = created
        lastAction = "SUPERVISOR STARTED"

        created.scheduleWithFixedDelay(
            { runCatching { tick() } },
            intervalSeconds,
            intervalSeconds,
            TimeUnit.SECONDS,
        )
    }

    @Synchronized
    fun stop() {
        executor?.shutdownNow()
        executor = null
        lastAction = "SUPERVISOR STOPPED"
    }

    @Synchronized
    fun resetQuarantine() {
        restartAttempts = 0
        quarantined = false
        lastAction = "QUARANTINE RESET"
    }

    fun snapshot(): SupervisorSnapshot =
        SupervisorSnapshot(
            running = executor != null,
            restartAttempts = restartAttempts,
            quarantined = quarantined,
            lastAction = lastAction,
        )

    private fun tick() {
        if (!store.desiredModelLoaded()) {
            restartAttempts = 0
            quarantined = false
            lastAction = "MODEL NOT REQUESTED"
            return
        }

        if (NativeBridge.isModelLoaded()) {
            lastAction = "HEALTHY"
            return
        }

        if (quarantined) {
            lastAction = "QUARANTINED"
            return
        }

        val path = store.modelPath()
        if (path.isNullOrBlank()) {
            quarantined = true
            lastAction = "QUARANTINED: MODEL PATH MISSING"
            return
        }

        val authorization = recoveryGate.evaluate()
        if (!authorization.allowed) {
            lastAction = "RECOVERY BLOCKED: ${authorization.reason}"
            return
        }

        if (restartAttempts >= maxRestartAttempts) {
            quarantined = true
            lastAction = "QUARANTINED: RESTART LIMIT"
            return
        }

        restartAttempts += 1
        lastAction = "RECOVERY ATTEMPT $restartAttempts/$maxRestartAttempts"

        val result = NativeBridge.loadModel(
            modelPath = path,
            contextSize = store.contextSize(),
            threads = store.threads(),
        )

        if (result == "MODEL LOADED") {
            lastAction = "RECOVERY PASS: MODEL RELOADED"
            return
        }

        lastAction = "RECOVERY FAIL: $result"

        if (restartAttempts >= maxRestartAttempts) {
            quarantined = true
            lastAction = "QUARANTINED AFTER FAILURE: $result"
        }
    }
}

package com.orbi.edgenode

import android.content.Context

object EdgeNodeRuntime {
    @Volatile
    private var initialized = false

    private lateinit var appContext: Context
    private var apiServer: LocalApiServer? = null
    private var advertiser: NsdAdvertiser? = null
    private var pairing: PairingManager? = null

    @Synchronized
    fun initialize(context: Context) {
        if (initialized) return
        appContext = context.applicationContext
        apiServer = LocalApiServer(appContext, 8080)
        advertiser = NsdAdvertiser(appContext)
        pairing = PairingManager(appContext)
        initialized = true
    }

    @Synchronized
    fun startApi(): String {
        ensureInitialized()
        val apiStatus = apiServer?.start() ?: "ERROR: API_NOT_INITIALIZED"

        if (
            apiStatus.startsWith("RUNNING") ||
            apiStatus.startsWith("ALREADY RUNNING")
        ) {
            val nodeId = pairing?.nodeId
            if (!nodeId.isNullOrBlank()) {
                advertiser?.start(8080, nodeId)
            }
        }

        return apiStatus
    }

    @Synchronized
    fun stopApi(): String {
        if (!initialized) return "STOPPED"
        advertiser?.stop()
        return apiServer?.stop() ?: "STOPPED"
    }

    fun isApiRunning(): Boolean =
        initialized && apiServer?.isRunning() == true

    private fun ensureInitialized() {
        check(initialized) {
            "EdgeNodeRuntime.initialize(context) must be called first."
        }
    }
}

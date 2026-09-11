package com.orbi.edgenode

import android.content.Context

object EdgeNodeRuntime {
    @Volatile
    private var initialized = false

    private lateinit var appContext: Context
    private var apiServer: LocalApiServer? = null

    @Synchronized
    fun initialize(context: Context) {
        if (initialized) return
        appContext = context.applicationContext
        apiServer = LocalApiServer(appContext, 8080)
        initialized = true
    }

    @Synchronized
    fun startApi(): String {
        ensureInitialized()
        return apiServer?.start() ?: "ERROR: API_NOT_INITIALIZED"
    }

    @Synchronized
    fun stopApi(): String {
        if (!initialized) return "STOPPED"
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

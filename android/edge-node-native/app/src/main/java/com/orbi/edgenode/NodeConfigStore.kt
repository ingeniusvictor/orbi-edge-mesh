package com.orbi.edgenode

import android.content.Context

class NodeConfigStore(
    context: Context,
) {
    private val prefs = context.applicationContext.getSharedPreferences(
        "orbi_edge_node_config",
        Context.MODE_PRIVATE,
    )

    fun setValidatedModelPath(path: String) {
        prefs.edit().putString(KEY_MODEL_PATH, path).apply()
    }

    fun modelPath(): String? =
        prefs.getString(KEY_MODEL_PATH, null)

    fun setDesiredModelLoaded(value: Boolean) {
        prefs.edit().putBoolean(KEY_DESIRED_MODEL_LOADED, value).apply()
    }

    fun desiredModelLoaded(): Boolean =
        prefs.getBoolean(KEY_DESIRED_MODEL_LOADED, false)

    fun contextSize(): Int =
        prefs.getInt(KEY_CONTEXT_SIZE, 4096)

    fun threads(): Int =
        prefs.getInt(KEY_THREADS, 4)

    fun setRuntimeConfig(
        contextSize: Int,
        threads: Int,
    ) {
        prefs.edit()
            .putInt(KEY_CONTEXT_SIZE, contextSize.coerceAtLeast(512))
            .putInt(KEY_THREADS, threads.coerceAtLeast(1))
            .apply()
    }

    companion object {
        private const val KEY_MODEL_PATH = "validated_model_path"
        private const val KEY_DESIRED_MODEL_LOADED = "desired_model_loaded"
        private const val KEY_CONTEXT_SIZE = "context_size"
        private const val KEY_THREADS = "threads"
    }
}

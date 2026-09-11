package com.orbi.edgenode

object NativeBridge {
    private val loaded: Boolean = runCatching {
        System.loadLibrary("orbi_native")
    }.isSuccess

    private external fun nativeStatus(): String
    private external fun llamaSystemInfoNative(): String
    private external fun loadModelNative(
        modelPath: String,
        contextSize: Int,
        threads: Int,
    ): String
    private external fun isModelLoadedNative(): Boolean
    private external fun generateNative(
        prompt: String,
        maxTokens: Int,
    ): String
    private external fun unloadModelNative(): String
    private external fun lastGenerationMetricsNative(): String

    fun status(): String {
        if (!loaded) return "JNI BRIDGE NOT LOADED"
        return runCatching { nativeStatus() }
            .getOrElse { "JNI BRIDGE ERROR: ${it.javaClass.simpleName}" }
    }

    fun llamaSystemInfo(): String {
        if (!loaded) return "LLAMA NOT AVAILABLE: JNI BRIDGE NOT LOADED"
        return runCatching { llamaSystemInfoNative() }
            .getOrElse { "LLAMA LINK ERROR: ${it.javaClass.simpleName}" }
    }

    fun loadModel(
        modelPath: String,
        contextSize: Int = 4096,
        threads: Int = 4,
    ): String {
        if (!loaded) return "ERROR: JNI_BRIDGE_NOT_LOADED"
        return runCatching {
            loadModelNative(modelPath, contextSize, threads)
        }.getOrElse {
            "ERROR: MODEL_LOAD_EXCEPTION_${it.javaClass.simpleName}"
        }
    }

    fun isModelLoaded(): Boolean {
        if (!loaded) return false
        return runCatching { isModelLoadedNative() }.getOrDefault(false)
    }

    fun generate(
        prompt: String,
        maxTokens: Int = 64,
    ): String {
        if (!loaded) return "ERROR: JNI_BRIDGE_NOT_LOADED"
        return runCatching {
            generateNative(prompt, maxTokens)
        }.getOrElse {
            "ERROR: GENERATION_EXCEPTION_${it.javaClass.simpleName}"
        }
    }

    fun lastGenerationMetrics(): String {
        if (!loaded) return "metrics unavailable: JNI bridge not loaded"
        return runCatching { lastGenerationMetricsNative() }
            .getOrElse { "metrics unavailable: ${it.javaClass.simpleName}" }
    }

    fun unloadModel(): String {
        if (!loaded) return "ERROR: JNI_BRIDGE_NOT_LOADED"
        return runCatching { unloadModelNative() }
            .getOrElse { "ERROR: MODEL_UNLOAD_EXCEPTION_${it.javaClass.simpleName}" }
    }
}

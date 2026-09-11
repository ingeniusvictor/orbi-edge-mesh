package com.orbi.edgenode

object NativeBridge {
    private val loaded: Boolean = runCatching {
        System.loadLibrary("orbi_native")
    }.isSuccess

    private external fun nativeStatus(): String
    private external fun llamaSystemInfoNative(): String

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
}

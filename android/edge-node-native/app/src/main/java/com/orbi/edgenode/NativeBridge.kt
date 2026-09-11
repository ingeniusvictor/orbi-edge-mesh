package com.orbi.edgenode

object NativeBridge {
    private val loaded: Boolean = runCatching {
        System.loadLibrary("orbi_native")
    }.isSuccess

    private external fun nativeStatus(): String

    fun status(): String {
        if (!loaded) return "JNI BRIDGE NOT LOADED"
        return runCatching { nativeStatus() }
            .getOrElse { "JNI BRIDGE ERROR: ${it.javaClass.simpleName}" }
    }
}

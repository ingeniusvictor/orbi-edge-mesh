package com.orbi.edgenode

import android.os.Build

object DeviceProfiler {
    fun snapshot(): DeviceSnapshot = DeviceSnapshot(
        model = Build.MODEL ?: "unknown",
        androidVersion = Build.VERSION.RELEASE ?: "unknown",
        abi = Build.SUPPORTED_ABIS.firstOrNull() ?: "unknown",
    )
}

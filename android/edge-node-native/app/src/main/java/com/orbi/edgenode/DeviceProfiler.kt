package com.orbi.edgenode

import android.os.Build

object DeviceProfiler {
    fun snapshot(): DeviceSnapshot = DeviceSnapshot(
        manufacturer = Build.MANUFACTURER ?: "unknown",
        model = Build.MODEL ?: "unknown",
        device = Build.DEVICE ?: "unknown",
        androidVersion = Build.VERSION.RELEASE ?: "unknown",
        apiLevel = Build.VERSION.SDK_INT,
        abi = Build.SUPPORTED_ABIS.firstOrNull() ?: "unknown",
        availableProcessors = Runtime.getRuntime().availableProcessors(),
    )
}

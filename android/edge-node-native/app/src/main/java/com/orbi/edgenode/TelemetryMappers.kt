package com.orbi.edgenode

import android.os.BatteryManager
import android.os.PowerManager

object TelemetryMappers {
    fun batterySource(plugged: Int?): String? = when (plugged) {
        BatteryManager.BATTERY_PLUGGED_AC -> "AC"
        BatteryManager.BATTERY_PLUGGED_USB -> "USB"
        BatteryManager.BATTERY_PLUGGED_WIRELESS -> "WIRELESS"
        BatteryManager.BATTERY_PLUGGED_DOCK -> "DOCK"
        0 -> "NOT_PLUGGED"
        null -> null
        else -> "OTHER"
    }

    fun thermalStatus(status: Int?): String? = when (status) {
        null -> null
        PowerManager.THERMAL_STATUS_NONE -> "NONE"
        PowerManager.THERMAL_STATUS_LIGHT -> "LIGHT"
        PowerManager.THERMAL_STATUS_MODERATE -> "MODERATE"
        PowerManager.THERMAL_STATUS_SEVERE -> "SEVERE"
        PowerManager.THERMAL_STATUS_CRITICAL -> "CRITICAL"
        PowerManager.THERMAL_STATUS_EMERGENCY -> "EMERGENCY"
        PowerManager.THERMAL_STATUS_SHUTDOWN -> "SHUTDOWN"
        else -> "UNKNOWN"
    }
}

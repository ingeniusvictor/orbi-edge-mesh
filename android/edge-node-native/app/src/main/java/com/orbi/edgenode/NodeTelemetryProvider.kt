package com.orbi.edgenode

import android.app.ActivityManager
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.BatteryManager
import android.os.Build
import android.os.PowerManager
import android.os.StatFs

class NodeTelemetryProvider(
    private val context: Context,
) {
    fun snapshot(): NodeHealthSnapshot = NodeHealthSnapshot(
        memory = readMemory(),
        storage = readStorage(),
        battery = readBattery(),
        network = readNetwork(),
        thermal = readThermal(),
    )

    private fun readMemory(): MemorySnapshot = runCatching {
        val manager = context.getSystemService(ActivityManager::class.java)
        val info = ActivityManager.MemoryInfo()
        manager.getMemoryInfo(info)
        MemorySnapshot(
            totalBytes = info.totalMem,
            availableBytes = info.availMem,
            lowMemory = info.lowMemory,
        )
    }.getOrElse {
        MemorySnapshot(null, null, null)
    }

    private fun readStorage(): StorageSnapshot = runCatching {
        val stats = StatFs(context.filesDir.absolutePath)
        StorageSnapshot(
            totalBytes = stats.totalBytes,
            availableBytes = stats.availableBytes,
        )
    }.getOrElse {
        StorageSnapshot(null, null)
    }

    private fun readBattery(): BatterySnapshot = runCatching {
        val intent = context.registerReceiver(
            null,
            IntentFilter(Intent.ACTION_BATTERY_CHANGED),
        )

        val level = intent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        val scale = intent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
        val percent = if (level >= 0 && scale > 0) {
            ((level.toDouble() / scale.toDouble()) * 100.0).toInt()
        } else {
            null
        }

        val status = intent?.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        val charging = when (status) {
            BatteryManager.BATTERY_STATUS_CHARGING,
            BatteryManager.BATTERY_STATUS_FULL -> true
            -1, null -> null
            else -> false
        }

        val plugged = intent?.getIntExtra(BatteryManager.EXTRA_PLUGGED, -1)
        BatterySnapshot(
            percent = percent,
            charging = charging,
            source = TelemetryMappers.batterySource(
                plugged?.takeIf { it >= 0 }
            ),
        )
    }.getOrElse {
        BatterySnapshot(null, null, null)
    }

    private fun readNetwork(): NetworkSnapshot = runCatching {
        val manager = context.getSystemService(ConnectivityManager::class.java)
        val network = manager.activeNetwork
            ?: return NetworkSnapshot(false, emptyList(), emptyList())

        val capabilities = manager.getNetworkCapabilities(network)
        val transports = buildList {
            if (capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) == true) add("WIFI")
            if (capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) == true) add("CELLULAR")
            if (capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) == true) add("ETHERNET")
            if (capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_VPN) == true) add("VPN")
            if (capabilities?.hasTransport(NetworkCapabilities.TRANSPORT_BLUETOOTH) == true) add("BLUETOOTH")
        }

        val addresses = manager.getLinkProperties(network)
            ?.linkAddresses
            ?.map { it.address.hostAddress ?: "unknown" }
            ?.distinct()
            ?: emptyList()

        NetworkSnapshot(
            connected = capabilities != null,
            transports = transports,
            addresses = addresses,
        )
    }.getOrElse {
        NetworkSnapshot(null, emptyList(), emptyList())
    }

    private fun readThermal(): ThermalSnapshot {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
            return ThermalSnapshot(null, null)
        }

        return runCatching {
            val manager = context.getSystemService(PowerManager::class.java)
            val raw = manager.currentThermalStatus
            ThermalSnapshot(
                status = TelemetryMappers.thermalStatus(raw),
                rawStatus = raw,
            )
        }.getOrElse {
            ThermalSnapshot(null, null)
        }
    }
}

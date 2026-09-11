package com.orbi.edgenode

data class MemorySnapshot(
    val totalBytes: Long?,
    val availableBytes: Long?,
    val lowMemory: Boolean?,
)

data class StorageSnapshot(
    val totalBytes: Long?,
    val availableBytes: Long?,
)

data class BatterySnapshot(
    val percent: Int?,
    val charging: Boolean?,
    val source: String?,
)

data class NetworkSnapshot(
    val connected: Boolean?,
    val transports: List<String>,
    val addresses: List<String>,
)

data class ThermalSnapshot(
    val status: String?,
    val rawStatus: Int?,
)

data class NodeHealthSnapshot(
    val memory: MemorySnapshot,
    val storage: StorageSnapshot,
    val battery: BatterySnapshot,
    val network: NetworkSnapshot,
    val thermal: ThermalSnapshot,
)

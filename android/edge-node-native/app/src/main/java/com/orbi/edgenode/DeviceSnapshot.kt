package com.orbi.edgenode

data class DeviceSnapshot(
    val manufacturer: String,
    val model: String,
    val device: String,
    val androidVersion: String,
    val apiLevel: Int,
    val abi: String,
    val availableProcessors: Int,
)

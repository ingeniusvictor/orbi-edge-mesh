package com.orbi.edgenode

import java.util.Locale

object Formatters {
    fun bytes(value: Long?): String {
        if (value == null || value < 0L) return "UNKNOWN"
        val gib = value.toDouble() / (1024.0 * 1024.0 * 1024.0)
        return String.format(Locale.US, "%.2f GiB", gib)
    }

    fun percent(value: Int?): String =
        value?.let { "$it%" } ?: "UNKNOWN"

    fun bool(value: Boolean?): String = when (value) {
        true -> "YES"
        false -> "NO"
        null -> "UNKNOWN"
    }

    fun list(values: List<String>): String =
        if (values.isEmpty()) "NONE / UNKNOWN" else values.joinToString(", ")
}

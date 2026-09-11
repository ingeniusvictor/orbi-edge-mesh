package com.orbi.edgenode

sealed interface ModelImportResult {
    data class Success(
        val filePath: String,
        val bytes: Long,
        val sha256: String,
    ) : ModelImportResult

    data class Failure(
        val code: String,
        val message: String,
    ) : ModelImportResult
}

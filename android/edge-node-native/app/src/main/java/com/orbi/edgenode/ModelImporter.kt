package com.orbi.edgenode

import android.content.Context
import android.net.Uri
import java.io.File
import java.nio.file.AtomicMoveNotSupportedException
import java.nio.file.Files
import java.nio.file.StandardCopyOption
import java.security.MessageDigest

class ModelImporter(
    private val context: Context,
) {
    fun importFromUri(
        uri: Uri,
        spec: ModelSpec,
    ): ModelImportResult {
        val modelsDir = File(context.filesDir, "models")
        if (!modelsDir.exists() && !modelsDir.mkdirs()) {
            return ModelImportResult.Failure(
                code = "MODEL_DIR_CREATE_FAILED",
                message = "Could not create app model directory.",
            )
        }

        val partial = File(modelsDir, "${spec.fileName}.part")
        val finalFile = File(modelsDir, spec.fileName)

        return try {
            partial.delete()

            val digest = MessageDigest.getInstance("SHA-256")
            var total = 0L

            val input = context.contentResolver.openInputStream(uri)
                ?: return ModelImportResult.Failure(
                    code = "MODEL_OPEN_FAILED",
                    message = "Android could not open the selected document.",
                )

            input.use { source ->
                partial.outputStream().buffered().use { sink ->
                    val buffer = ByteArray(1024 * 1024)
                    while (true) {
                        val read = source.read(buffer)
                        if (read < 0) break
                        if (read == 0) continue
                        sink.write(buffer, 0, read)
                        digest.update(buffer, 0, read)
                        total += read
                    }
                }
            }

            val actualSha = digest.digest().joinToString("") { "%02x".format(it) }

            if (!actualSha.equals(spec.expectedSha256, ignoreCase = true)) {
                partial.delete()
                return ModelImportResult.Failure(
                    code = "MODEL_HASH_MISMATCH",
                    message = "Selected GGUF SHA-256 does not match the Node-01 reference model.",
                )
            }

            try {
                Files.move(
                    partial.toPath(),
                    finalFile.toPath(),
                    StandardCopyOption.ATOMIC_MOVE,
                    StandardCopyOption.REPLACE_EXISTING,
                )
            } catch (_: AtomicMoveNotSupportedException) {
                Files.move(
                    partial.toPath(),
                    finalFile.toPath(),
                    StandardCopyOption.REPLACE_EXISTING,
                )
            }

            ModelImportResult.Success(
                filePath = finalFile.absolutePath,
                bytes = total,
                sha256 = actualSha,
            )
        } catch (t: Throwable) {
            partial.delete()
            ModelImportResult.Failure(
                code = "MODEL_IMPORT_ERROR",
                message = t.message ?: t.javaClass.simpleName,
            )
        }
    }
}

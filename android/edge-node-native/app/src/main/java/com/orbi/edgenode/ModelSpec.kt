package com.orbi.edgenode

data class ModelSpec(
    val id: String,
    val displayName: String,
    val fileName: String,
    val expectedSha256: String,
)

object ReferenceModels {
    val qwen3Node01 = ModelSpec(
        id = "qwen3-1.7b-q4_k_m-node01",
        displayName = "Qwen3 1.7B Q4_K_M",
        fileName = "Qwen3-1.7B-Q4_K_M.gguf",
        expectedSha256 = "d2387ca2dbfee2ffabce7120d3770dadca0b293052bc2f0e138fdc940d9bc7b5",
    )
}

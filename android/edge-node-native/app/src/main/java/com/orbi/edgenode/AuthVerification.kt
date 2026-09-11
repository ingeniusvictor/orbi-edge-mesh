package com.orbi.edgenode

data class AuthVerification(
    val allowed: Boolean,
    val code: String,
    val message: String,
)

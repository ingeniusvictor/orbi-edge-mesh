package com.orbi.edgenode

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import org.json.JSONArray
import org.json.JSONObject
import java.io.BufferedInputStream
import java.io.BufferedOutputStream
import java.io.ByteArrayOutputStream
import java.net.InetSocketAddress
import java.net.ServerSocket
import java.net.Socket
import java.nio.charset.StandardCharsets
import java.util.Locale
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.concurrent.atomic.AtomicBoolean

class LocalApiServer(
    private val context: Context,
    private val port: Int = 8080,
) {
    private val running = AtomicBoolean(false)
    private val pairing = PairingManager(context.applicationContext)
    private var serverSocket: ServerSocket? = null
    private var acceptThread: Thread? = null
    private var workers: ExecutorService? = null

    @Synchronized
    fun start(): String {
        if (running.get()) return "ALREADY RUNNING :$port"
        if (!hasTrustedLanTransport()) {
            return "ERROR: WIFI_OR_ETHERNET_REQUIRED"
        }

        return try {
            val socket = ServerSocket()
            socket.reuseAddress = true
            socket.bind(InetSocketAddress("0.0.0.0", port))

            val executor = Executors.newCachedThreadPool()
            serverSocket = socket
            workers = executor
            running.set(true)

            acceptThread = Thread({
                acceptLoop(socket, executor)
            }, "orbi-local-api-accept").apply {
                isDaemon = true
                start()
            }

            "RUNNING :$port"
        } catch (t: Throwable) {
            stop()
            "ERROR: API_START_${t.javaClass.simpleName}: ${t.message ?: "unknown"}"
        }
    }

    @Synchronized
    fun stop(): String {
        running.set(false)
        runCatching { serverSocket?.close() }
        serverSocket = null
        acceptThread = null
        workers?.shutdownNow()
        workers = null
        return "STOPPED"
    }

    fun isRunning(): Boolean = running.get()

    private fun acceptLoop(
        server: ServerSocket,
        executor: ExecutorService,
    ) {
        while (running.get()) {
            val client = try {
                server.accept()
            } catch (_: Throwable) {
                break
            }

            executor.execute {
                runCatching { handleClient(client) }
                client.closeQuietly()
            }
        }
        running.set(false)
    }

    private fun handleClient(socket: Socket) {
        socket.soTimeout = 60_000

        val input = BufferedInputStream(socket.getInputStream())
        val output = BufferedOutputStream(socket.getOutputStream())

        val requestLine = readLine(input)
            ?: return

        val parts = requestLine.split(" ", limit = 3)
        if (parts.size < 2) {
            writeJson(output, 400, errorJson("bad_request", "Malformed request line."))
            return
        }

        val method = parts[0].uppercase(Locale.US)
        val path = parts[1].substringBefore('?')

        val headers = linkedMapOf<String, String>()
        while (true) {
            val line = readLine(input) ?: break
            if (line.isEmpty()) break
            val index = line.indexOf(':')
            if (index > 0) {
                val name = line.substring(0, index).trim().lowercase(Locale.US)
                val value = line.substring(index + 1).trim()
                headers[name] = value
            }
        }

        val contentLength = headers["content-length"]?.toIntOrNull() ?: 0
        if (contentLength < 0 || contentLength > MAX_BODY_BYTES) {
            writeJson(output, 413, errorJson("payload_too_large", "Request body exceeds research limit."))
            return
        }

        val bodyBytes = ByteArray(contentLength)
        var offset = 0
        while (offset < contentLength) {
            val read = input.read(bodyBytes, offset, contentLength - offset)
            if (read < 0) {
                writeJson(output, 400, errorJson("bad_request", "Unexpected end of request body."))
                return
            }
            offset += read
        }

        val body = String(bodyBytes, StandardCharsets.UTF_8)

        when {
            method == "GET" && path == "/health" -> {
                val json = JSONObject()
                    .put("status", "ok")
                    .put("service", "orbi-edge-node")
                    .put("model_loaded", NativeBridge.isModelLoaded())
                    .put("api_mode", "trusted-lan-research")
                writeJson(output, 200, json)
            }

            method == "GET" && path == "/node" -> {
                val device = DeviceProfiler.snapshot()
                val health = NodeTelemetryProvider(context).snapshot()
                val policy = NodeResourcePolicy.evaluate(health)
                val supervisor = SupervisorMonitor.current
                val json = JSONObject()
                    .put("service", "orbi-edge-node")
                    .put("manufacturer", device.manufacturer)
                    .put("device_model", device.model)
                    .put("device_codename", device.device)
                    .put("android", device.androidVersion)
                    .put("api_level", device.apiLevel)
                    .put("abi", device.abi)
                    .put("logical_processors", device.availableProcessors)
                    .put("memory_total_bytes", health.memory.totalBytes ?: JSONObject.NULL)
                    .put("memory_available_bytes", health.memory.availableBytes ?: JSONObject.NULL)
                    .put("storage_total_bytes", health.storage.totalBytes ?: JSONObject.NULL)
                    .put("storage_available_bytes", health.storage.availableBytes ?: JSONObject.NULL)
                    .put("battery_percent", health.battery.percent ?: JSONObject.NULL)
                    .put("thermal_status", health.thermal.status ?: JSONObject.NULL)
                    .put("model_loaded", NativeBridge.isModelLoaded())
                    .put("resource_action", policy.action.name)
                    .put("resource_reason", policy.reason)
                    .put("supervisor_running", supervisor.running)
                    .put("supervisor_restart_attempts", supervisor.restartAttempts)
                    .put("supervisor_quarantined", supervisor.quarantined)
                    .put("supervisor_last_action", supervisor.lastAction)
                    .put("node_id", pairing.nodeId)
                    .put("paired", pairing.hasPairingSecret())
                    .put("services_supported", JSONArray().put("CHAT"))
                    .put("chat_model_id", ReferenceModels.qwen3Node01.id)
                writeJson(output, 200, json)
            }

            method == "GET" && path == "/v1/models" -> {
                val data = JSONArray()
                if (NativeBridge.isModelLoaded()) {
                    data.put(
                        JSONObject()
                            .put("id", ReferenceModels.qwen3Node01.id)
                            .put("object", "model")
                            .put("owned_by", "orbi-local")
                    )
                }

                writeJson(
                    output,
                    200,
                    JSONObject()
                        .put("object", "list")
                        .put("data", data),
                )
            }

            method == "POST" && path == "/v1/chat/completions" -> {
                val verification = pairing.verify(
                    method = method,
                    path = path,
                    body = bodyBytes,
                    headers = headers,
                )

                if (!verification.allowed) {
                    writeJson(
                        output,
                        401,
                        errorJson(verification.code, verification.message),
                    )
                    return
                }

                handleChat(output, body)
            }

            else -> {
                writeJson(output, 404, errorJson("not_found", "Endpoint not found."))
            }
        }
    }

    private fun handleChat(
        output: BufferedOutputStream,
        body: String,
    ) {
        if (!NativeBridge.isModelLoaded()) {
            writeJson(output, 503, errorJson("model_not_loaded", "Load the local model first."))
            return
        }

        val request = try {
            JSONObject(body)
        } catch (_: Throwable) {
            writeJson(output, 400, errorJson("invalid_json", "Body must be valid UTF-8 JSON."))
            return
        }

        val requestedModel = request
            .optString("model", ReferenceModels.qwen3Node01.id)
            .ifBlank { ReferenceModels.qwen3Node01.id }

        if (requestedModel != ReferenceModels.qwen3Node01.id) {
            writeJson(
                output,
                400,
                errorJson(
                    "model_not_available",
                    "Requested model is not loaded on this ORBI Edge Node.",
                ),
            )
            return
        }

        val messages = request.optJSONArray("messages")
        if (messages == null || messages.length() == 0) {
            writeJson(output, 400, errorJson("invalid_request", "messages[] is required."))
            return
        }

        var prompt: String? = null
        for (index in messages.length() - 1 downTo 0) {
            val item = messages.optJSONObject(index) ?: continue
            if (item.optString("role") == "user") {
                prompt = item.optString("content").takeIf { it.isNotBlank() }
                if (prompt != null) break
            }
        }

        if (prompt == null) {
            writeJson(output, 400, errorJson("invalid_request", "A user message with text content is required."))
            return
        }

        val policy = NodeResourcePolicy.evaluate(
            NodeTelemetryProvider(context).snapshot()
        )

        if (policy.action == ResourceAction.BLOCK) {
            writeJson(
                output,
                503,
                errorJson(
                    "resource_protected",
                    "ORBI resource policy blocked inference: ${policy.reason}",
                ),
            )
            return
        }

        val requested = request.optInt("max_tokens", 96)
        val ceiling = if (policy.action == ResourceAction.DEGRADE) 64 else 256
        val maxTokens = requested.coerceIn(1, ceiling)
        val response = NativeBridge.generate(prompt, maxTokens)

        if (response.startsWith("ERROR:")) {
            writeJson(output, 500, errorJson("inference_error", response))
            return
        }

        val completion = JSONObject()
            .put("id", "orbi-local")
            .put("object", "chat.completion")
            .put("model", ReferenceModels.qwen3Node01.id)
            .put(
                "choices",
                JSONArray().put(
                    JSONObject()
                        .put("index", 0)
                        .put(
                            "message",
                            JSONObject()
                                .put("role", "assistant")
                                .put("content", response),
                        )
                        .put("finish_reason", "stop"),
                ),
            )

        writeJson(output, 200, completion)
    }

    private fun hasTrustedLanTransport(): Boolean {
        return runCatching {
            val manager = context.getSystemService(ConnectivityManager::class.java)
            val network = manager.activeNetwork ?: return false
            val capabilities = manager.getNetworkCapabilities(network) ?: return false

            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) ||
                capabilities.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET)
        }.getOrDefault(false)
    }

    private fun readLine(input: BufferedInputStream): String? {
        val buffer = ByteArrayOutputStream()

        while (buffer.size() <= MAX_HEADER_LINE_BYTES) {
            val value = input.read()
            if (value < 0) {
                return if (buffer.size() == 0) null
                else buffer.toString(StandardCharsets.US_ASCII.name())
            }

            if (value == '\n'.code) break
            if (value != '\r'.code) buffer.write(value)
        }

        if (buffer.size() > MAX_HEADER_LINE_BYTES) return null
        return buffer.toString(StandardCharsets.US_ASCII.name())
    }

    private fun writeJson(
        output: BufferedOutputStream,
        status: Int,
        json: JSONObject,
    ) {
        val bytes = json.toString().toByteArray(StandardCharsets.UTF_8)
        val reason = when (status) {
            200 -> "OK"
            400 -> "Bad Request"
            401 -> "Unauthorized"
            404 -> "Not Found"
            413 -> "Payload Too Large"
            500 -> "Internal Server Error"
            503 -> "Service Unavailable"
            else -> "Response"
        }

        val header = buildString {
            append("HTTP/1.1 $status $reason\r\n")
            append("Content-Type: application/json; charset=utf-8\r\n")
            append("Content-Length: ${bytes.size}\r\n")
            append("Connection: close\r\n")
            append("X-ORBI-Research-Mode: trusted-lan\r\n")
            append("\r\n")
        }.toByteArray(StandardCharsets.US_ASCII)

        output.write(header)
        output.write(bytes)
        output.flush()
    }

    private fun errorJson(
        code: String,
        message: String,
    ): JSONObject = JSONObject().put(
        "error",
        JSONObject()
            .put("code", code)
            .put("message", message),
    )

    private fun Socket.closeQuietly() {
        runCatching { close() }
    }

    companion object {
        private const val MAX_BODY_BYTES = 64 * 1024
        private const val MAX_HEADER_LINE_BYTES = 8 * 1024
    }
}

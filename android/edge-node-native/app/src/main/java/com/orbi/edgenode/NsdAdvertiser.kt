package com.orbi.edgenode

import android.content.Context
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo

data class DiscoverySnapshot(
    val advertising: Boolean,
    val serviceName: String?,
    val serviceType: String,
    val port: Int?,
    val lastStatus: String,
)

object DiscoveryMonitor {
    @Volatile
    var current = DiscoverySnapshot(
        advertising = false,
        serviceName = null,
        serviceType = NsdAdvertiser.SERVICE_TYPE,
        port = null,
        lastStatus = "NOT STARTED",
    )
        private set

    fun publish(snapshot: DiscoverySnapshot) {
        current = snapshot
    }
}

class NsdAdvertiser(
    context: Context,
) {
    private val manager = context.applicationContext
        .getSystemService(NsdManager::class.java)

    @Volatile
    private var listener: NsdManager.RegistrationListener? = null

    @Synchronized
    fun start(
        port: Int,
        nodeId: String,
    ): String {
        if (listener != null) {
            return "ALREADY ADVERTISING"
        }

        val suffix = nodeId
            .replace("-", "")
            .takeLast(8)
            .ifBlank { "node" }

        val serviceInfo = NsdServiceInfo().apply {
            serviceName = "ORBI-$suffix"
            serviceType = SERVICE_TYPE
            setPort(port)
            setAttribute("proto", "1")
            setAttribute("node", nodeId)
            setAttribute("build", BuildConfig.VERSION_NAME)
            setAttribute("auth", "hmac-sha256")
        }

        val created = object : NsdManager.RegistrationListener {
            override fun onServiceRegistered(info: NsdServiceInfo) {
                DiscoveryMonitor.publish(
                    DiscoverySnapshot(
                        advertising = true,
                        serviceName = info.serviceName,
                        serviceType = info.serviceType ?: SERVICE_TYPE,
                        port = info.port,
                        lastStatus = "REGISTERED",
                    )
                )
            }

            override fun onRegistrationFailed(
                info: NsdServiceInfo,
                errorCode: Int,
            ) {
                synchronized(this@NsdAdvertiser) {
                    listener = null
                }
                DiscoveryMonitor.publish(
                    DiscoverySnapshot(
                        advertising = false,
                        serviceName = info.serviceName,
                        serviceType = info.serviceType ?: SERVICE_TYPE,
                        port = info.port.takeIf { it > 0 },
                        lastStatus = "REGISTRATION FAILED: $errorCode",
                    )
                )
            }

            override fun onServiceUnregistered(info: NsdServiceInfo) {
                DiscoveryMonitor.publish(
                    DiscoverySnapshot(
                        advertising = false,
                        serviceName = info.serviceName,
                        serviceType = info.serviceType ?: SERVICE_TYPE,
                        port = info.port.takeIf { it > 0 },
                        lastStatus = "UNREGISTERED",
                    )
                )
            }

            override fun onUnregistrationFailed(
                info: NsdServiceInfo,
                errorCode: Int,
            ) {
                DiscoveryMonitor.publish(
                    DiscoverySnapshot(
                        advertising = false,
                        serviceName = info.serviceName,
                        serviceType = info.serviceType ?: SERVICE_TYPE,
                        port = info.port.takeIf { it > 0 },
                        lastStatus = "UNREGISTER FAILED: $errorCode",
                    )
                )
            }
        }

        listener = created
        DiscoveryMonitor.publish(
            DiscoverySnapshot(
                advertising = false,
                serviceName = serviceInfo.serviceName,
                serviceType = SERVICE_TYPE,
                port = port,
                lastStatus = "REGISTERING",
            )
        )

        return try {
            manager.registerService(
                serviceInfo,
                NsdManager.PROTOCOL_DNS_SD,
                created,
            )
            "REGISTERING ${serviceInfo.serviceName}"
        } catch (t: Throwable) {
            listener = null
            DiscoveryMonitor.publish(
                DiscoverySnapshot(
                    advertising = false,
                    serviceName = serviceInfo.serviceName,
                    serviceType = SERVICE_TYPE,
                    port = port,
                    lastStatus = "ERROR: ${t.javaClass.simpleName}",
                )
            )
            "ERROR: NSD_${t.javaClass.simpleName}"
        }
    }

    @Synchronized
    fun stop(): String {
        val currentListener = listener ?: return "NOT ADVERTISING"
        listener = null

        return try {
            manager.unregisterService(currentListener)
            "UNREGISTER REQUESTED"
        } catch (t: Throwable) {
            DiscoveryMonitor.publish(
                DiscoveryMonitor.current.copy(
                    advertising = false,
                    lastStatus = "ERROR: ${t.javaClass.simpleName}",
                )
            )
            "ERROR: NSD_${t.javaClass.simpleName}"
        }
    }

    companion object {
        const val SERVICE_TYPE = "_orbi-edge._tcp."
    }
}

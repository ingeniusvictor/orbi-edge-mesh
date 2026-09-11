package com.orbi.edgenode

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val snapshot = DeviceProfiler.snapshot()
        val nativeStatus = NativeBridge.status()

        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    NodeStatusScreen(snapshot, nativeStatus)
                }
            }
        }
    }
}

@Composable
private fun NodeStatusScreen(
    snapshot: DeviceSnapshot,
    nativeStatus: String,
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        Text(
            text = "ORBI Edge Node",
            style = MaterialTheme.typography.headlineMedium,
        )
        Text("Research build: ${BuildConfig.VERSION_NAME}")
        Text("Device: ${snapshot.model}")
        Text("Android: ${snapshot.androidVersion}")
        Text("ABI: ${snapshot.abi}")
        Text("Native runtime: $nativeStatus")
        Text("AI runtime: NOT LOADED")
    }
}

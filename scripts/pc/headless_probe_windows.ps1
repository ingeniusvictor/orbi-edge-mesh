param(
    [Parameter(Mandatory=$false)][string]$HostIp = "192.168.1.7",
    [Parameter(Mandatory=$false)][int]$Port = 8080,
    [Parameter(Mandatory=$false)][int]$IntervalSeconds = 300,
    [Parameter(Mandatory=$false)][int]$Checks = 7,
    [Parameter(Mandatory=$false)][string]$Model = "Qwen3-1.7B-Q4_K_M.gguf",
    [Parameter(Mandatory=$false)][string]$Output = ".\node01-headless-probe.json"
)

$ErrorActionPreference = "Stop"
$base = "http://${HostIp}:$Port"
$results = @()

Write-Host "=== ORBI Edge Mesh - Node-01 Headless Probe ==="
Write-Host "Target: $base"
Write-Host "Checks: $Checks"
Write-Host "Interval: $IntervalSeconds seconds"
Write-Host "Estimated duration: $([math]::Round((($Checks-1)*$IntervalSeconds)/60,1)) minutes"
Write-Host ""

for ($i=1; $i -le $Checks; $i++) {
    $timestamp = (Get-Date).ToString("o")
    $ok = $false
    $detail = ""
    $elapsed = 0.0

    try {
        $sw = [System.Diagnostics.Stopwatch]::StartNew()
        $models = Invoke-RestMethod -Uri "$base/v1/models" -Method Get -TimeoutSec 20
        $sw.Stop()
        $elapsed = [math]::Round($sw.Elapsed.TotalSeconds,3)
        $ok = $true
        $detail = "models endpoint reachable"
    } catch {
        $detail = $_.Exception.Message
    }

    $state = if ($ok) { "PASS" } else { "FAIL" }
    Write-Host "[$state] check=$i/$Checks time=$timestamp elapsed=${elapsed}s $detail"

    $results += [pscustomobject]@{
        check = $i
        timestamp = $timestamp
        ok = $ok
        elapsed_s = $elapsed
        detail = $detail
    }

    if ($i -eq 5) {
        Write-Host ""
        Write-Host "[INFERENCE GATE] Running post-20-minute chat completion..."
        $body = @{
            model = $Model
            messages = @(
                @{
                    role = "user"
                    content = "Responde solo: ORBI HEADLESS OK"
                }
            )
            stream = $false
        } | ConvertTo-Json -Depth 5

        $bodyUtf8 = [System.Text.Encoding]::UTF8.GetBytes($body)

        try {
            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            $response = Invoke-RestMethod `
                -Uri "$base/v1/chat/completions" `
                -Method Post `
                -ContentType "application/json; charset=utf-8" `
                -Body $bodyUtf8 `
                -TimeoutSec 60
            $sw.Stop()
            $answer = $response.choices[0].message.content
            Write-Host "[INFERENCE PASS] elapsed=$([math]::Round($sw.Elapsed.TotalSeconds,3))s answer=$answer"
        } catch {
            Write-Host "[INFERENCE FAIL] $($_.Exception.Message)"
        }
        Write-Host ""
    }

    if ($i -lt $Checks) {
        Start-Sleep -Seconds $IntervalSeconds
    }
}

$summary = [pscustomobject]@{
    schema_version = "0.1"
    target = $base
    started_at = $results[0].timestamp
    finished_at = $results[-1].timestamp
    checks = $results
    pass_count = @($results | Where-Object { $_.ok }).Count
    fail_count = @($results | Where-Object { -not $_.ok }).Count
}

$summary | ConvertTo-Json -Depth 6 | Set-Content -Path $Output -Encoding UTF8
Write-Host ""
Write-Host "Evidence written to: $Output"
Write-Host "PASS=$($summary.pass_count) FAIL=$($summary.fail_count)"

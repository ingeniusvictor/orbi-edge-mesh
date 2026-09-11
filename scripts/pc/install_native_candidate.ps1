param(
    [Parameter(Mandatory=$true)]
    [string]$ApkPath,

    [Parameter(Mandatory=$true)]
    [ValidatePattern('^[0-9a-fA-F]{64}$')]
    [string]$ExpectedSha256
)

$ErrorActionPreference = "Stop"

Write-Host "=== ORBI Edge Node - Verified ADB Install ==="

if (-not (Test-Path -LiteralPath $ApkPath -PathType Leaf)) {
    throw "APK not found: $ApkPath"
}

$actualSha = (Get-FileHash -LiteralPath $ApkPath -Algorithm SHA256).Hash.ToLowerInvariant()
$expectedSha = $ExpectedSha256.ToLowerInvariant()

Write-Host "APK: $ApkPath"
Write-Host "SHA-256 actual:   $actualSha"
Write-Host "SHA-256 expected: $expectedSha"

if ($actualSha -ne $expectedSha) {
    throw "APK SHA-256 mismatch. Installation aborted."
}

$adb = Get-Command adb -ErrorAction SilentlyContinue
if (-not $adb) {
    throw "adb was not found in PATH. No installation was attempted."
}

$deviceLines = & adb devices |
    Select-Object -Skip 1 |
    Where-Object { $_ -match '\S' }

$authorized = @(
    $deviceLines |
    Where-Object { $_ -match "\tdevice$" }
)

$unauthorized = @(
    $deviceLines |
    Where-Object { $_ -match "\tunauthorized$" }
)

if ($unauthorized.Count -gt 0) {
    throw "An Android device is waiting for USB debugging authorization. Approve it on the phone, then retry."
}

if ($authorized.Count -ne 1) {
    throw "Expected exactly one authorized Android device, found $($authorized.Count). No installation was attempted."
}

$serial = ($authorized[0] -split "\t")[0]
Write-Host "Authorized device: $serial"
Write-Host "Installing verified research APK..."

& adb -s $serial install -r $ApkPath
if ($LASTEXITCODE -ne 0) {
    throw "adb install failed. The script will not uninstall the current app automatically."
}

Write-Host "PASS: verified APK installed/updated."
Write-Host "No application data was intentionally cleared by this script."

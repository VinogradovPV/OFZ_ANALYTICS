param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [switch]$Help,
    [string[]]$GuiArgs = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($Help) {
    Write-Host "OFZ Analytics GUI launcher"
    Write-Host ""
    Write-Host "Usage:"
    Write-Host "  powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1"
    Write-Host "  powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -GuiArgs --smoke"
    Write-Host ""
    Write-Host "The wrapper launches .venv\Scripts\ofz-gui.exe or dist\ofz-gui.exe."
    exit 0
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$venvGui = Join-Path $ProjectRoot ".venv\Scripts\ofz-gui.exe"
$distGui = Join-Path $ProjectRoot "dist\ofz-gui.exe"

if (Test-Path $venvGui -PathType Leaf) {
    $guiPath = $venvGui
}
elseif (Test-Path $distGui -PathType Leaf) {
    $guiPath = $distGui
}
else {
    Write-Error (
        "OFZ GUI entry point not found. From project root run: " +
        ".\.venv\Scripts\python.exe -m pip install -e ."
    )
    exit 1
}

Push-Location $ProjectRoot
try {
    & $guiPath @GuiArgs
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}

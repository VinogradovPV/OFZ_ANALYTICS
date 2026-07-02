Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

chcp 65001 | Out-Null
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$GuiExe = Join-Path $ProjectRoot ".venv\Scripts\ofz-gui.exe"

if (-not (Test-Path $GuiExe -PathType Leaf)) {
    Write-Host "GUI entry point not found: $GuiExe" -ForegroundColor Red
    Write-Host "Run: .\.venv\Scripts\python.exe -m pip install -e ." -ForegroundColor Yellow
    exit 1
}

& $GuiExe @args
exit $LASTEXITCODE

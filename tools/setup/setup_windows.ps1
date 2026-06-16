param(
    [switch]$DryRun,
    [switch]$IncludeDev,
    [switch]$RunFastQuality,
    [string]$PythonVersion = "3.14",
    [string]$ReportDate = "2026-05-01",
    [int]$RetrospectiveYears = 4,
    [ValidateSet("month", "quarter", "year")]
    [string]$PeriodType = "month",
    [ValidateSet("cumulative", "point")]
    [string]$AggregationMode = "cumulative"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$VenvDir = Join-Path $ProjectRoot ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"

function Write-Step {
    param([string]$Message)
    Write-Host "[setup] $Message"
}

function Invoke-SetupCommand {
    param(
        [string]$Description,
        [string]$FilePath,
        [string[]]$Arguments
    )

    $preview = "$FilePath $($Arguments -join ' ')"
    if ($DryRun) {
        Write-Step "DRY-RUN: $Description"
        Write-Host "  $preview"
        return
    }

    Write-Step $Description
    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $preview"
    }
}

function Test-RequiredPath {
    param(
        [string]$Path,
        [string]$Description
    )
    if (-not (Test-Path $Path)) {
        throw "$Description not found: $Path"
    }
}

Set-Location $ProjectRoot
Write-Step "Project root: $ProjectRoot"
Write-Step "PowerShell version: $($PSVersionTable.PSVersion)"

Test-RequiredPath -Path (Join-Path $ProjectRoot "pyproject.toml") -Description "pyproject.toml"
Test-RequiredPath -Path (Join-Path $ProjectRoot "requirements.txt") -Description "requirements.txt"
Test-RequiredPath -Path (Join-Path $ProjectRoot "data\raw") -Description "data/raw"

if (-not (Test-Path $VenvPython)) {
    Invoke-SetupCommand `
        -Description "Create .venv with Python $PythonVersion" `
        -FilePath "py" `
        -Arguments @("-$PythonVersion", "-m", "venv", ".venv")
} else {
    Write-Step ".venv already exists: $VenvDir"
}

if ($DryRun -and -not (Test-Path $VenvPython)) {
    Write-Step "DRY-RUN: .venv python will be available after venv creation: $VenvPython"
} else {
    Test-RequiredPath -Path $VenvPython -Description ".venv Python"
    Invoke-SetupCommand -Description "Check Python version" -FilePath $VenvPython -Arguments @("--version")
}

Invoke-SetupCommand `
    -Description "Upgrade pip tooling" `
    -FilePath $VenvPython `
    -Arguments @("-m", "pip", "install", "--upgrade", "pip", "setuptools")

Invoke-SetupCommand `
    -Description "Install runtime dependencies" `
    -FilePath $VenvPython `
    -Arguments @("-m", "pip", "install", "-r", "requirements.txt")

if ($IncludeDev) {
    Test-RequiredPath -Path (Join-Path $ProjectRoot "requirements-dev.txt") -Description "requirements-dev.txt"
    Invoke-SetupCommand `
        -Description "Install dev/QA dependencies" `
        -FilePath $VenvPython `
        -Arguments @("-m", "pip", "install", "-r", "requirements-dev.txt")
} else {
    Write-Step "Dev/QA dependencies skipped. Re-run with -IncludeDev when screenshot QA is needed."
}

Invoke-SetupCommand `
    -Description "Install project in editable mode" `
    -FilePath $VenvPython `
    -Arguments @("-m", "pip", "install", "-e", ".")

Invoke-SetupCommand -Description "pip check" -FilePath $VenvPython -Arguments @("-m", "pip", "check")

$CliExecutables = @(
    "ofz-run.exe",
    "ofz-interactive.exe",
    "ofz-quality.exe",
    "ofz-clean-outputs.exe",
    "ofz-schema.exe",
    "ofz-build-release-bundle.exe"
)

foreach ($exe in $CliExecutables) {
    $exePath = Join-Path $VenvDir "Scripts\$exe"
    Invoke-SetupCommand -Description "CLI help: $exe" -FilePath $exePath -Arguments @("--help")
}

Invoke-SetupCommand `
    -Description "Compile Python scripts" `
    -FilePath $VenvPython `
    -Arguments @("-m", "compileall", "-q", "scripts")

if ($RunFastQuality) {
    $qualityPath = Join-Path $VenvDir "Scripts\ofz-quality.exe"
    Invoke-SetupCommand `
        -Description "Optional fast quality gate" `
        -FilePath $qualityPath `
        -Arguments @(
            "--fast",
            "--report-date", $ReportDate,
            "--retrospective-years", [string]$RetrospectiveYears,
            "--period-type", $PeriodType,
            "--aggregation-mode", $AggregationMode
        )
} else {
    Write-Step "Fast quality gate skipped. Re-run with -RunFastQuality to execute it."
}

Write-Step "Windows setup workflow completed."

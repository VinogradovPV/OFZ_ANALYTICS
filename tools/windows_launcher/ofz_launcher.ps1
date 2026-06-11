param(
    [string]$ProjectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path,
    [string]$ReportDate = "2026-05-01",
    [int]$RetrospectiveYears = 4,
    [ValidateSet("month", "quarter", "year")]
    [string]$PeriodType = "month",
    [ValidateSet("cumulative", "point")]
    [string]$AggregationMode = "cumulative",
    [ValidateSet(
        "smoke",
        "validate",
        "run",
        "schema",
        "quality-fast",
        "quality-full",
        "cleanup-dry-run",
        "cleanup-archive-all",
        "cleanup-delete-all-with-archive",
        "release-dry-run",
        "release-build",
        "open-outputs",
        "open-release"
    )]
    [string]$Action = "smoke",
    [string]$Confirm = "",
    [switch]$Gui
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$LauncherTimestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$LauncherLogDir = Join-Path $ProjectRoot "outputs\reports\launcher"
$LauncherLogPath = Join-Path $LauncherLogDir "launcher_run_$LauncherTimestamp.log"

function Write-LauncherLog {
    param([string]$Message)

    New-Item -ItemType Directory -Force -Path $LauncherLogDir | Out-Null
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $LauncherLogPath -Value $line
    Write-Host $line
}

function Assert-ProjectEnvironment {
    param([string]$Root)

    if (-not (Test-Path $Root -PathType Container)) {
        throw "Project root does not exist: $Root"
    }

    $requiredPaths = @(
        "pyproject.toml",
        ".venv\Scripts",
        "data\raw"
    )

    foreach ($relativePath in $requiredPaths) {
        $fullPath = Join-Path $Root $relativePath
        if (-not (Test-Path $fullPath)) {
            throw "Required project path is missing: $relativePath"
        }
    }

    Push-Location $Root
    try {
        git status --short | Out-Null
    }
    finally {
        Pop-Location
    }
}

function Assert-ReportDate {
    param([string]$Value)

    $parsed = [DateTime]::MinValue
    $ok = [DateTime]::TryParseExact(
        $Value,
        "yyyy-MM-dd",
        [System.Globalization.CultureInfo]::InvariantCulture,
        [System.Globalization.DateTimeStyles]::None,
        [ref]$parsed
    )
    if (-not $ok) {
        throw "report_date must use YYYY-MM-DD format."
    }
    if ($parsed.Day -ne 1) {
        throw "report_date must be the first day of a month."
    }
}

function Assert-RetrospectiveYears {
    param([int]$Value)

    if ($Value -lt 1 -or $Value -gt 10) {
        throw "retrospective_years must be an integer in range 1..10."
    }
}

function Get-CliPath {
    param([string]$CliName)

    $allowedCli = @{
        "ofz-run.exe" = ".venv\Scripts\ofz-run.exe"
        "ofz-interactive.exe" = ".venv\Scripts\ofz-interactive.exe"
        "ofz-quality.exe" = ".venv\Scripts\ofz-quality.exe"
        "ofz-clean-outputs.exe" = ".venv\Scripts\ofz-clean-outputs.exe"
        "ofz-schema.exe" = ".venv\Scripts\ofz-schema.exe"
        "ofz-build-release-bundle.exe" = ".venv\Scripts\ofz-build-release-bundle.exe"
    }

    if (-not $allowedCli.ContainsKey($CliName)) {
        throw "Unsupported CLI: $CliName"
    }

    $path = Join-Path $ProjectRoot $allowedCli[$CliName]
    if (-not (Test-Path $path -PathType Leaf)) {
        throw "CLI entry point is missing: $path"
    }
    return $path
}

function Get-CommonArgs {
    return @(
        "--report-date", $ReportDate,
        "--retrospective-years", "$RetrospectiveYears",
        "--period-type", $PeriodType,
        "--aggregation-mode", $AggregationMode
    )
}

function Invoke-WhitelistedCli {
    param(
        [string]$CliName,
        [string[]]$Arguments
    )

    $cliPath = Get-CliPath $CliName
    $stdoutPath = Join-Path $LauncherLogDir "stdout_$LauncherTimestamp.txt"
    $stderrPath = Join-Path $LauncherLogDir "stderr_$LauncherTimestamp.txt"

    Write-LauncherLog ("Working directory: {0}" -f $ProjectRoot)
    Write-LauncherLog ("Command preview: {0} {1}" -f $CliName, ($Arguments -join " "))

    Push-Location $ProjectRoot
    try {
        & $cliPath @Arguments 1> $stdoutPath 2> $stderrPath
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }

    $stdout = ""
    $stderr = ""
    if (Test-Path $stdoutPath) {
        $stdoutContent = Get-Content $stdoutPath -Raw
        if ($null -ne $stdoutContent) {
            $stdout = [string]$stdoutContent
        }
    }
    if (Test-Path $stderrPath) {
        $stderrContent = Get-Content $stderrPath -Raw
        if ($null -ne $stderrContent) {
            $stderr = [string]$stderrContent
        }
    }

    if ($stdout.Trim()) {
        Write-LauncherLog "STDOUT:"
        Write-Host $stdout
        Add-Content -Path $LauncherLogPath -Value $stdout
    }
    if ($stderr.Trim()) {
        Write-LauncherLog "STDERR:"
        Write-Host $stderr
        Add-Content -Path $LauncherLogPath -Value $stderr
    }

    Write-LauncherLog ("Exit code: {0}" -f $exitCode)
    return $exitCode
}

function Assert-DeleteConfirmation {
    param(
        [string]$SelectedAction,
        [string]$Value
    )

    if ($SelectedAction -eq "cleanup-delete-all-with-archive" -and $Value -ne "DELETE_OUTPUTS") {
        throw "Delete cleanup is blocked. Pass -Confirm DELETE_OUTPUTS to continue."
    }
}

function Assert-BundleConfirmation {
    param(
        [string]$SelectedAction,
        [string]$Value
    )

    if ($SelectedAction -eq "release-build" -and $Value -ne "BUILD_RELEASE_BUNDLE") {
        throw "Release bundle creation is blocked. Pass -Confirm BUILD_RELEASE_BUNDLE to continue."
    }
}

function Invoke-LauncherAction {
    param([string]$SelectedAction)

    Assert-ProjectEnvironment $ProjectRoot
    Assert-ReportDate $ReportDate
    Assert-RetrospectiveYears $RetrospectiveYears
    Assert-DeleteConfirmation $SelectedAction $Confirm
    Assert-BundleConfirmation $SelectedAction $Confirm

    switch ($SelectedAction) {
        "validate" {
            Write-LauncherLog "Validate environment OK."
            return 0
        }
        "run" {
            return Invoke-WhitelistedCli "ofz-run.exe" (Get-CommonArgs)
        }
        "schema" {
            return Invoke-WhitelistedCli "ofz-schema.exe" (Get-CommonArgs)
        }
        "quality-fast" {
            return Invoke-WhitelistedCli "ofz-quality.exe" (@("--fast") + (Get-CommonArgs))
        }
        "quality-full" {
            return Invoke-WhitelistedCli "ofz-quality.exe" (@("--full") + (Get-CommonArgs))
        }
        "cleanup-dry-run" {
            return Invoke-WhitelistedCli "ofz-clean-outputs.exe" @("--dry-run")
        }
        "cleanup-archive-all" {
            return Invoke-WhitelistedCli "ofz-clean-outputs.exe" @("--archive-all")
        }
        "cleanup-delete-all-with-archive" {
            return Invoke-WhitelistedCli "ofz-clean-outputs.exe" @("--archive-all", "--delete-all", "--confirm", "DELETE_OUTPUTS")
        }
        "release-dry-run" {
            return Invoke-WhitelistedCli "ofz-build-release-bundle.exe" (@("--dry-run") + (Get-CommonArgs))
        }
        "release-build" {
            return Invoke-WhitelistedCli "ofz-build-release-bundle.exe" (@("--include-outputs", "--confirm", "BUILD_RELEASE_BUNDLE") + (Get-CommonArgs))
        }
        "open-outputs" {
            $outputsPath = Join-Path $ProjectRoot "outputs"
            Invoke-Item $outputsPath
            Write-LauncherLog "Opened outputs folder: $outputsPath"
            return 0
        }
        "open-release" {
            $releasePath = Join-Path $ProjectRoot "releases"
            if (-not (Test-Path $releasePath)) {
                throw "Release folder does not exist yet: $releasePath"
            }
            Invoke-Item $releasePath
            Write-LauncherLog "Opened release folder: $releasePath"
            return 0
        }
        default {
            throw "Unsupported action: $SelectedAction"
        }
    }
}

function Invoke-SmokeTest {
    Write-LauncherLog "Starting launcher smoke test."
    Assert-ProjectEnvironment $ProjectRoot
    Assert-ReportDate $ReportDate
    Assert-RetrospectiveYears $RetrospectiveYears
    Write-LauncherLog "Validate environment OK."

    try {
        Assert-ReportDate "2026-05-15"
        throw "Bad date validation did not fail."
    }
    catch {
        Write-LauncherLog "Bad date blocked."
    }

    try {
        Assert-DeleteConfirmation "cleanup-delete-all-with-archive" ""
        throw "Delete confirmation validation did not fail."
    }
    catch {
        Write-LauncherLog "Delete mode blocked without DELETE_OUTPUTS."
    }

    try {
        Assert-BundleConfirmation "release-build" ""
        throw "Bundle confirmation validation did not fail."
    }
    catch {
        Write-LauncherLog "Release bundle creation blocked without BUILD_RELEASE_BUNDLE."
    }

    $cleanupExitCode = Invoke-LauncherAction "cleanup-dry-run"
    if ($cleanupExitCode -ne 0) {
        throw "Cleanup dry-run failed with exit code $cleanupExitCode."
    }
    Write-LauncherLog "Dry-run cleanup does not delete."

    $bundleExitCode = Invoke-LauncherAction "release-dry-run"
    if ($bundleExitCode -ne 0) {
        throw "Release bundle dry-run failed with exit code $bundleExitCode."
    }
    Write-LauncherLog "Release bundle dry-run starts."
    Write-LauncherLog "Quality gate fast starts only when user selects it."
    Write-LauncherLog "Launcher log created: $LauncherLogPath"
    return 0
}

function Show-LauncherGui {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $form = New-Object System.Windows.Forms.Form
    $form.Text = "OFZ Analytics Launcher"
    $form.Width = 620
    $form.Height = 420
    $form.StartPosition = "CenterScreen"

    $label = New-Object System.Windows.Forms.Label
    $label.Text = "OFZ Analytics CLI launcher. Commands are limited to approved entry points."
    $label.Left = 12
    $label.Top = 12
    $label.Width = 570
    $form.Controls.Add($label)

    $dateBox = New-Object System.Windows.Forms.TextBox
    $dateBox.Text = $ReportDate
    $dateBox.Left = 150
    $dateBox.Top = 45
    $dateBox.Width = 120
    $form.Controls.Add($dateBox)

    $dateLabel = New-Object System.Windows.Forms.Label
    $dateLabel.Text = "Report date"
    $dateLabel.Left = 12
    $dateLabel.Top = 48
    $dateLabel.Width = 120
    $form.Controls.Add($dateLabel)

    $actionBox = New-Object System.Windows.Forms.ComboBox
    $actionBox.DropDownStyle = "DropDownList"
    [void]$actionBox.Items.AddRange(@(
        "validate",
        "run",
        "schema",
        "quality-fast",
        "cleanup-dry-run",
        "release-dry-run"
    ))
    $actionBox.SelectedItem = "validate"
    $actionBox.Left = 150
    $actionBox.Top = 80
    $actionBox.Width = 170
    $form.Controls.Add($actionBox)

    $actionLabel = New-Object System.Windows.Forms.Label
    $actionLabel.Text = "Action"
    $actionLabel.Left = 12
    $actionLabel.Top = 84
    $actionLabel.Width = 120
    $form.Controls.Add($actionLabel)

    $outputBox = New-Object System.Windows.Forms.TextBox
    $outputBox.Multiline = $true
    $outputBox.ScrollBars = "Vertical"
    $outputBox.Left = 12
    $outputBox.Top = 130
    $outputBox.Width = 570
    $outputBox.Height = 190
    $outputBox.ReadOnly = $true
    $form.Controls.Add($outputBox)

    $runButton = New-Object System.Windows.Forms.Button
    $runButton.Text = "Run"
    $runButton.Left = 12
    $runButton.Top = 335
    $runButton.Width = 90
    $runButton.Add_Click({
        try {
            $script:ReportDate = $dateBox.Text
            $exitCode = Invoke-LauncherAction ([string]$actionBox.SelectedItem)
            $outputBox.Text = "Exit code: $exitCode`r`nLog: $LauncherLogPath"
        }
        catch {
            $outputBox.Text = $_.Exception.Message
        }
    })
    $form.Controls.Add($runButton)

    $closeButton = New-Object System.Windows.Forms.Button
    $closeButton.Text = "Close"
    $closeButton.Left = 112
    $closeButton.Top = 335
    $closeButton.Width = 90
    $closeButton.Add_Click({ $form.Close() })
    $form.Controls.Add($closeButton)

    [void]$form.ShowDialog()
}

try {
    if ($Gui) {
        Show-LauncherGui
        exit 0
    }

    if ($Action -eq "smoke") {
        exit (Invoke-SmokeTest)
    }

    exit (Invoke-LauncherAction $Action)
}
catch {
    Write-LauncherLog ("ERROR: {0}" -f $_.Exception.Message)
    Write-Error $_.Exception.Message
    exit 1
}

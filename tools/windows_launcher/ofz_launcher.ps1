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
        "validate-environment",
        "run-pipeline",
        "schema",
        "quality-fast",
        "quality-full",
        "cleanup-dry-run",
        "cleanup-archive-all",
        "cleanup-delete-all",
        "release-dry-run",
        "release-build",
        "open-outputs",
        "open-releases"
    )]
    [string]$Action = "smoke",
    [string]$ConfirmDelete = "",
    [string]$ConfirmBundle = "",
    [switch]$Gui,
    [switch]$AutoCloseGuiForCheck,
    [switch]$PreviewOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$LauncherTimestamp = "{0}_{1}" -f (Get-Date -Format "yyyyMMdd_HHmmss_fffffff"), ([guid]::NewGuid().ToString("N").Substring(0, 8))
$LauncherLogDir = Join-Path $ProjectRoot "outputs\reports\launcher"
$LauncherLogPath = Join-Path $LauncherLogDir "launcher_run_$LauncherTimestamp.log"

function Set-LauncherContext {
    param([string]$Root)

    $script:ProjectRoot = $Root
    $script:LauncherLogDir = Join-Path $script:ProjectRoot "outputs\reports\launcher"
    $script:LauncherLogPath = Join-Path $script:LauncherLogDir "launcher_run_$script:LauncherTimestamp.log"
}

function Write-LauncherLog {
    param([string]$Message)

    New-Item -ItemType Directory -Force -Path $script:LauncherLogDir | Out-Null
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss"), $Message
    Add-Content -Path $script:LauncherLogPath -Value $line
    Write-Host $line
}

function Assert-ProjectEnvironment {
    param([string]$Root)

    $checks = Get-ProjectEnvironmentChecks $Root
    $failed = @($checks | Where-Object { -not $_.Ok })
    if ($failed.Count -gt 0) {
        $missing = ($failed | ForEach-Object { $_.Name }) -join ", "
        throw "Project environment validation failed: $missing"
    }
}

function Get-ProjectEnvironmentChecks {
    param([string]$Root)

    $items = @(
        @{ Name = "project root"; Path = $Root; Type = "Container" },
        @{ Name = "pyproject.toml"; Path = (Join-Path $Root "pyproject.toml"); Type = "Leaf" },
        @{ Name = ".venv\Scripts"; Path = (Join-Path $Root ".venv\Scripts"); Type = "Container" },
        @{ Name = "data\raw"; Path = (Join-Path $Root "data\raw"); Type = "Container" },
        @{ Name = "ofz-run.exe"; Path = (Join-Path $Root ".venv\Scripts\ofz-run.exe"); Type = "Leaf" },
        @{ Name = "ofz-schema.exe"; Path = (Join-Path $Root ".venv\Scripts\ofz-schema.exe"); Type = "Leaf" },
        @{ Name = "ofz-quality.exe"; Path = (Join-Path $Root ".venv\Scripts\ofz-quality.exe"); Type = "Leaf" },
        @{ Name = "ofz-clean-outputs.exe"; Path = (Join-Path $Root ".venv\Scripts\ofz-clean-outputs.exe"); Type = "Leaf" },
        @{ Name = "ofz-build-release-bundle.exe"; Path = (Join-Path $Root ".venv\Scripts\ofz-build-release-bundle.exe"); Type = "Leaf" }
    )

    return @($items | ForEach-Object {
        $exists = if ($_.Type -eq "Leaf") {
            Test-Path $_.Path -PathType Leaf
        }
        else {
            Test-Path $_.Path -PathType Container
        }
        [PSCustomObject]@{
            Name = [string]$_.Name
            Path = [string]$_.Path
            Ok = [bool]$exists
        }
    })
}

function Write-EnvironmentCheckReport {
    param([object[]]$Checks)

    foreach ($check in $Checks) {
        $status = if ($check.Ok) { "OK" } else { "FAIL" }
        Write-LauncherLog ("{0}: {1} ({2})" -f $status, $check.Name, $check.Path)
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

    $path = Join-Path $script:ProjectRoot $allowedCli[$CliName]
    if (-not (Test-Path $path -PathType Leaf)) {
        throw "CLI entry point is missing: $path"
    }
    return $path
}

function Get-CommonArgs {
    return @(
        "--report-date", $script:ReportDate,
        "--retrospective-years", "$script:RetrospectiveYears",
        "--period-type", $script:PeriodType,
        "--aggregation-mode", $script:AggregationMode
    )
}

function Assert-DeleteConfirmation {
    param([string]$SelectedAction, [string]$Value)

    if ($SelectedAction -eq "cleanup-delete-all" -and $Value -ne "DELETE_OUTPUTS") {
        throw "Delete cleanup is blocked. Pass DELETE_OUTPUTS to continue."
    }
}

function Assert-BundleConfirmation {
    param([string]$SelectedAction, [string]$Value)

    if ($SelectedAction -eq "release-build" -and $Value -ne "BUILD_RELEASE_BUNDLE") {
        throw "Release bundle creation is blocked. Pass BUILD_RELEASE_BUNDLE to continue."
    }
}

function Get-LauncherCommand {
    param([string]$SelectedAction)

    switch ($SelectedAction) {
        "validate-environment" { return @{ Cli = ""; Args = @(); Preview = "validate-environment uses local file checks; no pipeline process started." } }
        "run-pipeline" { return @{ Cli = "ofz-run.exe"; Args = (Get-CommonArgs) } }
        "schema" { return @{ Cli = "ofz-schema.exe"; Args = (Get-CommonArgs) } }
        "quality-fast" { return @{ Cli = "ofz-quality.exe"; Args = @("--fast") + (Get-CommonArgs) } }
        "quality-full" { return @{ Cli = "ofz-quality.exe"; Args = @("--full") + (Get-CommonArgs) } }
        "cleanup-dry-run" { return @{ Cli = "ofz-clean-outputs.exe"; Args = @("--dry-run") } }
        "cleanup-archive-all" { return @{ Cli = "ofz-clean-outputs.exe"; Args = @("--archive-all") } }
        "cleanup-delete-all" { return @{ Cli = "ofz-clean-outputs.exe"; Args = @("--archive-all", "--delete-all", "--confirm", "DELETE_OUTPUTS") } }
        "release-dry-run" { return @{ Cli = "ofz-build-release-bundle.exe"; Args = @("--dry-run") + (Get-CommonArgs) } }
        "release-build" { return @{ Cli = "ofz-build-release-bundle.exe"; Args = @("--include-outputs", "--confirm", "BUILD_RELEASE_BUNDLE") + (Get-CommonArgs) } }
        "open-outputs" { return @{ Cli = ""; Args = @(); Preview = "open outputs folder" } }
        "open-releases" { return @{ Cli = ""; Args = @(); Preview = "open releases folder" } }
        default { throw "Unsupported action: $SelectedAction" }
    }
}

function Format-CommandPreview {
    param([string]$SelectedAction)

    $command = Get-LauncherCommand $SelectedAction
    if ($command.ContainsKey("Preview") -and $command["Preview"]) {
        return [string]$command["Preview"]
    }
    $cliDisplay = ".\.venv\Scripts\{0}" -f $command["Cli"]
    return ("{0} {1}" -f $cliDisplay, (($command["Args"] | ForEach-Object { if ($_ -match "\s") { '"' + $_ + '"' } else { $_ } }) -join " "))
}

function Invoke-WhitelistedCli {
    param([string]$CliName, [string[]]$Arguments)

    $cliPath = Get-CliPath $CliName
    $stdoutPath = Join-Path $script:LauncherLogDir "stdout_$script:LauncherTimestamp.txt"
    $stderrPath = Join-Path $script:LauncherLogDir "stderr_$script:LauncherTimestamp.txt"

    Write-LauncherLog ("Working directory: {0}" -f $script:ProjectRoot)
    Write-LauncherLog ("Command preview: {0} {1}" -f $CliName, ($Arguments -join " "))

    Push-Location $script:ProjectRoot
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
        if ($null -ne $stdoutContent) { $stdout = [string]$stdoutContent }
    }
    if (Test-Path $stderrPath) {
        $stderrContent = Get-Content $stderrPath -Raw
        if ($null -ne $stderrContent) { $stderr = [string]$stderrContent }
    }

    if ($stdout.Trim()) {
        Write-LauncherLog "STDOUT:"
        Write-Host $stdout
        Add-Content -Path $script:LauncherLogPath -Value $stdout
    }
    if ($stderr.Trim()) {
        Write-LauncherLog "STDERR:"
        Write-Host $stderr
        Add-Content -Path $script:LauncherLogPath -Value $stderr
    }

    Write-LauncherLog ("Exit code: {0}" -f $exitCode)
    if ($exitCode -ne 0) {
        $lastMessage = Get-LastMeaningfulProcessLine $stderr $stdout
        Write-LauncherLog ("CLI failed. Exit code: {0}. Full log: {1}. Last message: {2}" -f $exitCode, $script:LauncherLogPath, $lastMessage)
    }
    return $exitCode
}

function Get-LastMeaningfulProcessLine {
    param([string]$Stderr, [string]$Stdout)

    foreach ($content in @($Stderr, $Stdout)) {
        if (-not [string]::IsNullOrWhiteSpace($content)) {
            $lines = @($content -split "`r?`n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
            if ($lines.Count -gt 0) {
                return [string]$lines[-1]
            }
        }
    }
    return "No stderr/stdout details captured."
}

function Invoke-LauncherAction {
    param([string]$SelectedAction)

    Set-LauncherContext $script:ProjectRoot
    Assert-ProjectEnvironment $script:ProjectRoot
    Assert-ReportDate $script:ReportDate
    Assert-RetrospectiveYears $script:RetrospectiveYears
    Assert-DeleteConfirmation $SelectedAction $script:ConfirmDelete
    Assert-BundleConfirmation $SelectedAction $script:ConfirmBundle

    if ($SelectedAction -eq "validate-environment") {
        $checks = Get-ProjectEnvironmentChecks $script:ProjectRoot
        Write-EnvironmentCheckReport $checks
        Assert-ProjectEnvironment $script:ProjectRoot
        Write-LauncherLog "validate-environment uses local file checks; no pipeline process started."
        Write-LauncherLog "Validate environment OK."
        return 0
    }
    if ($SelectedAction -eq "open-outputs") {
        $outputsPath = Join-Path $script:ProjectRoot "outputs"
        Invoke-Item $outputsPath
        Write-LauncherLog "Opened outputs folder: $outputsPath"
        return 0
    }
    if ($SelectedAction -eq "open-releases") {
        $releasePath = Join-Path $script:ProjectRoot "releases"
        if (-not (Test-Path $releasePath)) {
            throw "Release folder does not exist yet: $releasePath"
        }
        Invoke-Item $releasePath
        Write-LauncherLog "Opened release folder: $releasePath"
        return 0
    }

    $command = Get-LauncherCommand $SelectedAction
    return Invoke-WhitelistedCli ([string]$command.Cli) ([string[]]$command.Args)
}

function Invoke-SmokeTest {
    Write-LauncherLog "Starting launcher smoke test."
    Assert-ProjectEnvironment $script:ProjectRoot
    Assert-ReportDate $script:ReportDate
    Assert-RetrospectiveYears $script:RetrospectiveYears
    Write-LauncherLog "Validate environment OK."

    try {
        Assert-ReportDate "2026-05-15"
        throw "Bad date validation did not fail."
    }
    catch {
        Write-LauncherLog "Bad date blocked."
    }

    try {
        Assert-DeleteConfirmation "cleanup-delete-all" ""
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
    Write-LauncherLog "Launcher log created: $script:LauncherLogPath"
    return 0
}

function Add-Label {
    param($Form, [string]$Text, [int]$Left, [int]$Top, [int]$Width = 145)

    $label = New-Object System.Windows.Forms.Label
    $label.Text = $Text
    $label.Left = $Left
    $label.Top = $Top
    $label.Width = $Width
    $Form.Controls.Add($label)
    return $label
}

function Add-TextBox {
    param($Form, [string]$Text, [int]$Left, [int]$Top, [int]$Width = 220)

    $box = New-Object System.Windows.Forms.TextBox
    $box.Text = $Text
    $box.Left = $Left
    $box.Top = $Top
    $box.Width = $Width
    $Form.Controls.Add($box)
    return $box
}

function Add-ComboBox {
    param($Form, [string[]]$Items, [string]$Selected, [int]$Left, [int]$Top, [int]$Width = 180)

    $box = New-Object System.Windows.Forms.ComboBox
    $box.DropDownStyle = "DropDownList"
    [void]$box.Items.AddRange($Items)
    $box.SelectedItem = $Selected
    $box.Left = $Left
    $box.Top = $Top
    $box.Width = $Width
    $Form.Controls.Add($box)
    return $box
}

function Show-LauncherGui {
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $form = New-Object System.Windows.Forms.Form
    $form.Text = "OFZ Analytics Launcher"
    $form.Width = 980
    $form.Height = 760
    $form.StartPosition = "CenterScreen"

    $info = New-Object System.Windows.Forms.Label
    $info.Text = "OFZ Analytics CLI launcher. No arbitrary shell commands. UI calls approved entry points only."
    $info.Left = 12
    $info.Top = 12
    $info.Width = 930
    $form.Controls.Add($info)

    Add-Label $form "Project root" 12 48 | Out-Null
    $projectRootBox = Add-TextBox $form $script:ProjectRoot 170 45 620
    $browseButton = New-Object System.Windows.Forms.Button
    $browseButton.Text = "Browse"
    $browseButton.Left = 805
    $browseButton.Top = 43
    $browseButton.Width = 80
    $browseButton.Add_Click({
        $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
        $dialog.SelectedPath = $projectRootBox.Text
        if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            $projectRootBox.Text = $dialog.SelectedPath
        }
    })
    $form.Controls.Add($browseButton)

    Add-Label $form "Report date" 12 84 | Out-Null
    $dateBox = Add-TextBox $form $script:ReportDate 170 81 140
    Add-Label $form "Retrospective years" 330 84 150 | Out-Null
    $yearsBox = Add-TextBox $form ([string]$script:RetrospectiveYears) 485 81 70
    Add-Label $form "Period type" 580 84 90 | Out-Null
    $periodBox = Add-ComboBox $form @("month", "quarter", "year") $script:PeriodType 675 81 110
    Add-Label $form "Aggregation" 805 84 90 | Out-Null
    $aggregationBox = Add-ComboBox $form @("cumulative", "point") $script:AggregationMode 890 81 75

    Add-Label $form "Action" 12 122 | Out-Null
    $actionBox = Add-ComboBox $form @(
        "validate-environment",
        "run-pipeline",
        "schema",
        "quality-fast",
        "quality-full",
        "cleanup-dry-run",
        "cleanup-archive-all",
        "cleanup-delete-all",
        "release-dry-run",
        "release-build",
        "open-outputs",
        "open-releases"
    ) "validate-environment" 170 119 220

    Add-Label $form "Cleanup mode" 415 122 105 | Out-Null
    $cleanupModeBox = Add-ComboBox $form @("keep", "dry-run", "archive-all", "delete-all-with-archive") "keep" 525 119 170

    $schemaCheck = New-Object System.Windows.Forms.CheckBox
    $schemaCheck.Text = "Run schema validation"
    $schemaCheck.Left = 170
    $schemaCheck.Top = 158
    $schemaCheck.Width = 180
    $form.Controls.Add($schemaCheck)

    $fastCheck = New-Object System.Windows.Forms.CheckBox
    $fastCheck.Text = "Run quality gate fast"
    $fastCheck.Left = 360
    $fastCheck.Top = 158
    $fastCheck.Width = 180
    $form.Controls.Add($fastCheck)

    $fullCheck = New-Object System.Windows.Forms.CheckBox
    $fullCheck.Text = "Run quality gate full (manual)"
    $fullCheck.Left = 550
    $fullCheck.Top = 158
    $fullCheck.Width = 220
    $form.Controls.Add($fullCheck)

    $bundleCheck = New-Object System.Windows.Forms.CheckBox
    $bundleCheck.Text = "Build release bundle"
    $bundleCheck.Left = 170
    $bundleCheck.Top = 184
    $bundleCheck.Width = 170
    $form.Controls.Add($bundleCheck)

    $openOutputsCheck = New-Object System.Windows.Forms.CheckBox
    $openOutputsCheck.Text = "Open outputs after run"
    $openOutputsCheck.Left = 360
    $openOutputsCheck.Top = 184
    $openOutputsCheck.Width = 180
    $form.Controls.Add($openOutputsCheck)

    $openReleaseCheck = New-Object System.Windows.Forms.CheckBox
    $openReleaseCheck.Text = "Open release after bundle"
    $openReleaseCheck.Left = 550
    $openReleaseCheck.Top = 184
    $openReleaseCheck.Width = 205
    $form.Controls.Add($openReleaseCheck)

    Add-Label $form "Confirm DELETE_OUTPUTS" 12 222 155 | Out-Null
    $deleteConfirmBox = Add-TextBox $form "" 170 219 220
    Add-Label $form "Confirm BUILD_RELEASE_BUNDLE" 415 222 190 | Out-Null
    $bundleConfirmBox = Add-TextBox $form "" 610 219 220

    Add-Label $form "Command preview" 12 260 | Out-Null
    $previewBox = New-Object System.Windows.Forms.TextBox
    $previewBox.Multiline = $true
    $previewBox.ScrollBars = "Vertical"
    $previewBox.Left = 170
    $previewBox.Top = 255
    $previewBox.Width = 760
    $previewBox.Height = 80
    $previewBox.ReadOnly = $true
    $form.Controls.Add($previewBox)

    Add-Label $form "Output / status" 12 355 | Out-Null
    $outputBox = New-Object System.Windows.Forms.TextBox
    $outputBox.Multiline = $true
    $outputBox.ScrollBars = "Vertical"
    $outputBox.Left = 170
    $outputBox.Top = 350
    $outputBox.Width = 760
    $outputBox.Height = 270
    $outputBox.ReadOnly = $true
    $form.Controls.Add($outputBox)

    $logLabel = New-Object System.Windows.Forms.Label
    $logLabel.Text = "Log: $script:LauncherLogPath"
    $logLabel.Left = 170
    $logLabel.Top = 630
    $logLabel.Width = 760
    $form.Controls.Add($logLabel)

    function Sync-ContextFromGui {
        Set-LauncherContext $projectRootBox.Text
        $script:ReportDate = $dateBox.Text
        $script:RetrospectiveYears = [int]$yearsBox.Text
        $script:PeriodType = [string]$periodBox.SelectedItem
        $script:AggregationMode = [string]$aggregationBox.SelectedItem
        $script:ConfirmDelete = $deleteConfirmBox.Text
        $script:ConfirmBundle = $bundleConfirmBox.Text
        $logLabel.Text = "Log: $script:LauncherLogPath"
    }

    function Update-CommandPreview {
        try {
            Sync-ContextFromGui
            $previewBox.Text = Format-CommandPreview ([string]$actionBox.SelectedItem)
        }
        catch {
            $previewBox.Text = $_.Exception.Message
        }
    }

    function Set-ActionFromCleanupMode {
        switch ([string]$cleanupModeBox.SelectedItem) {
            "dry-run" { $actionBox.SelectedItem = "cleanup-dry-run" }
            "archive-all" { $actionBox.SelectedItem = "cleanup-archive-all" }
            "delete-all-with-archive" { $actionBox.SelectedItem = "cleanup-delete-all" }
        }
        Update-CommandPreview
    }

    foreach ($control in @($projectRootBox, $dateBox, $yearsBox, $periodBox, $aggregationBox, $actionBox, $deleteConfirmBox, $bundleConfirmBox)) {
        $control.Add_TextChanged({ Update-CommandPreview })
        if ($control -is [System.Windows.Forms.ComboBox]) {
            $control.Add_SelectedIndexChanged({ Update-CommandPreview })
        }
    }
    $cleanupModeBox.Add_SelectedIndexChanged({ Set-ActionFromCleanupMode })

    $previewButton = New-Object System.Windows.Forms.Button
    $previewButton.Text = "Preview"
    $previewButton.Left = 170
    $previewButton.Top = 665
    $previewButton.Width = 90
    $previewButton.Add_Click({ Update-CommandPreview })
    $form.Controls.Add($previewButton)

    $runButton = New-Object System.Windows.Forms.Button
    $runButton.Text = "Run selected"
    $runButton.Left = 270
    $runButton.Top = 665
    $runButton.Width = 110
    $runButton.Add_Click({
        try {
            Sync-ContextFromGui
            $selectedAction = [string]$actionBox.SelectedItem
            $exitCode = Invoke-LauncherAction $selectedAction
            $status = "Action: $selectedAction`r`nExit code: $exitCode`r`nLog: $script:LauncherLogPath"
            if ($exitCode -ne 0) {
                $status += "`r`nAction failed. See the full launcher log above for stdout/stderr details."
            }
            if ($schemaCheck.Checked -and $selectedAction -ne "schema") {
                $status += "`r`nSchema validation selected but not auto-chained; choose Action=schema to run it."
            }
            if ($fastCheck.Checked -and $selectedAction -ne "quality-fast") {
                $status += "`r`nQuality fast selected but not auto-chained; choose Action=quality-fast to run it."
            }
            if ($fullCheck.Checked -and $selectedAction -ne "quality-full") {
                $status += "`r`nQuality full is manual-only; choose Action=quality-full to run it."
            }
            if ($bundleCheck.Checked -and $selectedAction -ne "release-build") {
                $status += "`r`nBuild release bundle selected but not auto-chained; choose Action=release-build to run it."
            }
            if ($openOutputsCheck.Checked) {
                [void](Invoke-LauncherAction "open-outputs")
            }
            if ($openReleaseCheck.Checked) {
                [void](Invoke-LauncherAction "open-releases")
            }
            $outputBox.Text = $status
        }
        catch {
            $outputBox.Text = $_.Exception.Message
        }
    })
    $form.Controls.Add($runButton)

    $validateButton = New-Object System.Windows.Forms.Button
    $validateButton.Text = "Validate"
    $validateButton.Left = 390
    $validateButton.Top = 665
    $validateButton.Width = 90
    $validateButton.Add_Click({
        try {
            Sync-ContextFromGui
            [void](Invoke-LauncherAction "validate-environment")
            $outputBox.Text = "Validate environment OK.`r`nLog: $script:LauncherLogPath"
        }
        catch {
            $outputBox.Text = $_.Exception.Message
        }
    })
    $form.Controls.Add($validateButton)

    $closeButton = New-Object System.Windows.Forms.Button
    $closeButton.Text = "Close"
    $closeButton.Left = 490
    $closeButton.Top = 665
    $closeButton.Width = 90
    $closeButton.Add_Click({ $form.Close() })
    $form.Controls.Add($closeButton)

    Update-CommandPreview

    if ($AutoCloseGuiForCheck) {
        $timer = New-Object System.Windows.Forms.Timer
        $timer.Interval = 3000
        $timer.Add_Tick({
            $timer.Stop()
            $form.Close()
        })
        $timer.Start()
    }

    [void]$form.ShowDialog()
}

Set-LauncherContext $ProjectRoot

try {
    if ($PreviewOnly) {
        Assert-ReportDate $script:ReportDate
        Assert-RetrospectiveYears $script:RetrospectiveYears
        Assert-DeleteConfirmation $script:Action $script:ConfirmDelete
        Assert-BundleConfirmation $script:Action $script:ConfirmBundle
        $preview = Format-CommandPreview $script:Action
        Write-LauncherLog ("PreviewOnly: {0}" -f $preview)
        Write-Host $preview
        exit 0
    }

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

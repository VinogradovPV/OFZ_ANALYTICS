Attribute VB_Name = "OfzLauncher"
Option Explicit

' OFZ Analytics Word launcher source module.
' Import this .bas file into a trusted .docm release artifact.
' Do not commit .docm files without a separate artifact policy decision.

Private Const DEFAULT_REPORT_DATE As String = "2026-05-01"
Private Const DEFAULT_RETROSPECTIVE_YEARS As Long = 4
Private Const DEFAULT_PERIOD_TYPE As String = "month"
Private Const DEFAULT_AGGREGATION_MODE As String = "cumulative"
Private Const ENV_PROJECT_ROOT As String = "OFZ_PROJECT_ROOT"

Public Sub OfzValidateEnvironment()
    Dim projectRoot As String
    projectRoot = OfzProjectRoot()
    ValidateProjectEnvironment projectRoot
    MsgBox "OFZ Analytics environment OK." & vbCrLf & projectRoot, vbInformation, "OFZ Launcher"
End Sub

Public Sub OfzSmokeTest()
    Dim projectRoot As String
    Dim blocked As Boolean

    projectRoot = OfzProjectRoot()
    ValidateProjectEnvironment projectRoot
    ValidateReportDate DEFAULT_REPORT_DATE
    ValidateRetrospectiveYears DEFAULT_RETROSPECTIVE_YEARS
    ValidatePeriodType DEFAULT_PERIOD_TYPE
    ValidateAggregationMode DEFAULT_AGGREGATION_MODE

    blocked = False
    On Error Resume Next
    ValidateReportDate "2026-05-15"
    blocked = (Err.Number <> 0)
    Err.Clear
    On Error GoTo 0
    If Not blocked Then
        Err.Raise vbObjectError + 100, , "Bad date validation did not fail."
    End If

    blocked = False
    On Error Resume Next
    ValidateSafetyGate "cleanup-delete-all-with-archive", vbNullString
    blocked = (Err.Number <> 0)
    Err.Clear
    On Error GoTo 0
    If Not blocked Then
        Err.Raise vbObjectError + 101, , "Delete confirmation validation did not fail."
    End If

    blocked = False
    On Error Resume Next
    ValidateSafetyGate "release-build", vbNullString
    blocked = (Err.Number <> 0)
    Err.Clear
    On Error GoTo 0
    If Not blocked Then
        Err.Raise vbObjectError + 102, , "Bundle confirmation validation did not fail."
    End If

    MsgBox "OFZ Word launcher smoke OK." & vbCrLf & _
           "Environment validated; bad date, delete and bundle gates blocked.", _
           vbInformation, "OFZ Launcher"
End Sub

Public Function OfzRunAction(Optional ByVal actionName As String = "validate", Optional ByVal confirmToken As String = "") As Long
    Dim projectRoot As String
    Dim commandLine As String
    Dim logPath As String

    projectRoot = OfzProjectRoot()
    ValidateProjectEnvironment projectRoot
    ValidateAction actionName
    ValidateReportDate DEFAULT_REPORT_DATE
    ValidateRetrospectiveYears DEFAULT_RETROSPECTIVE_YEARS
    ValidatePeriodType DEFAULT_PERIOD_TYPE
    ValidateAggregationMode DEFAULT_AGGREGATION_MODE
    ValidateSafetyGate actionName, confirmToken

    If actionName = "validate" Then
        OfzRunAction = 0
        MsgBox "OFZ Analytics environment OK.", vbInformation, "OFZ Launcher"
        Exit Function
    End If

    logPath = CreateLauncherLogPath(projectRoot)
    commandLine = BuildCommandLine(projectRoot, actionName)
    OfzRunAction = ExecuteCommand(commandLine, projectRoot, logPath)

    MsgBox "Action: " & actionName & vbCrLf & _
           "Exit code: " & CStr(OfzRunAction) & vbCrLf & _
           "Log: " & logPath, vbInformation, "OFZ Launcher"
End Function

Private Function OfzProjectRoot() As String
    Dim envRoot As String
    envRoot = Environ$(ENV_PROJECT_ROOT)

    If Len(Trim$(envRoot)) > 0 Then
        OfzProjectRoot = envRoot
    Else
        OfzProjectRoot = CurDir$
    End If
End Function

Private Sub ValidateProjectEnvironment(ByVal projectRoot As String)
    RequireFolder projectRoot, "project_root"
    RequireFile CombinePath(projectRoot, "pyproject.toml"), "pyproject.toml"
    RequireFolder CombinePath(projectRoot, ".venv\Scripts"), ".venv\Scripts"
    RequireFolder CombinePath(projectRoot, "data\raw"), "data\raw"
End Sub

Private Sub ValidateReportDate(ByVal value As String)
    Dim yyyy As Long
    Dim mm As Long
    Dim dd As Long
    Dim parsed As Date

    If Len(value) <> 10 Then
        Err.Raise vbObjectError + 200, , "report_date must use YYYY-MM-DD format."
    End If
    If Mid$(value, 5, 1) <> "-" Or Mid$(value, 8, 1) <> "-" Then
        Err.Raise vbObjectError + 201, , "report_date must use YYYY-MM-DD format."
    End If
    If Not IsNumeric(Left$(value, 4)) Or Not IsNumeric(Mid$(value, 6, 2)) Or Not IsNumeric(Right$(value, 2)) Then
        Err.Raise vbObjectError + 202, , "report_date must use YYYY-MM-DD format."
    End If

    yyyy = CLng(Left$(value, 4))
    mm = CLng(Mid$(value, 6, 2))
    dd = CLng(Right$(value, 2))
    parsed = DateSerial(yyyy, mm, dd)

    If Year(parsed) <> yyyy Or Month(parsed) <> mm Or Day(parsed) <> dd Then
        Err.Raise vbObjectError + 203, , "report_date is not a valid calendar date."
    End If
    If dd <> 1 Then
        Err.Raise vbObjectError + 204, , "report_date must be the first day of a month."
    End If
End Sub

Private Sub ValidateRetrospectiveYears(ByVal value As Long)
    If value < 1 Or value > 10 Then
        Err.Raise vbObjectError + 205, , "retrospective_years must be in range 1..10."
    End If
End Sub

Private Sub ValidatePeriodType(ByVal value As String)
    Select Case value
        Case "month", "quarter", "year"
            Exit Sub
        Case Else
            Err.Raise vbObjectError + 206, , "Unsupported period_type."
    End Select
End Sub

Private Sub ValidateAggregationMode(ByVal value As String)
    Select Case value
        Case "cumulative", "point"
            Exit Sub
        Case Else
            Err.Raise vbObjectError + 207, , "Unsupported aggregation_mode."
    End Select
End Sub

Private Sub ValidateAction(ByVal actionName As String)
    Select Case actionName
        Case "validate", "run", "schema", "quality-fast", "quality-full", _
             "cleanup-dry-run", "cleanup-archive-all", "cleanup-delete-all-with-archive", _
             "release-dry-run", "release-build"
            Exit Sub
        Case Else
            Err.Raise vbObjectError + 208, , "Unsupported action."
    End Select
End Sub

Private Sub ValidateSafetyGate(ByVal actionName As String, ByVal confirmToken As String)
    If actionName = "cleanup-delete-all-with-archive" And confirmToken <> "DELETE_OUTPUTS" Then
        Err.Raise vbObjectError + 209, , "Delete cleanup is blocked. Use DELETE_OUTPUTS."
    End If

    If actionName = "release-build" And confirmToken <> "BUILD_RELEASE_BUNDLE" Then
        Err.Raise vbObjectError + 210, , "Release bundle creation is blocked. Use BUILD_RELEASE_BUNDLE."
    End If
End Sub

Private Function BuildCommandLine(ByVal projectRoot As String, ByVal actionName As String) As String
    Dim cliPath As String
    Dim args As String

    Select Case actionName
        Case "run"
            cliPath = CliPath(projectRoot, "ofz-run.exe")
            args = CommonArgs()
        Case "schema"
            cliPath = CliPath(projectRoot, "ofz-schema.exe")
            args = CommonArgs()
        Case "quality-fast"
            cliPath = CliPath(projectRoot, "ofz-quality.exe")
            args = "--fast " & CommonArgs()
        Case "quality-full"
            cliPath = CliPath(projectRoot, "ofz-quality.exe")
            args = "--full " & CommonArgs()
        Case "cleanup-dry-run"
            cliPath = CliPath(projectRoot, "ofz-clean-outputs.exe")
            args = "--dry-run"
        Case "cleanup-archive-all"
            cliPath = CliPath(projectRoot, "ofz-clean-outputs.exe")
            args = "--archive-all"
        Case "cleanup-delete-all-with-archive"
            cliPath = CliPath(projectRoot, "ofz-clean-outputs.exe")
            args = "--archive-all --delete-all --confirm DELETE_OUTPUTS"
        Case "release-dry-run"
            cliPath = CliPath(projectRoot, "ofz-build-release-bundle.exe")
            args = "--dry-run " & CommonArgs()
        Case "release-build"
            cliPath = CliPath(projectRoot, "ofz-build-release-bundle.exe")
            args = "--include-outputs --confirm BUILD_RELEASE_BUNDLE " & CommonArgs()
        Case Else
            Err.Raise vbObjectError + 211, , "Unsupported action."
    End Select

    BuildCommandLine = QuoteArg(cliPath) & " " & args
End Function

Private Function CommonArgs() As String
    CommonArgs = "--report-date " & QuoteArg(DEFAULT_REPORT_DATE) & _
                 " --retrospective-years " & CStr(DEFAULT_RETROSPECTIVE_YEARS) & _
                 " --period-type " & QuoteArg(DEFAULT_PERIOD_TYPE) & _
                 " --aggregation-mode " & QuoteArg(DEFAULT_AGGREGATION_MODE)
End Function

Private Function CliPath(ByVal projectRoot As String, ByVal cliName As String) As String
    Select Case cliName
        Case "ofz-run.exe", "ofz-interactive.exe", "ofz-quality.exe", _
             "ofz-clean-outputs.exe", "ofz-schema.exe", "ofz-build-release-bundle.exe"
            CliPath = CombinePath(projectRoot, ".venv\Scripts\" & cliName)
            RequireFile CliPath, cliName
        Case Else
            Err.Raise vbObjectError + 212, , "CLI is not whitelisted."
    End Select
End Function

Private Function ExecuteCommand(ByVal commandLine As String, ByVal projectRoot As String, ByVal logPath As String) As Long
    Dim shell As Object
    Dim exec As Object
    Dim stdoutText As String
    Dim stderrText As String

    WriteLog logPath, "Working directory: " & projectRoot
    WriteLog logPath, "Command preview: " & commandLine

    Set shell = CreateObject("WScript.Shell")
    shell.CurrentDirectory = projectRoot
    Set exec = shell.Exec(commandLine)

    Do While exec.Status = 0
        DoEvents
    Loop

    stdoutText = exec.StdOut.ReadAll
    stderrText = exec.StdErr.ReadAll

    If Len(stdoutText) > 0 Then
        WriteLog logPath, "STDOUT:"
        WriteLog logPath, stdoutText
    End If
    If Len(stderrText) > 0 Then
        WriteLog logPath, "STDERR:"
        WriteLog logPath, stderrText
    End If

    WriteLog logPath, "Exit code: " & CStr(exec.ExitCode)
    ExecuteCommand = exec.ExitCode
End Function

Private Function CreateLauncherLogPath(ByVal projectRoot As String) As String
    Dim logDir As String
    logDir = CombinePath(projectRoot, "outputs\reports\launcher")
    CreateFolderRecursive logDir
    CreateLauncherLogPath = CombinePath(logDir, "word_launcher_run_" & Format$(Now, "yyyymmdd_hhnnss") & ".log")
End Function

Private Sub WriteLog(ByVal logPath As String, ByVal message As String)
    Dim fso As Object
    Dim stream As Object

    Set fso = CreateObject("Scripting.FileSystemObject")
    Set stream = fso.OpenTextFile(logPath, 8, True)
    stream.WriteLine "[" & Format$(Now, "yyyy-mm-dd hh:nn:ss") & "] " & message
    stream.Close
End Sub

Private Function CombinePath(ByVal leftPart As String, ByVal rightPart As String) As String
    If Right$(leftPart, 1) = "\" Then
        CombinePath = leftPart & rightPart
    Else
        CombinePath = leftPart & "\" & rightPart
    End If
End Function

Private Function QuoteArg(ByVal value As String) As String
    QuoteArg = """" & Replace(value, """", """""") & """"
End Function

Private Sub RequireFile(ByVal pathValue As String, ByVal label As String)
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    If Not fso.FileExists(pathValue) Then
        Err.Raise vbObjectError + 300, , "Required file is missing: " & label & " (" & pathValue & ")"
    End If
End Sub

Private Sub RequireFolder(ByVal pathValue As String, ByVal label As String)
    Dim fso As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    If Not fso.FolderExists(pathValue) Then
        Err.Raise vbObjectError + 301, , "Required folder is missing: " & label & " (" & pathValue & ")"
    End If
End Sub

Private Sub CreateFolderRecursive(ByVal folderPath As String)
    Dim fso As Object
    Dim parentPath As String

    Set fso = CreateObject("Scripting.FileSystemObject")
    If fso.FolderExists(folderPath) Then
        Exit Sub
    End If

    parentPath = fso.GetParentFolderName(folderPath)
    If Len(parentPath) > 0 And Not fso.FolderExists(parentPath) Then
        CreateFolderRecursive parentPath
    End If

    fso.CreateFolder folderPath
End Sub

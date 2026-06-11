Attribute VB_Name = "OfzLauncher"
Option Explicit

Public Const OFZ_DEFAULT_REPORT_DATE As String = "2026-05-01"
Public Const OFZ_DEFAULT_RETROSPECTIVE_YEARS As String = "4"
Public Const OFZ_DEFAULT_PERIOD_TYPE As String = "month"
Public Const OFZ_DEFAULT_AGGREGATION_MODE As String = "cumulative"

Private Const OFZ_DELETE_CONFIRM As String = "DELETE_OUTPUTS"
Private Const OFZ_RELEASE_CONFIRM As String = "BUILD_RELEASE_BUNDLE"

Public Sub OFZ_ShowLauncher()
    frmOfzLauncher.Show
End Sub

Public Sub OFZ_RunPipeline()
    OFZ_RunAction "run-pipeline"
End Sub

Public Sub OFZ_RunSchemaValidation()
    OFZ_RunAction "schema"
End Sub

Public Sub OFZ_RunQualityGateFast()
    OFZ_RunAction "quality-fast"
End Sub

Public Sub OFZ_RunQualityGateFull()
    OFZ_RunAction "quality-full"
End Sub

Public Sub OFZ_CleanupDryRun()
    OFZ_RunAction "cleanup-dry-run"
End Sub

Public Sub OFZ_CleanupArchiveAll()
    OFZ_RunAction "cleanup-archive-all"
End Sub

Public Sub OFZ_CleanupDeleteAll()
    OFZ_RunAction "cleanup-delete-all", OFZ_DELETE_CONFIRM
End Sub

Public Sub OFZ_ReleaseBundleDryRun()
    OFZ_RunAction "release-dry-run"
End Sub

Public Sub OFZ_ReleaseBundleBuild()
    OFZ_RunAction "release-build", "", OFZ_RELEASE_CONFIRM
End Sub

Public Sub OFZ_OpenOutputsFolder()
    OFZ_OpenSafeFolder OFZ_CombinePath(OFZ_DefaultProjectRoot(), "outputs")
End Sub

Public Sub OFZ_OpenReleasesFolder()
    OFZ_OpenSafeFolder OFZ_CombinePath(OFZ_DefaultProjectRoot(), "releases")
End Sub

Public Function OFZ_DefaultProjectRoot() As String
    Dim envRoot As String
    envRoot = Trim$(Environ$("OFZ_PROJECT_ROOT"))
    If Len(envRoot) > 0 Then
        OFZ_DefaultProjectRoot = envRoot
    Else
        OFZ_DefaultProjectRoot = CurDir$
    End If
End Function

Public Function OFZ_ValidateProjectRoot(projectRoot As String) As Boolean
    Dim root As String
    root = OFZ_NormalizePath(projectRoot)
    OFZ_ValidateProjectRoot = False

    If Len(root) = 0 Then Exit Function
    If Dir$(root, vbDirectory) = vbNullString Then Exit Function
    If Dir$(OFZ_CombinePath(root, "pyproject.toml")) = vbNullString Then Exit Function
    If Dir$(OFZ_CombinePath(root, ".venv\Scripts"), vbDirectory) = vbNullString Then Exit Function
    If Dir$(OFZ_CombinePath(root, "data\raw"), vbDirectory) = vbNullString Then Exit Function

    OFZ_ValidateProjectRoot = True
End Function

Public Function OFZ_ValidateReportDate(reportDate As String) As Boolean
    On Error GoTo InvalidDate

    Dim yyyy As Integer
    Dim mm As Integer
    Dim dd As Integer
    Dim parsed As Date

    OFZ_ValidateReportDate = False
    If Len(reportDate) <> 10 Then Exit Function
    If Mid$(reportDate, 5, 1) <> "-" Or Mid$(reportDate, 8, 1) <> "-" Then Exit Function
    If Not IsNumeric(Left$(reportDate, 4)) Then Exit Function
    If Not IsNumeric(Mid$(reportDate, 6, 2)) Then Exit Function
    If Not IsNumeric(Right$(reportDate, 2)) Then Exit Function

    yyyy = CInt(Left$(reportDate, 4))
    mm = CInt(Mid$(reportDate, 6, 2))
    dd = CInt(Right$(reportDate, 2))
    parsed = DateSerial(yyyy, mm, dd)

    If Year(parsed) <> yyyy Or Month(parsed) <> mm Or Day(parsed) <> dd Then Exit Function
    If dd <> 1 Then Exit Function

    OFZ_ValidateReportDate = True
    Exit Function

InvalidDate:
    OFZ_ValidateReportDate = False
End Function

Public Function OFZ_ValidateRetrospectiveYears(value As String) As Boolean
    Dim n As Integer
    OFZ_ValidateRetrospectiveYears = False
    If Len(Trim$(value)) = 0 Then Exit Function
    If Not IsNumeric(value) Then Exit Function
    n = CInt(value)
    OFZ_ValidateRetrospectiveYears = (n >= 1 And n <= 10 And CStr(n) = Trim$(value))
End Function

Public Function OFZ_BuildCommand( _
    ByVal projectRoot As String, _
    ByVal actionName As String, _
    ByVal reportDate As String, _
    ByVal retrospectiveYears As String, _
    ByVal periodType As String, _
    ByVal aggregationMode As String, _
    Optional ByVal deleteConfirm As String = "", _
    Optional ByVal releaseConfirm As String = "" _
) As String
    Dim root As String
    Dim commonArgs As String
    Dim action As String

    root = OFZ_NormalizePath(projectRoot)
    action = LCase$(Trim$(actionName))

    If Not OFZ_ValidateProjectRoot(root) Then Err.Raise vbObjectError + 100, , "Invalid project_root"
    If Not OFZ_ValidateReportDate(reportDate) Then Err.Raise vbObjectError + 101, , "Invalid report_date; expected YYYY-MM-DD and first day of month"
    If Not OFZ_ValidateRetrospectiveYears(retrospectiveYears) Then Err.Raise vbObjectError + 102, , "Invalid retrospective_years; expected integer 1..10"
    If Not OFZ_IsAllowedValue(periodType, "month,quarter,year") Then Err.Raise vbObjectError + 103, , "Invalid period_type"
    If Not OFZ_IsAllowedValue(aggregationMode, "cumulative,point") Then Err.Raise vbObjectError + 104, , "Invalid aggregation_mode"

    commonArgs = " --report-date " & OFZ_QuoteArg(reportDate) & _
        " --retrospective-years " & OFZ_QuoteArg(retrospectiveYears) & _
        " --period-type " & OFZ_QuoteArg(periodType) & _
        " --aggregation-mode " & OFZ_QuoteArg(aggregationMode)

    Select Case action
        Case "validate-environment"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-schema.exe")) & " --help"
        Case "run-pipeline"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-run.exe")) & commonArgs
        Case "schema"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-schema.exe")) & commonArgs
        Case "quality-fast"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-quality.exe")) & " --fast" & commonArgs
        Case "quality-full"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-quality.exe")) & " --full" & commonArgs
        Case "cleanup-dry-run"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-clean-outputs.exe")) & " --dry-run"
        Case "cleanup-archive-all"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-clean-outputs.exe")) & " --archive-all"
        Case "cleanup-delete-all"
            If deleteConfirm <> OFZ_DELETE_CONFIRM Then Err.Raise vbObjectError + 105, , "DELETE_OUTPUTS confirmation is required"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-clean-outputs.exe")) & " --archive-all --delete-all --confirm " & OFZ_QuoteArg(OFZ_DELETE_CONFIRM)
        Case "release-dry-run"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-build-release-bundle.exe")) & " --dry-run" & commonArgs
        Case "release-build"
            If releaseConfirm <> OFZ_RELEASE_CONFIRM Then Err.Raise vbObjectError + 106, , "BUILD_RELEASE_BUNDLE confirmation is required"
            OFZ_BuildCommand = OFZ_QuoteArg(OFZ_CliPath(root, "ofz-build-release-bundle.exe")) & " --include-outputs --confirm " & OFZ_QuoteArg(OFZ_RELEASE_CONFIRM) & commonArgs
        Case "open-outputs", "open-releases"
            OFZ_BuildCommand = action
        Case Else
            Err.Raise vbObjectError + 107, , "Action is not whitelisted"
    End Select
End Function

Public Function OFZ_RunCommand(commandLine As String, workingDirectory As String) As Long
    Dim shellObj As Object
    Dim execObj As Object
    Dim logPath As String
    Dim stdoutText As String
    Dim stderrText As String

    If Not OFZ_ValidateProjectRoot(workingDirectory) Then Err.Raise vbObjectError + 120, , "Invalid working directory"
    If Not OFZ_IsWhitelistedCommandLine(commandLine, workingDirectory) Then Err.Raise vbObjectError + 121, , "Command is not approved by the Word launcher whitelist"

    logPath = OFZ_LogPath(workingDirectory)
    Set shellObj = CreateObject("WScript.Shell")
    shellObj.CurrentDirectory = OFZ_NormalizePath(workingDirectory)

    OFZ_AppendLog logPath, "Working directory: " & OFZ_NormalizePath(workingDirectory)
    OFZ_AppendLog logPath, "Command: " & commandLine

    Set execObj = shellObj.Exec(commandLine)
    Do While execObj.Status = 0
        DoEvents
    Loop

    stdoutText = execObj.StdOut.ReadAll
    stderrText = execObj.StdErr.ReadAll

    OFZ_AppendLog logPath, "Exit code: " & CStr(execObj.ExitCode)
    If Len(stdoutText) > 0 Then OFZ_AppendLog logPath, "STDOUT:" & vbCrLf & stdoutText
    If Len(stderrText) > 0 Then OFZ_AppendLog logPath, "STDERR:" & vbCrLf & stderrText

    OFZ_RunCommand = CLng(execObj.ExitCode)
End Function

Public Function OFZ_LogPath(projectRoot As String) As String
    Dim logDir As String
    logDir = OFZ_CombinePath(OFZ_NormalizePath(projectRoot), "outputs\reports\launcher")
    OFZ_CreateFolderRecursive logDir
    OFZ_LogPath = OFZ_CombinePath(logDir, "word_launcher_run_" & Format$(Now, "yyyymmdd_hhnnss") & ".log")
End Function

Public Sub OFZ_RunAction( _
    ByVal actionName As String, _
    Optional ByVal deleteConfirm As String = "", _
    Optional ByVal releaseConfirm As String = "" _
)
    Dim root As String
    Dim commandLine As String
    Dim exitCode As Long

    root = OFZ_DefaultProjectRoot()
    commandLine = OFZ_BuildCommand(root, actionName, OFZ_DEFAULT_REPORT_DATE, OFZ_DEFAULT_RETROSPECTIVE_YEARS, OFZ_DEFAULT_PERIOD_TYPE, OFZ_DEFAULT_AGGREGATION_MODE, deleteConfirm, releaseConfirm)

    If commandLine = "open-outputs" Then
        OFZ_OpenOutputsFolder
        Exit Sub
    End If
    If commandLine = "open-releases" Then
        OFZ_OpenReleasesFolder
        Exit Sub
    End If

    exitCode = OFZ_RunCommand(commandLine, root)
    MsgBox "OFZ launcher finished with exit code " & CStr(exitCode), vbInformation, "OFZ Analytics"
End Sub

Public Function OFZ_IsAllowedValue(ByVal value As String, ByVal csvValues As String) As Boolean
    Dim items() As String
    Dim item As Variant
    items = Split(csvValues, ",")
    For Each item In items
        If LCase$(Trim$(value)) = LCase$(Trim$(CStr(item))) Then
            OFZ_IsAllowedValue = True
            Exit Function
        End If
    Next item
    OFZ_IsAllowedValue = False
End Function

Public Function OFZ_CombinePath(ByVal leftPart As String, ByVal rightPart As String) As String
    If Right$(leftPart, 1) = "\" Then
        OFZ_CombinePath = leftPart & rightPart
    Else
        OFZ_CombinePath = leftPart & "\" & rightPart
    End If
End Function

Public Function OFZ_NormalizePath(ByVal pathValue As String) As String
    OFZ_NormalizePath = Trim$(Replace(pathValue, "/", "\"))
End Function

Public Function OFZ_QuoteArg(ByVal value As String) As String
    OFZ_QuoteArg = """" & Replace(value, """", """""") & """"
End Function

Private Function OFZ_CliPath(ByVal projectRoot As String, ByVal cliName As String) As String
    Dim pathValue As String
    pathValue = OFZ_CombinePath(OFZ_CombinePath(projectRoot, ".venv\Scripts"), cliName)
    If Dir$(pathValue) = vbNullString Then Err.Raise vbObjectError + 130, , "Missing CLI entry point: " & pathValue
    OFZ_CliPath = pathValue
End Function

Private Function OFZ_IsWhitelistedCommandLine(ByVal commandLine As String, ByVal projectRoot As String) As Boolean
    Dim allowed As Variant
    Dim cliName As Variant
    allowed = Array("ofz-run.exe", "ofz-schema.exe", "ofz-quality.exe", "ofz-clean-outputs.exe", "ofz-build-release-bundle.exe")

    For Each cliName In allowed
        If InStr(1, commandLine, OFZ_QuoteArg(OFZ_CliPath(projectRoot, CStr(cliName))), vbTextCompare) = 1 Then
            OFZ_IsWhitelistedCommandLine = True
            Exit Function
        End If
    Next cliName

    OFZ_IsWhitelistedCommandLine = False
End Function

Private Sub OFZ_CreateFolderRecursive(ByVal folderPath As String)
    Dim parts() As String
    Dim currentPath As String
    Dim i As Long

    parts = Split(OFZ_NormalizePath(folderPath), "\")
    currentPath = parts(0)
    For i = 1 To UBound(parts)
        currentPath = currentPath & "\" & parts(i)
        If Len(currentPath) > 2 Then
            If Dir$(currentPath, vbDirectory) = vbNullString Then MkDir currentPath
        End If
    Next i
End Sub

Private Sub OFZ_AppendLog(ByVal logPath As String, ByVal message As String)
    Dim fileNo As Integer
    fileNo = FreeFile
    Open logPath For Append As #fileNo
    Print #fileNo, Format$(Now, "yyyy-mm-dd hh:nn:ss") & " | " & message
    Close #fileNo
End Sub

Private Sub OFZ_OpenSafeFolder(ByVal folderPath As String)
    Dim shellObj As Object
    If Dir$(folderPath, vbDirectory) = vbNullString Then MkDir folderPath
    Set shellObj = CreateObject("WScript.Shell")
    shellObj.Run "explorer.exe " & OFZ_QuoteArg(folderPath), 1, False
End Sub


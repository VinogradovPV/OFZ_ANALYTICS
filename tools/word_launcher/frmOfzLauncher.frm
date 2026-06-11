VERSION 5.00
Begin VB.UserForm frmOfzLauncher
   Caption         =   "OFZ Analytics Launcher"
   ClientHeight    =   9000
   ClientLeft      =   120
   ClientTop       =   465
   ClientWidth     =   10800
   StartUpPosition =   1  'CenterOwner
   Begin MSForms.TextBox txtProjectRoot
      Height          =   300
      Left            =   180
      TabIndex        =   0
      Top             =   420
      Width           =   7200
   End
   Begin MSForms.CommandButton btnBrowseProjectRoot
      Caption         =   "Browse"
      Height          =   300
      Left            =   7560
      TabIndex        =   1
      Top             =   420
      Width           =   1200
   End
   Begin MSForms.CommandButton btnValidateProject
      Caption         =   "Validate"
      Height          =   300
      Left            =   8880
      TabIndex        =   2
      Top             =   420
      Width           =   1200
   End
   Begin MSForms.TextBox txtReportDate
      Height          =   300
      Left            =   180
      TabIndex        =   3
      Top             =   1140
      Width           =   1440
   End
   Begin MSForms.ComboBox cmbRetrospectiveYears
      Height          =   300
      Left            =   1800
      TabIndex        =   4
      Top             =   1140
      Width           =   960
   End
   Begin MSForms.ComboBox cmbPeriodType
      Height          =   300
      Left            =   2940
      TabIndex        =   5
      Top             =   1140
      Width           =   1260
   End
   Begin MSForms.ComboBox cmbAggregationMode
      Height          =   300
      Left            =   4380
      TabIndex        =   6
      Top             =   1140
      Width           =   1500
   End
   Begin MSForms.ComboBox cmbAction
      Height          =   300
      Left            =   6060
      TabIndex        =   7
      Top             =   1140
      Width           =   2460
   End
   Begin MSForms.CheckBox chkRunSchema
      Caption         =   "Schema"
      Height          =   240
      Left            =   180
      TabIndex        =   8
      Top             =   1800
      Width           =   960
   End
   Begin MSForms.CheckBox chkRunQualityFast
      Caption         =   "Quality fast"
      Height          =   240
      Left            =   1260
      TabIndex        =   9
      Top             =   1800
      Width           =   1320
   End
   Begin MSForms.CheckBox chkRunQualityFull
      Caption         =   "Quality full"
      Height          =   240
      Left            =   2760
      TabIndex        =   10
      Top             =   1800
      Width           =   1320
   End
   Begin MSForms.CheckBox chkBuildReleaseBundle
      Caption         =   "Build release bundle"
      Height          =   240
      Left            =   4260
      TabIndex        =   11
      Top             =   1800
      Width           =   2100
   End
   Begin MSForms.CheckBox chkOpenOutputs
      Caption         =   "Open outputs"
      Height          =   240
      Left            =   6540
      TabIndex        =   12
      Top             =   1800
      Width           =   1500
   End
   Begin MSForms.CheckBox chkOpenReleases
      Caption         =   "Open releases"
      Height          =   240
      Left            =   8220
      TabIndex        =   13
      Top             =   1800
      Width           =   1500
   End
   Begin MSForms.TextBox txtDeleteConfirm
      Height          =   300
      Left            =   180
      TabIndex        =   14
      Top             =   2460
      Width           =   2400
   End
   Begin MSForms.TextBox txtReleaseConfirm
      Height          =   300
      Left            =   2820
      TabIndex        =   15
      Top             =   2460
      Width           =   2760
   End
   Begin MSForms.TextBox txtCommandPreview
      Height          =   1320
      Left            =   180
      MultiLine       =   -1
      TabIndex        =   16
      Top             =   3300
      Width           =   9840
   End
   Begin MSForms.TextBox txtLogOutput
      Height          =   2340
      Left            =   180
      MultiLine       =   -1
      ScrollBars      =   2
      TabIndex        =   17
      Top             =   5100
      Width           =   9840
   End
   Begin MSForms.CommandButton btnPreviewCommand
      Caption         =   "Preview"
      Height          =   360
      Left            =   180
      TabIndex        =   18
      Top             =   7860
      Width           =   1200
   End
   Begin MSForms.CommandButton btnRun
      Caption         =   "Run"
      Height          =   360
      Left            =   1560
      TabIndex        =   19
      Top             =   7860
      Width           =   1200
   End
   Begin MSForms.CommandButton btnOpenOutputs
      Caption         =   "Outputs"
      Height          =   360
      Left            =   2940
      TabIndex        =   20
      Top             =   7860
      Width           =   1200
   End
   Begin MSForms.CommandButton btnOpenReleases
      Caption         =   "Releases"
      Height          =   360
      Left            =   4320
      TabIndex        =   21
      Top             =   7860
      Width           =   1200
   End
   Begin MSForms.CommandButton btnClose
      Caption         =   "Close"
      Height          =   360
      Left            =   8820
      TabIndex        =   22
      Top             =   7860
      Width           =   1200
   End
End
Attribute VB_Name = "frmOfzLauncher"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub UserForm_Initialize()
    Dim i As Integer

    txtProjectRoot.Text = OFZ_DefaultProjectRoot()
    txtReportDate.Text = OFZ_DEFAULT_REPORT_DATE

    For i = 1 To 10
        cmbRetrospectiveYears.AddItem CStr(i)
    Next i
    cmbRetrospectiveYears.Value = OFZ_DEFAULT_RETROSPECTIVE_YEARS

    cmbPeriodType.AddItem "month"
    cmbPeriodType.AddItem "quarter"
    cmbPeriodType.AddItem "year"
    cmbPeriodType.Value = OFZ_DEFAULT_PERIOD_TYPE

    cmbAggregationMode.AddItem "cumulative"
    cmbAggregationMode.AddItem "point"
    cmbAggregationMode.Value = OFZ_DEFAULT_AGGREGATION_MODE

    cmbAction.AddItem "validate-environment"
    cmbAction.AddItem "run-pipeline"
    cmbAction.AddItem "schema"
    cmbAction.AddItem "quality-fast"
    cmbAction.AddItem "quality-full"
    cmbAction.AddItem "cleanup-dry-run"
    cmbAction.AddItem "cleanup-archive-all"
    cmbAction.AddItem "cleanup-delete-all"
    cmbAction.AddItem "release-dry-run"
    cmbAction.AddItem "release-build"
    cmbAction.AddItem "open-outputs"
    cmbAction.AddItem "open-releases"
    cmbAction.Value = "validate-environment"

    txtDeleteConfirm.Text = ""
    txtReleaseConfirm.Text = ""
    RefreshPreview
End Sub

Private Sub btnValidateProject_Click()
    If OFZ_ValidateProjectRoot(txtProjectRoot.Text) Then
        txtLogOutput.Text = "Project root OK: " & txtProjectRoot.Text
    Else
        txtLogOutput.Text = "Project root failed validation."
    End If
End Sub

Private Sub btnBrowseProjectRoot_Click()
    txtLogOutput.Text = "Select the project root by typing the path. Arbitrary shell commands are not accepted."
End Sub

Private Sub btnPreviewCommand_Click()
    RefreshPreview
End Sub

Private Sub btnRun_Click()
    Dim commandLine As String
    Dim exitCode As Long

    On Error GoTo RunFailed
    RefreshPreview
    commandLine = txtCommandPreview.Text

    Select Case cmbAction.Value
        Case "open-outputs"
            OFZ_OpenOutputsFolder
            Exit Sub
        Case "open-releases"
            OFZ_OpenReleasesFolder
            Exit Sub
    End Select

    exitCode = OFZ_RunCommand(commandLine, txtProjectRoot.Text)
    txtLogOutput.Text = "Exit code: " & CStr(exitCode) & vbCrLf & "Log folder: outputs\reports\launcher"
    Exit Sub

RunFailed:
    txtLogOutput.Text = "Blocked or failed: " & Err.Description
End Sub

Private Sub btnOpenOutputs_Click()
    OFZ_OpenOutputsFolder
End Sub

Private Sub btnOpenReleases_Click()
    OFZ_OpenReleasesFolder
End Sub

Private Sub btnClose_Click()
    Unload Me
End Sub

Private Sub cmbAction_Change()
    RefreshPreview
End Sub

Private Sub txtReportDate_Change()
    RefreshPreview
End Sub

Private Sub cmbRetrospectiveYears_Change()
    RefreshPreview
End Sub

Private Sub cmbPeriodType_Change()
    RefreshPreview
End Sub

Private Sub cmbAggregationMode_Change()
    RefreshPreview
End Sub

Private Sub RefreshPreview()
    On Error GoTo PreviewFailed
    txtCommandPreview.Text = OFZ_BuildCommand( _
        txtProjectRoot.Text, _
        cmbAction.Value, _
        txtReportDate.Text, _
        cmbRetrospectiveYears.Value, _
        cmbPeriodType.Value, _
        cmbAggregationMode.Value, _
        txtDeleteConfirm.Text, _
        txtReleaseConfirm.Text _
    )
    Exit Sub

PreviewFailed:
    txtCommandPreview.Text = "Blocked: " & Err.Description
End Sub


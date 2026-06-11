# Word DOCM Build Instructions

Date: 2026-06-11.

## Status

The tracked source for the Word launcher is ready:

- `tools/word_launcher/OfzLauncher.bas`
- `tools/word_launcher/frmOfzLauncher.frm`

The macro-enabled Word document is a release artifact:

- recommended path: `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`;
- do not commit `.docm`;
- do not commit `releases/`.

In this repository step the `.docm` assembly is marked as manual/deferred unless Microsoft Word automation is available on the operator workstation.

## Manual Assembly

1. Open Microsoft Word on the trusted workstation.
2. Create a new blank document.
3. Save it immediately as a macro-enabled document:
   `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`.
4. Add the folder to Word Trusted Locations, or open the document from an already trusted location.
5. Press `Alt+F11` to open the VBA editor.
6. Choose `File -> Import File`.
7. Import `tools/word_launcher/OfzLauncher.bas`.
8. Import `tools/word_launcher/frmOfzLauncher.frm`.
9. If Word asks for a `.frx` file and it is not present, create the form manually using the control list below and paste the code section from `frmOfzLauncher.frm`.
10. Save the document.
11. Run `OFZ_ShowLauncher`.

## Required UserForm

Form name:

- `frmOfzLauncher`

Required controls:

- `txtProjectRoot`
- `btnBrowseProjectRoot`
- `btnValidateProject`
- `txtReportDate`
- `cmbRetrospectiveYears`
- `cmbPeriodType`
- `cmbAggregationMode`
- `cmbAction`
- `chkRunSchema`
- `chkRunQualityFast`
- `chkRunQualityFull`
- `chkBuildReleaseBundle`
- `chkOpenOutputs`
- `chkOpenReleases`
- `txtDeleteConfirm`
- `txtReleaseConfirm`
- `txtCommandPreview`
- `txtLogOutput`
- `btnPreviewCommand`
- `btnRun`
- `btnOpenOutputs`
- `btnOpenReleases`
- `btnClose`

## Manual Verification

Run these checks before sharing the `.docm` as a release artifact:

1. `OFZ_ShowLauncher` opens the form.
2. `txtProjectRoot` points to the OFZ_ANALYTICS project root.
3. `btnValidateProject` confirms `pyproject.toml`, `.venv\Scripts`, and `data\raw`.
4. Invalid `report_date` is blocked.
5. `release-build` is blocked unless `txtReleaseConfirm = BUILD_RELEASE_BUNDLE`.
6. `cleanup-delete-all` is blocked unless `txtDeleteConfirm = DELETE_OUTPUTS`.
7. Command preview contains only one of the approved CLI entry points.
8. Running a command writes a log to `outputs\reports\launcher`.
9. `.docm` remains outside Git.
10. `git status --short` does not show `.docm`, `releases/`, or launcher logs staged.

## Security

- Word macros can be blocked by Microsoft Office security policy.
- Use a Trusted Location for local execution.
- Do not distribute `.docm` without release control.
- Code signing is recommended before broad use.
- The launcher must not accept arbitrary shell commands.
- The launcher calls only whitelisted CLI entry points in `.venv\Scripts`.
- Delete cleanup requires `DELETE_OUTPUTS`.
- Release bundle creation requires `BUILD_RELEASE_BUNDLE`.


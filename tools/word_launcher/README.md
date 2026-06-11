# Word VBA Launcher Source

This folder contains tracked source artifacts for the optional Microsoft Word launcher.

Tracked source:

- `OfzLauncher.bas`
- `frmOfzLauncher.frm`
- `word_docm_build_instructions.md`

Release artifacts, not tracked by default:

- `.docm`
- `.dotm`
- `releases/ui_launcher/*`

The `.docm` file must not be committed unless artifact policy is explicitly changed.

## What The Launcher Does

The Word launcher is a thin UI wrapper around approved OFZ_ANALYTICS CLI entry points. It does not call internal Python functions and does not accept arbitrary shell commands.

Supported CLI:

- `ofz-run.exe`
- `ofz-schema.exe`
- `ofz-quality.exe`
- `ofz-clean-outputs.exe`
- `ofz-build-release-bundle.exe`

## UserForm

Form name:

- `frmOfzLauncher`

The form source includes controls for:

- project root;
- report date;
- retrospective years;
- period type;
- aggregation mode;
- action;
- delete/release confirmation tokens;
- command preview;
- log/output display;
- open outputs/releases buttons.

## Import Into Word

1. Open Microsoft Word.
2. Create a new macro-enabled document.
3. Save it outside Git, for example:
   `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`.
4. Press `Alt+F11`.
5. In VBA editor, choose `File -> Import File`.
6. Import `tools/word_launcher/OfzLauncher.bas`.
7. Import `tools/word_launcher/frmOfzLauncher.frm`.
8. If Word cannot import the form without a `.frx`, create the form manually using `word_docm_build_instructions.md`.
9. Run `OFZ_ShowLauncher`.

## Required Public Procedures

The module exposes:

```vb
OFZ_ShowLauncher
OFZ_RunPipeline
OFZ_RunSchemaValidation
OFZ_RunQualityGateFast
OFZ_RunQualityGateFull
OFZ_CleanupDryRun
OFZ_CleanupArchiveAll
OFZ_CleanupDeleteAll
OFZ_ReleaseBundleDryRun
OFZ_ReleaseBundleBuild
OFZ_OpenOutputsFolder
OFZ_OpenReleasesFolder
```

## Safety

The module:

- calls only whitelisted CLI entry points under `.venv\Scripts`;
- validates project root, report date, period type, aggregation mode and retrospective years;
- blocks cleanup delete without `DELETE_OUTPUTS`;
- blocks release bundle creation without `BUILD_RELEASE_BUNDLE`;
- writes logs to `outputs\reports\launcher`;
- does not create GitHub releases;
- does not accept arbitrary shell commands.

## Manual Checks

If Word is available:

1. Import the `.bas` and `.frm` sources.
2. Run `OFZ_ShowLauncher`.
3. Confirm the form opens.
4. Confirm bad `report_date` is blocked.
5. Confirm `release-build` is blocked without `BUILD_RELEASE_BUNDLE`.
6. Confirm `cleanup-delete-all` is blocked without `DELETE_OUTPUTS`.
7. Confirm command preview contains only approved CLI.
8. Confirm `.docm`, launcher logs and `releases/` are not staged.


# Windows UI launcher MVP

PowerShell launcher is a thin UI wrapper around the approved OFZ Analytics CLI entry points. It does not accept arbitrary shell commands and does not call internal Python functions directly.

## Run smoke check

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

The default action is `smoke`. It validates the project environment, checks that invalid dates are blocked, verifies confirmation gates, runs cleanup dry-run, starts release bundle dry-run, and writes a launcher log.

## Open GUI

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui
```

The GUI exposes only whitelisted actions:

- validate environment;
- run pipeline;
- schema validation;
- quality gate fast;
- cleanup dry-run;
- release bundle dry-run.

## CLI actions

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action validate
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action run
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action schema
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action quality-fast
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action cleanup-dry-run
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action release-dry-run
```

Destructive cleanup requires an explicit confirmation token:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action cleanup-delete-all-with-archive -Confirm DELETE_OUTPUTS
```

Release bundle creation requires an explicit confirmation token:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Action release-build -Confirm BUILD_RELEASE_BUNDLE
```

## Logs

Launcher logs are written to:

```text
outputs/reports/launcher/launcher_run_<timestamp>.log
```

Generated logs and outputs are not committed to Git.

## Safety contract

- Calls only approved CLI entry points.
- Validates `report_date`, `retrospective_years`, `period_type`, `aggregation_mode`, and action.
- Blocks delete cleanup without `DELETE_OUTPUTS`.
- Blocks release bundle creation without `BUILD_RELEASE_BUNDLE`.
- Does not modify `data/raw`.
- Does not create GitHub releases.
- Does not stage or commit generated outputs.

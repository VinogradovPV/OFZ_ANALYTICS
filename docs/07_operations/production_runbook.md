# Production Runbook

Date: 2026-06-05.

This runbook describes the safe production workflow for OFZ_ANALYTICS after Git initialization and artifact policy stabilization.

## Preconditions

- Work from the project root.
- Use only the local virtual environment command style:

```powershell
.\.venv\Scripts\python.exe
```

- `data/raw/` is source data and must not be modified by cleanup commands.
- Generated outputs are not committed to Git.

## Before A Production Run

Check repository state:

```powershell
git status --short --branch
git log --oneline --decorate -5
```

Run dependency and script checks when environment changes:

```powershell
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m compileall -q scripts
```

## Safe Outputs Cleanup

Default inspection:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
```

Archive current working outputs:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
```

Delete working outputs only after explicit confirmation:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

Archive and delete in one controlled command:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all --delete-all --confirm DELETE_OUTPUTS
```

Cleanup guarantees:

- paths outside `outputs/` are never touched;
- `outputs/archive/` is preserved during delete;
- a cleanup manifest is written before deletion;
- skeleton directories are recreated after deletion;
- `.gitkeep` files are restored.

Cleanup reports and manifests under `outputs/` are generated artifacts and are not committed.

## Production Regeneration

Run full pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Run fast quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Git Safety

Before commit:

```powershell
git status --short
git diff --cached --name-only
git diff --cached --name-only | Select-String "outputs/charts|outputs/exports|outputs/reports|outputs/dashboards|outputs/archive|outputs/tmp|data/processed|logs"
```

Only source/config/docs/scripts/contracts/prompts, `data/raw`, and `outputs` skeleton files should be committed. Generated outputs belong in release bundles or external artifacts.

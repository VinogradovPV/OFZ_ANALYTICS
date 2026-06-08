# Scripts Archive Decision

Date: 2026-06-08.

## Decision

Physical archiving of legacy scripts is deferred until P2 / post production-ready v1.

Status: `deferred_until_references_are_resolved`.

No Python files were moved or deleted in this stage. The conservative option was selected because all five archive candidates still have active references in README, documentation, inventories or historical migration materials.

## Reference Scan Scope

References were checked in:

- `README.md`;
- `docs/**`;
- `scripts/**`;
- `pyproject.toml`;
- `scripts/run_pipeline.py`;
- `scripts/quality_gate.py`;
- `scripts/config.py`;
- `scripts/maintenance/**`;
- `docs/index.md`.

## Candidate Table

| Script path | Current status | References found | Referenced by | Production risk | Recommendation | Reason |
|---|---|---|---|---|---|---|
| `scripts/cleanup_docs.py` | legacy docs cleanup utility, `archive_candidate` | yes | `scripts/README.md`; `docs/00_project/scripts_inventory_before_cleanup.md`; `docs/00_project/scripts_structure_plan.md`; `docs/00_project/scripts_migration_plan.md`; `docs/03_pipeline/module_decomposition_plan.md`; `docs/00_project/final_project_summary.md`; historical docs | low direct runtime risk, medium documentation/reference risk | `keep_legacy_until_p2` | Replaced by `scripts/maintenance/cleanup_docs.py`, but still referenced in active docs and inventories. |
| `scripts/migrate_outputs_structure.py` | one-time outputs migration utility, `archive_candidate` | yes | `scripts/README.md`; `docs/00_project/outputs_structure.md`; `docs/00_project/final_project_summary.md`; `docs/00_project/scripts_inventory_before_cleanup.md`; migration/structure docs | low runtime risk, medium historical reproducibility risk | `keep_legacy_until_p2` | Not a production pipeline entry point, but still documents a completed migration path. |
| `scripts/reorganize_outputs.py` | legacy outputs reorganization utility, `archive_candidate` | yes | `README.md`; `scripts/README.md`; `docs/00_project/outputs_structure.md`; `docs/00_project/scripts_inventory_before_cleanup.md`; historical reports/docs | low runtime risk, medium documentation/reference risk | `keep_legacy_until_p2` | Historical utility remains referenced by project docs and README command history. |
| `scripts/maintenance/migrate_legacy_docs_archive.py` | one-time legacy docs archive migration utility, `archive_candidate` | yes | `scripts/README.md`; `docs/00_project/scripts_inventory_before_cleanup.md`; scripts structure/migration docs | low runtime risk, medium historical audit risk | `keep_legacy_until_p2` | Completed migration helper. Keep in place until production-ready v1 and explicit archive step. |
| `scripts/maintenance/reorganize_docs.py` | previous docs reorganization utility, `archive_candidate` | yes | `scripts/README.md`; `docs/00_project/scripts_inventory_before_cleanup.md`; scripts structure/migration docs; docs reorganization materials | low runtime risk, medium documentation/reference risk | `keep_legacy_until_p2` | Superseded by inventory-first cleanup workflow, but still referenced. |

## Current Result

- Physical archive is deferred until references are resolved.
- No files were moved or deleted.
- No entry points were changed.
- Module decomposition remains P2-only.
- Generated outputs were not staged.

## Future Archive Rule

Physical archive is allowed only as a separate future stage after production-ready v1.

Before any future physical move:

1. Remove or update active references in README/docs/scripts plans.
2. Confirm that no candidate is called from `run_pipeline.py`, `quality_gate.py`, `pyproject.toml` entry points or maintenance workflows.
3. Create `scripts/archive/YYYY-MM-DD/README.md` explaining the moved scripts.
4. Run:

```powershell
.\.venv\Scripts\python.exe -m compileall -q scripts
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

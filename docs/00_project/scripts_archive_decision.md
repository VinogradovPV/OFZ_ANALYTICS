# Решение по архивированию scripts

Date: 2026-06-15.

## Решение

P2.10 Controlled legacy scripts archive apply completed.

Status: `archived_to_scripts_archive_2026-06-15`.

Five legacy maintenance scripts were moved to `scripts/archive/2026-06-15/`. No files were deleted.

## Область сканирования ссылок

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

No production entry point, quality gate, package entry point or current maintenance workflow calls the archived scripts.

## Таблица кандидатов

| Script path | Current status | Active production references | Referenced by | Production risk | Recommendation | Reason |
|---|---|---|---|---|---|---|
| `scripts/archive/2026-06-15/cleanup_docs.py` | archived legacy docs cleanup utility | no | archive README; historical inventory docs | low | `archived` | Replaced by `scripts/maintenance/cleanup_docs.py`. |
| `scripts/archive/2026-06-15/migrate_outputs_structure.py` | archived one-time outputs migration utility | no | archive README; historical inventory docs | low | `archived` | Replaced by current outputs policy and `ofz-clean-outputs`. |
| `scripts/archive/2026-06-15/reorganize_outputs.py` | archived legacy outputs reorganization utility | no | archive README; historical inventory docs | low | `archived` | Replaced by current outputs policy and `ofz-clean-outputs`. |
| `scripts/archive/2026-06-15/migrate_legacy_docs_archive.py` | archived one-time legacy docs archive migration utility | no | archive README; historical inventory docs | low | `archived` | Completed migration helper. |
| `scripts/archive/2026-06-15/reorganize_docs.py` | archived previous docs reorganization utility | no | archive README; historical inventory docs | low | `archived` | Superseded by inventory-first cleanup workflow. |

## Текущий результат

- Physical archive was applied.
- Five files were moved to `scripts/archive/2026-06-15/`.
- No files were deleted.
- No entry points were changed.
- Module decomposition remains P2-only.
- Generated outputs were not staged.

## Будущее правило

Archived scripts are audit artifacts. They must not be used for new production runs.

If a future release removes archived scripts, it must be a separate controlled step after stable release, with reference scan, `compileall`, quality gate and explicit approval.

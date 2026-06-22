# Аудит UTF-8 и mojibake

- Дата: `2026-06-22`
- Commit/base commit: `b6fb134` (Git не вызывается из QA-скрипта).
- Корень проверки: `C:\Users\Rockaudit\LLM_CHAT\ofz_analytics`
- Scope: source, tests, docs, configs и другие поддерживаемые текстовые файлы проекта.
- Расширения: `.bat`, `.cfg`, `.css`, `.csv`, `.html`, `.ini`, `.js`, `.json`, `.md`, `.ps1`, `.py`, `.rst`, `.sh`, `.spec`, `.sql`, `.toml`, `.txt`, `.yaml`, `.yml`
- Исключенные каталоги: `.git`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`, `.tmp`, `.venv`, `__pycache__`, `build`, `dist`, `logs`, `outputs`, `releases`, `venv`
- Дополнительные исключения: `data/processed`, весь `outputs` (включая reports/charts/exports/dashboards/archive/tmp/cache).

## Итог

- Проверено файлов: `240`
- Исключено каталогов: `12`
- Invalid UTF-8: `0`
- Файлы с mojibake: `0`
- Allowlisted marker contexts: `0`
- Безопасно исправлено в этом запуске: `0`
- Статус: `PASSED`

## Найденные проблемы и действия

Invalid UTF-8 и запрещенные mojibake-маркеры не обнаружены.

## История remediation

Первичный запуск до исправлений проверил `238` файлов: invalid UTF-8 `0`, mojibake-файлов `9`.

| Файл | Классификация | Действие |
| --- | --- | --- |
| `docs/00_project/artifact_policy.md` | `mojibake_detected` | Очевидные союзы и поврежденная конструкция восстановлены по смыслу. |
| `docs/00_project/p2_modernization_progress_report.md` | `mojibake_detected` | Заголовки `Был ли push` восстановлены по смыслу. |
| `docs/00_project/scripts_inventory_before_cleanup.md` | `mojibake_detected` | Поврежденное слово `Новый` восстановлено. |
| `docs/00_project/self_review.md` | `mojibake_detected` | Заголовки и союзы восстановлены по смыслу. |
| `docs/03_pipeline/module_decomposition_plan.md` | `mojibake_detected` | Предлоги и союзы восстановлены по смыслу. |
| `README.md` | `mojibake_detected` | Поврежденные заголовки и союзы восстановлены. |
| `prompts/ofz_p3_modernization_step_by_step.md` | `allowed_marker_context` | Намеренные примеры заменены Unicode-кодами без изменения назначения инструкции. |
| `scripts/maintenance/audit_docs_encoding.py` | `allowed_marker_context` | Compatibility-маркеры переведены в escape-представление; поведение сохранено. |
| `scripts/source_acquisition/minfin_patterns.py` | `allowed_marker_context` | Compatibility regex переведен в Unicode escape-представление; поведение сохранено. |

Автоматический `--fix-safe` не применялся. Все изменения просмотрены как однозначные; `manual_review_required` отсутствует.

## Manual review

Неоднозначные случаи автоматически не исправляются. При чистом результате открытых пунктов нет.

## Политика

- Все source/docs/config/scripts хранятся в UTF-8.
- Generated artifacts, caches, virtual environments и raw Excel не проверяются.
- Mojibake допускается только в allowlisted тестовых контекстах.
- Invalid UTF-8 или mojibake блокирует quality gate и release.

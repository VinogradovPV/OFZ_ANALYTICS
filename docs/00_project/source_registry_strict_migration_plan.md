# План миграции source registry в strict mode

Дата: 2026-06-25.

## NEXT.8 update - CLI plumbing completed

Дата актуализации: 2026-07-01.

NEXT.8 completed the low-risk plumbing step without changing production defaults:

- `ofz-run` / `scripts/run_pipeline.py` now accepts `--source-registry-mode off|warn|strict`, `--allow-legacy-raw` and `--no-allow-legacy-raw`.
- Stage 1 (`scripts/01_data_audit.py`) receives those flags on every pipeline run.
- GUI pipeline command construction now appends the selected registry mode and legacy fallback checkbox state to the `ofz-run.exe` command.
- Default remains `source-registry-mode=warn` and `allow-legacy-raw=true`.
- Strict-by-default is still not approved and still requires a separate operator decision.

The NEXT.7 blocker notes below are kept as historical context for the migration plan.

## NEXT.9 update - strict full pipeline precheck completed

Дата актуализации: 2026-07-01.

Full pipeline strict/no-legacy precheck passed through the canonical entry point:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode strict --no-allow-legacy-raw
```

Additional local gates passed: editable install, `pip check`, `compileall`, UTF-8/mojibake scan, `ofz-schema`, `ofz-quality --fast` and `ofz-quality --full`.

Fresh data audit recorded `source_registry_status=ok`, `registry_warnings_count=0`, `registry_errors_count=0` and `legacy_raw_fallback_used=False`.

Strict-ready for full pipeline precheck: yes. Default remains `warn + allow-legacy-raw` until a separate approval request is prepared and approved.

## 1. Current mode

Текущий production-friendly режим остается совместимым:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

Data audit умеет проверять controlled Minfin registry, но legacy raw ingestion продолжает работать как fallback. Default не менялся в рамках NEXT.7.

Фактическая проверка 2026-06-25:

- `scripts/qa/minfin_data_audit_registry_smoke.py` - OK.
- `scripts/qa/minfin_source_acquisition_tests.py` - OK.
- `scripts/01_data_audit.py --source-registry-mode strict --no-allow-legacy-raw` - OK.
- `ofz-run.exe --help` - pipeline runner пока не принимает `--source-registry-mode` и `--no-allow-legacy-raw`.

## 2. Target mode

Целевой режим после отдельного approval:

```text
source-registry-mode=strict
allow-legacy-raw=false
```

Strict mode должен означать, что registry обязателен, active rows ссылаются на существующие файлы, SHA-256 и размер active files совпадают с registry, duplicate active rows блокируют audit, manual raw drop не считается штатным источником, monthly update идет через `ofz-fetch-minfin`, а manual fallback - через `--mode manual-import`.

## 3. Registry readiness

Текущий registry готов к strict validation на уровне data audit:

| Проверка | Статус |
|---|---|
| Registry CSV/JSON читается | OK |
| Active rows есть | OK |
| Duplicate active rows не обнаружены | OK |
| Active `2025 final` файл существует | OK |
| Active `2026 latest` файл существует | OK |
| Hash/size active files совпадают | OK |
| `strict --no-allow-legacy-raw` в `01_data_audit.py` | OK |

Текущие active rows:

- `2025 final`: `INTERNET_Auction_Results_rus_2025_20251231.xlsx`;
- `2026 latest`: `INTERNET_Auction_Results_rus_2026_20260618.xlsx`.

Отдельное наблюдение:

- В `data/raw/minfin/ofz_auction_results/versions/2026/` физически есть snapshots.
- Один старый snapshot `INTERNET_Auction_Results_rus_2026_20260611_6c25411847ae.xlsx` уже tracked в Git исторически.
- Новый snapshot `INTERNET_Auction_Results_rus_2026_20260618_3e748e88be0e.xlsx` скрыт через `.git/info/exclude` и не должен коммититься.
- Это не блокирует data audit strict validation, но требует отдельного operator decision перед полной policy cleanup, потому что текущая политика говорит не коммитить `versions/`.

## 4. Legacy fallback dependencies

Остающиеся зависимости от legacy mode:

1. `ofz-run.exe` не пробрасывает `--source-registry-mode` и `--no-allow-legacy-raw` в stage 1.
2. Default pipeline продолжает запускать data audit без strict flags.
3. Operator procedures описывают strict как validation mode, но не как default production gate.
4. GUI/launcher может показывать source registry mode, но фактический pipeline CLI пока не принимает этот параметр.

## 5. Required code changes

Перед включением strict-by-default нужны отдельные low-risk code changes:

1. Добавить в `ofz-run` / `scripts/run_pipeline.py` параметры `--source-registry-mode off|warn|strict`, `--allow-legacy-raw`, `--no-allow-legacy-raw`.
2. Пробрасывать эти параметры в stage 1 `scripts/01_data_audit.py`.
3. Обновить GUI action builder для pipeline, чтобы выбранный source registry mode действительно попадал в pipeline command.
4. Добавить smoke/regression test на command construction.
5. Улучшить сообщение ошибки full pipeline, если strict registry validation падает.

## 6. Required docs changes

Перед переключением default обновить:

- `docs/07_operations/minfin_source_acquisition.md`;
- `docs/07_operations/minfin_monthly_update_procedure.md`;
- `docs/07_operations/production_runbook.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/07_operations/gui_launcher.md`;
- README, если там описан production workflow.

Документы должны явно различать strict readiness, strict dry-run/precheck, strict-by-default и emergency rollback to `warn + allow-legacy-raw`.

## 7. Required operator procedure changes

Операторский workflow после migration:

1. Перед monthly pipeline выполнить `ofz-fetch-minfin --mode monthly --dry-run`.
2. При необходимости выполнить controlled download с `DOWNLOAD_MINFIN_SOURCE`.
3. Проверить registry active rows и source acquisition report.
4. Запустить pipeline в strict/no-legacy режиме.
5. При strict failure не подменять raw вручную, а исправить registry/source acquisition state или выполнить manual-import.

Запрещено вручную класть XLSX в legacy `data/raw` как единственный источник, переключать default на strict без отдельного approval и коммитить `versions/` snapshots без отдельного operator decision.

## 8. Migration phases

### Phase 1 - readiness documentation

Статус: выполнено в NEXT.7.

- Создан этот план.
- Подтверждено, что data audit strict validation проходит.
- Подтверждено, что `ofz-run` пока не поддерживает strict flags.
- Default не изменен.

### Phase 2 - CLI plumbing

Статус: выполнено в NEXT.8.

Добавлены strict flags в `ofz-run`, flags пробрасываются в stage 1, GUI command builder передает выбранный source registry mode и legacy fallback, добавлен smoke `scripts/qa/pipeline_registry_cli_smoke.py`. Default после Phase 2 все еще `warn + allow-legacy-raw`.

### Phase 3 - strict precheck gate

Статус: выполнено в NEXT.9.

Полный pipeline в strict/no-legacy режиме, `ofz-quality --fast` и `ofz-quality --full` прошли. Операторский default switch не выполнялся.

### Phase 4 - default switch

Только после отдельного approval: поменять default на strict/no-legacy, обновить release checklist, выполнить full quality gate, проверить GUI и monthly procedure.

## 9. Rollback plan

Если strict mode ломает production workflow:

1. Вернуть запуск к `source-registry-mode=warn`.
2. Временно разрешить `allow-legacy-raw=true`.
3. Не менять raw вручную без registry repair plan.
4. Зафиксировать failure category: missing registry row, missing file, hash mismatch, duplicate active row, unsupported CLI option или docs/operator mismatch.
5. После repair повторить strict precheck.

## 10. Approval checklist

Перед strict-by-default нужно явное approval пользователя:

- [x] `ofz-run` поддерживает strict/no-legacy flags.
- [x] GUI pipeline action пробрасывает registry mode.
- [x] Full pipeline strict/no-legacy прошел.
- [x] `ofz-quality --fast` прошел.
- [x] `ofz-quality --full` прошел.
- [ ] Operator docs обновлены.
- [ ] Исторический tracked `versions/2026` snapshot классифицирован отдельным решением.
- [ ] Release checklist обновлен.
- [ ] Rollback команда documented.
- [ ] Пользователь явно подтвердил switch default to strict.

## 11. Итог NEXT.7

```text
strict-ready=true for data-audit validation
strict-ready=false for full pipeline default switch
default-change-approved=false
```

Причина неполной готовности: `ofz-run` пока не принимает `--source-registry-mode` и `--no-allow-legacy-raw`, поэтому full pipeline strict/no-legacy нельзя проверить через canonical pipeline entry point без отдельной доработки.

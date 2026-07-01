# Запрос на approval для strict default source registry

Дата: 2026-07-01.

## 1. Что изменится

Если пользователь отдельно одобрит следующий шаг, default-политика source registry изменится с:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

на:

```text
source-registry-mode=strict
allow-legacy-raw=false
```

Ожидаемый эффект: canonical pipeline будет останавливаться на stage 1, если controlled registry Минфина отсутствует, неконсистентен, ссылается на отсутствующие active files, содержит mismatch по hash/size или duplicate active rows.

Сам switch потребует отдельного implementation commit только после явного approval:

- изменить defaults в `scripts/run_pipeline.py`;
- изменить GUI defaults в `scripts/gui_launcher/state.py`;
- обновить operator docs, release checklist и monthly procedure;
- повторить full local gate.

## 2. Что не изменится

Этот документ не меняет defaults.

Текущее поведение остается прежним:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

Controlled registry остается validation gate. NEXT.10 не меняет финансовую методологию, chart semantics, processed schema, output paths, raw files, release artifacts или BI package behavior.

Ручные обновления источников по-прежнему должны идти через workflows `ofz-fetch-minfin`, а не через blind copy XLSX в legacy raw folders.

## 3. Какие проверки прошли

NEXT.8 добавил CLI plumbing и GUI command construction:

- `ofz-run` принимает `--source-registry-mode off|warn|strict`;
- `ofz-run` принимает `--allow-legacy-raw` и `--no-allow-legacy-raw`;
- stage 1 `scripts/01_data_audit.py` получает registry flags;
- GUI pipeline command передает выбранный registry mode и состояние legacy checkbox.

NEXT.9 выполнил strict full pipeline precheck:

| Проверка | Результат |
|---|---|
| `pip install -e .` | OK |
| `pip check` | OK |
| `compileall -q scripts` | OK |
| UTF-8/mojibake scan | OK |
| Full `ofz-run` с `--source-registry-mode strict --no-allow-legacy-raw` | OK |
| `ofz-schema` | OK, 16 checks passed |
| `ofz-quality --fast` | OK |
| `ofz-quality --full` | OK |

Свежий data audit из NEXT.9 зафиксировал:

```text
source_registry_mode=strict
source_registry_status=ok
registry_warnings_count=0
registry_errors_count=0
legacy_raw_fallback_used=False
```

## 4. Какие риски

- Broken registry, missing active row, missing active file, duplicate active row, hash mismatch или size mismatch будут останавливать pipeline на stage 1.
- Операторам, которые полагаются на legacy raw fallback, сначала потребуется исправить source acquisition state.
- Ручное копирование raw XLSX станет явнее несовместимым с production workflow.
- Перед strict-by-default желательно провести GUI manual rehearsal в strict/no-legacy режиме.
- Один historical tracked snapshot в `data/raw/minfin/ofz_auction_results/versions/2026/` все еще требует отдельного raw versions policy decision.
- `ofz-quality --full` сейчас проходит с существующими analytical warnings и visual regression fallback в managed Codex environment; это не blocker для strict precheck, но должно оставаться видимым.

## 5. Rollback

Если strict default будет approved и позже создаст операционные проблемы, rollback прямой:

1. Вернуть default `source-registry-mode=warn`.
2. Вернуть default `allow-legacy-raw=true`.
3. Оставить explicit strict/no-legacy CLI flags доступными для precheck runs.
4. Зафиксировать категорию failure:
   - unsupported CLI option;
   - missing registry row;
   - missing active file;
   - hash mismatch;
   - duplicate active row;
   - unexpected legacy fallback;
   - data audit failure;
   - downstream schema или quality failure.
5. Исправить registry/source acquisition state перед повторным strict run.

Rollback нельзя делать через ручное подкладывание XLSX в raw folders как единственный source update path.

## 6. Операторская процедура

Рекомендуемый operator procedure после approval strict default:

1. Запустить Minfin dry-run для нужного года и режима.
2. При необходимости выполнить controlled download или manual import с нужным confirm token.
3. Проверить registry active rows и source acquisition reports.
4. Запустить pipeline с default strict/no-legacy behavior.
5. Запустить `ofz-quality --fast`; перед release или major handoff запускать `ofz-quality --full`.
6. Если strict validation падает, исправить registry/source acquisition state или использовать documented manual-import workflow.

Пока approval не получен, операторы должны продолжать использовать текущий default и включать strict явно:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode strict --no-allow-legacy-raw
```

## 7. Решение пользователя

Выберите один вариант:

```text
[ ] approve strict default switch
[ ] defer strict default switch
[ ] reject strict default switch
```

Текущая рекомендация: defer до завершения GUI manual rehearsal в strict/no-legacy режиме и отдельного raw versions policy decision.

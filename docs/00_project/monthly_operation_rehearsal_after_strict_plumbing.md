# NEXT.12 - Ежемесячная операционная репетиция после strict plumbing

Дата выполнения команд: 2026-07-01  
Дата оформления отчета: 2026-07-02

## Цель

Проверить, что ежемесячный операторский workflow понятен и безопасен после добавления strict registry plumbing в canonical pipeline entry point `ofz-run`.

Репетиция выполнялась без raw mutation:

- live download не запускался;
- import/replacement raw-файлов не выполнялся;
- source registry default не менялся;
- strict-by-default не включался.

Default policy остается прежней:

```text
source-registry-mode=warn
allow-legacy-raw=true
```

## Preflight

Перед началом выполнены проверки из корня проекта:

```powershell
git status --short --branch
git log --oneline -5
git ls-files -v | Select-String '^S '
Get-Content .git\info\exclude
```

Наблюдения:

- ветка: `main`;
- последние commits включали `dc782f3`, `d03a119`, `ce05753`, `83da318`, `e354471`;
- tracked-изменений перед репетицией не было;
- в working tree оставались только локальные untracked prompt-файлы;
- skip-worktree entries относятся к старым generated/report документам и не менялись;
- `.git/info/exclude` содержит прежние локальные исключения для prompt/raw-version leftovers.

## Minfin dry-run

Выполнена команда:

```powershell
.\.venv\Scripts\ofz-fetch-minfin.exe --year 2026 --mode monthly --dry-run --timeout-seconds 20 --retries 1
```

Результат: OK.

Команда завершилась штатно и не запросила download. Raw storage и registry не мутировали.

Наблюдение: live discovery вернул предупреждение о недоступности сайта Минфина:

```text
Live discovery failed; raw unchanged
```

Это не является blocker для dry-run rehearsal, потому что сценарий подтвердил безопасное поведение при сетевой недоступности.

## Pipeline в совместимом режиме

Выполнена команда:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-06-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode warn --allow-legacy-raw
```

Результат: OK.

В логе pipeline подтверждено, что stage 1 получил registry flags:

```text
scripts\01_data_audit.py --source-registry-mode warn --allow-legacy-raw
```

Это соответствует текущей default-compatible политике.

## Quality-fast

Выполнена команда:

```powershell
.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-06-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Результат: OK.

Ключевые блоки quality-fast прошли:

- encoding/mojibake check;
- py_compile key scripts;
- schema validation;
- regression tests;
- smoke tests;
- HTML chart QA;
- visual regression в fallback mode;
- README/docs/outputs/charts/scripts structure checks;
- run manifest check;
- dashboard semantic model check.

Ограничение: visual regression использовал fallback mode, потому что screenshot backend недоступен в managed sandbox.

## Strict/no-legacy контроль

После успешного NEXT.9 выполнен контрольный strict/no-legacy прогон:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-06-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --source-registry-mode strict --no-allow-legacy-raw
```

Результат: OK.

В логе pipeline подтверждено, что stage 1 получил strict flags:

```text
scripts\01_data_audit.py --source-registry-mode strict --no-allow-legacy-raw
```

Это подтверждает, что strict plumbing работает не только на майском precheck scope, но и на июньском monthly rehearsal scope.

## GUI rehearsal

Интерактивное окно `ofz-gui.exe` не открывалось как автоматизированная проверка, чтобы не оставлять зависший GUI process. Вместо этого выполнены smoke/preview проверки GUI:

```powershell
.\.venv\Scripts\ofz-gui.exe --help
.\.venv\Scripts\python.exe scripts\qa\gui_launcher_smoke.py
.\.venv\Scripts\python.exe scripts\qa\gui_command_runner_smoke.py
.\.venv\Scripts\ofz-gui.exe --smoke
.\.venv\Scripts\ofz-gui.exe --smoke-ui
```

Результат: OK.

Проверено:

- GUI entry point доступен;
- state/actions создаются без открытия окна;
- command runner smoke проходит;
- widgets создаются и закрываются в smoke-ui;
- GUI actions count: 29;
- GUI tabs count: 9.

Ручная интерактивная проверка остается операторским действием:

1. вкладка `Обзор`: проверить registry mode labels;
2. вкладка `Минфин`: проверить dry-run сайта Минфина;
3. вкладка `Pipeline`: запустить pipeline в warn mode;
4. вкладка `Pipeline`: проверить preview для strict/no-legacy;
5. вкладка `Проверки качества`: запустить quality-fast;
6. вкладка `Журнал`: убедиться, что сообщения понятны оператору.

## Итог

NEXT.12 rehearsal успешен.

Подтверждено:

- monthly dry-run source acquisition не мутирует raw;
- pipeline warn/allow режим работает для `2026-06-01`;
- quality-fast проходит для `2026-06-01`;
- strict/no-legacy pipeline проходит для `2026-06-01`;
- GUI command/state/widget smoke проходит;
- default source registry policy не менялась;
- generated outputs не предназначены для staging.

## Что не выполнялось

Не выполнялись:

- real Minfin download;
- manual import;
- annual-final replacement;
- release bundle build;
- BI package build;
- default switch to strict/no-legacy;
- GitHub Actions checks.

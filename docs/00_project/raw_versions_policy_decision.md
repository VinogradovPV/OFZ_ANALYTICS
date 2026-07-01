# Решение по policy для Minfin raw versions

Дата: 2026-07-01.

## 1. Scope

NEXT.11 фиксирует решение по историческому snapshot в:

```text
data/raw/minfin/ofz_auction_results/versions/2026/
```

Текущая проектная policy говорит, что `versions/` snapshots не коммитятся по умолчанию. При этом один старый snapshot уже tracked в Git исторически, а новый локальный snapshot скрыт через `.git/info/exclude`.

Этот документ сначала был подготовлен как decision report. После отдельного approval пользователя в этом же NEXT.11 применен вариант B: tracked snapshot снят из Git index через `git rm --cached`, физический файл оставлен локально.

## 2. Фактическое состояние

Tracked в Git:

```text
data/raw/minfin/ofz_auction_results/versions/2026/INTERNET_Auction_Results_rus_2026_20260611_6c25411847ae.xlsx
```

Физически присутствуют файлы:

| Файл | Размер | Git status |
|---|---:|---|
| `INTERNET_Auction_Results_rus_2026_20260611_6c25411847ae.xlsx` | 20053 bytes | снят из Git index через `git rm --cached`, локальный файл сохранен |
| `INTERNET_Auction_Results_rus_2026_20260618_3e748e88be0e.xlsx` | 20131 bytes | local ignored via `.git/info/exclude` |

После применения варианта B `git ls-files data/raw/minfin/ofz_auction_results/versions` не показывает tracked files.

`.gitignore` теперь содержит правило:

```text
data/raw/minfin/ofz_auction_results/versions/
```

`git check-ignore -v` подтверждает, что оба локальных snapshots в `versions/2026/` игнорируются этим правилом.

## 3. Почему это важно

`versions/` snapshots являются побочным результатом controlled source acquisition и могут расти со временем. Если такие файлы коммитить без отдельного решения, repository начнет хранить mutable raw history вместо source policy/report metadata.

Текущий historical tracked snapshot не блокирует:

- strict registry validation;
- strict/no-legacy full pipeline precheck;
- quality-fast/full;
- текущий default `warn + allow-legacy-raw`.

Но он создает policy inconsistency: документация говорит не коммитить `versions/`, а история репозитория уже содержит один такой файл.

## 4. Варианты решения

### A. Оставить tracked snapshot как legacy exception

Плюсы:

- не меняет Git index;
- сохраняет исторический snapshot как audit artifact;
- минимальный operational risk.

Минусы:

- policy остается неоднородной;
- будущим операторам сложнее объяснить, почему один `versions/` файл tracked, а остальные нет.

### B. Убрать tracked snapshot из Git через `git rm --cached`, оставить файл локально/ignored

Плюсы:

- приводит repository policy к текущему правилу: `versions/` не коммитится;
- файл можно оставить локально для operator review;
- future snapshots остаются external/local artifacts.

Минусы:

- требует явного approval, потому что меняет tracked raw file state;
- в Git history файл останется в старых commits, но исчезнет из текущего tree.

Команда только после approval:

```powershell
git rm --cached data/raw/minfin/ofz_auction_results/versions/2026/INTERNET_Auction_Results_rus_2026_20260611_6c25411847ae.xlsx
```

После этого нужно убедиться, что `.gitignore` или `.git/info/exclude` скрывает `versions/`.

### C. Перенести snapshot в release asset/archive вне repo

Плюсы:

- сохраняет audit artifact вне Git repository;
- подходит, если snapshot нужен как handoff artifact.

Минусы:

- требует отдельного release/archive process;
- не нужен для текущего strict registry gate.

### D. Принять policy tracking для selected versions snapshots с size limits

Плюсы:

- делает raw version history частью Git-managed audit trail.

Минусы:

- противоречит текущей lightweight repository policy;
- увеличивает риск разрастания repo;
- требует новых правил отбора, лимитов размера и review gate.

## 5. Рекомендация

Рекомендуемый вариант: B. Пользователь явно одобрил выполнение варианта B.

Причина: текущая policy уже говорит не коммитить `versions/`; вариант B выравнивает текущий tree с этой policy и оставляет snapshot локально/ignored без удаления физического файла.

Фактическое состояние после применения:

```text
decision=approved_option_B
action_taken=git_rm_cached
tracked_snapshot_removed_from_current_tree=true
physical_file_deleted=false
default_source_registry_policy=warn + allow-legacy-raw
```

## 6. Если approval не получен

Этот раздел оставлен как исторический вариант. На момент завершения NEXT.11 approval получен, поэтому применен вариант B.

Не выполнять:

- `git rm --cached`;
- удаление файлов из `data/raw/minfin/ofz_auction_results/versions/`;
- изменение default source registry policy;
- staging новых raw versions snapshots.

## 7. Если approval получен

Выполнено в рамках NEXT.11 после явного approval:

1. Выполнен `git rm --cached` для tracked snapshot.
2. `.gitignore` обновлен правилом `data/raw/minfin/ofz_auction_results/versions/`.
3. Проверено, что `versions/` snapshots игнорируются.
4. Artifact guard должен оставаться clean для generated outputs, releases, logs, processed data, raw versions и `.ofz_launcher`.

## 8. Текущее решение

На момент завершения NEXT.11 пользователь одобрил вариант B.

Решение: перестать tracking historical Minfin version snapshot в текущем tree, оставить файл локально и закрепить ignore rule для `versions/`.

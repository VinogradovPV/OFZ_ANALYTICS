# Синхронизация Этапа 3 - Feature engineering

Дата проверки: `2026-05-18`.

Проверка выполнена с учетом текущего состояния Этапа 2. `data/raw/` не изменялся. Существующие outputs не перезаписывались.

## Источник Этапа 3

`scripts/03_feature_engineering.py` использует cleaned dataset:

```text
data/processed/ofz_auctions_clean.csv
```

Это подтверждается кодом: скрипт проверяет `config.OFZ_AUCTIONS_CLEAN_CSV.exists()` и читает `pd.read_csv(config.OFZ_AUCTIONS_CLEAN_CSV)`.

## Выходные артефакты Этапа 3

| Артефакт | Статус |
|---|---|
| `scripts/03_feature_engineering.py` | существует, обновлен |
| `data/processed/ofz_auctions_features.csv` | существует, но был создан до текущей синхронизации скрипта |
| `docs/feature_engineering.md` | существует, но был создан до текущей синхронизации скрипта |

Скрипт записывает:

- `data/processed/ofz_auctions_features.csv`;
- `docs/feature_engineering.md`;
- логи в `logs/pipeline.log`.

## Проверка признаков

| Признак | Текущий generated dataset | Обновленный скрипт | Комментарий |
|---|---|---|---|
| `bid_to_cover_ratio` | есть | рассчитывает | `demand_amount_mln_rub / placement_amount_mln_rub`. |
| `placement_volume` | есть | рассчитывает | Alias для `placement_amount_mln_rub`. |
| `demand_volume` | есть | рассчитывает | Alias для `demand_amount_mln_rub`. |
| `supply_volume` | отсутствует | добавлено | Alias для `offer_amount_mln_rub`, нужен для таблицы спроса и предложения. |
| `yield` | отсутствует | добавлено | Alias для основной доходности, нужен табличному слою. |
| `weighted_avg_yield` | есть | рассчитывает | Alias для `weighted_avg_yield_pct`. |
| `maturity_years` | есть | рассчитывает | `days_to_maturity / 365.25`. |
| `maturity_bucket` | есть, но старая шкала | обновлено | Теперь шкала: до 5 лет, 5-10 лет, свыше 10 лет. |
| `maturity_bucket_label` | отсутствует | добавлено | Человекочитаемая метка категории срока. |
| `ofz_type` | есть | рассчитывает | Alias для `security_type`. |
| `auction_year` | есть | рассчитывает | Из `auction_date`. |
| `auction_quarter` | есть | рассчитывает | Из `auction_date`. |
| `auction_month` | есть | рассчитывает | Из `auction_date`. |
| `demand_pressure_indicator` | есть | рассчитывает | На основе `bid_to_cover_ratio`. |
| `yield_pressure_indicator` | есть | рассчитывает | На основе z-score доходности внутри года. |
| `auction_efficiency_score` | есть | рассчитывает | Композит из размещения, спроса и доходности. |

## Признаки для новых табличных отчетов

| Требуемое поле | Статус после обновления скрипта |
|---|---|
| `ofz_type` | реализовано |
| `yield` | добавлено |
| `weighted_avg_yield` | реализовано |
| `demand_volume` | реализовано |
| `supply_volume` | добавлено |
| `placement_volume` | реализовано |
| `maturity_years` | реализовано |
| `maturity_bucket` | обновлено |
| `maturity_bucket_label` | добавлено |

## Правило классификации сроков обращения

В `scripts/03_feature_engineering.py` применена следующая шкала:

- `short_term`: краткосрочные ОФЗ, срок обращения до 5 лет;
- `medium_term`: среднесрочные ОФЗ, срок обращения от 5 до 10 лет включительно;
- `long_term`: долгосрочные ОФЗ, срок обращения свыше 10 лет;
- `requires_review`: срок обращения невозможно надежно определить.

Метки:

- `Краткосрочные (до 5 лет)`;
- `Среднесрочные (5-10 лет)`;
- `Долгосрочные (свыше 10 лет)`;
- `Требует проверки`.

## Связь с текущим состоянием Этапа 2

Этап 3 зависит от `data/processed/ofz_auctions_clean.csv`. Текущий clean dataset существует, но Этап 2 был обновлен на уровне кода для нового `format_assumption_flag`; generated clean CSV нужно регенерировать вручную.

Рекомендуемый порядок:

1. Сначала вручную запустить обновленный Этап 2.
2. Затем вручную запустить обновленный Этап 3.
3. После этого повторно проверить заголовок `ofz_auctions_features.csv`: в нем должны появиться `supply_volume`, `yield`, `maturity_bucket_label`.

## Ограничение sandbox / manual check

Codex sandbox не смог выполнить проектный Python:

```text
did not find executable at 'C:\Users\Rockaudit\AppData\Local\Programs\Python\Python314\python.exe'
```

Это не считается поломкой `.venv`. Требуется ручная проверка через проектный Python.

## Команды ручной проверки

Проверка компиляции:

```powershell
& "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe" -m py_compile "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\scripts\03_feature_engineering.py"
```

Ожидаемый результат: команда завершится без вывода.

Регенерация Этапа 3:

```powershell
& "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\.venv\Scripts\python.exe" "C:\Users\Rockaudit\LLM_CHAT\ofz_analytics\scripts\03_feature_engineering.py"
```

Ожидаемый результат:

- будет обновлен `data/processed/ofz_auctions_features.csv`;
- будет обновлен `docs/feature_engineering.md`;
- в `logs/pipeline.log` появятся записи запуска Этапа 3;
- в features dataset появятся `supply_volume`, `yield`, `maturity_bucket_label`;
- `maturity_bucket` будет использовать категории `short_term`, `medium_term`, `long_term`, `requires_review`.

## Итог

Этап 3 был подтвержден предыдущими артефактами, но не был полностью синхронизирован с новыми требованиями табличных отчетов. Скрипт обновлен. Полное подтверждение Этапа 3 требует ручного запуска после актуализации Этапа 2.

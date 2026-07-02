# План декомпозиции Chart/QA

Дата: 2026-06-25.

## Контекст

Этап `NEXT.6 - Chart/QA decomposition foundation` выполняет первый низкорисковый шаг после релиза `v0.1.0`: фиксирует план декомпозиции крупных chart/QA модулей и выносит только инфраструктурные helper-функции без изменения финансовой методологии, путей output, имен файлов, визуальной семантики графиков и политики source acquisition.

## Текущее состояние крупных модулей

По размеру верхнеуровневых файлов `scripts/` самые крупные кандидаты:

| Файл | Размер, байт | Наблюдение |
|---|---:|---|
| `scripts/06_build_charts.py` | 345706 | Основной монолит годовых/структурных графиков: builders, label policy, export, markdown summaries. |
| `scripts/html_chart_qa.py` | 114712 | Проверки HTML-графиков, contracts, manifest/summary reporting. |
| `scripts/10_build_monthly_charts.py` | 87426 | Помесячные графики, heatmap, yield/volume labels и export. |
| `scripts/visual_regression.py` | 77399 | Авто/screenshot visual regression, manifests, browser/fallback logic. |
| `scripts/07_dashboard_exports.py` | 72673 | Dashboard/export package generation. |
| `scripts/12_build_revenue_charts.py` | 32785 | Revenue chart builders и export loop. |

В `scripts/charts/` уже есть частичная модульная структура: `common.py`, `structure.py`, `scatter.py`, `monthly.py`, `revenue.py`, `boxplot.py`. Поэтому первый extraction не дублирует существующие formatter helpers.

## Найденные зоны дублирования

- Создание output-директорий перед записью HTML/CSV.
- Запись пары `figure.write_html(...)` + `dataframe.to_csv(...)`.
- Сборка common suffix для chart/export names.
- Metadata/label policy вокруг chart titles, tooltips и OFZ-PD yield scope.
- QA contract helpers для HTML chart QA и visual regression.

## Что можно выносить без изменения поведения

- Инфраструктурные операции записи chart artifacts.
- Общие helper-функции для гарантированного создания output-директорий.
- В дальнейшем: metadata/label policy helpers, если они будут покрыты snapshot/contract checks.
- В дальнейшем: QA contract helpers, если сигнатуры reports и exit codes останутся прежними.

Нельзя в рамках foundation-step:

- менять формулы доходности, включая scope `ОФЗ-ПД only`;
- менять `yield_weighted_avg`, `yield_min`, `yield_median`, `yield_max`, `cumulative_weighted_avg_yield`;
- менять имена HTML/CSV/XLSX/JSON artifacts;
- менять директории outputs, archive/tmp/cache или release policy;
- менять title/tooltip semantics без отдельного visual/contract шага.

## Контракты защиты

- `py_compile` для основных chart/QA файлов.
- `compileall` по `scripts`.
- Полный `ofz-run` на `2026-05-01 / month / cumulative / retrospective 4`.
- `html_chart_qa.py` на том же scope.
- `visual_regression.py --mode auto` на том же scope.
- Regression test `scripts/qa/ofz_pd_yield_metrics_regression.py`.
- Artifact guard перед commit, чтобы generated outputs не попали в staging.

## Первый extraction

Выбран минимальный helper-module:

- `scripts/charts/export_utils.py`

Вынесены только:

- `ensure_directories(*directories)`;
- `write_chart_artifacts(figure, dataframe, html_path, csv_path, csv_encoding=...)`.

Подключение выполнено в:

- `scripts/06_build_charts.py`;
- `scripts/10_build_monthly_charts.py`.

Поведение сохранено:

- `06_build_charts.py` продолжает писать CSV в `utf-8`;
- `10_build_monthly_charts.py` продолжает писать CSV в `utf-8-sig`;
- paths, suffix, filenames, chart builders, labels и financial methodology не менялись.

## Следующие шаги

1. Выделить `chart_metadata.py` или `label_policy.py` только после contract snapshot по title/tooltip/yield_scope.
2. Выделить `qa/chart_contract_helpers.py` для HTML QA после фиксации текущих report fields.
3. Разделять `visual_regression.py` по backend/manifest/reporting только после отдельного smoke для fallback и screenshot режимов.
4. Не начинать методологические изменения в рамках decompositions; финансовые изменения должны идти отдельными stages.

## NEXT.14 - второй extraction

Дата: 2026-07-02.

В `NEXT.14 - Chart/QA decomposition iteration 2` выполнен следующий малый behavior-neutral шаг:

- создан `scripts/charts/chart_metadata.py`;
- вынесены `make_report_suffix(params)` и `chart_data_dir_for_name(name)`;
- `scripts/06_build_charts.py` сохранил совместимые wrapper-функции `make_suffix(...)` и `chart_data_dir_for_name(...)`;
- добавлен `scripts/qa/chart_metadata_smoke.py`.

Поведение сохранено:

- suffix для HTML/CSV имен остается `period_type_aggregation_mode_report-date_retrospective_N`;
- routing chart data CSV остается прежним: risk/scatter/sankey/boxplot/structure;
- output directories, filenames, chart builders, labels и financial methodology не менялись;
- yield/boxplot methodology не затрагивалась.

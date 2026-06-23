"""Русская встроенная справка OFZ GUI."""

HELP_TEXT = """OFZ_ANALYTICS

Приложение анализирует результаты размещений ОФЗ, формирует очищенные данные, аналитические таблицы, интерактивные графики, dashboard exports и release packages.

Основной workflow

Минфин -> source registry -> pipeline -> QA -> reports -> release.

Report date

Отчетная дата задается в формате YYYY-MM-01 и определяет целевой месяц, квартал или год. Дата всегда должна быть первым днем месяца.

Retrospective years

Количество предыдущих лет, которые включаются в сравнительный scope.

Period type и aggregation mode

Period type: month, quarter или year. Cumulative включает период с начала года до report date. Point показывает только выбранный период.

Source acquisition Минфина

Вкладка Минфина построена вокруг обычного пользовательского сценария. Основные кнопки: проверить сайт Минфина, обновить данные текущего года, проверить или закрыть предыдущий год, проверить registry и открыть папки registry/reports. URL override, HTML fixture, no network и max pages нужны только для диагностики парсера и скрыты в расширенном блоке. Manual XLSX используется как аварийный fallback, если сайт Минфина недоступен или изменилась верстка.

Monthly download, annual-final download, annual-final replacement и manual import меняют controlled raw storage только после exact typed confirm. При HTTP 503 повторите dry-run позже: сайт Минфина временно недоступен, raw не изменен.

Dry-run

Dry-run строит план и проверяет входы, но не выполняет production mutation.

Typed confirm

Опасные операции доступны только после точного ввода показанного token. Token относится к конкретному action и не заменяет проверку command preview.

Pipeline stage 0

Stage 0 может выполнить Minfin monthly dry-run или подтвержденный download перед pipeline. Если stage 0 или optional schema завершится с non-zero code, pipeline не запускается.

Проверки качества

Quality fast подходит для обычного рабочего цикла. Quality full является длительной pre-release проверкой. UTF-8/Mojibake gate входит в fast/full и доступен отдельно.

Результаты

HTML-графики: outputs/charts/
Экспорты: outputs/exports/
Отчеты: outputs/reports/
Launcher logs: outputs/reports/launcher/

Generated outputs не коммитятся. Не добавляйте в Git outputs/, releases/, logs/, data/processed/ и data/raw/minfin/ofz_auction_results/versions/.

Release bundle

Сначала выполните dry-run. Build требует BUILD_RELEASE_BUNDLE. BI build требует BUILD_BI_PACKAGE. GitHub release не создается этим GUI.

GUI и CLI

GUI безопасно выполняет утвержденные CLI actions и показывает output. CLI остается интерфейсом для automation и продвинутых сценариев. Поля произвольной shell-команды в GUI нет.

При ошибке

Откройте вкладку Журнал, проверьте exit code и log path. Ошибка не скрывается; следующий шаг последовательности не запускается после non-zero code.
"""

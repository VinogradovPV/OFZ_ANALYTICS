# План Docker

Дата: 2026-06-16.

Docker для OFZ_ANALYTICS является optional-направлением. Production baseline проекта остается Windows-first: локальная `.venv`, PowerShell, CLI entry points и generated outputs вне Git.

## Статус

- Dockerfile в P2.12 не создается.
- `.dockerignore` в P2.12 не создается.
- Решение о Docker runtime переносится в отдельный controlled step.

Причина: проект уже имеет рабочий Windows setup workflow, а Docker требует отдельной проверки русских шрифтов, locale, browser dependencies для screenshot regression и стратегии mount для raw/generated artifacts.

## Целевой Docker-сценарий

Будущий Docker образ должен:

- устанавливать Python из поддержанного диапазона `>=3.11,<3.15`;
- устанавливать runtime dependencies из `requirements.txt`;
- опционально устанавливать dev/QA dependencies из `requirements-dev.txt`;
- выполнять `pip install -e .`;
- поддерживать CLI:
  - `ofz-run`;
  - `ofz-quality`;
  - `ofz-schema`;
  - `ofz-clean-outputs`;
  - `ofz-build-release-bundle`;
- не содержать generated outputs внутри image layer;
- писать generated artifacts только в mounted volume.

## Locale и русские шрифты

Контейнер должен поддерживать:

- UTF-8 locale;
- корректное чтение/запись русских Markdown/CSV/HTML;
- русские шрифты для screenshot visual regression;
- стабильное отображение Plotly HTML.

Для Linux-based image потребуется пакет шрифтов с кириллицей, например семейство DejaVu/Noto. Конкретный набор должен быть проверен screenshot backend.

## Browser-зависимости

Для screenshot visual regression в Docker потребуется:

- Playwright browser dependencies;
- Chromium;
- headless execution;
- стабильный viewport `1920x1080`;
- отключение toolbar/cursor effects на уровне `visual_regression.py`.

Если browser dependencies не установлены, `visual_regression.py --mode auto` должен переходить в fallback static HTML / Plotly JSON inspection.

## Стратегия mount для raw data

`data/raw` является source dataset проекта и tracked in Git. Для Docker есть два допустимых варианта:

1. Включать `data/raw` в checkout внутри container workspace.
2. Монтировать `data/raw` read-only:

```text
./data/raw:/app/data/raw:ro
```

Pipeline и cleanup scripts не должны менять `data/raw`.

## Стратегия mount для generated outputs

Generated outputs не коммитятся в Git. В Docker они должны писаться в mounted volume:

```text
./outputs:/app/outputs
```

Очистка outputs допускается только через:

```powershell
ofz-clean-outputs --dry-run
ofz-clean-outputs --archive-all --delete-all --confirm DELETE_OUTPUTS
```

## Путь релизного пакета

Release bundle должен писаться во внешний mounted path:

```text
./releases:/app/releases
```

`releases/` остается external artifact storage и не коммитится.

## Кандидатные Docker-команды

После отдельного решения Dockerfile может поддержать:

```powershell
docker build -t ofz-analytics:local .
docker run --rm `
  -v ${PWD}/data/raw:/app/data/raw:ro `
  -v ${PWD}/outputs:/app/outputs `
  -v ${PWD}/releases:/app/releases `
  ofz-analytics:local `
  ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Риски

- Windows Excel/source filename behavior may differ from Linux container behavior.
- Browser screenshots may differ by fonts and rendering backend.
- File permissions on mounted outputs need explicit validation.
- Large generated HTML artifacts should remain outside image layers.

## Рекомендация

Keep Windows setup as the primary supported path for production-ready v1/P2. Docker should be implemented later as a separate P2/P3 step after:

- screenshot backend is stable on local Windows;
- release bundle automation is stable;
- CI behavior is stable;
- Russian font rendering is specified and verified.

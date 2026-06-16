# Visual Regression Backend Decision

Date: 2026-06-11.

## Decision

The project uses a two-layer visual regression strategy:

1. `fallback` mode: static HTML / Plotly JSON inspection.
2. `screenshot` mode: Playwright-based browser screenshots for generated local HTML charts.
3. `auto` mode: tries Playwright screenshot backend first and falls back to static inspection if the backend is unavailable.

Recommended production mode after backend stabilization:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

## Alternatives Reviewed

| Backend | Assessment | Decision |
|---|---|---|
| Playwright | Opens local HTML in a real browser, supports stable viewport, waits for Plotly, can hide modebar and save full-page PNG. | Selected primary screenshot backend. |
| Kaleido | Good for direct Plotly figure export, but current artifacts are standalone HTML files and not all page-level layout issues are represented by a single figure object. | Not selected as primary backend. Remains runtime dependency for Plotly export tasks. |
| Selenium/browser-based | Similar browser coverage, but heavier driver management and less convenient local automation than Playwright. | Not selected. |
| Existing Plotly JSON fallback | Fast, stable and useful for contracts, axis labels, legends and trace metadata, but cannot prove actual rendered layout. | Kept as reserve and contract-inspection layer. |

## Screenshot Backend Contract

`scripts/visual_regression.py` supports:

- `--mode fallback`
- `--mode screenshot`
- `--mode auto`

`auto` behavior:

1. Try Playwright screenshot backend.
2. If Playwright package or browser binaries are unavailable, record warning and use fallback inspection.
3. Always write `visual_regression_mode` to the report.

Screenshot backend behavior:

- opens local HTML via `file:///`;
- uses viewport `1920x1080`;
- waits for Plotly graph containers and SVG rendering;
- hides Plotly toolbar/modebar;
- disables cursor effects through injected CSS;
- saves screenshots under `outputs/reports/visual_regression/screenshots/<run_id>/`;
- writes screenshot manifest JSON and diff report under `outputs/reports/visual_regression/`;
- treats screenshots, manifests and diff reports as generated outputs.

## Baseline And Diff Policy

If a matching baseline screenshot exists in:

```text
outputs/reports/visual_regression/baseline/
```

the backend compares SHA256 checksums and records:

- `match`;
- `changed`.

If no baseline exists, the status is:

- `missing_baseline`.

Missing baseline is not a failure during P2.7 stabilization. It is a documented warning/initialization state.

## Generated Artifacts

Do not commit:

- `outputs/reports/visual_regression/screenshots/**`;
- `outputs/reports/visual_regression/screenshot_manifest_*.json`;
- `outputs/reports/visual_regression/diffs/**`;
- `outputs/reports/visual_regression/*.png`.

Release bundles may include visual regression reports and screenshots as external artifacts.

## Dependency Policy

Playwright is a dev/QA dependency, not a runtime pipeline dependency.

Install dev dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

If Playwright is not installed, `--mode auto` falls back to static HTML inspection.

## Codex Sandbox And Manual PowerShell Runs

The screenshot backend launches a browser subprocess. In the Codex managed sandbox this subprocess can be blocked by Windows pipe permissions even when Playwright and Chromium are installed correctly. In that case `--mode auto` records a warning and uses fallback inspection.

For production or local QA, run screenshot mode from the project PowerShell session:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Manual smoke validation can be done with:

```powershell
.\.venv\Scripts\python.exe -m playwright --version
.\.venv\Scripts\python.exe -c "from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(headless=True); page=b.new_page(viewport={'width': 1600, 'height': 900}); page.set_content('<html><body><h1>OK</h1></body></html>'); page.screenshot(path='playwright_smoke.png'); b.close(); p.stop(); print('OK')"
```

`playwright_smoke.png` is a local generated artifact and must not be committed.

## Quality Gate

`quality_gate.py` keeps invoking `visual_regression.py` without forcing screenshot mode. Because the default is `--mode auto`, the quality gate benefits from screenshots when Playwright is available and remains stable through fallback otherwise.

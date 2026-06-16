# OFZ_ANALITICS

Python-first pipeline РґР»СЏ Р°РЅР°Р»РёС‚РёРєРё СЂР°Р·РјРµС‰РµРЅРёР№ РћР¤Р—. РџСЂРѕРµРєС‚ РіРѕС‚РѕРІРёС‚ РѕС‡РёС‰РµРЅРЅС‹Рµ datasets, РїР°СЂР°РјРµС‚СЂРёР·СѓРµРјС‹Р№ report scope, Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹, РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Рµ HTML-РіСЂР°С„РёРєРё, monthly layer, dashboard-ready exports Рё executive summary.

РџРµСЂРІР°СЏ РјРѕРґРµСЂРЅРёР·Р°С†РёСЏ РїСЂРѕРµРєС‚Р° Р·Р°РІРµСЂС€РµРЅР° РїРѕР»РЅРѕСЃС‚СЊСЋ. РўРµРєСѓС‰РёРµ Р±Р»РѕРєРё `quality_gate.py`, `visual_regression.py`, `run_manifest.py`, `anomaly_tests.py`, `semantic_model_v2`, revenue analytics Рё revenue charts РѕС‚РЅРѕСЃСЏС‚СЃСЏ РєРѕ РІС‚РѕСЂРѕР№ РјРѕРґРµСЂРЅРёР·Р°С†РёРё Рё РґРѕР±Р°РІР»РµРЅС‹ РїРѕРІРµСЂС… СѓР¶Рµ СЃС‚Р°Р±РёР»РёР·РёСЂРѕРІР°РЅРЅРѕР№ Р±Р°Р·С‹.

Р’СЃРµ РєРѕРјР°РЅРґС‹ РЅРёР¶Рµ РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ РёР· РєРѕСЂРЅСЏ РїСЂРѕРµРєС‚Р° `OFZ_ANALITICS` С‡РµСЂРµР· Р»РѕРєР°Р»СЊРЅС‹Р№ Python:

```powershell
.\.venv\Scripts\python.exe
```

РђР±СЃРѕР»СЋС‚РЅС‹Рµ РїСѓС‚Рё Рє Python РІ РєРѕРјР°РЅРґР°С… РЅРµ РёСЃРїРѕР»СЊР·СѓСЋС‚СЃСЏ.

## РќР°Р·РЅР°С‡РµРЅРёРµ РїСЂРѕРµРєС‚Р°

РџСЂРѕРµРєС‚ РїРѕР·РІРѕР»СЏРµС‚:

- Р°РЅР°Р»РёР·РёСЂРѕРІР°С‚СЊ СЂР°Р·РјРµС‰РµРЅРёСЏ РћР¤Р— РїРѕ Р°СѓРєС†РёРѕРЅР°Рј Рё Р”Р РџРђ;
- СЃСЂР°РІРЅРёРІР°С‚СЊ РѕС‚С‡РµС‚РЅС‹Р№ РїРµСЂРёРѕРґ СЃ СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІРѕР№ РїСЂРѕС€Р»С‹С… Р»РµС‚;
- С„РѕСЂРјРёСЂРѕРІР°С‚СЊ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹;
- СЃС‚СЂРѕРёС‚СЊ РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Рµ РІРёР·СѓР°Р»РёР·Р°С†РёРё;
- РѕР±СЉСЏСЃРЅСЏС‚СЊ РЅР°РєРѕРїР»РµРЅРЅС‹Р№ РёС‚РѕРі С‡РµСЂРµР· monthly layer;
- РіРѕС‚РѕРІРёС‚СЊ BI-ready dashboard exports Рё semantic layer;
- РїСЂРѕРІРµСЂСЏС‚СЊ СЃС…РµРјСѓ, РІРѕСЃРїСЂРѕРёР·РІРѕРґРёРјРѕСЃС‚СЊ Рё РєР°С‡РµСЃС‚РІРѕ РіСЂР°С„РёРєРѕРІ;
- Р°РєРєСѓСЂР°С‚РЅРѕ РѕСЂРіР°РЅРёР·РѕРІС‹РІР°С‚СЊ outputs Р±РµР· СѓРґР°Р»РµРЅРёСЏ РёСЃС…РѕРґРЅС‹С… РґР°РЅРЅС‹С….

`data/raw/` РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ С‚РѕР»СЊРєРѕ РєР°Рє РёСЃС‚РѕС‡РЅРёРє С‡С‚РµРЅРёСЏ Рё РЅРµ РґРѕР»Р¶РµРЅ РёР·РјРµРЅСЏС‚СЊСЃСЏ pipeline-СЃРєСЂРёРїС‚Р°РјРё.

## РЎС‚СЂСѓРєС‚СѓСЂР° РїСЂРѕРµРєС‚Р°

```text
data/raw/                         РёСЃС…РѕРґРЅС‹Рµ Excel/CSV
data/processed/                   РѕС‡РёС‰РµРЅРЅС‹Рµ Рё СЂР°СЃС‡РµС‚РЅС‹Рµ datasets
docs/                             РїСЂРѕРµРєС‚РЅР°СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ
logs/                             pipeline.log
outputs/charts/                   HTML-РіСЂР°С„РёРєРё
outputs/reports/                  С‡РµР»РѕРІРµРєРѕС‡РёС‚Р°РµРјС‹Рµ РѕС‚С‡РµС‚С‹
outputs/reports/analytical_tables/ РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ XLSX-С‚Р°Р±Р»РёС†С‹
outputs/reports/monthly_tables/   monthly XLSX-С‚Р°Р±Р»РёС†С‹
outputs/exports/analytical_csv/   CSV-РєРѕРїРёРё РѕС‚С‡РµС‚РЅС‹С… С‚Р°Р±Р»РёС†
outputs/exports/chart_data/       CSV-РѕСЃРЅРѕРІС‹ РіСЂР°С„РёРєРѕРІ
outputs/dashboards/               BI-ready exports
outputs/archive/                  Р°СЂС…РёРІРЅС‹Рµ outputs
prompts/                          СЂР°Р±РѕС‡РёРµ РїСЂРѕРјРїС‚С‹ РїСЂРѕРµРєС‚Р°
scripts/                          Python-СЃРєСЂРёРїС‚С‹ pipeline
```

## РўСЂРµР±РѕРІР°РЅРёСЏ Рє РѕРєСЂСѓР¶РµРЅРёСЋ

- Windows Рё PowerShell РєР°Рє РѕР±РѕР»РѕС‡РєР° Р·Р°РїСѓСЃРєР°;
- Python РІ Р»РѕРєР°Р»СЊРЅРѕРј `.venv`;
- Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РёР· `requirements.txt`, РµСЃР»Рё С„Р°Р№Р» РїСЂРёСЃСѓС‚СЃС‚РІСѓРµС‚;
- Р·Р°РїСѓСЃРє РєРѕРјР°РЅРґ РёР· РєРѕСЂРЅСЏ РїСЂРѕРµРєС‚Р°.

РџСЂРѕРІРµСЂРёС‚СЊ Python:

```powershell
.\.venv\Scripts\python.exe --version
```

Python version policy:

- package metadata supports Python `>=3.11,<3.15`;
- current production baseline was actually tested on Python `3.14.5`;
- source syntax was checked as Python 3.11-compatible;
- runtime dependency metadata requires Python `>=3.11` at the strictest point (`pandas`/`numpy`);
- if another Python version from the supported range is used, run `quality_gate.py --fast` before relying on outputs.

РЈСЃС‚Р°РЅРѕРІРёС‚СЊ Р·Р°РІРёСЃРёРјРѕСЃС‚Рё:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Dev/QA dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Dependency check:

```powershell
.\.venv\Scripts\python.exe -m pip check
```

Editable install and CLI entry points:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\ofz-run.exe --help
.\.venv\Scripts\ofz-quality.exe --help
.\.venv\Scripts\ofz-schema.exe --help
.\.venv\Scripts\ofz-clean-outputs.exe --help
.\.venv\Scripts\ofz-build-release-bundle.exe --help
```

Existing script launch commands remain supported. `ofz-clean-outputs` is a safe maintenance entry point for generated `outputs/`: it defaults to dry-run and requires `--confirm DELETE_OUTPUTS` for deletion. `ofz-build-release-bundle` creates an external release bundle under ignored `releases/` and requires `--include-outputs --confirm BUILD_RELEASE_BUNDLE` outside dry-run.

Environment details are documented in [`docs/07_operations/environment.md`](docs/07_operations/environment.md).

Safe outputs cleanup:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --dry-run
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --archive-all
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_outputs.py --delete-all --confirm DELETE_OUTPUTS
```

The cleanup command only works inside `outputs/`, preserves `outputs/archive/`, writes cleanup manifests, and recreates the tracked folder skeleton with `.gitkeep`.

Release bundle dry-run:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Release bundle creation:

```powershell
.\.venv\Scripts\ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI release package dry-run:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI release package creation:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\build_bi_package.py --include-outputs --confirm BUILD_BI_PACKAGE --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

BI package is an external artifact under ignored `releases/bi/`. It is documented in [`docs/07_operations/bi_release_package.md`](docs/07_operations/bi_release_package.md) and governed by [`docs/02_data_contracts/bi_exports_contract.md`](docs/02_data_contracts/bi_exports_contract.md).

The bundle is written to `releases/ofz_analytics_<report_date>_<period_type>_<aggregation_mode>_retrospective_<N>_<timestamp>/`, which is excluded from Git. The bundle includes generated HTML charts, chart data, dashboard exports, run manifests, QA reports and release manifests.

Pipeline telemetry:

```powershell
.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Each full pipeline run writes telemetry summaries to `outputs/reports/telemetry/telemetry_<run_id>.json` and `.md`. Telemetry records stage durations, artifact counts and sizes, cleanup mode, quality/schema status, Git commit/dirty flag and raw data hashes. These generated telemetry files are not committed and are included in release bundles when present.

Windows UI launcher MVP:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui
```

The default launcher action is a safe smoke check. The GUI mode calls only approved CLI entry points, validates report parameters, writes logs to `outputs/reports/launcher/`, blocks delete cleanup without `DELETE_OUTPUTS`, and blocks release bundle creation without `BUILD_RELEASE_BUNDLE`. The GUI includes project root, report date, retrospective years, period type, aggregation mode, action, cleanup mode, release/cleanup confirmations, command preview and output/status fields.

Русскоязычная UX-инструкция по полям, сценариям, Preview, run-pipeline и логам: [`tools/windows_launcher/README.md`](tools/windows_launcher/README.md).

UI launchers do not replace the CLI or quality gate. The supported production interface remains the CLI (`ofz-run`, `ofz-quality`, `ofz-schema`, `ofz-clean-outputs`, `ofz-build-release-bundle`). The PowerShell launcher is the recommended Windows UI MVP for operators who need a guided local launcher.

Word VBA launcher source:

```text
tools/word_launcher/OfzLauncher.bas
tools/word_launcher/README.md
docs/07_operations/word_vba_launcher_spec.md
```

The `.bas` source can be committed. A future `.docm` file is a release artifact, not a source artifact, and must not be committed without a separate artifact policy decision. The VBA launcher calls only whitelisted CLI entry points and applies the same `DELETE_OUTPUTS` and `BUILD_RELEASE_BUNDLE` confirmation gates.

Word VBA is optional. Text source files (`.bas`, `.frm`) are source artifacts; `.docm` packages are release artifacts unless explicitly approved by artifact policy. Launcher logs under `outputs/reports/launcher/` are generated outputs and are excluded from Git. Release bundles remain external artifacts under ignored `releases/`.

Interactive cleanup pre-flight:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

Before running the selected pipeline command, the interactive launcher checks whether generated `outputs/` artifacts already exist. If they do, it offers to keep outputs, run cleanup dry-run, archive and clean outputs, clean without archive after explicit `DELETE_OUTPUTS_NO_ARCHIVE`, or cancel the run. The launcher never deletes files directly: it calls `scripts/maintenance/cleanup_outputs.py` and stops the pipeline if cleanup fails. The selected cleanup status is recorded in the run manifest for full interactive runs.

РРЅС‚РµСЂР°РєС‚РёРІРЅР°СЏ Р°РєС‚РёРІР°С†РёСЏ `.venv`, РµСЃР»Рё РЅСѓР¶РЅР°:

```powershell
.\.venv\Scripts\Activate.ps1
```

## РџР°СЂР°РјРµС‚СЂС‹ Р·Р°РїСѓСЃРєР°

РћСЃРЅРѕРІРЅС‹Рµ РїР°СЂР°РјРµС‚СЂС‹:

- `--report-date` вЂ” РѕС‚С‡РµС‚РЅР°СЏ РґР°С‚Р°, РІСЃРµРіРґР° РїРµСЂРІРѕРµ С‡РёСЃР»Рѕ РјРµСЃСЏС†Р°;
- `--period-type` вЂ” `month`, `quarter` РёР»Рё `year`;
- `--retrospective-years` вЂ” С‡РёСЃР»Рѕ Р»РµС‚ СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІС‹;
- `--aggregation-mode` вЂ” `cumulative` РёР»Рё `point`;
- `--stage` вЂ” Р·Р°РїСѓСЃРє РѕРґРЅРѕРіРѕ СЌС‚Р°РїР°;
- `--stages` вЂ” Р·Р°РїСѓСЃРє РЅРµСЃРєРѕР»СЊРєРёС… СЌС‚Р°РїРѕРІ;
- `--all` вЂ” РїРѕР»РЅС‹Р№ Р·Р°РїСѓСЃРє;
- `--safe` вЂ” safe reproduction mode РґР»СЏ СЂР°РЅРЅРёС… СЌС‚Р°РїРѕРІ;
- `--compare` вЂ” СЃСЂР°РІРЅРµРЅРёРµ outputs, РµСЃР»Рё РїСЂРёРјРµРЅРёРјРѕ;
- `--interactive` вЂ” РёРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ СЂРµР¶РёРј РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂР°.

### cumulative Рё point

`cumulative` РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ.

- `month + cumulative + report_date=2026-05-01` РѕР·РЅР°С‡Р°РµС‚ СЏРЅРІР°СЂСЊ-Р°РїСЂРµР»СЊ 2026.
- `month + point + report_date=2026-05-01` РѕР·РЅР°С‡Р°РµС‚ С‚РѕР»СЊРєРѕ Р°РїСЂРµР»СЊ 2026.
- `quarter + cumulative + report_date=2026-07-01` РѕР·РЅР°С‡Р°РµС‚ СЏРЅРІР°СЂСЊ-РёСЋРЅСЊ 2026.
- `quarter + point + report_date=2026-07-01` РѕР·РЅР°С‡Р°РµС‚ С‚РѕР»СЊРєРѕ II РєРІР°СЂС‚Р°Р» 2026.
- `year + report_date=2026-01-01` РѕР·РЅР°С‡Р°РµС‚ Р·Р°РІРµСЂС€РµРЅРЅС‹Р№ 2025 РіРѕРґ.

Р РµС‚СЂРѕСЃРїРµРєС‚РёРІР° СЃСЂР°РІРЅРёРІР°РµС‚ Р°РЅР°Р»РѕРіРёС‡РЅС‹Рµ РёРЅС‚РµСЂРІР°Р»С‹ РїСЂРѕС€Р»С‹С… Р»РµС‚. Outputs `cumulative` Рё `point` РЅРµ СЃРјРµС€РёРІР°СЋС‚СЃСЏ: СЂРµР¶РёРј Р°РіСЂРµРіР°С†РёРё РІС…РѕРґРёС‚ РІ РёРјРµРЅР° С„Р°Р№Р»РѕРІ.

## Р‘С‹СЃС‚СЂС‹Р№ Р·Р°РїСѓСЃРє

РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ launcher:

```powershell
.\.venv\Scripts\python.exe scripts\interactive_pipeline.py
```

РРЅС‚РµСЂР°РєС‚РёРІРЅС‹Р№ launcher СЃРїСЂР°С€РёРІР°РµС‚ `report_date`, `period_type`, `aggregation_mode`, `retrospective_years`, СЂРµР¶РёРј Р·Р°РїСѓСЃРєР° Рё РїРѕРґС‚РІРµСЂР¶РґРµРЅРёРµ РїРµСЂРµРґ РІС‹РїРѕР»РЅРµРЅРёРµРј. Р”РѕСЃС‚СѓРїРЅС‹Рµ СЂРµР¶РёРјС‹:

Р•СЃР»Рё РІ `outputs/` СѓР¶Рµ РµСЃС‚СЊ generated artifacts, launcher РїРµСЂРµРґ Р·Р°РїСѓСЃРєРѕРј РїРѕРєР°Р·С‹РІР°РµС‚ cleanup pre-flight menu. Default-РґРµР№СЃС‚РІРёРµ: РѕСЃС‚Р°РІРёС‚СЊ outputs РєР°Рє РµСЃС‚СЊ. РђСЂС…РёРІР°С†РёСЏ Рё РѕС‡РёСЃС‚РєР° РІС‹РїРѕР»РЅСЏСЋС‚СЃСЏ С‚РѕР»СЊРєРѕ С‡РµСЂРµР· `scripts/maintenance/cleanup_outputs.py`; РѕС‡РёСЃС‚РєР° Р±РµР· Р°СЂС…РёРІР° С‚СЂРµР±СѓРµС‚ РІРІРѕРґР° `DELETE_OUTPUTS_NO_ARCHIVE`.

- `all` вЂ” РїРѕР»РЅС‹Р№ pipeline;
- `stages` вЂ” СЂСѓС‡РЅРѕР№ СЃРїРёСЃРѕРє stage numbers / stage names;
- `validate` вЂ” С„РѕСЂРјРёСЂРѕРІР°РЅРёРµ report scope;
- `charts` вЂ” report scope Рё РѕСЃРЅРѕРІРЅС‹Рµ РіСЂР°С„РёРєРё;
- `tables` вЂ” report scope Рё Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹;
- `monthly` вЂ” monthly layer Рё РїРѕРјРµСЃСЏС‡РЅС‹Рµ РіСЂР°С„РёРєРё;
- `dashboard` вЂ” dashboard exports Рё semantic model v2;
- `revenue` вЂ” С‚Р°Р±Р»РёС†С‹ Рё РіСЂР°С„РёРєРё РІС‹СЂСѓС‡РєРё;
- `quality` вЂ” quality gate РІ fast-СЂРµР¶РёРјРµ;
- `anomaly` вЂ” anomaly tests;
- `manifest` вЂ” run manifest;
- `semantic` вЂ” semantic model v2.

РџРѕР»РЅС‹Р№ РјРµСЃСЏС‡РЅС‹Р№ РѕС‚С‡РµС‚ РЅР°РєРѕРїР»РµРЅРЅС‹Рј РёС‚РѕРіРѕРј:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

РџРѕР»РЅС‹Р№ РјРµСЃСЏС‡РЅС‹Р№ РѕС‚С‡РµС‚ Р·Р° РѕРґРёРЅ РјРµСЃСЏС†:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode point
```

РџРѕР»РЅС‹Р№ РєРІР°СЂС‚Р°Р»СЊРЅС‹Р№ РѕС‚С‡РµС‚:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-04-01 --retrospective-years 2 --period-type quarter --aggregation-mode cumulative
```

РџРѕР»РЅС‹Р№ РіРѕРґРѕРІРѕР№ РѕС‚С‡РµС‚:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-01-01 --retrospective-years 5 --period-type year --aggregation-mode cumulative
```

Р—Р°РїСѓСЃРє СЌС‚Р°РїРѕРІ 1-3:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stages 1 2 3 --report-date 2026-04-01 --retrospective-years 2 --period-type quarter --aggregation-mode cumulative
```

## РџРѕСЂСЏРґРѕРє РїРѕР»РЅРѕРіРѕ pipeline

РџСЂРё `--all` РѕСЂРєРµСЃС‚СЂР°С‚РѕСЂ Р·Р°РїСѓСЃРєР°РµС‚:

1. `scripts\01_data_audit.py` вЂ” Р°СѓРґРёС‚ РёСЃС…РѕРґРЅС‹С… РґР°РЅРЅС‹С….
2. `scripts\02_data_cleaning.py` вЂ” РѕС‡РёСЃС‚РєР° РґР°РЅРЅС‹С….
3. `scripts\03_feature_engineering.py` вЂ” СЂР°СЃС‡РµС‚ РїСЂРёР·РЅР°РєРѕРІ.
4. `scripts\period_filter.py` вЂ” report scope dataset.
5. `scripts\04_kpi_map.py` вЂ” РєР°СЂС‚Р° KPI.
6. `scripts\05_visualization_strategy.py` вЂ” СЃС‚СЂР°С‚РµРіРёСЏ РІРёР·СѓР°Р»РёР·Р°С†РёР№.
7. `scripts\06_build_charts.py` вЂ” HTML-РіСЂР°С„РёРєРё.
8. `scripts\08_analytical_tables.py` вЂ” РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹.
9. `scripts\11_revenue_analytics.py` вЂ” С‚Р°Р±Р»РёС†С‹ РІС‹СЂСѓС‡РєРё РѕС‚ СЂРµР°Р»РёР·Р°С†РёРё РћР¤Р—.
10. `scripts\12_build_revenue_charts.py` вЂ” РіСЂР°С„РёРєРё РІС‹СЂСѓС‡РєРё РѕС‚ СЂРµР°Р»РёР·Р°С†РёРё РћР¤Р—.
11. Р”РѕРєСѓРјРµРЅС‚ dashboard architecture.
12. `scripts\07_dashboard_exports.py` вЂ” dashboard exports.
13. `scripts\build_semantic_model_v2.py` вЂ” semantic model v2 РґР»СЏ dashboard.
14. `scripts\generate_executive_summary.py` вЂ” executive summary.
15. Self-review.
16. Final project summary.
17. Run manifest вЂ” Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё РїРѕСЃР»Рµ СѓСЃРїРµС€РЅРѕРіРѕ `--all`.

Monthly layer Рё monthly charts РґРѕСЃС‚СѓРїРЅС‹ РєР°Рє РѕС‚РґРµР»СЊРЅС‹Рµ СЌС‚Р°РїС‹ Рё РІС…РѕРґСЏС‚ РІ `--all`, РµСЃР»Рё СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РёРµ СЃРєСЂРёРїС‚С‹ РїСЂРёСЃСѓС‚СЃС‚РІСѓСЋС‚.

Р”РѕРїРѕР»РЅРёС‚РµР»СЊРЅС‹Рµ stage names / stage numbers РІС‚РѕСЂРѕР№ РјРѕРґРµСЂРЅРёР·Р°С†РёРё:

| РќРѕРјРµСЂ | Stage name | РЎРєСЂРёРїС‚ / РґРµР№СЃС‚РІРёРµ | РљР°Рє Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ |
|---|---|---|---|
| 13.1 | `run_manifest` | Р·Р°РїРёСЃСЊ run manifest | РѕС‚РґРµР»СЊРЅРѕ С‡РµСЂРµР· `--stage run_manifest`, РїРѕСЃР»Рµ `--all` СЃРѕР·РґР°РµС‚СЃСЏ Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРё |
| 13.2 | `quality_gate` | `scripts\quality_gate.py` | РѕС‚РґРµР»СЊРЅРѕ С‡РµСЂРµР· `--stage quality_gate`; РёР· pipeline РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ fast mode |
| 13.3 | `anomaly_tests` | `scripts\anomaly_tests.py` | РѕС‚РґРµР»СЊРЅРѕ С‡РµСЂРµР· `--stage anomaly_tests` |
| 13.4 | `revenue_analytics` | `scripts\11_revenue_analytics.py` | РІС…РѕРґРёС‚ РІ `--all`, РјРѕР¶РЅРѕ Р·Р°РїСѓСЃРєР°С‚СЊ РѕС‚РґРµР»СЊРЅРѕ |
| 13.5 | `revenue_charts` | `scripts\12_build_revenue_charts.py` | РІС…РѕРґРёС‚ РІ `--all`, РјРѕР¶РЅРѕ Р·Р°РїСѓСЃРєР°С‚СЊ РѕС‚РґРµР»СЊРЅРѕ |
| 13.6 | `semantic_model_v2` | `scripts\build_semantic_model_v2.py` | РІС…РѕРґРёС‚ РІ `--all`, РјРѕР¶РЅРѕ Р·Р°РїСѓСЃРєР°С‚СЊ РѕС‚РґРµР»СЊРЅРѕ |

## РћС‚РґРµР»СЊРЅС‹Рµ СЃРєСЂРёРїС‚С‹

РђСѓРґРёС‚ РёСЃС…РѕРґРЅС‹С… РґР°РЅРЅС‹С…:

```powershell
.\.venv\Scripts\python.exe scripts\01_data_audit.py
```

РћС‡РёСЃС‚РєР°:

```powershell
.\.venv\Scripts\python.exe scripts\02_data_cleaning.py
```

Feature engineering:

```powershell
.\.venv\Scripts\python.exe scripts\03_feature_engineering.py
```

Р’С‹Р±РѕСЂ report scope:

```powershell
.\.venv\Scripts\python.exe scripts\period_filter.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

KPI map:

```powershell
.\.venv\Scripts\python.exe scripts\04_kpi_map.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Р“СЂР°С„РёРєРё:

```powershell
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

РђРЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹:

```powershell
.\.venv\Scripts\python.exe scripts\08_analytical_tables.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Monthly analytics:

```powershell
.\.venv\Scripts\python.exe scripts\09_monthly_analytics.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Monthly charts:

```powershell
.\.venv\Scripts\python.exe scripts\10_build_monthly_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Revenue analytics:

```powershell
.\.venv\Scripts\python.exe scripts\11_revenue_analytics.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Revenue charts:

```powershell
.\.venv\Scripts\python.exe scripts\12_build_revenue_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Dashboard exports:

```powershell
.\.venv\Scripts\python.exe scripts\07_dashboard_exports.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Semantic model v2:

```powershell
.\.venv\Scripts\python.exe scripts\build_semantic_model_v2.py
```

Executive summary:

```powershell
.\.venv\Scripts\python.exe scripts\generate_executive_summary.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Raw data registry:

```powershell
.\.venv\Scripts\python.exe scripts\raw_data_registry.py
```

Run manifest С‡РµСЂРµР· pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage run_manifest --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Quality gate С‡РµСЂРµР· pipeline РІ fast-СЂРµР¶РёРјРµ:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage quality_gate --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Quality gate РЅР°РїСЂСЏРјСѓСЋ РІ full-СЂРµР¶РёРјРµ:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression / fallback HTML inspection:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression modes after P2.7:

```powershell
# Contract/static inspection only
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode fallback --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

# Try Playwright screenshots, then fallback if unavailable
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative

# Require screenshot backend
.\.venv\Scripts\python.exe scripts\visual_regression.py --mode screenshot --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Playwright screenshot backend is a dev/QA dependency. Install it when screenshot mode is needed:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

In the Codex managed sandbox browser subprocesses can be blocked by Windows pipe permissions. If `--mode auto` records a sandbox warning, run `--mode screenshot` from the project PowerShell session. A local smoke file such as `playwright_smoke.png` is a generated artifact and must not be committed.

Anomaly tests:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage anomaly_tests
```

Anomaly tests РЅР°РїСЂСЏРјСѓСЋ:

```powershell
.\.venv\Scripts\python.exe scripts\anomaly_tests.py
```

Semantic model v2 С‡РµСЂРµР· pipeline:

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --stage semantic_model_v2
```

Run manifest РЅР°РїСЂСЏРјСѓСЋ:

```powershell
.\.venv\Scripts\python.exe scripts\run_manifest.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --stages all
```

## Outputs

РћСЃРЅРѕРІРЅС‹Рµ СЂРµР·СѓР»СЊС‚Р°С‚С‹:

- `data/processed/ofz_auctions_clean.csv`;
- `data/processed/ofz_auctions_features.csv`;
- `data/processed/ofz_auctions_report_scope.csv`;
- `data/processed/ofz_monthly_metrics.csv`;
- `outputs/charts/**/*.html`;
- `outputs/reports/analytical_tables/*.xlsx`;
- `outputs/reports/monthly_tables/*.xlsx`;
- `outputs/reports/executive_summary_<...>.md`;
- `outputs/reports/run_manifest_<run_id>.json`;
- `outputs/reports/run_manifest_<run_id>.md`;
- `outputs/reports/quality_gate_report_<run_id>.md`;
- `outputs/reports/visual_regression/**/*.md`;
- `outputs/exports/analytical_csv/*.csv`;
- `outputs/exports/chart_data/**/*.csv`;
- `outputs/dashboards/**/*.csv`;
- `outputs/dashboards/**/*.json`;
- `outputs/dashboards/semantic_layer/*`;
- `outputs/dashboards/semantic_model_v2/*`.

РћС‚С‡РµС‚РЅС‹Рµ `.xlsx` РЅРµ РґРѕР»Р¶РЅС‹ СЃРѕС…СЂР°РЅСЏС‚СЊСЃСЏ РЅР°РїСЂСЏРјСѓСЋ РІ РєРѕСЂРµРЅСЊ `outputs/exports/`.

Revenue outputs:

- `outputs/reports/analytical_tables/revenue_summary_<...>.xlsx`;
- `outputs/exports/analytical_csv/revenue_summary_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_by_ofz_type_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_by_maturity_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_by_format_<...>.csv`;
- `outputs/exports/analytical_csv/revenue_monthly_<...>.csv`;
- `outputs/exports/chart_data/structure/revenue_*_<...>.csv`;
- `outputs/charts/revenue/**/*.html`;
- `outputs/charts/scatter/discount_revenue_gap/discount_vs_revenue_gap_<...>.html`.

## Р’РёР·СѓР°Р»РёР·Р°С†РёРё

РљР»СЋС‡РµРІС‹Рµ РіСЂР°С„РёРєРё:

- РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РћР¤Р— РїРѕ РЅРѕРјРёРЅР°Р»Сѓ;
- СЃРїСЂРѕСЃ Рё РїСЂРµРґР»РѕР¶РµРЅРёРµ;
- РїРѕРєСЂС‹С‚РёРµ РїСЂРµРґР»РѕР¶РµРЅРёСЏ СЃРїСЂРѕСЃРѕРј;
- РґРѕС…РѕРґРЅРѕСЃС‚СЊ РїРѕ РІРёРґР°Рј РћР¤Р—;
- СЃС‚СЂСѓРєС‚СѓСЂР° РїРѕ СЃСЂРѕРєР°Рј;
- СЃС‚СЂСѓРєС‚СѓСЂР° РїРѕ С„РѕСЂРјР°С‚Р°Рј;
- risk quadrant;
- СЂРµС‚СЂРѕСЃРїРµРєС‚РёРІРЅС‹Р№ risk quadrant;
- boxplot РґРѕС…РѕРґРЅРѕСЃС‚Рё РїРѕ РІРёРґР°Рј РћР¤Р—;
- РіСЂР°С„РёРє РѕС‚СЃРµС‡РµРЅРёСЏ СЃРїСЂРѕСЃР°;
- Sankey-РіСЂР°С„РёРєРё СЃС‚СЂСѓРєС‚СѓСЂС‹ СЂР°Р·РјРµС‰РµРЅРёР№;
- monthly charts.
- revenue charts РїРѕ РІС‹СЂСѓС‡РєРµ РѕС‚ СЂРµР°Р»РёР·Р°С†РёРё.

Р”Р»СЏ РіСЂР°С„РёРєРѕРІ СЃ РѕР±СЉРµРјРѕРј СЂР°Р·РјРµС‰РµРЅРёСЏ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РµРґРёРЅС‹Р№ СЃС‚Р°РЅРґР°СЂС‚: РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ, РјР»СЂРґ СЂСѓР±Р»РµР№.

Revenue-РіСЂР°С„РёРєРё С‚Р°РєР¶Рµ РёСЃРїРѕР»СЊР·СѓСЋС‚ РјР»СЂРґ СЂСѓР±Р»РµР№ Рё СЃС‚СЂРѕСЏС‚СЃСЏ РїРѕ С‚Р°Р±Р»РёС†Р°Рј Р­С‚Р°РїР° 10:

- `revenue_vs_nominal_by_period`;
- `nominal_revenue_gap_by_period`;
- `revenue_to_nominal_ratio`;
- `monthly_revenue_vs_nominal`;
- `monthly_nominal_revenue_gap`;
- `revenue_gap_by_ofz_type`;
- `revenue_gap_by_maturity`;
- `discount_vs_revenue_gap`.

## Dashboard exports

Dashboard-ready С„Р°Р№Р»С‹ СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/dashboards/`.

РћСЃРЅРѕРІРЅС‹Рµ datasets:

- `dashboard_auction_level_<...>.csv`;
- `dashboard_period_summary_<...>.csv`;
- `dashboard_kpi_summary_<...>.csv`;
- `dashboard_maturity_structure_<...>.csv`;
- `dashboard_yield_distribution_<...>.csv`;
- `dashboard_demand_supply_<...>.csv`;
- `dashboard_metadata_<...>.json`;
- `dashboard_data_dictionary_<...>.csv`;
- `dashboard_monthly_metrics_<...>.csv`;
- `dashboard_monthly_data_dictionary_<...>.csv`;
- semantic layer РїРµСЂРІРѕРіРѕ РїРѕРєРѕР»РµРЅРёСЏ РІ `outputs/dashboards/semantic_layer/`;
- semantic model v2 РІ `outputs/dashboards/semantic_model_v2/`.

Semantic model v2 РІРєР»СЋС‡Р°РµС‚:

- `field_dictionary.csv`;
- `kpi_dictionary.csv`;
- `measures.csv`;
- `model_manifest.json`.

## РџСЂРѕРІРµСЂРєРё РєР°С‡РµСЃС‚РІР°

РљРѕРјРїРёР»СЏС†РёСЏ РєР»СЋС‡РµРІС‹С… СЃРєСЂРёРїС‚РѕРІ:

```powershell
.\.venv\Scripts\python.exe -m py_compile scripts\run_pipeline.py
.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py
.\.venv\Scripts\python.exe -m py_compile scripts\08_analytical_tables.py
.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py
```

Schema validation:

```powershell
.\.venv\Scripts\python.exe scripts\schema_validation.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Regression tests:

```powershell
.\.venv\Scripts\python.exe scripts\regression_tests.py
```

Smoke tests:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_tests.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

HTML chart QA:

```powershell
.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Visual regression / fallback HTML inspection:

```powershell
.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Anomaly tests:

```powershell
.\.venv\Scripts\python.exe scripts\anomaly_tests.py
```

Run manifest:

```powershell
.\.venv\Scripts\python.exe scripts\run_manifest.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative --stages all
```

Quality gate:

```powershell
.\.venv\Scripts\python.exe scripts\quality_gate.py --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Quality gate РѕР±СЉРµРґРёРЅСЏРµС‚ `py_compile`, `schema_validation.py`, `regression_tests.py`, `anomaly_tests.py`, `smoke_tests.py`, `html_chart_qa.py`, `visual_regression.py`, РїСЂРѕРІРµСЂРєРё README, outputs structure, run manifest Рё dashboard semantic model. Р•СЃР»Рё С‡Р°СЃС‚СЊ РїСЂРѕРІРµСЂРѕРє РЅРµРґРѕСЃС‚СѓРїРЅР°, СЂРµР·СѓР»СЊС‚Р°С‚ С„РёРєСЃРёСЂСѓРµС‚СЃСЏ РєР°Рє warning, Р° РѕСЃС‚Р°Р»СЊРЅС‹Рµ РїСЂРѕРІРµСЂРєРё РїСЂРѕРґРѕР»Р¶Р°СЋС‚СЃСЏ.

## РЈРїРѕСЂСЏРґРѕС‡РёРІР°РЅРёРµ outputs

Dry-run:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

Production delete/archive modes описаны в `docs/07_operations/production_runbook.md`; destructive cleanup требует explicit confirmation token.

Legacy migration reports are archive/audit documents and are not part of the active production contract.

## РњРµС‚РѕРґРѕР»РѕРіРёС‡РµСЃРєРёРµ РїСЂР°РІРёР»Р°

Р¤РѕСЂРјР°С‚ СЂР°Р·РјРµС‰РµРЅРёСЏ:

- `format` СЃРѕС…СЂР°РЅСЏРµС‚СЃСЏ РєР°Рє РѕС‚РґРµР»СЊРЅР°СЏ РєРѕР»РѕРЅРєР°;
- `format_assumption_flag` С„РёРєСЃРёСЂСѓРµС‚ СѓРІРµСЂРµРЅРЅРѕСЃС‚СЊ РєР»Р°СЃСЃРёС„РёРєР°С†РёРё;
- Р”Р РџРђ РЅРµ РґРѕР»Р¶РЅС‹ РјРµС…Р°РЅРёС‡РµСЃРєРё РІРєР»СЋС‡Р°С‚СЊСЃСЏ РІ demand-based ratios Р±РµР· РѕРіСЂР°РЅРёС‡РµРЅРёСЏ.

РЎСЂРѕРєРё РѕР±СЂР°С‰РµРЅРёСЏ:

- `short_term` вЂ” РґРѕ 5 Р»РµС‚ РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ;
- `medium_term` вЂ” СЃРІС‹С€Рµ 5 Рё РґРѕ 10 Р»РµС‚ РІРєР»СЋС‡РёС‚РµР»СЊРЅРѕ;
- `long_term` вЂ” Р±РѕР»РµРµ 10 Р»РµС‚;
- `requires_review` вЂ” СЃСЂРѕРє РЅРµР»СЊР·СЏ РЅР°РґРµР¶РЅРѕ РѕРїСЂРµРґРµР»РёС‚СЊ.

РџРѕРєР°Р·Р°С‚РµР»Рё СЃРїСЂРѕСЃР° Рё РїРѕРєСЂС‹С‚РёСЏ:

- `demand_satisfaction_ratio = placement_volume / demand_volume`;
- `demand_to_placement_ratio = demand_volume / placement_volume`;
- `bid_to_cover_ratio = demand_volume / supply_volume`.

`demand_to_placement_ratio` РЅРµР»СЊР·СЏ РЅР°Р·С‹РІР°С‚СЊ РєР»Р°СЃСЃРёС‡РµСЃРєРёРј bid-to-cover.

РџРѕРєР°Р·Р°С‚РµР»Рё РІС‹СЂСѓС‡РєРё:

- `placement_volume` вЂ” РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ, РјР»РЅ СЂСѓР±Р»РµР№;
- `revenue_volume` вЂ” РІС‹СЂСѓС‡РєР° РѕС‚ СЂРµР°Р»РёР·Р°С†РёРё, РјР»РЅ СЂСѓР±Р»РµР№; С‚РµРєСѓС‰РёР№ source mapping РёСЃРїРѕР»СЊР·СѓРµС‚ `proceeds_mln_rub`, РµСЃР»Рё РєР°РЅРѕРЅРёС‡РµСЃРєРёР№ `revenue_volume` РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚;
- `nominal_revenue_gap = placement_volume - revenue_volume`;
- `revenue_to_nominal_ratio = revenue_volume / placement_volume`;
- `nominal_discount_ratio = nominal_revenue_gap / placement_volume`.

Р•СЃР»Рё РІС‹СЂСѓС‡РєР° РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ РёР»Рё Р·Р°РїРѕР»РЅРµРЅР° РЅРµРїРѕР»РЅРѕ, РїСЂРѕРµРєС‚ РЅРµ РІС‹РґСѓРјС‹РІР°РµС‚ Р·РЅР°С‡РµРЅРёСЏ: РѕРіСЂР°РЅРёС‡РµРЅРёРµ С„РёРєСЃРёСЂСѓРµС‚СЃСЏ С‡РµСЂРµР· `data_quality_flag`, `docs/03_analytics/revenue_analytics_report.md` Рё `docs/01_methodology/revenue_kpi_map.md`.

Revenue analytics СЃС‚СЂРѕРёС‚СЃСЏ С‚РѕР»СЊРєРѕ РїСЂРё РЅР°Р»РёС‡РёРё РЅР°РґРµР¶РЅРѕР№ РєРѕР»РѕРЅРєРё РІС‹СЂСѓС‡РєРё РёР»Рё СЃРѕРїРѕСЃС‚Р°РІРёРјРѕРіРѕ source mapping. Р•СЃР»Рё РґРѕСЃС‚СѓРїРµРЅ С‚РѕР»СЊРєРѕ РЅРѕРјРёРЅР°Р»СЊРЅС‹Р№ РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ, С‚Р°Р±Р»РёС†С‹ Рё РіСЂР°С„РёРєРё РІС‹СЂСѓС‡РєРё РЅРµ РґРѕР»Р¶РЅС‹ РїРѕРґРјРµРЅСЏС‚СЊ РІС‹СЂСѓС‡РєСѓ РЅРѕРјРёРЅР°Р»РѕРј.

`nominal_revenue_gap`, `revenue_to_nominal_ratio` Рё `nominal_discount_ratio` РёРЅС‚РµСЂРїСЂРµС‚РёСЂСѓСЋС‚СЃСЏ С‚РѕР»СЊРєРѕ РІ РїСЂРµРґРµР»Р°С… СЃС‚СЂРѕРє СЃ РІР°Р»РёРґРЅС‹РјРё `placement_volume` Рё `revenue_volume`.

## Р§Р°СЃС‚С‹Рµ РїСЂРѕР±Р»РµРјС‹

`run_pipeline.py` С‚СЂРµР±СѓРµС‚ `--stage`, `--stages` РёР»Рё `--all`.

```powershell
.\.venv\Scripts\python.exe scripts\run_pipeline.py --all --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Р•СЃР»Рё report scope РїСѓСЃС‚, СЃРЅР°С‡Р°Р»Р° РІС‹РїРѕР»РЅРёС‚Рµ СЌС‚Р°Рї 4:

```powershell
.\.venv\Scripts\python.exe scripts\period_filter.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Р•СЃР»Рё Excel-С„Р°Р№Р» РѕС‚РєСЂС‹С‚, Р·Р°РїРёСЃСЊ XLSX РјРѕР¶РµС‚ Р·Р°РІРµСЂС€РёС‚СЊСЃСЏ `PermissionError`. Р—Р°РєСЂРѕР№С‚Рµ С„Р°Р№Р» РёР»Рё РёСЃРїРѕР»СЊР·СѓР№С‚Рµ fallback-С„Р°Р№Р», РєРѕС‚РѕСЂС‹Р№ СЃРѕР·РґР°СЋС‚ СЃРєСЂРёРїС‚С‹.

Р•СЃР»Рё `html_chart_qa.py` СЃРѕРѕР±С‰Р°РµС‚ Рѕ СЃС‚Р°СЂС‹С… РіСЂР°С„РёРєР°С…, РїРµСЂРµСЃРѕР±РµСЂРёС‚Рµ РіСЂР°С„РёРєРё РїРµСЂРµРґ QA:

```powershell
.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative
```

Р•СЃР»Рё outputs РїРµСЂРµРїСѓС‚Р°РЅС‹ РїРѕСЃР»Рµ СЃС‚Р°СЂС‹С… Р·Р°РїСѓСЃРєРѕРІ, СЃРЅР°С‡Р°Р»Р° РІС‹РїРѕР»РЅРёС‚Рµ dry-run СЂРµРѕСЂРіР°РЅРёР·Р°С†РёРё:

```powershell
.\.venv\Scripts\ofz-clean-outputs.exe --dry-run
```

## РћРіСЂР°РЅРёС‡РµРЅРёСЏ

- РРЅРІРµРЅС‚Р°СЂРёР·Р°С†РёСЏ С„Р°Р№Р»РѕРІ РЅРµ Р·Р°РјРµРЅСЏРµС‚ runtime-РїСЂРѕРІРµСЂРєСѓ СЂР°СЃС‡РµС‚РѕРІ.
- Executive summary РЅРµ С„РѕСЂРјРёСЂСѓРµС‚ РІС‹РІРѕРґС‹ Р±РµР· СЂР°СЃСЃС‡РёС‚Р°РЅРЅС‹С… РёСЃС‚РѕС‡РЅРёРєРѕРІ.
- РџСЂРё РѕС‚СЃСѓС‚СЃС‚РІРёРё `cutoff_price` Р°РЅР°Р»РёР· РґРёСЃРєРѕРЅС‚Р° Рє РЅРѕРјРёРЅР°Р»Сѓ РѕРіСЂР°РЅРёС‡РµРЅ.
- Р“СЂСѓРїРїС‹ boxplot СЃ `n=1` РЅРµ РёРЅС‚РµСЂРїСЂРµС‚РёСЂСѓСЋС‚СЃСЏ РєР°Рє СЂР°СЃРїСЂРµРґРµР»РµРЅРёРµ.
- РћРєРѕР»Рѕ-РЅСѓР»РµРІС‹Рµ РґРѕС…РѕРґРЅРѕСЃС‚Рё РћР¤Р—-РџРљ С‚СЂРµР±СѓСЋС‚ РїСЂРѕРІРµСЂРєРё РєР°С‡РµСЃС‚РІР° РґР°РЅРЅС‹С….
- РќРµРїРѕР»РЅС‹Рµ РїРµСЂРёРѕРґС‹ РґРѕР»Р¶РЅС‹ РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°С‚СЊСЃСЏ РІ РѕС‚С‡РµС‚Р°С….
- Outputs СЂРµР¶РёРјРѕРІ `cumulative` Рё `point` РЅРµ РґРѕР»Р¶РЅС‹ СЃРјРµС€РёРІР°С‚СЊСЃСЏ.
- `data/raw/` РЅРµ РёР·РјРµРЅСЏРµС‚СЃСЏ pipeline-СЃРєСЂРёРїС‚Р°РјРё.

## Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ

РљР»СЋС‡РµРІС‹Рµ РґРѕРєСѓРјРµРЅС‚С‹:

- `docs/00_project/project_inventory.md`;
- `docs/02_data_pipeline/data_audit.md`;
- `docs/02_data_pipeline/data_cleaning_report.md`;
- `docs/02_data_pipeline/feature_engineering.md`;
- `docs/01_methodology/period_selection_report.md`;
- `docs/01_methodology/kpi_map.md`;
- `docs/00_project/analytical_architecture.md`;
- `docs/04_visualization/visualization_strategy.md`;
- `docs/04_visualization/chart_build_limitations.md`;
- `docs/03_analytics/analytical_tables_report.md`;
- `docs/03_analytics/analytical_tables_limitations.md`;
- `docs/03_analytics/monthly_analytics_report.md`;
- `docs/04_visualization/monthly_visualization_strategy.md`;
- `docs/00_project/dashboard_architecture.md`;
- `docs/05_dashboard/dashboard_exports_report.md`;
- `docs/05_dashboard/dashboard_exports_limitations.md`;
- `docs/03_analytics/executive_summary_report.md`;
- `docs/06_quality/run_manifest_report.md`;
- `docs/06_quality/quality_gate_report.md`;
- `docs/06_quality/visual_regression_report.md`;
- `docs/06_quality/anomaly_tests_report.md`;
- `docs/05_dashboard/dashboard_semantic_model_v2.md`;
- `docs/03_analytics/revenue_analytics_report.md`;
- `docs/01_methodology/revenue_kpi_map.md`;
- `docs/02_data_pipeline/schema_validation_report.md`;
- `docs/00_project/self_review.md`;
- `docs/00_project/final_project_summary.md`;

## РЎС‚СЂСѓРєС‚СѓСЂР° РґРѕРєСѓРјРµРЅС‚Р°С†РёРё, СЃРєСЂРёРїС‚РѕРІ Рё РіСЂР°С„РёРєРѕРІ

Р”РѕРєСѓРјРµРЅС‚Р°С†РёСЏ РѕСЂРіР°РЅРёР·РѕРІР°РЅР° С‚РµРјР°С‚РёС‡РµСЃРєРё. Р“Р»Р°РІРЅР°СЏ РєР°СЂС‚Р° РЅР°С…РѕРґРёС‚СЃСЏ РІ [`docs/index.md`](docs/index.md).

- [`docs/00_project/`](docs/00_project/) вЂ” РїСЂРѕРµРєС‚РЅР°СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ, Р°СЂС…РёС‚РµРєС‚СѓСЂР°, summary, РїР»Р°РЅС‹ СЃС‚СЂСѓРєС‚СѓСЂС‹ scripts.
- [`docs/01_methodology/`](docs/01_methodology/) вЂ” РјРµС‚РѕРґРѕР»РѕРіРёСЏ, KPI, РїСЂР°РІРёР»Р° РїРµСЂРёРѕРґРѕРІ, revenue KPI.
- [`docs/02_data_pipeline/`](docs/02_data_pipeline/) вЂ” Р°СѓРґРёС‚, РѕС‡РёСЃС‚РєР°, feature engineering, schema validation.
- [`docs/03_analytics/`](docs/03_analytics/) вЂ” Р°РЅР°Р»РёС‚РёС‡РµСЃРєРёРµ С‚Р°Р±Р»РёС†С‹, monthly analytics, revenue analytics, executive summary.
- [`docs/04_visualization/`](docs/04_visualization/) вЂ” СЃС‚СЂР°С‚РµРіРёСЏ РІРёР·СѓР°Р»РёР·Р°С†РёР№, РѕРіСЂР°РЅРёС‡РµРЅРёСЏ РіСЂР°С„РёРєРѕРІ, palette policy.
- [`docs/05_dashboard/`](docs/05_dashboard/) вЂ” dashboard exports Рё semantic model.
- [`docs/06_quality/`](docs/06_quality/) вЂ” quality gate, visual regression, anomaly tests, manual checks, run manifest.
- [`docs/90_archive/`](docs/90_archive/) вЂ” Р°СЂС…РёРІ РїСЂРѕРјРµР¶СѓС‚РѕС‡РЅС‹С… Рё СѓСЃС‚Р°СЂРµРІС€РёС… РґРѕРєСѓРјРµРЅС‚РѕРІ.

РЎРєСЂРёРїС‚С‹ РїРѕРєР° С„РёР·РёС‡РµСЃРєРё РѕСЃС‚Р°СЋС‚СЃСЏ РІ РєРѕСЂРЅРµ `scripts/`, РЅРѕ Р»РѕРіРёС‡РµСЃРєРё РєР»Р°СЃСЃРёС„РёС†РёСЂРѕРІР°РЅС‹. РЎРј.:

- [`scripts/README.md`](scripts/README.md);
- [`docs/00_project/scripts_structure_plan.md`](docs/00_project/scripts_structure_plan.md);
- [`docs/00_project/scripts_migration_plan.md`](docs/00_project/scripts_migration_plan.md).

HTML-РіСЂР°С„РёРєРё РѕСЂРіР°РЅРёР·РѕРІР°РЅС‹ РїРѕ С‚РµРјР°С‚РёС‡РµСЃРєРёРј РїРѕРґРїР°РїРєР°Рј. РљР°СЂС‚Р° РіСЂР°С„РёРєРѕРІ РЅР°С…РѕРґРёС‚СЃСЏ РІ [`outputs/charts/index.md`](outputs/charts/index.md).

- [`outputs/charts/monthly/`](outputs/charts/monthly/) вЂ” РїРѕРјРµСЃСЏС‡РЅС‹Рµ РіСЂР°С„РёРєРё.
- [`outputs/charts/monthly/heatmap/`](outputs/charts/monthly/heatmap/) вЂ” heatmap СЂР°Р·РјРµС‰РµРЅРёСЏ Рё РІС‹СЂСѓС‡РєРё, РІРєР»СЋС‡Р°СЏ `monthly_heatmap_placement_*` Рё `monthly_heatmap_revenue_*`.
- [`outputs/charts/risk/`](outputs/charts/risk/) вЂ” risk quadrant Рё РµРіРѕ РІРµСЂСЃРёРё.
- [`outputs/charts/scatter/`](outputs/charts/scatter/) вЂ” scatter-РіСЂР°С„РёРєРё.
- [`outputs/charts/scatter/yield_discount/`](outputs/charts/scatter/yield_discount/) вЂ” СЃРµРјРµР№СЃС‚РІРѕ `yield_vs_discount`: main, facet Рё outliers.
- [`outputs/charts/scatter/format_terms/`](outputs/charts/scatter/format_terms/) вЂ” РіСЂР°С„РёРєРё СѓСЃР»РѕРІРёР№ СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ С„РѕСЂРјР°С‚Р°Рј: `format_terms_scatter_*` Рё `format_terms_aggregate_scatter_*`.
- [`outputs/charts/yield/`](outputs/charts/yield/) вЂ” yield boxplots.
- [`outputs/charts/sankey/`](outputs/charts/sankey/) вЂ” Sankey-РіСЂР°С„РёРєРё.
- [`outputs/charts/structure/`](outputs/charts/structure/) вЂ” СЃС‚СЂСѓРєС‚СѓСЂРЅС‹Рµ РіСЂР°С„РёРєРё.
- [`outputs/charts/structure/format/`](outputs/charts/structure/format/) вЂ” СЃС‚СЂСѓРєС‚СѓСЂР° Рё СѓСЃР»РѕРІРёСЏ РїРѕ С„РѕСЂРјР°С‚Р°Рј: `format_structure_*`, `format_discount_*`, `format_terms_comparison_*`, `format_terms_delta_by_format_*`.
- [`outputs/charts/revenue/`](outputs/charts/revenue/) вЂ” revenue analytics.
- [`outputs/charts/revenue/gap/`](outputs/charts/revenue/gap/) вЂ” РіСЂР°С„РёРєРё СЂР°Р·РЅРёС†С‹ РЅРѕРјРёРЅР°Р»-РІС‹СЂСѓС‡РєР°, РІРєР»СЋС‡Р°СЏ `format_nominal_revenue_gap_*`.

### Р“СЂР°С„РёРє `yield_vs_discount`

РЎРµРјРµР№СЃС‚РІРѕ `yield_vs_discount` РЅР°С…РѕРґРёС‚СЃСЏ РІ `outputs/charts/scatter/yield_discount/` Рё РїРѕРєР°Р·С‹РІР°РµС‚ СЃРІСЏР·СЊ РґРёСЃРєРѕРЅС‚Р° Рє РЅРѕРјРёРЅР°Р»Сѓ Рё РґРѕС…РѕРґРЅРѕСЃС‚Рё. Р’ РѕСЃРЅРѕРІРЅС‹С… РІРµСЂСЃРёСЏС… С†РІРµС‚ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ РіРѕРґСѓ (`report_year`), СЂР°Р·РјРµСЂ С‚РѕС‡РєРё СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ РѕР±СЉРµРјСѓ СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ, Р° СЃСЂРѕРєРѕРІР°СЏ РєР°С‚РµРіРѕСЂРёСЏ РґРѕСЃС‚СѓРїРЅР° РІ hover. CSV-РѕСЃРЅРѕРІС‹ СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РІ `outputs/exports/chart_data/scatter/`.

Р’ СЃРµРјРµР№СЃС‚РІРµ СЃРѕР·РґР°СЋС‚СЃСЏ С‚СЂРё РІРµСЂСЃРёРё:

- `yield_vs_discount_<...>.html` вЂ” РѕСЃРЅРѕРІРЅРѕР№ РіСЂР°С„РёРє РїРѕ РІСЃРµРј РїСЂРёРіРѕРґРЅС‹Рј РЅР°Р±Р»СЋРґРµРЅРёСЏРј.
- `yield_vs_discount_facet_<...>.html` вЂ” СЃСЂР°РІРЅРµРЅРёРµ РїРѕ РїРµСЂРёРѕРґР°Рј/РіРѕРґР°Рј РІ РѕС‚РґРµР»СЊРЅС‹С… РїР°РЅРµР»СЏС….
- `yield_vs_discount_outliers_<...>.html` вЂ” С„РѕРєСѓСЃ РЅР° СЌРєСЃС‚СЂРµРјР°Р»СЊРЅС‹С… С‚РѕС‡РєР°С… РїРѕ РґРёСЃРєРѕРЅС‚Сѓ, РґРѕС…РѕРґРЅРѕСЃС‚Рё РёР»Рё РѕР±СЉРµРјСѓ СЂР°Р·РјРµС‰РµРЅРёСЏ.

РџРѕРґРїРёСЃРё С‚РѕС‡РµРє СѓРїСЂР°РІР»СЏСЋС‚СЃСЏ РїРѕР»РµРј `label_visible` РІ CSV export. Р•СЃР»Рё `label_visible=True`, РїРѕРґРїРёСЃСЊ РІС‹РІРѕРґРёС‚СЃСЏ РЅР° РіСЂР°С„РёРє. Р•СЃР»Рё `False`, РЅР°Р±Р»СЋРґРµРЅРёРµ РѕСЃС‚Р°РµС‚СЃСЏ РІ hover Рё CSV, РЅРѕ РїРѕРґРїРёСЃСЊ СЃРєСЂС‹РІР°РµС‚СЃСЏ РёР·-Р·Р° Р»РёРјРёС‚Р°, РїР»РѕС‚РЅРѕСЃС‚Рё РёР»Рё РѕС‚СЃСѓС‚СЃС‚РІРёСЏ Р°РЅР°Р»РёС‚РёС‡РµСЃРєРѕР№ РїСЂРёС‡РёРЅС‹. Р”Р»СЏ main-РіСЂР°С„РёРєР° Р»РёРјРёС‚ вЂ” 25 РїРѕРґРїРёСЃРµР№, РґР»СЏ outliers вЂ” 30, РґР»СЏ facet вЂ” 15 РІСЃРµРіРѕ Рё РЅРµ Р±РѕР»РµРµ 3 РЅР° РїР°РЅРµР»СЊ.

РњРµРґРёР°РЅРЅС‹Рµ Р»РёРЅРёРё РёРјРµСЋС‚ СЂР°Р·РЅСѓСЋ РјРµС‚РѕРґРѕР»РѕРіРёСЋ. Р’ main/outliers РѕРЅРё СЃС‡РёС‚Р°СЋС‚СЃСЏ РїРѕ РІСЃРµР№ РІС‹Р±РѕСЂРєРµ РіСЂР°С„РёРєР° (`median_scope=global`) Рё РїРѕРґРїРёСЃС‹РІР°СЋС‚СЃСЏ РєР°Рє `РјРµРґ. РґРёСЃРєРѕРЅС‚` Рё `РјРµРґ. РґРѕС…РѕРґРЅРѕСЃС‚СЊ`. Р’ facet-РіСЂР°С„РёРєРµ РјРµРґРёР°РЅС‹ СЃС‡РёС‚Р°СЋС‚СЃСЏ РІРЅСѓС‚СЂРё РєР°Р¶РґРѕР№ РїР°РЅРµР»Рё (`median_scope=period`), Р° РїРѕСЏСЃРЅРµРЅРёРµ РІС‹РЅРµСЃРµРЅРѕ РІ subtitle: РїСѓРЅРєС‚РёСЂРЅС‹Рµ Р»РёРЅРёРё вЂ” РјРµРґРёР°РЅС‹ РїРµСЂРёРѕРґР°.

Р Р°Р·РјРµСЂ С‚РѕС‡РєРё РѕР·РЅР°С‡Р°РµС‚ РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ. РќР° РіСЂР°С„РёРєРµ РµСЃС‚СЊ РїРѕСЏСЃРЅРµРЅРёРµ СЂР°Р·РјРµСЂР° Рё РѕСЂРёРµРЅС‚РёСЂС‹ `50 / 250 / 500 РјР»СЂРґ СЂСѓР±.`, С‚РѕС‡РЅРѕРµ Р·РЅР°С‡РµРЅРёРµ РґРѕСЃС‚СѓРїРЅРѕ РІ hover. Р•СЃР»Рё РїРµСЂРёРѕРґ РЅРµРїРѕР»РЅС‹Р№ РїРѕСЃР»Рµ С„РёР»СЊС‚СЂР°С†РёРё РІР°Р»РёРґРЅС‹С… СЃС‚СЂРѕРє, CSV СЃРѕРґРµСЂР¶РёС‚ `is_incomplete_period=True` Рё С‡РµР»РѕРІРµРєРѕС‡РёС‚Р°РµРјСѓСЋ РїСЂРёС‡РёРЅСѓ, РЅР°РїСЂРёРјРµСЂ `РґРѕСЃС‚СѓРїРЅС‹ РґР°РЅРЅС‹Рµ С‚РѕР»СЊРєРѕ Р·Р° СЏРЅРІвЂ“С„РµРІ`.

РРЅС‚РµСЂРїСЂРµС‚Р°С†РёСЏ РєРІР°РґСЂР°РЅС‚РѕРІ:

- РІС‹СЃРѕРєРёР№ РґРёСЃРєРѕРЅС‚ / РІС‹СЃРѕРєР°СЏ РґРѕС…РѕРґРЅРѕСЃС‚СЊ вЂ” Р·РѕРЅР° РїРѕРІС‹С€РµРЅРЅРѕР№ СЃС‚РѕРёРјРѕСЃС‚Рё РїСЂРёРІР»РµС‡РµРЅРёСЏ Рё С†РµРЅРѕРІРѕРіРѕ РґРёСЃРєРѕРЅС‚Р°;
- РІС‹СЃРѕРєРёР№ РґРёСЃРєРѕРЅС‚ / РЅРёР·РєР°СЏ РґРѕС…РѕРґРЅРѕСЃС‚СЊ вЂ” С†РµРЅРѕРІРѕР№ РґРёСЃРєРѕРЅС‚ РїСЂРё СѓРјРµСЂРµРЅРЅРѕР№ РґРѕС…РѕРґРЅРѕСЃС‚Рё;
- РЅРёР·РєРёР№ РґРёСЃРєРѕРЅС‚ / РІС‹СЃРѕРєР°СЏ РґРѕС…РѕРґРЅРѕСЃС‚СЊ вЂ” РІС‹СЃРѕРєР°СЏ РґРѕС…РѕРґРЅРѕСЃС‚СЊ Р±РµР· РІС‹СЂР°Р¶РµРЅРЅРѕРіРѕ С†РµРЅРѕРІРѕРіРѕ РґРёСЃРєРѕРЅС‚Р°;
- РЅРёР·РєРёР№ РґРёСЃРєРѕРЅС‚ / РЅРёР·РєР°СЏ РґРѕС…РѕРґРЅРѕСЃС‚СЊ вЂ” РѕС‚РЅРѕСЃРёС‚РµР»СЊРЅРѕ СЃРїРѕРєРѕР№РЅР°СЏ Р·РѕРЅР°.

Р•СЃР»Рё СЂР°Р·РјРµСЂ С‚РѕС‡РєРё РїР»РѕС…Рѕ С‡РёС‚Р°РµС‚СЃСЏ РёР»Рё РїРµСЂРµРєСЂС‹РІР°РµС‚ РЅР°Р±Р»СЋРґРµРЅРёСЏ, РіСЂР°С„РёРє РјРѕР¶РµС‚ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ fixed-size fallback. Р’ СЌС‚РѕРј СЃР»СѓС‡Р°Рµ СЂР°Р·РјРµСЂ РјР°СЂРєРµСЂР° РЅРµ РёРЅС‚РµСЂРїСЂРµС‚РёСЂСѓРµС‚СЃСЏ РєР°Рє РѕР±СЉРµРј, РЅРѕ РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ РѕСЃС‚Р°РµС‚СЃСЏ РІ hover Рё CSV.

### РџСЂР°РІРёР»Р° С‡РёС‚Р°РµРјРѕСЃС‚Рё РіСЂР°С„РёРєРѕРІ

- Monthly bar charts РїРѕРєР°Р·С‹РІР°СЋС‚ РїРѕРґРїРёСЃРё С‚РѕР»СЊРєРѕ РґР»СЏ С‡РёС‚Р°РµРјС‹С… СЃС‚РѕР»Р±С†РѕРІ; РјР°Р»С‹Рµ Р·РЅР°С‡РµРЅРёСЏ РѕСЃС‚Р°СЋС‚СЃСЏ РІ hover.
- Monthly line charts РїРѕРґРїРёСЃС‹РІР°СЋС‚ РєР»СЋС‡РµРІС‹Рµ С‚РѕС‡РєРё: РїРѕСЃР»РµРґРЅРёРµ Р·РЅР°С‡РµРЅРёСЏ, РјР°РєСЃРёРјСѓРјС‹, РѕС‚С‡РµС‚РЅС‹Р№ РіРѕРґ Рё СЂРµР·РєРёРµ РёР·РјРµРЅРµРЅРёСЏ.
- Facet-РіСЂР°С„РёРєРё РґРѕР»Р¶РЅС‹ РёРјРµС‚СЊ РѕРґРёРЅ РѕР±С‰РёР№ Y-axis title; РїРѕРІС‚РѕСЂРµРЅРёРµ РїРѕРґРїРёСЃРё Y РІ РєР°Р¶РґРѕР№ РїР°РЅРµР»Рё СЃС‡РёС‚Р°РµС‚СЃСЏ РґРµС„РµРєС‚РѕРј.
- Scatter-РіСЂР°С„РёРєРё СЃ bubble-size РѕР±СЏР·Р°РЅС‹ РѕР±СЉСЏСЃРЅСЏС‚СЊ, С‡С‚Рѕ РѕР·РЅР°С‡Р°РµС‚ СЂР°Р·РјРµСЂ С‚РѕС‡РєРё, Р»РёР±Рѕ СЏРІРЅРѕ РёСЃРїРѕР»СЊР·РѕРІР°С‚СЊ fixed-size fallback.
### РњР°СЂС€СЂСѓС‚РёР·Р°С†РёСЏ РЅРѕРІС‹С… РіСЂР°С„РёРєРѕРІ СѓСЃР»РѕРІРёР№ Рё РІС‹СЂСѓС‡РєРё

РќРѕРІС‹Рµ HTML-РіСЂР°С„РёРєРё СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ СЃСЂР°Р·Сѓ РІ С‚РµРјР°С‚РёС‡РµСЃРєРёРµ РїРѕРґРїР°РїРєРё `outputs/charts/`; РїСЂРё РјРёРіСЂР°С†РёРё СЃС‚Р°СЂС‹С… С„Р°Р№Р»РѕРІ С‚Рµ Р¶Рµ РїСЂР°РІРёР»Р° РїСЂРёРјРµРЅСЏРµС‚ `scripts/maintenance/reorganize_charts.py`.

- `format_discount_*` -> `outputs/charts/structure/format/`.
- `format_terms_comparison_*` -> `outputs/charts/structure/format/`.
- `format_terms_delta_by_format_*` -> `outputs/charts/structure/format/`.
- `format_nominal_revenue_gap_*` -> `outputs/charts/revenue/gap/`.
- `monthly_heatmap_revenue_*` -> `outputs/charts/monthly/heatmap/`.
- `format_terms_scatter_*` Рё `format_terms_aggregate_scatter_*` -> `outputs/charts/scatter/format_terms/`.
## Р“СЂР°С„РёРєРё РїРѕ С„РѕСЂРјР°С‚Р°Рј, РґРёСЃРєРѕРЅС‚Сѓ Рё РІС‹СЂСѓС‡РєРµ

Р’ Р°РєС‚СѓР°Р»СЊРЅРѕР№ СЃС‚СЂСѓРєС‚СѓСЂРµ РіСЂР°С„РёРєРё РїРѕ С„РѕСЂРјР°С‚Р°Рј СЂР°Р·РјРµС‰РµРЅРёСЏ РЅР°С…РѕРґСЏС‚СЃСЏ РІ С‚РµРјР°С‚РёС‡РµСЃРєРёС… РїР°РїРєР°С… `outputs/charts/structure/format/`, `outputs/charts/revenue/gap/`, `outputs/charts/monthly/heatmap/` Рё `outputs/charts/scatter/format_terms/`.

РљР»СЋС‡РµРІС‹Рµ РіСЂР°С„РёРєРё:

- `format_structure_<...>.html` - stacked bar СЃС‚СЂСѓРєС‚СѓСЂС‹ СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ С„РѕСЂРјР°С‚Р°Рј `РђСѓРєС†РёРѕРЅ` / `Р”Р РџРђ`. Р’С‹СЃРѕС‚Р° СЃРµРіРјРµРЅС‚Р° СЂР°РІРЅР° РѕР±СЉРµРјСѓ СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ РІ РјР»СЂРґ СЂСѓР±Р»РµР№. РќР°Рґ СЃС‚РѕР»Р±С†Р°РјРё СЃ РґРІСѓРјСЏ Рё Р±РѕР»РµРµ СЃРµРіРјРµРЅС‚Р°РјРё РІС‹РІРѕРґРёС‚СЃСЏ РёС‚РѕРіРѕРІР°СЏ СЃСѓРјРјР°, Р° РїРѕРґРїРёСЃРё СЃРµРіРјРµРЅС‚РѕРІ СѓРїСЂР°РІР»СЏСЋС‚СЃСЏ РїРѕР»РµРј `label_visible`.
- `format_discount_<...>.html` - СЃСЂРµРґРЅРµРІР·РІРµС€РµРЅРЅС‹Р№ РґРёСЃРєРѕРЅС‚ Рє РЅРѕРјРёРЅР°Р»Сѓ РїРѕ С„РѕСЂРјР°С‚Р°Рј. РћСЃСЊ Y: `РЎСЂРµРґРЅРµРІР·РІРµС€РµРЅРЅС‹Р№ РґРёСЃРєРѕРЅС‚ Рє РЅРѕРјРёРЅР°Р»Сѓ, Рї.Рї.`. РќРѕРјРёРЅР°Р»СЊРЅС‹Р№ РѕР±СЉРµРј, РІС‹СЂСѓС‡РєР°, min/max РґРёСЃРєРѕРЅС‚ Рё РєР°С‡РµСЃС‚РІРѕ РґР°РЅРЅС‹С… РґРѕСЃС‚СѓРїРЅС‹ РІ hover Рё CSV.
- `format_nominal_revenue_gap_<...>.html` - РґРµРЅРµР¶РЅР°СЏ СЂР°Р·РЅРёС†Р° РјРµР¶РґСѓ РЅРѕРјРёРЅР°Р»СЊРЅС‹Рј СЂР°Р·РјРµС‰РµРЅРёРµРј Рё РІС‹СЂСѓС‡РєРѕР№ РїРѕ С„РѕСЂРјР°С‚Р°Рј: `nominal_revenue_gap_bln = placement_volume_bln - revenue_volume_bln`.
- `monthly_heatmap_revenue_<...>.html` - heatmap РїРѕРјРµСЃСЏС‡РЅРѕР№ РІС‹СЂСѓС‡РєРё СЃ РєРѕР»РѕРЅРєРѕР№ `РС‚РѕРіРѕ`. РС‚РѕРіРѕРІР°СЏ РєРѕР»РѕРЅРєР° СЃРїСЂР°РІРѕС‡РЅР°СЏ Рё РЅРµ СѓС‡Р°СЃС‚РІСѓРµС‚ РІ РѕСЃРЅРѕРІРЅРѕР№ С†РІРµС‚РѕРІРѕР№ С€РєР°Р»Рµ.
- `format_terms_comparison_<...>.html` - small multiples РґР»СЏ СЃСЂР°РІРЅРµРЅРёСЏ С„РѕСЂРјР°С‚РѕРІ РїРѕ РґРѕС…РѕРґРЅРѕСЃС‚Рё, РґРёСЃРєРѕРЅС‚Сѓ, РІС‹СЂСѓС‡РєРµ / РЅРѕРјРёРЅР°Р»Сѓ Рё СЂР°Р·РЅРёС†Рµ РЅРѕРјРёРЅР°Р» РјРёРЅСѓСЃ РІС‹СЂСѓС‡РєР°. `n` РѕР·РЅР°С‡Р°РµС‚ РєРѕР»РёС‡РµСЃС‚РІРѕ СЂР°Р·РјРµС‰РµРЅРёР№ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓСЋС‰РµРіРѕ С„РѕСЂРјР°С‚Р° РІ РїРµСЂРёРѕРґРµ.
- `format_terms_scatter_<...>.html` - scatter РѕС‚РґРµР»СЊРЅС‹С… СЂР°Р·РјРµС‰РµРЅРёР№: С†РІРµС‚ = С„РѕСЂРјР°С‚, С„РѕСЂРјР° = РІРёРґ РћР¤Р—, СЂР°Р·РјРµСЂ = РѕР±СЉРµРј СЂР°Р·РјРµС‰РµРЅРёСЏ РїРѕ РЅРѕРјРёРЅР°Р»Сѓ.

РћРіСЂР°РЅРёС‡РµРЅРёСЏ:

- РµСЃР»Рё РІС‹СЂСѓС‡РєР° РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚, РїСЂРѕРµРєС‚ РЅРµ РїРѕРґСЃС‚Р°РІР»СЏРµС‚ СЃРёРЅС‚РµС‚РёС‡РµСЃРєРёРµ Р·РЅР°С‡РµРЅРёСЏ РёР· РЅРѕРјРёРЅР°Р»Р° РёР»Рё СЃРїСЂРѕСЃР°;
- РµСЃР»Рё РґРёСЃРєРѕРЅС‚ РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ Рё РµРіРѕ РЅРµР»СЊР·СЏ РЅР°РґРµР¶РЅРѕ РїРѕР»СѓС‡РёС‚СЊ РёР· С†РµРЅС‹ РѕС‚СЃРµС‡РµРЅРёСЏ, СЃС‚СЂРѕРєР° РёСЃРєР»СЋС‡Р°РµС‚СЃСЏ РёР· СЂР°СЃС‡РµС‚Р° РґРёСЃРєРѕРЅС‚Р° РёР»Рё РїРѕРјРµС‡Р°РµС‚СЃСЏ С‡РµСЂРµР· `data_quality_flag`;
- РїРѕРєР°Р·Р°С‚РµР»Рё РїРѕ Р”Р РџРђ РїСЂРё РјР°Р»РѕРј `n` РЅСѓР¶РЅРѕ РёРЅС‚РµСЂРїСЂРµС‚РёСЂРѕРІР°С‚СЊ РѕСЃС‚РѕСЂРѕР¶РЅРѕ.

## Data raw dataset and Git policy

`data/raw/` contains the baseline source dataset for the project. These raw Excel files are intentionally included in the repository because the current files are small and are required to reproduce the pipeline from source data.

For the first Git commit, `data/raw/` is committed as the source dataset. Generated outputs are not committed to normal Git history and are recreated by the pipeline or preserved separately as release artifacts.

Generated outputs are not part of the normal Git history:

- `outputs/charts/`;
- `outputs/exports/`;
- `outputs/reports/`;
- `outputs/dashboards/`.

For a specific reporting run, generated outputs should be preserved as a release bundle or external artifact together with the run manifest and quality reports.

## Version Control

- Repository: GitHub / `OFZ_ANALYTICS`
- Remote: `https://github.com/VinogradovPV/OFZ_ANALYTICS.git`
- Default branch: `main`
- Visibility: private
- Initial commit: `4fa6d61fa67281c20d5d7a878cd2191e953507bc`
- Initial commit message: `Initial source dataset and OFZ analytics pipeline`

Git artifact strategy:

- the first commit includes source code, configuration, documentation, scripts, prompts, data contracts and `data/raw`;
- generated outputs are excluded from ordinary Git history;
- `outputs/charts/`, `outputs/exports/`, `outputs/reports/` and `outputs/dashboards/` are regenerated by the pipeline;
- release outputs should be stored as a release bundle, external artifact or GitHub Release asset when that release process is configured;
- the empty outputs folder skeleton is kept in Git via `.gitkeep` and lightweight navigation files such as `outputs/charts/index.md`.

Data strategy:

- `data/raw` is committed as the project source dataset;
- raw file hashes are tracked by raw data registry and/or run manifest;
- generated data such as `data/processed` is not committed and is recreated by pipeline stages.
## Production operations

Production-Р·Р°РїСѓСЃРє РѕРїРёСЃР°РЅ РІ:

- `docs/07_operations/production_runbook.md` вЂ” РїРѕС€Р°РіРѕРІС‹Р№ runbook РґР»СЏ clone, `.venv`, CLI, pipeline, cleanup outputs, QA, release bundle Рё Git workflow.
- `docs/07_operations/release_checklist.md` вЂ” РєРѕРЅС‚СЂРѕР»СЊРЅС‹Р№ checklist РїРµСЂРµРґ production release.
- `docs/07_operations/windows_setup.md` — reproducible Windows setup workflow for a new machine.
- `docs/07_operations/docker_plan.md` — optional Docker plan; Windows-first remains the primary supported path.

Windows setup dry-run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/setup/setup_windows.ps1 -DryRun
```

РђРєС‚СѓР°Р»СЊРЅС‹Рµ CLI entry points:

```powershell
ofz-run --help
ofz-interactive --help
ofz-quality --help
ofz-clean-outputs --help
ofz-schema --help
```

Р•СЃР»Рё `.venv` РЅРµ Р°РєС‚РёРІРёСЂРѕРІР°РЅР°, РёСЃРїРѕР»СЊР·СѓР№С‚Рµ СЏРІРЅС‹Рµ executables РёР· `.venv\Scripts`, РЅР°РїСЂРёРјРµСЂ `.\.venv\Scripts\ofz-quality.exe --help`.

Generated outputs РЅРµ РІС…РѕРґСЏС‚ РІ РѕР±С‹С‡РЅСѓСЋ Git-РёСЃС‚РѕСЂРёСЋ. Р”Р»СЏ РєРѕРЅРєСЂРµС‚РЅРѕРіРѕ РѕС‚С‡РµС‚РЅРѕРіРѕ Р·Р°РїСѓСЃРєР° РѕРЅРё СЃРѕС…СЂР°РЅСЏСЋС‚СЃСЏ РєР°Рє release bundle / external artifact.

## CI / GitHub Actions

GitHub Actions workflow `.github/workflows/quality.yml` запускает `quality-fast` на `push`/`pull_request` в `main` и вручную через `workflow_dispatch`.

CI выполняет `pip install`, editable install, `pip check`, `compileall`, `ofz-schema` и `ofz-quality --fast`. Manual `quality-full` job доступен только через `workflow_dispatch` и зависит от `quality-fast`, чтобы fast/full не выполнялись параллельно в одном workflow.

QA reports сохраняются как GitHub Actions artifacts. Generated outputs и `releases/` не коммитятся. Подробный контракт: [`docs/07_operations/ci_workflow.md`](docs/07_operations/ci_workflow.md).

## Ограничения

Ограничения production-запуска, визуализаций и release artifacts описаны в `docs/07_operations/release_checklist.md`, `docs/07_operations/production_runbook.md` и `docs/04_visualization/chart_build_limitations.md`.

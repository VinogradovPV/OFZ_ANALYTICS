# P2 modernization progress report

Р”Р°С‚Р° СЃРѕР·РґР°РЅРёСЏ: 2026-06-09.

Р­С‚РѕС‚ РґРѕРєСѓРјРµРЅС‚ СЏРІР»СЏРµС‚СЃСЏ СЃРІРѕРґРЅС‹Рј РёРЅС„РѕСЂРјР°С†РёРѕРЅРЅС‹Рј РѕС‚С‡РµС‚РѕРј РїРѕ СЌС‚Р°РїР°Рј P2 modernization. РџРѕСЃР»Рµ РєР°Р¶РґРѕРіРѕ P2-СЌС‚Р°РїР° СЃСЋРґР° РґРѕР±Р°РІР»СЏРµС‚СЃСЏ РєСЂР°С‚РєРёР№ РёС‚РѕРі: РІС‹РїРѕР»РЅРµРЅРЅС‹Р№ СЌС‚Р°Рї, РёР·РјРµРЅРµРЅРёСЏ, РїСЂРѕРІРµСЂРєРё, warnings, commits, push, Git status Рё СЃР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї.

## P2.0 - Starting checkpoint

Р”Р°С‚Р°: 2026-06-09.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.0 Starting checkpoint`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

РЎРѕР·РґР°РЅ baseline РїРµСЂРµРґ РЅР°С‡Р°Р»РѕРј P2:

- РїСЂРѕР°РЅР°Р»РёР·РёСЂРѕРІР°РЅ `prompts/ofz_p2_modernization_system_prompt_v3.md`;
- РїРѕРґС‚РІРµСЂР¶РґРµРЅ production-ready candidate baseline;
- Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅ P2 execution protocol;
- Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅ СѓС‚РѕС‡РЅРµРЅРЅС‹Р№ РїРѕСЂСЏРґРѕРє P2.0-P2.15;
- СЃРѕР·РґР°РЅ РґРѕРєСѓРјРµРЅС‚ `docs/00_project/p2_starting_checkpoint.md`;
- СЃРѕР·РґР°РЅ СЌС‚РѕС‚ СЃРІРѕРґРЅС‹Р№ progress report.

### 3. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РїСЂРѕС€Р»Рё

- `git status --short --branch`: branch `main`, remote synced with `origin/main` before P2 docs changes.
- `git branch --show-current`: `main`.
- `git remote -v`: `origin https://github.com/VinogradovPV/OFZ_ANALYTICS.git`.
- `git log --oneline -5`: latest history reviewed.
- `git ls-files data/raw`: 8 raw Excel files tracked.
- `git ls-files outputs`: only skeleton/index files tracked.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --full --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- CLI help through `.venv\Scripts\ofz-*.exe`: OK.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё СѓРїР°Р»Рё

РџР°РґРµРЅРёР№ РїСЂРѕРІРµСЂРѕРє РЅРµ Р±С‹Р»Рѕ.

### 5. РљР°РєРёРµ warnings documented

- `anomaly_tests` СЃРѕРґРµСЂР¶РёС‚ РґРѕРєСѓРјРµРЅС‚РёСЂРѕРІР°РЅРЅС‹Рµ data warnings.
- `visual_regression` РїРѕРєР° РёСЃРїРѕР»СЊР·СѓРµС‚ fallback static HTML / Plotly JSON inspection.
- `prompts/ofz_p2_modernization_system_prompt_v3.md` РІРєР»СЋС‡Р°РµС‚СЃСЏ РєР°Рє Р°РєС‚СѓР°Р»СЊРЅС‹Р№ source prompt asset; СЃС‚Р°СЂР°СЏ РІРµСЂСЃРёСЏ prompt СѓРґР°Р»СЏРµС‚СЃСЏ РёР· Р°РєС‚РёРІРЅРѕРіРѕ РЅР°Р±РѕСЂР°.

### 6. РљР°РєРёРµ commits СЃРѕР·РґР°РЅС‹

Commit message: `Record P2 starting checkpoint`.

### 7. Р‘С‹Р» Р»Рё push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РІ `origin/main` РїРѕСЃР»Рµ commit P2.0.

### 8. РўРµРєСѓС‰РёР№ git status

РќР° РјРѕРјРµРЅС‚ РїРѕРґРіРѕС‚РѕРІРєРё P2.0 РѕР¶РёРґР°РµРјС‹Рµ РёР·РјРµРЅРµРЅРёСЏ:

- РЅРѕРІС‹Р№ P2 checkpoint doc;
- РЅРѕРІС‹Р№ P2 progress report;
- QA reports, РѕР±РЅРѕРІР»РµРЅРЅС‹Рµ baseline quality gate;
- untracked P2 system prompt, РєРѕС‚РѕСЂС‹Р№ РІРєР»СЋС‡Р°РµС‚СЃСЏ РІ commit РєР°Рє source prompt asset.

### 9. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РїСЂРѕРІРµСЂРµРЅРѕ РїРµСЂРµРґ commit;
- `data/raw` tracked: РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ;
- CLI entry points still work: РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ.

### 10. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.1 Release bundle automation`.

## P2.1 - Release bundle automation

Р”Р°С‚Р°: 2026-06-09.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.1 Release bundle automation`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

- СЃРѕР·РґР°РЅ `scripts/maintenance/build_release_bundle.py`;
- РґРѕР±Р°РІР»РµРЅ CLI entry point `ofz-build-release-bundle`;
- РґРѕР±Р°РІР»РµРЅРѕ РїСЂР°РІРёР»Рѕ `.gitignore` РґР»СЏ `releases/`;
- СЃРѕР·РґР°РЅ `docs/07_operations/release_bundle_plan.md`;
- РѕР±РЅРѕРІР»РµРЅС‹ README, production runbook Рё release checklist;
- release bundle СЃРѕР·РґР°РµС‚СЃСЏ РєР°Рє РІРЅРµС€РЅРёР№ artifact Рё РЅРµ РїРѕРїР°РґР°РµС‚ РІ Git.

### 3. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РїСЂРѕС€Р»Рё

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\build_release_bundle.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\build_release_bundle.py --dry-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe -m pip install -e .`: OK after approved retry.
- `.\.venv\Scripts\ofz-build-release-bundle.exe --help`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё СѓРїР°Р»Рё

Production-РїСЂРѕРІРµСЂРєРё РЅРµ СѓРїР°Р»Рё. РџРµСЂРІС‹Р№ Р·Р°РїСѓСЃРє `pip install -e .` РІРЅСѓС‚СЂРё sandbox РїРѕР»СѓС‡РёР» permission denied РЅР° `%TEMP%`; РїРѕРІС‚РѕСЂ СЃ СЂР°Р·СЂРµС€РµРЅРёРµРј РїСЂРѕС€РµР».

### 5. РљР°РєРёРµ warnings documented

- `telemetry_summary` РѕСЃС‚Р°РµС‚СЃСЏ optional РґРѕ СЌС‚Р°РїР° `P2.2 Pipeline telemetry`;
- СЂРµР°Р»СЊРЅС‹Р№ release bundle РЅРµ СЃРѕР·РґР°РµС‚СЃСЏ Р±РµР· `--include-outputs --confirm BUILD_RELEASE_BUNDLE`;
- generated outputs Рё `releases/` РЅРµ РєРѕРјРјРёС‚СЏС‚СЃСЏ.

### 6. РљР°РєРёРµ commits СЃРѕР·РґР°РЅС‹

Commit message: `Add release bundle automation`.

### 7. Р‘С‹Р» Р»Рё push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РїРѕСЃР»Рµ commit P2.1.

### 8. РўРµРєСѓС‰РёР№ git status

Р¤РёРєСЃРёСЂСѓРµС‚СЃСЏ РїРѕСЃР»Рµ commit/push P2.1.

### 9. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- `data/raw` tracked: РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ С‡РµСЂРµР· `git ls-files data/raw`;
- CLI entry points still work: `ofz-build-release-bundle --help` OK, РѕСЃС‚Р°Р»СЊРЅС‹Рµ entry points РЅРµ РјРµРЅСЏР»РёСЃСЊ.

### 10. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.2 Pipeline telemetry`.

## P2.2 - Pipeline telemetry

Р”Р°С‚Р°: 2026-06-09.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.2 Pipeline telemetry`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

- СЃРѕР·РґР°РЅ РјРѕРґСѓР»СЊ `scripts/pipeline/telemetry.py`;
- РґРѕР±Р°РІР»РµРЅ package marker `scripts/pipeline/__init__.py`;
- `ofz-run` С‚РµРїРµСЂСЊ РїРёС€РµС‚ telemetry JSON/MD РґР»СЏ РїРѕР»РЅРѕРіРѕ pipeline run;
- run manifest РІРєР»СЋС‡Р°РµС‚ СЃСЃС‹Р»РєРё РЅР° telemetry summary;
- release bundle РїРѕРґС…РІР°С‚С‹РІР°РµС‚ telemetry summary С‡РµСЂРµР· СЃСѓС‰РµСЃС‚РІСѓСЋС‰СѓСЋ РєР°С‚РµРіРѕСЂРёСЋ `telemetry_summary`;
- РєРѕРјР°РЅРґР° `ofz-run` Р±РµР· `--all/--stage/--stages`, РЅРѕ СЃ report params, Р·Р°РїСѓСЃРєР°РµС‚ РїРѕР»РЅС‹Р№ pipeline РєР°Рє production default.

### 3. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РїСЂРѕС€Р»Рё

РџСЂРѕРІРµСЂРєРё С„РёРєСЃРёСЂСѓСЋС‚СЃСЏ РїРѕСЃР»Рµ РІС‹РїРѕР»РЅРµРЅРёСЏ P2.2 validation commands.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё СѓРїР°Р»Рё

РџР°РґРµРЅРёСЏ С„РёРєСЃРёСЂСѓСЋС‚СЃСЏ РїРѕСЃР»Рµ РІС‹РїРѕР»РЅРµРЅРёСЏ P2.2 validation commands.

### 5. РљР°РєРёРµ warnings documented

- telemetry outputs СЏРІР»СЏСЋС‚СЃСЏ generated artifacts Рё РЅРµ РєРѕРјРјРёС‚СЏС‚СЃСЏ;
- telemetry summary РЅРµ Р·Р°РјРµРЅСЏРµС‚ QA scripts, Р° С„РёРєСЃРёСЂСѓРµС‚ runtime/audit metadata.

### 6. РљР°РєРёРµ commits СЃРѕР·РґР°РЅС‹

Commit message: `Add pipeline telemetry reporting`.

### 7. Р‘С‹Р» Р»Рё push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РїРѕСЃР»Рµ commit P2.2.

### 8. РўРµРєСѓС‰РёР№ git status

Р¤РёРєСЃРёСЂСѓРµС‚СЃСЏ РїРѕСЃР»Рµ commit/push P2.2.

### 9. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- `data/raw` tracked: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- CLI entry points still work: РїСЂРѕРІРµСЂРёС‚СЊ С‡РµСЂРµР· `ofz-run` Рё `ofz-quality`.

### 10. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.3 UI launcher contract`.

## P2.2 - Pipeline telemetry validation close-out

Р”Р°С‚Р°: 2026-06-09.

### РС‚РѕРі

`P2.2 Pipeline telemetry` Р·Р°РІРµСЂС€РµРЅ. `ofz-run` РїРёС€РµС‚ runtime telemetry РІ `outputs/reports/telemetry/`, run manifest СЃРѕРґРµСЂР¶РёС‚ СЃСЃС‹Р»РєРё РЅР° telemetry JSON/MD, Р° release bundle automation РїРѕРґС…РІР°С‚С‹РІР°РµС‚ telemetry summary РїСЂРё РЅР°Р»РёС‡РёРё.

### Р¤Р°РєС‚РёС‡РµСЃРєРёРµ РїСЂРѕРІРµСЂРєРё

- `.\.venv\Scripts\python.exe -m py_compile scripts\generate_executive_summary.py scripts\pipeline\telemetry.py scripts\run_pipeline.py scripts\run_manifest.py`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-run.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `Get-ChildItem outputs/reports/telemetry -Recurse -File`: telemetry JSON/MD files created.

### Р—Р°С„РёРєСЃРёСЂРѕРІР°РЅРЅС‹Рµ telemetry fields

- `run_id`, `started_at`, `finished_at`, `duration_seconds`;
- `stage_durations`;
- `input_row_counts`;
- `output_file_counts`;
- `generated_artifacts_count`, `artifacts_total_size_bytes`;
- `warnings_count`, `errors_count`;
- `cleanup_mode`;
- `quality_gate_results`, `schema_validation_results`;
- `git_commit`, `git_dirty_flag`;
- `raw_data_hashes`.

### Warnings documented

- Telemetry outputs are generated artifacts and are not committed.
- During validation an existing runtime cast issue in `generate_executive_summary.py` was fixed: runtime `cast(pd.Series[Any], ...)` was replaced with non-subscripted `pd.Series`.
- The latest telemetry run was executed with a dirty working tree because P2.2 source changes were intentionally uncommitted during validation.

### РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

`P2.3 UI launcher contract`.

### 11. P2.2 validation update

- `py_compile`: OK.
- `compileall`: OK.
- `ofz-run --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `ofz-quality --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- Latest telemetry summary: `outputs/reports/telemetry/telemetry_20260609_080836_53742514.json` and `.md`.
- Latest run manifest contains telemetry links.
- Initial P2.2 validation run found and fixed a runtime cast issue in `scripts/generate_executive_summary.py`: `pd.Series[Any]` was replaced with runtime-safe `pd.Series` inside `cast`.
- Generated outputs and telemetry reports remain ignored and must not be staged.

## Cost-aware rules accepted / session preflight

Р”Р°С‚Р°: 2026-06-11.

РџСЂРёРЅСЏС‚С‹ Р°РєС‚СѓР°Р»СЊРЅС‹Рµ СЂР°Р±РѕС‡РёРµ РїСЂР°РІРёР»Р°:

- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md`;
- `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md`.

РўРµРєСѓС‰РёР№ СЃС‚Р°С‚СѓСЃ P2 РїРѕРґС‚РІРµСЂР¶РґРµРЅ:

- `P2.0 Starting checkpoint`: completed;
- `P2.1 Release bundle automation`: completed;
- `P2.2 Pipeline telemetry`: completed;
- СЃР»РµРґСѓСЋС‰РёР№ СЌС‚Р°Рї: `P2.3 UI launcher contract`.

Session preflight РІС‹РїРѕР»РЅРµРЅ РѕРґРёРЅ СЂР°Р· РґР»СЏ С‚РµРєСѓС‰РµР№ СЂР°Р±РѕС‡РµР№ СЃРµСЃСЃРёРё:

- `git status --short --branch`: branch `main`, remote `origin/main`, untracked С‚РѕР»СЊРєРѕ РЅРѕРІС‹Рµ prompt-РёРЅСЃС‚СЂСѓРєС†РёРё v4/v5;
- `git branch --show-current`: `main`;
- `git remote -v`: `origin https://github.com/VinogradovPV/OFZ_ANALYTICS.git`;
- `git log --oneline -5`: latest commit `1b07100 Add pipeline telemetry reporting`;
- `gh --version`: OK;
- `gh auth status`: OK after approved outside-sandbox check;
- `gh repo view VinogradovPV/OFZ_ANALYTICS`: OK after approved outside-sandbox check;
- CLI help OK: `ofz-run`, `ofz-interactive`, `ofz-quality`, `ofz-clean-outputs`, `ofz-schema`, `ofz-build-release-bundle`.

Cost-aware / credit-aware СЂРµР¶РёРј РїСЂРёРЅСЏС‚:

- session preflight РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РѕРґРёРЅ СЂР°Р· РІ РЅР°С‡Р°Р»Рµ СЂР°Р±РѕС‡РµР№ СЃРµСЃСЃРёРё;
- docs-only СЌС‚Р°РїС‹ РёСЃРїРѕР»СЊР·СѓСЋС‚ Level 0 checks;
- UI source only СЌС‚Р°РїС‹ РёСЃРїРѕР»СЊР·СѓСЋС‚ Level 1 checks;
- Python/pipeline/schema/release/telemetry РёР·РјРµРЅРµРЅРёСЏ Р·Р°РїСѓСЃРєР°СЋС‚ targeted checks;
- full quality gate Р·Р°РїСѓСЃРєР°РµС‚СЃСЏ С‚РѕР»СЊРєРѕ РїРѕ СЏРІРЅС‹Рј С‚СЂРёРіРіРµСЂР°Рј РёР»Рё РїРµСЂРµРґ release/final close-out;
- generated outputs Рё `releases/` РЅРёРєРѕРіРґР° РЅРµ staged/committed.

РЎР»РµРґСѓСЋС‰РёР№ СЌС‚Р°Рї `P2.3 UI launcher contract` СЏРІР»СЏРµС‚СЃСЏ Level 0 / docs-only, РµСЃР»Рё Р±СѓРґРµС‚ РјРµРЅСЏС‚СЊСЃСЏ С‚РѕР»СЊРєРѕ РєРѕРЅС‚СЂР°РєС‚РЅР°СЏ РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ.

## P2.3 - UI launcher contract

Р”Р°С‚Р°: 2026-06-11.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.3 UI launcher contract`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

РЎРѕР·РґР°РЅ РґРѕРєСѓРјРµРЅС‚ `docs/07_operations/ui_launcher_contract.md`.

РљРѕРЅС‚СЂР°РєС‚ С„РёРєСЃРёСЂСѓРµС‚:

- UI launcher РІС‹Р·С‹РІР°РµС‚ С‚РѕР»СЊРєРѕ CLI, Р° РЅРµ РІРЅСѓС‚СЂРµРЅРЅРёРµ Python-С„СѓРЅРєС†РёРё;
- supported CLI: `ofz-run`, `ofz-interactive`, `ofz-quality`, `ofz-clean-outputs`, `ofz-schema`, `ofz-build-release-bundle`;
- РІР°Р»РёРґРёСЂСѓРµРјС‹Рµ РїР°СЂР°РјРµС‚СЂС‹ Р·Р°РїСѓСЃРєР°;
- cleanup modes Рё РѕР±СЏР·Р°С‚РµР»СЊРЅС‹Р№ `DELETE_OUTPUTS` РґР»СЏ СѓРґР°Р»РµРЅРёСЏ;
- release bundle creation С‚РѕР»СЊРєРѕ СЃ `--include-outputs --confirm BUILD_RELEASE_BUNDLE`;
- launcher logs РІ `outputs/reports/launcher/`;
- Р·Р°РїСЂРµС‚ arbitrary shell command, РёР·РјРµРЅРµРЅРёСЏ `data/raw`, commit generated outputs Рё РїР°СЂР°Р»Р»РµР»СЊРЅРѕРіРѕ fast/full quality gate;
- Word VBA launcher policy: `.bas/.frm` source, `.docm` release artifact;
- PowerShell GUI launcher policy: recommended first UI implementation, safe process arguments.

PowerShell GUI Рё Word VBA source РІ P2.3 РЅРµ СЃРѕР·РґР°РІР°Р»РёСЃСЊ.

### 3. РџСЂРѕРІРµСЂРѕС‡РЅС‹Р№ СѓСЂРѕРІРµРЅСЊ

Level 0 / docs-only.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РІС‹РїРѕР»РЅРµРЅС‹

- `git status --short --branch`;
- `git diff --name-only`;
- staged generated artifacts check;
- `Select-String` РїРѕ `docs/07_operations/ui_launcher_contract.md` РЅР° РєР»СЋС‡РµРІС‹Рµ С‚РѕРєРµРЅС‹.

### 5. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё skipped Рё РїРѕС‡РµРјСѓ

- `compileall`: skipped, Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --fast`: skipped, Python/pipeline/schema/release/telemetry РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --full`: skipped, РЅРµС‚ release/final close-out trigger.
- `gh auth status` / CLI help: skipped РїРѕРІС‚РѕСЂРЅРѕ, session preflight СѓР¶Рµ РІС‹РїРѕР»РЅРµРЅ Рё Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅ 2026-06-11.

### 6. Warnings documented

- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` Рё `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` РѕСЃС‚Р°СЋС‚СЃСЏ untracked source prompt files РґРѕ РѕС‚РґРµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ Рѕ commit.
- UI launcher log under `outputs/reports/launcher/` СЏРІР»СЏРµС‚СЃСЏ generated artifact Рё РЅРµ РєРѕРјРјРёС‚РёС‚СЃСЏ.

### 7. Commit

Commit message: `Document UI launcher contract`.

### 8. Push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РїРѕСЃР»Рµ commit P2.3.

### 9. Git status

Р¤РёРєСЃРёСЂСѓРµС‚СЃСЏ РїРѕСЃР»Рµ commit/push P2.3.

### 10. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- releases not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- `data/raw` tracked: СЂР°РЅРµРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ, РЅРµ РјРµРЅСЏР»РѕСЃСЊ;
- CLI entry points still work: РЅРµ С‚СЂРµР±РѕРІР°Р»Рё РїРѕРІС‚РѕСЂРЅРѕР№ РїСЂРѕРІРµСЂРєРё РїРѕ cost-aware rules, session preflight OK.

### 11. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.4 PowerShell GUI launcher MVP`.

## P2.4 - PowerShell GUI launcher MVP

Р”Р°С‚Р°: 2026-06-11.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.4 PowerShell GUI launcher MVP`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

РЎРѕР·РґР°РЅС‹:

- `tools/windows_launcher/ofz_launcher.ps1`;
- `tools/windows_launcher/README.md`.

РћР±РЅРѕРІР»РµРЅС‹:

- `README.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

Launcher СЂРµР°Р»РёР·РѕРІР°РЅ РєР°Рє Р±РµР·РѕРїР°СЃРЅР°СЏ РѕР±РѕР»РѕС‡РєР° РЅР°Рґ CLI:

- РІС‹Р·С‹РІР°РµС‚ С‚РѕР»СЊРєРѕ whitelisted CLI entry points;
- РІР°Р»РёРґРёСЂСѓРµС‚ `project_root`, `.venv`, `pyproject.toml`, `data/raw`, `report_date`, `retrospective_years`, `period_type`, `aggregation_mode` Рё action;
- РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ РІС‹РїРѕР»РЅСЏРµС‚ Р±РµР·РѕРїР°СЃРЅС‹Р№ smoke-check, Р° GUI РѕС‚РєСЂС‹РІР°РµС‚ С‚РѕР»СЊРєРѕ РїРѕ `-Gui`;
- РїРёС€РµС‚ Р»РѕРіРё РІ `outputs/reports/launcher/`;
- Р±Р»РѕРєРёСЂСѓРµС‚ delete cleanup Р±РµР· `DELETE_OUTPUTS`;
- Р±Р»РѕРєРёСЂСѓРµС‚ release bundle creation Р±РµР· `BUILD_RELEASE_BUNDLE`;
- РЅРµ РїСЂРёРЅРёРјР°РµС‚ arbitrary shell command input;
- РЅРµ СЃРѕР·РґР°РµС‚ GitHub release.

### 3. РџСЂРѕРІРµСЂРѕС‡РЅС‹Р№ СѓСЂРѕРІРµРЅСЊ

Level 1 / UI source only.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РІС‹РїРѕР»РЅРµРЅС‹

- `git status --short --branch`;
- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`;
- staged generated artifacts check;
- `git diff --name-only`;
- launcher smoke РїРѕРґС‚РІРµСЂРґРёР» environment validation, bad-date block, delete confirmation block, bundle confirmation block, cleanup dry-run, release bundle dry-run Рё СЃРѕР·РґР°РЅРёРµ launcher log.

### 5. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё skipped Рё РїРѕС‡РµРјСѓ

- `compileall`: skipped, Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --fast`: skipped, pipeline/schema/release/telemetry Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --full`: skipped, РЅРµС‚ release/final close-out trigger.
- `gh auth status` Рё CLI help preflight: skipped РїРѕРІС‚РѕСЂРЅРѕ, session preflight СѓР¶Рµ РІС‹РїРѕР»РЅРµРЅ Рё Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅ.

### 6. Warnings documented

- Smoke launcher СЃРѕР·РґР°РµС‚ generated log under `outputs/reports/launcher/`; СЌС‚РѕС‚ С„Р°Р№Р» РёРіРЅРѕСЂРёСЂСѓРµС‚СЃСЏ Git.
- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` Рё `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` РѕСЃС‚Р°СЋС‚СЃСЏ untracked source prompt files РґРѕ РѕС‚РґРµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ.

### 7. Commit

Commit message: `Add Windows UI launcher MVP`.

### 8. Push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РїРѕСЃР»Рµ commit P2.4.

### 9. Git status

Р¤РёРєСЃРёСЂСѓРµС‚СЃСЏ РїРѕСЃР»Рµ commit/push P2.4.

### 10. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- releases not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- `data/raw` tracked: СЂР°РЅРµРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ, РЅРµ РјРµРЅСЏР»РѕСЃСЊ;
- CLI entry points still work: session preflight OK; launcher РІС‹Р·С‹РІР°РµС‚ entry points С‡РµСЂРµР· `.venv\Scripts`.

### 11. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.5 Word VBA launcher spec and source`.

## P2.5 - Word VBA launcher spec and source

Р”Р°С‚Р°: 2026-06-11.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.5 Word VBA launcher spec and source`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

РЎРѕР·РґР°РЅС‹:

- `docs/07_operations/word_vba_launcher_spec.md`;
- `tools/word_launcher/README.md`;
- `tools/word_launcher/OfzLauncher.bas`.

РћР±РЅРѕРІР»РµРЅС‹:

- `README.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

Word VBA launcher source С„РёРєСЃРёСЂСѓРµС‚:

- `.bas` source РјРѕР¶РЅРѕ РєРѕРјРјРёС‚РёС‚СЊ;
- `.docm` СЏРІР»СЏРµС‚СЃСЏ release artifact Рё РЅРµ РєРѕРјРјРёС‚РёС‚СЃСЏ Р±РµР· РѕС‚РґРµР»СЊРЅРѕРіРѕ artifact policy decision;
- VBA РІС‹Р·С‹РІР°РµС‚ С‚РѕР»СЊРєРѕ whitelisted CLI under `.venv\Scripts`;
- delete cleanup С‚СЂРµР±СѓРµС‚ `DELETE_OUTPUTS`;
- release bundle creation С‚СЂРµР±СѓРµС‚ `BUILD_RELEASE_BUNDLE`;
- macro security documented;
- arbitrary shell command input Рё GitHub Release creation Р·Р°РїСЂРµС‰РµРЅС‹.

### 3. РџСЂРѕРІРµСЂРѕС‡РЅС‹Р№ СѓСЂРѕРІРµРЅСЊ

Level 1 / UI source only.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РІС‹РїРѕР»РЅРµРЅС‹

- `git status --short --branch`;
- reference/status review РїРѕСЃР»Рµ P2.4;
- `Select-String` РїРѕ `tools/word_launcher/OfzLauncher.bas`, `tools/word_launcher/README.md`, `docs/07_operations/word_vba_launcher_spec.md` РЅР° РєР»СЋС‡РµРІС‹Рµ safety-С‚РѕРєРµРЅС‹;
- staged generated artifacts check.

### 5. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё skipped Рё РїРѕС‡РµРјСѓ

- `compileall`: skipped, Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --fast`: skipped, pipeline/schema/release/telemetry Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --full`: skipped, РЅРµС‚ release/final close-out trigger.
- Word import smoke: manual-only; Р°РІС‚РѕРјР°С‚РёС‡РµСЃРєРёР№ Word UI Р·Р°РїСѓСЃРє РЅРµ РІС‹РїРѕР»РЅСЏР»СЃСЏ РІ СЌС‚РѕРј СЌС‚Р°РїРµ.

### 6. Warnings documented

- `.docm` РЅРµ СЃРѕР·РґР°РЅ Рё РЅРµ РєРѕРјРјРёС‚РёС‚СЃСЏ.
- РџРµСЂРµРґ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёРµРј Word launcher РЅСѓР¶РЅРѕ РёРјРїРѕСЂС‚РёСЂРѕРІР°С‚СЊ `OfzLauncher.bas` РІ trusted `.docm` Рё РІС‹РїРѕР»РЅРёС‚СЊ СЂСѓС‡РЅРѕР№ smoke `OfzSmokeTest`.
- `prompts/ofz_p2_modernization_system_prompt_v4_cost_aware.md` Рё `prompts/ofz_p2_modernization_step_by_step_v5_cost_aware.md` РѕСЃС‚Р°СЋС‚СЃСЏ untracked source prompt files РґРѕ РѕС‚РґРµР»СЊРЅРѕРіРѕ СЂРµС€РµРЅРёСЏ.

### 7. Commit

Commit message: `Add Word VBA launcher specification`.

### 8. Push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РїРѕСЃР»Рµ commit P2.5.

### 9. Git status

Р¤РёРєСЃРёСЂСѓРµС‚СЃСЏ РїРѕСЃР»Рµ commit/push P2.5.

### 10. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- releases not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- `data/raw` tracked: СЂР°РЅРµРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ, РЅРµ РјРµРЅСЏР»РѕСЃСЊ;
- CLI entry points still work: session preflight OK; VBA source РІС‹Р·С‹РІР°РµС‚ С‚РѕР»СЊРєРѕ whitelisted CLI paths.

### 11. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.6 UI launcher documentation and artifact policy update`.

## P2.6 - UI launcher documentation and artifact policy update

Р”Р°С‚Р°: 2026-06-11.

### 1. РљР°РєРѕР№ P2-СЌС‚Р°Рї РІС‹РїРѕР»РЅРµРЅ

Р’С‹РїРѕР»РЅРµРЅ `P2.6 UI launcher documentation and artifact policy update`.

### 2. Р§С‚Рѕ РёР·РјРµРЅРµРЅРѕ

РћР±РЅРѕРІР»РµРЅС‹:

- `README.md`;
- `docs/07_operations/production_runbook.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/00_project/artifact_policy.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

Р—Р°С„РёРєСЃРёСЂРѕРІР°РЅРѕ:

- CLI РѕСЃС‚Р°РµС‚СЃСЏ РіР»Р°РІРЅС‹Рј supported production interface;
- PowerShell GUI launcher СЏРІР»СЏРµС‚СЃСЏ recommended Windows UI MVP;
- Word VBA launcher СЏРІР»СЏРµС‚СЃСЏ optional launcher;
- `.ps1`, `.bas`, `.frm` СЏРІР»СЏСЋС‚СЃСЏ source artifacts;
- `.docm` СЏРІР»СЏРµС‚СЃСЏ release artifact unless explicitly approved;
- launcher logs under `outputs/reports/launcher/` СЏРІР»СЏСЋС‚СЃСЏ generated outputs;
- release bundle РѕСЃС‚Р°РµС‚СЃСЏ external artifact under ignored `releases/`;
- UI launcher РЅРµ Р·Р°РјРµРЅСЏРµС‚ quality gate.

### 3. РџСЂРѕРІРµСЂРѕС‡РЅС‹Р№ СѓСЂРѕРІРµРЅСЊ

Level 0 / docs-only.

### 4. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё РІС‹РїРѕР»РЅРµРЅС‹

- `git status --short --branch`;
- docs diff review;
- staged generated artifacts check.

### 5. РљР°РєРёРµ РїСЂРѕРІРµСЂРєРё skipped Рё РїРѕС‡РµРјСѓ

- `compileall`: skipped, Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --fast`: skipped, Python/pipeline/schema/release/telemetry РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.
- `ofz-quality --full`: skipped, РЅРµС‚ release/final close-out trigger.

### 6. Warnings documented

- Р’ СЂР°Р±РѕС‡РµРј РґРµСЂРµРІРµ СѓР¶Рµ Р±С‹Р»Рё РЅРµР·Р°РєРѕРјРјРёС‡РµРЅРЅС‹Рµ P2.5 source/docs РёР·РјРµРЅРµРЅРёСЏ РґРѕ РЅР°С‡Р°Р»Р° P2.6; P2.6 РЅРµ РІС‹РїРѕР»РЅСЏР» С„РёР·РёС‡РµСЃРєРёРµ cleanup/decomposition РґРµР№СЃС‚РІРёСЏ.
- `tools/word_launcher/` Рё prompt v4/v5 С„Р°Р№Р»С‹ РѕСЃС‚Р°СЋС‚СЃСЏ РІРЅРµ P2.6, РµСЃР»Рё РЅРµ Р±СѓРґСѓС‚ РѕС‚РґРµР»СЊРЅРѕ staged.

### 7. Commit

Commit message: `Document UI launcher usage and artifact policy`.

### 8. Push

Push РІС‹РїРѕР»РЅСЏРµС‚СЃСЏ РїРѕСЃР»Рµ commit P2.6.

### 9. Git status

Р¤РёРєСЃРёСЂСѓРµС‚СЃСЏ РїРѕСЃР»Рµ commit/push P2.6.

### 10. РџРѕРґС‚РІРµСЂР¶РґРµРЅРёСЏ

- generated outputs not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- releases not staged: РїСЂРѕРІРµСЂРёС‚СЊ РїРµСЂРµРґ commit;
- `data/raw` tracked: СЂР°РЅРµРµ РїРѕРґС‚РІРµСЂР¶РґРµРЅРѕ, РЅРµ РјРµРЅСЏР»РѕСЃСЊ;
- CLI entry points still work: session preflight OK, Python-РєРѕРґ РЅРµ РјРµРЅСЏР»СЃСЏ.

### 11. РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ P2-СЌС‚Р°Рї

РЎР»РµРґСѓСЋС‰РёР№ СЂРµРєРѕРјРµРЅРґСѓРµРјС‹Р№ СЌС‚Р°Рї: `P2.7 Screenshot visual regression backend`.
## P2.6.1 - PowerShell GUI launcher hardening close-out

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен обязательный промежуточный этап `P2.6.1 PowerShell GUI launcher hardening close-out`.

### 2. Исходный gap

После P2.4 PowerShell GUI launcher был функциональным smoke-wrapper, но GUI содержал только `Report date` и `Action`. Этого было недостаточно для production-like ручного запуска, потому что нельзя было выбирать:

- `project_root`;
- `retrospective_years`;
- `period_type`;
- `aggregation_mode`;
- cleanup mode;
- release/delete confirmation tokens;
- open outputs/release folders;
- command preview.

Также GUI закрывался автоматически через таймер, что было допустимо для проверки, но неверно для ручной работы.

### 3. Что изменено

Обновлены:

- `tools/windows_launcher/ofz_launcher.ps1`;
- `tools/windows_launcher/README.md`;
- `README.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

GUI теперь содержит:

- project root;
- report date;
- retrospective years;
- period type;
- aggregation mode;
- action;
- cleanup mode;
- schema/quality/release options;
- `DELETE_OUTPUTS` confirmation;
- `BUILD_RELEASE_BUNDLE` confirmation;
- command preview;
- output/status area;
- launcher log path.

### 4. Safety policy

Сохранено:

- только approved CLI entry points;
- no arbitrary shell command;
- no internal Python function calls;
- no `data/raw` changes;
- no GitHub Release creation;
- no fast/full quality gate parallel run;
- delete cleanup blocked without `DELETE_OUTPUTS`;
- release-build blocked without `BUILD_RELEASE_BUNDLE`.

### 5. Проверочный уровень

Level 1 / UI source only.

### 6. Какие проверки выполнены

- PowerShell parse check for `tools/windows_launcher/ofz_launcher.ps1`: OK;
- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1`: OK;
- `powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Gui -AutoCloseGuiForCheck`: OK;
- smoke подтвердил environment validation, bad date block, delete confirmation block, release confirmation block, cleanup dry-run, release bundle dry-run и launcher log creation.

### 7. Какие проверки skipped и почему

- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, UI source only.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.
- Ручной interactive GUI smoke пользователем остается желательным: открыть `-Gui`, проверить поля и нажать `Validate`.

### 8. Warnings documented

- `tools/word_launcher/` и prompt v4/v5/v6 файлы остаются вне этого этапа, если отдельно не staged.
- Запуск smoke создает generated logs under `outputs/reports/launcher/` и cleanup dry-run manifests under `outputs/reports/cleanup/`; они игнорируются Git.

### 9. Commit

Commit message: `Enhance Windows UI launcher parameters`.

### 10. Push

Push выполняется после commit P2.6.1.

### 11. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап после закрытия launcher gap: `P2.7 Screenshot visual regression backend`.

## P2.6.2 - Word VBA docm assembly and UserForm

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен обязательный промежуточный этап `P2.6.2 Word VBA docm assembly and UserForm`.

### 2. Что изменено

Обновлены и добавлены:

- `tools/word_launcher/OfzLauncher.bas`;
- `tools/word_launcher/frmOfzLauncher.frm`;
- `tools/word_launcher/word_docm_build_instructions.md`;
- `tools/word_launcher/README.md`;
- `docs/07_operations/word_vba_launcher_spec.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/00_project/artifact_policy.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

`OfzLauncher.bas` теперь содержит required `OFZ_*` procedures/functions, validation, command preview/build logic, safe CLI-only process execution and launcher logging.

`frmOfzLauncher.frm` содержит source UserForm `frmOfzLauncher` с required controls for project root, report params, action, confirmation tokens, command preview, log output and action buttons.

### 3. Artifact status

- `.bas` / `.frm` / build instructions are source artifacts.
- `.docm` is a release artifact.
- Recommended `.docm` path: `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`.
- `.docm` and `releases/` must not be committed.

### 4. Проверочный уровень

Level 1 / UI source only.

### 5. Какие проверки выполнены

- required `OFZ_*` procedure/function scan in `OfzLauncher.bas`;
- required UserForm control scan in `frmOfzLauncher.frm`;
- `.docm` / `releases/` not staged check before commit;
- generated outputs not staged check before commit.

### 6. Какие проверки skipped и почему

- Word automation/manual import: skipped in this environment; `.docm` assembly is `deferred/manual`.
- `compileall`: skipped, Python-код не менялся.
- `ofz-quality --fast`: skipped, UI source/docs only.
- `ofz-quality --full`: skipped, нет release/final close-out trigger.

### 7. Warnings documented

- `.docm` must be assembled manually in Word or by a controlled Word automation step on an operator workstation.
- Macros can be blocked; use Trusted Location and consider code signing.
- Word launcher does not accept arbitrary shell commands and calls only whitelisted CLI.
- Delete cleanup requires `DELETE_OUTPUTS`.
- Release bundle creation requires `BUILD_RELEASE_BUNDLE`.

### 8. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап после закрытия Word launcher gap: `P2.7 Screenshot visual regression backend`.

## P2.7 - Screenshot visual regression backend

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.7 Screenshot visual regression backend`.

### 2. Что изменено

Обновлены:

- `scripts/visual_regression.py`;
- `requirements-dev.txt`;
- `pyproject.toml`;
- `README.md`;
- `docs/06_quality/visual_regression_backend_decision.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

### 3. Backend decision

Основное решение: Playwright screenshot backend для локальных HTML/Plotly charts.

Fallback static HTML / Plotly JSON inspection сохранен как резервный и контрактный режим.

Поддержанные режимы:

- `--mode fallback`;
- `--mode screenshot`;
- `--mode auto`.

`auto` сначала пытается использовать Playwright, а если backend или browser binaries недоступны, явно фиксирует warning и переходит в fallback.

### 4. Generated artifacts

Screenshot backend пишет generated outputs:

- `outputs/reports/visual_regression/screenshots/<run_id>/*.png`;
- `outputs/reports/visual_regression/screenshot_manifest_*.json`;
- `outputs/reports/visual_regression/diffs/screenshot_diff_report_*.md`.

Эти файлы не коммитятся.

### 5. Проверочный уровень

Level 3 initially. Level 5 only after backend stabilization and explicit full-gate trigger.

### 6. Какие проверки выполнены

- `.\.venv\Scripts\python.exe -m py_compile scripts\visual_regression.py`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode fallback --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --mode auto --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK, with documented Playwright-unavailable warning and fallback.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- Pylance missing-import issue for `playwright.sync_api`: fixed by replacing direct optional imports with dynamic `importlib.import_module`.

### 7. Какие warnings documented

- Playwright is not installed in the current `.venv`; `--mode auto` uses fallback and records a warning.
- Screenshot mode requires `requirements-dev.txt` plus `python -m playwright install chromium`.
- Screenshot PNG/manifest/diff outputs are generated artifacts and must not be committed.
- Missing baseline screenshots are recorded as `missing_baseline`, not as a failure during backend stabilization.

### 8. Следующий рекомендуемый P2-этап

После завершения P2.7 и стабилизации проверок: `P2.8 CI / GitHub Actions`.

## P2.8 - CI / GitHub Actions

Дата: 2026-06-11.

### 1. Какой P2-этап выполнен

Выполнен `P2.8 CI / GitHub Actions`.

### 2. Что изменено

Добавлены и обновлены:

- `.github/workflows/quality.yml`;
- `docs/07_operations/ci_workflow.md`;
- `README.md`;
- `docs/07_operations/release_checklist.md`;
- `docs/06_quality/manual_checks_log.md`;
- `docs/00_project/p2_modernization_progress_report.md`.

### 3. CI contract

Workflow запускает `quality-fast` на `push`/`pull_request` в `main` и через `workflow_dispatch`.

`quality-fast` выполняет checkout, setup Python, install runtime/dev dependencies, editable install, `pip check`, `compileall`, `ofz-schema` и `ofz-quality --fast`.

`quality-full` доступен только вручную через `workflow_dispatch`, зависит от `quality-fast` и не запускается параллельно с fast job.

### 4. Artifact policy

CI не коммитит generated outputs. QA reports сохраняются как GitHub Actions artifacts. Кешируется только pip cache; `outputs/` и `releases/` не кешируются.

### 5. Проверочный уровень

Level 2 locally. GitHub-side validation через `gh workflow list` / `gh run list` после push.

### 6. Какие проверки выполнены

- `.\.venv\Scripts\python.exe -m pip check`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-schema.exe --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK, 16/16 checks passed.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- staged generated artifacts check: OK before commit.
- GitHub-side `gh workflow list` / `gh run list`: planned after push.

### 7. Warnings documented

Screenshot backend browser binaries are not installed in CI during P2.8. Local fast gate completed with expected warning: screenshot backend unavailable and visual regression used fallback/static inspection mode.

### 8. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.9 Controlled docs archive apply`.

## P2.9 - Controlled docs archive apply

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен `P2.9 Controlled docs archive apply`.

### 2. Что изменено

Обновлены и созданы:

- `scripts/maintenance/cleanup_docs.py`;
- `scripts/quality_gate.py`;
- `docs/index.md`;
- `docs/00_project/docs_inventory_before_cleanup.md`;
- `docs/00_project/docs_inventory_after_cleanup.md`;
- `docs/00_project/docs_archive_apply_report.md`;
- `docs/archive/2026-06-15/`;
- `README.md`.

### 3. Результат cleanup

После повторного dry-run активные P2 operation docs сохранены как `keep_active`, а legacy diagnostics/stage/reproducibility reports переведены в controlled archive.

Итог archive mode:

- `keep_active`: 61 documents;
- `archive_candidate`: 39 documents;
- archive folder: `docs/archive/2026-06-15/`;
- `--delete-archived`: not executed.

### 4. Что не делалось

- Generated cleanup manifests under `outputs/reports/cleanup/` are not committed.
- No archived docs were deleted.
- No scripts were moved or deleted.
- P2.10 legacy scripts archive remains a separate controlled stage.

### 5. Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\maintenance\cleanup_docs.py scripts\quality_gate.py`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run`: OK.
- `.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --archive`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.10 Controlled legacy scripts archive apply`.

## P2.10 - Controlled legacy scripts archive apply

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен `P2.10 Controlled legacy scripts archive apply`.

### 2. Что изменено

Пять legacy maintenance scripts перенесены в `scripts/archive/2026-06-15/`:

- `cleanup_docs.py`;
- `migrate_outputs_structure.py`;
- `reorganize_outputs.py`;
- `migrate_legacy_docs_archive.py`;
- `reorganize_docs.py`.

Добавлен `scripts/archive/2026-06-15/README.md`.

Обновлены active docs so old scripts are no longer presented as production commands:

- `README.md`;
- `scripts/README.md`;
- `docs/00_project/scripts_archive_decision.md`;
- `docs/00_project/scripts_inventory_before_cleanup.md`;
- `docs/00_project/scripts_structure_plan.md`;
- `docs/00_project/scripts_migration_plan.md`;
- `docs/00_project/outputs_structure.md`;
- `docs/00_project/production_readiness_report.md`;
- `docs/00_project/final_project_summary.md`;
- `docs/03_pipeline/module_decomposition_plan.md`.

### 3. Что не делалось

- No files were deleted.
- No production entry points were changed.
- Generated outputs were not staged.
- Physical module decomposition remains P2-only.

### 4. Проверки

- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- CLI help checks for `ofz-run`, `ofz-quality`, `ofz-clean-outputs`, `ofz-schema`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 5. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.11 Controlled module decomposition`.

## P2.11.1 - Chart common helpers

Дата: 2026-06-15.

### 1. Какой P2-этап выполнен

Выполнен первый малый шаг `P2.11 Controlled module decomposition`: `P2.11.1 Chart common helpers`.

### 2. Что изменено

Создан пакет `scripts/charts/`:

- `scripts/charts/__init__.py`;
- `scripts/charts/common.py`.

Из `scripts/06_build_charts.py` вынесены только pure formatting helpers:

- `format_number_text`;
- `format_hover_number`;
- `format_bln`;
- `format_percent_label`;
- `format_metric_value`;
- `format_signed_metric_value`;
- `format_ru_number`.

`scripts/06_build_charts.py` остается стабильным wrapper/orchestrator. CLI behavior, output filenames, chart contracts and schema contracts were not changed.

### 3. Что не делалось

- No chart family builders were moved.
- No QA modules were extracted.
- No output filename changes.
- No generated outputs were staged.
- Physical module decomposition remains incremental: one small extraction per commit.

### 4. Проверки

- `.\.venv\Scripts\python.exe -m py_compile scripts\06_build_charts.py scripts\charts\common.py scripts\charts\__init__.py`: OK.
- `.\.venv\Scripts\python.exe -m compileall -q scripts`: OK.
- `.\.venv\Scripts\python.exe scripts\06_build_charts.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\html_chart_qa.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\python.exe scripts\visual_regression.py --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.
- `.\.venv\Scripts\ofz-quality.exe --fast --report-date 2026-05-01 --retrospective-years 4 --period-type month --aggregation-mode cumulative`: OK.

### 5. Warnings documented

Visual regression in `auto` mode recorded the known warning that the screenshot backend was unavailable in the current environment and fallback static inspection was used.

### 6. Следующий рекомендуемый P2-этап

Следующий рекомендуемый этап: `P2.11.2 Chart family modules`, but only as another small extraction with the same no-behavior-change rule.

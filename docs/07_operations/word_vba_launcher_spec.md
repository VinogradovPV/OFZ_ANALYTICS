# Word VBA Launcher Specification

Дата: 2026-06-11.

## Статус

`P2.5 Word VBA launcher spec and source` добавляет только исходный VBA-код и документацию.

Разрешено хранить в Git:

- `tools/word_launcher/OfzLauncher.bas`;
- `tools/word_launcher/README.md`;
- будущие `.frm` / `.frx` source-файлы, если будет создан UserForm.

Не хранить в Git без отдельного artifact policy decision:

- `.docm`;
- `.dotm`;
- сгенерированные logs;
- generated outputs;
- release bundles.

`.docm` считается release artifact, а не source artifact.

## Назначение

Word VBA launcher нужен как офисный thin UI-wrapper для пользователей, которым удобнее запускать production CLI из Word-документа с макросом. Он не заменяет CLI, PowerShell launcher или interactive pipeline.

Основной принцип:

> VBA вызывает только разрешенные CLI entry points и не принимает произвольные shell-команды.

## Supported CLI

VBA launcher может вызывать только:

- `ofz-run.exe`;
- `ofz-interactive.exe`;
- `ofz-quality.exe`;
- `ofz-clean-outputs.exe`;
- `ofz-schema.exe`;
- `ofz-build-release-bundle.exe`.

CLI должны находиться в:

```text
<project_root>\.venv\Scripts\
```

## Поддерживаемые параметры

- `project_root`;
- `report_date`;
- `retrospective_years`;
- `period_type`;
- `aggregation_mode`;
- `action`;
- `confirm_token`.

## Validation Rules

VBA launcher обязан проверять:

- `project_root` существует;
- `pyproject.toml` существует;
- `.venv\Scripts` существует;
- `data\raw` существует;
- `report_date` соответствует `YYYY-MM-DD`;
- `report_date` является первым днем месяца;
- `retrospective_years` находится в диапазоне `1..10`;
- `period_type` входит в `month`, `quarter`, `year`;
- `aggregation_mode` входит в `cumulative`, `point`;
- `action` входит в whitelist.

## Actions

Разрешенные actions:

- `validate`;
- `run`;
- `schema`;
- `quality-fast`;
- `quality-full`;
- `cleanup-dry-run`;
- `cleanup-archive-all`;
- `cleanup-delete-all-with-archive`;
- `release-dry-run`;
- `release-build`.

## Safety Gates

### Cleanup Delete

`cleanup-delete-all-with-archive` должен быть заблокирован, если не передан token:

```text
DELETE_OUTPUTS
```

VBA не должен выполнять удаление напрямую. Он может только вызвать:

```text
ofz-clean-outputs.exe --archive-all --delete-all --confirm DELETE_OUTPUTS
```

### Release Bundle Build

`release-build` должен быть заблокирован, если не передан token:

```text
BUILD_RELEASE_BUNDLE
```

VBA может вызвать build только так:

```text
ofz-build-release-bundle.exe --include-outputs --confirm BUILD_RELEASE_BUNDLE ...
```

## Logging

Launcher пишет log в:

```text
outputs\reports\launcher\word_launcher_run_<timestamp>.log
```

Log должен фиксировать:

- timestamp;
- working directory;
- command preview;
- stdout;
- stderr;
- exit code.

Logs являются generated artifacts и не коммитятся.

## Macro Security

Перед использованием `.docm`:

- включить макросы только для доверенного файла;
- хранить source `.bas` в Git, а `.docm` собирать как release artifact;
- не вставлять секреты, tokens или credentials в VBA-код;
- не добавлять arbitrary command textbox;
- не создавать GitHub Release из Word macro.

## Manual Import Check

Если Microsoft Word доступен:

1. Открыть Word.
2. Создать пустой `.docm`.
3. Открыть VBA editor.
4. Import File: `tools/word_launcher/OfzLauncher.bas`.
5. Запустить `OfzValidateEnvironment`.
6. Проверить, что bad date блокируется через `OfzSmokeTest`.
7. Сохранить `.docm` вне Git или как external release artifact.

## Relationship With Other Launchers

- PowerShell launcher остается recommended first UI implementation.
- Word VBA launcher source нужен для будущего `.docm` release artifact.
- Оба launcher вызывают один и тот же CLI-контракт.
- UI launcher contract: `docs/07_operations/ui_launcher_contract.md`.
- Release bundle behavior: `docs/07_operations/release_bundle_plan.md`.
## P2.6.2 Word DOCM Assembly Contract

Дата: 2026-06-11.

`P2.6.2` добавляет source-файл UserForm и инструкцию сборки `.docm`.

Tracked source:

- `tools/word_launcher/OfzLauncher.bas`;
- `tools/word_launcher/frmOfzLauncher.frm`;
- `tools/word_launcher/word_docm_build_instructions.md`.

Release artifact:

- `releases/ui_launcher/ofz_launcher_word_<timestamp>.docm`.

`.docm` не коммитится в Git и собирается вручную или через Word automation на рабочей станции, где доступен Microsoft Word.

### Required VBA entry points

`OfzLauncher.bas` экспортирует:

- `OFZ_ShowLauncher`;
- `OFZ_RunPipeline`;
- `OFZ_RunSchemaValidation`;
- `OFZ_RunQualityGateFast`;
- `OFZ_RunQualityGateFull`;
- `OFZ_CleanupDryRun`;
- `OFZ_CleanupArchiveAll`;
- `OFZ_CleanupDeleteAll`;
- `OFZ_ReleaseBundleDryRun`;
- `OFZ_ReleaseBundleBuild`;
- `OFZ_OpenOutputsFolder`;
- `OFZ_OpenReleasesFolder`.

Обязательные validation/helper functions:

- `OFZ_ValidateProjectRoot`;
- `OFZ_ValidateReportDate`;
- `OFZ_ValidateRetrospectiveYears`;
- `OFZ_BuildCommand`;
- `OFZ_RunCommand`;
- `OFZ_LogPath`.

### UserForm controls

Form name: `frmOfzLauncher`.

Required controls:

- `txtProjectRoot`;
- `btnBrowseProjectRoot`;
- `btnValidateProject`;
- `txtReportDate`;
- `cmbRetrospectiveYears`;
- `cmbPeriodType`;
- `cmbAggregationMode`;
- `cmbAction`;
- `chkRunSchema`;
- `chkRunQualityFast`;
- `chkRunQualityFull`;
- `chkBuildReleaseBundle`;
- `chkOpenOutputs`;
- `chkOpenReleases`;
- `txtDeleteConfirm`;
- `txtReleaseConfirm`;
- `txtCommandPreview`;
- `txtLogOutput`;
- `btnPreviewCommand`;
- `btnRun`;
- `btnOpenOutputs`;
- `btnOpenReleases`;
- `btnClose`.

### Assembly status

Автоматическая сборка `.docm` не имитируется, если Word automation недоступна. В этом случае статус: `docm assembly deferred/manual`, а ручная сборка выполняется по `tools/word_launcher/word_docm_build_instructions.md`.

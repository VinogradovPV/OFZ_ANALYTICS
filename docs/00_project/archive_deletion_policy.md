# Политика удаления архивов

Дата актуализации: 2026-06-16.

## Назначение

Этот документ фиксирует правила физического удаления архивированных документов и legacy scripts после controlled archive steps P2.9 и P2.10.

Архивы являются audit artifacts. В production-ready candidate их нельзя удалять физически, даже если документы или scripts уже перенесены в archive folders.

## Область действия

Политика применяется к:

- `docs/archive/**`;
- `docs/90_archive/**`, если используется как legacy/archive зона;
- `scripts/archive/**`;
- archive manifests, созданным cleanup tooling;
- future archived docs/scripts после P2.

Политика не применяется к generated outputs under `outputs/archive/`; для них действует `docs/00_project/artifact_policy.md` и cleanup outputs policy.

## Базовые правила

1. Archived docs/scripts не удаляются в статусе production-ready candidate.
2. Физическое удаление разрешено только после stable release.
3. Перед удалением должен существовать release tag.
4. Перед удалением должен существовать release bundle или equivalent external artifact.
5. Перед удалением должен быть выполнен references check.
6. Перед удалением должен быть archive manifest.
7. Удаление выполняется отдельным commit.
8. `--delete-archived` запрещен без explicit approval пользователя.

## Обязательные предварительные условия

Перед физическим удалением archived docs/scripts должны быть выполнены все условия:

- stable release завершен и принят;
- создан release tag, например `v1.0.0` или другой утвержденный tag;
- создан release bundle, содержащий документацию, manifest, QA reports и relevant archived inventory;
- references check подтверждает, что archived files не используются в:
  - `README.md`;
  - `docs/**`;
  - `scripts/**`;
  - `pyproject.toml`;
  - operations docs;
  - CI workflow;
- archive manifest содержит список удаляемых файлов, их прежние пути, размеры и checksums;
- deletion plan reviewed manually;
- пользователь явно подтвердил deletion command.

## Команды и подтверждения

Dry-run обязателен:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --dry-run
```

Archive mode не является удалением:

```powershell
.\.venv\Scripts\python.exe scripts\maintenance\cleanup_docs.py --archive
```

Физическое удаление archive candidates допускается только отдельной будущей командой и только после explicit approval. Нельзя запускать `--delete-archived` как часть обычного cleanup или release run.

## Политика commit

Удаление archived docs/scripts должно идти отдельным commit:

```powershell
git status --short
git diff --name-only
git add <only deletion-related docs/scripts changes>
git commit -m "Delete archived documentation after stable release"
git push
```

Нельзя смешивать physical archive deletion с:

- pipeline changes;
- schema/data contract changes;
- chart changes;
- release bundle build outputs;
- generated outputs cleanup;
- module decomposition.

## Аудиторский след

После удаления нужно обновить:

- `docs/00_project/archive_deletion_policy.md`;
- `docs/00_project/p2_modernization_progress_report.md` или актуальный release progress report;
- `docs/06_quality/manual_checks_log.md`;
- archive manifest или deletion manifest.

Deletion manifest должен фиксировать:

- дату;
- release tag;
- release bundle path/id;
- список удаленных файлов;
- checksums из archive manifest;
- references check result;
- explicit approval reference.

## Текущий статус

На 2026-06-16 физическое удаление archived docs/scripts запрещено.

Текущий статус: `deferred_until_after_stable_release`.


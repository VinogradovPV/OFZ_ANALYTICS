# Ручная проверка desktop GUI launcher

Дата: 2026-06-22.

1. Запустить `.\.venv\Scripts\ofz-gui.exe` и проверить девять вкладок.
2. На вкладке `Обзор` проверить project root, report date и environment action.
3. Подготовить Minfin monthly dry-run без сети; command preview должен содержать `--dry-run --no-network`.
4. Убедиться, что download-кнопки disabled без exact confirm и становятся доступны только с правильным token.
5. На вкладке `Pipeline` проверить sequence stage 0 dry-run -> optional schema -> pipeline.
6. Запустить `Quality fast`; во время выполнения второй action должен быть заблокирован.
7. Открыть charts/reports и quick links monthly weighted yield/monthly metrics. При отсутствии файла должно появиться сообщение `Сначала запустите pipeline`.
8. Подготовить release bundle dry-run; build должен быть disabled без `BUILD_RELEASE_BUNDLE`.
9. Запустить artifact guard и проверить отсутствие staged generated paths.
10. На вкладке `Журнал` проверить live output, exit code, log path, copy/open и stop.
11. Проверить сообщение при simulated/live HTTP 503: raw не изменен.
12. Закрыть GUI и убедиться, что runtime logs остались под ignored `.ofz_launcher/logs/`.

Manual live download, delete outputs, release build и BI build не выполнять без отдельной операционной необходимости.

# Windows launcher OFZ Analytics

`ofz_launcher.ps1` является thin wrapper для Python tkinter entry point `ofz-gui`. Вся UI-логика, allowlist, typed confirmations, streaming output и журнал находятся в `scripts/gui_launcher/`.

## Запуск

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1
```

Headless smoke:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -GuiArgs --smoke
```

Справка wrapper:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/windows_launcher/ofz_launcher.ps1 -Help
```

Wrapper ищет `.venv\Scripts\ofz-gui.exe`, затем optional `dist\ofz-gui.exe`. Если entry point отсутствует, он показывает команду editable install. Произвольные shell-команды wrapper не принимает.

Полная инструкция: [`docs/07_operations/gui_launcher.md`](../../docs/07_operations/gui_launcher.md).

@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
set PROJECT_ROOT=%~dp0
set GUI_EXE=%PROJECT_ROOT%.venv\Scripts\ofz-gui.exe

if not exist "%GUI_EXE%" (
  echo GUI entry point not found: "%GUI_EXE%"
  echo Run: .\.venv\Scripts\python.exe -m pip install -e .
  exit /b 1
)

"%GUI_EXE%" %*
exit /b %ERRORLEVEL%

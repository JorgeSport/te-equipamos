@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0PUBLICAR-TE-EQUIPAMOS.ps1"
) else (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0PUBLICAR-TE-EQUIPAMOS.ps1" -SourcePath "%~1"
)
echo.
pause

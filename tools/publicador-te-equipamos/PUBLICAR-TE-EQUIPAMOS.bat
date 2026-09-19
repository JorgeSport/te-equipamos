@echo off
setlocal
cd /d "%~dp0"

rem Mantener el motor del publicador actualizado antes de cada uso.
set "TE_REMOTE=https://raw.githubusercontent.com/JorgeSport/te-equipamos/main/tools/publicador-te-equipamos/PUBLICAR-TE-EQUIPAMOS.ps1?nocache=%RANDOM%%RANDOM%"
set "TE_TMP=%TEMP%\PUBLICAR-TE-EQUIPAMOS-%RANDOM%%RANDOM%.ps1"
curl.exe -L --fail --silent --show-error -H "Cache-Control: no-cache" "%TE_REMOTE%" -o "%TE_TMP%" >nul 2>&1
if not errorlevel 1 (
  move /y "%TE_TMP%" "%~dp0PUBLICAR-TE-EQUIPAMOS.ps1" >nul
) else (
  if exist "%TE_TMP%" del "%TE_TMP%" >nul 2>&1
  echo [AVISO] No se pudo comprobar una actualizacion. Se usara la version local.
)

if "%~1"=="" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0PUBLICAR-TE-EQUIPAMOS.ps1"
) else (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0PUBLICAR-TE-EQUIPAMOS.ps1" -SourcePath "%~1"
)
echo.
pause

@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "TE_LOCAL=%~dp0PUBLICAR-TE-EQUIPAMOS.ps1"
set "TE_BACKUP_DIR=%~dp0respaldo"
set "TE_BACKUP=%TE_BACKUP_DIR%\PUBLICAR-TE-EQUIPAMOS-ULTIMO-ESTABLE.ps1"
set "TE_REMOTE=https://raw.githubusercontent.com/JorgeSport/te-equipamos/main/tools/publicador-te-equipamos/PUBLICAR-TE-EQUIPAMOS.ps1?nocache=%RANDOM%%RANDOM%"
set "TE_REMOTE_STABLE=https://raw.githubusercontent.com/JorgeSport/te-equipamos/main/tools/publicador-te-equipamos/PUBLICAR-TE-EQUIPAMOS-ESTABLE.ps1?nocache=%RANDOM%%RANDOM%"
set "TE_TMP=%TEMP%\PUBLICAR-TE-EQUIPAMOS-%RANDOM%%RANDOM%.ps1"
set "TE_TMP_STABLE=%TEMP%\PUBLICAR-TE-EQUIPAMOS-ESTABLE-%RANDOM%%RANDOM%.ps1"

if not exist "%TE_BACKUP_DIR%" mkdir "%TE_BACKUP_DIR%" >nul 2>&1

rem 1) Si la copia local actual es valida y aun no existe respaldo, guardarla.
if exist "%TE_LOCAL%" (
  call :ValidatePs1 "%TE_LOCAL%"
  if not errorlevel 1 (
    if not exist "%TE_BACKUP%" copy /y "%TE_LOCAL%" "%TE_BACKUP%" >nul
  )
)

rem 2) Descargar una posible actualizacion, pero NO reemplazar nada hasta validarla.
curl.exe -L --fail --silent --show-error -H "Cache-Control: no-cache" "%TE_REMOTE%" -o "%TE_TMP%" >nul 2>&1
if not errorlevel 1 (
  call :ValidatePs1 "%TE_TMP%"
  if not errorlevel 1 (
    rem Antes de activar la nueva version, conservar la version local valida anterior.
    if exist "%TE_LOCAL%" (
      call :ValidatePs1 "%TE_LOCAL%"
      if not errorlevel 1 copy /y "%TE_LOCAL%" "%TE_BACKUP%" >nul
    )
    move /y "%TE_TMP%" "%TE_LOCAL%" >nul
    echo [OK] Actualizacion del publicador validada antes de activarse.
  ) else (
    del "%TE_TMP%" >nul 2>&1
    echo [AVISO] La actualizacion descargada no es valida. Se conserva la version local.
  )
) else (
  if exist "%TE_TMP%" del "%TE_TMP%" >nul 2>&1
  echo [AVISO] No se pudo comprobar una actualizacion. Se usara la version local.
)

rem 3) Comprobar el motor que se va a ejecutar. Si esta roto, recuperar automaticamente.
if exist "%TE_LOCAL%" (
  call :ValidatePs1 "%TE_LOCAL%"
  if not errorlevel 1 goto :RunPublisher
)

echo [AVISO] La version local no es valida. Intentando recuperar el ultimo respaldo...

if exist "%TE_BACKUP%" (
  call :ValidatePs1 "%TE_BACKUP%"
  if not errorlevel 1 (
    copy /y "%TE_BACKUP%" "%TE_LOCAL%" >nul
    echo [OK] Publicador restaurado desde el respaldo local.
    goto :RunPublisher
  )
)

echo [AVISO] El respaldo local tampoco esta disponible. Recuperando la version estable desde GitHub...
curl.exe -L --fail --silent --show-error -H "Cache-Control: no-cache" "%TE_REMOTE_STABLE%" -o "%TE_TMP_STABLE%" >nul 2>&1
if errorlevel 1 goto :FatalRecovery

call :ValidatePs1 "%TE_TMP_STABLE%"
if errorlevel 1 goto :FatalRecovery

copy /y "%TE_TMP_STABLE%" "%TE_LOCAL%" >nul
copy /y "%TE_TMP_STABLE%" "%TE_BACKUP%" >nul
del "%TE_TMP_STABLE%" >nul 2>&1
echo [OK] Publicador recuperado desde la version estable de GitHub.

:RunPublisher
if "%~1"=="" (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%TE_LOCAL%"
) else (
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%TE_LOCAL%" -SourcePath "%~1"
)
set "TE_EXIT=%ERRORLEVEL%"
echo.
if not "%TE_EXIT%"=="0" (
  echo [AVISO] El publicador termino con codigo %TE_EXIT%. No se sustituiran respaldos por este resultado.
)
pause
exit /b %TE_EXIT%

:ValidatePs1
set "TE_VALIDATE_PATH=%~1"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$tokens=$null;$errors=$null;[System.Management.Automation.Language.Parser]::ParseFile($env:TE_VALIDATE_PATH,[ref]$tokens,[ref]$errors) ^| Out-Null; if($errors.Count -gt 0){ exit 1 } else { exit 0 }" >nul 2>&1
set "TE_VALIDATE_RESULT=%ERRORLEVEL%"
set "TE_VALIDATE_PATH="
exit /b %TE_VALIDATE_RESULT%

:FatalRecovery
if exist "%TE_TMP_STABLE%" del "%TE_TMP_STABLE%" >nul 2>&1
echo.
echo [ERROR] No existe una copia valida del publicador que pueda ejecutarse con seguridad.
echo [ERROR] No se ha publicado ni modificado ningun proyecto.
echo.
echo Abre esta carpeta y conserva los archivos. No publiques manualmente hasta reparar el publicador.
pause
exit /b 1

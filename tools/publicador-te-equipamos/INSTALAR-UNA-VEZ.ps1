$ErrorActionPreference = "Stop"

function Test-Command([string]$Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Install-WingetPackage([string]$Id, [string]$Label) {
    Write-Host ""
    Write-Host "Instalando $Label..." -ForegroundColor Cyan
    & winget install --id $Id -e --source winget --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) {
        throw "No pude instalar $Label con winget."
    }
}

function Convert-ScriptsToUtf8Bom {
    $folder = Split-Path -Parent $MyInvocation.MyCommand.Path
    $encoding = New-Object System.Text.UTF8Encoding($true)
    Get-ChildItem -LiteralPath $folder -Filter "*.ps1" -File | ForEach-Object {
        $text = [System.IO.File]::ReadAllText($_.FullName, [System.Text.Encoding]::UTF8)
        [System.IO.File]::WriteAllText($_.FullName, $text, $encoding)
    }
}

try {
    Write-Host "TE EQUIPAMOS | PREPARACION INICIAL" -ForegroundColor White
    Write-Host "Esto solo se hace una vez en este PC." -ForegroundColor DarkGray

    Convert-ScriptsToUtf8Bom

    if (-not (Test-Command "winget")) {
        throw "No encuentro winget. Actualiza Instalador de aplicaciones desde Microsoft Store y vuelve a intentarlo."
    }

    if (-not (Test-Command "git")) {
        Install-WingetPackage "Git.Git" "Git"
    }
    else {
        Write-Host "[OK] Git ya esta instalado" -ForegroundColor Green
    }

    if (-not (Test-Command "gh")) {
        Install-WingetPackage "GitHub.cli" "GitHub CLI"
    }
    else {
        Write-Host "[OK] GitHub CLI ya esta instalado" -ForegroundColor Green
    }

    $gh = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $gh) {
        $commonGh = "C:\Program Files\GitHub CLI\gh.exe"
        if (Test-Path $commonGh) {
            $ghPath = $commonGh
        }
        else {
            Write-Host ""
            Write-Host "GitHub CLI se instalo, pero Windows todavia no actualizo el PATH de esta ventana." -ForegroundColor Yellow
            Write-Host "Cierra esta ventana, vuelve a ejecutar INSTALAR-UNA-VEZ.bat y continua con el inicio de sesion." -ForegroundColor Yellow
            exit 0
        }
    }
    else {
        $ghPath = $gh.Source
    }

    & $ghPath auth status *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "Ahora GitHub abrira el navegador para autorizar este PC." -ForegroundColor Cyan
        Write-Host "Inicia sesion con tu cuenta JorgeSport y acepta la autorizacion." -ForegroundColor White
        & $ghPath auth login --hostname github.com --git-protocol https --web --scopes "repo,workflow"
        if ($LASTEXITCODE -ne 0) {
            throw "No se completo el inicio de sesion de GitHub CLI."
        }
    }
    else {
        Write-Host "[OK] GitHub CLI ya tiene sesion iniciada" -ForegroundColor Green
        Write-Host "Comprobando permisos para repositorios y workflows..." -ForegroundColor Cyan
        & $ghPath auth refresh --hostname github.com --scopes "repo,workflow"
        if ($LASTEXITCODE -ne 0) {
            throw "No se pudieron confirmar los permisos repo y workflow de GitHub CLI."
        }
    }

    Write-Host ""
    Write-Host "CONFIGURACION COMPLETADA" -ForegroundColor Green
    Write-Host "A partir de ahora usa PUBLICAR-TE-EQUIPAMOS.bat para cada landing nueva." -ForegroundColor White
}
catch {
    Write-Host ""
    Write-Host "CONFIGURACION DETENIDA" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    exit 1
}

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

function Resolve-GhPath {
    $command = Get-Command gh -ErrorAction SilentlyContinue
    if ($command -and -not [string]::IsNullOrWhiteSpace([string]$command.Source)) {
        return [string]$command.Source
    }

    $candidates = @(
        "C:\Program Files\GitHub CLI\gh.exe",
        "C:\Program Files (x86)\GitHub CLI\gh.exe",
        (Join-Path $env:LOCALAPPDATA "Programs\GitHub CLI\gh.exe")
    )

    foreach ($candidate in $candidates) {
        if (-not [string]::IsNullOrWhiteSpace($candidate) -and (Test-Path -LiteralPath $candidate)) {
            return $candidate
        }
    }

    return $null
}

try {
    Write-Host "TE EQUIPAMOS | PREPARACION INICIAL" -ForegroundColor White
    Write-Host "Esto solo se hace una vez en este PC." -ForegroundColor DarkGray

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
        $existingGh = Resolve-GhPath
        if (-not $existingGh) {
            Install-WingetPackage "GitHub.cli" "GitHub CLI"
        }
        else {
            Write-Host "[OK] GitHub CLI ya esta instalado" -ForegroundColor Green
        }
    }
    else {
        Write-Host "[OK] GitHub CLI ya esta instalado" -ForegroundColor Green
    }

    $ghPath = Resolve-GhPath
    if ([string]::IsNullOrWhiteSpace($ghPath)) {
        Write-Host ""
        Write-Host "GitHub CLI se instalo, pero Windows todavia no actualizo sus rutas." -ForegroundColor Yellow
        Write-Host "Cierra esta ventana y vuelve a ejecutar INSTALAR-UNA-VEZ.bat." -ForegroundColor Yellow
        exit 0
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

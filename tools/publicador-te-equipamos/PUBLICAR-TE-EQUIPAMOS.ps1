param(
    [Parameter(Mandatory = $false)]
    [string]$SourcePath,

    [Parameter(Mandatory = $false)]
    [string]$RepoName,

    [string]$Owner = "JorgeSport",
    [string]$HubRepo = "JorgeSport/te-equipamos"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Write-Step([string]$Text) {
    Write-Host ""
    Write-Host "==> $Text" -ForegroundColor Cyan
}

function Write-Ok([string]$Text) {
    Write-Host "[OK] $Text" -ForegroundColor Green
}

function Stop-Publish([string]$Text) {
    throw $Text
}

function Test-Command([string]$Name) {
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Get-ProjectRoot([string]$Path) {
    if ((Test-Path (Join-Path $Path "index.html")) -and (Test-Path (Join-Path $Path "te-equipamos.json"))) {
        return (Resolve-Path $Path).Path
    }

    $matches = @(Get-ChildItem -LiteralPath $Path -Directory -ErrorAction SilentlyContinue | Where-Object {
        (Test-Path (Join-Path $_.FullName "index.html")) -and (Test-Path (Join-Path $_.FullName "te-equipamos.json"))
    })

    if ($matches.Count -eq 1) {
        return $matches[0].FullName
    }

    Stop-Publish "No encuentro una raíz única de landing con index.html y te-equipamos.json."
}

function Get-StableId([string]$Value) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Value)
        $hash = $sha.ComputeHash($bytes)
        $id = [BitConverter]::ToUInt32($hash, 0)
        if ($id -eq 0) { $id = 1 }
        return [uint32]$id
    }
    finally {
        $sha.Dispose()
    }
}

function Test-StrategicManifest([string]$ManifestPath, [string]$ExpectedRepoName) {
    $raw = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8
    try {
        $manifest = $raw | ConvertFrom-Json
    }
    catch {
        Stop-Publish "te-equipamos.json no es JSON válido."
    }

    if (-not $manifest.brand -or $manifest.brand -ne "Te Equipamos") {
        Stop-Publish "te-equipamos.json debe declarar brand = Te Equipamos."
    }

    if (-not $manifest.schema_version -or [int]$manifest.schema_version -lt 3) {
        Stop-Publish "La landing usa un esquema antiguo. Debe tener schema_version 3."
    }

    if (-not $manifest.items -or @($manifest.items).Count -lt 1) {
        Stop-Publish "te-equipamos.json no contiene ningún producto."
    }

    $item = @($manifest.items)[0]
    $expectedUrl = "https://$($Owner.ToLower()).github.io/$ExpectedRepoName/"

    # Automatizaciones seguras que no alteran el copy creativo.
    [uint32]$idValue = 0
    $hasNumericId = [uint32]::TryParse([string]$item.id, [ref]$idValue)
    if (-not $hasNumericId -or $idValue -eq 0) {
        $item.id = Get-StableId "$Owner/$ExpectedRepoName|$($item.title)"
    }

    $item.url = $expectedUrl

    $dateValue = [datetime]::MinValue
    $validDate = [datetime]::TryParse([string]$item.published_at, [ref]$dateValue)
    if (-not $validDate -or [string]$item.published_at -match '^REEMPLAZAR_') {
        $item.published_at = Get-Date -Format "yyyy-MM-dd"
    }

    $cardTitle = [string]$item.card_title
    $summary = [string]$item.summary
    $seoTitle = [string]$item.seo_title
    $seoDescription = [string]$item.seo_description
    $keywords = @($item.seo_keywords)

    if ([string]::IsNullOrWhiteSpace($cardTitle) -or $cardTitle -match 'REEMPLAZAR_') {
        Stop-Publish "Falta el título estratégico del Hub (card_title). Créalo antes de publicar."
    }
    if ($cardTitle.Length -lt 35 -or $cardTitle.Length -gt 95) {
        Stop-Publish "card_title debe tener entre 35 y 95 caracteres. Actual: $($cardTitle.Length)."
    }
    if ([string]::IsNullOrWhiteSpace($summary) -or $summary -match 'REEMPLAZAR_') {
        Stop-Publish "Falta el subtítulo estratégico del Hub (summary). Créalo antes de publicar."
    }
    if ([string]::IsNullOrWhiteSpace($seoTitle) -or $seoTitle -match 'REEMPLAZAR_') {
        Stop-Publish "Falta seo_title."
    }
    if ($seoTitle.Length -lt 35 -or $seoTitle.Length -gt 75) {
        Stop-Publish "seo_title debe tener entre 35 y 75 caracteres. Actual: $($seoTitle.Length)."
    }
    if ([string]::IsNullOrWhiteSpace($seoDescription) -or $seoDescription -match 'REEMPLAZAR_') {
        Stop-Publish "Falta seo_description."
    }
    if ($seoDescription.Length -lt 90 -or $seoDescription.Length -gt 180) {
        Stop-Publish "seo_description debe tener entre 90 y 180 caracteres. Actual: $($seoDescription.Length)."
    }
    if ($keywords.Count -lt 3 -or $keywords.Count -gt 8) {
        Stop-Publish "seo_keywords debe contener entre 3 y 8 términos."
    }

    $normalized = $manifest | ConvertTo-Json -Depth 20
    if ($normalized -match 'REEMPLAZAR_') {
        Stop-Publish "El manifiesto todavía contiene campos REEMPLAZAR_. Completa la landing antes de publicar."
    }

    $normalized | Set-Content -LiteralPath $ManifestPath -Encoding UTF8
    return $expectedUrl
}

function Wait-ForWorkflow([string]$Repository, [string]$Workflow, [string]$Event = "workflow_dispatch") {
    Start-Sleep -Seconds 3
    $runId = & gh run list --repo $Repository --workflow $Workflow --event $Event --limit 1 --json databaseId --jq '.[0].databaseId'
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($runId)) {
        Stop-Publish "No pude localizar la ejecución de $Workflow en $Repository."
    }

    Write-Host "Esperando GitHub Actions (run $runId)..."
    & gh run watch $runId --repo $Repository --exit-status
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "GitHub Actions falló en $Repository. Revisa la pestaña Acciones."
    }
}

function Enable-Pages([string]$Repository) {
    & gh api "repos/$Repository/pages" *> $null
    if ($LASTEXITCODE -eq 0) {
        & gh api --method PUT "repos/$Repository/pages" -f build_type=workflow *> $null
        if ($LASTEXITCODE -ne 0) {
            Stop-Publish "No pude configurar GitHub Pages para usar Actions en $Repository."
        }
    }
    else {
        & gh api --method POST "repos/$Repository/pages" -f build_type=workflow *> $null
        if ($LASTEXITCODE -ne 0) {
            Stop-Publish "No pude activar GitHub Pages en $Repository."
        }
    }
}

$tempRoot = $null
$originalLocation = Get-Location

try {
    Write-Host "TE EQUIPAMOS | PUBLICADOR AUTOMÁTICO" -ForegroundColor White
    Write-Host "Repositorio + Pages + Hub, en un solo proceso" -ForegroundColor DarkGray

    Write-Step "Comprobando herramientas"
    if (-not (Test-Command "git")) {
        Stop-Publish "Falta Git. Ejecuta primero INSTALAR-UNA-VEZ.bat."
    }
    if (-not (Test-Command "gh")) {
        Stop-Publish "Falta GitHub CLI. Ejecuta primero INSTALAR-UNA-VEZ.bat."
    }

    & gh auth status *> $null
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "GitHub CLI no está autenticado. Ejecuta INSTALAR-UNA-VEZ.bat o 'gh auth login --web'."
    }
    Write-Ok "Git y GitHub CLI listos"

    if ([string]::IsNullOrWhiteSpace($SourcePath)) {
        $SourcePath = Read-Host "Pega la ruta de la carpeta o ZIP de la landing"
    }
    $SourcePath = $SourcePath.Trim('"')
    if (-not (Test-Path -LiteralPath $SourcePath)) {
        Stop-Publish "No existe la ruta: $SourcePath"
    }

    Write-Step "Preparando la landing"
    $resolvedSource = (Resolve-Path -LiteralPath $SourcePath).Path
    if ([System.IO.Path]::GetExtension($resolvedSource).ToLowerInvariant() -eq ".zip") {
        $tempRoot = Join-Path $env:TEMP ("te-equipamos-publish-" + [guid]::NewGuid().ToString("N"))
        New-Item -ItemType Directory -Path $tempRoot | Out-Null
        Expand-Archive -LiteralPath $resolvedSource -DestinationPath $tempRoot -Force
        $projectRoot = Get-ProjectRoot $tempRoot
    }
    else {
        $projectRoot = Get-ProjectRoot $resolvedSource
    }
    Write-Ok "Proyecto detectado: $projectRoot"

    $manifestPath = Join-Path $projectRoot "te-equipamos.json"

    if ([string]::IsNullOrWhiteSpace($RepoName)) {
        try {
            $probe = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
            $candidateUrl = [string](@($probe.items)[0].url)
            if ($candidateUrl -match 'github\.io/([^/]+)/?') {
                $candidate = $Matches[1]
                if ($candidate -and $candidate -notmatch '^REEMPLAZAR_') {
                    $RepoName = $candidate
                }
            }
        }
        catch { }
    }

    if ([string]::IsNullOrWhiteSpace($RepoName)) {
        $RepoName = Read-Host "Nombre del repositorio (ejemplo: te-equipamos-producto-xyz)"
    }
    $RepoName = $RepoName.Trim()

    if ($RepoName -notmatch '^[A-Za-z0-9._-]+$') {
        Stop-Publish "El nombre del repositorio contiene caracteres no válidos."
    }

    $requiredFiles = @(
        "index.html",
        "te-equipamos.json",
        ".github/workflows/pages.yml"
    )
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path -LiteralPath (Join-Path $projectRoot $file))) {
            Stop-Publish "Falta el archivo obligatorio: $file"
        }
    }

    Write-Step "Validando título, subtítulo, SEO y esquema del Hub"
    $siteUrl = Test-StrategicManifest $manifestPath $RepoName
    Write-Ok "Manifiesto schema 3 correcto"

    $fullRepo = "$Owner/$RepoName"
    & gh repo view $fullRepo --json nameWithOwner *> $null
    if ($LASTEXITCODE -eq 0) {
        Stop-Publish "El repositorio $fullRepo ya existe. Por seguridad, este publicador automático solo crea landings nuevas."
    }

    Write-Step "Creando el repositorio público $fullRepo"
    Set-Location $projectRoot

    if (Test-Path -LiteralPath (Join-Path $projectRoot ".git")) {
        Remove-Item -LiteralPath (Join-Path $projectRoot ".git") -Recurse -Force
    }

    & git init -b main *> $null
    if ($LASTEXITCODE -ne 0) {
        & git init *> $null
        & git branch -M main *> $null
    }

    $gitUser = (& git config user.name)
    if ([string]::IsNullOrWhiteSpace($gitUser)) {
        & git config user.name $Owner
    }
    $gitEmail = (& git config user.email)
    if ([string]::IsNullOrWhiteSpace($gitEmail)) {
        & git config user.email "$Owner@users.noreply.github.com"
    }

    & git add -A
    & git commit -m "Publicar landing Te Equipamos: $RepoName" *> $null
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "No pude crear el commit inicial."
    }

    & gh repo create $fullRepo --public --source . --remote origin --push
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "No pude crear o subir el repositorio $fullRepo."
    }
    Write-Ok "Repositorio público creado y código subido"

    Write-Step "Activando GitHub Pages con Acciones de GitHub"
    Enable-Pages $fullRepo
    Write-Ok "GitHub Pages habilitado"

    Write-Step "Publicando la landing"
    & gh workflow run pages.yml --repo $fullRepo
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "No pude iniciar el workflow pages.yml en $fullRepo."
    }
    Wait-ForWorkflow $fullRepo "pages.yml"
    Write-Ok "Landing publicada"

    Write-Step "Actualizando el Hub principal de Te Equipamos"
    Start-Sleep -Seconds 4
    & gh workflow run pages.yml --repo $HubRepo
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "La landing ya está publicada, pero no pude lanzar la actualización del Hub $HubRepo."
    }
    Wait-ForWorkflow $HubRepo "pages.yml"
    Write-Ok "Hub actualizado"

    Write-Host ""
    Write-Host "PUBLICACIÓN COMPLETADA" -ForegroundColor Green
    Write-Host "Landing: $siteUrl" -ForegroundColor White
    Write-Host "Hub: https://jorgesport.github.io/te-equipamos/" -ForegroundColor White
    Write-Host "Repositorio: https://github.com/$fullRepo" -ForegroundColor White

    try { Start-Process $siteUrl } catch { }
}
catch {
    Write-Host ""
    Write-Host "PUBLICACIÓN DETENIDA" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host ""
    Write-Host "No se ha continuado para evitar publicar una landing incompleta." -ForegroundColor DarkGray
    exit 1
}
finally {
    try { Set-Location $originalLocation } catch { }
    if ($tempRoot -and (Test-Path -LiteralPath $tempRoot)) {
        try { Remove-Item -LiteralPath $tempRoot -Recurse -Force } catch { }
    }
}

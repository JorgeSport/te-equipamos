param(
    [Parameter(Mandatory = $false)]
    [string]$SourcePath,

    [Parameter(Mandatory = $false)]
    [string]$RepoName,

    [string]$Owner = "JorgeSport",
    [string]$HubRepo = "JorgeSport/te-equipamos"
)

$PublisherVersion = "2026.09.20.3"

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

# Ejecuta comandos externos que pueden fallar como parte normal de una comprobacion.
# Evita que PowerShell convierta el stderr esperado de GitHub CLI en una excepcion.
function Invoke-QuietExitCode([scriptblock]$Command) {
    $previousPreference = $ErrorActionPreference
    try {
        $ErrorActionPreference = "Continue"
        & $Command *> $null
        return $LASTEXITCODE
    }
    catch {
        return 1
    }
    finally {
        $ErrorActionPreference = $previousPreference
    }
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

    Stop-Publish "No encuentro una raiz unica de landing con index.html y te-equipamos.json."
}

function Get-JsonPropertyValue($Object, [string]$Name) {
    if ($null -eq $Object) { return $null }
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) { return $null }
    return $property.Value
}

function Set-JsonPropertyValue($Object, [string]$Name, $Value) {
    if ($null -eq $Object) {
        Stop-Publish "No se puede escribir '$Name' porque el objeto JSON no existe."
    }

    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        $Object | Add-Member -MemberType NoteProperty -Name $Name -Value $Value
    }
    else {
        $property.Value = $Value
    }
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
        Stop-Publish "te-equipamos.json no es JSON valido."
    }

    $brand = [string](Get-JsonPropertyValue $manifest "brand")
    if ([string]::IsNullOrWhiteSpace($brand) -or $brand -ne "Te Equipamos") {
        Stop-Publish "te-equipamos.json debe declarar brand = Te Equipamos."
    }

    $schemaVersion = Get-JsonPropertyValue $manifest "schema_version"
    if ($null -eq $schemaVersion -or [int]$schemaVersion -lt 3) {
        Stop-Publish "La landing usa un esquema antiguo. Debe tener schema_version 3."
    }

    $itemsValue = Get-JsonPropertyValue $manifest "items"
    if ($null -eq $itemsValue -or @($itemsValue).Count -lt 1) {
        Stop-Publish "te-equipamos.json no contiene ningun producto."
    }

    $item = @($itemsValue)[0]
    $expectedUrl = "https://$($Owner.ToLower()).github.io/$ExpectedRepoName/"

    # Automatizaciones seguras que no alteran el copy creativo.
    # id, url y published_at pueden faltar: el publicador los normaliza.
    [uint32]$idValue = 0
    $currentId = Get-JsonPropertyValue $item "id"
    $hasNumericId = [uint32]::TryParse([string]$currentId, [ref]$idValue)
    if (-not $hasNumericId -or $idValue -eq 0) {
        $titleForId = [string](Get-JsonPropertyValue $item "title")
        $generatedId = Get-StableId "$Owner/$ExpectedRepoName|$titleForId"
        Set-JsonPropertyValue $item "id" $generatedId
    }

    Set-JsonPropertyValue $item "url" $expectedUrl

    $publishedAt = Get-JsonPropertyValue $item "published_at"
    $dateValue = [datetime]::MinValue
    $validDate = [datetime]::TryParse([string]$publishedAt, [ref]$dateValue)
    if (-not $validDate -or [string]$publishedAt -match '^REEMPLAZAR_') {
        Set-JsonPropertyValue $item "published_at" (Get-Date -Format "yyyy-MM-dd")
    }

    $cardTitle = [string](Get-JsonPropertyValue $item "card_title")
    $summary = [string](Get-JsonPropertyValue $item "summary")
    $seoTitle = [string](Get-JsonPropertyValue $item "seo_title")
    $seoDescription = [string](Get-JsonPropertyValue $item "seo_description")
    $keywordsValue = Get-JsonPropertyValue $item "seo_keywords"
    $keywords = @($keywordsValue)

    if ([string]::IsNullOrWhiteSpace($cardTitle) -or $cardTitle -match 'REEMPLAZAR_') {
        Stop-Publish "Falta el titulo estrategico del Hub (card_title). Crealo antes de publicar."
    }
    if ($cardTitle.Length -lt 35 -or $cardTitle.Length -gt 95) {
        Stop-Publish "card_title debe tener entre 35 y 95 caracteres. Actual: $($cardTitle.Length)."
    }
    if ([string]::IsNullOrWhiteSpace($summary) -or $summary -match 'REEMPLAZAR_') {
        Stop-Publish "Falta el subtitulo estrategico del Hub (summary). Crealo antes de publicar."
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
    if ($null -eq $keywordsValue -or $keywords.Count -lt 3 -or $keywords.Count -gt 8) {
        Stop-Publish "seo_keywords debe contener entre 3 y 8 terminos."
    }

    $normalized = $manifest | ConvertTo-Json -Depth 20
    if ($normalized -match 'REEMPLAZAR_') {
        Stop-Publish "El manifiesto todavia contiene campos REEMPLAZAR_. Completa la landing antes de publicar."
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($ManifestPath, $normalized, $utf8NoBom)
    return $expectedUrl
}

function Normalize-SocialStrategy([string]$HtmlPath, [string]$ManifestPath) {
    $html = Get-Content -LiteralPath $HtmlPath -Raw -Encoding UTF8
    $manifestRaw = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8

    try {
        $manifest = $manifestRaw | ConvertFrom-Json
    }
    catch {
        Stop-Publish "No pude leer te-equipamos.json para preparar los metadatos sociales."
    }

    $item = @((Get-JsonPropertyValue $manifest "items"))[0]
    if ($null -eq $item) {
        Stop-Publish "No hay un item valido para preparar los metadatos sociales."
    }

    $cardTitle = [string](Get-JsonPropertyValue $item "card_title")
    $fallbackTitle = [string](Get-JsonPropertyValue $item "title")
    $summary = [string](Get-JsonPropertyValue $item "summary")
    $image = [string](Get-JsonPropertyValue $item "image")
    $url = [string](Get-JsonPropertyValue $item "url")

    $socialTitle = $cardTitle.Trim()
    if ([string]::IsNullOrWhiteSpace($socialTitle)) {
        $socialTitle = $fallbackTitle.Trim()
    }
    if ([string]::IsNullOrWhiteSpace($socialTitle)) {
        Stop-Publish "No existe un titulo estrategico para redes sociales."
    }

    $socialDescription = $summary.Trim()
    if ([string]::IsNullOrWhiteSpace($socialDescription)) {
        $socialDescription = [string](Get-JsonPropertyValue $item "seo_description")
        $socialDescription = $socialDescription.Trim()
    }

    $encodedTitle = [System.Net.WebUtility]::HtmlEncode($socialTitle)
    $encodedDescription = [System.Net.WebUtility]::HtmlEncode($socialDescription)
    $encodedImage = [System.Net.WebUtility]::HtmlEncode($image.Trim())
    $encodedUrl = [System.Net.WebUtility]::HtmlEncode($url.Trim())

    function Set-MetaProperty([string]$Source, [string]$Property, [string]$Value) {
        if ([string]::IsNullOrWhiteSpace($Value)) { return $Source }
        $pattern = '<meta\s+property=["'']' + [regex]::Escape($Property) + '["''][^>]*>'
        $replacement = '<meta property="' + $Property + '" content="' + $Value + '">'
        if ([regex]::IsMatch($Source, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)) {
            return [regex]::Replace($Source, $pattern, $replacement, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
        }
        return $Source -replace '</head>', ("  " + $replacement + [Environment]::NewLine + "</head>")
    }

    function Set-MetaName([string]$Source, [string]$Name, [string]$Value) {
        if ([string]::IsNullOrWhiteSpace($Value)) { return $Source }
        $pattern = '<meta\s+name=["'']' + [regex]::Escape($Name) + '["''][^>]*>'
        $replacement = '<meta name="' + $Name + '" content="' + $Value + '">'
        if ([regex]::IsMatch($Source, $pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)) {
            return [regex]::Replace($Source, $pattern, $replacement, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
        }
        return $Source -replace '</head>', ("  " + $replacement + [Environment]::NewLine + "</head>")
    }

    $html = Set-MetaProperty $html "og:title" $encodedTitle
    $html = Set-MetaProperty $html "og:description" $encodedDescription
    if (-not [string]::IsNullOrWhiteSpace($encodedImage)) {
        $html = Set-MetaProperty $html "og:image" $encodedImage
    }
    if (-not [string]::IsNullOrWhiteSpace($encodedUrl)) {
        $html = Set-MetaProperty $html "og:url" $encodedUrl
    }

    $html = Set-MetaName $html "twitter:card" "summary_large_image"
    $html = Set-MetaName $html "twitter:title" $encodedTitle
    $html = Set-MetaName $html "twitter:description" $encodedDescription
    if (-not [string]::IsNullOrWhiteSpace($encodedImage)) {
        $html = Set-MetaName $html "twitter:image" $encodedImage
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($HtmlPath, $html, $utf8NoBom)
}

function Normalize-PriceSystem([string]$HtmlPath) {
    $html = Get-Content -LiteralPath $HtmlPath -Raw -Encoding UTF8

    $priceMatch = [regex]::Match(
        $html,
        '<meta\s+name=["'']te:price["''][^>]*content=["'']([^"'']*)["''][^>]*>',
        [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
    )

    if (-not $priceMatch.Success) {
        return
    }

    $priceValue = $priceMatch.Groups[1].Value.Trim()
    if ([string]::IsNullOrWhiteSpace($priceValue) -or $priceValue -match 'REEMPLAZAR_') {
        return
    }

    if ($html -notmatch 'landing-core\.js') {
        Stop-Publish "La landing tiene precio, pero falta el nucleo central landing-core.js."
    }

    if ($html -notmatch 'data-te-price') {
        Stop-Publish "La landing tiene precio, pero falta data-te-price en el bloque visual del precio."
    }

    $today = Get-Date -Format "yyyy-MM-dd"
    $updatedMetaPattern = '<meta\s+name=["'']te:price-updated["''][^>]*>'
    $updatedMeta = '<meta name="te:price-updated" content="' + $today + '">'

    if ([regex]::IsMatch($html, $updatedMetaPattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)) {
        $html = [regex]::Replace(
            $html,
            $updatedMetaPattern,
            $updatedMeta,
            [System.Text.RegularExpressions.RegexOptions]::IgnoreCase
        )
    }
    elseif ($html -match '</head>') {
        $html = $html -replace '</head>', ("  " + $updatedMeta + [Environment]::NewLine + "</head>")
    }
    else {
        Stop-Publish "No pude registrar la fecha de actualizacion del precio porque falta </head>."
    }

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($HtmlPath, $html, $utf8NoBom)
}

function Wait-ForWorkflow([string]$Repository, [string]$Workflow, [string]$Event = "workflow_dispatch") {
    Start-Sleep -Seconds 3
    $runId = & gh run list --repo $Repository --workflow $Workflow --event $Event --limit 1 --json databaseId --jq '.[0].databaseId'
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($runId)) {
        Stop-Publish "No pude localizar la ejecucion de $Workflow en $Repository."
    }

    Write-Host "Esperando GitHub Actions (run $runId)..."
    & gh run watch $runId --repo $Repository --exit-status
    if ($LASTEXITCODE -ne 0) {
        Stop-Publish "GitHub Actions fallo en $Repository. Revisa la pestana Acciones."
    }
}

function Enable-Pages([string]$Repository) {
    $pagesExists = Invoke-QuietExitCode { & gh api "repos/$Repository/pages" }
    if ($pagesExists -eq 0) {
        $configurePages = Invoke-QuietExitCode { & gh api --method PUT "repos/$Repository/pages" -f build_type=workflow }
        if ($configurePages -ne 0) {
            Stop-Publish "No pude configurar GitHub Pages para usar Actions en $Repository."
        }
    }
    else {
        $createPages = Invoke-QuietExitCode { & gh api --method POST "repos/$Repository/pages" -f build_type=workflow }
        if ($createPages -ne 0) {
            Stop-Publish "No pude activar GitHub Pages en $Repository."
        }
    }
}

$tempRoot = $null
$originalLocation = Get-Location

try {
    Write-Host "TE EQUIPAMOS | PUBLICADOR AUTOMATICO" -ForegroundColor White
    Write-Host "Repositorio + Pages + Hub, en un solo proceso" -ForegroundColor DarkGray
    Write-Host "Motor: $PublisherVersion" -ForegroundColor DarkGray

    Write-Step "Comprobando herramientas"
    if (-not (Test-Command "git")) {
        Stop-Publish "Falta Git. Ejecuta primero INSTALAR-UNA-VEZ.bat."
    }
    if (-not (Test-Command "gh")) {
        Stop-Publish "Falta GitHub CLI. Ejecuta primero INSTALAR-UNA-VEZ.bat."
    }

    $authExit = Invoke-QuietExitCode { & gh auth status }
    if ($authExit -ne 0) {
        Stop-Publish "GitHub CLI no esta autenticado. Ejecuta INSTALAR-UNA-VEZ.bat o 'gh auth login --web'."
    }
    Write-Ok "Git y GitHub CLI listos"

    if ([string]::IsNullOrWhiteSpace($SourcePath)) {
        $SourcePath = Read-Host "Pega la ruta de la carpeta o ZIP de la landing"
    }
    $SourcePath = $SourcePath.Trim('"')
    if (-not (Test-Path -LiteralPath $SourcePath)) {
        Stop-Publish "No existe la ruta: $SourcePath"
    }

    Write-Step "Preparando una copia temporal de la landing"
    $resolvedSource = (Resolve-Path -LiteralPath $SourcePath).Path
    $tempRoot = Join-Path $env:TEMP ("te-equipamos-publish-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempRoot | Out-Null

    if ([System.IO.Path]::GetExtension($resolvedSource).ToLowerInvariant() -eq ".zip") {
        Expand-Archive -LiteralPath $resolvedSource -DestinationPath $tempRoot -Force
        $projectRoot = Get-ProjectRoot $tempRoot
    }
    else {
        $copyRoot = Join-Path $tempRoot "project"
        New-Item -ItemType Directory -Path $copyRoot | Out-Null
        Get-ChildItem -LiteralPath $resolvedSource -Force | Where-Object { $_.Name -ne ".git" } | ForEach-Object {
            Copy-Item -LiteralPath $_.FullName -Destination $copyRoot -Recurse -Force
        }
        $projectRoot = Get-ProjectRoot $copyRoot
    }
    Write-Ok "Copia de trabajo preparada: $projectRoot"

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
        Stop-Publish "El nombre del repositorio contiene caracteres no validos."
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

    Write-Step "Normalizando aviso y fecha del precio"
    Normalize-PriceSystem (Join-Path $projectRoot "index.html")
    Write-Ok "Sistema de precio correcto"

    Write-Step "Validando titulo, subtitulo, SEO y esquema del Hub"
    $siteUrl = Test-StrategicManifest $manifestPath $RepoName
    Write-Ok "Manifiesto schema 3 correcto"

    Write-Step "Preparando titulo estrategico para redes sociales"
    Normalize-SocialStrategy (Join-Path $projectRoot "index.html") $manifestPath
    Write-Ok "Open Graph y Twitter usan el titulo estrategico del Hub"

    $fullRepo = "$Owner/$RepoName"
    $repoExists = Invoke-QuietExitCode { & gh repo view $fullRepo --json nameWithOwner }
    if ($repoExists -eq 0) {
        Stop-Publish "El repositorio $fullRepo ya existe. Por seguridad, este publicador automatico solo crea landings nuevas."
    }
    Write-Ok "Nombre de repositorio disponible"

    Write-Step "Creando el repositorio publico $fullRepo"
    Set-Location $projectRoot

    $gitInitExit = Invoke-QuietExitCode { & git init -b main }
    if ($gitInitExit -ne 0) {
        $gitInitFallback = Invoke-QuietExitCode { & git init }
        if ($gitInitFallback -ne 0) {
            Stop-Publish "No pude inicializar Git en la copia temporal."
        }
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
    Write-Ok "Repositorio publico creado y codigo subido"

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
        Stop-Publish "La landing ya esta publicada, pero no pude lanzar la actualizacion del Hub $HubRepo."
    }
    Wait-ForWorkflow $HubRepo "pages.yml"
    Write-Ok "Hub actualizado"

    Write-Step "Sincronizando la Fabrica y el Centro de Control"
    $privateControlRepo = "JorgeSport/te-equipamos-prompts"

    $factorySyncExit = Invoke-QuietExitCode { & gh workflow run fabrica-sync.yml --repo $privateControlRepo }
    if ($factorySyncExit -eq 0) {
        Write-Ok "Sincronizacion de la Fabrica solicitada"
    }
    else {
        Write-Host "[AVISO] La landing esta publicada, pero no pude lanzar la sincronizacion de la Fabrica." -ForegroundColor Yellow
    }

    $controlSyncExit = Invoke-QuietExitCode { & gh workflow run control-te-equipamos.yml --repo $privateControlRepo }
    if ($controlSyncExit -eq 0) {
        Write-Ok "Revision del Centro de Control solicitada"
    }
    else {
        Write-Host "[AVISO] La landing esta publicada, pero no pude lanzar el Centro de Control." -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "PUBLICACION COMPLETADA" -ForegroundColor Green
    Write-Host "Landing: $siteUrl" -ForegroundColor White
    Write-Host "Hub: https://jorgesport.github.io/te-equipamos/" -ForegroundColor White
    Write-Host "Repositorio: https://github.com/$fullRepo" -ForegroundColor White

    # No abrir el navegador automaticamente. El lanzador deja las URLs visibles.
}
catch {
    Write-Host ""
    Write-Host "PUBLICACION DETENIDA" -ForegroundColor Red
    $errorMessage = "Error desconocido."
    if ($Error.Count -gt 0 -and $null -ne $Error[0].Exception) {
        $errorMessage = $Error[0].Exception.Message
    }
    Write-Host $errorMessage -ForegroundColor Yellow
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

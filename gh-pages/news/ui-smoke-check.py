from pathlib import Path

root = Path(__file__).resolve().parent.parent
index = root / 'index.html'
newsletter_css = root / 'newsletter.css'
newsletter_js = root / 'newsletter.js'
footer_js = root / 'universal-footer.js'

errors = []

for path in [index, newsletter_css, newsletter_js, footer_js]:
    if not path.exists():
        errors.append(f'Falta archivo final: {path.name}')

if not errors:
    html = index.read_text(encoding='utf-8', errors='replace')
    css = newsletter_css.read_text(encoding='utf-8', errors='replace')
    njs = newsletter_js.read_text(encoding='utf-8', errors='replace')
    fjs = footer_js.read_text(encoding='utf-8', errors='replace')

    for marker, label in [
        ('id="tePremiumHeader"', 'cabecera premium'),
        ('--te-header-bg:rgba(250,250,248,.88)', 'cabecera clara transparente'),
        ('display:inline-flex!important;align-items:center!important;width:auto!important', 'marca visible en móvil y escritorio'),
        ('id="teDesktopQuickNav"', 'navegación superior'),
        ('Te Equipamos</span>', 'marca completa'),
    ]:
        if marker not in html:
            errors.append(f'No está activo: {label}')

    if '--te-header-bg:#2A2D2A' in html:
        errors.append('La cabecera oscura antigua volvió al artefacto final')
    if 'api.github.com/users/JorgeSport/repos' in html:
        errors.append('Sigue activa una consulta GitHub en navegador que puede devolver 403')

    if 'data-te-premium-slider-style>\\n' in html:
        errors.append('Hay texto residual \\n después del CSS del slider')
    if 'data-te-premium-slider></script>\\n' in html:
        errors.append('Hay texto residual \\n después del JS del slider')

    for marker, label in [
        ('width:100%;\n  margin:0;\n  padding:56px 24px', 'newsletter full-width'),
        ('@media(max-width:520px)', 'newsletter móvil'),
    ]:
        if marker not in css:
            errors.append(f'No está activo: {label}')

    if 'placeBeforeFooter' not in njs or '#teBusinessFooter,footer' not in njs:
        errors.append('La newsletter no está fijada antes del footer del Hub')

    for marker, label in [
        ('id="teBusinessFooter"', 'footer del Hub'),
        ('background:#E6E6E2', 'footer gris'),
        ('width:100%', 'footer a ancho completo'),
        ('text-align:center', 'footer centrado'),
    ]:
        if marker not in html:
            errors.append(f'No está activo: {label}')

    for marker, label in [
        ('document.body.appendChild(universal)', 'footer universal al final del body'),
        ('text-align:center', 'footer universal centrado'),
        (':host{display:block;clear:both;width:100%', 'footer universal full-width'),
    ]:
        if marker not in fjs:
            errors.append(f'No está activo: {label}')

if errors:
    print('Errores de interfaz final:')
    for error in errors:
        print(' - ' + error)
    raise SystemExit(1)

print('UI SMOKE CHECK OK · marca visible · sin texto residual · newsletter antes del footer · footer responsive')

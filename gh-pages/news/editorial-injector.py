from pathlib import Path

news_dir = Path(__file__).resolve().parent
root = news_dir.parent
index = news_dir / 'index.html'
html = index.read_text(encoding='utf-8')

editorial_css = '<link id="teEditorialExperienceCss" rel="stylesheet" href="/te-equipamos-arpenaz-27l/news/editorial-experience.css?v=1">'
editorial_js = '<script id="teEditorialExperienceJs" src="/te-equipamos-arpenaz-27l/news/editorial-experience.js?v=1"></script>'
if 'id="teEditorialExperienceCss"' not in html and '</head>' in html:
    html = html.replace('</head>', editorial_css + '</head>', 1)
if 'id="teEditorialExperienceJs"' not in html and '</body>' in html:
    html = html.replace('</body>', editorial_js + '</body>', 1)
index.write_text(html, encoding='utf-8')

progress_css = '<link id="teReadingProgressCss" rel="stylesheet" href="/te-equipamos-arpenaz-27l/reading-progress.css?v=1">'
progress_js = '<script id="teReadingProgressJs" src="/te-equipamos-arpenaz-27l/reading-progress.js?v=1"></script>'
skip_roots = {'news', 'studio', 'kalenji'}
updated = 0
for page in root.rglob('index.html'):
    if page == index or page == root / 'index.html':
        continue
    rel = page.relative_to(root)
    if rel.parts and rel.parts[0] in skip_roots:
        continue
    text = page.read_text(encoding='utf-8')
    changed = False
    if 'id="teReadingProgressCss"' not in text and '</head>' in text:
        text = text.replace('</head>', progress_css + '</head>', 1)
        changed = True
    if 'id="teReadingProgressJs"' not in text and '</body>' in text:
        text = text.replace('</body>', progress_js + '</body>', 1)
        changed = True
    if changed:
        page.write_text(text, encoding='utf-8')
        updated += 1

# Primero se ejecuta la auditoría integral sobre la arquitectura previa.
audit = news_dir / 'final-site-audit.py'
if not audit.exists():
    raise RuntimeError('Falta final-site-audit.py')
code = compile(audit.read_text(encoding='utf-8'), str(audit), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(audit)})

# Después se instala la cabecera premium. Al ir tras la auditoría no invalida
# la protección histórica de la cabecera antigua.
premium_header = news_dir / 'install-premium-header.py'
if not premium_header.exists():
    raise RuntimeError('Falta install-premium-header.py')
code = compile(premium_header.read_text(encoding='utf-8'), str(premium_header), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(premium_header)})

# La marca completa se aplica como una capa mínima sobre la cabecera ya instalada.
full_brand = news_dir / 'full-brand-header.py'
if not full_brand.exists():
    raise RuntimeError('Falta full-brand-header.py')
code = compile(full_brand.read_text(encoding='utf-8'), str(full_brand), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(full_brand)})

# Navegación rápida únicamente en escritorio: desaparece en móvil y al hacer scroll.
quick_nav = news_dir / 'install-desktop-quick-nav.py'
if not quick_nav.exists():
    raise RuntimeError('Falta install-desktop-quick-nav.py')
code = compile(quick_nav.read_text(encoding='utf-8'), str(quick_nav), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(quick_nav)})

# Y por último se comprueba el artefacto ya con la nueva cabecera instalada.
quality = news_dir / 'quality-check.py'
if not quality.exists():
    raise RuntimeError('Falta quality-check.py')
code = compile(quality.read_text(encoding='utf-8'), str(quality), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(quality)})

print(f'Experiencia editorial conectada · progreso de lectura instalado en {updated} páginas largas potenciales · auditoría integral superada · cabecera premium con nombre completo y navegación rápida de escritorio activa y verificada')

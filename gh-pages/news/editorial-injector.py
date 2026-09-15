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

# La cabecera premium se instala al final del build, después de todas las capas
# visuales anteriores y antes de la auditoría final. Así no se pierde en futuras
# publicaciones automáticas.
premium_header = news_dir / 'install-premium-header.py'
if not premium_header.exists():
    raise RuntimeError('Falta install-premium-header.py')
code = compile(premium_header.read_text(encoding='utf-8'), str(premium_header), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(premium_header)})

# Última capa del build: auditoría integral y una segunda comprobación de calidad
# sobre el artefacto que realmente será publicado.
for script_name in ('final-site-audit.py', 'quality-check.py'):
    script = news_dir / script_name
    if not script.exists():
        raise RuntimeError(f'Falta {script_name}')
    code = compile(script.read_text(encoding='utf-8'), str(script), 'exec')
    exec(code, {'__name__': '__main__', '__file__': str(script)})

print(f'Experiencia editorial conectada · progreso de lectura instalado en {updated} páginas largas potenciales · cabecera premium activa · auditoría final superada')

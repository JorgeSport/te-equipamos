from pathlib import Path

base = Path(__file__).resolve().parent
root = base.parent
css_tag = '<link rel="stylesheet" href="/te-equipamos-arpenaz-27l/editorial-credibility.css">'
js_tag = '<script src="/te-equipamos-arpenaz-27l/editorial-credibility.js"></script>'
skip = {'news', 'studio', 'kalenji'}
count = 0

for page in root.rglob('index.html'):
    rel = page.relative_to(root)
    if rel.parts and rel.parts[0] in skip:
        continue
    html = page.read_text(encoding='utf-8')
    changed = False
    if css_tag not in html and '</head>' in html:
        html = html.replace('</head>', css_tag + '</head>', 1)
        changed = True
    if js_tag not in html and '</body>' in html:
        html = html.replace('</body>', js_tag + '</body>', 1)
        changed = True
    if changed:
        page.write_text(html, encoding='utf-8')
        count += 1

methodology = base / 'metodologia' / 'index.html'
if not methodology.exists():
    raise RuntimeError('Falta la página de metodología editorial')

for asset in [root / 'editorial-credibility.css', root / 'editorial-credibility.js']:
    if not asset.exists():
        raise RuntimeError(f'Falta el activo editorial: {asset.name}')

print(f'Credibilidad editorial instalada en {count} landings · metodología disponible')

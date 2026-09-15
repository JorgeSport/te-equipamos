from pathlib import Path
from html.parser import HTMLParser
import json
import re

base = Path(__file__).resolve().parent
index = base / 'index.html'
html = index.read_text(encoding='utf-8')
size = len(html.encode('utf-8'))

class AuditParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.images = 0
        self.scripts = 0
        self.styles = 0
        self.links = 0
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.append(data['id'])
        if tag == 'img':
            self.images += 1
        elif tag == 'script':
            self.scripts += 1
        elif tag == 'style':
            self.styles += 1
        elif tag == 'link':
            self.links += 1

parser = AuditParser()
parser.feed(html)
duplicates = sorted({x for x in parser.ids if parser.ids.count(x) > 1})

required = {
    'hero_priority': 'fetchpriority="high"',
    'lazy_images': 'loading="lazy"',
    'async_decode': 'decoding="async"',
    'mobile_progressive_render': 'TE_MOBILE_PERFORMANCE',
    'comparator': 'TE_PRODUCT_COMPARATOR_JS',
    'reduced_motion': 'prefers-reduced-motion',
}
checks = {name: marker in html for name, marker in required.items()}

# El Hub es deliberadamente una aplicación estática con datos y estilos integrados.
# Este límite no pretende sustituir Lighthouse: impide únicamente que un cambio futuro
# haga crecer el documento principal de forma descontrolada.
MAX_INDEX_BYTES = 650_000
if size > MAX_INDEX_BYTES:
    raise RuntimeError(f'Presupuesto de rendimiento superado: index.html pesa {size} bytes (máximo {MAX_INDEX_BYTES})')
if duplicates:
    raise RuntimeError('IDs HTML duplicados en el artefacto: ' + ', '.join(duplicates))
missing = [name for name, ok in checks.items() if not ok]
if missing:
    raise RuntimeError('Faltan protecciones de rendimiento: ' + ', '.join(missing))

report = {
    'type': 'static-build-performance-budget',
    'index_bytes': size,
    'max_index_bytes': MAX_INDEX_BYTES,
    'html_ids': len(parser.ids),
    'duplicate_ids': duplicates,
    'script_tags': parser.scripts,
    'style_tags': parser.styles,
    'link_tags': parser.links,
    'checks': checks,
    'note': 'Este informe es un control estático de compilación. Core Web Vitals reales requieren medición en navegador o datos de campo.'
}
(base / 'performance-build-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Presupuesto de rendimiento superado correctamente: {size} bytes · sin IDs duplicados · protecciones activas')

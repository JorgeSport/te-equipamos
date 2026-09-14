from pathlib import Path
import json
import re

base = Path(__file__).resolve().parent
index = base / 'index.html'
data_file = base / 'news-data.json'
restore_script = base / 'restore-desktop-card-images.py'

errors = []
warnings = []

if not index.exists():
    errors.append('Falta gh-pages/news/index.html')
if not data_file.exists():
    errors.append('Falta gh-pages/news/news-data.json')

if errors:
    raise SystemExit('\n'.join(errors))

# Normaliza el resultado final antes de verificarlo: las imágenes deben quedar visibles
# en escritorio aunque un CSS anterior haya intentado ocultarlas.
if restore_script.exists():
    code = compile(restore_script.read_text(encoding='utf-8'), str(restore_script), 'exec')
    exec(code, {'__name__': '__main__', '__file__': str(restore_script)})
else:
    errors.append('Falta restore-desktop-card-images.py')

html = index.read_text(encoding='utf-8')
items = json.loads(data_file.read_text(encoding='utf-8'))

required_markers = {
    'Pulido de escritorio': '/* TE_DESKTOP_POLISH */',
    'Script de escritorio': 'id="teDesktopPolish"',
    'Imágenes de tarjetas en escritorio': '/* TE_DESKTOP_CARD_IMAGES */',
    'Protección de miniaturas móvil': '/* TE_IMAGE_FAILSAFE */',
    'Buscador y descubrimiento': 'TE_DISCOVERY_PHASE1_JS',
    'Etiquetas activas': 'function applyTagFilter(',
    'Compartir tarjetas': 'function shareHubItem(id,action,button)',
    'Menú de secciones': "const CATS=['Todas','Ventas','Reviews','Vídeos','Consejos','Ofertas','Novedades','Siguiendo'];",
}
for label, marker in required_markers.items():
    if marker not in html:
        errors.append(f'No se encontró: {label}')

for obsolete in ['id="promoBar"', 'id="promoHome"']:
    if obsolete in html:
        errors.append(f'Sigue presente un bloque promocional retirado: {obsolete}')

if 'CONTENIDO PROPIO · GITHUB' in html.upper():
    errors.append('Hay una referencia técnica visible a GitHub')

if len(items) == 0:
    errors.append('El portal no tiene contenidos')

seen_ids = set()
for i, item in enumerate(items, start=1):
    title = str(item.get('title') or '').strip()
    url = str(item.get('url') or '').strip()
    iid = item.get('id')
    if not title:
        errors.append(f'Contenido {i}: título vacío')
    if not url.startswith(('https://','http://')):
        errors.append(f'Contenido {i}: URL no válida')
    if iid in seen_ids:
        errors.append(f'ID duplicado: {iid}')
    seen_ids.add(iid)
    if not item.get('image'):
        errors.append(f'Contenido sin imagen: {title[:70]}')

# Verifica que el CSS de escritorio no afecte al móvil por accidente.
block = re.search(r'/\* TE_DESKTOP_POLISH \*/(.*?)(?:</style>|$)', html, flags=re.S)
if not block:
    errors.append('No se pudo inspeccionar el bloque de escritorio')
elif '@media(min-width:1101px)' not in block.group(0):
    errors.append('El pulido de escritorio no está aislado por breakpoint')

# Las imágenes deben restaurarse DESPUÉS del pulido que originalmente las ocultaba.
polish_pos = html.find('/* TE_DESKTOP_POLISH */')
images_pos = html.find('/* TE_DESKTOP_CARD_IMAGES */')
if images_pos == -1:
    errors.append('Falta la restauración de imágenes de escritorio')
elif polish_pos != -1 and images_pos < polish_pos:
    errors.append('La regla de imágenes se aplica antes del pulido y puede quedar anulada')
else:
    images_end = html.find('</style>', images_pos)
    images_block = html[images_pos:images_end if images_end != -1 else len(html)]
    if '.feed .card>.thumb{display:block!important' not in images_block:
        errors.append('Las miniaturas de escritorio no están configuradas como visibles')
    if 'grid-template-columns:minmax(0,1fr) 190px' not in images_block:
        errors.append('Las tarjetas de escritorio no reservan espacio para la imagen')

# La navegación lateral original debe seguir disponible para móvil/tablet.
if '.side .nav{display:none!important}' not in html:
    errors.append('No se encontró la sustitución del menú lateral en escritorio')
if '@media(max-width:760px)' not in html:
    errors.append('Faltan reglas responsive para móvil')

# Comprobación simple de IDs estáticos duplicados. Ignora plantillas JS con ${...}.
static_ids = re.findall(r'\bid=["\']([A-Za-z][\w:-]*)["\']', html)
duplicates = sorted({x for x in static_ids if static_ids.count(x) > 1 and not x.startswith('teRail')})
if duplicates:
    warnings.append('IDs repetidos detectados para revisar: ' + ', '.join(duplicates[:10]))

if errors:
    print('Errores:')
    for e in errors:
        print(' - ' + e)
    raise SystemExit(1)

print(f'CONTROL DE CALIDAD OK · {len(items)} contenidos · imágenes de escritorio verificadas')
if warnings:
    print('Avisos no bloqueantes:')
    for w in warnings:
        print(' - ' + w)

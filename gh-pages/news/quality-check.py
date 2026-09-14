from pathlib import Path
import json
import re

base = Path(__file__).resolve().parent
index = base / 'index.html'
data_file = base / 'news-data.json'
restore_script = base / 'restore-desktop-card-images.py'
errors, warnings = [], []

if not index.exists(): errors.append('Falta gh-pages/news/index.html')
if not data_file.exists(): errors.append('Falta gh-pages/news/news-data.json')
if errors: raise SystemExit('\n'.join(errors))

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
    'Mosaico editorial Sigue explorando': '/* SECTION_JOURNEY_VISUAL */',
    'Restauración responsive independiente': 'id="teResponsiveRestore"',
    'Protección de imágenes': '/* TE_IMAGE_FAILSAFE */',
    'Buscador y descubrimiento': 'TE_DISCOVERY_PHASE1_JS',
    'Etiquetas activas': 'function applyTagFilter(',
    'Filtro real por actividad': 'function applyActivityFilter(',
    'Etiquetas visuales de actividad': 'function renderActivityPills(',
    'Compartir tarjetas': 'function shareHubItem(id,action,button)',
    'Menú de secciones': "const CATS=['Todas','Ventas','Reviews','Vídeos','Consejos','Ofertas','Novedades','Siguiendo'];",
}
for label, marker in required_markers.items():
    if marker not in html: errors.append(f'No se encontró: {label}')

for obsolete in ['id="promoBar"', 'id="promoHome"']:
    if obsolete in html: errors.append(f'Sigue presente un bloque promocional retirado: {obsolete}')
if 'CONTENIDO PROPIO · GITHUB' in html.upper(): errors.append('Hay una referencia técnica visible a GitHub')
if not items: errors.append('El portal no tiene contenidos')

seen_ids = set()
for i, item in enumerate(items, start=1):
    title = str(item.get('title') or '').strip()
    url = str(item.get('url') or '').strip()
    iid = item.get('id')
    if not title: errors.append(f'Contenido {i}: título vacío')
    if not url.startswith(('https://','http://')): errors.append(f'Contenido {i}: URL no válida')
    if iid in seen_ids: errors.append(f'ID duplicado: {iid}')
    seen_ids.add(iid)
    if not item.get('image'): errors.append(f'Contenido sin imagen: {title[:70]}')
    activities = item.get('activities')
    if not isinstance(activities, list) or not activities:
        errors.append(f'Contenido sin actividad: {title[:70]}')
    if not str(item.get('product_type') or '').strip():
        errors.append(f'Contenido sin product_type: {title[:70]}')
    if item.get('activities_inferred'):
        warnings.append(f'Actividad inferida en lugar de declarada: {title[:70]}')

# ESCRITORIO: los cambios visuales específicos deben seguir aislados.
block = re.search(r'/\* TE_DESKTOP_POLISH \*/(.*?)(?:</style>|$)', html, flags=re.S)
if not block: errors.append('No se pudo inspeccionar el bloque de escritorio')
elif '@media(min-width:1101px)' not in block.group(0): errors.append('El pulido de escritorio no está aislado por breakpoint')

for label in ['Tu espacio','Explorar','Senderismo','Running','Ciclismo','Natación','Travel','Más actividades']:
    if label not in html: errors.append(f'Falta navegación lateral: {label}')
if 'const ACTIVITIES=[' not in html or 'data-activity-query=' not in html:
    errors.append('La navegación por actividades no está activa')
if 'state.activity' not in html:
    errors.append('El Hub no mantiene un estado propio de actividad')
if '#teRailTopics{display:none!important}' not in html:
    errors.append('La columna derecha puede volver a duplicar Explorar/Temas')

for marker in ['const EXTRA_ACTIVITIES=[', 'let activitiesOpen=false', 'data-activity-extra', 'aria-expanded=', "activitiesOpen=!activitiesOpen"]:
    if marker not in html: errors.append('El desplegable Más actividades no está completo: falta ' + marker)
for label in ['Trekking','Trail running','Alpinismo','Escalada','Camping','Esquí y nieve','Kayak y remo','Surf','Fitness']:
    if label not in html: errors.append(f'Falta actividad ampliada: {label}')

# Las actividades se deben mostrar como chips distintos de los tags normales.
for marker in ['class="activityRow"', 'data-activity-filter=', 'teNormalTags(n)']:
    if marker not in html: errors.append('Falta separación visual entre actividades y etiquetas: ' + marker)

polish_pos = html.find('/* TE_DESKTOP_POLISH */')
images_pos = html.find('/* TE_DESKTOP_CARD_IMAGES */')
if images_pos == -1:
    errors.append('Falta la restauración de imágenes de escritorio')
elif polish_pos != -1 and images_pos < polish_pos:
    errors.append('La regla de imágenes se aplica antes del pulido y puede quedar anulada')
else:
    images_end = html.find('</style>', images_pos)
    images_block = html[images_pos:images_end if images_end != -1 else len(html)]
    if '@media(min-width:1101px)' not in images_block: errors.append('El formato 60/40 no está limitado a escritorio')
    if '.feed .card>.thumb{display:block!important' not in images_block: errors.append('Las imágenes de escritorio no están visibles')
    if 'grid-template-columns:minmax(0,3fr) minmax(280px,2fr)' not in images_block: errors.append('Las tarjetas de escritorio no usan 60/40')
    if 'aspect-ratio:16/9!important' not in images_block: errors.append('Las imágenes de escritorio no mantienen 16:9')

# RESPONSIVE: no heredar las miniaturas laterales del escritorio.
rstart = html.find('<style id="teResponsiveRestore">')
if rstart == -1:
    errors.append('No existe la restauración específica de responsive')
else:
    rend = html.find('</style>', rstart)
    responsive = html[rstart:rend if rend != -1 else len(html)]
    for marker in ['@media(max-width:760px)','flex-direction:column!important','order:-1!important;width:100%!important','aspect-ratio:16/9!important']:
        if marker not in responsive: errors.append('Responsive no restaurado correctamente: falta ' + marker)
    if '108px!important' in responsive or '118px!important' in responsive:
        errors.append('El responsive sigue forzando miniaturas laterales pequeñas')

journey_pos = html.find('/* SECTION_JOURNEY_VISUAL */')
if journey_pos == -1:
    errors.append('No existe el mosaico visual al final de las secciones')
else:
    journey_end = html.find('</style>', journey_pos)
    journey_css = html[journey_pos:journey_end if journey_end != -1 else len(html)]
    for marker, label in [('.journeyHero','bloque protagonista'),('.journeySide','bloques secundarios'),('.journeyWide','bloque panorámico')]:
        if marker not in journey_css: errors.append(f'El mosaico editorial no incluye {label}')
if 'function journeyMedia(cat)' not in html: errors.append('El mosaico editorial no toma imágenes reales del contenido')
if 'journeyItems(x.cat).length>0' not in html: errors.append('El mosaico no oculta secciones sin contenido')
if '.side .nav{display:none!important}' not in html: errors.append('No se encontró la sustitución del menú lateral en escritorio')

static_ids = re.findall(r'\bid=["\']([A-Za-z][\w:-]*)["\']', html)
duplicates = sorted({x for x in static_ids if static_ids.count(x) > 1 and not x.startswith('teRail')})
if duplicates: warnings.append('IDs repetidos detectados para revisar: ' + ', '.join(duplicates[:10]))

if errors:
    print('Errores:')
    for e in errors: print(' - ' + e)
    raise SystemExit(1)

activity_set = sorted({a for item in items for a in item.get('activities', [])})
print(f'CONTROL DE CALIDAD OK · {len(items)} contenidos · {len(activity_set)} actividades · clasificación nativa verificada')
if warnings:
    print('Avisos no bloqueantes:')
    for w in warnings: print(' - ' + w)

from pathlib import Path
from datetime import datetime
import json
import re

base = Path(__file__).resolve().parent
index = base / 'index.html'
data_file = base / 'news-data.json'
restore_script = base / 'restore-desktop-card-images.py'
legacy_repositories_file = base / 'seo-legacy-repositories.json'
errors, warnings = [], []
OFFICIAL_URL = 'https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/'

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
legacy_repositories = set(json.loads(legacy_repositories_file.read_text(encoding='utf-8'))) if legacy_repositories_file.exists() else set()

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
    'Inicio completo tras filtrar actividad': 'function scrollActivityResultsStart()',
    'Estado vacío por actividad': '/* TE_ACTIVITY_EMPTY_STATE */',
    'Alternativas separadas por actividad': 'function renderActivityAlternatives(',
    'Etiquetas visuales de actividad': 'function renderActivityPills(',
    'Etiquetas neutras globales': '/* TE_NEUTRAL_PRODUCT_TAGS */',
    'Etiquetas neutras responsive': '/* TE_RESPONSIVE_NEUTRAL_TAGS */',
    'Compartir tarjetas': 'function shareHubItem(id,action,button)',
    'Actividades responsive': '/* TE_RESPONSIVE_ACTIVITY_NAV */',
    'Script de actividades responsive': 'id="teResponsiveActivitiesScript"',
    'Metadatos oficiales': '<!-- TE_OFFICIAL_SITE_META -->',
    'Datos estructurados oficiales': 'id="teOfficialSchema"',
    'Menú de secciones': "const CATS=['Todas','Ventas','Reviews','Ofertas','Novedades','Vídeos','Consejos','Siguiendo'];",
}
for label, marker in required_markers.items():
    if marker not in html: errors.append(f'No se encontró: {label}')

for obsolete in ['id="promoBar"', 'id="promoHome"']:
    if obsolete in html: errors.append(f'Sigue presente un bloque promocional retirado: {obsolete}')
if 'CONTENIDO PROPIO · GITHUB' in html.upper(): errors.append('Hay una referencia técnica visible a GitHub')
if not items: errors.append('El portal no tiene contenidos')

# La identidad pública ya no debe presentarse como Noticias/News y la marca debe volver al Hub oficial.
if '<title>Te Equipamos | Deporte, actividades y equipamiento</title>' not in html:
    errors.append('El título estratégico del portal no está activo')
if 'Te Equipamos News' in html:
    errors.append('Sigue apareciendo la identidad antigua Te Equipamos News')
if '<small>Noticias</small>' in html or '← Volver a noticias' in html:
    errors.append('Sigue apareciendo Noticias en la identidad o navegación principal')
for marker in [
    f'href="{OFFICIAL_URL}" class="brand"',
    f'<link rel="canonical" href="{OFFICIAL_URL}">',
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Te Equipamos">',
    '<meta property="og:title"',
    '<meta property="og:description"',
    f'<meta property="og:url" content="{OFFICIAL_URL}">',
    '<meta property="og:image"',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="twitter:title"',
    '<meta name="twitter:description"',
    '<meta name="twitter:image"',
]:
    if marker not in html:
        errors.append('Falta metadato o enlace oficial: ' + marker)

# Incluso la landing de producto principal debe usar TE EQUIPAMOS como acceso al Hub, no como enlace al producto.
main_product = base.parent / 'index.html'
if main_product.exists():
    main_html = main_product.read_text(encoding='utf-8')
    if f'href="{OFFICIAL_URL}"' not in main_html or 'aria-label="Ir al inicio de Te Equipamos"' not in main_html:
        errors.append('La marca de la landing principal no vuelve al Hub oficial')

# Los lectores centrales deben conservar siempre un camino al Hub oficial.
read_root = base.parent / 'read'
if read_root.exists():
    for reader in read_root.glob('*/index.html'):
        reader_html = reader.read_text(encoding='utf-8')
        if OFFICIAL_URL not in reader_html:
            errors.append(f'El lector {reader.parent.name} no enlaza al Hub oficial')

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
    source_repo = str(item.get('source_repo') or '').strip()
    schema_version = int(item.get('schema_version') or 1)
    if source_repo and source_repo not in legacy_repositories and schema_version < 3:
        errors.append(f'Repositorio nuevo sin schema_version 3: {source_repo}')
    if source_repo and source_repo not in legacy_repositories:
        published_at = str(item.get('published_at') or '').strip()
        try:
            datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        except (TypeError, ValueError):
            errors.append(f'Repositorio nuevo sin published_at válido: {source_repo}')
    if schema_version >= 3:
        stable_id = item.get('id')
        card_title = str(item.get('card_title') or '').strip()
        seo_title = str(item.get('seo_title') or '').strip()
        seo_description = str(item.get('seo_description') or '').strip()
        seo_keywords = item.get('seo_keywords') if isinstance(item.get('seo_keywords'), list) else []
        if not item.get('seo_ready'):
            errors.append(f'Contenido schema 3 incompleto para SEO: {source_repo or title[:70]}')
        if not isinstance(stable_id, int) or stable_id <= 0:
            errors.append(f'Contenido schema 3 sin ID estable: {source_repo or title[:70]}')
        if not 35 <= len(card_title) <= 95:
            errors.append(f'card_title fuera de longitud estratégica: {card_title[:70]}')
        if not 35 <= len(seo_title) <= 75:
            errors.append(f'seo_title fuera de longitud estratégica: {seo_title[:70]}')
        if not 90 <= len(seo_description) <= 180:
            errors.append(f'seo_description fuera de longitud estratégica: {seo_title[:70]}')
        if not 3 <= len(seo_keywords) <= 8:
            errors.append(f'seo_keywords debe contener entre 3 y 8 términos: {seo_title[:70]}')

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

for marker in ['class="activityRow"', 'data-activity-filter=', 'teNormalTags(n)']:
    if marker not in html: errors.append('Falta separación visual entre actividades y etiquetas: ' + marker)

# Las etiquetas de producto deben ser neutras tanto en escritorio como en responsive.
global_neutral_pos = html.find('/* TE_NEUTRAL_PRODUCT_TAGS */')
if global_neutral_pos == -1:
    errors.append('No existe el estilo neutro global de etiquetas')
else:
    global_neutral_end = html.find('</style>', global_neutral_pos)
    global_neutral_css = html[global_neutral_pos:global_neutral_end if global_neutral_end != -1 else len(html)]
    for marker in ['.tagPill.tone-green,.tagPill.tone-blue,.tagPill.tone-amber,.tagPill.tone-violet,.tagPill.tone-neutral', 'background:transparent', 'border-color:var(--line)']:
        if marker not in global_neutral_css:
            errors.append('Etiquetas globales no están neutralizadas correctamente: falta ' + marker)

neutral_pos = html.find('/* TE_RESPONSIVE_NEUTRAL_TAGS */')
if neutral_pos == -1:
    errors.append('No existe el estilo neutro de etiquetas responsive')
else:
    neutral_end = html.find('</style>', neutral_pos)
    neutral_css = html[neutral_pos:neutral_end if neutral_end != -1 else len(html)]
    for marker in ['@media(max-width:1100px)', 'background:transparent!important', 'border-color:var(--line)!important']:
        if marker not in neutral_css:
            errors.append('Etiquetas responsive no están neutralizadas correctamente: falta ' + marker)

# Al filtrar por actividad, la primera tarjeta o el estado vacío deben quedar completos bajo la cabecera sticky.
for marker in ["document.querySelector('#feed .card')", "document.querySelector('#empty.activityEmptyPanel')", "document.querySelector('.top')", "getBoundingClientRect().height", "scrollActivityResultsStart()"]:
    if marker not in html:
        errors.append('El inicio de resultados por actividad puede quedar cortado: falta ' + marker)

# Si una actividad no tiene contenido, primero debe mostrarse un estado vacío y solo después alternativas.
for marker in ['id=\'activityAlternatives\'', 'className=\'activityAlternatives hidden\'', 'Aún no hay contenido en ${esc(label)}', 'También puedes explorar', 'data-activity-alt=', "if(feed)feed.classList.add('hidden')", "if(journey)journey.classList.add('hidden')"]:
    if marker not in html:
        errors.append('La experiencia de actividad vacía no está completa: falta ' + marker)

empty_css_pos = html.find('/* TE_ACTIVITY_EMPTY_STATE */')
if empty_css_pos != -1:
    empty_css_end = html.find('</style>', empty_css_pos)
    empty_css = html[empty_css_pos:empty_css_end if empty_css_end != -1 else len(html)]
    for marker in ['#empty.activityEmptyPanel', '.activityAlternatives{margin-top:', '.activityAlternativesGrid']:
        if marker not in empty_css:
            errors.append('El estado vacío no mantiene la jerarquía visual esperada: falta ' + marker)

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

resp_nav_pos = html.find('/* TE_RESPONSIVE_ACTIVITY_NAV */')
if resp_nav_pos == -1:
    errors.append('No existe la navegación de actividades responsive')
else:
    resp_nav_end = html.find('</style>', resp_nav_pos)
    resp_nav = html[resp_nav_pos:resp_nav_end if resp_nav_end != -1 else len(html)]
    if '@media(max-width:1100px)' not in resp_nav:
        errors.append('La navegación de actividades responsive no está limitada a tablet/móvil')
for marker in ['id="teResponsiveActivities"', 'data-resp-activity=', 'data-resp-more', 'Explorar actividades']:
    if marker not in html:
        errors.append('Falta navegación responsive por actividad: ' + marker)

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
print(f'CONTROL DE CALIDAD OK · {len(items)} contenidos · {len(activity_set)} actividades · URL oficial, metadatos sociales y navegación verificados')
if warnings:
    print('Avisos no bloqueantes:')
    for w in warnings: print(' - ' + w)

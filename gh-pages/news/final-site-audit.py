from pathlib import Path
from urllib.parse import urlparse
import json
import re

NEWS = Path(__file__).resolve().parent
ROOT = NEWS.parent
INDEX = NEWS / 'index.html'
BASE_URL = 'https://jorgesport.github.io/te-equipamos-arpenaz-27l/'
SOCIAL_IMAGE = 'https://res.cloudinary.com/detstbpo9/image/upload/v1789444910/te-equipamos-social-share-v2.jpg'

html = INDEX.read_text(encoding='utf-8')


def replace_function(text: str, name: str, replacement: str) -> str:
    pattern = rf'function {re.escape(name)}\([^)]*\)\{{.*?\}}\n(?=function )'
    out, count = re.subn(pattern, replacement.rstrip() + '\n', text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f'No se pudo reemplazar la función {name}')
    return out


# 1. Cabecera: controles reales, semántica de búsqueda y ningún botón decorativo muerto.
old_header = '<header class="top"><div class="row"><button class="icon menuBtn" id="menuBtn">☰</button><a href="https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/" class="brand" aria-label="Ir al inicio de Te Equipamos"><span class="mark">TE</span><span>Te Equipamos</span></a><form class="search" id="searchForm"><span>⌕</span><input id="searchInput" placeholder="Buscar productos, reviews, actividades y consejos"><button type="button" id="clearBtn">×</button></form><div class="actions"><button class="icon" id="themeBtn">☼</button><button class="icon avatar">J</button></div></div><nav class="cats" id="cats"></nav><section id="teResponsiveActivities" class="teResponsiveActivities" aria-label="Explorar actividades"></section></header>'
new_header = '<header class="top"><div class="row"><button class="icon menuBtn" id="menuBtn" type="button" aria-label="Abrir menú" aria-expanded="false">☰</button><a href="https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/" class="brand" aria-label="Ir al inicio de Te Equipamos"><span class="mark">TE</span><span>Te Equipamos</span></a><form class="search" id="searchForm" role="search"><span aria-hidden="true">⌕</span><input id="searchInput" aria-label="Buscar en Te Equipamos" autocomplete="off" enterkeyhint="search" placeholder="Buscar productos, reviews, actividades y consejos"><button type="button" id="clearBtn" aria-label="Limpiar búsqueda" title="Limpiar búsqueda" hidden>×</button></form><div class="actions"><button class="icon" id="themeBtn" type="button" aria-label="Cambiar tema" title="Cambiar tema">☼</button><span class="icon avatar teBrandDot" aria-label="Te Equipamos">TE</span></div></div><nav class="cats" id="cats" aria-label="Secciones de Te Equipamos"></nav><section id="teResponsiveActivities" class="teResponsiveActivities" aria-label="Explorar actividades"></section></header>'
if old_header in html:
    html = html.replace(old_header, new_header, 1)
elif 'id="tePremiumHeader"' in html and '/* TE_PREMIUM_HEADER */' in html:
    pass
elif 'id="teFinalUxPolishScript"' not in html:
    raise RuntimeError('La cabecera del Hub cambió y requiere revisión antes de aplicar el pulido final')

html = html.replace('<p id="feedSub">', '<p id="feedSub" aria-live="polite">', 1)
html = html.replace('<div class="empty hidden" id="empty">', '<div class="empty hidden" id="empty" aria-live="polite">', 1)

# 2. Menú dinámico: una sección vacía no se anuncia. Reaparece sola cuando tenga contenido.
nav_fn = r'''function teAvailableCats(){const has=c=>NEWS.some(n=>n.category===c||(Array.isArray(n.sections)&&n.sections.includes(c)));return CATS.filter(c=>c==='Todas'||c==='Siguiendo'||has(c))}
function renderNav(){const visible=teAvailableCats();const label=c=>c==='Todas'?'Inicio':c==='Ventas'?'Productos':c;$('#cats').innerHTML=visible.map(c=>`<button class="chip ${state.cat===c?'active':''}" data-cat="${c}" ${state.cat===c?'aria-current="page"':''}>${label(c)}</button>`).join('');$('#nav').innerHTML=visible.map(c=>`<button class="${state.cat===c?'active':''}" data-cat="${c}" ${state.cat===c?'aria-current="page"':''}>${c==='Todas'?'⌂ Inicio':c==='Siguiendo'?'★ Siguiendo':label(c)}</button>`).join('')}'''
if 'function teAvailableCats()' not in html:
    html = replace_function(html, 'renderNav', nav_fn)

# 3. Portada robusta y accesible. La imagen principal se prioriza y las secundarias cargan bajo demanda.
hero_fn = r'''function renderHero(){let f=NEWS.filter(n=>n.featured).slice(0,4);if(!f.length)f=[...NEWS].sort((a,b)=>Number(b.score||0)-Number(a.score||0)).slice(0,4);const m=f[0];if(!m){$('#hero').classList.add('hidden');return}$('#hero').classList.remove('hidden');$('#hero').innerHTML=`<article class="panel heroMain"><img src="${m.image}" data-article="${m.id}" alt="${esc(m.title)}" fetchpriority="high" decoding="async"><div class="heroCopy"><span class="kicker">${esc(cardLabel(m))} · Destacado</span>${freshBadge(m)}<h2><a href="?id=${m.id}" data-article="${m.id}">${esc(cardTitle(m))}</a></h2><p>${esc(m.summary)}</p><div class="meta">${esc(cardMeta(m))}</div></div></article><div class="panel">${f.slice(1).map(n=>`<article class="heroItem"><div><span class="kicker">${esc(cardLabel(n))}</span>${freshBadge(n)}<h3><a href="?id=${n.id}" data-article="${n.id}">${esc(cardTitle(n))}</a></h3><span class="meta">${esc(cardMeta(n))}</span></div><img src="${n.image}" alt="" loading="lazy" decoding="async"></article>`).join('')}</div>`}'''
if 'fetchpriority="high" decoding="async"' not in html:
    html = replace_function(html, 'renderHero', hero_fn)

# 4. Portada sin repetición inmediata: los cuatro destacados no vuelven a aparecer justo debajo.
feed_fn = r'''function renderFeed(){let list=filtered();const home=state.cat==='Todas'&&!state.q&&!state.activity;if(home){const featuredIds=new Set(NEWS.filter(n=>n.featured).slice(0,4).map(n=>n.id));const fresh=list.filter(n=>!featuredIds.has(n.id));if(fresh.length)list=fresh}$('#feed').innerHTML=list.map(n=>{const saved=state.saved.has(n.id);return `<article class="card"><div><div class="meta">${esc(cardLabel(n))} · ${esc(cardMeta(n))}${freshBadge(n)}</div><a class="title" href="?id=${n.id}" data-article="${n.id}">${esc(cardTitle(n))}</a><p class="summary">${esc(n.summary)}</p>${renderActivityPills(n)}${renderTagPills(n)}<div class="cardShare" aria-label="Compartir esta tarjeta">
<button class="cardShareBtn" type="button" data-share-action="whatsapp" data-share-id="${n.id}" aria-label="Compartir por WhatsApp" title="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M20 11.7a8 8 0 0 1-11.8 7L4 20l1.3-4.1A8 8 0 1 1 20 11.7Z"/><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M8.8 8.4c.4 3 2.2 4.9 5.2 6l1.3-1.3 2 .8c.2.1.3.3.2.6-.4 1.2-1.5 1.9-2.7 1.7-4.4-.8-7.6-4-8.3-8.3-.2-1.2.5-2.3 1.7-2.7.3-.1.5 0 .6.2l.8 2-1 1Z"/></svg></button>
<button class="cardShareBtn" type="button" data-share-action="facebook" data-share-id="${n.id}" aria-label="Compartir en Facebook" title="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.6 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.7-1.6H17V4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.5v3.2h2.8V22h3.3Z"/></svg></button>
<button class="cardShareBtn" type="button" data-share-action="telegram" data-share-id="${n.id}" aria-label="Compartir por Telegram" title="Telegram"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.4 4.2 18.7 19c-.2 1-.8 1.3-1.6.8l-4.1-3-2 1.9c-.2.2-.4.4-.8.4l.3-4.2 7.6-6.9c.3-.3-.1-.5-.5-.2l-9.4 5.9-4-1.3c-.9-.3-.9-.9.2-1.3L20.1 4c.7-.3 1.5.2 1.3.2Z"/></svg></button>
<button class="cardShareBtn" type="button" data-share-action="copy" data-share-id="${n.id}" aria-label="Copiar enlace" title="Copiar enlace"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M10.6 13.4a4 4 0 0 0 5.7 0l2.1-2.1a4 4 0 0 0-5.7-5.7l-1.2 1.2M13.4 10.6a4 4 0 0 0-5.7 0l-2.1 2.1a4 4 0 0 0 5.7 5.7l1.2-1.2"/></svg></button>
</div><div class="cardMeta"><span>${n.time}</span><span>•</span><span>${n.category==='Ventas'?'Productos':n.category}</span><button class="save ${saved?'on':''}" data-save="${n.id}" aria-label="${saved?'Quitar de guardados':'Guardar contenido'}" aria-pressed="${saved?'true':'false'}" title="${saved?'Quitar de guardados':'Guardar contenido'}">${saved?'★':'☆'}</button></div></div><img class="thumb" src="${n.image}" data-article="${n.id}" alt="${esc(n.title)}" loading="lazy" decoding="async"></article>`}).join('');$('#empty').classList.toggle('hidden',list.length>0);$('#feed').classList.toggle('hidden',list.length===0);$('#feedTitle').textContent=state.q?`Resultados para “${state.q}”`:(home?'Más para descubrir':state.cat);$('#feedSub').textContent=state.q?`${list.length} resultados`:(home?'Más productos, reviews y novedades para seguir explorando.':`Contenido de ${(state.cat==='Ventas'?'productos':state.cat.toLowerCase())}`)}'''
if 'const featuredIds=new Set(' not in html:
    html = replace_function(html, 'renderFeed', feed_fn)

# 5. Micro-UX y accesibilidad. No cambia el layout aprobado.
if 'id="teFinalUxPolish"' not in html:
    ux_css = r'''<style id="teFinalUxPolish">/* TE_FINAL_UX_POLISH */
.teBrandDot{display:grid;place-items:center;cursor:default;font-size:11px;letter-spacing:-.02em;user-select:none}
#clearBtn[hidden]{display:none!important}
.heroItem h3 a{color:inherit;text-decoration:none}.heroItem h3 a:hover{color:var(--accent)}
.rel .kicker{display:block;margin-bottom:5px}.rel b{display:block}
.rel[role=link]:focus-visible{outline:2px solid color-mix(in srgb,var(--accent) 58%,transparent);outline-offset:3px;border-radius:8px}
@media(max-width:760px){.actions{gap:4px}.teBrandDot{font-size:10px}}
</style>'''
    html = html.replace('</head>', ux_css + '</head>', 1)

if 'id="teFinalUxPolishScript"' not in html:
    ux_js = r'''<script id="teFinalUxPolishScript">/* TE_ACCESSIBILITY_POLISH */
(function(){
  const q=s=>document.querySelector(s);
  const search=q('#searchInput'),clear=q('#clearBtn'),theme=q('#themeBtn'),menu=q('#menuBtn'),side=q('#side');
  function syncSearch(){if(clear)clear.hidden=!(search&&search.value.trim())}
  function syncTheme(){if(!theme)return;const dark=document.documentElement.dataset.theme==='dark';theme.setAttribute('aria-pressed',dark?'true':'false');theme.setAttribute('aria-label',dark?'Cambiar a tema claro':'Cambiar a tema oscuro');theme.title=theme.getAttribute('aria-label')}
  function syncMenu(){if(menu&&side)menu.setAttribute('aria-expanded',side.classList.contains('open')?'true':'false')}
  function enhanceLinks(root=document){root.querySelectorAll('.rel[data-article]').forEach(el=>{if(el.matches('a,button'))return;el.setAttribute('role','link');el.tabIndex=0;el.setAttribute('aria-label',el.querySelector('b')?.textContent?.trim()||'Abrir contenido')})}
  if(search)search.addEventListener('input',syncSearch);
  document.addEventListener('click',()=>setTimeout(()=>{syncSearch();syncTheme();syncMenu();enhanceLinks()},0));
  document.addEventListener('keydown',e=>{const el=e.target.closest&&e.target.closest('.rel[data-article][role="link"]');if(el&&(e.key==='Enter'||e.key===' ')){e.preventDefault();el.click()}});
  const obs=new MutationObserver(records=>{for(const r of records)for(const n of r.addedNodes)if(n.nodeType===1)enhanceLinks(n)});
  if(document.body)obs.observe(document.body,{childList:true,subtree:true});
  syncSearch();syncTheme();syncMenu();enhanceLinks();
})();
</script>'''
    html = html.replace('</body>', ux_js + '</body>', 1)

# 6. Datos estructurados reales de la colección y conexión anticipada con hosts de imágenes.
items = json.loads((NEWS / 'news-data.json').read_text(encoding='utf-8'))
collection = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    'name': 'Te Equipamos | Deporte, actividades y equipamiento',
    'url': BASE_URL + 'news/',
    'description': 'Productos, reviews, ofertas y guías de Te Equipamos organizados por actividad.',
    'mainEntity': {
        '@type': 'ItemList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'url': str(x.get('url') or ''), 'name': str(x.get('title') or '')}
            for i, x in enumerate(items[:12]) if x.get('url') and x.get('title')
        ],
    },
}
collection_schema = '<script type="application/ld+json" id="teCollectionSchema">' + json.dumps(collection, ensure_ascii=False, separators=(',', ':')) + '</script>'
if 'id="teCollectionSchema"' not in html:
    html = html.replace('</head>', collection_schema + '</head>', 1)

hosts = []
for item in items:
    host = urlparse(str(item.get('image') or '')).netloc
    if host and host not in hosts:
        hosts.append(host)
for host in hosts[:3]:
    tag = f'<link rel="preconnect" href="https://{host}">'
    if tag not in html:
        html = html.replace('</head>', tag + '</head>', 1)

INDEX.write_text(html, encoding='utf-8')

# 7. Seguridad de enlaces externos y coherencia cromática en breadcrumbs/lectores.
TARGET_RE = re.compile(r'<a\b([^>]*\btarget=["\']_blank["\'][^>]*)>', re.I)


def secure_target_blank(text: str) -> str:
    def repl(match):
        attrs = match.group(1)
        rel = re.search(r'\brel=["\']([^"\']*)["\']', attrs, re.I)
        if rel:
            values = set(rel.group(1).split())
            values.update({'noopener', 'noreferrer'})
            attrs = attrs[:rel.start()] + f'rel="{" ".join(sorted(values))}"' + attrs[rel.end():]
        else:
            attrs += ' rel="noopener noreferrer"'
        return '<a' + attrs + '>'
    return TARGET_RE.sub(repl, text)


def page_url(page: Path) -> str:
    rel = page.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return BASE_URL
    return BASE_URL + rel[:-len('index.html')]


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    return re.sub(r'\s+', ' ', match.group(1)).strip() if match else ''


for page in ROOT.rglob('index.html'):
    text = page.read_text(encoding='utf-8', errors='replace')
    text = secure_target_blank(text)
    text = text.replace('.te-breadcrumbbar a{color:#1a73e8;', '.te-breadcrumbbar a{color:#355345;')
    if '/read/' in page.as_posix():
        text = text.replace('footer a{color:#1a73e8;', 'footer a{color:#355345;')

    is_redirect = 'http-equiv="refresh"' in text.lower() or '<title>Redirigiendo a Te Equipamos</title>' in text
    if not is_redirect and page != INDEX:
        canonical = page_url(page)
        title = first_match(r'<title>(.*?)</title>', text)
        description = first_match(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', text)
        if not description:
            description = first_match(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']description["\']', text)
        image = first_match(r'<img[^>]+src=["\'](https://[^"\']+)', text)
        extra = []
        if '<link rel="canonical"' not in text:
            extra.append(f'<link rel="canonical" href="{canonical}">')
        if '<meta name="robots"' not in text:
            extra.append('<meta name="robots" content="index,follow,max-image-preview:large">')
        if title and 'property="og:title"' not in text:
            extra.append(f'<meta property="og:title" content="{title}">')
        if description and 'property="og:description"' not in text:
            extra.append(f'<meta property="og:description" content="{description}">')
        if 'property="og:url"' not in text:
            extra.append(f'<meta property="og:url" content="{canonical}">')
        if 'property="og:site_name"' not in text:
            extra.append('<meta property="og:site_name" content="Te Equipamos">')
        if 'property="og:type"' not in text:
            extra.append('<meta property="og:type" content="website">')
        share_image = image or (SOCIAL_IMAGE if page == NEWS / 'metodologia' / 'index.html' else '')
        if share_image and 'property="og:image"' not in text:
            extra.append(f'<meta property="og:image" content="{share_image}">')
        if 'name="twitter:card"' not in text:
            extra.append('<meta name="twitter:card" content="summary_large_image">')
        if title and 'name="twitter:title"' not in text:
            extra.append(f'<meta name="twitter:title" content="{title}">')
        if description and 'name="twitter:description"' not in text:
            extra.append(f'<meta name="twitter:description" content="{description}">')
        if share_image and 'name="twitter:image"' not in text:
            extra.append(f'<meta name="twitter:image" content="{share_image}">')
        if extra:
            text = text.replace('</head>', ''.join(extra) + '</head>', 1)

    page.write_text(text, encoding='utf-8')

# 8. Verificaciones de esta capa antes de entregar el artefacto.
final_html = INDEX.read_text(encoding='utf-8')
required = [
    'function teAvailableCats()',
    'const featuredIds=new Set(',
    'id="teFinalUxPolish"',
    'id="teFinalUxPolishScript"',
    'id="teCollectionSchema"',
    'aria-label="Buscar en Te Equipamos"',
    'fetchpriority="high" decoding="async"',
]
for marker in required:
    if marker not in final_html:
        raise RuntimeError('La auditoría final no dejó activo: ' + marker)

print('AUDITORÍA FINAL OK · navegación útil · portada sin duplicados · accesibilidad · rendimiento · SEO · seguridad')

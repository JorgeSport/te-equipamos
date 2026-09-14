from pathlib import Path
from urllib.parse import urlparse
import html as html_lib
import json
import re

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
INDEX = BASE / 'index.html'
DATA = BASE / 'news-data.json'
CENTRAL_HOST = 'jorgesport.github.io'
CENTRAL_PREFIX = '/te-equipamos-arpenaz-27l/'

items = json.loads(DATA.read_text(encoding='utf-8'))
html = INDEX.read_text(encoding='utf-8')

css = r'''/* TE_SHARE_HUB */
.shareCard{border:0;background:transparent;color:var(--accent);font-size:12px;font-weight:800;cursor:pointer;padding:4px 7px;border-radius:999px;white-space:nowrap}.shareCard:hover{background:var(--soft)}
@media(max-width:760px){.shareCard{font-size:12px;padding:5px 7px}.cardMeta{flex-wrap:wrap}}
'''
if '/* TE_SHARE_HUB */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

old = '<span>${n.category}</span><button class="save '
new = '<span>${n.category}</span><button class="shareCard" type="button" data-share-id="${n.id}" aria-label="Compartir ${esc(n.title)}">↗ Compartir</button><button class="save '
if old in html:
    html = html.replace(old, new, 1)
elif 'data-share-id="${n.id}"' not in html:
    raise RuntimeError('No se encontró el punto para añadir Compartir en las tarjetas')

share_js = r'''async function shareHubItem(id){
 const n=NEWS.find(x=>x.id===Number(id));if(!n)return;
 const url=String(n.url||location.href);const text=`Mira esto en Te Equipamos: ${n.title}`;
 try{
   if(navigator.share){await navigator.share({title:n.title,text,url});return}
   if(navigator.clipboard&&navigator.clipboard.writeText){await navigator.clipboard.writeText(`${n.title}\n${url}`);toast('Enlace copiado');return}
 }catch(err){if(err&&err.name==='AbortError')return}
 const area=document.createElement('textarea');area.value=`${n.title}\n${url}`;area.style.position='fixed';area.style.opacity='0';document.body.appendChild(area);area.select();document.execCommand('copy');area.remove();toast('Enlace copiado')
}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-share-id]');if(!b)return;e.preventDefault();e.stopPropagation();shareHubItem(b.dataset.shareId)},true);
'''
if 'async function shareHubItem' not in html:
    marker = "document.addEventListener('click',e=>{const a=e.target.closest('[data-article]');"
    if marker not in html:
        raise RuntimeError('No se encontró el manejador principal para conectar Compartir')
    html = html.replace(marker, share_js + marker, 1)

INDEX.write_text(html, encoding='utf-8')

meta_pattern = re.compile(
    r'<meta\b(?=[^>]*(?:property|name)=["\'](?:og:(?:title|description|image|image:alt|url|site_name|type)|twitter:(?:card|title|description|image))["\'])[^>]*>\s*',
    flags=re.I,
)
meta_start = '<!-- TE_SHARE_META_START -->'
meta_end = '<!-- TE_SHARE_META_END -->'
updated = 0

for item in items:
    share_url = str(item.get('url') or '').strip()
    parsed = urlparse(share_url)
    if parsed.netloc.lower() != CENTRAL_HOST or not parsed.path.startswith(CENTRAL_PREFIX):
        continue

    rel = parsed.path[len(CENTRAL_PREFIX):].strip('/')
    target = ROOT / 'index.html' if not rel else ROOT / rel / 'index.html'
    if not target.exists():
        continue

    page = target.read_text(encoding='utf-8')
    title = str(item.get('title') or 'Te Equipamos').strip()
    summary = str(item.get('summary') or 'Productos, reviews, ofertas y contenido outdoor de Te Equipamos.').strip()
    image = str(item.get('image') or '').strip()

    title_attr = html_lib.escape(title + ' | Te Equipamos', quote=True)
    summary_attr = html_lib.escape(summary[:240], quote=True)
    image_attr = html_lib.escape(image, quote=True)
    url_attr = html_lib.escape(share_url, quote=True)
    image_alt = html_lib.escape(title, quote=True)

    meta = f'''{meta_start}\n<meta property="og:type" content="website">\n<meta property="og:site_name" content="Te Equipamos">\n<meta property="og:title" content="{title_attr}">\n<meta property="og:description" content="{summary_attr}">\n<meta property="og:image" content="{image_attr}">\n<meta property="og:image:alt" content="{image_alt}">\n<meta property="og:url" content="{url_attr}">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="{title_attr}">\n<meta name="twitter:description" content="{summary_attr}">\n<meta name="twitter:image" content="{image_attr}">\n{meta_end}\n'''

    if meta_start in page and meta_end in page:
        page = re.sub(re.escape(meta_start) + r'.*?' + re.escape(meta_end) + r'\s*', meta, page, count=1, flags=re.S)
    else:
        page = meta_pattern.sub('', page)
        if '</head>' not in page:
            continue
        page = page.replace('</head>', meta + '</head>', 1)

    target.write_text(page, encoding='utf-8')
    updated += 1

print(f'Compartir activado en el hub y metadatos sociales preparados en {updated} fichas.')

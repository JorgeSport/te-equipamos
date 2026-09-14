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
.cardShare{display:flex;align-items:center;gap:8px;margin:10px 0 12px}.cardShareBtn{width:36px;height:36px;border-radius:50%;border:1px solid var(--line);background:var(--surface);display:grid;place-items:center;padding:0;cursor:pointer;transition:transform .15s ease,box-shadow .15s ease,background .15s ease}.cardShareBtn:hover{transform:translateY(-1px);box-shadow:0 3px 10px rgba(0,0,0,.08);background:var(--surface2)}.cardShareBtn svg{width:20px;height:20px;display:block}.cardShareBtn[data-share-action="whatsapp"] svg{color:#25D366}.cardShareBtn[data-share-action="facebook"] svg{color:#1877F2}.cardShareBtn[data-share-action="telegram"] svg{color:#229ED9}.cardShareBtn[data-share-action="copy"] svg{color:var(--muted)}
@media(max-width:760px){.cardShare{gap:7px;margin:11px 0 10px}.cardShareBtn{width:38px;height:38px}.cardShareBtn svg{width:21px;height:21px}.cardMeta{flex-wrap:wrap}}
'''
if '/* TE_SHARE_HUB */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

share_row = '''<div class="cardShare" aria-label="Compartir esta tarjeta">
<button class="cardShareBtn" type="button" data-share-action="whatsapp" data-share-id="${n.id}" aria-label="Compartir por WhatsApp" title="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" d="M20 11.7a8 8 0 0 1-11.8 7L4 20l1.3-4.1A8 8 0 1 1 20 11.7Z"/><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" d="M8.8 8.4c.4 3 2.2 4.9 5.2 6l1.3-1.3 2 .8c.2.1.3.3.2.6-.4 1.2-1.5 1.9-2.7 1.7-4.4-.8-7.6-4-8.3-8.3-.2-1.2.5-2.3 1.7-2.7.3-.1.5 0 .6.2l.8 2-1 1Z"/></svg></button>
<button class="cardShareBtn" type="button" data-share-action="facebook" data-share-id="${n.id}" aria-label="Compartir en Facebook" title="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.6 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.7-1.6H17V4c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.5v3.2h2.8V22h3.3Z"/></svg></button>
<button class="cardShareBtn" type="button" data-share-action="telegram" data-share-id="${n.id}" aria-label="Compartir por Telegram" title="Telegram"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M21.4 4.2 18.7 19c-.2 1-.8 1.3-1.6.8l-4.1-3-2 1.9c-.2.2-.4.4-.8.4l.3-4.2 7.6-6.9c.3-.3-.1-.5-.5-.2l-9.4 5.9-4-1.3c-.9-.3-.9-.9.2-1.3L20.1 4c.7-.3 1.5.2 1.3.2Z"/></svg></button>
<button class="cardShareBtn" type="button" data-share-action="copy" data-share-id="${n.id}" aria-label="Copiar enlace" title="Copiar enlace"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M10.6 13.4a4 4 0 0 0 5.7 0l2.1-2.1a4 4 0 0 0-5.7-5.7l-1.2 1.2M13.4 10.6a4 4 0 0 0-5.7 0l-2.1 2.1a4 4 0 0 0 5.7 5.7l1.2-1.2"/></svg></button>
</div>'''

# Compatible con tarjetas normales, tags y la nueva fila de actividades.
card_points = [
    ('<p class="summary">${esc(n.summary)}</p>${renderActivityPills(n)}${renderTagPills(n)}<div class="cardMeta">', '<p class="summary">${esc(n.summary)}</p>${renderActivityPills(n)}${renderTagPills(n)}'),
    ('<p class="summary">${esc(n.summary)}</p>${renderTagPills(n)}<div class="cardMeta">', '<p class="summary">${esc(n.summary)}</p>${renderTagPills(n)}'),
    ('<p class="summary">${esc(n.summary)}</p><div class="cardMeta">', '<p class="summary">${esc(n.summary)}</p>'),
]
inserted = False
for old_card, prefix in card_points:
    if old_card in html:
        html = html.replace(old_card, prefix + share_row + '<div class="cardMeta">', 1)
        inserted = True
        break
if not inserted and 'class="cardShare"' not in html:
    raise RuntimeError('No se encontró el punto para añadir los iconos de compartir en las tarjetas')

share_js = r'''function copyShareLink(title,url,button){
 const value=`${title}\n${url}`;
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(value).then(()=>{toast('Enlace copiado');if(button){button.style.transform='scale(.92)';setTimeout(()=>button.style.transform='',180)}});return}
 const area=document.createElement('textarea');area.value=value;area.style.position='fixed';area.style.opacity='0';document.body.appendChild(area);area.select();document.execCommand('copy');area.remove();toast('Enlace copiado')
}
function shareHubItem(id,action,button){
 const n=NEWS.find(x=>x.id===Number(id));if(!n)return;
 const url=String(n.url||location.href);const title=String(n.title||'Te Equipamos');const text=`Mira esto en Te Equipamos: ${title}`;
 if(action==='whatsapp'){window.open(`https://wa.me/?text=${encodeURIComponent(text+'\n'+url)}`,'_blank','noopener,noreferrer');return}
 if(action==='facebook'){window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`,'_blank','noopener,noreferrer');return}
 if(action==='telegram'){window.open(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`,'_blank','noopener,noreferrer');return}
 if(action==='copy'){copyShareLink(title,url,button)}
}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-share-action][data-share-id]');if(!b)return;e.preventDefault();e.stopPropagation();shareHubItem(b.dataset.shareId,b.dataset.shareAction,b)},true);
'''
if 'function shareHubItem(id,action,button)' not in html:
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
    summary = str(item.get('summary') or 'Productos, reviews, ofertas y contenidos de Te Equipamos.').strip()
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

print(f'Iconos sociales activados en tarjetas y metadatos preparados en {updated} fichas.')

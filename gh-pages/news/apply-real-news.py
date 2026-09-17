from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import re

base = Path(__file__).resolve().parent
target = base / "index.html"
data = json.loads((base / "news-data.json").read_text(encoding="utf-8"))
html = target.read_text(encoding="utf-8")

months = {1:"ENE",2:"FEB",3:"MAR",4:"ABR",5:"MAY",6:"JUN",7:"JUL",8:"AGO",9:"SEP",10:"OCT",11:"NOV",12:"DIC"}
today = datetime.now(ZoneInfo("Europe/Madrid"))
edition = f"{today.day} {months[today.month]} {today.year}"

news_js = "const NEWS=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";"
html, n = re.subn(
    r"const NEWS=\[.*?\];\nconst TOPICS=",
    lambda m: news_js + "\nconst TOPICS=",
    html,
    count=1,
    flags=re.S,
)
if n != 1:
    raise RuntimeError("No se pudo actualizar el bloque NEWS")

html = html.replace(
    'content="Te Equipamos News — demo funcional con noticias ficticias de ejemplo."',
    'content="Te Equipamos News — actualidad outdoor, senderismo, trail running, ciclismo, montaña, equipamiento y reviews."',
)
html = html.replace(
    '<div class="demo"><b>DEMO FUNCIONAL</b><span>Todos los titulares, fuentes y artículos de esta versión son ficticios y sirven únicamente como ejemplo.</span></div>',
    f'<div class="demo"><b>EDICIÓN OUTDOOR · {edition}</b><span>Actualidad seleccionada automáticamente y contenido propio de Te Equipamos, siempre con enlace a la fuente o landing correspondiente.</span></div>',
)
html = html.replace(
    'Espacio preparado para conectar más adelante con tu newsletter.',
    'Noticias, guías, reviews y selección outdoor de Te Equipamos.',
)

source_css = '.sourceBtn{display:inline-block;margin-top:16px;background:var(--accent);color:#fff;padding:11px 18px;border-radius:22px;font-family:Arial,sans-serif;font-size:14px;font-weight:800}'
if source_css not in html:
    html = html.replace('.empty{', source_css + '.empty{', 1)

credibility_css = r'''/* TE_EDITORIAL_CREDIBILITY */
.te-editorial-meta{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:16px 0 24px;padding:12px 0 18px;border-bottom:1px solid var(--line);font-family:Arial,Helvetica,sans-serif;font-size:12px;color:var(--muted)}
.te-editorial-meta strong{color:var(--text);font-size:12px}.te-editorial-meta a{margin-left:auto;color:var(--accent);font-weight:800;text-decoration:none}.te-editorial-meta a:hover{text-decoration:underline}
.te-editorial-dot{color:color-mix(in srgb,var(--muted) 50%,transparent)}
.te-editorial-why{margin:28px 0 8px;padding:20px 22px;background:color-mix(in srgb,var(--soft) 58%,var(--surface));border:1px solid color-mix(in srgb,var(--line) 78%,transparent);border-radius:16px;font-family:Arial,Helvetica,sans-serif}
.te-editorial-why>span{display:block;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin-bottom:6px}.te-editorial-why h2{margin:0 0 12px!important;font-family:Arial,Helvetica,sans-serif!important;font-size:20px!important;letter-spacing:-.025em}.te-editorial-why ul{margin:0;padding:0;list-style:none;display:grid;gap:8px}.te-editorial-why li{position:relative;padding-left:17px;color:var(--muted);font-size:13px;line-height:1.45}.te-editorial-why li:before{content:'•';position:absolute;left:1px;color:var(--accent);font-weight:900}
@media(max-width:760px){.te-editorial-meta{align-items:flex-start;gap:7px 9px;margin:14px 0 20px}.te-editorial-meta a{width:100%;margin:3px 0 0}.te-editorial-why{padding:18px;border-radius:14px}.te-editorial-why h2{font-size:18px!important}}
'''
if '/* TE_EDITORIAL_CREDIBILITY */' not in html:
    html = html.replace('</style>', credibility_css + '</style>', 1)

# Responsive móvil inspirado en Google News: tarjetas compactas con miniatura lateral.
mobile_css = r'''.relMedia{display:none}
@media(max-width:760px){
  .feed{border-left:0;border-right:0;border-radius:0;box-shadow:none;background:transparent}
  .card{display:grid;grid-template-columns:minmax(0,1fr) 108px;gap:12px;padding:16px 16px 18px;margin:0 0 10px;background:var(--surface);border-bottom:1px solid var(--line);align-items:start}
  .card>div:first-child{padding:0;min-width:0}
  .card .thumb{order:initial;width:108px;height:82px;aspect-ratio:auto;object-fit:cover;border-radius:11px;align-self:start;background:var(--surface2)}
  .card.noThumb{grid-template-columns:1fr}
  .card .title{font-size:20px;line-height:1.22;margin:7px 0 10px;letter-spacing:-.01em}
  .card .summary{display:none}
  .card .cardMeta{font-size:12px;padding-bottom:0}
  .card .tagRow{margin:8px 0 8px}
  .card .cardShare{margin:8px 0 8px}
  .articleWrap{padding-left:0;padding-right:0}
  .articleWrap>.back{margin-left:14px}
  .articleGrid{display:block}
  .article{border-left:0;border-right:0;border-radius:0;box-shadow:none}
  .articleHero{width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
  .articleBody{padding:22px 18px 28px}
  .articleBody h1{font-size:34px;line-height:1.08;letter-spacing:-.035em}
  .related{margin-top:14px;border-left:0;border-right:0;border-radius:0;box-shadow:none;padding:22px 0;background:var(--bg)}
  .related h3{font-size:22px;padding:0 18px 14px;margin:0;background:var(--surface)}
  .rel{display:block;padding:0 0 22px;margin:0 0 12px;background:var(--surface);border-bottom:8px solid var(--bg)}
  .rel:nth-child(n+5){display:block}
  .relMedia{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}
  .relText{padding:16px 18px 0}
  .rel .kicker{display:block;margin-bottom:7px}
  .rel b{display:block;font-size:22px;line-height:1.22;letter-spacing:-.01em}
  .rel small{font-size:13px;margin-top:12px}
}
@media(min-width:761px){.rel:nth-child(n+5){display:none}}'''
if '.relMedia{display:none}' not in html:
    html = html.replace('</style>', mobile_css + '</style>', 1)

article_fn = r'''function teEditorialDate(n){const raw=String(n&&n.published||'').trim();if(!raw)return '';const d=new Date(raw);if(Number.isNaN(d.getTime()))return '';return new Intl.DateTimeFormat('es-ES',{day:'numeric',month:'long',year:'numeric'}).format(d)}
function tePublicSection(value){return value==='Ventas'?'Productos':String(value||'Te Equipamos')}
function teActivityLabel(value){const labels={'senderismo':'Senderismo','trekking':'Trekking','running':'Running','trail-running':'Trail running','ciclismo':'Ciclismo','natacion':'Natación','travel':'Travel','alpinismo':'Alpinismo','escalada':'Escalada','camping':'Camping','esqui':'Esquí y nieve','kayak':'Kayak y remo','surf':'Surf','fitness':'Fitness','urbano':'Urbano'};const key=String(value||'').toLowerCase();return labels[key]||String(value||'').replace(/-/g,' ').replace(/^./,m=>m.toUpperCase())}
function teEditorialReasons(n,own){const reasons=[];if(own)reasons.push('Contenido propio de Te Equipamos');else reasons.push(`Fuente identificada: ${n.source||'publicación original'}`);const sections=(n.sections||[]).map(tePublicSection).filter(Boolean);if(sections.length)reasons.push(`Sección: ${sections.slice(0,2).join(' · ')}`);const activities=(n.activities||[]).map(teActivityLabel).filter(Boolean);if(activities.length)reasons.push(`Actividad: ${activities.slice(0,2).join(' · ')}`);if(own&&n.product_type&&String(n.product_type).toLowerCase()!=='equipamiento')reasons.push(`Tipo de contenido: ${teActivityLabel(n.product_type)}`);if(!own)reasons.push('Enlace directo a la publicación original');return reasons.slice(0,4)}
function renderArticle(id){const n=NEWS.find(x=>x.id===Number(id));if(!n){history.replaceState({},'','./');renderPortal();return}$('#portal').classList.add('hidden');$('#articleView').classList.remove('hidden');document.title=`${n.title} — Te Equipamos`;const own=!!n.owned;const label=own?'Contenido Te Equipamos':'Actualidad';const published=teEditorialDate(n);const p=own?[n.summary,n.details||'Contenido propio de Te Equipamos.','Esta pieza forma parte del ecosistema de reviews, guías, novedades y landings de Te Equipamos.']:[n.summary,n.details||'Te Equipamos ha seleccionado esta información por su interés para el mundo outdoor.','Para ampliar contexto, datos, declaraciones y posibles actualizaciones, consulta siempre la publicación original enlazada.'];const button=own?'Abrir contenido de Te Equipamos →':`Leer noticia original en ${esc(n.source)} ↗`;const note=own?'<strong>Contenido propio:</strong> esta publicación enlaza a una review, guía, novedad o landing de Te Equipamos.':'<strong>Transparencia editorial:</strong> Te Equipamos organiza y presenta esta información para facilitar su descubrimiento. La autoría y el contenido completo pertenecen al medio enlazado.';const reasons=teEditorialReasons(n,own);const meta=[own?'Por Te Equipamos':`Selección: Te Equipamos`,published?`Publicado ${published}`:'',!own&&n.source?`Fuente: ${n.source}`:''].filter(Boolean);$('#article').innerHTML=`<img class="articleHero" src="${esc(n.image)}" alt="${esc(n.title)}"><div class="articleBody"><span class="kicker">${esc(n.category)} · ${label}</span><h1>${esc(n.title)}</h1><p class="deck">${esc(n.summary)}</p><div class="te-editorial-meta">${meta.map((x,i)=>`${i?'<span class="te-editorial-dot">•</span>':''}<strong>${esc(x)}</strong>`).join('')}<a href="./metodologia/">Cómo trabajamos →</a></div><div class="copy">${p.map((x,i)=>`${i===1?'<h2>Lo más importante</h2>':''}<p>${esc(x)}</p>`).join('')}<a class="sourceBtn" href="${esc(n.url)}" target="_blank" rel="noopener noreferrer">${button}</a></div><section class="te-editorial-why"><span>POR QUÉ ESTÁ AQUÍ</span><h2>Contexto editorial</h2><ul>${reasons.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></section><div class="note">${note} <a href="./metodologia/">Consulta nuestro criterio editorial.</a></div></div>`;const related=[...NEWS.filter(x=>x.id!==n.id)].sort((a,b)=>((b.category===n.category)-(a.category===n.category))||((b.owned?1:0)-(a.owned?1:0))||((b.score||0)-(a.score||0))).slice(0,6);$('#related').innerHTML=related.map(x=>`<div class="rel" data-article="${x.id}"><img class="relMedia" src="${esc(x.image)}" alt="${esc(x.title)}"><div class="relText"><span class="kicker">${esc(x.category)}${x.owned?' · Te Equipamos':''}</span>${freshBadge(x)}<b>${esc(cardTitle(x))}</b><small>${esc(cardMeta(x))}</small></div></div>`).join('')}
'''

html, n = re.subn(
    r"function renderArticle\(id\)\{.*?\}\ndocument\.addEventListener",
    lambda m: article_fn + "document.addEventListener",
    html,
    count=1,
    flags=re.S,
)
if n != 1:
    raise RuntimeError("No se pudo actualizar renderArticle")

target.write_text(html, encoding="utf-8")
print(f"Te Equipamos News actualizado con {len(data)} contenidos y tarjetas móviles compactas")

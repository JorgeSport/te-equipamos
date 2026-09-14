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

# Mejora exclusivamente responsive: el escritorio conserva su diseño actual.
mobile_css = r'''.relMedia{display:none}
@media(max-width:760px){
  .feed{border-left:0;border-right:0;border-radius:0;box-shadow:none;background:transparent}
  .card{display:flex;flex-direction:column;gap:0;padding:0 0 22px;margin:0 0 14px;background:var(--surface);border-bottom:8px solid var(--bg)}
  .card>div:first-child{padding:18px 18px 0}
  .card .thumb{order:-1;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover;border-radius:0}
  .card .title{font-size:23px;line-height:1.22;margin:8px 0 14px;letter-spacing:-.01em}
  .card .summary{display:none}
  .card .cardMeta{font-size:13px;padding-bottom:2px}
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

article_fn = r'''function renderArticle(id){const n=NEWS.find(x=>x.id===Number(id));if(!n){history.replaceState({},'','./');renderPortal();return}$('#portal').classList.add('hidden');$('#articleView').classList.remove('hidden');document.title=`${n.title} — Te Equipamos News`;const own=!!n.owned;const label=own?'Contenido Te Equipamos':'Actualidad';const p=own?[n.summary,n.details||'Contenido propio de Te Equipamos.','Esta pieza forma parte del ecosistema de reviews, guías, novedades y landings de Te Equipamos.']:[n.summary,n.details||'Te Equipamos News ha seleccionado esta información por su interés para el mundo outdoor.','Para ampliar contexto, datos, declaraciones y posibles actualizaciones, consulta siempre la publicación original enlazada.'];const button=own?'Abrir contenido de Te Equipamos →':`Leer noticia original en ${esc(n.source)} ↗`;const note=own?'<strong>Contenido propio:</strong> esta publicación enlaza a una review, guía, novedad o landing de Te Equipamos.':'<strong>Transparencia editorial:</strong> Te Equipamos organiza y presenta esta información para facilitar su descubrimiento. La autoría y el contenido completo pertenecen al medio enlazado.';$('#article').innerHTML=`<img class="articleHero" src="${esc(n.image)}" alt="${esc(n.title)}"><div class="articleBody"><span class="kicker">${esc(n.category)} · ${label}</span><h1>${esc(n.title)}</h1><p class="deck">${esc(n.summary)}</p><div class="byline"><strong>${own?esc(n.source):'Te Equipamos News'}</strong><span>•</span><span>${own?'Te Equipamos':'Fuente: '+esc(n.source)}</span><span>•</span><span>${esc(n.time)}</span></div><div class="copy">${p.map((x,i)=>`${i===1?'<h2>Lo más importante</h2>':''}<p>${esc(x)}</p>`).join('')}<a class="sourceBtn" href="${esc(n.url)}" target="_blank" rel="noopener noreferrer">${button}</a></div><div class="note">${note}</div></div>`;const related=[...NEWS.filter(x=>x.id!==n.id)].sort((a,b)=>((b.category===n.category)-(a.category===n.category))||((b.owned?1:0)-(a.owned?1:0))||((b.score||0)-(a.score||0))).slice(0,6);$('#related').innerHTML=related.map(x=>`<div class="rel" data-article="${x.id}"><img class="relMedia" src="${esc(x.image)}" alt="${esc(x.title)}"><div class="relText"><span class="kicker">${esc(x.category)}${x.owned?' · Te Equipamos':''}</span><b>${esc(x.title)}</b><small>${esc(x.source)} · ${esc(x.time)}</small></div></div>`).join('')}
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
print(f"Te Equipamos News actualizado con {len(data)} contenidos y responsive móvil mejorado")

from pathlib import Path
import re

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")

css = r'''/* TE_ACTIVE_TAGS */
.topic{cursor:pointer;position:relative;overflow:hidden;transition:transform .15s ease,box-shadow .15s ease,border-color .15s ease}.topic:hover{transform:translateY(-2px);box-shadow:0 5px 16px rgba(60,64,67,.10)}.topic:focus-visible{outline:3px solid var(--soft);outline-offset:2px}.topic[data-tone="green"]{border-top:3px solid #34a853;background:linear-gradient(180deg,rgba(52,168,83,.08),var(--surface) 52%)}.topic[data-tone="blue"]{border-top:3px solid #4285f4;background:linear-gradient(180deg,rgba(66,133,244,.08),var(--surface) 52%)}.topic[data-tone="amber"]{border-top:3px solid #f9ab00;background:linear-gradient(180deg,rgba(249,171,0,.09),var(--surface) 52%)}.topic[data-tone="violet"]{border-top:3px solid #7e57c2;background:linear-gradient(180deg,rgba(126,87,194,.08),var(--surface) 52%)}.topic.active{box-shadow:0 0 0 2px var(--accent) inset}.activityRow,.tagRow{display:flex;gap:6px;flex-wrap:wrap}.activityRow{margin:7px 0 6px}.tagRow{margin:0 0 12px}.tagPill{border:1px solid transparent;border-radius:999px;padding:5px 9px;font-size:10px;font-weight:800;line-height:1;cursor:pointer;transition:transform .12s ease,filter .12s ease}.tagPill:hover{transform:translateY(-1px);filter:saturate(1.15)}.tagPill.active{box-shadow:0 0 0 2px var(--text) inset}.activityPill{font-weight:900;letter-spacing:.01em}.tagPill.tone-green{background:#e8f5ec;color:#18763a;border-color:#cce9d5}.tagPill.tone-blue{background:#eaf2ff;color:#1769d2;border-color:#d2e2ff}.tagPill.tone-amber{background:#fff4d6;color:#8a5a00;border-color:#f7dfa2}.tagPill.tone-violet{background:#f1eafe;color:#6542a6;border-color:#dfd2f7}.tagPill.tone-neutral{background:var(--surface2);color:var(--muted);border-color:var(--line)}
/* TE_RESPONSIVE_NEUTRAL_TAGS */
@media(max-width:1100px){
  .activityRow{margin:5px 0 6px}.tagRow{margin:2px 0 10px}.tagPill{font-size:10px;padding:5px 8px;background:transparent!important;color:var(--muted)!important;border-color:var(--line)!important;box-shadow:none!important;filter:none!important}.tagPill:hover{transform:none;filter:none}.tagPill.activityPill{color:var(--text)!important;font-weight:800;letter-spacing:.01em}.tagPill.active{background:transparent!important;color:var(--text)!important;border-color:var(--text)!important;box-shadow:none!important}.topic{border-top-width:3px}
}
@media(prefers-color-scheme:dark){.tagPill.tone-green{background:#173523;color:#9bd6ad;border-color:#28553a}.tagPill.tone-blue{background:#172b49;color:#a8c7fa;border-color:#294a78}.tagPill.tone-amber{background:#3b2d10;color:#f8cf72;border-color:#654d18}.tagPill.tone-violet{background:#2d2144;color:#d4bbff;border-color:#49356d}}
'''
if '/* TE_ACTIVE_TAGS */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

pattern_topics = r"function renderTopics\(\)\{.*?\}\nfunction filtered"
new_topics = r'''function topicTone(t){const s=String(t||'').toLowerCase();if(/sender|trek|monta/.test(s))return'green';if(/running|correr|calzado/.test(s))return'blue';if(/oferta|segunda|precio/.test(s))return'amber';return'violet'}
function renderTopics(){$('#topics').innerHTML=TOPICS.map(t=>`<article class="topic ${state.q&&state.q.toLowerCase()===String(t[0]).toLowerCase()?'active':''}" data-topic="${esc(t[0])}" data-tone="${topicTone(t[0])}" tabindex="0" role="button" aria-label="Explorar ${esc(t[0])}"><div class="topicTop"><h3>${t[0]}</h3><button class="follow ${state.follow.has(t[0])?'on':''}" data-follow="${t[0]}">${state.follow.has(t[0])?'Siguiendo':'+ Seguir'}</button></div><p>${t[1]}</p><span class="kicker">Explorar tema →</span></article>`).join('')}
function filtered'''
html, count = re.subn(pattern_topics, new_topics, html, count=1, flags=re.S)
if count != 1 and 'function topicTone(' not in html:
    raise RuntimeError('No se pudo activar Temas destacados')

helpers = r'''function tagTone(t){const s=String(t||'').toLowerCase();if(/sender|trek|monta|mochila|outdoor|camp|alpin|escal/.test(s))return'green';if(/running|trail|calzado|zapat|mesh|cicl|nataci|kayak|surf/.test(s))return'blue';if(/oferta|segunda|verano|sol|frío|frio|esquí|esqui|nieve/.test(s))return'amber';if(/quechua|forclaz|mujer|niñ|infantil|travel|viaje/.test(s))return'violet';return'neutral'}
function teActivityLabel(v){if(typeof activityLabel==='function')return activityLabel(v);const m={'senderismo':'Senderismo','trekking':'Trekking','running':'Running','trail-running':'Trail running','ciclismo':'Ciclismo','natacion':'Natación','travel':'Travel','alpinismo':'Alpinismo','escalada':'Escalada','camping':'Camping','esqui':'Esquí y nieve','kayak':'Kayak y remo','surf':'Surf','fitness':'Fitness'};return m[String(v||'').toLowerCase()]||String(v||'')}
function renderActivityPills(n){const a=(n.activities||[]).slice(0,3);return a.length?`<div class="activityRow">${a.map(v=>`<button type="button" class="tagPill activityPill tone-${tagTone(teActivityLabel(v))} ${state.activity===v?'active':''}" data-activity-filter="${esc(v)}" aria-label="Ver actividad ${esc(teActivityLabel(v))}">${esc(teActivityLabel(v))}</button>`).join('')}</div>`:''}
function teNormalTags(n){const activityWords=/^(senderismo|trekking|running|trail running|trail-running|ciclismo|natación|natacion|travel|viaje|viajes|alpinismo|escalada|camping|esquí|esqui|nieve|kayak|remo|surf|fitness)$/i;return (n.tags||[]).filter(t=>!activityWords.test(String(t||'').trim())).slice(0,4)}
function renderTagPills(n){const tags=teNormalTags(n);return tags.length?`<div class="tagRow">${tags.map(t=>`<button type="button" class="tagPill tone-${tagTone(t)} ${state.q&&state.q.toLowerCase()===String(t).toLowerCase()?'active':''}" data-tag-filter="${esc(t)}" aria-label="Ver contenido sobre ${esc(t)}">${esc(t)}</button>`).join('')}</div>`:''}
'''
if 'function tagTone(' not in html:
    html = html.replace('function renderFeed(){', helpers + 'function renderFeed(){', 1)

old = '<p class="summary">${esc(n.summary)}</p><div class="cardMeta">'
new = '<p class="summary">${esc(n.summary)}</p>${renderActivityPills(n)}${renderTagPills(n)}<div class="cardMeta">'
if old in html:
    html = html.replace(old, new, 1)
elif '${renderActivityPills(n)}' not in html:
    raise RuntimeError('No se pudo añadir actividades y etiquetas a las tarjetas')

filter_js = r'''function applyTagFilter(value){const tag=String(value||'').trim();if(!tag)return;state.activity='';state.q=tag;state.cat='Todas';$('#searchInput').value=tag;renderNav();renderTopics();$('#following').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#hero').classList.add('hidden');renderFeed();const feed=document.getElementById('feedSection');if(feed)feed.scrollIntoView({behavior:'smooth',block:'start'})}
document.addEventListener('click',e=>{const activity=e.target.closest&&e.target.closest('[data-activity-filter]');if(activity){e.preventDefault();e.stopPropagation();if(typeof applyActivityFilter==='function')applyActivityFilter(activity.dataset.activityFilter);return}const tag=e.target.closest&&e.target.closest('[data-tag-filter]');if(tag){e.preventDefault();e.stopPropagation();applyTagFilter(tag.dataset.tagFilter);return}const topic=e.target.closest&&e.target.closest('[data-topic]');if(topic&&!e.target.closest('[data-follow]')){e.preventDefault();e.stopPropagation();applyTagFilter(topic.dataset.topic)}},true);
document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target&&e.target.matches&&e.target.matches('[data-topic]')){e.preventDefault();applyTagFilter(e.target.dataset.topic)}});
'''
if 'function applyTagFilter(' not in html:
    marker = "document.addEventListener('click',e=>{const a=e.target.closest('[data-article]');"
    if marker not in html:
        raise RuntimeError('No se encontró el controlador principal de clics')
    html = html.replace(marker, filter_js + marker, 1)

path.write_text(html, encoding='utf-8')
print('Actividades y etiquetas activas: responsive neutro y elegante; colores reservados a escritorio')

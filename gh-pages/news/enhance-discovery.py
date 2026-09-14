from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

css = r'''/* TE_DISCOVERY_PHASE1 */
.search{position:relative}.searchSuggest{position:absolute;left:0;right:0;top:50px;z-index:80;background:var(--surface);border:1px solid var(--line);border-radius:16px;box-shadow:0 12px 30px rgba(32,33,36,.16);overflow:hidden;display:none}.searchSuggest.show{display:block}.searchSuggest button{width:100%;display:grid;grid-template-columns:50px minmax(0,1fr);gap:11px;align-items:center;border:0;border-bottom:1px solid var(--line);background:var(--surface);padding:9px 11px;text-align:left;cursor:pointer}.searchSuggest button:last-child{border-bottom:0}.searchSuggest button:hover,.searchSuggest button.active{background:var(--surface2)}.searchSuggest img{width:50px;height:42px;border-radius:8px;object-fit:cover}.searchSuggest strong{display:block;font-size:13px;line-height:1.25}.searchSuggest small{display:block;margin-top:3px;color:var(--muted);font-size:10px}.saleFilters{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;margin:0 0 13px;padding:2px 0}.saleFilters::-webkit-scrollbar{display:none}.saleFilter{border:1px solid var(--line);background:var(--surface);color:var(--muted);border-radius:999px;padding:8px 12px;font-size:11px;font-weight:800;white-space:nowrap;cursor:pointer}.saleFilter:hover{background:var(--surface2)}.saleFilter.active{background:var(--text);border-color:var(--text);color:var(--surface)}.recentSection{margin-top:30px}.recentHead{display:flex;align-items:end;justify-content:space-between;gap:12px;margin-bottom:12px}.recentHead h2{margin:0;font-size:22px}.recentHead p{margin:5px 0 0;color:var(--muted);font-size:13px}.recentClear{border:0;background:transparent;color:var(--accent);font-size:11px;font-weight:800;cursor:pointer}.recentGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.recentCard{display:grid;grid-template-columns:105px minmax(0,1fr);gap:0;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;cursor:pointer;min-height:90px}.recentCard:hover{box-shadow:var(--shadow)}.recentCard img{width:105px;height:100%;min-height:90px;object-fit:cover}.recentCard div{padding:11px 12px}.recentCard small{display:block;color:var(--accent);font-size:9px;font-weight:900;text-transform:uppercase;margin-bottom:5px}.recentCard b{display:block;font-size:14px;line-height:1.25}.savedHeader{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:14px 0 10px}.savedHeader h3{margin:0;font-size:18px}.savedCount{background:var(--soft);color:var(--accent);border-radius:999px;padding:5px 9px;font-size:11px;font-weight:900}.save{border-radius:50%;width:32px;height:32px;display:grid;place-items:center}.save:hover{background:var(--surface2)}.save.on{background:var(--soft)}
@media(max-width:760px){.searchSuggest{top:47px;border-radius:13px}.searchSuggest button{grid-template-columns:46px minmax(0,1fr);padding:8px 10px}.searchSuggest img{width:46px;height:39px}.saleFilters{margin:0 -2px 12px;padding:2px}.saleFilter{padding:7px 11px}.recentSection{margin-top:24px}.recentGrid{grid-template-columns:1fr}.recentCard{grid-template-columns:92px minmax(0,1fr);min-height:82px}.recentCard img{width:92px;min-height:82px}.recentHead h2{font-size:20px}}
@media(prefers-color-scheme:dark){.searchSuggest{box-shadow:0 12px 30px rgba(0,0,0,.35)}}
'''
if '/* TE_DISCOVERY_PHASE1 */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

js = r'''/* TE_DISCOVERY_PHASE1_JS */
let teSaleFilter='Todos';
const TE_SALE_FILTERS=[
 ['Todos',()=>true],
 ['Mochilas',n=>/mochila|backpack|rolltop|\b\d+\s*l\b/i.test(teHay(n))],
 ['Ropa',n=>/camiseta|pantal[oó]n|chaqueta|plum[oó]n|impermeable|mesh|shirt|textil/i.test(teHay(n))],
 ['Calzado',n=>/zapat|sandalia|bota|calzado/i.test(teHay(n))],
 ['Mujer',n=>/mujer|woman/i.test(teHay(n))],
 ['Hombre',n=>/hombre|men\b/i.test(teHay(n))],
 ['Infantil',n=>/niñ|infantil|kids|junior/i.test(teHay(n))],
 ['Segunda mano',n=>/segunda mano|usado|como nuevo/i.test(teHay(n))],
 ['Oferta',n=>(n.sections||[]).includes('Ofertas')||/oferta|remate|promoci/i.test(teHay(n))]
];
function teHay(n){return `${n.title||''} ${n.summary||''} ${n.category||''} ${(n.tags||[]).join(' ')} ${(n.sections||[]).join(' ')}`.toLowerCase()}
function teSaleMatch(n){const row=TE_SALE_FILTERS.find(x=>x[0]===teSaleFilter);return !row||row[1](n)}
const teBaseFiltered=filtered;
filtered=function(){const list=teBaseFiltered();return state.cat==='Ventas'&&teSaleFilter!=='Todos'?list.filter(teSaleMatch):list};

function ensureSaleFilters(){let box=document.getElementById('saleFilters');if(!box){box=document.createElement('div');box.id='saleFilters';box.className='saleFilters hidden';const feed=document.getElementById('feed');if(feed&&feed.parentNode)feed.parentNode.insertBefore(box,feed)}return box}
function renderSaleFilters(){const box=ensureSaleFilters();if(!box)return;const visible=state.cat==='Ventas'&&!state.q;box.classList.toggle('hidden',!visible);if(!visible)return;const sales=NEWS.filter(n=>n.category==='Ventas'||(n.sections||[]).includes('Ventas'));const available=TE_SALE_FILTERS.filter((row,i)=>i===0||sales.some(row[1]));if(!available.some(x=>x[0]===teSaleFilter))teSaleFilter='Todos';box.innerHTML=available.map(([name])=>`<button type="button" class="saleFilter ${name===teSaleFilter?'active':''}" data-sale-filter="${name}">${name}</button>`).join('')}

function teRecentIds(){try{return JSON.parse(localStorage.getItem('teRecentItems')||'[]').map(Number).filter(Boolean)}catch(e){return[]}}
function recordRecent(id){id=Number(id);if(!id)return;const ids=teRecentIds().filter(x=>x!==id);ids.unshift(id);localStorage.setItem('teRecentItems',JSON.stringify(ids.slice(0,8)))}
function ensureRecent(){let sec=document.getElementById('recentSection');if(!sec){sec=document.createElement('section');sec.id='recentSection';sec.className='recentSection hidden';const topics=document.getElementById('topicsSection');if(topics&&topics.parentNode)topics.parentNode.insertBefore(sec,topics.nextSibling)}return sec}
function renderRecent(){const sec=ensureRecent();if(!sec)return;const items=teRecentIds().map(id=>NEWS.find(n=>Number(n.id)===id)).filter(Boolean).slice(0,4);const show=state.cat==='Todas'&&!state.q&&items.length;sec.classList.toggle('hidden',!show);if(!show)return;sec.innerHTML=`<div class="recentHead"><div><h2>Visto recientemente</h2><p>Continúa donde lo dejaste.</p></div><button type="button" class="recentClear" id="recentClear">Limpiar</button></div><div class="recentGrid">${items.map(n=>`<article class="recentCard" data-article="${n.id}"><img src="${esc(n.image)}" alt="${esc(n.title)}"><div><small>${esc(n.category||'Te Equipamos')}</small><b>${esc(n.title)}</b></div></article>`).join('')}</div>`}

function ensureSuggestions(){let box=document.getElementById('searchSuggest');if(!box){box=document.createElement('div');box.id='searchSuggest';box.className='searchSuggest';box.setAttribute('role','listbox');const form=document.getElementById('searchForm');if(form)form.appendChild(box)}return box}
let teSuggestIndex=-1;
function closeSuggestions(){const box=document.getElementById('searchSuggest');if(box){box.classList.remove('show');box.innerHTML=''}teSuggestIndex=-1}
function renderSuggestions(value){const q=String(value||'').trim().toLowerCase();const box=ensureSuggestions();if(!box||q.length<1){closeSuggestions();return}const rows=NEWS.map(n=>({n,pos:teHay(n).indexOf(q)})).filter(x=>x.pos>=0).sort((a,b)=>a.pos-b.pos||Number(b.n.score||0)-Number(a.n.score||0)).slice(0,6).map(x=>x.n);if(!rows.length){closeSuggestions();return}box.innerHTML=rows.map(n=>`<button type="button" data-suggest-id="${n.id}" role="option"><img src="${esc(n.image)}" alt=""><span><strong>${esc(n.title)}</strong><small>${esc((n.tags||[]).slice(0,2).join(' · ')||(n.sections||[])[0]||n.category||'Te Equipamos')}</small></span></button>`).join('');box.classList.add('show');teSuggestIndex=-1}
function openSuggestion(id){const n=NEWS.find(x=>Number(x.id)===Number(id));if(!n)return;recordRecent(n.id);closeSuggestions();if(n.direct&&n.url){location.assign(n.url);return}openArticle(n.id)}

const teBaseRenderFeed=renderFeed;
renderFeed=function(){teBaseRenderFeed();renderSaleFilters();renderRecent()};
const teBaseSetCat=setCat;
setCat=function(c){if(c!=='Ventas')teSaleFilter='Todos';teBaseSetCat(c);renderSaleFilters();renderRecent();closeSuggestions()};
const teBaseRenderPortal=renderPortal;
renderPortal=function(){teBaseRenderPortal();renderSaleFilters();renderRecent();const section=new URLSearchParams(location.search).get('section');if(section&&CATS.includes(section)&&section!=='Todas'&&section!=='Siguiendo'){setTimeout(()=>setCat(section),0)}};
const teBaseRenderFollowing=renderFollowing;
renderFollowing=function(){teBaseRenderFollowing();const host=document.getElementById('saved');if(host&&!document.getElementById('savedHeader')){const h=document.createElement('div');h.id='savedHeader';h.className='savedHeader';h.innerHTML=`<h3>Guardados</h3><span class="savedCount">${state.saved.size}</span>`;host.parentNode.insertBefore(h,host)}else{const c=document.querySelector('#savedHeader .savedCount');if(c)c.textContent=state.saved.size}};

document.addEventListener('click',e=>{const f=e.target.closest&&e.target.closest('[data-sale-filter]');if(f){e.preventDefault();teSaleFilter=f.dataset.saleFilter;renderFeed();return}const s=e.target.closest&&e.target.closest('[data-suggest-id]');if(s){e.preventDefault();openSuggestion(s.dataset.suggestId);return}const a=e.target.closest&&e.target.closest('[data-article]');if(a)recordRecent(a.dataset.article);if(e.target&&e.target.id==='recentClear'){localStorage.removeItem('teRecentItems');renderRecent();return}if(!e.target.closest||!e.target.closest('#searchForm'))closeSuggestions()},true);

const teSearch=document.getElementById('searchInput');
if(teSearch){teSearch.addEventListener('input',e=>renderSuggestions(e.target.value));teSearch.addEventListener('keydown',e=>{const box=document.getElementById('searchSuggest');if(!box||!box.classList.contains('show'))return;const rows=[...box.querySelectorAll('[data-suggest-id]')];if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();teSuggestIndex=(teSuggestIndex+(e.key==='ArrowDown'?1:-1)+rows.length)%rows.length;rows.forEach((r,i)=>r.classList.toggle('active',i===teSuggestIndex));rows[teSuggestIndex]?.scrollIntoView({block:'nearest'})}else if(e.key==='Enter'&&teSuggestIndex>=0){e.preventDefault();openSuggestion(rows[teSuggestIndex].dataset.suggestId)}else if(e.key==='Escape')closeSuggestions()})}
const teClear=document.getElementById('clearBtn');if(teClear)teClear.addEventListener('click',()=>closeSuggestions());
'''

if '/* TE_DISCOVERY_PHASE1_JS */' not in html:
    marker = "document.addEventListener('click',e=>{const a=e.target.closest('[data-article]');"
    if marker not in html:
        raise RuntimeError('No se encontró el controlador principal para instalar descubrimiento')
    html = html.replace(marker, js + marker, 1)

path.write_text(html, encoding='utf-8')
print('Descubrimiento mejorado: búsqueda predictiva, filtros, vistos recientemente y guardados')

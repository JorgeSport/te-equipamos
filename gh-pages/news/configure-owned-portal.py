from pathlib import Path
import re

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")

# Menú editorial de Te Equipamos. Las actividades viven como una segunda capa de navegación.
html = re.sub(
    r"const CATS=\[[^;]+\];",
    "const CATS=['Todas','Ventas','Reviews','Ofertas','Novedades','Vídeos','Consejos','Siguiendo'];",
    html,
    count=1,
)
html = re.sub(
    r"const TOPICS=\[[^;]+\];",
    "const TOPICS=[['Senderismo','Productos, reviews y consejos para caminar mejor equipado.'],['Running','Equipamiento, pruebas y contenidos para correr.'],['Ciclismo','Selección y contenidos propios relacionados con la bici.']];",
    html,
    count=1,
)

html = html.replace("c==='Todas'?'Principal':c", "c==='Todas'?'Inicio':c")
html = html.replace("c==='Todas'?'⌂ Principal':c==='Siguiendo'?'★ Siguiendo':c", "c==='Todas'?'⌂ Inicio':c==='Siguiendo'?'★ Siguiendo':c")

# Un contenido puede pertenecer a varios menús y a varias actividades reales.
html = re.sub(
    r"function filtered\(\)\{return NEWS\.filter\(n=>\(state\.cat==='Todas'\|\|state\.cat==='Para ti'\|\|n\.category===state\.cat\)&&\(!state\.q\|\|\(`\$\{n\.title\} \$\{n\.summary\} \$\{n\.category\} \$\{n\.source\}`\)\.toLowerCase\(\)\.includes\(state\.q\.toLowerCase\(\)\)\)\)\}",
    "function filtered(){return NEWS.filter(n=>(state.cat==='Todas'||n.category===state.cat||(Array.isArray(n.sections)&&n.sections.includes(state.cat)))&&(!state.activity||(Array.isArray(n.activities)&&n.activities.includes(state.activity)))&&(!state.q||(`${n.title} ${n.summary} ${n.category} ${n.source} ${(n.sections||[]).join(' ')} ${(n.activities||[]).join(' ')} ${n.product_type||''} ${(n.tags||[]).join(' ')}`).toLowerCase().includes(state.q.toLowerCase())))}",
    html,
    count=1,
)

html = html.replace('placeholder="Buscar temas, noticias y fuentes"', 'placeholder="Buscar productos, reviews, actividades y consejos"')
html = html.replace('<h1>Tu resumen</h1>', '<h1>Te Equipamos</h1>')
html = html.replace('<small>Madrid</small><strong>Actualidad y novedades</strong>', '<small>Contenido propio</small><strong>Deporte · Aventura · Actividades</strong>')
html = html.replace('<h2 id="feedTitle">Últimas noticias</h2>', '<h2 id="feedTitle">Últimos contenidos</h2>')
html = html.replace('Información organizada para leer de un vistazo', 'Todo lo nuevo de Te Equipamos, organizado para leer de un vistazo')
html = html.replace("state.cat==='Todas'?'Últimas noticias':state.cat", "state.cat==='Todas'?'Últimos contenidos':state.cat")
html = html.replace("state.cat==='Todas'?'Información organizada para leer de un vistazo':`Últimas noticias de ${state.cat.toLowerCase()}`", "state.cat==='Todas'?'Todo lo nuevo de Te Equipamos, organizado para leer de un vistazo':`Contenido de ${state.cat.toLowerCase()}`")
html = html.replace('<h3>Lo más leído</h3>', '<h3>Destacados</h3>')
html = html.replace('<span class="kicker">Resumen diario</span><h3>Las noticias importantes, sin ruido.</h3><p class="summary">Noticias, guías, reviews y selección outdoor de Te Equipamos.</p>', '<span class="kicker">TE EQUIPAMOS</span><h3>Todo nuestro contenido, en un solo lugar.</h3><p class="summary">Productos, reviews, ofertas y contenidos para distintas actividades.</p>')

html = html.replace('<span class="kicker">Tema de ejemplo</span>', '<span class="kicker">Explorar tema</span>')
html = html.replace('<h3>No encontramos noticias</h3><p>Prueba otra búsqueda o categoría.</p>', '<h3>Aún no hay contenido en esta sección</h3><p>Cuando publiquemos algo nuevo, aparecerá aquí automáticamente.</p>')

html = re.sub(
    r'<div class="demo"><b>EDICIÓN OUTDOOR · [^<]+</b><span>[^<]+</span></div>',
    '<div class="demo hidden" id="portalIntro"><b>CONTENIDO PROPIO · TE EQUIPAMOS</b><span>Productos, reviews, vídeos, consejos, ofertas y novedades organizados por actividad.</span></div>',
    html,
    count=1,
)

activity_empty_css = r'''/* TE_ACTIVITY_EMPTY_STATE */
#empty.activityEmptyPanel{display:block!important;text-align:left;padding:30px 32px;background:var(--surface);border:1px solid var(--line);border-radius:18px;box-shadow:var(--shadow);color:var(--text)}
#empty.activityEmptyPanel .activityEmptyEyebrow{display:block;margin-bottom:8px;color:var(--muted);font-size:11px;font-weight:800;letter-spacing:.06em;text-transform:uppercase}
#empty.activityEmptyPanel h3{margin:0 0 8px;font-size:24px;line-height:1.2;letter-spacing:-.02em}
#empty.activityEmptyPanel p{margin:0;max-width:620px;color:var(--muted);font-size:14px;line-height:1.55}
.activityAlternatives{margin-top:52px}
.activityAlternativesHead{margin-bottom:14px}
.activityAlternativesHead h3{margin:0 0 5px;font-size:20px;letter-spacing:-.02em}
.activityAlternativesHead p{margin:0;color:var(--muted);font-size:13px}
.activityAlternativesGrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.activityAlternative{border:1px solid var(--line);background:var(--surface);color:var(--text);border-radius:15px;padding:15px 16px;text-align:left;cursor:pointer}
.activityAlternative:hover{background:var(--surface2)}
.activityAlternative strong{display:block;font-size:14px}
.activityAlternative small{display:block;margin-top:5px;color:var(--muted);font-size:11px}
@media(max-width:760px){#empty.activityEmptyPanel{padding:24px 20px;border-radius:16px}#empty.activityEmptyPanel h3{font-size:21px}.activityAlternatives{margin-top:38px;padding:0 2px}.activityAlternativesGrid{grid-template-columns:1fr 1fr;gap:8px}.activityAlternative{padding:13px 14px}}
'''
if '/* TE_ACTIVITY_EMPTY_STATE */' not in html:
    html = html.replace('</style>', activity_empty_css + '</style>', 1)

old_setcat = "function setCat(c){state.cat=c;state.q='';$('#searchInput').value='';renderNav();if(c==='Siguiendo'){$('#following').classList.remove('hidden');$('#feedSection').classList.add('hidden');$('#hero').classList.add('hidden');$('#topicsSection').classList.add('hidden');renderFollowing()}else{$('#following').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#topicsSection').classList.remove('hidden');$('#hero').classList.toggle('hidden',c!=='Todas');renderFeed()}closeMenu();scrollTo({top:0,behavior:'smooth'})}"
new_setcat = """const SECTION_COPY={
'Ventas':['Productos disponibles','Explora el catálogo actual de Te Equipamos.'],
'Reviews':['Reviews y análisis','Pruebas, análisis y experiencias con equipamiento.'],
'Vídeos':['Vídeos Te Equipamos','Demostraciones, pruebas y contenido visual de nuestros productos.'],
'Consejos':['Consejos y guías','Información práctica para elegir y usar mejor tu equipamiento.'],
'Ofertas':['Ofertas actuales','Oportunidades y promociones disponibles ahora.'],
'Novedades':['Lo último de Te Equipamos','Nuevos productos, contenidos y publicaciones.']};
const ACTIVITY_LABELS={'senderismo':'Senderismo','trekking':'Trekking','running':'Running','trail-running':'Trail running','ciclismo':'Ciclismo','natacion':'Natación','travel':'Travel','alpinismo':'Alpinismo','escalada':'Escalada','camping':'Camping','esqui':'Esquí y nieve','kayak':'Kayak y remo','surf':'Surf','fitness':'Fitness'};
function activityLabel(value){return ACTIVITY_LABELS[String(value||'').toLowerCase()]||String(value||'').replace(/-/g,' ').replace(/^./,m=>m.toUpperCase())}
function updateSectionHead(c){if(c==='Todas'||c==='Siguiendo'||state.q||state.activity)return;const copy=SECTION_COPY[c]||[c,`Contenido de ${c.toLowerCase()}`];const count=filtered().length;$('#feedTitle').textContent=copy[0];$('#feedSub').textContent=count?`${copy[1]} · ${count} ${count===1?'contenido':'contenidos'}`:copy[1]}
function ensureActivityAlternatives(){let host=document.getElementById('activityAlternatives');if(host)return host;host=document.createElement('section');host.id='activityAlternatives';host.className='activityAlternatives hidden';const feedSection=document.getElementById('feedSection');if(feedSection)feedSection.insertAdjacentElement('afterend',host);return host}
function clearActivityEmptyState(){const feed=document.getElementById('feed');const empty=document.getElementById('empty');const alt=document.getElementById('activityAlternatives');if(feed)feed.classList.remove('hidden');if(empty){empty.classList.remove('activityEmptyPanel');empty.innerHTML='<h3>Aún no hay contenido en esta sección</h3><p>Cuando publiquemos algo nuevo, aparecerá aquí automáticamente.</p>'}if(alt){alt.classList.add('hidden');alt.innerHTML=''}}
function renderActivityAlternatives(slug){const host=ensureActivityAlternatives();if(!host)return;const options=Object.entries(ACTIVITY_LABELS).map(([key,label])=>({key,label,count:NEWS.filter(n=>Array.isArray(n.activities)&&n.activities.includes(key)).length})).filter(x=>x.key!==slug&&x.count>0).sort((a,b)=>b.count-a.count||a.label.localeCompare(b.label,'es')).slice(0,6);if(!options.length){host.classList.add('hidden');host.innerHTML='';return}host.classList.remove('hidden');host.innerHTML=`<div class="activityAlternativesHead"><h3>También puedes explorar</h3><p>Mientras añadimos contenido a esta actividad, aquí tienes otras opciones disponibles.</p></div><div class="activityAlternativesGrid">${options.map(x=>`<button type="button" class="activityAlternative" data-activity-alt="${esc(x.key)}"><strong>${esc(x.label)}</strong><small>${x.count} ${x.count===1?'contenido':'contenidos'}</small></button>`).join('')}</div>`}
function renderActivityState(slug,count){const feed=document.getElementById('feed');const empty=document.getElementById('empty');const journey=document.getElementById('sectionJourney');if(count>0){if(feed)feed.classList.remove('hidden');if(empty){empty.classList.remove('activityEmptyPanel');empty.classList.add('hidden')}const alt=document.getElementById('activityAlternatives');if(alt){alt.classList.add('hidden');alt.innerHTML=''}return}const label=activityLabel(slug);if(feed)feed.classList.add('hidden');if(empty){empty.classList.remove('hidden');empty.classList.add('activityEmptyPanel');empty.innerHTML=`<span class="activityEmptyEyebrow">${esc(label)}</span><h3>Aún no hay contenido en ${esc(label)}</h3><p>Todavía no hemos publicado productos, reviews o guías para esta actividad. En cuanto añadamos contenido, aparecerá aquí automáticamente.</p>`}if(journey)journey.classList.add('hidden');renderActivityAlternatives(slug)}
function scrollActivityResultsStart(){requestAnimationFrame(()=>requestAnimationFrame(()=>{const target=document.querySelector('#feed .card')||document.querySelector('#empty.activityEmptyPanel');if(!target)return;const sticky=document.querySelector('.top');const responsive=window.matchMedia('(max-width:1100px)').matches;const offset=responsive?((sticky?sticky.getBoundingClientRect().height:0)+12):24;const y=Math.max(0,window.scrollY+target.getBoundingClientRect().top-offset);window.scrollTo({top:y,behavior:'smooth'})}))}
function applyActivityFilter(value){const slug=String(value||'').trim().toLowerCase();if(!slug)return;state.activity=slug;state.q='';state.cat='Todas';$('#searchInput').value='';renderNav();$('#following').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#hero').classList.add('hidden');$('#topicsSection').classList.add('hidden');const welcome=document.querySelector('.welcome');if(welcome)welcome.classList.add('hidden');renderFeed();const count=filtered().length;const label=activityLabel(slug);$('#feedTitle').textContent=label;$('#feedSub').textContent=count?`${count} ${count===1?'contenido':'contenidos'} para esta actividad`:'Contenido de esta actividad';renderActivityState(slug,count);scrollActivityResultsStart()}
function setCat(c){state.cat=c;state.q='';state.activity='';$('#searchInput').value='';clearActivityEmptyState();renderNav();const home=c==='Todas';const intro=$('#portalIntro');const welcome=document.querySelector('.welcome');if(intro)intro.classList.add('hidden');if(welcome)welcome.classList.toggle('hidden',!home);$('#topicsSection').classList.add('hidden');if(c==='Siguiendo'){$('#following').classList.remove('hidden');$('#feedSection').classList.add('hidden');$('#hero').classList.add('hidden');renderFollowing()}else{$('#following').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#hero').classList.toggle('hidden',!home);renderFeed();updateSectionHead(c)}closeMenu();scrollTo({top:0,behavior:'smooth'})}
document.addEventListener('click',e=>{const alt=e.target.closest&&e.target.closest('[data-activity-alt]');if(alt){e.preventDefault();applyActivityFilter(alt.dataset.activityAlt||'')}});
document.addEventListener('input',e=>{if(e.target&&e.target.id==='searchInput'&&e.target.value.trim()){state.activity='';clearActivityEmptyState()}});"""
if old_setcat in html:
    html = html.replace(old_setcat, new_setcat, 1)
elif "const SECTION_COPY=" not in html:
    raise RuntimeError("No se encontró la función setCat para mejorar la navegación")

old_portal = "function renderPortal(){document.title='Te Equipamos News';$('#portal').classList.remove('hidden');$('#articleView').classList.add('hidden');renderNav();renderHero();renderTopics();renderFeed();renderTrend();$('#today').textContent=new Intl.DateTimeFormat('es-ES',{weekday:'long',day:'numeric',month:'long'}).format(new Date()).replace(/^./,m=>m.toUpperCase())}"
new_portal = "function renderPortal(){document.title='Te Equipamos';state.cat='Todas';state.activity='';$('#portal').classList.remove('hidden');$('#articleView').classList.add('hidden');clearActivityEmptyState();const intro=$('#portalIntro');const welcome=document.querySelector('.welcome');if(intro)intro.classList.add('hidden');if(welcome)welcome.classList.remove('hidden');$('#hero').classList.remove('hidden');$('#topicsSection').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#following').classList.add('hidden');renderNav();renderHero();renderTopics();renderFeed();renderTrend();$('#today').textContent=new Intl.DateTimeFormat('es-ES',{weekday:'long',day:'numeric',month:'long'}).format(new Date()).replace(/^./,m=>m.toUpperCase())}"
if old_portal in html:
    html = html.replace(old_portal, new_portal, 1)

path.write_text(html, encoding="utf-8")
print("Portal preparado para actividades reales, estados vacíos y alternativas separadas")

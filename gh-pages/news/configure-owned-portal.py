from pathlib import Path
import re

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")

# Menú propio de Te Equipamos. Se conserva el diseño y solo cambia la organización del contenido.
html = re.sub(
    r"const CATS=\[[^;]+\];",
    "const CATS=['Todas','Ventas','Reviews','Vídeos','Consejos','Ofertas','Novedades','Siguiendo'];",
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

# Un contenido puede pertenecer a varios menús mediante el campo sections.
html = re.sub(
    r"function filtered\(\)\{return NEWS\.filter\(n=>\(state\.cat==='Todas'\|\|state\.cat==='Para ti'\|\|n\.category===state\.cat\)&&\(!state\.q\|\|\(`\$\{n\.title\} \$\{n\.summary\} \$\{n\.category\} \$\{n\.source\}`\)\.toLowerCase\(\)\.includes\(state\.q\.toLowerCase\(\)\)\)\)\}",
    "function filtered(){return NEWS.filter(n=>(state.cat==='Todas'||n.category===state.cat||(Array.isArray(n.sections)&&n.sections.includes(state.cat)))&&(!state.q||(`${n.title} ${n.summary} ${n.category} ${n.source} ${(n.sections||[]).join(' ')} ${(n.tags||[]).join(' ')}`).toLowerCase().includes(state.q.toLowerCase())))}",
    html,
    count=1,
)

html = html.replace('placeholder="Buscar temas, noticias y fuentes"', 'placeholder="Buscar productos, reviews, vídeos y consejos"')
html = html.replace('<h1>Tu resumen</h1>', '<h1>Te Equipamos</h1>')
html = html.replace('<small>Madrid</small><strong>Actualidad y novedades</strong>', '<small>Contenido propio</small><strong>Outdoor · Reviews · Ventas</strong>')
html = html.replace('<h2 id="feedTitle">Últimas noticias</h2>', '<h2 id="feedTitle">Últimos contenidos</h2>')
html = html.replace('Información organizada para leer de un vistazo', 'Todo lo nuevo de Te Equipamos, organizado para leer de un vistazo')
html = html.replace("state.cat==='Todas'?'Últimas noticias':state.cat", "state.cat==='Todas'?'Últimos contenidos':state.cat")
html = html.replace("state.cat==='Todas'?'Información organizada para leer de un vistazo':`Últimas noticias de ${state.cat.toLowerCase()}`", "state.cat==='Todas'?'Todo lo nuevo de Te Equipamos, organizado para leer de un vistazo':`Contenido de ${state.cat.toLowerCase()}`")
html = html.replace('<h3>Lo más leído</h3>', '<h3>Destacados</h3>')
html = html.replace('<span class="kicker">Resumen diario</span><h3>Las noticias importantes, sin ruido.</h3><p class="summary">Noticias, guías, reviews y selección outdoor de Te Equipamos.</p>', '<span class="kicker">TE EQUIPAMOS</span><h3>Todo nuestro contenido, en un solo lugar.</h3><p class="summary">Ventas, reviews, vídeos, consejos, ofertas y novedades publicadas desde GitHub.</p>')

# Elimina cualquier lenguaje heredado de la demo.
html = html.replace('<span class="kicker">Tema de ejemplo</span>', '<span class="kicker">Explorar tema</span>')
html = html.replace('<h3>No encontramos noticias</h3><p>Prueba otra búsqueda o categoría.</p>', '<h3>Aún no hay contenido en esta sección</h3><p>Cuando publiquemos algo nuevo en GitHub aparecerá aquí automáticamente.</p>')

# apply-real-news.py genera este aviso durante el despliegue; aquí se convierte en identidad del nuevo portal.
html = re.sub(
    r'<div class="demo"><b>EDICIÓN OUTDOOR · [^<]+</b><span>[^<]+</span></div>',
    '<div class="demo" id="portalIntro"><b>CONTENIDO PROPIO · GITHUB</b><span>Ventas, reviews, vídeos, consejos, ofertas y novedades de Te Equipamos. Cada publicación se clasifica automáticamente desde su repositorio.</span></div>',
    html,
    count=1,
)

# Navegación profesional: en submenús se muestra directamente el contenido solicitado.
# Temas destacados, hero e introducción general quedan exclusivamente en Inicio.
old_setcat = "function setCat(c){state.cat=c;state.q='';$('#searchInput').value='';renderNav();if(c==='Siguiendo'){$('#following').classList.remove('hidden');$('#feedSection').classList.add('hidden');$('#hero').classList.add('hidden');$('#topicsSection').classList.add('hidden');renderFollowing()}else{$('#following').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#topicsSection').classList.remove('hidden');$('#hero').classList.toggle('hidden',c!=='Todas');renderFeed()}closeMenu();scrollTo({top:0,behavior:'smooth'})}"
new_setcat = """const SECTION_COPY={
'Ventas':['Productos disponibles','Explora el catálogo actual de Te Equipamos.'],
'Reviews':['Reviews y análisis','Pruebas, análisis y experiencias con equipamiento outdoor.'],
'Vídeos':['Vídeos Te Equipamos','Demostraciones, pruebas y contenido visual de nuestros productos.'],
'Consejos':['Consejos y guías','Información práctica para elegir y usar mejor tu equipamiento.'],
'Ofertas':['Ofertas actuales','Oportunidades y promociones disponibles ahora.'],
'Novedades':['Lo último de Te Equipamos','Nuevos productos, contenidos y publicaciones.']};
function updateSectionHead(c){if(c==='Todas'||c==='Siguiendo'||state.q)return;const copy=SECTION_COPY[c]||[c,`Contenido de ${c.toLowerCase()}`];const count=filtered().length;$('#feedTitle').textContent=copy[0];$('#feedSub').textContent=count?`${copy[1]} · ${count} ${count===1?'contenido':'contenidos'}`:copy[1]}
function setCat(c){state.cat=c;state.q='';$('#searchInput').value='';renderNav();const home=c==='Todas';const intro=$('#portalIntro');const welcome=document.querySelector('.welcome');if(intro)intro.classList.toggle('hidden',!home);if(welcome)welcome.classList.toggle('hidden',!home);if(c==='Siguiendo'){$('#following').classList.remove('hidden');$('#feedSection').classList.add('hidden');$('#hero').classList.add('hidden');$('#topicsSection').classList.add('hidden');renderFollowing()}else{$('#following').classList.add('hidden');$('#feedSection').classList.remove('hidden');$('#topicsSection').classList.toggle('hidden',!home);$('#hero').classList.toggle('hidden',!home);renderFeed();updateSectionHead(c)}closeMenu();scrollTo({top:0,behavior:'smooth'})}"""
if old_setcat in html:
    html = html.replace(old_setcat, new_setcat, 1)
elif "const SECTION_COPY=" not in html:
    raise RuntimeError("No se encontró la función setCat para mejorar la navegación")

# Cuando se vuelve a Inicio mediante historial, restaurar los bloques exclusivos de portada.
old_portal = "function renderPortal(){document.title='Te Equipamos News';$('#portal').classList.remove('hidden');$('#articleView').classList.add('hidden');renderNav();renderHero();renderTopics();renderFeed();renderTrend();$('#today').textContent=new Intl.DateTimeFormat('es-ES',{weekday:'long',day:'numeric',month:'long'}).format(new Date()).replace(/^./,m=>m.toUpperCase())}"
new_portal = "function renderPortal(){document.title='Te Equipamos News';state.cat='Todas';$('#portal').classList.remove('hidden');$('#articleView').classList.add('hidden');const intro=$('#portalIntro');const welcome=document.querySelector('.welcome');if(intro)intro.classList.remove('hidden');if(welcome)welcome.classList.remove('hidden');$('#hero').classList.remove('hidden');$('#topicsSection').classList.remove('hidden');$('#feedSection').classList.remove('hidden');$('#following').classList.add('hidden');renderNav();renderHero();renderTopics();renderFeed();renderTrend();$('#today').textContent=new Intl.DateTimeFormat('es-ES',{weekday:'long',day:'numeric',month:'long'}).format(new Date()).replace(/^./,m=>m.toUpperCase())}"
if old_portal in html:
    html = html.replace(old_portal, new_portal, 1)

path.write_text(html, encoding="utf-8")
print("UX profesional aplicada: Inicio conserva descubrimiento; cada menú abre directamente su contenido")

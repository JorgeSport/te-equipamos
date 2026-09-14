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

# apply-real-news.py genera este aviso durante el despliegue; aquí se convierte en identidad del nuevo portal.
html = re.sub(
    r'<div class="demo"><b>EDICIÓN OUTDOOR · [^<]+</b><span>[^<]+</span></div>',
    '<div class="demo"><b>CONTENIDO PROPIO · GITHUB</b><span>Ventas, reviews, vídeos, consejos, ofertas y novedades de Te Equipamos. Cada publicación se clasifica automáticamente desde su repositorio.</span></div>',
    html,
    count=1,
)

path.write_text(html, encoding="utf-8")
print("Portal configurado: Inicio · Ventas · Reviews · Vídeos · Consejos · Ofertas · Novedades · Siguiendo")

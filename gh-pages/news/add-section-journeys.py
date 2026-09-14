from pathlib import Path

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")

css = r'''/* SECTION_JOURNEY */
.journey{margin-top:34px}.journeyShell{background:var(--surface);border:1px solid var(--line);border-radius:22px;box-shadow:var(--shadow);padding:26px}.journeyHead{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:18px}.journeyHead h2{margin:6px 0 0;font-size:26px;letter-spacing:-.03em}.journeyHead p{margin:0;max-width:520px;color:var(--muted);font-size:14px;line-height:1.55}.journeyGrid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.journeyCard{appearance:none;width:100%;border:1px solid var(--line);background:var(--bg);color:var(--text);border-radius:17px;padding:18px;text-align:left;cursor:pointer;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:16px;align-items:center;transition:transform .16s ease,border-color .16s ease,background .16s ease}.journeyCard:hover{transform:translateY(-2px);border-color:var(--accent);background:var(--surface2)}.journeyCard small{display:block;color:var(--accent);font-weight:800;font-size:10px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:7px}.journeyCard strong{display:block;font-size:17px;line-height:1.3}.journeyCard p{margin:6px 0 0;color:var(--muted);font-size:12px;line-height:1.45}.journeyArrow{font-size:23px;color:var(--accent)}
@media(max-width:760px){.journey{margin-top:18px}.journeyShell{border-left:0;border-right:0;border-radius:0;padding:24px 16px}.journeyHead{display:block}.journeyHead h2{font-size:24px}.journeyHead p{margin-top:8px}.journeyGrid{grid-template-columns:1fr}.journeyCard{padding:17px;border-radius:15px}.journeyCard strong{font-size:17px}}
'''
if "/* SECTION_JOURNEY */" not in html:
    html = html.replace("</style>", css + "</style>", 1)

journey_html = '''<section class="section journey hidden" id="sectionJourney"><div class="journeyShell"><div class="journeyHead"><div><span class="kicker" id="journeyEyebrow">SIGUE EXPLORANDO</span><h2 id="journeyTitle">Sigue explorando Te Equipamos</h2></div><p id="journeyText">Descubre otras formas de encontrar el equipo y la información que necesitas.</p></div><div class="journeyGrid" id="journeyGrid"></div></div></section>'''
if 'id="sectionJourney"' not in html:
    marker = '<section class="section hidden" id="following">'
    if marker not in html:
        raise RuntimeError("No se encontró el punto de inserción del cierre estratégico")
    html = html.replace(marker, journey_html + marker, 1)

js = r'''const JOURNEY_MAP={
'Ventas':{title:'Has visto el catálogo. Ahora elige con más criterio.',text:'Compara, profundiza o descubre qué acaba de llegar antes de tomar una decisión.',targets:[{cat:'Reviews',title:'Mira lo que hay detrás del producto',text:'Análisis y reviews para entender mejor cada elección.'},{cat:'Ofertas',title:'Revisa las oportunidades activas',text:'Productos y promociones que merece la pena mirar ahora.'},{cat:'Consejos',title:'Entender el equipo ayuda a elegir mejor',text:'Guías prácticas para acertar con materiales, tallas y uso.'},{cat:'Novedades',title:'Descubre lo último de Te Equipamos',text:'Nuevos productos, contenidos y publicaciones.'}]},
'Reviews':{title:'Del análisis a la elección.',text:'Si una review te ha ayudado, sigue con los productos disponibles o compara otras opciones.',targets:[{cat:'Ventas',title:'Mira qué está disponible ahora',text:'Pasa del análisis al catálogo actual de Te Equipamos.'},{cat:'Consejos',title:'Aprende antes de elegir',text:'Guías para entender mejor materiales, uso y prestaciones.'},{cat:'Ofertas',title:'Comprueba si hay una oportunidad',text:'Revisa promociones y productos destacados.'},{cat:'Novedades',title:'Sigue con lo más reciente',text:'Descubre las últimas incorporaciones y publicaciones.'}]},
'Vídeos':{title:'Has visto cómo funciona. Ahora profundiza.',text:'Continúa con análisis, guías y productos relacionados dentro de Te Equipamos.',targets:[{cat:'Reviews',title:'Lee el análisis completo',text:'Más contexto y detalles sobre el equipamiento.'},{cat:'Consejos',title:'Convierte la demostración en conocimiento',text:'Consejos para elegir y usar mejor tu equipo.'},{cat:'Ventas',title:'Explora los productos disponibles',text:'Consulta el catálogo actual.'},{cat:'Novedades',title:'Descubre lo nuevo',text:'Últimos contenidos publicados.'}]},
'Consejos':{title:'De la teoría a una mejor elección.',text:'Ahora que tienes el criterio, puedes comparar análisis o ver qué productos encajan contigo.',targets:[{cat:'Reviews',title:'Compara con análisis reales',text:'Reviews y lecturas para profundizar antes de elegir.'},{cat:'Ventas',title:'Lleva el consejo al catálogo',text:'Consulta los productos disponibles.'},{cat:'Vídeos',title:'Míralo en acción',text:'Demostraciones y contenido visual de Te Equipamos.'},{cat:'Ofertas',title:'Revisa las oportunidades actuales',text:'Promociones y selecciones disponibles.'}]},
'Ofertas':{title:'Una oferta importa más cuando sabes qué estás comprando.',text:'Compara, revisa y descubre otras opciones antes de decidir.',targets:[{cat:'Ventas',title:'Ver todo el catálogo',text:'Explora todos los productos disponibles.'},{cat:'Reviews',title:'Comprueba si realmente merece la pena',text:'Lee análisis antes de elegir por precio.'},{cat:'Consejos',title:'Elige por necesidad, no solo por descuento',text:'Guías para tomar una decisión más informada.'},{cat:'Novedades',title:'Mira qué acaba de llegar',text:'Nuevos productos y publicaciones.'}]},
'Novedades':{title:'Lo nuevo es solo el comienzo.',text:'Sigue explorando productos, análisis y oportunidades dentro de Te Equipamos.',targets:[{cat:'Ventas',title:'Ver productos disponibles',text:'Consulta el catálogo actual.'},{cat:'Reviews',title:'Profundiza con nuestras reviews',text:'Análisis para entender mejor cada producto.'},{cat:'Ofertas',title:'Descubre oportunidades activas',text:'Promociones y selecciones actuales.'},{cat:'Consejos',title:'Aprende a elegir mejor',text:'Guías prácticas para tu equipo outdoor.'}]}
};
function journeySectionCount(cat){return NEWS.filter(n=>n.category===cat||(Array.isArray(n.sections)&&n.sections.includes(cat))).length}
function renderJourney(c){const section=$('#sectionJourney');if(!section)return;const cfg=JOURNEY_MAP[c];if(!cfg||c==='Todas'||c==='Siguiendo'||state.q){section.classList.add('hidden');return}const targets=cfg.targets.filter(x=>journeySectionCount(x.cat)>0).slice(0,4);if(!targets.length){section.classList.add('hidden');return}section.classList.remove('hidden');$('#journeyTitle').textContent=cfg.title;$('#journeyText').textContent=cfg.text;$('#journeyGrid').innerHTML=targets.map(x=>{const count=journeySectionCount(x.cat);return `<button type="button" class="journeyCard" data-journey-cat="${x.cat}"><span><small>${x.cat} · ${count} ${count===1?'contenido':'contenidos'}</small><strong>${x.title}</strong><p>${x.text}</p></span><span class="journeyArrow">→</span></button>`}).join('')}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-journey-cat]');if(!b)return;setCat(b.dataset.journeyCat)});
document.addEventListener('input',e=>{if(e.target&&e.target.id==='searchInput'){const j=$('#sectionJourney');if(j)j.classList.toggle('hidden',!!e.target.value.trim()||state.cat==='Todas'||state.cat==='Siguiendo')}});
document.addEventListener('click',e=>{if(e.target&&e.target.id==='clearBtn')setTimeout(()=>renderJourney(state.cat),0)});
'''
if "const JOURNEY_MAP=" not in html:
    marker = "const SECTION_COPY="
    if marker not in html:
        raise RuntimeError("No se encontró SECTION_COPY para conectar los cierres estratégicos")
    html = html.replace(marker, js + marker, 1)

old = "renderFeed();updateSectionHead(c)}closeMenu();"
new = "renderFeed();updateSectionHead(c);renderJourney(c)}closeMenu();"
if old in html:
    html = html.replace(old, new, 1)
elif new not in html:
    raise RuntimeError("No se pudo conectar renderJourney con setCat")

old_home = "renderFeed();renderTrend();$('#today').textContent="
new_home = "renderFeed();renderTrend();renderJourney('Todas');$('#today').textContent="
if old_home in html:
    html = html.replace(old_home, new_home, 1)
elif new_home not in html:
    raise RuntimeError("No se pudo conectar renderJourney con Inicio")

path.write_text(html, encoding="utf-8")
print("Cierres estratégicos añadidos: cada sección conduce a contenido útil y omite destinos vacíos")

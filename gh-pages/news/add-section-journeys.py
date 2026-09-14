from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

css = r'''/* SECTION_JOURNEY_VISUAL */
.journey{margin-top:38px}.journeyShell{padding:0;background:transparent;border:0;box-shadow:none}.journeyHead{display:flex;justify-content:space-between;gap:24px;align-items:end;margin-bottom:18px}.journeyHead h2{margin:6px 0 0;font-size:27px;letter-spacing:-.03em}.journeyHead p{margin:0;max-width:520px;color:var(--muted);font-size:13px;line-height:1.55}.journeyGrid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));grid-auto-rows:168px;gap:12px}.journeyCard{appearance:none;border:1px solid var(--line);background:var(--surface);color:var(--text);border-radius:20px;padding:0;text-align:left;cursor:pointer;overflow:hidden;min-width:0;transition:transform .18s ease,box-shadow .18s ease}.journeyCard:hover{transform:translateY(-2px);box-shadow:0 10px 26px rgba(0,0,0,.08)}.journeyCardInner{height:100%;display:grid;grid-template-columns:minmax(0,1fr) 44%;min-width:0}.journeyCopy{padding:18px;display:flex;flex-direction:column;justify-content:center;min-width:0}.journeyCopy small{display:block;color:var(--accent);font-weight:900;font-size:10px;letter-spacing:.08em;text-transform:uppercase;margin-bottom:8px}.journeyCopy strong{display:block;font-size:17px;line-height:1.27}.journeyCopy p{margin:7px 0 0;color:var(--muted);font-size:12px;line-height:1.45}.journeyCta{margin-top:11px;color:var(--accent);font-size:11px;font-weight:900}.journeyMedia{overflow:hidden;background:var(--surface2);min-width:0}.journeyMedia img{width:100%;height:100%;display:block;object-fit:cover;transition:transform .3s ease}.journeyCard:hover img{transform:scale(1.025)}.journeyHero{grid-column:1/8;grid-row:span 2}.journeyHero .journeyCopy{padding:26px}.journeyHero .journeyCopy strong{font-size:23px;line-height:1.2}.journeySide{grid-column:8/13}.journeySide .journeyCopy{padding:15px}.journeySide .journeyCopy p{display:none}.journeyWide{grid-column:1/13}.journeyWide .journeyCardInner{grid-template-columns:34% minmax(0,1fr)}.journeyWide .journeyMedia{order:-1}.journeyWide .journeyCopy strong{font-size:19px}.journeyGrid.count2{grid-auto-rows:220px}.journeyGrid.count2 .journeyCard{grid-column:span 6;grid-row:auto}.journeyGrid.count1{grid-auto-rows:225px}.journeyGrid.count1 .journeyCard{grid-column:1/13;grid-row:auto}
@media(max-width:760px){.journey{margin-top:24px}.journeyHead{display:block;padding:0 16px}.journeyHead h2{font-size:24px}.journeyHead p{margin-top:8px}.journeyGrid,.journeyGrid.count1,.journeyGrid.count2{grid-template-columns:1fr;grid-auto-rows:auto;gap:10px;padding:0 12px}.journeyCard,.journeyGrid.count1 .journeyCard,.journeyGrid.count2 .journeyCard{grid-column:1;grid-row:auto;border-radius:16px}.journeyHero .journeyCardInner{display:block}.journeyHero .journeyMedia{aspect-ratio:16/9}.journeyHero .journeyCopy{padding:18px}.journeyHero .journeyCopy strong{font-size:20px}.journeySide .journeyCardInner,.journeyWide .journeyCardInner{grid-template-columns:minmax(0,1fr) 118px;min-height:124px}.journeyWide .journeyMedia{order:0}.journeySide .journeyCopy p,.journeyWide .journeyCopy p{display:none}.journeyCopy strong,.journeyWide .journeyCopy strong{font-size:16px}}
'''
if '/* SECTION_JOURNEY_VISUAL */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

journey_html = '''<section class="section journey hidden" id="sectionJourney"><div class="journeyShell"><div class="journeyHead"><div><span class="kicker">SIGUE EXPLORANDO</span><h2 id="journeyTitle">Sigue explorando</h2></div><p id="journeyText">Descubre otras secciones de Te Equipamos.</p></div><div class="journeyGrid" id="journeyGrid"></div></div></section>'''
if 'id="sectionJourney"' not in html:
    marker = '<section class="section hidden" id="following">'
    if marker not in html:
        raise RuntimeError('No se encontró el punto de inserción del cierre editorial')
    html = html.replace(marker, journey_html + marker, 1)

js = r'''const JOURNEY_MAP={
'Ventas':{text:'Después del catálogo, compara, mira oportunidades y descubre lo último.',targets:[{cat:'Reviews',title:'Mira lo que hay detrás del producto',text:'Análisis para entender mejor cada elección.'},{cat:'Ofertas',title:'Revisa las oportunidades activas',text:'Promociones y selecciones que merece la pena mirar.'},{cat:'Novedades',title:'Descubre lo último de Te Equipamos',text:'Nuevos productos y publicaciones.'},{cat:'Consejos',title:'Aprende a elegir mejor',text:'Guías prácticas para acertar con tu equipo.'}]},
'Reviews':{text:'Del análisis puedes pasar al catálogo, a las oportunidades o a lo más reciente.',targets:[{cat:'Ventas',title:'Mira qué está disponible ahora',text:'Pasa del análisis al catálogo actual.'},{cat:'Ofertas',title:'Comprueba si hay una oportunidad',text:'Revisa promociones y productos destacados.'},{cat:'Novedades',title:'Sigue con lo más reciente',text:'Últimas incorporaciones y publicaciones.'},{cat:'Consejos',title:'Aprende antes de elegir',text:'Guías para entender materiales y uso.'}]},
'Vídeos':{text:'Profundiza con análisis, guías y productos relacionados.',targets:[{cat:'Reviews',title:'Lee el análisis completo',text:'Más contexto sobre el equipamiento.'},{cat:'Consejos',title:'Convierte la demostración en conocimiento',text:'Consejos para elegir y usar mejor.'},{cat:'Ventas',title:'Explora los productos disponibles',text:'Consulta el catálogo actual.'},{cat:'Novedades',title:'Descubre lo nuevo',text:'Últimos contenidos publicados.'}]},
'Consejos':{text:'Compara análisis, mira productos y descubre oportunidades relacionadas.',targets:[{cat:'Reviews',title:'Compara con análisis',text:'Reviews para profundizar antes de elegir.'},{cat:'Ventas',title:'Lleva el consejo al catálogo',text:'Consulta los productos disponibles.'},{cat:'Ofertas',title:'Revisa las oportunidades',text:'Promociones y selecciones disponibles.'},{cat:'Novedades',title:'Mira qué hay de nuevo',text:'Últimos contenidos de Te Equipamos.'}]},
'Ofertas':{text:'Una buena oportunidad gana valor cuando la comparas con el resto del contenido.',targets:[{cat:'Ventas',title:'Ver todo el catálogo',text:'Explora los productos disponibles.'},{cat:'Reviews',title:'Comprueba si realmente merece la pena',text:'Lee análisis antes de elegir solo por precio.'},{cat:'Novedades',title:'Mira qué acaba de llegar',text:'Nuevos productos y publicaciones.'},{cat:'Consejos',title:'Elige por necesidad',text:'Guías para decidir con más criterio.'}]},
'Novedades':{text:'Continúa con productos, análisis y oportunidades dentro de Te Equipamos.',targets:[{cat:'Ventas',title:'Ver productos disponibles',text:'Consulta el catálogo actual.'},{cat:'Reviews',title:'Profundiza con nuestras reviews',text:'Análisis para entender cada producto.'},{cat:'Ofertas',title:'Descubre oportunidades activas',text:'Promociones y selecciones actuales.'},{cat:'Consejos',title:'Aprende a elegir mejor',text:'Guías prácticas para tu equipo outdoor.'}]}
};
function journeyItems(cat){return NEWS.filter(n=>n.category===cat||(Array.isArray(n.sections)&&n.sections.includes(cat)))}
function journeyMedia(cat){const n=journeyItems(cat).find(x=>x.image);return n&&n.image?`<div class="journeyMedia"><img src="${esc(n.image)}" alt="" loading="lazy"></div>`:''}
function renderJourney(c){const section=$('#sectionJourney');if(!section)return;const cfg=JOURNEY_MAP[c];if(!cfg||c==='Todas'||c==='Siguiendo'||state.q){section.classList.add('hidden');return}const targets=cfg.targets.filter(x=>journeyItems(x.cat).length>0).slice(0,4);if(!targets.length){section.classList.add('hidden');return}section.classList.remove('hidden');$('#journeyTitle').textContent='Sigue explorando';$('#journeyText').textContent=cfg.text;const kinds=targets.length===1?['journeyHero']:targets.length===2?['journeyHero','journeyHero']:targets.length===3?['journeyHero','journeySide','journeySide']:['journeyHero','journeySide','journeySide','journeyWide'];const grid=$('#journeyGrid');grid.className=`journeyGrid count${targets.length}`;grid.innerHTML=targets.map((x,i)=>{const count=journeyItems(x.cat).length;return `<button type="button" class="journeyCard ${kinds[i]}" data-journey-cat="${x.cat}"><div class="journeyCardInner"><div class="journeyCopy"><small>${x.cat} · ${count} ${count===1?'contenido':'contenidos'}</small><strong>${x.title}</strong><p>${x.text}</p><span class="journeyCta">Explorar ${x.cat} →</span></div>${journeyMedia(x.cat)}</div></button>`}).join('')}
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-journey-cat]');if(!b)return;setCat(b.dataset.journeyCat)});
document.addEventListener('input',e=>{if(e.target&&e.target.id==='searchInput'){const j=$('#sectionJourney');if(j)j.classList.toggle('hidden',!!e.target.value.trim()||state.cat==='Todas'||state.cat==='Siguiendo')}});
document.addEventListener('click',e=>{if(e.target&&e.target.id==='clearBtn')setTimeout(()=>renderJourney(state.cat),0)});
'''
if 'const JOURNEY_MAP=' not in html:
    marker = 'const SECTION_COPY='
    if marker not in html:
        raise RuntimeError('No se encontró SECTION_COPY')
    html = html.replace(marker, js + marker, 1)

old = 'renderFeed();updateSectionHead(c)}closeMenu();'
new = 'renderFeed();updateSectionHead(c);renderJourney(c)}closeMenu();'
if old in html:
    html = html.replace(old, new, 1)
elif new not in html:
    raise RuntimeError('No se pudo conectar el mosaico con las secciones')

old_home = "renderFeed();renderTrend();$('#today').textContent="
new_home = "renderFeed();renderTrend();renderJourney('Todas');$('#today').textContent="
if old_home in html:
    html = html.replace(old_home, new_home, 1)

path.write_text(html, encoding='utf-8')
print('Sigue explorando convertido en mosaico editorial con imágenes reales')

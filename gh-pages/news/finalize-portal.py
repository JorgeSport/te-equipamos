from pathlib import Path
import re

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

# Identidad final: la marca es Te Equipamos, sin el antiguo apellido Noticias/News.
html = html.replace('Te Equipamos News', 'Te Equipamos')
html = html.replace('<span>Te Equipamos <small>Noticias</small></span>', '<span>Te Equipamos</span>')
html = html.replace('← Volver a noticias', '← Volver a Te Equipamos')
html = html.replace('Tus temas y noticias guardadas', 'Tus temas y contenidos guardados')
html = html.replace('placeholder="Buscar temas, noticias y fuentes"', 'placeholder="Buscar productos, reviews, actividades y consejos"')
html = re.sub(r'<title>.*?</title>', '<title>Te Equipamos</title>', html, count=1, flags=re.S)
html = re.sub(
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Te Equipamos — productos, reviews, ofertas y guías para deporte, aventura y todo tipo de actividades.">',
    html,
    count=1,
)

css = r'''/* TE_RESPONSIVE_ACTIVITY_NAV */
.teResponsiveActivities{display:none}
@media(max-width:1100px){
  .teResponsiveActivities{display:block;border-top:1px solid var(--line);background:var(--surface)}
  .teRespActivitiesInner{padding:9px 16px 10px}
  .teRespActivitiesHead{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:7px}
  .teRespActivitiesHead strong{font-size:12px;letter-spacing:.01em}
  .teRespActivitiesHead span{font-size:10px;color:var(--muted)}
  .teRespActivityRow{display:flex;gap:7px;overflow-x:auto;scrollbar-width:none;padding:1px 0 2px}
  .teRespActivityRow::-webkit-scrollbar{display:none}
  .teRespActivityChip{flex:0 0 auto;border:1px solid var(--line);background:var(--surface);color:var(--muted);border-radius:999px;min-height:36px;padding:7px 12px;font-size:12px;font-weight:700;cursor:pointer;white-space:nowrap}
  .teRespActivityChip:hover,.teRespActivityChip.isActive{background:var(--soft);border-color:color-mix(in srgb,var(--accent) 38%,var(--line));color:var(--accent)}
  .teRespActivityMore{color:var(--accent);font-weight:900}
  .teRespActivityExtra{display:flex;gap:7px;flex-wrap:wrap;padding-top:9px;margin-top:7px;border-top:1px solid var(--line)}
  .teRespActivityExtra .teRespActivityChip{font-size:11px;min-height:34px;padding:6px 10px}
}
@media(max-width:760px){
  .teRespActivitiesInner{padding:8px 12px 9px}
  .teRespActivitiesHead{margin-bottom:6px}
  .teRespActivitiesHead strong{font-size:12px}
  .teRespActivitiesHead span{display:none}
  .teRespActivityChip{min-height:35px;padding:7px 11px;font-size:12px}
  .teRespActivityExtra{gap:6px;padding-top:8px;margin-top:6px}
}
'''
if '/* TE_RESPONSIVE_ACTIVITY_NAV */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

# El contenedor queda presente en el HTML y el script solo rellena su contenido.
if 'id="teResponsiveActivities"' not in html:
    html = html.replace(
        '<nav class="cats" id="cats"></nav>',
        '<nav class="cats" id="cats"></nav><section id="teResponsiveActivities" class="teResponsiveActivities" aria-label="Explorar actividades"></section>',
        1,
    )

js = r'''<script id="teResponsiveActivitiesScript">
(function(){
  const mq=window.matchMedia('(max-width:1100px)');
  const MAIN=[
    ['senderismo','Senderismo'],
    ['running','Running'],
    ['ciclismo','Ciclismo'],
    ['natacion','Natación'],
    ['travel','Travel']
  ];
  const EXTRA=[
    ['trekking','Trekking'],
    ['trail-running','Trail running'],
    ['alpinismo','Alpinismo'],
    ['escalada','Escalada'],
    ['camping','Camping'],
    ['esqui','Esquí y nieve'],
    ['kayak','Kayak y remo'],
    ['surf','Surf'],
    ['fitness','Fitness']
  ];
  let open=false;
  function escHtml(value){return String(value||'').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))}
  function ensure(){
    const cats=document.getElementById('cats');
    if(!cats)return null;
    let host=document.getElementById('teResponsiveActivities');
    if(!host){
      host=document.createElement('section');
      host.id='teResponsiveActivities';
      host.className='teResponsiveActivities';
      host.setAttribute('aria-label','Explorar actividades');
      cats.insertAdjacentElement('afterend',host);
    }
    return host;
  }
  function button(pair,active){
    const slug=pair[0],label=pair[1];
    return `<button type="button" class="teRespActivityChip ${active===slug?'isActive':''}" data-resp-activity="${escHtml(slug)}" aria-pressed="${active===slug?'true':'false'}">${escHtml(label)}</button>`;
  }
  function render(){
    const host=ensure();
    if(!host)return;
    const active=(typeof state!=='undefined'&&state.activity)?String(state.activity):'';
    if(active&&EXTRA.some(x=>x[0]===active))open=true;
    host.innerHTML=`<div class="teRespActivitiesInner"><div class="teRespActivitiesHead"><strong>Explorar actividades</strong><span>Elige lo que quieres practicar</span></div><div class="teRespActivityRow">${MAIN.map(x=>button(x,active)).join('')}<button type="button" class="teRespActivityChip teRespActivityMore" data-resp-more aria-expanded="${open?'true':'false'}">${open?'Menos':'Más actividades'} ${open?'↑':'↓'}</button></div>${open?`<div class="teRespActivityExtra">${EXTRA.map(x=>button(x,active)).join('')}</div>`:''}</div>`;
  }
  function choose(slug){
    if(typeof applyActivityFilter==='function')applyActivityFilter(slug);
    else if(typeof state!=='undefined'){
      state.activity=slug;state.q='';state.cat='Todas';
      if(typeof renderFeed==='function')renderFeed();
    }
    if(EXTRA.some(x=>x[0]===slug))open=true;
    setTimeout(render,40);
  }
  window.renderResponsiveActivities=render;
  document.addEventListener('click',e=>{
    const activity=e.target.closest&&e.target.closest('[data-resp-activity]');
    if(activity){e.preventDefault();choose(activity.dataset.respActivity||'');return}
    const more=e.target.closest&&e.target.closest('[data-resp-more]');
    if(more){e.preventDefault();open=!open;render();return}
    if(e.target.closest&&e.target.closest('.chip,.nav button,[data-tag-filter],[data-activity-filter],#clearBtn'))setTimeout(render,100);
  });
  window.addEventListener('pageshow',()=>setTimeout(render,30));
  window.addEventListener('resize',()=>{if(mq.matches)render()});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();
</script>'''

if 'id="teResponsiveActivitiesScript"' not in html:
    html = html.replace('</body>', js + '</body>', 1)

path.write_text(html, encoding='utf-8')
print('Identidad Te Equipamos cerrada y actividades responsive activadas')

from pathlib import Path
import json
import re

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

OFFICIAL_URL = 'https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/'
SHARE_IMAGE = 'https://res.cloudinary.com/detstbpo9/image/upload/v1789420923/te-equipamos-social-share.png'
PAGE_TITLE = 'Te Equipamos | Deporte, actividades y equipamiento'
SOCIAL_TITLE = 'Te Equipamos — Encuentra equipamiento para lo que te gusta hacer'
DESCRIPTION = 'Productos, reviews, ofertas y guías para senderismo, running, ciclismo, natación, viajes y muchas más actividades.'

# Identidad final: la marca es Te Equipamos, sin el antiguo apellido Noticias/News.
html = html.replace('Te Equipamos News', 'Te Equipamos')
html = html.replace('<span>Te Equipamos <small>Noticias</small></span>', '<span>Te Equipamos</span>')
html = html.replace('← Volver a noticias', '← Volver a Te Equipamos')
html = html.replace('Tus temas y noticias guardadas', 'Tus temas y contenidos guardados')
html = html.replace('placeholder="Buscar temas, noticias y fuentes"', 'placeholder="Buscar productos, reviews, actividades y consejos"')
html = re.sub(r'<title>.*?</title>', f'<title>{PAGE_TITLE}</title>', html, count=1, flags=re.S)
html = re.sub(
    r'<meta name="description" content="[^"]*">',
    f'<meta name="description" content="{DESCRIPTION}">',
    html,
    count=1,
)
html = html.replace("document.title='Te Equipamos';", f"document.title='{PAGE_TITLE}';")

# El nombre de la marca siempre vuelve al Hub oficial, nunca a una landing de producto.
html = re.sub(
    r'<a href="[^"]*" class="brand">',
    f'<a href="{OFFICIAL_URL}" class="brand" aria-label="Ir al inicio de Te Equipamos">',
    html,
    count=1,
)
html = re.sub(
    r'<a class="back" href="[^"]*">',
    f'<a class="back" href="{OFFICIAL_URL}">',
    html,
    count=1,
)

# Metadatos oficiales para SEO y para compartir por WhatsApp, Facebook, Telegram, etc.
html = re.sub(
    r'<!-- TE_OFFICIAL_SITE_META -->.*?<!-- /TE_OFFICIAL_SITE_META -->',
    '',
    html,
    flags=re.S,
)
schema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    'name': 'Te Equipamos',
    'url': OFFICIAL_URL,
    'description': DESCRIPTION,
    'publisher': {
        '@type': 'Organization',
        'name': 'Te Equipamos',
        'url': OFFICIAL_URL,
        'logo': {
            '@type': 'ImageObject',
            'url': SHARE_IMAGE,
        },
    },
}
meta = f'''<!-- TE_OFFICIAL_SITE_META -->
<link rel="canonical" href="{OFFICIAL_URL}">
<link rel="icon" href="/te-equipamos-arpenaz-27l/favicon.svg" type="image/svg+xml">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="application-name" content="Te Equipamos">
<meta name="apple-mobile-web-app-title" content="Te Equipamos">
<meta property="og:locale" content="es_ES">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Te Equipamos">
<meta property="og:title" content="{SOCIAL_TITLE}">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:url" content="{OFFICIAL_URL}">
<meta property="og:image" content="{SHARE_IMAGE}">
<meta property="og:image:secure_url" content="{SHARE_IMAGE}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Te Equipamos — deporte, actividades y equipamiento">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{SOCIAL_TITLE}">
<meta name="twitter:description" content="{DESCRIPTION}">
<meta name="twitter:image" content="{SHARE_IMAGE}">
<meta name="twitter:image:alt" content="Te Equipamos — deporte, actividades y equipamiento">
<script type="application/ld+json" id="teOfficialSchema">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script>
<!-- /TE_OFFICIAL_SITE_META -->'''
html = html.replace('</head>', meta + '\n</head>', 1)

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
  .teRespActivityChip small{margin-left:5px;color:inherit;font-size:9px;font-weight:900;opacity:.72}
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
  function countActivity(slug){return (typeof NEWS!=='undefined'?NEWS:[]).filter(n=>Array.isArray(n.activities)&&n.activities.includes(slug)).length}
  function available(items){return items.map(pair=>[pair[0],pair[1],countActivity(pair[0])]).filter(pair=>pair[2]>0)}
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
    const slug=pair[0],label=pair[1],count=pair[2];
    return `<button type="button" class="teRespActivityChip ${active===slug?'isActive':''}" data-resp-activity="${escHtml(slug)}" aria-pressed="${active===slug?'true':'false'}" aria-label="${escHtml(label)} · ${count} ${count===1?'contenido':'contenidos'}">${escHtml(label)}<small>${count}</small></button>`;
  }
  function render(){
    const host=ensure();
    if(!host)return;
    const active=(typeof state!=='undefined'&&state.activity)?String(state.activity):'';
    const main=available(MAIN),extra=available(EXTRA);
    if(active&&extra.some(x=>x[0]===active))open=true;
    const more=extra.length?`<button type="button" class="teRespActivityChip teRespActivityMore" data-resp-more aria-expanded="${open?'true':'false'}">${open?'Menos':'Más actividades'} ${open?'↑':'↓'}</button>`:'';
    host.innerHTML=`<div class="teRespActivitiesInner"><div class="teRespActivitiesHead"><strong>Explorar actividades</strong><span>Solo actividades con contenido disponible</span></div><div class="teRespActivityRow">${main.map(x=>button(x,active)).join('')}${more}</div>${open&&extra.length?`<div class="teRespActivityExtra">${extra.map(x=>button(x,active)).join('')}</div>`:''}</div>`;
    host.classList.toggle('hidden',main.length===0&&extra.length===0);
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


# Orden responsive del inicio: primero tarjetas completas, después contenidos relacionados.
responsive_home_css = r'''/* TE_RESPONSIVE_HOME_ORDER */
@media(max-width:760px){
  #portal .main{display:flex;flex-direction:column;min-width:0}
  #portal .welcome{order:1}
  #portal #hero{order:2}
  #portal #topicsSection{order:3}
  #portal #feedSection{order:4}
  #portal #homeRelated{order:5}
  #portal #sectionJourney{order:6}
  #portal #following{order:7}

  #feed{background:transparent;border:0;border-radius:0;box-shadow:none;overflow:visible}
  #feed .card{
    display:flex!important;
    flex-direction:column!important;
    gap:0!important;
    padding:0!important;
    margin:0 0 18px!important;
    background:var(--surface)!important;
    border:1px solid var(--line)!important;
    border-radius:18px!important;
    overflow:hidden!important;
    box-shadow:var(--shadow)!important;
  }
  #feed .card>.thumb{
    order:-1!important;
    width:100%!important;
    height:auto!important;
    aspect-ratio:16/9!important;
    object-fit:cover!important;
    border-radius:0!important;
    margin:0!important;
  }
  #feed .card>div:first-child{padding:16px 16px 17px!important}
  #feed .card .title{font-size:21px!important;line-height:1.2!important;margin:7px 0 9px!important}
  #feed .card .summary{display:block!important;font-size:13px!important;line-height:1.5!important;margin:0 0 13px!important}
  #feed .card .cardMeta{padding:0!important;font-size:11px!important}

  #hero>.panel:nth-child(2){display:none!important}
  #homeRelated{
    display:block;
    margin-top:28px;
    padding-top:22px;
    border-top:1px solid var(--line);
  }
  #homeRelated.hidden{display:none!important}
  #homeRelated .homeRelatedHead{margin:0 0 12px}
  #homeRelated .homeRelatedHead .kicker{display:block;margin-bottom:5px}
  #homeRelated .homeRelatedHead h2{margin:0;font-size:23px;letter-spacing:-.03em}
  #homeRelated .homeRelatedList{border-top:1px solid var(--line)}
  #homeRelated .homeRelatedItem{
    width:100%;
    display:grid;
    grid-template-columns:92px minmax(0,1fr);
    gap:12px;
    align-items:center;
    padding:13px 0;
    border:0;
    border-bottom:1px solid var(--line);
    background:transparent;
    color:var(--text);
    text-align:left;
    cursor:pointer;
  }
  #homeRelated .homeRelatedItem img{
    width:92px;height:74px;object-fit:cover;border-radius:11px;background:var(--surface2)
  }
  #homeRelated .homeRelatedItem small{
    display:block;margin-bottom:4px;color:var(--accent);font-size:9px;font-weight:900;letter-spacing:.06em;text-transform:uppercase
  }
  #homeRelated .homeRelatedItem strong{
    display:block;font-size:16px;line-height:1.28;letter-spacing:-.01em
  }
}
@media(min-width:761px){
  #homeRelated{display:none!important}
}
'''
if '/* TE_RESPONSIVE_HOME_ORDER */' not in html:
    html = html.replace('</style>', responsive_home_css + '</style>', 1)

responsive_home_js = r'''<script id="teResponsiveHomeOrder">
(function(){
  function ensureRelatedHost(){
    let host=document.getElementById('homeRelated');
    if(host)return host;
    const feed=document.getElementById('feedSection');
    if(!feed||!feed.parentElement)return null;
    host=document.createElement('section');
    host.id='homeRelated';
    host.className='section hidden';
    host.setAttribute('aria-label','Contenidos relacionados');
    feed.insertAdjacentElement('afterend',host);
    return host;
  }
  function renderHomeRelated(){
    const host=ensureRelatedHost();
    if(!host)return;
    if(!window.matchMedia('(max-width:760px)').matches){
      host.classList.add('hidden');
      return;
    }
    if(typeof state!=='undefined' && (state.q || state.cat!=='Todas')){
      host.classList.add('hidden');
      return;
    }
    const all=(typeof NEWS!=='undefined'&&Array.isArray(NEWS))?NEWS:[];
    const featured=all.filter(n=>n.featured).slice(1,4);
    const related=(featured.length?featured:all.slice(1,4)).filter(Boolean);
    if(!related.length){
      host.classList.add('hidden');
      return;
    }
    const escapeValue=typeof esc==='function'?esc:(v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c])));
    const getTitle=typeof cardTitle==='function'?cardTitle:(n=>n.title||'Te Equipamos');
    const getLabel=typeof cardLabel==='function'?cardLabel:(n=>n.category||'Te Equipamos');
    host.innerHTML='<div class="homeRelatedHead"><span class="kicker">RELACIONADOS</span><h2>También te puede interesar</h2></div><div class="homeRelatedList">'+related.map(n=>'<button type="button" class="homeRelatedItem" data-article="'+escapeValue(n.id)+'"><img src="'+escapeValue(n.image||'')+'" alt="'+escapeValue(n.title||'')+'" loading="lazy"><span><small>'+escapeValue(getLabel(n))+'</small><strong>'+escapeValue(getTitle(n))+'</strong></span></button>').join('')+'</div>';
    host.classList.remove('hidden');
  }
  const rerender=()=>setTimeout(renderHomeRelated,40);
  document.addEventListener('click',e=>{
    if(e.target.closest&&e.target.closest('[data-cat],#clearBtn,[data-resp-activity],[data-activity-filter],[data-tag-filter]'))rerender();
  });
  document.addEventListener('input',e=>{if(e.target&&e.target.id==='searchInput')rerender()});
  window.addEventListener('resize',rerender);
  window.addEventListener('pageshow',rerender);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',renderHomeRelated,{once:true});else renderHomeRelated();
})();
</script>'''
if 'id="teResponsiveHomeOrder"' not in html:
    html = html.replace('</body>', responsive_home_js + '</body>', 1)

path.write_text(html, encoding='utf-8')

# La landing principal del repositorio sigue siendo un producto. Su nombre de marca debe volver al Hub oficial.
root_index = path.parent.parent / 'index.html'
if root_index.exists():
    root_html = root_index.read_text(encoding='utf-8')
    root_html = root_html.replace(
        '<div class="brand">TE EQUIPAMOS</div>',
        f'<a class="brand" href="{OFFICIAL_URL}" aria-label="Ir al inicio de Te Equipamos" style="background:transparent;color:inherit;padding:0;border-radius:0">TE EQUIPAMOS</a>',
        1,
    )
    root_index.write_text(root_html, encoding='utf-8')

# Después de que el workflow añade breadcrumbs, convertimos la ruta técnica en un regreso limpio al Hub.
product_nav_script = path.parent / 'polish-product-navigation.py'
if not product_nav_script.exists():
    raise RuntimeError('Falta polish-product-navigation.py')
exec(
    compile(product_nav_script.read_text(encoding='utf-8'), str(product_nav_script), 'exec'),
    {'__name__': '__main__', '__file__': str(product_nav_script)},
)

# Comprobaciones mínimas: si fallan, el despliegue debe detenerse.
for marker in [
    f'href="{OFFICIAL_URL}" class="brand"',
    f'<link rel="canonical" href="{OFFICIAL_URL}">',
    'property="og:title"',
    f'property="og:image" content="{SHARE_IMAGE}"',
    'property="og:image:width" content="1200"',
    'property="og:image:height" content="630"',
    'name="twitter:card"',
    'id="teOfficialSchema"',
]:
    if marker not in html:
        raise RuntimeError('Falta identidad oficial o metadato: ' + marker)

print('Te Equipamos: navegación responsive muestra solo actividades con contenido real')

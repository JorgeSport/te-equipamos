from pathlib import Path
from urllib.parse import quote
import html as h
import json
import re

NEWS = Path(__file__).resolve().parent
ROOT = NEWS.parent
BASE = 'https://jorgesport.github.io/te-equipamos-arpenaz-27l/'
HUB = BASE + 'news/'
WHATSAPP = '51920807184'

# ---------- Assets de medición y publicidad ----------
analytics_js = r'''(function(){
  const layer=window.teDataLayer=window.teDataLayer||[];
  function cleanProps(input){const out={};for(const [k,v] of Object.entries(input||{})){if(v===undefined||v===null)continue;if(typeof v==='string')out[k]=v.slice(0,180);else if(['number','boolean'].includes(typeof v))out[k]=v}return out}
  window.teTrack=function(event,props){
    const payload={event:String(event||'event'),ts:Date.now(),path:location.pathname,page_title:document.title,...cleanProps(props)};
    layer.push(payload);
    document.dispatchEvent(new CustomEvent('te:analytics',{detail:payload}));
    if(typeof window.gtag==='function')window.gtag('event',payload.event,cleanProps(props));
    if(typeof window.plausible==='function')window.plausible(payload.event,{props:cleanProps(props)});
    return payload;
  };
  const track=window.teTrack;
  function closest(el,sel){return el&&el.closest?el.closest(sel):null}
  function pageKind(){const p=location.pathname;if(p.includes('/anunciate/'))return'advertising';if(p.includes('/media-kit/'))return'media_kit';if(p.includes('/metodologia/'))return'methodology';if(p.endsWith('/news/')||p.endsWith('/news/index.html'))return'hub';return'landing'}
  track('page_view',{page_kind:pageKind()});
  document.addEventListener('click',e=>{
    const a=closest(e.target,'a,button');if(!a)return;
    const explicit=a.getAttribute('data-track');
    if(explicit)track(explicit,{label:a.getAttribute('data-track-label')||a.textContent.trim().slice(0,80),placement:a.getAttribute('data-placement')||undefined});
    const href=a.getAttribute('href')||'';
    if(/wa\.me\//.test(href)||a.id==='waBtn')track('contact_click',{channel:'whatsapp'});
    if(a.matches('[data-compare-id]'))track('compare_select',{product_id:Number(a.getAttribute('data-compare-id'))||0});
    if(a.id==='teCompareOpen')track('compare_open');
    if(a.matches('[data-save]'))track('save_toggle');
    if(a.matches('[data-share-action]'))track('share_click',{channel:a.getAttribute('data-share-action')||'unknown'});
    if(a.matches('[data-premium-section],[data-quick-section],[data-cat]'))track('section_navigation',{section:a.getAttribute('data-premium-section')||a.getAttribute('data-quick-section')||a.getAttribute('data-cat')||''});
    if(a.matches('[data-premium-activity],[data-resp-activity],[data-activity-alt]'))track('activity_navigation',{activity:a.getAttribute('data-premium-activity')||a.getAttribute('data-resp-activity')||a.getAttribute('data-activity-alt')||''});
  },{passive:true});
  const form=document.getElementById('searchForm');if(form)form.addEventListener('submit',()=>{const q=document.getElementById('searchInput');track('search_submit',{query_length:q&&q.value?Math.min(q.value.length,120):0})});
  let lcp=0,cls=0,inp=0;
  try{new PerformanceObserver(list=>{for(const e of list.getEntries())lcp=Math.max(lcp,e.startTime||0)}).observe({type:'largest-contentful-paint',buffered:true})}catch(e){}
  try{let session=0;new PerformanceObserver(list=>{for(const e of list.getEntries()){if(!e.hadRecentInput){session+=e.value||0;cls=Math.max(cls,session)}}}).observe({type:'layout-shift',buffered:true})}catch(e){}
  try{new PerformanceObserver(list=>{for(const e of list.getEntries())inp=Math.max(inp,e.duration||0)}).observe({type:'event',buffered:true,durationThreshold:40})}catch(e){}
  let sent=false;function sendVitals(){if(sent)return;sent=true;track('web_vitals',{lcp_ms:Math.round(lcp),cls:Number(cls.toFixed(4)),inp_ms:Math.round(inp)})}
  addEventListener('pagehide',sendVitals,{once:true});document.addEventListener('visibilitychange',()=>{if(document.visibilityState==='hidden')sendVitals()},{once:true});
})();'''
(ROOT / 'te-business-analytics.js').write_text(analytics_js, encoding='utf-8')

sponsor_css = r'''.teSponsorSlot{display:none;margin:34px 0}.teSponsorSlot.hasCampaign{display:block}.teSponsorCard{display:grid;grid-template-columns:180px minmax(0,1fr);gap:18px;background:var(--surface,#fff);border:1px solid var(--line,#dddcd7);border-radius:20px;overflow:hidden}.teSponsorMedia{width:100%;height:100%;min-height:148px;object-fit:cover;background:var(--surface2,#efeee9)}.teSponsorCopy{padding:19px 20px 19px 0}.teSponsorLabel{display:block;color:var(--muted,#6c6b67);font-size:10px;font-weight:900;letter-spacing:.09em;text-transform:uppercase}.teSponsorCopy h3{margin:6px 0 8px;font-size:20px;letter-spacing:-.025em}.teSponsorCopy p{margin:0;color:var(--muted,#6c6b67);font-size:13px;line-height:1.5}.teSponsorCopy a{display:inline-flex;margin-top:12px;color:var(--accent,#355345);font-size:12px;font-weight:850;text-decoration:none}@media(max-width:760px){.teSponsorSlot{margin:26px 0}.teSponsorCard{grid-template-columns:1fr}.teSponsorMedia{aspect-ratio:16/9;min-height:0}.teSponsorCopy{padding:16px 17px 18px}.teSponsorCopy h3{font-size:19px}}'''
(ROOT / 'sponsored-content.css').write_text(sponsor_css, encoding='utf-8')

sponsor_js = r'''(function(){
  const endpoint='/te-equipamos-arpenaz-27l/news/sponsored-campaigns.json';
  const esc=v=>String(v??'').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[s]));
  function active(c){if(!c||c.active!==true)return false;const now=Date.now(),s=c.start?Date.parse(c.start):0,e=c.end?Date.parse(c.end):Infinity;return (!s||now>=s)&&(!e||now<=e)}
  function renderCampaign(c){let host=document.getElementById('teSponsorSlotHome');if(!host){host=document.createElement('section');host.id='teSponsorSlotHome';host.className='teSponsorSlot';host.setAttribute('aria-label','Publicidad');const hero=document.getElementById('hero');if(hero)hero.insertAdjacentElement('afterend',host);else return}host.classList.add('hasCampaign');host.innerHTML=`<article class="teSponsorCard"><img class="teSponsorMedia" src="${esc(c.image||'')}" alt="${esc(c.title||'Contenido patrocinado')}" loading="lazy" decoding="async"><div class="teSponsorCopy"><span class="teSponsorLabel">PUBLICIDAD · ${esc(c.sponsor||'Patrocinado')}</span><h3>${esc(c.title||'')}</h3><p>${esc(c.description||'')}</p><a href="${esc(c.url||'#')}" target="_blank" rel="sponsored noopener noreferrer" data-track="sponsor_click" data-track-label="${esc(c.sponsor||'Patrocinado')}">Ver contenido patrocinado →</a></div></article>`}
  fetch(endpoint,{cache:'no-store'}).then(r=>r.ok?r.json():[]).then(items=>{const c=(Array.isArray(items)?items:[]).filter(active).find(x=>(x.placement||'home_after_hero')==='home_after_hero');if(c)renderCampaign(c)}).catch(()=>{});
})();'''
(ROOT / 'sponsored-content.js').write_text(sponsor_js, encoding='utf-8')

# ---------- Páginas comerciales ----------
common_css = '''
:root{--bg:#F7F6F2;--surface:#fff;--text:#1D1D1F;--muted:#6C6B67;--line:#DDDCD7;--accent:#355345;--soft:#E7ECE8;--chrome:#F1F1EF}*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}.top{position:sticky;top:0;z-index:20;background:rgba(250,250,248,.86);color:var(--text);border-bottom:1px solid rgba(29,29,31,.10);backdrop-filter:blur(22px) saturate(145%);-webkit-backdrop-filter:blur(22px) saturate(145%)}.topin{max-width:1180px;margin:auto;min-height:68px;padding:0 22px;display:flex;align-items:center;justify-content:space-between;gap:20px}.brand{font-size:18px;font-weight:800;letter-spacing:-.035em;color:inherit;text-decoration:none}.topnav{display:flex;gap:8px;align-items:center}.topnav a{color:var(--muted);text-decoration:none;font-size:12px;font-weight:700;padding:10px 11px;border-radius:999px}.topnav a:hover{background:#fff;color:var(--text)}.wrap{max-width:1120px;margin:auto;padding:0 22px}.hero{padding:90px 0 54px}.eyebrow{font-size:11px;font-weight:900;letter-spacing:.11em;text-transform:uppercase;color:var(--accent)}h1{font-size:clamp(52px,8vw,104px);line-height:.9;letter-spacing:-.07em;margin:14px 0 24px;max-width:10ch}.lead{font-size:clamp(19px,2.1vw,26px);line-height:1.42;color:var(--muted);max-width:780px}.ctaRow{display:flex;gap:10px;flex-wrap:wrap;margin-top:28px}.cta,.ghost{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 18px;border-radius:999px;text-decoration:none;font-size:13px;font-weight:850}.cta{background:var(--accent);color:#fff}.ghost{border:1px solid var(--line);color:var(--text);background:var(--surface)}.section{padding:46px 0 70px}.section h2{font-size:clamp(34px,5vw,58px);line-height:1;letter-spacing:-.055em;margin:0 0 22px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:23px}.card span{font-size:10px;font-weight:900;letter-spacing:.09em;text-transform:uppercase;color:var(--accent)}.card h3{font-size:20px;letter-spacing:-.025em;margin:8px 0}.card p,.copy p,.copy li{color:var(--muted);line-height:1.6}.metric{font-size:36px;font-weight:800;letter-spacing:-.055em}.note{background:var(--soft);border-radius:18px;padding:20px 22px;color:var(--muted);line-height:1.55}.copy{max-width:820px}.copy h2{font-size:32px;margin-top:42px}.copy ul{padding-left:20px}.footer{border-top:1px solid #d6d6d2;margin-top:50px;background:#E6E6E2;text-align:center}.footerin{max-width:1120px;margin:auto;padding:36px 22px 46px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;color:var(--muted);font-size:12px;text-align:center}.footer a{color:inherit;text-decoration:none;margin-right:14px}.footer a:hover{color:var(--accent)}@media(max-width:780px){.topnav{display:none}.hero{padding-top:58px}.grid{grid-template-columns:1fr}.section{padding:34px 0 54px}.cta,.ghost{width:100%}}
'''

def page(title, desc, body, canonical, robots='index,follow,max-image-preview:large'):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{h.escape(title)}</title><meta name="description" content="{h.escape(desc)}"><meta name="robots" content="{robots}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:site_name" content="Te Equipamos"><meta property="og:title" content="{h.escape(title)}"><meta property="og:description" content="{h.escape(desc)}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><style>{common_css}</style></head><body><header class="top"><div class="topin"><a class="brand" href="{HUB}">Te Equipamos</a><nav class="topnav"><a href="{HUB}">Inicio</a><a href="{HUB}anunciate/">Anúnciate</a><a href="{HUB}media-kit/">Media Kit</a><a href="{HUB}metodologia/">Cómo trabajamos</a></nav></div></header>{body}<footer class="footer"><div class="footerin"><b>Te Equipamos</b><div><a href="{HUB}metodologia/">Cómo trabajamos</a><a href="{HUB}anunciate/">Anúnciate</a><a href="{HUB}media-kit/">Media Kit</a><a href="{HUB}privacidad/">Privacidad</a><a href="{HUB}cookies/">Cookies</a></div></div></footer><script defer src="/te-equipamos-arpenaz-27l/te-business-analytics.js"></script></body></html>'''

wa_ad = 'https://wa.me/' + WHATSAPP + '?text=' + quote('Hola Te Equipamos. Quiero información comercial sobre publicidad, contenido patrocinado o una landing para mi marca.')

anunciate_body = f'''<main><section class="hero"><div class="wrap"><div class="eyebrow">TE EQUIPAMOS · COLABORACIONES</div><h1>Tu marca, bien presentada.</h1><p class="lead">Creamos espacios comerciales integrados con la experiencia de Te Equipamos, siempre identificados con claridad. Nada de disfrazar publicidad como contenido editorial.</p><div class="ctaRow"><a class="cta" href="{wa_ad}" target="_blank" rel="noopener" data-track="commercial_lead" data-track-label="Anunciate">Solicitar propuesta por WhatsApp</a><a class="ghost" href="{HUB}media-kit/">Ver Media Kit</a></div></div></section><section class="section"><div class="wrap"><h2>Formatos preparados.</h2><div class="grid"><article class="card"><span>01</span><h3>Landing patrocinada</h3><p>Página propia para producto, lanzamiento o campaña, diseñada con criterio editorial y marcada como colaboración comercial.</p></article><article class="card"><span>02</span><h3>Presencia patrocinada</h3><p>Bloques premium dentro de Te Equipamos, con etiqueta PUBLICIDAD y enlace patrocinado. Solo se activan cuando existe una campaña real.</p></article><article class="card"><span>03</span><h3>Contenido de marca</h3><p>Presentación de producto o historia de marca claramente diferenciada del contenido editorial independiente.</p></article><article class="card"><span>04</span><h3>Lanzamientos</h3><p>Combinación de landing, presencia en portada y distribución interna durante un periodo definido.</p></article><article class="card"><span>05</span><h3>Afiliación</h3><p>Integraciones de producto con trazabilidad y transparencia cuando exista un acuerdo de afiliación verificable.</p></article><article class="card"><span>06</span><h3>Proyectos a medida</h3><p>Experiencias específicas para marcas outdoor, deporte, viaje y equipamiento cuando tengan sentido para la audiencia.</p></article></div></div></section><section class="section"><div class="wrap"><div class="note"><strong>Política comercial.</strong> Toda colaboración pagada se identifica como Publicidad, Patrocinado o Colaboración comercial. La compra de un espacio no convierte una afirmación comercial en opinión editorial de Te Equipamos.</div></div></section></main>'''

media_body = f'''<main><section class="hero"><div class="wrap"><div class="eyebrow">MEDIA KIT · TE EQUIPAMOS</div><h1>Una plataforma que está creciendo.</h1><p class="lead">Productos, reviews, ofertas, actividades y herramientas de decisión dentro de una misma experiencia. Este Media Kit no publica cifras de audiencia hasta que puedan demostrarse con medición real.</p><div class="ctaRow"><a class="cta" href="{wa_ad}" target="_blank" rel="noopener" data-track="commercial_lead" data-track-label="Media Kit">Hablar de una campaña</a><a class="ghost" href="{HUB}anunciate/">Ver formatos</a></div></div></section><section class="section"><div class="wrap"><h2>Lo que sí podemos ofrecer hoy.</h2><div class="grid"><article class="card"><span>PLATAFORMA</span><div class="metric">Editorial</div><p>Hub de descubrimiento con productos, reviews, ofertas, actividades y contenido relacionado.</p></article><article class="card"><span>FORMATO</span><div class="metric">Premium</div><p>Landings y presencia comercial diseñadas para integrarse sin destruir la experiencia de lectura.</p></article><article class="card"><span>MEDICIÓN</span><div class="metric">Preparada</div><p>Eventos de navegación, producto, comparador, búsqueda, contacto y Core Web Vitals listos para conectarse a un proveedor real.</p></article></div></div></section><section class="section"><div class="wrap"><h2>Métricas.</h2><div class="note"><strong>Audiencia y rendimiento comercial: en medición.</strong> No mostramos usuarios, impresiones, CTR, conversiones ni alcance hasta disponer de datos verificables y una muestra suficiente. Cuando exista medición activa, este Media Kit se actualizará con cifras reales.</div></div></section></main>'''

privacy_body = '''<main><section class="hero"><div class="wrap"><div class="eyebrow">PRIVACIDAD</div><h1>Privacidad por defecto.</h1><p class="lead">Te Equipamos ha preparado una arquitectura de medición que no envía datos a terceros mientras no exista un proveedor de analítica activado expresamente.</p></div></section><section class="section"><div class="wrap copy"><h2>Qué ocurre actualmente</h2><p>El sitio puede generar eventos técnicos dentro de la propia página para preparar métricas de navegación y rendimiento. Por sí solos, esos eventos no se transmiten a Te Equipamos ni a un proveedor externo.</p><h2>Preferencias locales</h2><p>Algunas funciones pueden usar almacenamiento local o de sesión del navegador para recordar guardados, vistos recientemente, tema o productos seleccionados en el comparador. Esa información permanece en el dispositivo salvo que en el futuro se conecte un servicio que indique lo contrario.</p><h2>Servicios externos</h2><p>Si pulsas enlaces hacia WhatsApp, redes sociales, medios, tiendas u otros servicios, esos terceros aplican sus propias políticas de privacidad.</p><h2>Antes de activar analítica o publicidad de terceros</h2><p>Esta política deberá actualizarse con el proveedor, finalidad, base jurídica y demás información exigible antes de activar cualquier herramienta que envíe datos fuera del sitio.</p><div class="note"><strong>Documento técnico provisional.</strong> Falta incorporar los datos jurídicos completos del responsable del sitio antes de considerar cerrada la documentación legal.</div></div></section></main>'''

cookies_body = '''<main><section class="hero"><div class="wrap"><div class="eyebrow">COOKIES Y ALMACENAMIENTO</div><h1>Sin cookies publicitarias por defecto.</h1><p class="lead">La arquitectura comercial y de analítica está preparada, pero no activa cookies de medición o publicidad de terceros mientras no exista una configuración real y una política actualizada.</p></div></section><section class="section"><div class="wrap copy"><h2>Almacenamiento funcional</h2><p>Te Equipamos puede utilizar localStorage o sessionStorage para funciones como guardados, vistos recientemente, comparador y preferencias de interfaz. Estos mecanismos sirven para mantener funciones solicitadas por el usuario en el navegador.</p><h2>Analítica</h2><p>Actualmente la capa de eventos no envía métricas a Google Analytics, Plausible, Matomo ni otro proveedor por defecto.</p><h2>Publicidad</h2><p>El sistema de campañas patrocinadas está preparado, pero no carga redes publicitarias de terceros ni cookies de segmentación. Las campañas propias pueden mostrarse desde un archivo interno y siempre se identifican como publicidad.</p><div class="note"><strong>Si en el futuro activamos herramientas que requieran consentimiento,</strong> añadiremos el mecanismo de preferencias y actualizaremos esta información antes de activarlas.</div></div></section></main>'''

legal_body = '''<main><section class="hero"><div class="wrap"><div class="eyebrow">AVISO LEGAL</div><h1>Información pendiente de completar.</h1><p class="lead">La estructura legal está creada, pero no vamos a inventar los datos del titular del sitio.</p></div></section><section class="section"><div class="wrap copy"><h2>Datos que faltan</h2><ul><li>Nombre o razón social del responsable.</li><li>NIF, NIE o identificador fiscal que corresponda.</li><li>Domicilio o dirección a efectos legales.</li><li>Correo electrónico de contacto legal.</li><li>Información adicional exigible según la actividad y jurisdicción aplicable.</li></ul><div class="note"><strong>No se presenta esta página como aviso legal completo.</strong> Permanecerá fuera del índice de buscadores hasta que esos datos se incorporen.</div></div></section></main>'''

pages = {
    'anunciate': page('Anúnciate en Te Equipamos', 'Publicidad, landings patrocinadas y colaboraciones comerciales en Te Equipamos.', anunciate_body, HUB+'anunciate/'),
    'media-kit': page('Media Kit | Te Equipamos', 'Formatos comerciales y capacidades publicitarias de Te Equipamos, sin métricas inventadas.', media_body, HUB+'media-kit/'),
    'privacidad': page('Privacidad | Te Equipamos', 'Información sobre privacidad y arquitectura de medición de Te Equipamos.', privacy_body, HUB+'privacidad/', 'noindex,follow'),
    'cookies': page('Cookies | Te Equipamos', 'Información sobre cookies, almacenamiento local y futuras herramientas de analítica.', cookies_body, HUB+'cookies/', 'noindex,follow'),
    'aviso-legal': page('Aviso legal | Te Equipamos', 'Estructura provisional del aviso legal de Te Equipamos pendiente de datos del titular.', legal_body, HUB+'aviso-legal/', 'noindex,follow'),
}
for slug, content in pages.items():
    d = NEWS / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / 'index.html').write_text(content, encoding='utf-8')

# ---------- Integración en Hub final ----------
hub_path = NEWS / 'index.html'
hub = hub_path.read_text(encoding='utf-8')
analytics_tag = '<script defer id="teBusinessAnalytics" src="/te-equipamos-arpenaz-27l/te-business-analytics.js"></script>'
sponsor_css_tag = '<link id="teSponsoredCss" rel="stylesheet" href="/te-equipamos-arpenaz-27l/sponsored-content.css">'
sponsor_js_tag = '<script defer id="teSponsoredJs" src="/te-equipamos-arpenaz-27l/sponsored-content.js"></script>'
if 'id="teSponsoredCss"' not in hub: hub = hub.replace('</head>', sponsor_css_tag + '</head>', 1)
if 'id="teBusinessAnalytics"' not in hub: hub = hub.replace('</body>', analytics_tag + '</body>', 1)
if 'id="teSponsoredJs"' not in hub: hub = hub.replace('</body>', sponsor_js_tag + '</body>', 1)

if '/news/anunciate/' not in hub:
    needle = '<a class="teHeaderTool" href="/te-equipamos-arpenaz-27l/news/metodologia/"><span>Cómo trabajamos</span><span aria-hidden="true">↗</span></a>'
    extra = needle + '<a class="teHeaderTool" href="/te-equipamos-arpenaz-27l/news/anunciate/"><span>Anúnciate</span><span aria-hidden="true">↗</span></a><a class="teHeaderTool" href="/te-equipamos-arpenaz-27l/news/media-kit/"><span>Media Kit</span><span aria-hidden="true">↗</span></a>'
    if needle in hub: hub = hub.replace(needle, extra, 1)

footer = '''<footer id="teBusinessFooter" style="display:block;clear:both;width:100%;box-sizing:border-box;border-top:1px solid #d6d6d2;margin:0;background:#E6E6E2;text-align:center"><div style="max-width:1180px;margin:auto;padding:38px 22px 44px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;color:var(--muted);font-size:11px;text-align:center"><strong style="color:var(--text);font-size:18px">Te Equipamos</strong><nav aria-label="Información de Te Equipamos" style="display:flex;justify-content:center;flex-wrap:wrap;gap:12px 20px"><a href="/te-equipamos-arpenaz-27l/news/metodologia/" style="color:inherit;text-decoration:none;margin-right:0">Cómo trabajamos</a><a href="/te-equipamos-arpenaz-27l/news/anunciate/" style="color:inherit;text-decoration:none;margin-right:0">Anúnciate</a><a href="/te-equipamos-arpenaz-27l/news/media-kit/" style="color:inherit;text-decoration:none;margin-right:0">Media Kit</a><a href="/te-equipamos-arpenaz-27l/news/privacidad/" style="color:inherit;text-decoration:none;margin-right:0">Privacidad</a><a href="/te-equipamos-arpenaz-27l/news/cookies/" style="color:inherit;text-decoration:none">Cookies</a></nav></div></footer>'''
if 'id="teBusinessFooter"' not in hub: hub = hub.replace('</body>', footer + '</body>', 1)
hub_path.write_text(hub, encoding='utf-8')

# ---------- Analítica preparada en páginas indexables ----------
count_analytics = 0
for p in ROOT.rglob('index.html'):
    if p.relative_to(ROOT).parts[:1] == ('studio',):
        continue
    txt = p.read_text(encoding='utf-8')
    low = txt.lower()
    if '<meta http-equiv="refresh"' in low or 'noindex' in low: continue
    if 'te-business-analytics.js' in txt: continue
    if '</body>' in txt:
        txt = txt.replace('</body>', analytics_tag + '</body>', 1)
        p.write_text(txt, encoding='utf-8')
        count_analytics += 1

# ---------- Sitemap y robots ----------
urls = []
for p in ROOT.rglob('index.html'):
    if p.relative_to(ROOT).parts[:1] == ('studio',):
        continue
    txt = p.read_text(encoding='utf-8')
    low = txt.lower()
    if 'noindex' in low or '<meta http-equiv="refresh"' in low: continue
    m = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', txt, re.I)
    if not m:
        m = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']', txt, re.I)
    if m:
        u = m.group(1).strip()
    else:
        rel = p.relative_to(ROOT)
        u = BASE if rel.as_posix() == 'index.html' else BASE + rel.parent.as_posix().strip('/') + '/'
    if u.startswith(BASE) and u not in urls: urls.append(u)
urls.sort()
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{h.escape(u)}</loc></url>\n' for u in urls) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(xml, encoding='utf-8')
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: ' + BASE + 'sitemap.xml\n', encoding='utf-8')

# ---------- Controles de calidad ----------
checks = {
    'sitemap': (ROOT / 'sitemap.xml').exists() and HUB in xml,
    'robots': 'Sitemap:' in (ROOT / 'robots.txt').read_text(encoding='utf-8'),
    'analytics_asset': (ROOT / 'te-business-analytics.js').exists(),
    'sponsor_config': isinstance(json.loads((NEWS / 'sponsored-campaigns.json').read_text(encoding='utf-8')), list),
    'anunciate': (NEWS / 'anunciate/index.html').exists(),
    'media_kit': (NEWS / 'media-kit/index.html').exists(),
    'legal_noindex': 'noindex' in (NEWS / 'aviso-legal/index.html').read_text(encoding='utf-8').lower(),
    'hub_business_links': '/news/anunciate/' in hub and '/news/media-kit/' in hub,
}
failed = [k for k,v in checks.items() if not v]
if failed: raise RuntimeError('Fallo Business Ready: ' + ', '.join(failed))
print(f'Te Equipamos Business Ready: {len(urls)} URLs en sitemap · analítica preparada en {count_analytics} páginas adicionales · publicidad transparente preparada · Media Kit y Anúnciate activos · legal provisional noindex')

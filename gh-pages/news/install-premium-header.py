from pathlib import Path
import re

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')
OFFICIAL_URL='https://jorgesport.github.io/te-equipamos/'

# Remove prior version if present.
for sid in ['tePremiumHeaderCss']:
    start=html.find(f'<style id="{sid}">')
    if start!=-1:
        end=html.find('</style>',start)
        if end!=-1: html=html[:start]+html[end+8:]
for sid in ['tePremiumHeaderScript']:
    start=html.find(f'<script id="{sid}">')
    if start!=-1:
        end=html.find('</script>',start)
        if end!=-1: html=html[:start]+html[end+9:]

header = f'''<header class="top tePremiumHeader" id="tePremiumHeader">
  <div class="row tePremiumHeaderRow">
    <a href="{OFFICIAL_URL}" class="brand" aria-label="Ir al inicio de Te Equipamos"><span class="mark teFullBrand" aria-hidden="true">Te Equipamos</span><span class="teBrandName">Te Equipamos</span></a>
    <div class="actions tePremiumActions">
      <button class="icon teSearchToggle" id="teSearchToggle" type="button" aria-label="Buscar" aria-expanded="false" aria-controls="searchForm"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.6"></circle><path d="m16 16 4.1 4.1"></path></svg></button>
      <button class="icon menuBtn" id="menuBtn" type="button" aria-label="Abrir menú" aria-expanded="false" aria-controls="teHeaderMenu"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"></path></svg></button>
    </div>
    <form class="search tePremiumSearch" id="searchForm" role="search"><svg class="teSearchGlyph" viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.6"></circle><path d="m16 16 4.1 4.1"></path></svg><input id="searchInput" aria-label="Buscar en Te Equipamos" autocomplete="off" enterkeyhint="search" placeholder="Buscar productos, reviews, actividades y consejos"><button type="button" id="clearBtn" aria-label="Limpiar búsqueda" title="Limpiar búsqueda" hidden>×</button></form>
  </div>
  <nav class="cats" id="cats" aria-label="Secciones de Te Equipamos"></nav>
  <section id="teResponsiveActivities" class="teResponsiveActivities" aria-label="Explorar actividades"></section>
</header>
<div class="teHeaderMenuBackdrop" id="teHeaderMenuBackdrop" aria-hidden="true"></div>
<aside class="teHeaderMenu" id="teHeaderMenu" aria-label="Menú de Te Equipamos" aria-hidden="true">
  <div class="teHeaderMenuTop"><a href="{OFFICIAL_URL}" class="teHeaderMenuBrand" aria-label="Ir al inicio">TE EQUIPAMOS</a><button type="button" id="teHeaderMenuClose" class="teHeaderMenuClose" aria-label="Cerrar menú"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"></path></svg></button></div>
  <div class="teHeaderMenuBody">
    <nav class="teHeaderMenuSections" id="teHeaderMenuSections" aria-label="Secciones"></nav>
    <div class="teHeaderMenuDivider"></div>
    <div class="teHeaderMenuGroup"><span class="teHeaderMenuEyebrow">Explorar actividades</span><div class="teHeaderMenuActivities" id="teHeaderMenuActivities"></div></div>
    <div class="teHeaderMenuDivider"></div>
    <div class="teHeaderMenuTools"><button type="button" class="teHeaderTool" data-header-section="Siguiendo"><span>Guardados</span><span aria-hidden="true">☆</span></button><a class="teHeaderTool" href="/te-equipamos-arpenaz-27l/news/metodologia/"><span>Cómo trabajamos</span><span aria-hidden="true">↗</span></a><button class="teHeaderTool" id="themeBtn" type="button" aria-label="Cambiar tema"><span>Tema</span><span id="teThemeLabel">Automático</span></button></div>
  </div>
</aside>'''

html, n = re.subn(r'<header class="top".*?</header>', header, html, count=1, flags=re.S)
if n != 1:
    html, n = re.subn(r'<header class="top[^\"]*".*?</header>', header, html, count=1, flags=re.S)
if n != 1:
    raise RuntimeError('No se pudo localizar la cabecera actual')

css = r'''<style id="tePremiumHeaderCss">/* TE_PREMIUM_HEADER */
:root{--te-header-bg:rgba(250,250,248,.88);--te-header-fg:#1D1D1F;--te-header-muted:#666A65;--te-header-h:72px}
#tePremiumHeader{position:sticky;top:0;z-index:120;background:var(--te-header-bg)!important;border:0!important;border-bottom:1px solid rgba(29,29,31,.09)!important;box-shadow:0 8px 30px rgba(29,29,31,.055)!important;backdrop-filter:blur(24px) saturate(150%)!important;-webkit-backdrop-filter:blur(24px) saturate(150%)!important;color:var(--te-header-fg)!important}
#tePremiumHeader .tePremiumHeaderRow{height:var(--te-header-h)!important;max-width:1480px;margin:0 auto;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:20px!important;padding:0 34px!important;transition:height .22s ease}
#tePremiumHeader .brand{display:flex;align-items:center;color:var(--te-header-fg)!important;text-decoration:none;min-width:180px}
#tePremiumHeader .mark{width:auto!important;height:auto!important;border-radius:0!important;background:transparent!important;color:var(--te-header-fg)!important;font-size:19px!important;line-height:1!important;font-weight:850!important;letter-spacing:-.045em!important;white-space:nowrap!important}
#tePremiumHeader .teBrandName{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
#tePremiumHeader .tePremiumActions{margin-left:auto;display:flex!important;align-items:center;gap:10px!important}
#tePremiumHeader .icon{display:grid!important;place-items:center;width:46px!important;height:46px!important;border:0!important;border-radius:50%!important;background:transparent!important;color:var(--te-header-fg)!important;cursor:pointer;transition:background .16s ease,transform .16s ease}
#tePremiumHeader .icon:hover{background:rgba(29,29,31,.055)!important}
#tePremiumHeader .icon:active{transform:scale(.96)}
#tePremiumHeader .icon svg{width:27px;height:27px;fill:none;stroke:currentColor;stroke-width:1.65;stroke-linecap:round;stroke-linejoin:round}
#tePremiumHeader .menuBtn{display:grid!important}
#tePremiumHeader .cats,#tePremiumHeader .teResponsiveActivities{display:none!important}
#tePremiumHeader .tePremiumSearch{position:absolute!important;left:50%!important;top:calc(100% + 10px)!important;transform:translate(-50%,-8px)!important;width:min(760px,calc(100vw - 32px))!important;height:54px!important;margin:0!important;padding:0 18px!important;display:flex!important;align-items:center!important;gap:12px!important;background:#FFFFFF!important;border:1px solid rgba(29,29,31,.12)!important;border-radius:18px!important;box-shadow:0 18px 55px rgba(16,20,17,.14)!important;opacity:0;visibility:hidden;pointer-events:none;transition:opacity .18s ease,transform .18s ease,visibility .18s ease;z-index:125}
#tePremiumHeader.searchOpen .tePremiumSearch{opacity:1;visibility:visible;pointer-events:auto;transform:translate(-50%,0)!important}
#tePremiumHeader .teSearchGlyph{width:22px;height:22px;fill:none;stroke:#6C6B67;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;flex:0 0 auto}
#tePremiumHeader .tePremiumSearch input{font-size:16px;color:#1D1D1F!important;background:transparent!important;border:0!important;outline:0!important;min-width:0;flex:1}
#tePremiumHeader .tePremiumSearch input::placeholder{color:#7A7D78}
#tePremiumHeader #clearBtn{width:34px;height:34px;border:0;border-radius:50%;background:#F1F1EF;color:#6C6B67;font-size:21px;line-height:1;cursor:pointer}
#tePremiumHeader.scrolled .tePremiumHeaderRow{height:62px!important}
.teHeaderMenuBackdrop{position:fixed;inset:0;z-index:128;background:rgba(8,10,8,.46);opacity:0;visibility:hidden;pointer-events:none;transition:opacity .22s ease,visibility .22s ease}
.teHeaderMenuBackdrop.open{opacity:1;visibility:visible;pointer-events:auto}
.teHeaderMenu{position:fixed;z-index:129;top:0;right:0;width:min(420px,92vw);height:100dvh;background:#FAFAF8;color:#1D1D1F;box-shadow:-20px 0 60px rgba(8,10,8,.18);transform:translateX(102%);transition:transform .28s cubic-bezier(.2,.75,.25,1);overflow:auto;overscroll-behavior:contain}
.teHeaderMenu.open{transform:translateX(0)}
.teHeaderMenuTop{min-height:76px;display:flex;align-items:center;justify-content:space-between;padding:0 24px;border-bottom:1px solid var(--line)}
.teHeaderMenuBrand{font-size:13px;font-weight:900;letter-spacing:.08em;color:#1D1D1F;text-decoration:none}
.teHeaderMenuClose{width:42px;height:42px;display:grid;place-items:center;border:0;border-radius:50%;background:transparent;color:#1D1D1F;cursor:pointer}
.teHeaderMenuClose:hover{background:var(--surface2)}
.teHeaderMenuClose svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
.teHeaderMenuBody{padding:22px 24px 36px}
.teHeaderMenuSections{display:grid;gap:2px}
.teHeaderMenuSections button{width:100%;border:0;background:transparent;color:#1D1D1F;text-align:left;padding:11px 2px;font-size:27px;line-height:1.15;font-weight:650;letter-spacing:-.035em;cursor:pointer}
.teHeaderMenuSections button:hover,.teHeaderMenuSections button[aria-current="page"]{color:var(--accent)}
.teHeaderMenuDivider{height:1px;background:var(--line);margin:22px 0}
.teHeaderMenuEyebrow{display:block;margin-bottom:12px;color:var(--muted);font-size:10px;font-weight:900;letter-spacing:.09em;text-transform:uppercase}
.teHeaderMenuActivities{display:flex;flex-wrap:wrap;gap:8px}
.teHeaderMenuActivities button{border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:999px;padding:8px 11px;font-size:12px;font-weight:700;cursor:pointer}
.teHeaderMenuActivities button:hover,.teHeaderMenuActivities button[aria-pressed="true"]{border-color:color-mix(in srgb,var(--accent) 40%,var(--line));background:var(--soft);color:var(--accent)}
.teHeaderMenuTools{display:grid;gap:2px}
.teHeaderTool{width:100%;min-height:45px;border:0;background:transparent;color:#1D1D1F;display:flex;align-items:center;justify-content:space-between;gap:14px;text-decoration:none;padding:8px 2px;font-size:14px;cursor:pointer;text-align:left}
.teHeaderTool:hover{color:var(--accent)}
body.teMenuLocked{overflow:hidden}
@media(max-width:760px){
  :root{--te-header-h:64px}
  #tePremiumHeader .tePremiumHeaderRow{height:var(--te-header-h)!important;padding:0 18px!important}
  #tePremiumHeader .mark{font-size:18px!important}
  #tePremiumHeader .icon{width:42px!important;height:42px!important}
  #tePremiumHeader .icon svg{width:25px;height:25px}
  #tePremiumHeader .tePremiumActions{gap:3px!important}
  #tePremiumHeader.scrolled .tePremiumHeaderRow{height:58px!important}
  #tePremiumHeader .tePremiumSearch{top:calc(100% + 8px)!important;width:calc(100vw - 24px)!important;height:52px!important;border-radius:16px!important}
  .teHeaderMenu{width:100%;max-width:none}
  .teHeaderMenuTop{min-height:66px;padding:0 18px}
  .teHeaderMenuBody{padding:20px 20px 34px}
  .teHeaderMenuSections button{font-size:26px;padding:10px 0}
}
@media(prefers-reduced-motion:reduce){#tePremiumHeader .tePremiumHeaderRow,#tePremiumHeader .tePremiumSearch,.teHeaderMenu,.teHeaderMenuBackdrop{transition:none!important}}
</style>'''
html=html.replace('</head>',css+'</head>',1)

script = r'''<script id="tePremiumHeaderScript">/* TE_PREMIUM_HEADER_JS */
(function(){
  const header=document.getElementById('tePremiumHeader');
  const searchToggle=document.getElementById('teSearchToggle');
  const searchForm=document.getElementById('searchForm');
  const searchInput=document.getElementById('searchInput');
  const oldMenuBtn=document.getElementById('menuBtn');
  const menuBtn=oldMenuBtn?oldMenuBtn.cloneNode(true):null;
  if(oldMenuBtn&&menuBtn)oldMenuBtn.replaceWith(menuBtn);
  const menu=document.getElementById('teHeaderMenu');
  const menuBackdrop=document.getElementById('teHeaderMenuBackdrop');
  const closeBtn=document.getElementById('teHeaderMenuClose');
  const sectionHost=document.getElementById('teHeaderMenuSections');
  const activityHost=document.getElementById('teHeaderMenuActivities');
  const themeBtn=document.getElementById('themeBtn');
  const themeLabel=document.getElementById('teThemeLabel');
  const sectionDefs=[['Todas','Inicio'],['Ofertas','Ofertas'],['Ventas','Productos'],['Reviews','Reviews'],['Novedades','Novedades'],['Consejos','Consejos'],['Vídeos','Vídeos'],['Siguiendo','Guardados']];
  const activityLabels={'senderismo':'Senderismo','trekking':'Trekking','running':'Running','trail-running':'Trail running','ciclismo':'Ciclismo','natacion':'Natación','travel':'Travel','alpinismo':'Alpinismo','escalada':'Escalada','camping':'Camping','esqui':'Esquí y nieve','kayak':'Kayak y remo','surf':'Surf','fitness':'Fitness'};
  const esc=v=>String(v??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[ch]));
  function items(){return typeof NEWS!=='undefined'&&Array.isArray(NEWS)?NEWS:[]}
  function sectionCount(section){if(section==='Todas'||section==='Siguiendo')return 1;return items().filter(n=>n.category===section||(Array.isArray(n.sections)&&n.sections.includes(section))).length}
  function activityCounts(){const map=new Map();items().forEach(n=>(Array.isArray(n.activities)?n.activities:[]).forEach(a=>map.set(a,(map.get(a)||0)+1)));return [...map.entries()].filter(([,count])=>count>0).sort((a,b)=>b[1]-a[1]||String(activityLabels[a[0]]||a[0]).localeCompare(String(activityLabels[b[0]]||b[0]),'es'))}
  function renderMenu(){
    if(sectionHost){sectionHost.innerHTML=sectionDefs.filter(([key])=>sectionCount(key)>0).map(([key,label])=>`<button type="button" data-premium-section="${esc(key)}" ${typeof state!=='undefined'&&state.cat===key&&!state.activity?'aria-current="page"':''}>${esc(label)}</button>`).join('')}
    if(activityHost){const active=typeof state!=='undefined'?String(state.activity||''):'';activityHost.innerHTML=activityCounts().map(([key,count])=>`<button type="button" data-premium-activity="${esc(key)}" aria-pressed="${active===key?'true':'false'}">${esc(activityLabels[key]||key)} · ${count}</button>`).join('')}
    syncThemeLabel();
  }
  function openMenu(){renderMenu();menu&&menu.classList.add('open');menuBackdrop&&menuBackdrop.classList.add('open');menu&&menu.setAttribute('aria-hidden','false');menuBackdrop&&menuBackdrop.setAttribute('aria-hidden','false');menuBtn&&menuBtn.setAttribute('aria-expanded','true');document.body.classList.add('teMenuLocked');setTimeout(()=>closeBtn&&closeBtn.focus(),30)}
  function closePremiumMenu(){menu&&menu.classList.remove('open');menuBackdrop&&menuBackdrop.classList.remove('open');menu&&menu.setAttribute('aria-hidden','true');menuBackdrop&&menuBackdrop.setAttribute('aria-hidden','true');menuBtn&&menuBtn.setAttribute('aria-expanded','false');document.body.classList.remove('teMenuLocked')}
  function openSearch(){if(!header)return;header.classList.add('searchOpen');searchToggle&&searchToggle.setAttribute('aria-expanded','true');setTimeout(()=>searchInput&&searchInput.focus(),20)}
  function closeSearch(){if(!header)return;header.classList.remove('searchOpen');searchToggle&&searchToggle.setAttribute('aria-expanded','false')}
  function syncThemeLabel(){if(!themeLabel)return;const t=document.documentElement.dataset.theme||'light';themeLabel.textContent=t==='dark'?'Oscuro':'Claro'}
  if(menuBtn)menuBtn.addEventListener('click',openMenu);
  if(closeBtn)closeBtn.addEventListener('click',closePremiumMenu);
  if(menuBackdrop)menuBackdrop.addEventListener('click',closePremiumMenu);
  if(searchToggle)searchToggle.addEventListener('click',()=>header&&header.classList.contains('searchOpen')?closeSearch():openSearch());
  if(themeBtn)themeBtn.addEventListener('click',()=>setTimeout(syncThemeLabel,0));
  document.addEventListener('click',e=>{
    const s=e.target.closest&&e.target.closest('[data-premium-section]');if(s){const key=s.dataset.premiumSection;closePremiumMenu();if(typeof setCat==='function')setCat(key);return}
    const a=e.target.closest&&e.target.closest('[data-premium-activity]');if(a){const key=a.dataset.premiumActivity;closePremiumMenu();if(typeof applyActivityFilter==='function')applyActivityFilter(key);return}
    if(header&&header.classList.contains('searchOpen')&&!e.target.closest('#tePremiumHeader'))closeSearch();
  });
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(menu&&menu.classList.contains('open')){closePremiumMenu();menuBtn&&menuBtn.focus()}else if(header&&header.classList.contains('searchOpen')){closeSearch();searchToggle&&searchToggle.focus()}}});
  let ticking=false;function onScroll(){if(ticking)return;ticking=true;requestAnimationFrame(()=>{header&&header.classList.toggle('scrolled',window.scrollY>18);ticking=false})}window.addEventListener('scroll',onScroll,{passive:true});onScroll();
  window.addEventListener('popstate',()=>setTimeout(renderMenu,0));
})();
</script>'''
html=html.replace('</body>',script+'</body>',1)
html=re.sub(r'<meta name="theme-color" content="[^"]*">','<meta name="theme-color" content="#FAFAF8">',html,count=1)

for marker in ['id="tePremiumHeader"','id="teSearchToggle"','id="menuBtn"','id="searchInput"','id="themeBtn"','/* TE_PREMIUM_HEADER */','/* TE_PREMIUM_HEADER_JS */']:
    if marker not in html: raise RuntimeError('Falta marcador de cabecera: '+marker)
if 'bolsa' in header.lower() or 'bag' in header.lower(): raise RuntimeError('La cabecera no debe incluir bolsa')

path.write_text(html,encoding='utf-8')
print('Cabecera premium clara instalada: Te Equipamos + búsqueda + menú')

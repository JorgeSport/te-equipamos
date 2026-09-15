from pathlib import Path

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")
meta = '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">'
if 'http-equiv="Cache-Control"' not in html:
    html = html.replace('</head>', meta + '</head>', 1)

# TE_OFFICIAL_SOCIAL_IMAGE: imagen editorial propia usada por Facebook, WhatsApp,
# Telegram y tarjetas sociales. Se entrega desde una URL versionada para evitar
# que las plataformas sigan mostrando una miniatura antigua en caché.
social_image = 'https://res.cloudinary.com/detstbpo9/image/upload/v1789444910/te-equipamos-social-share-v2.jpg'
old_social_image = 'https://res.cloudinary.com/detstbpo9/image/upload/v1789420923/te-equipamos-social-share.png'
html = html.replace(old_social_image, social_image)
html = html.replace('<meta property="og:image:type" content="image/png">', '<meta property="og:image:type" content="image/jpeg">')
html = html.replace('<meta property="og:image:width" content="1200">', '<meta property="og:image:width" content="600">')
html = html.replace('<meta property="og:image:height" content="630">', '<meta property="og:image:height" content="315">')

if f'<meta property="og:image" content="{social_image}">' not in html:
    raise RuntimeError('La nueva imagen social oficial no quedó conectada a og:image')
if f'<meta name="twitter:image" content="{social_image}">' not in html:
    raise RuntimeError('La nueva imagen social oficial no quedó conectada a twitter:image')

# "Sigue explorando" se gestiona exclusivamente desde add-section-journeys.py.
# Si existe una capa antigua de override responsive de despliegues anteriores,
# se elimina para evitar que vuelva a convertir las miniaturas en tarjetas grandes.
start = html.find('<style id="teResponsiveJourneyCompact">')
if start != -1:
    end = html.find('</style>', start)
    if end != -1:
        html = html[:start] + html[end+8:]

# TE_BRAND_IDENTITY: identidad cromática editorial propia de Te Equipamos.
# Es una capa puramente visual: no modifica layout, tamaños, componentes ni responsive.
identity_css = r'''<style id="teBrandIdentity">/* TE_BRAND_IDENTITY */
:root{
  --bg:#F7F6F2;
  --surface:#FFFFFF;
  --surface2:#EFEEE9;
  --text:#1D1D1F;
  --muted:#6C6B67;
  --line:#DDDCD7;
  --accent:#355345;
  --soft:#E7ECE8;
  --shadow:0 1px 2px rgba(29,29,31,.05),0 8px 24px rgba(29,29,31,.04)
}
html[data-theme=dark]{
  --bg:#111310;
  --surface:#181B18;
  --surface2:#20241F;
  --text:#F5F5F2;
  --muted:#A8ADA7;
  --line:#303630;
  --accent:#A6B9AD;
  --soft:#263129;
  --shadow:none
}
::selection{background:var(--soft);color:var(--text)}
a:focus-visible,button:focus-visible,input:focus-visible{outline:2px solid color-mix(in srgb,var(--accent) 58%,transparent);outline-offset:2px}
</style>'''
start = html.find('<style id="teBrandIdentity">')
if start != -1:
    end = html.find('</style>', start)
    if end != -1:
        html = html[:start] + html[end+8:]
html = html.replace('</head>', identity_css + '</head>', 1)

# TE_EDITORIAL_MICRO_POLISH: micro-pulido premium sin alterar estructura.
# Solo afina jerarquía, aire, separadores, imágenes e interacción visual.
polish_css = r'''<style id="teEditorialMicroPolish">/* TE_EDITORIAL_MICRO_POLISH */
:root{--te-hairline:color-mix(in srgb,var(--line) 72%,transparent)}
html{text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
body{letter-spacing:-.004em}
.welcome{margin-bottom:28px}
.welcome h1,.heroCopy h2,.head h2,.journeyHead h2,.recentHead h2,.articleBody h1,.copy h2{font-weight:700;letter-spacing:-.035em}
.welcome p,.head p,.journeyHead p,.summary,.deck,.meta,.cardMeta{color:var(--muted)}
.section{margin-top:34px}
.head{margin-bottom:16px}
.feed,.panel,.railCard,.topic,.place,.recentCard,.article,.related{box-shadow:var(--shadow)}
.card,.heroItem,.journeyCard,.recentCard,.trend li,.rel{transition:background-color .18s ease,color .18s ease}
.card .title,.heroItem h3,.journeyCard strong,.recentCard b,.rel b{transition:color .18s ease}
.card:hover,.heroItem:hover,.recentCard:hover,.rel:hover{background:color-mix(in srgb,var(--surface2) 44%,transparent)}
.card:hover .title,.heroItem:hover h3,.journeyCard:hover strong,.recentCard:hover b,.rel:hover b{color:var(--accent)}
.title:hover{text-decoration:none}
.thumb,.heroMain img,.heroItem img,.journeyMedia img,.recentCard img,.articleHero{object-position:center;background:var(--surface2);transition:filter .18s ease,opacity .18s ease}
.card:hover .thumb,.heroItem:hover img,.journeyCard:hover img,.recentCard:hover img{filter:saturate(.94) contrast(1.01)}
.feed .card,.heroItem,.journeyCard,.trend li,.rel,.byline{border-color:var(--te-hairline)}
.kicker,.journeyCopy small,.recentCard small{letter-spacing:.075em}
.sourceBtn,.follow,.chip,.teRespActivityChip,.saleFilter{transition:background-color .18s ease,color .18s ease,border-color .18s ease,transform .18s ease}
.sourceBtn:hover,.follow:hover,.chip:hover,.teRespActivityChip:hover,.saleFilter:hover{transform:translateY(-1px)}
.copy{line-height:1.82}
.copy p{margin-top:0;margin-bottom:1.35em}
.articleBody h1{max-width:18ch}
.related h3,.railCard h3{letter-spacing:-.02em}
@media(min-width:1101px){
  .shell{padding-top:32px}
  .section{margin-top:38px}
  .journey{margin-top:44px}
  .articleWrap{padding-top:40px}
}
@media(max-width:760px){
  .section{margin-top:28px}
  .head{margin-bottom:12px}
  .journey{margin-top:32px}
  .welcome{margin-bottom:22px}
}
@media(prefers-reduced-motion:reduce){
  .card,.heroItem,.journeyCard,.recentCard,.trend li,.rel,.card .title,.heroItem h3,.journeyCard strong,.recentCard b,.rel b,.thumb,.heroMain img,.heroItem img,.journeyMedia img,.recentCard img,.articleHero,.sourceBtn,.follow,.chip,.teRespActivityChip,.saleFilter{transition:none!important}
}
</style>'''
start = html.find('<style id="teEditorialMicroPolish">')
if start != -1:
    end = html.find('</style>', start)
    if end != -1:
        html = html[:start] + html[end+8:]
html = html.replace('</head>', polish_css + '</head>', 1)

# TE_STRATEGIC_MENU: mantener los nombres internos para no romper filtros,
# pero presentar al visitante un orden más comercial y claro.
menu_script = r'''<script id="teStrategicMenuScript">
(function(){
  const ORDER=['Inicio','Ofertas','Productos','Reviews','Novedades','Consejos','Vídeos','Siguiendo'];
  let scheduled=false;
  function keyOf(text){
    const t=String(text||'').replace(/[⌂★]/g,'').trim();
    if(t==='Ventas'||t==='Productos')return 'Productos';
    return t;
  }
  function renameButton(btn){
    const raw=btn.textContent||'';
    if(raw.includes('Ventas'))btn.textContent=raw.replace('Ventas','Productos');
  }
  function sortContainer(container){
    if(!container)return;
    const buttons=[...container.querySelectorAll(':scope > button')];
    if(!buttons.length)return;
    buttons.forEach(renameButton);
    const desired=[...buttons].sort((a,b)=>{
      const ai=ORDER.indexOf(keyOf(a.textContent));
      const bi=ORDER.indexOf(keyOf(b.textContent));
      return (ai<0?999:ai)-(bi<0?999:bi);
    });
    const same=buttons.every((b,i)=>b===desired[i]);
    if(!same)desired.forEach(b=>container.appendChild(b));
  }
  function refresh(){
    scheduled=false;
    sortContainer(document.getElementById('cats'));
    sortContainer(document.getElementById('nav'));
  }
  function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(refresh)}
  const observer=new MutationObserver(schedule);
  function start(){
    ['cats','nav'].forEach(id=>{const el=document.getElementById(id);if(el)observer.observe(el,{childList:true,subtree:true})});
    refresh();
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
</script>'''
if 'id="teStrategicMenuScript"' not in html:
    html = html.replace('</body>', menu_script + '</body>', 1)

# TE_ACTIVITY_DEPTH: las actividades con muy poco contenido no terminan en un callejón sin salida.
activity_depth_script = r'''<script id="teActivityDepthScript">
(function(){
  function enhanceSparseActivity(slug){
    if(!slug||typeof NEWS==='undefined'||typeof renderActivityAlternatives!=='function')return;
    const count=NEWS.filter(n=>Array.isArray(n.activities)&&n.activities.includes(slug)).length;
    if(count>0&&count<=2){
      setTimeout(()=>{
        renderActivityAlternatives(slug);
        const host=document.getElementById('activityAlternatives');
        const head=host&&host.querySelector('.activityAlternativesHead');
        if(head)head.innerHTML='<h3>Sigue explorando</h3><p>Esta actividad todavía tiene pocos contenidos. Aquí tienes otras actividades con publicaciones disponibles.</p>';
      },60);
    }
  }
  if(typeof applyActivityFilter==='function'){
    const original=applyActivityFilter;
    window.applyActivityFilter=function(value){const result=original.apply(this,arguments);enhanceSparseActivity(String(value||'').trim().toLowerCase());return result};
  }
})();
</script>'''
if 'id="teActivityDepthScript"' not in html:
    html = html.replace('</body>', activity_depth_script + '</body>', 1)

path.write_text(html, encoding="utf-8")

injector = Path(__file__).resolve().parent / 'editorial-injector.py'
code = compile(injector.read_text(encoding='utf-8'), str(injector), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(injector)})

print('Política de caché actualizada · imagen social oficial v2 activa · identidad Bosque Editorial activa · micro-pulido editorial activo · actividades sin callejones sin salida · selección editorial y progreso de lectura activos · menú estratégico activo')

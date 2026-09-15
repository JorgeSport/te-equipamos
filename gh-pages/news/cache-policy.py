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

# TE_RESPONSIVE_JOURNEY_COMPACT: solo corrige la capa secundaria "Sigue explorando"
# en móvil. No modifica tarjetas principales, navegación, escritorio ni filtros.
responsive_journey_css = r'''<style id="teResponsiveJourneyCompact">/* TE_RESPONSIVE_JOURNEY_COMPACT */
@media(max-width:760px){
  .journey{margin-top:26px;padding-top:20px;border-top:1px solid var(--line)}
  .journeyHead{display:block;padding:0 14px;margin-bottom:8px}
  .journeyHead .kicker{font-size:9px;letter-spacing:.08em}
  .journeyHead h2{margin-top:3px;font-size:20px;line-height:1.15}
  .journeyHead p{margin-top:5px;font-size:12px;line-height:1.45}
  .journeyGrid,.journeyGrid.count1,.journeyGrid.count2{display:block;padding:0 12px}
  .journeyCard,.journeyGrid.count1 .journeyCard,.journeyGrid.count2 .journeyCard{display:block;width:100%;margin:0;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent;box-shadow:none;overflow:visible}
  .journeyCard:hover{transform:none;box-shadow:none;background:var(--surface2)}
  .journeyCardInner,.journeyHero .journeyCardInner,.journeySide .journeyCardInner,.journeyWide .journeyCardInner{height:auto;min-height:88px;display:grid;grid-template-columns:minmax(0,1fr) 84px;align-items:center;gap:10px}
  .journeyCopy,.journeyHero .journeyCopy,.journeySide .journeyCopy,.journeyWide .journeyCopy{padding:11px 4px 11px 2px}
  .journeyCopy small{margin-bottom:4px;font-size:9px;letter-spacing:.06em}
  .journeyCopy strong,.journeyHero .journeyCopy strong,.journeyWide .journeyCopy strong{font-size:14px;line-height:1.28}
  .journeyCopy p,.journeySide .journeyCopy p,.journeyWide .journeyCopy p{display:none}
  .journeyCta{margin-top:5px;font-size:10px}
  .journeyMedia,.journeyHero .journeyMedia,.journeyWide .journeyMedia{order:0;width:84px;height:68px;aspect-ratio:auto;border-radius:10px;overflow:hidden}
  .journeyMedia img{width:100%;height:100%;object-fit:cover}
  .journeyCard:nth-child(even) .journeyCardInner{grid-template-columns:1fr}
  .journeyCard:nth-child(even) .journeyMedia{display:none}
}
</style>'''
if 'id="teResponsiveJourneyCompact"' not in html:
    html = html.replace('</head>', responsive_journey_css + '</head>', 1)
if '/* TE_RESPONSIVE_JOURNEY_COMPACT */' not in html:
    raise RuntimeError('No se pudo fijar el diseño compacto de Sigue explorando en responsive')

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

path.write_text(html, encoding="utf-8")
print('Política de caché actualizada · imagen social oficial v2 activa · menú estratégico activo · Sigue explorando compacto en responsive')

from pathlib import Path

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")
meta = '<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">'
if 'http-equiv="Cache-Control"' not in html:
    html = html.replace('</head>', meta + '</head>', 1)

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
print('Política de caché actualizada · menú: Inicio, Ofertas, Productos, Reviews, Novedades, Consejos, Vídeos, Siguiendo')

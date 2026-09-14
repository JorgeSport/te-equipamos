from pathlib import Path

base = Path(__file__).resolve().parent
index = base / 'index.html'
data = base / 'news-data.json'

# Sustitución del recurso antiguo conocido.
old_img = 'https://contents.mediadecathlon.com/p1017638/k$acfc8255883c31e43fb353aa7ddfe230/daunenjacke-x-light2-damen-schwarz.jpg'
new_img = 'https://contents.mediadecathlon.com/p1017720/k$68617b1a72d5486a1684964419d42a71/women-s-x-light-2-black-trekking-down-jacket.jpg'

if data.exists():
    text = data.read_text(encoding='utf-8').replace(old_img, new_img)
    data.write_text(text, encoding='utf-8')

html = index.read_text(encoding='utf-8').replace(old_img, new_img)

# Esta regla se inyecta al final y manda sobre el responsive anterior.
# Mantiene en móvil el patrón Google News: texto + miniatura lateral.
css = r'''/* TE_IMAGE_FAILSAFE */
.card img.thumb.te-img-failed{display:none!important;width:0!important;height:0!important;min-height:0!important;aspect-ratio:auto!important;margin:0!important;padding:0!important}
@media(max-width:760px){
  .feed .card{display:grid!important;grid-template-columns:minmax(0,1fr) 108px!important;gap:12px!important;padding:16px 16px 18px!important;margin:0 0 10px!important;align-items:start!important;background:var(--surface)!important;border-bottom:1px solid var(--line)!important}
  .feed .card>div:first-child{padding:0!important;min-width:0!important}
  .feed .card .thumb{order:initial!important;width:108px!important;height:82px!important;min-height:0!important;aspect-ratio:auto!important;object-fit:cover!important;border-radius:11px!important;align-self:start!important;margin:0!important;background:var(--surface2)!important}
  .feed .card.noThumb{grid-template-columns:1fr!important}
  .feed .card.noThumb .thumb{display:none!important}
  .feed .card .title{font-size:20px!important;line-height:1.22!important;margin:7px 0 10px!important}
  .feed .card .summary{display:none!important}
  .feed .card .cardMeta{font-size:12px!important;padding-bottom:0!important}
  .feed .card .tagRow{margin:8px 0!important}
  .feed .card .cardShare{margin:8px 0!important}
}
'''
if '/* TE_IMAGE_FAILSAFE */' in html:
    start = html.index('/* TE_IMAGE_FAILSAFE */')
    end = html.find('</style>', start)
    if end != -1:
        # Solo sustituimos nuestro bloque anterior, no otros estilos.
        old_end = html.find('\n', start)
        # Si ya existe nuestra regla móvil nueva, no duplicar.
        if '.feed .card{display:grid!important' not in html[start:end]:
            html = html[:start] + css + html[end:]
else:
    html = html.replace('</style>', css + '</style>', 1)

js = r'''<script id="teImageFailsafe">
(function(){
  function fail(img){
    if(!img) return;
    img.classList.add('te-img-failed');
    img.setAttribute('aria-hidden','true');
    const card=img.closest&&img.closest('.card');
    if(card) card.classList.add('noThumb');
  }
  function guard(img){
    if(!img || img.dataset.teImgGuard==='1') return;
    img.dataset.teImgGuard='1';
    img.addEventListener('error',()=>fail(img),{once:true});
    if(img.complete && img.naturalWidth===0) fail(img);
  }
  function scan(root){(root||document).querySelectorAll('img.thumb').forEach(guard)}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>scan(document));
  else scan(document);
  const start=()=>{
    if(!document.body) return;
    new MutationObserver(m=>m.forEach(x=>x.addedNodes.forEach(n=>{
      if(n.nodeType!==1) return;
      if(n.matches&&n.matches('img.thumb')) guard(n);
      if(n.querySelectorAll) scan(n);
    }))).observe(document.body,{childList:true,subtree:true});
  };
  if(document.body) start(); else document.addEventListener('DOMContentLoaded',start,{once:true});
})();
</script>'''

if 'id="teImageFailsafe"' in html:
    a = html.find('<script id="teImageFailsafe">')
    b = html.find('</script>', a)
    if a != -1 and b != -1:
        html = html[:a] + js + html[b+9:]
else:
    html = html.replace('</body>', js + '</body>', 1)

index.write_text(html, encoding='utf-8')
print('Tarjetas móviles compactas: eliminado el hueco blanco y añadida protección de miniaturas')

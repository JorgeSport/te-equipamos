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

# Protección general: si una imagen falla, desaparece sin reservar espacio.
failsafe_css = r'''/* TE_IMAGE_FAILSAFE */
.card img.thumb.te-img-failed{display:none!important;width:0!important;height:0!important;min-height:0!important;aspect-ratio:auto!important;margin:0!important;padding:0!important}
'''
if '/* TE_IMAGE_FAILSAFE */' not in html:
    html = html.replace('</style>', failsafe_css + '</style>', 1)

# Restauración explícita del responsive de las tarjetas principales.
# IMPORTANTE: este bloque no modifica "Sigue explorando". Esa sección se controla
# exclusivamente desde add-section-journeys.py para evitar reglas contradictorias.
responsive_css = r'''<style id="teResponsiveRestore">
@media(max-width:760px){
  .feed{border-left:0!important;border-right:0!important;border-radius:0!important;box-shadow:none!important;background:transparent!important}
  .feed .card{display:flex!important;flex-direction:column!important;grid-template-columns:none!important;gap:0!important;padding:0 0 22px!important;margin:0 0 14px!important;background:var(--surface)!important;border-bottom:8px solid var(--bg)!important;align-items:stretch!important}
  .feed .card>div:first-child{padding:18px 18px 0!important;min-width:0!important;order:0!important}
  .feed .card .thumb{display:block!important;order:-1!important;width:100%!important;height:auto!important;min-height:0!important;aspect-ratio:16/9!important;object-fit:cover!important;border-radius:0!important;align-self:stretch!important;margin:0!important;background:var(--surface2)!important}
  .feed .card.noThumb{display:block!important}
  .feed .card.noThumb .thumb,.feed .card .thumb.te-img-failed{display:none!important}
  .feed .card .title{font-size:23px!important;line-height:1.22!important;margin:8px 0 14px!important;letter-spacing:-.01em!important}
  .feed .card .summary{display:none!important}
  .feed .card .cardMeta{font-size:13px!important;padding-bottom:2px!important}
  .feed .card .tagRow{margin:8px 0!important}
  .feed .card .cardShare{margin:8px 0!important}
}
</style>'''

# Elimina una versión previa de esta restauración y coloca la actual al final del <head>.
start = html.find('<style id="teResponsiveRestore">')
if start != -1:
    end = html.find('</style>', start)
    if end != -1:
        html = html[:start] + html[end+8:]
html = html.replace('</head>', responsive_css + '</head>', 1)

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
print('Responsive de tarjetas restaurado sin modificar Sigue explorando')

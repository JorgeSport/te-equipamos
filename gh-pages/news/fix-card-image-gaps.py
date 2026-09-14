from pathlib import Path

base = Path(__file__).resolve().parent
index = base / 'index.html'
data = base / 'news-data.json'

# Algunos recursos antiguos pueden dejar de responder. Sustituimos el caso conocido
# y, además, instalamos una protección general para cualquier imagen futura que falle.
old_img = 'https://contents.mediadecathlon.com/p1017638/k$acfc8255883c31e43fb353aa7ddfe230/daunenjacke-x-light2-damen-schwarz.jpg'
new_img = 'https://contents.mediadecathlon.com/p1017720/k$68617b1a72d5486a1684964419d42a71/women-s-x-light-2-black-trekking-down-jacket.jpg'

if data.exists():
    text = data.read_text(encoding='utf-8').replace(old_img, new_img)
    data.write_text(text, encoding='utf-8')

html = index.read_text(encoding='utf-8').replace(old_img, new_img)

css = r'''/* TE_IMAGE_FAILSAFE */
.card img.thumb.te-img-failed{display:none!important;width:0!important;height:0!important;min-height:0!important;aspect-ratio:auto!important;margin:0!important;padding:0!important}
'''
if '/* TE_IMAGE_FAILSAFE */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

js = r'''<script id="teImageFailsafe">
(function(){
  function guard(img){
    if(!img || img.dataset.teImgGuard==='1') return;
    img.dataset.teImgGuard='1';
    const fail=()=>{
      if(img.classList.contains('thumb')){
        img.classList.add('te-img-failed');
        img.setAttribute('aria-hidden','true');
      }
    };
    img.addEventListener('error',fail,{once:true});
    if(img.complete && img.naturalWidth===0) fail();
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
if 'id="teImageFailsafe"' not in html:
    html = html.replace('</body>', js + '</body>', 1)

index.write_text(html, encoding='utf-8')
print('Protección de imágenes aplicada: sin huecos blancos si una miniatura falla')

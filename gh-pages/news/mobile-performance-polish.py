from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

# Quitar una versión previa si existiera.
for sid, closing in [('teMobilePerformanceCss', '</style>'), ('teMobilePerformanceScript', '</script>')]:
    tag = '<style' if closing == '</style>' else '<script'
    start = html.find(f'{tag} id="{sid}">')
    if start != -1:
        end = html.find(closing, start)
        if end != -1:
            html = html[:start] + html[end + len(closing):]

css = r'''<style id="teMobilePerformanceCss">/* TE_MOBILE_PERFORMANCE */
html{scroll-behavior:smooth}
button,a,input,[role="button"],[role="link"]{touch-action:manipulation}
img{max-width:100%}
@supports(content-visibility:auto){
  .journey,.recentSection,.activityAlternatives,.teEditorialPick,.teEditorialRail,.section:not(#feedSection){
    content-visibility:auto;contain-intrinsic-size:auto 520px
  }
}
@media(max-width:760px){
  html{scroll-padding-top:70px}
  body{overflow-x:hidden;-webkit-text-size-adjust:100%}
  #tePremiumHeader .icon{width:44px!important;height:44px!important;min-width:44px!important;min-height:44px!important}
  #tePremiumHeader .brand{min-height:44px}
  #tePremiumHeader .tePremiumSearch{max-width:calc(100vw - 20px)!important}
  .teHeaderMenuBody{padding-bottom:max(34px,env(safe-area-inset-bottom))!important}
  .heroMain img,.thumb,.heroItem img,.recentCard img,.journeyMedia img{background:var(--surface2)}
  .heroCopy h2{overflow-wrap:anywhere}
  .card .title{overflow-wrap:anywhere}
  .card .save,.cardShareBtn,.follow,.saleFilter,.teRespActivityChip,.activityAlternative{min-height:44px}
  .sourceBtn{min-height:44px;display:inline-flex!important;align-items:center;justify-content:center}
  .teCompareButton{min-height:40px}
}
@media(max-width:390px){
  #tePremiumHeader .teBrandName{font-size:17px!important}
  #tePremiumHeader .tePremiumHeaderRow{padding-left:14px!important;padding-right:10px!important;gap:10px!important}
  #tePremiumHeader .tePremiumActions{gap:0!important}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
</style>'''
html = html.replace('</head>', css + '</head>', 1)

script = r'''<script id="teMobilePerformanceScript">/* TE_MOBILE_PERFORMANCE_JS */
(function(){
  function tuneImages(root){
    const scope=root&&root.querySelectorAll?root:document;
    scope.querySelectorAll('img').forEach(img=>{
      if(img.closest('.heroMain')){
        img.setAttribute('fetchpriority','high');
        img.setAttribute('decoding','async');
        if(!img.getAttribute('loading'))img.setAttribute('loading','eager');
      }else{
        if(!img.getAttribute('loading'))img.setAttribute('loading','lazy');
        if(!img.getAttribute('decoding'))img.setAttribute('decoding','async');
        img.setAttribute('fetchpriority','low');
      }
    });
  }
  function tuneInteractive(root){
    const scope=root&&root.querySelectorAll?root:document;
    scope.querySelectorAll('button,a,[role="button"],[role="link"]').forEach(el=>{
      if(!el.style.touchAction)el.style.touchAction='manipulation';
    });
  }
  function tune(root){tuneImages(root);tuneInteractive(root)}
  const start=()=>{
    tune(document);
    const observer=new MutationObserver(records=>{
      for(const record of records){
        for(const node of record.addedNodes){if(node.nodeType===1)tune(node)}
      }
    });
    observer.observe(document.body,{childList:true,subtree:true});
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
</script>'''
html = html.replace('</body>', script + '</body>', 1)

for marker in ['/* TE_MOBILE_PERFORMANCE */','/* TE_MOBILE_PERFORMANCE_JS */']:
    if marker not in html:
        raise RuntimeError('No se instaló el pulido móvil/rendimiento: ' + marker)

path.write_text(html, encoding='utf-8')
print('Pulido móvil y rendimiento progresivo instalados')

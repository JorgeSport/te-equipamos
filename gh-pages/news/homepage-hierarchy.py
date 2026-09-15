from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

# Evitar duplicar visualmente la marca: la cabecera ya muestra "Te Equipamos" completo.
# Conservamos un H1 semántico para estructura y accesibilidad, pero no ocupa espacio visual.
html = html.replace('<h1>Te Equipamos</h1>', '<h1 class="teHomeSemanticTitle">Te Equipamos</h1>', 1)

css = r'''<style id="teHomepageHierarchyCss">/* TE_HOMEPAGE_HIERARCHY */
.welcome .teHomeSemanticTitle{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important;border:0!important}
.welcome .teHomeSemanticTitle + #today{margin:0!important}
#hero .teKickerLink{appearance:none;border:0;background:transparent;padding:0;margin:0;color:var(--accent);font:inherit;font-weight:inherit;letter-spacing:inherit;text-transform:inherit;cursor:pointer}
#hero .teKickerLink:hover{text-decoration:underline;text-underline-offset:3px}
#hero .teKickerLink:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px}
#hero .teKickerStatus{color:var(--muted);font-weight:800;letter-spacing:.075em;text-transform:uppercase}
#hero .teKickerSep{color:var(--muted);padding:0 4px}
@media(prefers-reduced-motion:reduce){#hero .teKickerLink{transition:none!important}}
</style>'''
if 'id="teHomepageHierarchyCss"' not in html:
    html = html.replace('</head>', css + '</head>', 1)

script = r'''<script id="teHomepageHierarchyScript">/* TE_HOMEPAGE_HIERARCHY_JS */
(function(){
  const PUBLIC_LABELS={Ventas:'Productos'};
  function publicLabel(cat){return PUBLIC_LABELS[cat]||cat}
  function enhanceKickers(){
    const hero=document.getElementById('hero');
    if(!hero)return;
    hero.querySelectorAll('.kicker').forEach(k=>{
      if(k.dataset.teKickerEnhanced==='1')return;
      const raw=(k.textContent||'').trim();
      if(!raw)return;
      const parts=raw.split('·').map(x=>x.trim()).filter(Boolean);
      const cat=parts[0]||'';
      if(!cat)return;
      k.dataset.teKickerEnhanced='1';
      k.textContent='';
      const btn=document.createElement('button');
      btn.type='button';
      btn.className='teKickerLink';
      btn.dataset.teKickerCat=cat;
      btn.textContent=publicLabel(cat);
      btn.setAttribute('aria-label','Ver '+publicLabel(cat));
      k.appendChild(btn);
      if(parts.length>1){
        const sep=document.createElement('span');sep.className='teKickerSep';sep.textContent='·';k.appendChild(sep);
        const status=document.createElement('span');status.className='teKickerStatus';status.textContent=parts.slice(1).join(' · ');k.appendChild(status);
      }
    });
  }
  document.addEventListener('click',e=>{
    const btn=e.target.closest&&e.target.closest('[data-te-kicker-cat]');
    if(!btn)return;
    e.preventDefault();e.stopPropagation();
    const cat=btn.dataset.teKickerCat||'';
    if(typeof setCat==='function')setCat(cat);
  });
  const hero=document.getElementById('hero');
  if(hero)new MutationObserver(enhanceKickers).observe(hero,{childList:true,subtree:true});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',enhanceKickers,{once:true});else enhanceKickers();
  window.addEventListener('pageshow',()=>setTimeout(enhanceKickers,30));
})();
</script>'''
if 'id="teHomepageHierarchyScript"' not in html:
    html = html.replace('</body>', script + '</body>', 1)

if '<h1>Te Equipamos</h1>' in html:
    raise RuntimeError('Sigue existiendo el título duplicado visible de Te Equipamos en portada')
if '<h1 class="teHomeSemanticTitle">Te Equipamos</h1>' not in html:
    raise RuntimeError('No se instaló el H1 semántico de portada')
if 'data-te-kicker-cat' not in html:
    raise RuntimeError('No se instaló la navegación de categorías del destacado')

path.write_text(html, encoding='utf-8')
print('Portada corregida: solo fecha visible bajo la cabecera y categorías del hero navegables')

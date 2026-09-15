from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

# Eliminar una versión previa si existiera.
for sid, closing in [('teDesktopQuickNavCss', '</style>'), ('teDesktopQuickNavScript', '</script>')]:
    tag = '<style' if closing == '</style>' else '<script'
    start = html.find(f'{tag} id="{sid}">')
    if start != -1:
        end = html.find(closing, start)
        if end != -1:
            html = html[:start] + html[end + len(closing):]

# Insertar la barra dentro de la cabecera premium, justo bajo la fila principal.
if 'id="teDesktopQuickNav"' not in html:
    anchor = '</div>\n  <nav class="cats" id="cats"'
    replacement = '</div>\n  <nav class="teDesktopQuickNav" id="teDesktopQuickNav" aria-label="Accesos rápidos"></nav>\n  <nav class="cats" id="cats"'
    if anchor not in html:
        raise RuntimeError('No se encontró el punto seguro para instalar la navegación rápida')
    html = html.replace(anchor, replacement, 1)

css = r'''<style id="teDesktopQuickNavCss">/* TE_DESKTOP_QUICK_NAV */
#tePremiumHeader .teDesktopQuickNav{
  min-height:40px;display:flex;align-items:center;justify-content:center;gap:30px;
  padding:0 34px;border-top:1px solid rgba(255,255,255,.055);
  background:var(--te-header-bg);overflow:hidden;
  transition:max-height .22s ease,min-height .22s ease,opacity .18s ease,transform .22s ease,border-color .18s ease;
  max-height:40px;opacity:1;transform:translateY(0)
}
#tePremiumHeader .teDesktopQuickNav:empty{display:none}
#tePremiumHeader .teDesktopQuickNav button{
  appearance:none;border:0;background:transparent;color:var(--te-header-muted);padding:0;
  font:inherit;font-size:12px;font-weight:650;letter-spacing:.005em;line-height:40px;
  cursor:pointer;white-space:nowrap;position:relative;transition:color .16s ease
}
#tePremiumHeader .teDesktopQuickNav button:hover{color:var(--te-header-fg)}
#tePremiumHeader .teDesktopQuickNav button[aria-current="page"]{color:var(--te-header-fg)}
#tePremiumHeader .teDesktopQuickNav button[aria-current="page"]::after{
  content:"";position:absolute;left:0;right:0;bottom:5px;height:1px;background:var(--te-header-fg);opacity:.72
}
#tePremiumHeader.scrolled .teDesktopQuickNav{
  min-height:0;max-height:0;opacity:0;transform:translateY(-7px);border-top-color:transparent;pointer-events:none
}
@media(max-width:760px){#tePremiumHeader .teDesktopQuickNav{display:none!important}}
@media(prefers-reduced-motion:reduce){#tePremiumHeader .teDesktopQuickNav{transition:none!important}}
</style>'''
html = html.replace('</head>', css + '</head>', 1)

script = r'''<script id="teDesktopQuickNavScript">/* TE_DESKTOP_QUICK_NAV_JS */
(function(){
  const host=document.getElementById('teDesktopQuickNav');
  if(!host)return;
  const defs=[['Todas','Inicio'],['Ventas','Productos'],['Reviews','Reviews'],['Ofertas','Ofertas'],['Novedades','Novedades']];
  const items=()=>typeof NEWS!=='undefined'&&Array.isArray(NEWS)?NEWS:[];
  function count(section){
    if(section==='Todas')return 1;
    return items().filter(n=>n.category===section||(Array.isArray(n.sections)&&n.sections.includes(section))).length;
  }
  function render(){
    const active=typeof state!=='undefined'?String(state.cat||'Todas'):'Todas';
    const activity=typeof state!=='undefined'?String(state.activity||''):'';
    const visible=defs.filter(([key])=>count(key)>0);
    host.innerHTML=visible.map(([key,label])=>`<button type="button" data-quick-section="${key}" ${active===key&&!activity?'aria-current="page"':''}>${label}</button>`).join('');
  }
  host.addEventListener('click',e=>{
    const btn=e.target.closest('[data-quick-section]');
    if(!btn)return;
    if(typeof setCat==='function')setCat(btn.dataset.quickSection);
    setTimeout(render,0);
  });
  document.addEventListener('click',e=>{
    if(e.target.closest&&e.target.closest('[data-premium-section],[data-cat],[data-activity],[data-premium-activity]'))setTimeout(render,0);
  });
  window.addEventListener('popstate',()=>setTimeout(render,0));
  render();
})();
</script>'''
html = html.replace('</body>', script + '</body>', 1)

for marker in ['id="teDesktopQuickNav"', '/* TE_DESKTOP_QUICK_NAV */', '/* TE_DESKTOP_QUICK_NAV_JS */']:
    if marker not in html:
        raise RuntimeError('Falta marcador de navegación rápida: ' + marker)

path.write_text(html, encoding='utf-8')
print('Navegación rápida de escritorio instalada: Inicio · Productos · Reviews · Ofertas · Novedades')

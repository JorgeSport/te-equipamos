from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

old = '<span class="mark" aria-hidden="true">TE</span><span class="teBrandName">Te Equipamos</span>'
new = '<span class="mark teFullBrand" aria-hidden="true">Te Equipamos</span><span class="teBrandName">Te Equipamos</span>'
if old in html:
    html = html.replace(old, new, 1)
elif 'class="mark teFullBrand"' not in html:
    raise RuntimeError('No se pudo localizar la marca visible de la cabecera premium')

start = html.find('<style id="teFullBrandHeaderCss">')
if start != -1:
    end = html.find('</style>', start)
    if end != -1:
        html = html[:start] + html[end+8:]

css = '''<style id="teFullBrandHeaderCss">/* TE_FULL_BRAND_HEADER */
#tePremiumHeader .mark.teFullBrand{
  width:auto!important;
  min-width:0!important;
  font-size:19px!important;
  font-weight:700!important;
  letter-spacing:-.035em!important;
  line-height:1!important;
  white-space:nowrap!important;
}
@media(max-width:760px){
  #tePremiumHeader .mark.teFullBrand{font-size:17px!important;letter-spacing:-.03em!important}
}
</style>'''
html = html.replace('</head>', css + '</head>', 1)

if '>Te Equipamos</span><span class="teBrandName">Te Equipamos</span>' not in html:
    raise RuntimeError('El nombre completo Te Equipamos no quedó visible en la cabecera')

path.write_text(html, encoding='utf-8')
print('Marca completa visible en cabecera: Te Equipamos')

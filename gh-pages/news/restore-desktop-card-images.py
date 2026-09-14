from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

css = r'''/* TE_DESKTOP_CARD_IMAGES */
@media(min-width:1101px){
  .feed .card{display:grid!important;grid-template-columns:minmax(0,1fr) 190px!important;gap:20px!important;padding:18px 22px!important;align-items:center!important;min-height:0!important}
  .feed .card>div:first-child{min-width:0!important;padding:0!important}
  .feed .card>.thumb{display:block!important;width:190px!important;height:132px!important;min-height:0!important;aspect-ratio:auto!important;object-fit:cover!important;border-radius:12px!important;align-self:center!important;margin:0!important;background:var(--surface2)!important}
  .feed .card.noThumb{grid-template-columns:1fr!important}
  .feed .card.noThumb>.thumb,.feed .card>.thumb.te-img-failed{display:none!important}
  .feed .card .save{position:static!important;top:auto!important;right:auto!important;margin-left:auto!important;width:30px!important;height:30px!important;font-size:19px!important;border-radius:50%!important}
}
@media(min-width:1400px){
  .feed .card{grid-template-columns:minmax(0,1fr) 210px!important;gap:22px!important;padding:20px 24px!important}
  .feed .card>.thumb{width:210px!important;height:145px!important}
}
'''

if '/* TE_DESKTOP_CARD_IMAGES */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

path.write_text(html, encoding='utf-8')
print('Imágenes restauradas en tarjetas de escritorio con tamaño editorial')

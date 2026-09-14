from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

css = r'''/* TE_DESKTOP_CARD_IMAGES */
@media(min-width:1101px){
  .feed .card{display:grid!important;grid-template-columns:minmax(0,3fr) minmax(280px,2fr)!important;gap:28px!important;padding:22px 24px!important;align-items:center!important;min-height:0!important}
  .feed .card>div:first-child{min-width:0!important;padding:0!important}
  .feed .card>.thumb{display:block!important;width:100%!important;height:auto!important;min-height:0!important;aspect-ratio:16/9!important;object-fit:contain!important;border-radius:14px!important;align-self:center!important;margin:0!important;background:var(--surface2)!important}
  .feed .card.noThumb{grid-template-columns:1fr!important}
  .feed .card.noThumb>.thumb,.feed .card>.thumb.te-img-failed{display:none!important}
  .feed .card .title{font-size:23px!important;line-height:1.2!important;margin:6px 0 10px!important}
  .feed .card .summary{font-size:14px!important;line-height:1.5!important;margin:0 0 10px!important;max-width:760px!important}
  .feed .card .save{position:static!important;top:auto!important;right:auto!important;margin-left:auto!important;width:30px!important;height:30px!important;font-size:19px!important;border-radius:50%!important}
}
@media(min-width:1400px){
  .feed .card{grid-template-columns:minmax(0,1.55fr) minmax(340px,1fr)!important;gap:34px!important;padding:24px 28px!important}
  .feed .card>.thumb{border-radius:16px!important}
  .feed .card .title{font-size:25px!important}
}
'''

if '/* TE_DESKTOP_CARD_IMAGES */' in html:
    start = html.index('/* TE_DESKTOP_CARD_IMAGES */')
    end = html.find('</style>', start)
    if end != -1:
        html = html[:start] + css + html[end:]
else:
    html = html.replace('</style>', css + '</style>', 1)

path.write_text(html, encoding='utf-8')
print('Tarjetas de escritorio: imagen grande lateral y texto editorial 60/40')

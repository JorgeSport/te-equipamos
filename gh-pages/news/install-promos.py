from pathlib import Path
p=Path(__file__).resolve().parent/'index.html'
h=p.read_text(encoding='utf-8')
css='<link rel="stylesheet" href="promos.css">'
js='<script src="promos.js"></script>'
bar='<div class="promo-bar" id="promoBar"><div class="promo-bar__inner"><span class="promo-bar__tag">PROMOCIÓN PROPIA</span><span class="promo-bar__text">Oportunidades y selecciones de Te Equipamos.</span><button type="button" class="promoBtn" data-cat="Ofertas">Ver ofertas →</button></div></div>'
card='<section class="promo-card" id="promoHome"><small>SELECCIÓN TE EQUIPAMOS · PROMOCIÓN PROPIA</small><h2>Antes de comprar por impulso, mira lo que realmente merece una segunda mirada.</h2><p>Descubre oportunidades y contrástalas con nuestras reviews antes de decidir.</p><div class="promo-card__actions"><button type="button" data-cat="Ofertas">Ver oportunidades</button><button type="button" data-cat="Reviews">Comparar con reviews</button></div></section>'
if css not in h:h=h.replace('</head>',css+'</head>',1)
if 'id="promoBar"' not in h:h=h.replace('<div id="portal">','<div id="portal">'+bar,1)
if 'id="promoHome"' not in h:h=h.replace('<section class="section" id="feedSection">',card+'<section class="section" id="feedSection">',1)
if js not in h:h=h.replace('</body>',js+'</body>',1)
p.write_text(h,encoding='utf-8')
print('Prueba visual de banners instalada')
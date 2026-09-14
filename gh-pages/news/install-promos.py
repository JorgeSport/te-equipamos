from pathlib import Path
import re

p = Path(__file__).resolve().parent / 'index.html'
h = p.read_text(encoding='utf-8')

# La publicidad/promoción propia queda aplazada. Este paso limpia cualquier resto
# sin tocar el resto del diseño ni la navegación editorial.
h = re.sub(r'<div class="promo-bar" id="promoBar">.*?</div></div>', '', h, count=1, flags=re.S)
h = re.sub(r'<section class="promo-card" id="promoHome">.*?</section>', '', h, count=1, flags=re.S)
h = h.replace('<link rel="stylesheet" href="promos.css">', '')
h = h.replace('<script src="promos.js"></script>', '')

p.write_text(h, encoding='utf-8')
print('Inicio limpio: publicidad y promociones propias aplazadas')

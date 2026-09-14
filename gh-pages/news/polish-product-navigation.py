from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL_URL = 'https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/'
STYLE_ID = 'teProductHomeNav'

css = r'''<style id="teProductHomeNav">
.te-breadcrumbbar{font-family:Arial,Helvetica,sans-serif;background:rgba(255,255,255,.96)!important;border-bottom:1px solid #e7e7e7!important;color:#666!important;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
.te-breadcrumbbar-wrap{max-width:1180px!important;min-height:54px!important;padding:0 20px!important;gap:9px!important;font-size:12px!important}
.te-breadcrumbbar .te-homeback{display:inline-flex;align-items:center;gap:9px;color:#161616!important;text-decoration:none!important;font-weight:800!important;letter-spacing:-.01em;flex:0 0 auto}
.te-homeback-arrow{width:30px;height:30px;border:1px solid #dedede;border-radius:50%;display:grid;place-items:center;font-size:17px;line-height:1;background:#fff;color:#222;transition:transform .16s ease,border-color .16s ease}
.te-homeback:hover .te-homeback-arrow{transform:translateX(-2px);border-color:#bdbdbd}
.te-breadcrumbbar-wrap>a:not(.te-homeback){color:#666!important;font-weight:650!important}
.te-breadcrumbbar-wrap>strong{color:#2d2d2d!important;font-weight:700!important}
@media(max-width:720px){
 .te-breadcrumbbar{background:#fff!important}
 .te-breadcrumbbar-wrap{min-height:52px!important;padding:0 14px!important;overflow:visible!important}
 .te-breadcrumbbar-wrap>span,.te-breadcrumbbar-wrap>a:not(.te-homeback),.te-breadcrumbbar-wrap>strong{display:none!important}
 .te-breadcrumbbar .te-homeback{font-size:13px!important;gap:8px}
 .te-homeback-arrow{width:31px;height:31px;font-size:18px}
}
@media(prefers-color-scheme:dark){
 .te-breadcrumbbar{background:rgba(17,19,21,.96)!important;border-color:#303134!important;color:#aeb3b8!important}
 .te-breadcrumbbar .te-homeback{color:#f1f3f4!important}
 .te-homeback-arrow{background:#202124;color:#f1f3f4;border-color:#3c4043}
 .te-breadcrumbbar-wrap>a:not(.te-homeback),.te-breadcrumbbar-wrap>strong{color:#d7d9dc!important}
}
</style>'''

count = 0
for page in ROOT.rglob('index.html'):
    text = page.read_text(encoding='utf-8')
    if 'class="te-breadcrumbbar"' not in text:
        continue

    # Quita una versión anterior del pulido si existiera.
    text = re.sub(r'<style id="teProductHomeNav">.*?</style>', '', text, flags=re.S)

    # Convierte el primer enlace de la ruta en un regreso explícito a la portada oficial.
    text, changed = re.subn(
        r'<a href="(?:https://jorgesport\.github\.io)?/te-equipamos-arpenaz-27l/news/">Te Equipamos</a>',
        f'<a class="te-homeback" href="{OFFICIAL_URL}" aria-label="Volver a Te Equipamos"><span class="te-homeback-arrow" aria-hidden="true">←</span><span>Volver a Te Equipamos</span></a>',
        text,
        count=1,
    )
    if not changed and 'class="te-homeback"' not in text:
        continue

    if '</head>' in text:
        text = text.replace('</head>', css + '</head>', 1)
    page.write_text(text, encoding='utf-8')
    count += 1

if count == 0:
    raise RuntimeError('No se encontró ninguna ficha con navegación Te Equipamos para pulir')

print(f'Navegación de regreso a Te Equipamos mejorada en {count} fichas')

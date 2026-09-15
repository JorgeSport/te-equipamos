from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NEWS = ROOT / "news"
BASE = "https://jorgesport.github.io/te-equipamos/"
NEWS_BASE = BASE + "news/"
PRODUCT_SLUG = "arpenaz-100-27l"
PRODUCT_URL = BASE + PRODUCT_SLUG + "/"
PUBLIC_ROOT = "/te-equipamos/"

root_index = ROOT / "index.html"
news_index = NEWS / "index.html"
product_index = ROOT / PRODUCT_SLUG / "index.html"
sitemap = ROOT / "sitemap.xml"

if not root_index.exists() or not news_index.exists():
    raise RuntimeError("Falta la landing histórica o el Hub antes de promover la portada")

# 1) Conserva la landing histórica de la Arpenaz en una URL propia antes de
# sustituir el index raíz por el Hub editorial.
product_html = root_index.read_text(encoding="utf-8")
if "Arpenaz 100 27 L" not in product_html and "ARPENAZ 100" not in product_html:
    raise RuntimeError("La portada histórica ya no parece ser la landing Arpenaz esperada")
product_html = product_html.replace(BASE, PRODUCT_URL)
product_index.parent.mkdir(parents=True, exist_ok=True)
product_index.write_text(product_html, encoding="utf-8")

# 2) Promueve el Hub generado a la raíz sin mover sus assets. Los CSS/JS
# editoriales siguen viviendo bajo /news/, pero canonical, Open Graph,
# schema y enlaces de inicio pasan a la URL oficial raíz.
hub = news_index.read_text(encoding="utf-8")
if "tePremiumHeader" not in hub or "Te Equipamos | Deporte, actividades y equipamiento" not in hub:
    raise RuntimeError("El archivo news/index.html no contiene el Hub aprobado")

# Reemplazos exactos de la URL de inicio. No se cambian rutas auxiliares
# como /news/metodologia/ ni los assets /news/*.css y /news/*.js.
hub = hub.replace(f'href="{NEWS_BASE}"', f'href="{BASE}"')
hub = hub.replace(f'content="{NEWS_BASE}"', f'content="{BASE}"')
hub = hub.replace(f'"url":"{NEWS_BASE}"', f'"url":"{BASE}"')
hub = hub.replace('href="./metodologia/"', f'href="{PUBLIC_ROOT}news/metodologia/"')

root_index.write_text(hub, encoding="utf-8")

# 3) /news/ queda como URL antigua compatible. Conserva query y hash para
# enlaces previos a secciones, búsquedas o artículos internos.
redirect = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Te Equipamos</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{BASE}">
<meta http-equiv="refresh" content="0;url={PUBLIC_ROOT}">
<script>location.replace('{PUBLIC_ROOT}'+location.search+location.hash)</script>
</head>
<body><p>Te estamos llevando a <a href="{PUBLIC_ROOT}">Te Equipamos</a>.</p></body>
</html>'''
news_index.write_text(redirect, encoding="utf-8")

# 4) El sitemap debe considerar la raíz como portada canónica y no /news/.
if sitemap.exists():
    xml = sitemap.read_text(encoding="utf-8")
    xml = xml.replace(f"<loc>{NEWS_BASE}</loc>", f"<loc>{BASE}</loc>")
    sitemap.write_text(xml, encoding="utf-8")

# 5) Validaciones de migración. Fallar aquí impide publicar una portada rota.
root_html = root_index.read_text(encoding="utf-8")
redirect_html = news_index.read_text(encoding="utf-8")
product_check = product_index.read_text(encoding="utf-8")

checks = {
    "hub_en_raiz": "tePremiumHeader" in root_html,
    "canonical_raiz": f'href="{BASE}"' in root_html,
    "sin_canonical_news": f'href="{NEWS_BASE}"' not in root_html,
    "redirect_news_noindex": 'name="robots" content="noindex,follow"' in redirect_html,
    "producto_conservado": "Arpenaz 100 27 L" in product_check or "ARPENAZ 100" in product_check,
    "producto_url_propia": PRODUCT_URL in product_check,
    "asset_css_presente": (NEWS / "editorial-experience.css").exists(),
    "asset_js_presente": (NEWS / "editorial-experience.js").exists(),
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError("Migración de portada incompleta: " + ", ".join(failed))

if sitemap.exists():
    xml = sitemap.read_text(encoding="utf-8")
    if f"<loc>{NEWS_BASE}</loc>" in xml:
        raise RuntimeError("El sitemap todavía publica /news/ como portada")

print(
    "PORTADA OFICIAL ACTIVA · "
    f"{BASE} · Hub promovido · /news/ redirige · producto conservado en {PRODUCT_URL}"
)

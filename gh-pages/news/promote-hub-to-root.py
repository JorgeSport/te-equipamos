from pathlib import Path
from html import escape
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
NEWS = ROOT / "news"
BASE = "https://jorgesport.github.io/te-equipamos/"
NEWS_BASE = BASE + "news/"
PRODUCT_SLUG = "arpenaz-100-27l"
PRODUCT_URL = BASE + PRODUCT_SLUG + "/"
PRODUCT_REPOSITORY = "te-equipamos-arpenaz-100-27l"
PRODUCT_TARGET = "https://jorgesport.github.io/te-equipamos-arpenaz-100-27l/"
PUBLIC_ROOT = "/te-equipamos/"
FOOTER_LOADER = '<script defer src="https://jorgesport.github.io/te-equipamos/universal-footer.js" data-te-universal-footer-loader></script>'

root_index = ROOT / "index.html"
news_index = NEWS / "index.html"
product_index = ROOT / PRODUCT_SLUG / "index.html"
sitemap = ROOT / "sitemap.xml"

if not root_index.exists() or not news_index.exists():
    raise RuntimeError("Falta la landing histórica o el Hub antes de promover la portada")

# 1) La landing histórica ya vive en un repositorio independiente. Conserva
# esta ruta como redirección compatible antes de sustituir la portada.
product_html = root_index.read_text(encoding="utf-8")
if "Arpenaz 100 27 L" not in product_html and "ARPENAZ 100" not in product_html:
    raise RuntimeError("La portada histórica ya no parece ser la landing Arpenaz esperada")
product_index.parent.mkdir(parents=True, exist_ok=True)
product_index.write_text(f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{PRODUCT_TARGET}">
<title>Arpenaz 100 27 L · Te Equipamos</title></head>
<body><p>Te estamos llevando al producto… <a href="{PRODUCT_TARGET}">Abrir producto</a>.</p>
<script>location.replace('{PRODUCT_TARGET}'+location.search+location.hash);</script>
</body></html>''', encoding="utf-8")

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

# La lista de contenidos ya se sincroniza durante el build. Evitamos consultar
# la API pública de GitHub desde el navegador, porque puede alcanzar el rate limit
# y mostrar errores 403 sin aportar nada a la experiencia del usuario.
hub = re.sub(
    r'async function showCurrentContent\(\)\{.*?\}\s*showCurrentContent\(\);',
    "function showCurrentContent(){const id=new URLSearchParams(location.search).get('id');id?renderArticle(id):renderPortal();}\\nshowCurrentContent();",
    hub,
    count=1,
    flags=re.S,
)

# La interfaz enriquece estas zonas con JavaScript, pero los enlaces esenciales
# también deben existir en el HTML inicial. Así los buscadores y los usuarios
# sin JavaScript pueden descubrir las fichas sin alterar el diseño hidratado.
if sitemap.exists():
    sitemap_xml = sitemap.read_text(encoding="utf-8")
    sitemap_urls = list(dict.fromkeys(re.findall(r"<loc>([^<]+)</loc>", sitemap_xml)))
    excluded_prefixes = (
        "news/", "read/", "studio/", "arpenaz-100-27l/",
    )
    cards = []
    for url in sitemap_urls:
        parsed = urlparse(url)
        if parsed.netloc.lower() != "jorgesport.github.io":
            continue
        path = parsed.path
        for public_prefix in ("/te-equipamos/",):
            if path.startswith(public_prefix):
                path = path[len(public_prefix):]
                break
        relative = path.strip("/")
        if not relative or relative.startswith(excluded_prefixes):
            continue
        page = ROOT / relative / "index.html"
        if not page.exists():
            continue
        page_html = page.read_text(encoding="utf-8")
        if re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', page_html, re.I):
            continue
        title_match = re.search(r"<title>(.*?)</title>", page_html, re.I | re.S)
        title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else relative.replace("-", " ").title()
        title = re.sub(r"\s*[|·—-]\s*Te Equipamos.*$", "", title, flags=re.I).strip() or title
        cards.append(
            '<article class="card te-static-card"><div>'
            '<div class="meta">Te Equipamos · Contenido propio</div>'
            f'<a class="title" href="{escape(url, quote=True)}">{escape(title)}</a>'
            '<p class="summary">Consulta la ficha completa, disponibilidad y detalles.</p>'
            '</div></article>'
        )

    if cards:
        empty_feed = '<div class="feed" id="feed"></div>'
        static_feed = '<div class="feed" id="feed">' + "".join(cards) + '</div>'
        if empty_feed not in hub:
            raise RuntimeError("No se encontró el contenedor inicial del feed para prerenderizar enlaces")
        hub = hub.replace(empty_feed, static_feed, 1)

# El footer oficial se carga desde un único componente central. Mantener el
# loader aquí garantiza que cada despliegue del Hub conserve el footer aunque
# news/index.html se regenere por completo.
if 'data-te-universal-footer-loader' not in hub:
    if '</body>' not in hub:
        raise RuntimeError("El Hub no contiene </body> para instalar el footer universal")
    hub = hub.replace('</body>', FOOTER_LOADER + '</body>', 1)

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
# Tras sustituir /news/ por la raíz se deduplican también todas las URLs,
# para impedir que una transformación posterior deje dos entradas iguales.
if sitemap.exists():
    xml = sitemap.read_text(encoding="utf-8")
    xml = xml.replace(f"<loc>{NEWS_BASE}</loc>", f"<loc>{BASE}</loc>")
    locations = re.findall(r"<loc>([^<]+)</loc>", xml)
    unique_locations = list(dict.fromkeys(locations))
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url>\n    <loc>{url}</loc>\n  </url>\n' for url in unique_locations
    ) + '</urlset>\n'
    sitemap.write_text(xml, encoding="utf-8")

# 5) Validaciones de migración. Fallar aquí impide publicar una portada rota.
root_html = root_index.read_text(encoding="utf-8")
redirect_html = news_index.read_text(encoding="utf-8")
product_check = product_index.read_text(encoding="utf-8")

checks = {
    "hub_en_raiz": "tePremiumHeader" in root_html,
    "canonical_raiz": f'href="{BASE}"' in root_html,
    "sin_canonical_news": f'<link rel="canonical" href="{NEWS_BASE}">' not in root_html,
    "redirect_news_noindex": 'name="robots" content="noindex,follow"' in redirect_html,
    "producto_conservado": "Arpenaz 100 27 L" in product_check,
    "producto_url_propia": PRODUCT_TARGET in product_check,
    "asset_css_presente": (NEWS / "editorial-experience.css").exists(),
    "asset_js_presente": (NEWS / "editorial-experience.js").exists(),
    "footer_universal": 'data-te-universal-footer-loader' in root_html,
    "enlaces_estaticos": 'class="title" href="' in root_html,
}
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise RuntimeError("Migración de portada incompleta: " + ", ".join(failed))

if sitemap.exists():
    xml = sitemap.read_text(encoding="utf-8")
    if f"<loc>{NEWS_BASE}</loc>" in xml:
        raise RuntimeError("El sitemap todavía publica /news/ como portada")
    locations = re.findall(r"<loc>([^<]+)</loc>", xml)
    if len(locations) != len(set(locations)):
        raise RuntimeError("El sitemap contiene URLs duplicadas")

print(
    "PORTADA OFICIAL ACTIVA · "
    f"{BASE} · Hub promovido · footer universal activo · /news/ redirige · producto independiente en {PRODUCT_TARGET} · sitemap sin duplicados"
)

from pathlib import Path
import json

base = Path(__file__).resolve().parent
news_path = base / "news-data.json"
products_path = base / "te-equipamos-content.json"

news = json.loads(news_path.read_text(encoding="utf-8"))
products = [dict(x) for x in json.loads(products_path.read_text(encoding="utf-8")) if x.get("active", True)]

for product in products:
    product["owned"] = True
    product.setdefault("kind", "product")
    product.setdefault("source", "Te Equipamos · Venta")
    product.setdefault("category", "Novedades")
    product.setdefault("time", "Producto · Consultar disponibilidad")
    product.setdefault("featured", False)
    product.setdefault("details", product.get("summary", "Producto de venta de Te Equipamos."))

product_ids = {p.get("id") for p in products}
product_urls = {p.get("url") for p in products}

# El actualizador automático puede haber insertado hasta cinco contenidos propios.
# Se retiran primero para volver a colocar el catálogo completo, sin duplicados.
external = [
    item for item in news
    if not item.get("owned")
    and item.get("id") not in product_ids
    and item.get("url") not in product_urls
]

# Mantiene la portada editorial: una ficha comercial cada cuatro noticias externas.
combined = []
product_index = 0
for idx, item in enumerate(external, start=1):
    combined.append(item)
    if idx % 4 == 0 and product_index < len(products):
        combined.append(products[product_index])
        product_index += 1

# Si hay más productos que huecos entre noticias, se conservan todos al final.
combined.extend(products[product_index:])

news_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"Catálogo Te Equipamos incorporado: {len(products)} productos de venta, {len(combined)} contenidos totales.")

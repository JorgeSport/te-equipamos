from pathlib import Path
import json

base = Path(__file__).resolve().parent
news_path = base / "news-data.json"
products_path = base / "te-equipamos-content.json"

news = json.loads(news_path.read_text(encoding="utf-8"))
products = [dict(x) for x in json.loads(products_path.read_text(encoding="utf-8")) if x.get("active", True)]

# Titulares editoriales: despiertan curiosidad sin inventar ni exagerar.
STRATEGIC_TITLES = {
    920001: "¿27 litros dan para una ruta y para el día a día? Esta Arpenaz intenta hacer las dos cosas",
    920002: "Una camiseta que seca rápido parece simple… hasta que empiezas a caminar con calor",
    920003: "Para pies pequeños, el agarre importa más de lo que parece: así trabaja la NH500",
    920004: "¿Un solo bolso para oficina y gimnasio? El Move 500 apuesta por eso",
    920005: "16 litros que se convierten en 20: una mochila que cambia según el plan",
    920006: "250 g y 5000 mm: por qué esta Raincut puede ayudarte cuando cambia el tiempo",
    920007: "Solo 5 litros, pero pensada para que un niño empiece a llevar su propia mochila",
    920008: "¿Plumón en una chaqueta compacta de segunda mano? Esto es lo que ofrece la X-Light 2",
    920009: "Piel, EVA y tacos de 4 mm: una zapatilla de senderismo más seria de lo que parece",
    920010: "El accesorio que muchos olvidan hasta que llevan horas caminando bajo el sol",
    920011: "¿Sandalias para senderos? La clave está en la suela y el ajuste de la NH100",
    920012: "Parece urbana, pero el mesh cambia mucho cuando sube la temperatura",
    920013: "45 gramos y 10 litros: la mochila que casi desaparece cuando no la usas",
    920014: "Cinco bolsillos en 20 litros: por qué esta mochila aprovecha mejor el espacio de lo que parece",
}

for product in products:
    product["owned"] = True
    product["kind"] = "product"
    product["direct"] = True
    if product.get("id") in STRATEGIC_TITLES:
        product["title"] = STRATEGIC_TITLES[product["id"]]
    product.setdefault("source", "Te Equipamos · Venta")
    product.setdefault("category", "Novedades")
    product.setdefault("time", "Producto · Consultar disponibilidad")
    product.setdefault("featured", False)
    product.setdefault("details", product.get("summary", "Producto de venta de Te Equipamos."))

product_ids = {p.get("id") for p in products}
product_urls = {p.get("url") for p in products}

# El actualizador automático puede haber insertado contenidos propios.
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

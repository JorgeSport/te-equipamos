# Clasificación de actividades — Te Equipamos

A partir de ahora cada landing que deba aparecer en el Hub declara explícitamente **qué actividad o actividades cubre** y **qué tipo de producto es**.

## Campos obligatorios por contenido

```json
{
  "activities": ["senderismo", "trekking"],
  "product_type": "sandalias",
  "tags": ["quechua", "hombre", "verano"]
}
```

- `activities`: para qué actividades sirve el producto. Puede contener una o varias.
- `product_type`: qué producto es: `mochila`, `zapatillas`, `sandalias`, `camiseta`, `chaqueta`, `sombrero`, `bolso`, etc.
- `tags`: características complementarias, marca, público, material, temporada, estado, etc. **No hace falta repetir aquí la actividad.**

## IDs de actividad recomendados

| Visible | Valor en JSON |
|---|---|
| Senderismo | `senderismo` |
| Trekking | `trekking` |
| Running | `running` |
| Trail running | `trail-running` |
| Ciclismo | `ciclismo` |
| Natación | `natacion` |
| Travel / Viaje | `travel` |
| Alpinismo | `alpinismo` |
| Escalada | `escalada` |
| Camping | `camping` |
| Esquí y nieve | `esqui` |
| Kayak y remo | `kayak` |
| Surf | `surf` |
| Fitness | `fitness` |

El sincronizador admite nuevas actividades: normaliza el nombre a un identificador estable para que el sistema pueda crecer sin rehacer el Hub.

## Ejemplo completo

```json
{
  "brand": "Te Equipamos",
  "schema_version": 2,
  "items": [
    {
      "active": true,
      "type": "sale",
      "sections": ["Ventas", "Novedades"],
      "activities": ["senderismo", "trekking"],
      "product_type": "sandalias",
      "title": "Título editorial del producto",
      "summary": "Resumen del contenido.",
      "url": "https://jorgesport.github.io/repositorio/",
      "image": "https://...",
      "direct": true,
      "tags": ["quechua", "hombre", "verano"]
    }
  ]
}
```

## Cómo funciona en el Hub

1. El Hub lee `activities` desde cada `te-equipamos.json`.
2. **Explorar → Senderismo/Running/etc.** filtra por ese campo, no por palabras sueltas.
3. La tarjeta muestra las actividades como etiquetas propias y separadas de los tags normales.
4. Un mismo producto puede aparecer en varias actividades sin duplicar la landing ni el repositorio.
5. `product_type` queda disponible para futuros filtros como Senderismo → Calzado o Travel → Mochilas.

Si una landing antigua no declara `activities`, el sincronizador intenta inferirlas para mantener compatibilidad, pero el estándar para contenidos nuevos es declararlas siempre.

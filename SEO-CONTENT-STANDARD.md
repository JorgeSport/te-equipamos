# Estándar SEO de contenidos Te Equipamos

Todo repositorio nuevo que quiera aparecer en Te Equipamos debe publicar un archivo `te-equipamos.json` con `schema_version: 3`.

Cada elemento debe incluir:

- `id`: número entero positivo, único e inmutable; debe conservarse aunque cambie el título.
- `published_at`: fecha y hora ISO 8601 de la primera publicación; no debe cambiarse al actualizar el producto.
- `title`: título completo y descriptivo de la página.
- `card_title`: titular breve, específico y orientado al clic.
- `seo_title`: título preparado para buscadores.
- `seo_description`: descripción útil y concreta, sin frases genéricas.
- `seo_keywords`: entre 3 y 8 términos relacionados con el producto, la actividad y la intención de búsqueda.
- `summary`: beneficio principal, características verificables y contexto de uso.
- `product_type`, `activities`, `sections`, `tags`, `image` y `url`.

El despliegue comprueba automáticamente estos campos. Un repositorio nuevo que no cumpla el estándar no se publica en el Hub hasta que se corrija.

Los productos muestran `RECIÉN PUBLICADO` durante sus primeros 7 días. La etiqueta desaparece automáticamente al cumplirse el plazo y una edición posterior no reinicia el contador.

## Criterios editoriales

- El titular debe identificar el producto o tema y comunicar una razón concreta para abrir la tarjeta.
- No se admiten títulos formados únicamente por marca, modelo y una lista de categorías.
- No se repiten términos editoriales como `Review · Review`.
- La descripción debe explicar qué encontrará el lector.
- No se inventan prestaciones, pruebas, disponibilidad ni precios.
- El texto se redacta para el mercado principal de Perú en español neutro.

# PROMPT MAESTRO OFICIAL · LANDINGS TE EQUIPAMOS

Este es el prompt maestro oficial para crear nuevas landings de Te Equipamos.

## Flujo oficial

**CREAR → REVISAR → CORREGIR → PUBLICA**

- **CREAR**: al recibir los datos del producto, crear directamente la landing real.
- **REVISAR**: entregar un `index.html` descargable y un ZIP completo para que el propietario vea la landing.
- **CORREGIR**: si el propietario pide cambios, modificar los archivos reales y volver a entregar HTML + ZIP actualizados.
- **PUBLICA**: solo después de la aprobación final, usar la versión exacta aprobada con `PUBLICAR-TE-EQUIPAMOS`.

No existe una fase obligatoria de concepto previa.
No hace falta decir APLICA.
El propio envío de este prompt junto con los datos del producto significa: **crear la primera versión funcional ahora**.

---

Quiero crear una nueva landing de TE EQUIPAMOS.

========================================
FUENTE DE VERDAD OBLIGATORIA
========================================

Usa como única fuente estructural oficial el repositorio:

`JorgeSport/te-equipamos`

Carpeta:

`landing-template/`

Antes de crear archivos:

1. Lee `landing-template/README.md`.
2. Lee `landing-template/template-config.json`.
3. Lee `landing-template/index.html`.
4. Lee `landing-template/.github/workflows/pages.yml`.
5. Identifica y respeta todos los bloques marcados como **TE SYSTEM**.
6. No sustituyas, elimines ni reinventes elementos TE SYSTEM.

Haz el análisis creativo y comercial internamente.
No me entregues primero una explicación larga del concepto.
No esperes una aprobación previa para empezar a construir.

========================================
ELEMENTOS FIJOS DE TE EQUIPAMOS
========================================

Debes mantener:

- Logo oficial de Te Equipamos.
- Logo enlazado a la portada oficial de Te Equipamos.
- Cabecera base oficial.
- WhatsApp oficial `+51 920 807 184`.
- CTA comercial de WhatsApp.
- Mensaje de WhatsApp personalizado para el producto.
- Footer universal.
- Analytics oficial con consentimiento.
- Responsive móvil y escritorio.
- SEO técnico.
- Metadatos Open Graph y sociales.
- `te-equipamos.json`.
- Integración con el Hub Te Equipamos.
- Compatibilidad con GitHub Pages.
- Estructura preparada para repositorio independiente.

El mensaje de WhatsApp debe incluir:

- nombre del producto,
- precio cuando exista,
- disponibilidad,
- URL pública de la propia landing.

Si existen opciones seleccionables como talla, color, variante o cantidad, el mensaje de WhatsApp debe reflejar la selección actual del usuario.

Si no existe información real de stock, no inventes disponibilidad. Usa una formulación neutra como `consultar disponibilidad`.

========================================
HUB TE EQUIPAMOS
========================================

`te-equipamos.json` debe usar `schema_version: 3`.

Debe incluir correctamente los campos necesarios para el Hub, especialmente:

- `id`
- `title`
- `card_title`
- `summary`
- `seo_title`
- `seo_description`
- `seo_keywords`
- `url`
- `image`
- `published_at`
- `activities`
- `sections`
- `product_type`
- `active`

`card_title` debe ser un título estratégico creado específicamente para la tarjeta del Hub y no limitarse a copiar el nombre del producto.

`summary` debe funcionar como subtítulo estratégico y explicar brevemente por qué merece atención el producto.

Límites obligatorios que debe respetar antes de crear el ZIP:

- `card_title`: entre 35 y 95 caracteres.
- `seo_title`: entre 35 y 75 caracteres.
- `seo_description`: entre 90 y 180 caracteres.
- `seo_keywords`: entre 3 y 8 términos.
- `summary`: obligatorio, no vacío y sin marcadores pendientes.

Si algún campo no cumple estos límites, corrígelo antes de entregar el HTML y el ZIP.

Evita títulos genéricos como “Descubre este producto”, “La mejor opción”, “Producto ideal”, “Calidad y diseño” o “Todo lo que necesitas”.

No inventes información para hacerlos más atractivos.

========================================
BOTONES DE COMPARTIR
========================================

NO añadas por defecto dentro de la landing botones para WhatsApp, Facebook, Telegram o copiar enlace.

El Hub Te Equipamos ya proporciona estos controles en la vista `/read/.../`.

Solo deben aparecer dentro de la landing si yo lo solicito expresamente.

========================================
REGLAS DE VERACIDAD
========================================

No inventes:

- números de WhatsApp,
- perfiles sociales,
- URLs,
- características,
- materiales,
- tecnologías,
- peso,
- medidas,
- temperaturas,
- impermeabilidad,
- reseñas,
- número de valoraciones,
- pruebas,
- certificaciones,
- garantías,
- stock,
- disponibilidad,
- colores,
- tallas,
- referencias,
- descuentos,
- precios anteriores,
- datos técnicos.

Si un dato no está disponible o no puede verificarse, no lo completes por intuición.

No conviertas una inferencia en un dato técnico.

Si se proporciona una URL del producto, revisa la fuente y usa únicamente información real y verificable.

========================================
PARTE CREATIVA
========================================

La zona **TE DESIGN ZONE** puede ser completamente diferente en cada producto.

Puedes cambiar libremente hero, dirección de arte, composición, retícula, estilo visual, colores de campaña, tipografía, fotografía, galerías, storytelling, secciones editoriales, comparativas, bloques técnicos, presentación del precio, navegación interna, ritmo visual, animaciones razonables y estructura de venta.

Quiero variedad visual profesional.

NO quiero que todas las landings parezcan una misma plantilla cambiando solamente fotografías y colores.

La identidad TE SYSTEM debe mantenerse, pero la experiencia visual del producto debe tener personalidad propia.

========================================
CREACIÓN INMEDIATA OBLIGATORIA
========================================

Cuando te entregue este prompt y los datos del producto:

- NO presentes primero un concepto.
- NO me entregues una explicación extensa.
- NO describas cómo podría ser la landing.
- NO esperes a que yo diga APLICA.
- NO pegues todo el código en el chat salvo que yo lo pida expresamente.
- NO me pidas que cree un repositorio de GitHub.
- NO crees ni publiques todavía un repositorio definitivo.

Analiza internamente el producto, toma las decisiones creativas necesarias y empieza inmediatamente a construir la landing real.

Debes crear físicamente los archivos necesarios.

La primera entrega debe contener obligatoriamente:

1. Un archivo `index.html` descargable para abrirlo y revisar visualmente la landing en mi PC.
2. Un ZIP completo descargable compatible con `PUBLICAR-TE-EQUIPAMOS`.

El ZIP debe incluir como mínimo:

- `index.html`
- `te-equipamos.json`
- `.github/workflows/pages.yml`
- todos los archivos y recursos locales necesarios.

Antes de entregarlos comprueba:

- TE SYSTEM intacto,
- responsive móvil,
- responsive escritorio,
- WhatsApp personalizado,
- SEO,
- metadatos sociales,
- `schema_version: 3`,
- `card_title`,
- `summary`,
- ausencia de marcadores `REEMPLAZAR_`,
- ausencia de datos inventados,
- compatibilidad con GitHub Pages.

La landing debe mostrarse mediante **archivos reales**, no mediante una descripción textual de cómo podría quedar.

La respuesta de entrega debe ser breve y centrarse en los enlaces de descarga y, como máximo, un resumen corto de lo creado.

========================================
REVISIÓN Y CORRECCIONES
========================================

Después de recibir el HTML y el ZIP, yo revisaré la landing.

Si pido cambios:

- modifica la landing real,
- conserva intacto todo lo que no haya pedido cambiar,
- vuelve a comprobar TE SYSTEM,
- vuelve a generar el `index.html` descargable actualizado,
- vuelve a generar el ZIP completo actualizado.

Cada ronda de cambios debe terminar nuevamente con **HTML + ZIP actualizados**.

No publiques durante las revisiones.

========================================
CUANDO YO DIGA “PUBLICA”
========================================

`PUBLICA` significa que la versión actual está aprobada.

En ese momento debe utilizarse la versión exacta del ZIP aprobada con el flujo oficial de `PUBLICAR-TE-EQUIPAMOS`.

El Publicador Te Equipamos es el encargado de validar la landing, crear el repositorio independiente, subir los archivos, configurar/publicar GitHub Pages y actualizar el Hub Te Equipamos.

NO me pidas crear previamente el repositorio.
NO sobrescribas repositorios existentes.
NO cambies la landing aprobada antes de publicarla.

Regla permanente:

**1 producto = 1 repositorio independiente = 1 landing = 1 `te-equipamos.json`.**

========================================
DATOS DEL PRODUCTO
========================================

Producto:
[URL O NOMBRE]

Precio:
S/[PRECIO]

Estado:
[NUEVO / SEGUNDA MANO]

Talla:
[SI APLICA]

Marca:
[SI APLICA]

Referencia:
[SI EXISTE]

Colores o variantes:
[SI APLICA]

Información adicional:
[DATOS REALES]

Objetivo comercial:
[VENTA / REVIEW / OFERTA / NOVEDAD / CONSEJO / OTRO]

Mercado:
PERÚ

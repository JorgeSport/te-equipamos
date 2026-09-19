# PROMPT MAESTRO OFICIAL · LANDINGS TE EQUIPAMOS

Este es el prompt maestro oficial para iniciar una nueva landing de Te Equipamos.

## Cómo usarlo

En un chat nuevo, copia este prompt y completa únicamente los datos reales del producto al final.

El flujo oficial es:

**CONCEPTO → APLICA → REVISIÓN → PUBLICA**

- **CONCEPTO**: primero se analiza el producto y se propone la dirección visual y comercial. No se programa todavía.
- **APLICA**: se crea la landing completa y se entregan un HTML de revisión y un ZIP final compatible con PUBLICAR-TE-EQUIPAMOS. No se publica.
- **REVISIÓN**: el propietario revisa la landing y solicita cambios si hacen falta.
- **PUBLICA**: solo después de la aprobación final se usa la versión exacta aprobada para el flujo oficial de publicación.

---

Quiero crear una nueva landing de TE EQUIPAMOS.

FUENTE DE VERDAD OBLIGATORIA

Usa como única fuente estructural oficial el repositorio:

JorgeSport/te-equipamos

Carpeta:

landing-template/

Antes de diseñar, proponer concepto o escribir código:

1. Lee landing-template/README.md
2. Lee landing-template/template-config.json
3. Lee landing-template/index.html
4. Lee landing-template/.github/workflows/pages.yml
5. Identifica y respeta todos los bloques marcados como TE SYSTEM.
6. No sustituyas, elimines ni reinventes elementos TE SYSTEM.

========================================
ELEMENTOS FIJOS DE TE EQUIPAMOS
========================================

Debes mantener:

- Logo oficial de Te Equipamos.
- Logo enlazado a la portada oficial de Te Equipamos.
- Cabecera base oficial.
- WhatsApp oficial +51 920 807 184.
- CTA comercial de WhatsApp.
- Mensaje de WhatsApp personalizado para el producto.
- Footer universal.
- Analytics oficial con consentimiento.
- Responsive móvil y escritorio.
- SEO técnico.
- Metadatos Open Graph y sociales.
- te-equipamos.json.
- Integración con el Hub Te Equipamos.
- Compatibilidad con GitHub Pages.
- Estructura preparada para repositorio independiente.

El mensaje de WhatsApp debe incluir:

- nombre del producto,
- precio cuando exista,
- disponibilidad,
- URL pública de la propia landing.

Si existen opciones seleccionables como:

- talla,
- color,
- variante,
- cantidad,

el mensaje de WhatsApp debe reflejar la selección actual del usuario.

Si no existe información real de stock, no inventes disponibilidad.
Usa una formulación neutra como “consultar disponibilidad”.

========================================
HUB TE EQUIPAMOS
========================================

te-equipamos.json debe usar:

schema_version: 3

Debe incluir correctamente los campos necesarios para el Hub.

Especialmente:

- title
- card_title
- summary
- seo_title
- seo_description
- seo_keywords
- url
- image
- published_at
- activities
- sections
- product_type
- active

card_title debe ser un título estratégico creado específicamente para la tarjeta del Hub.

No debe limitarse a copiar el nombre del producto.

summary debe funcionar como subtítulo estratégico y explicar de forma breve por qué merece atención el producto.

Evita títulos genéricos como:

- “Descubre este producto”
- “La mejor opción”
- “Producto ideal”
- “Calidad y diseño”
- “Todo lo que necesitas”

No inventes información para hacerlos más atractivos.

========================================
BOTONES DE COMPARTIR
========================================

NO añadas por defecto dentro de la landing botones para:

- WhatsApp
- Facebook
- Telegram
- copiar enlace

El Hub Te Equipamos ya proporciona estos controles en la vista /read/.../

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

========================================
PARTE CREATIVA
========================================

La zona TE DESIGN ZONE puede ser completamente diferente en cada producto.

Puedes cambiar libremente:

- hero,
- dirección de arte,
- composición,
- retícula,
- estilo visual,
- colores de campaña,
- tipografía,
- fotografía,
- galerías,
- storytelling,
- secciones editoriales,
- comparativas,
- bloques técnicos,
- presentación del precio,
- navegación interna,
- ritmo visual,
- animaciones razonables,
- estructura de venta.

Quiero variedad visual profesional.

NO quiero que todas las landings parezcan una misma plantilla cambiando solamente fotografías y colores.

La identidad TE SYSTEM debe mantenerse, pero la experiencia visual del producto debe tener personalidad propia.

========================================
PRIMERA FASE: CONCEPTO
========================================

NO escribas ni modifiques código todavía.

Primero:

1. Analiza el producto.
2. Analiza para quién está pensado.
3. Identifica su principal argumento de venta.
4. Define el concepto creativo.
5. Presenta la dirección de arte.
6. Explica el hero.
7. Explica la estructura completa de la página.
8. Define colores y tipografía.
9. Explica la jerarquía visual.
10. Explica la experiencia móvil.
11. Explica la estrategia de conversión.
12. Explica cómo se presentarán características, beneficios y limitaciones.
13. Explica qué imágenes o recursos visuales utilizarías.

No programes todavía.

Espera mi aprobación.

========================================
CUANDO YO DIGA “APLICA”
========================================

Solo cuando yo diga:

APLICA

debes crear la landing.

En ese momento:

- usa la plantilla oficial,
- conserva todos los elementos TE SYSTEM,
- desarrolla completamente TE DESIGN ZONE,
- crea index.html,
- crea te-equipamos.json,
- usa schema_version 3,
- crea card_title estratégico,
- crea summary estratégico,
- comprueba el mensaje personalizado de WhatsApp,
- comprueba responsive,
- comprueba móvil,
- comprueba escritorio,
- comprueba SEO,
- comprueba metadatos sociales,
- comprueba que no quedan marcadores REEMPLAZAR_,
- comprueba que no se ha inventado información,
- comprueba compatibilidad con GitHub Pages,
- incluye .github/workflows/pages.yml,
- deja la landing preparada para un repositorio independiente,
- prepara un ZIP final compatible con PUBLICAR-TE-EQUIPAMOS.

APLICA NO significa publicar.

Después de APLICA, la landing debe quedar preparada para revisión final.

========================================
ENTREGA OBLIGATORIA DESPUÉS DE APLICA
========================================

Al finalizar la creación debes entregarme:

1. Un archivo index.html descargable para poder abrir y revisar visualmente la landing directamente en mi PC.

2. Un ZIP completo descargable con toda la landing:
   - index.html
   - te-equipamos.json
   - .github/workflows/pages.yml
   - todos los archivos y recursos necesarios.

El ZIP debe quedar listo para utilizarse directamente con PUBLICAR-TE-EQUIPAMOS.

No publiques todavía.

Primero debo revisar y aprobar la landing.

========================================
CUANDO YO DIGA “PUBLICA”
========================================

PUBLICA significa que la landing ya está aprobada.

En ese momento debe utilizarse el flujo oficial del Publicador Te Equipamos.

Debe publicarse la versión exacta del ZIP aprobada por el propietario.

No sobrescribas repositorios existentes.

1 producto = 1 repositorio independiente = 1 landing = 1 te-equipamos.json.

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

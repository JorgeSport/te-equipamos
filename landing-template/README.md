# Te Equipamos · Landing Template

Plantilla maestra para crear nuevas landings de producto sin perder la identidad ni la infraestructura de Te Equipamos.

## Regla de uso

Cada producto nuevo debe terminar como:

**1 producto/proyecto = 1 repositorio independiente = 1 landing = 1 `te-equipamos.json`.**

Esta carpeta es la fuente de verdad para crear esos repositorios. No es una landing comercial definitiva.

## BLOQUEADO: no reinventar

En una landing nueva se mantienen:

- Marca `Te Equipamos`.
- Logo universal enlazado a `https://jorgesport.github.io/te-equipamos/`.
- WhatsApp oficial: `+51 920 807 184` (`51920807184` en enlaces).
- Mensaje de WhatsApp personalizado para el producto.
- Enlace de la landing incluido dentro del mensaje de WhatsApp.
- Precio incluido en el mensaje cuando esté definido.
- Si hay selector de color, talla, variante o cantidad, el mensaje debe incluir la selección actual.
- Cabecera base de Te Equipamos.
- Footer universal.
- Analítica con consentimiento usando la configuración central de Te Equipamos.
- Responsive móvil.
- Manifiesto `te-equipamos.json` para que el Hub descubra y clasifique la landing.
- Título estratégico y subtítulo estratégico para la tarjeta del Hub.
- GitHub Pages mediante Actions.

## Título y subtítulo estratégicos para el Hub

Toda landing que se publique e integre en Te Equipamos debe entrar al Hub con una presentación editorial propia. No basta con copiar el nombre del producto y una ficha técnica.

Reglas obligatorias:

- `card_title` = **título estratégico visible en la tarjeta del Hub**. Debe generar interés con un beneficio real, un dato diferenciador, una tensión útil o un contexto de uso. No debe ser simplemente `Marca + modelo + categoría`.
- `summary` = **subtítulo estratégico visible bajo el título**. Debe complementar al título explicando el beneficio, el uso o la razón por la que ese producto merece atención, sin repetir literalmente el título.
- `title` también debe tener enfoque editorial y puede ser algo más amplio que `card_title`.
- No inventar datos para hacer el copy más atractivo. La estrategia se construye únicamente con información real del producto.
- El título estratégico debe tener entre 35 y 95 caracteres para mantener una buena jerarquía en escritorio y móvil.
- Antes de publicar, comprobar cómo se verá el conjunto `card_title + summary` dentro de Te Equipamos.

Ejemplo correcto:

`card_title`: `24 g, categoría 3 y visión envolvente: unas gafas pensadas para moverse`

`summary`: `Protección 100 % anti-UV, lente oscura y diseño envolvente para ciclismo, ciudad y viajes cuando el sol aprieta.`

Ejemplo a evitar:

`card_title`: `Gafas Roadr 100 Categoría 3 · ciclismo y urbano`

## WhatsApp: comportamiento obligatorio

No basta con enlazar al número.

El CTA debe abrir `51920807184` con un mensaje comercial específico. Como mínimo debe contener:

1. Nombre real del producto.
2. Precio, cuando exista.
3. Petición de disponibilidad o consulta.
4. URL de la landing bajo el texto `Enlace del producto:`.

El archivo central `landing-core.js` genera automáticamente ese mensaje usando `meta[name="te:product"]`, `meta[name="te:price"]` y la URL actual.

Si la landing tiene opciones dinámicas como color o talla, el código creativo debe actualizar `data-te-message` con la selección real y después llamar:

`window.TeEquipamosLanding.refreshWhatsApp()`

Ejemplo de mensaje esperado:

`Hola Te Equipamos, deseo consultar por Mochila X. Color: Verde. Talla: M. Precio: S/199.00. Quisiera confirmar disponibilidad.\n\nEnlace del producto: https://...`

## Compartir: responsabilidad del Hub Te Equipamos

Los controles para compartir por WhatsApp, Facebook, Telegram y copiar enlace **no son obligatorios dentro de la landing independiente**.

El Hub de Te Equipamos los añade en la experiencia `/read/.../` junto con categoría, etiquetas y otros elementos editoriales. Por tanto, una landing nueva no debe duplicar ese bloque salvo que el propietario lo pida expresamente para una campaña concreta.

Regla por defecto:

- Landing independiente: WhatsApp comercial personalizado.
- Hub `/read/.../`: compartir por WhatsApp, Facebook, Telegram y copiar enlace.

No inventar perfiles oficiales de Instagram, TikTok, Facebook u otras redes. Solo añadir perfiles si sus URLs oficiales están verificadas y configuradas expresamente.

## LIBRE: aquí sí cambia el diseño

Se puede rediseñar por completo:

- hero,
- composición,
- fotografías,
- paleta de campaña,
- tipografía de campaña,
- galerías,
- storytelling,
- comparativas,
- fichas técnicas,
- bloques de oferta,
- orden y narrativa de la landing.

La variedad visual es intencionada. La identidad y la infraestructura no deben cambiar.

## Archivos del molde

- `index.html`: shell oficial + zona creativa.
- `te-equipamos.json`: manifiesto del producto para el Hub.
- `.github/workflows/pages.yml`: validación y publicación en GitHub Pages.

Los recursos centrales se sirven desde el Hub:

- `landing-shell.css`
- `landing-core.js`
- `universal-footer.js`
- `te-analytics-provider.js`

## Prompt maestro oficial y flujo de trabajo

El archivo oficial es:

`landing-template/PROMPT-MAESTRO-LANDING.md`

Debe leerse junto con este README, `template-config.json`, `index.html` y `.github/workflows/pages.yml`.

El flujo oficial es:

**CREAR → REVISAR → CORREGIR → PUBLICA**

1. **CREAR**: al recibir el prompt y los datos del producto, crear inmediatamente la primera versión funcional. No presentar primero un concepto ni esperar `APLICA`.
2. **REVISAR**: entregar obligatoriamente un `index.html` descargable y un ZIP completo compatible con `PUBLICAR-TE-EQUIPAMOS`.
3. **CORREGIR**: si el propietario pide cambios, modificar los archivos reales y volver a entregar HTML + ZIP actualizados.
4. **PUBLICA**: solo después de la aprobación final. Utilizar la versión exacta aprobada con el Publicador Te Equipamos.
5. No pedir al propietario que cree previamente un repositorio. `PUBLICAR-TE-EQUIPAMOS` crea el repositorio independiente.
6. Nunca sobrescribir repositorios existentes.
7. Regla permanente: **1 producto = 1 repositorio independiente = 1 landing = 1 `te-equipamos.json`.**

### Regla de entrega

La primera respuesta útil debe materializar la landing en archivos.

No sustituir la entrega por una explicación larga del concepto.

La entrega debe contener:

- `index.html` descargable para revisión,
- ZIP completo descargable,
- una respuesta breve con los enlaces y, como máximo, un resumen corto.

Cada corrección debe volver a terminar con HTML + ZIP actualizados.

La publicación en GitHub se realiza únicamente después de la aprobación final.

## Prompt corto para un chat nuevo

`Quiero crear una nueva landing de Te Equipamos. Abre y lee JorgeSport/te-equipamos-prompts/LANDINGS/PROMPT-MAESTRO-LANDING.md y úsalo como instrucciones obligatorias. Lee también los archivos oficiales de JorgeSport/te-equipamos/landing-template/. Crea directamente la primera versión real y entrégame index.html descargable + ZIP compatible con PUBLICAR-TE-EQUIPAMOS. No me presentes primero un concepto, no esperes APLICA, no publiques todavía y no me pidas crear un repositorio.`

## Reglas de contenido

- Mercado principal: Perú.
- Español neutro.
- No inventar características, pruebas, valoraciones, garantías, disponibilidad ni precios.
- No publicar nombres de terceros que el propietario haya pedido excluir de los textos comerciales.
- El CTA comercial debe usar `data-te-whatsapp`; el núcleo central construye el enlace oficial automáticamente.
- Nunca sustituir el número oficial por otro número.
- Nunca dejar un mensaje genérico si existen datos del producto disponibles.
- Nunca inventar perfiles sociales.

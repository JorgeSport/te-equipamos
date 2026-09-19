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

El archivo oficial para iniciar nuevas landings es:

`landing-template/PROMPT-MAESTRO-LANDING.md`

Ese archivo define el flujo obligatorio y debe leerse junto con este README, `template-config.json`, `index.html` y `.github/workflows/pages.yml`.

El flujo oficial es:

**CONCEPTO → APLICA → REVISIÓN → PUBLICA**

1. **CONCEPTO**: analizar el producto, su público, argumento de venta, dirección de arte, hero, estructura, colores, tipografía, móvil y estrategia de conversión. No escribir código todavía.
2. **APLICA**: crear la landing completa respetando TE SYSTEM, generar `index.html`, `te-equipamos.json` con `schema_version: 3`, workflow de Pages, SEO, WhatsApp personalizado, responsive y todos los recursos necesarios.
3. Después de **APLICA**, entregar obligatoriamente:
   - un `index.html` descargable para revisión visual;
   - un ZIP completo compatible con `PUBLICAR-TE-EQUIPAMOS`.
4. **APLICA no publica**. El propietario revisa la versión entregada y puede pedir cambios.
5. **PUBLICA**: solo después de una aprobación explícita. Debe utilizarse la versión exacta aprobada y el flujo oficial del Publicador Te Equipamos.
6. Nunca sobrescribir repositorios existentes.
7. Regla permanente: **1 producto = 1 repositorio independiente = 1 landing = 1 `te-equipamos.json`.**

### Regla de revisión

La landing debe poder revisarse localmente antes de publicarse.

El HTML de revisión debe permitir comprobar:

- diseño real,
- imágenes disponibles,
- precio,
- CTA de WhatsApp,
- comportamiento responsive,
- SEO básico,
- elementos TE SYSTEM aplicables.

La publicación en GitHub se realiza únicamente después de la aprobación final.

## Prompt corto para un chat nuevo

`Quiero crear una nueva landing de Te Equipamos. Usa como fuente de verdad obligatoria JorgeSport/te-equipamos/landing-template/ y sigue landing-template/PROMPT-MAESTRO-LANDING.md. Lee también README.md, template-config.json, index.html y .github/workflows/pages.yml. Primero presenta únicamente el concepto visual y comercial y espera mi aprobación. Cuando diga APLICA, crea la landing completa y entrégame un HTML descargable de revisión y un ZIP compatible con PUBLICAR-TE-EQUIPAMOS. APLICA no significa publicar. Solo cuando diga PUBLICA debe pasar al flujo oficial de publicación.`

## Reglas de contenido

- Mercado principal: Perú.
- Español neutro.
- No inventar características, pruebas, valoraciones, garantías, disponibilidad ni precios.
- No publicar nombres de terceros que el propietario haya pedido excluir de los textos comerciales.
- El CTA comercial debe usar `data-te-whatsapp`; el núcleo central construye el enlace oficial automáticamente.
- Nunca sustituir el número oficial por otro número.
- Nunca dejar un mensaje genérico si existen datos del producto disponibles.
- Nunca inventar perfiles sociales.

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
- GitHub Pages mediante Actions.

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

## Flujo rápido obligatorio

El objetivo es ahorrar tiempo. Cuando el propietario entregue el enlace del producto, precio, imágenes, referencias y demás datos, **no se debe parar en una explicación conceptual antes de generar la vista previa**.

1. Leer `README.md` y `template-config.json`.
2. Revisar la fuente del producto y usar solo datos reales y verificables.
3. Analizar la referencia visual aportada, si existe.
4. Crear directamente una primera versión funcional en HTML siguiendo la plantilla oficial.
5. Entregar un **HTML descargable/abrible como vista previa** para que el propietario vea el diseño real en móvil y escritorio.
6. No crear todavía el repositorio definitivo ni publicar en GitHub Pages.
7. Si el propietario pide cambios, modificar la vista previa HTML hasta que quede aprobada.
8. Solo después de una aprobación explícita como `APROBADO`, `PUBLICA`, `SUBE`, `CREA EL REPOSITORIO` o equivalente, preparar el repositorio independiente.
9. Crear/copiar `te-equipamos.json` y el workflow oficial.
10. Publicar en GitHub Pages.
11. Confirmar la URL pública, WhatsApp, responsive, SEO e integración con el Hub.

### Regla de vista previa

La primera entrega después de recibir los datos del producto debe ser **la landing real en HTML**, no solo una descripción del concepto. Se puede resumir brevemente la idea visual, pero no se debe pedir una aprobación previa para empezar el HTML.

La vista previa debe incluir ya:

- diseño real,
- imágenes disponibles,
- precio,
- CTA de WhatsApp,
- comportamiento responsive,
- SEO básico,
- elementos TE SYSTEM aplicables.

El repositorio definitivo se crea únicamente después de que el propietario haya visto y aprobado esa vista previa.

## Prompt corto para un chat nuevo

`Crea una nueva landing Te Equipamos usando como fuente de verdad la carpeta landing-template del repositorio JorgeSport/te-equipamos. Lee primero README.md y template-config.json. Cuando te entregue el enlace del producto, precio, imágenes, referencia visual y demás datos, analiza las fuentes y genera directamente una primera versión funcional en HTML para que pueda abrirla y revisar el diseño. No te detengas antes a pedirme aprobación del concepto. Mantén intactos los bloques TE SYSTEM, incluido WhatsApp personalizado con producto, precio, variantes y enlace de la landing. No añadas dentro de la landing el bloque de compartir por WhatsApp, Facebook, Telegram y copiar enlace, porque lo aporta el Hub Te Equipamos en /read/.../, salvo que yo lo pida expresamente. No crees ni publiques todavía el repositorio definitivo. Primero entrégame el HTML de vista previa. Cuando yo lo apruebe, entonces prepara el repositorio independiente, te-equipamos.json, GitHub Pages e integración con el Hub.`

## Reglas de contenido

- Mercado principal: Perú.
- Español neutro.
- No inventar características, pruebas, valoraciones, garantías, disponibilidad ni precios.
- No publicar nombres de terceros que el propietario haya pedido excluir de los textos comerciales.
- El CTA comercial debe usar `data-te-whatsapp`; el núcleo central construye el enlace oficial automáticamente.
- Nunca sustituir el número oficial por otro número.
- Nunca dejar un mensaje genérico si existen datos del producto disponibles.
- Nunca inventar perfiles sociales.

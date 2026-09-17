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
- Bloque para compartir por WhatsApp, Facebook, Telegram y copiar enlace.
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

## Compartir en redes: comportamiento obligatorio

Toda landing nueva debe conservar los controles de compartir mediante:

- WhatsApp, para compartir el producto con otra persona.
- Facebook.
- Telegram.
- Copiar enlace.

Estos botones usan `data-te-share` y el núcleo central construye las URLs de compartir.

Importante: esto se refiere a **compartir la landing en redes**. No hay perfiles oficiales de Instagram, TikTok, Facebook u otras redes definidos en esta plantilla mientras no exista una URL oficial verificada y añadida expresamente a `template-config.json`. Nunca inventar perfiles sociales.

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

## Flujo para una nueva landing

1. Crear un repositorio nuevo con nombre `te-equipamos-<producto-slug>`.
2. Copiar el contenido de esta carpeta a la raíz del repositorio nuevo.
3. Sustituir los marcadores `REEMPLAZAR_*` del `index.html` y del `te-equipamos.json`.
4. Diseñar únicamente la zona `TE DESIGN ZONE` del `index.html`.
5. Mantener intactos los bloques marcados `TE SYSTEM` salvo que se actualice oficialmente el sistema.
6. Si hay variantes, conectar color/talla/cantidad con el mensaje personalizado de WhatsApp.
7. Revisar los cuatro controles de compartir.
8. Revisar móvil y escritorio.
9. Publicar con GitHub Pages.
10. Confirmar que la URL pública coincide con la del manifiesto.
11. El Hub podrá detectar el `te-equipamos.json` del repositorio público y clasificarlo.

## Prompt corto para un chat nuevo

`Crea una nueva landing Te Equipamos usando como fuente de verdad la carpeta landing-template del repositorio JorgeSport/te-equipamos. Lee primero README.md y template-config.json. Mantén intactos los bloques TE SYSTEM, incluido WhatsApp personalizado con producto, precio, variantes y enlace de la landing, y los controles para compartir por WhatsApp, Facebook, Telegram y copiar enlace. Diseña solo la TE DESIGN ZONE. Antes de tocar código, muéstrame la idea visual y espera mi aprobación.`

## Reglas de contenido

- Mercado principal: Perú.
- Español neutro.
- No inventar características, pruebas, valoraciones, garantías, disponibilidad ni precios.
- No publicar nombres de terceros que el propietario haya pedido excluir de los textos comerciales.
- El CTA comercial debe usar `data-te-whatsapp`; el núcleo central construye el enlace oficial automáticamente.
- Nunca sustituir el número oficial por otro número.
- Nunca dejar un mensaje genérico si existen datos del producto disponibles.
- Nunca inventar perfiles sociales.

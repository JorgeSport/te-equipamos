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
- Cabecera base de Te Equipamos.
- Footer universal.
- Analítica con consentimiento usando la configuración central de Te Equipamos.
- Responsive móvil.
- Manifiesto `te-equipamos.json` para que el Hub descubra y clasifique la landing.
- GitHub Pages mediante Actions.

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
6. Revisar móvil y escritorio.
7. Publicar con GitHub Pages.
8. Confirmar que la URL pública coincide con la del manifiesto.
9. El Hub podrá detectar el `te-equipamos.json` del repositorio público y clasificarlo.

## Prompt corto para un chat nuevo

`Crea una nueva landing Te Equipamos usando como fuente de verdad la carpeta landing-template del repositorio JorgeSport/te-equipamos. Mantén intactos los bloques TE SYSTEM y diseña solo la TE DESIGN ZONE. Antes de tocar código, muéstrame la idea visual y espera mi aprobación.`

## Reglas de contenido

- Mercado principal: Perú.
- Español neutro.
- No inventar características, pruebas, valoraciones, garantías, disponibilidad ni precios.
- No publicar nombres de terceros que el propietario haya pedido excluir de los textos comerciales.
- El CTA comercial debe usar `data-te-whatsapp`; el núcleo central construye el enlace oficial automáticamente.

# Mapa maestro de repositorios — Te Equipamos

Este archivo existe para que ningún producto, review o landing vuelva a quedar escondido dentro de una carpeta.

## Regla a partir de ahora

**1 proyecto público = 1 repositorio independiente = 1 landing = 1 manifiesto `te-equipamos.json`.**

El repositorio `te-equipamos-arpenaz-27l` se mantiene como repositorio principal porque contiene el Hub/News y la landing Arpenaz 27 L.

## Repositorios que ya existen de forma independiente

| Estado | Repositorio | Contenido |
|---|---|---|
| ✅ | `te-equipamos-arpenaz-27l` | Hub Te Equipamos + Arpenaz 100 27 L |
| ✅ | `te-equipamos-camiseta-mh100-mujer` | Camiseta MH100 mujer |
| ✅ | `quechua-nh500-ninos-remate` | Quechua NH500 niños |
| ✅ | `escape-journal` | Quechua Escape 500 Rolltop |
| ✅ | `move-500` | Move 500 25 L |
| ✅ | `te-equipamos-quechua-raincut-mujer` | Raincut mujer |
| ✅ | `te-equipamos-quechua-mh100-5l` | Mochila MH100 5 L |
| ✅ | `te-equipamos-arpenaz-500-review` | Review Arpenaz 500 |
| ✅ | `te-equipamos-forclaz-mt100-sombrero` | Sombrero Forclaz MT100 |
| ✅ | `te-equipamos-nh100-sandalias` | Sandalias NH100 |
| ✅ | `te-equipamos-player-t-mesh` | PLAYER T MESH |
| ✅ | `te-equipamos-forclaz-compact-10l` | Forclaz Compact 10 L |
| ✅ | `te-equipamos-arpenaz-100-20l-marron` | Arpenaz 100 20 L |
| ✅ | `te-equipamos-kalenji-editorial` | Editorial Kalenji |
| ✅ | `te-equipamos-nh100-mujer-naranja-remate` | NH100 mujer naranja · remate |

## Repositorios creados y pendientes de recibir su landing desde el repositorio principal

| Estado | Repositorio | Fuente actual |
|---|---|---|
| 🟡 Pendiente de migración | `te-equipamos-quechua-raincut-mujer` | `gh-pages/quechua-raincut-mujer/` |
| 🟡 Pendiente de migración | `te-equipamos-quechua-mh100-5l` | `gh-pages/quechua-mh100-5l-promocion/` |
| 🟡 Pendiente de migración | `te-equipamos-arpenaz-500-review` | `gh-pages/arpenaz-500-review/` |
| 🟡 Pendiente de migración | `te-equipamos-forclaz-mt100-sombrero` | `gh-pages/forclaz-mt100-sombrero/` |
| 🟡 Pendiente de migración | `te-equipamos-nh100-sandalias` | `gh-pages/nh100-sandalias/` |
| 🟡 Pendiente de migración | `te-equipamos-player-t-mesh` | `gh-pages/player-t-mesh/` |
| 🟡 Pendiente de migración | `te-equipamos-forclaz-compact-10l` | `gh-pages/forclaz-compact-10l/` |
| 🟡 Pendiente de migración | `te-equipamos-arpenaz-100-20l-marron` | `gh-pages/arpenaz-100-20l-marron/` |
| 🟡 Pendiente de migración | `te-equipamos-kalenji-editorial` | `gh-pages/kalenji/` |

## Eliminados intencionalmente — NO recrear

- `te-equipamos-plumon-quechua-mujer-xs`: eliminado por decisión del propietario. No debe volver a crearse automáticamente.
- `te-equipamos-studio`: eliminado por decisión del propietario. No debe volver a crearse automáticamente.

> Esta lista evita confundir un repositorio eliminado a propósito con uno que “falta”.

## Duplicados o carpetas que NO deben crear otro repositorio

- `gh-pages/escape-500-rolltop/`: copia antigua del producto que ya vive en `escape-journal`.
- `player-t-mesh/` en la raíz: copia heredada; la fuente desplegada es `gh-pages/player-t-mesh/`.
- `kalenji/` en la raíz: copia heredada; la fuente desplegada es `gh-pages/kalenji/`.
- `gh-pages/news/`: es el Hub, no un producto independiente.
- `gh-pages/read/`: se genera automáticamente durante el despliegue.

## Estado de la migración

Los repositorios de destino que continúan activos ya están creados. Las URLs públicas actuales del repositorio principal se mantienen hasta que cada nuevo repositorio tenga su landing y GitHub Pages esté publicado. Después se podrán actualizar los enlaces del Hub y conservar redirecciones desde las rutas antiguas.

Los datos técnicos de esta migración están en `migration/repositorios.json`.

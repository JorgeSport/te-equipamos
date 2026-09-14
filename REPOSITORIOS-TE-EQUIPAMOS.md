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

## Proyectos que están dentro del repositorio principal y deben quedar independientes

| Estado | Nuevo repositorio previsto | Ubicación actual | Página actual |
|---|---|---|---|
| 🟡 Preparado | `te-equipamos-quechua-raincut-mujer` | `gh-pages/quechua-raincut-mujer/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/quechua-raincut-mujer/ |
| 🟡 Preparado | `te-equipamos-quechua-mh100-5l` | `gh-pages/quechua-mh100-5l-promocion/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/quechua-mh100-5l-promocion/ |
| 🟡 Preparado | `te-equipamos-plumon-quechua-mujer-xs` | `gh-pages/plumon-quechua-mujer-xs/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/plumon-quechua-mujer-xs/ |
| 🟡 Preparado | `te-equipamos-arpenaz-500-review` | `gh-pages/arpenaz-500-review/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/arpenaz-500-review/ |
| 🟡 Preparado | `te-equipamos-forclaz-mt100-sombrero` | `gh-pages/forclaz-mt100-sombrero/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/forclaz-mt100-sombrero/ |
| 🟡 Preparado | `te-equipamos-nh100-sandalias` | `gh-pages/nh100-sandalias/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/nh100-sandalias/ |
| 🟡 Preparado | `te-equipamos-player-t-mesh` | `gh-pages/player-t-mesh/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/player-t-mesh/ |
| 🟡 Preparado | `te-equipamos-forclaz-compact-10l` | `gh-pages/forclaz-compact-10l/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/forclaz-compact-10l/ |
| 🟡 Preparado | `te-equipamos-arpenaz-100-20l-marron` | `gh-pages/arpenaz-100-20l-marron/` | https://jorgesport.github.io/te-equipamos-arpenaz-27l/arpenaz-100-20l-marron/ |
| 🟡 Preparado | `te-equipamos-kalenji-editorial` | `gh-pages/kalenji/` | Página editorial Kalenji |
| 🟡 Preparado | `te-equipamos-studio` | `gh-pages/studio/` | Te Equipamos Studio |

## Duplicados o carpetas que NO deben crear otro repositorio

- `gh-pages/escape-500-rolltop/`: copia antigua del producto que ya vive en `escape-journal`.
- `player-t-mesh/` en la raíz: copia heredada; la fuente desplegada es `gh-pages/player-t-mesh/`.
- `kalenji/` en la raíz: copia heredada; la fuente desplegada es `gh-pages/kalenji/`.
- `gh-pages/news/`: es el Hub, no un producto independiente.
- `gh-pages/read/`: se genera automáticamente durante el despliegue.

## Estado de la migración

La estructura y los nombres de destino ya están definidos. Las URLs públicas actuales se mantienen activas hasta que cada repositorio independiente exista y GitHub Pages esté publicado. Solo entonces se deben actualizar los enlaces del Hub y dejar redirecciones desde las rutas antiguas.

Los datos técnicos para completar esa segunda fase están en `migration/repositorios.json`.

# Migración a repositorios independientes

Este directorio contiene la preparación para separar las landings que todavía viven dentro del repositorio principal.

## Objetivo

Que cada proyecto público tenga su propio repositorio y pueda verse directamente en la lista de repositorios de GitHub.

## Orden correcto de migración

1. Crear el repositorio independiente con el nombre indicado en `repositorios.json`.
2. Copiar el `index.html` indicado por `source_path` a la raíz del nuevo repositorio.
3. Para los proyectos con `hub: true`, crear en la raíz del nuevo repositorio un `te-equipamos.json` con el elemento indicado en `item` y con `url` apuntando a `target_url`.
4. Activar GitHub Pages para publicar desde el repositorio independiente.
5. Verificar que la URL `target_url` funciona.
6. Solo después, actualizar el Hub para sustituir la URL antigua por la nueva.
7. Mantener una redirección desde la ruta antigua para no romper enlaces compartidos previamente.

## Regla de seguridad

Nunca se cambia una URL del Hub hacia un repositorio nuevo antes de verificar que GitHub Pages está publicado. Así evitamos tarjetas rotas, enlaces 404 o pérdida de tráfico.

## Qué NO se migra

Los elementos listados en `do_not_migrate` son duplicados, archivos técnicos o partes del Hub. No deben convertirse en repositorios adicionales.

## Estado actual

Los nombres, rutas de origen, URLs actuales y URLs de destino están definidos. La única acción que no puede ejecutarse desde la conexión GitHub disponible en este chat es la creación de repositorios nuevos en la cuenta. Una vez creados esos repositorios, el resto de la migración puede aplicarse de forma mecánica con este manifiesto.

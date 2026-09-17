# Publicador automático de Te Equipamos

Este paquete reduce la publicación de una landing nueva a un proceso casi de un clic.

## Qué hace

`PUBLICAR-TE-EQUIPAMOS.bat`:

1. acepta una carpeta o ZIP de landing;
2. comprueba que existan `index.html`, `te-equipamos.json` y `.github/workflows/pages.yml`;
3. valida `schema_version: 3`;
4. exige título estratégico del Hub en `card_title`;
5. exige subtítulo estratégico en `summary`;
6. valida SEO básico obligatorio;
7. genera automáticamente un ID estable si falta;
8. actualiza la URL pública al nombre real del repositorio;
9. completa `published_at` con la fecha actual si hace falta;
10. crea un repositorio público independiente en `JorgeSport`;
11. sube la landing a `main`;
12. activa GitHub Pages con GitHub Actions;
13. ejecuta y espera el despliegue de la landing;
14. ejecuta y espera la actualización del Hub principal de Te Equipamos;
15. abre la nueva landing al terminar.

## Primera vez en este PC

Ejecuta:

`INSTALAR-UNA-VEZ.bat`

El instalador comprueba e instala, si hacen falta:

- Git;
- GitHub CLI (`gh`).

Después abre el inicio de sesión de GitHub en el navegador. Autoriza la cuenta `JorgeSport`.

Este paso se hace una sola vez por equipo, salvo que cierres o revoques la sesión de GitHub CLI.

## Cada nueva landing

La landing debe haberse creado usando `landing-template/` y estar ya aprobada.

Opción rápida:

1. guarda la landing como carpeta o ZIP;
2. arrastra ese ZIP o carpeta encima de `PUBLICAR-TE-EQUIPAMOS.bat`;
3. si el nombre del repositorio ya está definido en `te-equipamos.json`, el publicador lo detecta;
4. si no está definido, te pedirá el nombre;
5. espera hasta ver `PUBLICACIÓN COMPLETADA`.

También puedes hacer doble clic en `PUBLICAR-TE-EQUIPAMOS.bat` y pegar la ruta cuando la pida.

## Protección contra errores

El publicador se detiene antes de crear el repositorio si detecta:

- esquema anterior a 3;
- campos `REEMPLAZAR_` sin completar;
- título estratégico ausente o fuera del rango del Hub;
- subtítulo estratégico ausente;
- SEO obligatorio incompleto;
- archivos esenciales ausentes;
- repositorio con ese nombre ya existente.

El script no sobrescribe automáticamente repositorios existentes.

## Flujo recomendado desde ChatGPT o Codex

Cuando la landing esté aprobada, pide que se entregue el proyecto final usando `JorgeSport/te-equipamos/landing-template/` como fuente de verdad y que `te-equipamos.json` incluya título y subtítulo estratégicos para el Hub.

Después usa este publicador. No necesitas crear manualmente el repositorio, activar Pages ni volver al Hub para lanzar la sincronización.

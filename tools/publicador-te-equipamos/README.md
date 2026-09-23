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
15. deja visibles las URLs de la landing, el Hub y el repositorio al terminar.

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

## Protección del propio publicador

El lanzador ya no sustituye el motor de PowerShell inmediatamente después de descargarlo.

Antes de activar una actualización:

1. descarga la nueva versión a un archivo temporal;
2. analiza su sintaxis con el parser oficial de PowerShell;
3. conserva una copia local válida en la carpeta `respaldo/`;
4. solo reemplaza el motor activo si la versión descargada es válida;
5. si la versión local queda dañada, restaura automáticamente `PUBLICAR-TE-EQUIPAMOS-ULTIMO-ESTABLE.ps1`;
6. si tampoco existe un respaldo local válido, recupera `PUBLICAR-TE-EQUIPAMOS-ESTABLE.ps1` desde GitHub;
7. si ninguna copia supera la validación, se detiene sin publicar ni modificar proyectos.

Además, GitHub Actions ejecuta `.github/workflows/validate-publisher.yml` en Windows cuando cambia el publicador. El workflow comprueba la sintaxis de la versión actual y de la versión estable.

La versión estable de GitHub se mantiene separada del archivo de desarrollo para que una modificación futura defectuosa no elimine el último punto de recuperación conocido.

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

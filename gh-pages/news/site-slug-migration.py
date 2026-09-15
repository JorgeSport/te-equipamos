from pathlib import Path
import json
import os

NEWS = Path(__file__).resolve().parent
ROOT = NEWS.parent
OWNER = 'JorgeSport'
OLD_SLUG = 'te-equipamos-arpenaz-27l'
TARGET_SLUG = 'te-equipamos'

repo_env = os.environ.get('GITHUB_REPOSITORY', f'{OWNER}/{OLD_SLUG}')
CURRENT_SLUG = repo_env.split('/')[-1].strip() or OLD_SLUG
OLD_BASE = f'https://jorgesport.github.io/{OLD_SLUG}/'
CURRENT_BASE = f'https://jorgesport.github.io/{CURRENT_SLUG}/'

# Solo se postprocesan archivos que realmente se publican. Los generadores .py
# permanecen intactos para que el cambio sea reversible y auditable.
extensions = {'.html', '.js', '.css', '.json', '.xml', '.txt', '.svg', '.webmanifest'}
changed_files = 0
replacements = 0

if CURRENT_SLUG != OLD_SLUG:
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        new = text
        # Primero URLs completas, después cualquier referencia restante al slug.
        new = new.replace(OLD_BASE, CURRENT_BASE)
        new = new.replace(f'https://github.com/{OWNER}/{OLD_SLUG}', f'https://github.com/{OWNER}/{CURRENT_SLUG}')
        new = new.replace(OLD_SLUG, CURRENT_SLUG)
        if new != text:
            replacements += text.count(OLD_SLUG)
            path.write_text(new, encoding='utf-8')
            changed_files += 1

# Estado público de la ubicación actual. Sirve para auditoría y futuras migraciones.
status = {
    'brand': 'Te Equipamos',
    'repository_slug': CURRENT_SLUG,
    'public_base_url': CURRENT_BASE,
    'target_slug': TARGET_SLUG,
    'migration_active': CURRENT_SLUG == TARGET_SLUG,
    'changed_files_this_build': changed_files,
    'replacements_this_build': replacements,
}
(NEWS / 'site-location.json').write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding='utf-8')

# En el nuevo repositorio no debe sobrevivir ninguna ruta pública con el slug antiguo.
if CURRENT_SLUG == TARGET_SLUG:
    leftovers = []
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in extensions:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            continue
        if OLD_SLUG in text:
            leftovers.append(str(path.relative_to(ROOT)))
    if leftovers:
        raise RuntimeError('Quedan referencias públicas al slug antiguo: ' + ', '.join(leftovers[:20]))
    hub = NEWS / 'index.html'
    if hub.exists() and CURRENT_BASE not in hub.read_text(encoding='utf-8'):
        raise RuntimeError('La portada no contiene la nueva base pública de Te Equipamos')
    print(f'MIGRACIÓN ACTIVA · {CURRENT_BASE} · {changed_files} archivos normalizados')
else:
    print(f'MIGRACIÓN PREPARADA · repositorio actual: {CURRENT_SLUG} · destino: {TARGET_SLUG} · sin cambiar URLs públicas todavía')

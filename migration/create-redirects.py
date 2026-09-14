"""Keep published legacy product URLs working after repository migration."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "migration/repositorios.json").read_text(encoding="utf-8"))
SITE = ROOT / "gh-pages"

for repo in CONFIG["repositories"]:
    old = repo["current_url"]
    prefix = "https://jorgesport.github.io/te-equipamos-arpenaz-27l/"
    if not old.startswith(prefix):
        raise ValueError(f"Unexpected source URL: {old}")
    slug = old[len(prefix):].strip("/")
    target = repo["target_url"]
    page = SITE / slug / "index.html"
    if not page.exists():
        raise FileNotFoundError(page)
    safe = html.escape(target, quote=True)
    page.write_text(
        '<!doctype html>\n<html lang="es"><head><meta charset="utf-8">\n'
        f'<meta http-equiv="refresh" content="0; url={safe}">\n'
        f'<link rel="canonical" href="{safe}">\n'
        f'<title>Redirigiendo a Te Equipamos</title></head><body>\n'
        f'<p>Esta página se ha trasladado. <a href="{safe}">Abrir la nueva dirección</a>.</p>\n'
        f'<script>location.replace({json.dumps(target)} + location.search + location.hash)</script>\n'
        '</body></html>\n',
        encoding="utf-8",
    )
    print(f"{slug}/ -> {target}")

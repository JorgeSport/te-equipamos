"""Keep legacy URLs working and hide deleted repositories from the portal."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "migration/repositorios.json").read_text(encoding="utf-8"))
SITE = ROOT / "gh-pages"
NEWS_URL = "https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/"

portal = SITE / "news/index.html"
portal_html = portal.read_text(encoding="utf-8")
startup = "const id=new URLSearchParams(location.search).get('id');id?renderArticle(id):renderPortal();"
if portal_html.count(startup) != 1:
    raise RuntimeError("Could not find the portal startup code")
live_check = """async function showCurrentContent(){
  try {
    const controller=new AbortController();
    const timeout=setTimeout(()=>controller.abort(),4000);
    let response;
    try {
      response=await fetch('https://api.github.com/users/JorgeSport/repos?per_page=100&type=owner',
        {cache:'no-store',signal:controller.signal});
    } finally { clearTimeout(timeout); }
    if(response.ok){
      const repos=await response.json();
      const available=new Set(repos.map(repo=>repo.full_name.toLowerCase()));
      for(let i=NEWS.length-1;i>=0;i--){
        const item=NEWS[i];
        if(item.owned&&item.source_repo&&!available.has(item.source_repo.toLowerCase())) NEWS.splice(i,1);
      }
    }
  } catch(error) { console.warn('No se pudo comprobar GitHub; se muestra la última publicación.',error); }
  const id=new URLSearchParams(location.search).get('id');
  id?renderArticle(id):renderPortal();
}
showCurrentContent();"""
portal.write_text(portal_html.replace(startup, live_check), encoding="utf-8")

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
    check = (
        f"fetch('https://api.github.com/repos/JorgeSport/{repo['name']}',{{cache:'no-store'}})"
        f".then(r=>location.replace(r.status===404?{json.dumps(NEWS_URL)}:"
        f"{json.dumps(target)}+location.search+location.hash))"
        f".catch(()=>location.replace({json.dumps(target)}+location.search+location.hash));"
    )
    page.write_text(
        '<!doctype html>\n<html lang="es"><head><meta charset="utf-8">\n'
        f'<link rel="canonical" href="{safe}">\n'
        f'<title>Redirigiendo a Te Equipamos</title></head><body>\n'
        f'<p>Comprobando la dirección… <a href="{safe}">Abrir la página del producto</a>.</p>\n'
        f'<script>{check}</script>\n'
        '</body></html>\n',
        encoding="utf-8",
    )
    print(f"{slug}/ -> {target}")

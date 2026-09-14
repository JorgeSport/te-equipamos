from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
from html import unescape
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
DATA_FILE = BASE / "news-data.json"
OWNER = "JorgeSport"
MANIFEST = "te-equipamos.json"

HEADERS = {
    "User-Agent": "TeEquipamosHub/2.0 (+https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/)"
}

TYPE_TO_SECTION = {
    "sale": "Ventas",
    "venta": "Ventas",
    "ventas": "Ventas",
    "review": "Reviews",
    "reviews": "Reviews",
    "video": "Vídeos",
    "videos": "Vídeos",
    "vídeo": "Vídeos",
    "vídeos": "Vídeos",
    "tip": "Consejos",
    "tips": "Consejos",
    "consejo": "Consejos",
    "consejos": "Consejos",
    "offer": "Ofertas",
    "oferta": "Ofertas",
    "ofertas": "Ofertas",
    "news": "Novedades",
    "novedad": "Novedades",
    "novedades": "Novedades",
}
VALID_SECTIONS = ["Ventas", "Reviews", "Vídeos", "Consejos", "Ofertas", "Novedades"]
FALLBACK_IMAGES = {
    "Ventas": "https://images.unsplash.com/photo-1551632811-561732d1e306?auto=format&fit=crop&w=1200&q=82",
    "Reviews": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?auto=format&fit=crop&w=1200&q=82",
    "Vídeos": "https://images.unsplash.com/photo-1526481280695-3c687fd643ed?auto=format&fit=crop&w=1200&q=82",
    "Consejos": "https://images.unsplash.com/photo-1464822759844-d150baec0494?auto=format&fit=crop&w=1200&q=82",
    "Ofertas": "https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&w=1200&q=82",
    "Novedades": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=82",
}


def get_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def stable_id(value: str) -> int:
    return int(hashlib.sha1(value.encode("utf-8")).hexdigest()[:8], 16)


def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def normalize_section(value: str) -> str | None:
    text = clean(value)
    if text in VALID_SECTIONS:
        return text
    key = text.lower()
    return TYPE_TO_SECTION.get(key)


def discover_og_image(url: str) -> str:
    if not url.startswith("http"):
        return ""
    try:
        html = get_text(url)[:250000]
    except Exception:
        return ""
    patterns = [
        r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html, flags=re.I)
        if match:
            return unescape(match.group(1)).strip()
    return ""


def list_public_repositories() -> list[dict]:
    repos = []
    for page in range(1, 6):
        url = f"https://api.github.com/users/{OWNER}/repos?per_page=100&page={page}&type=owner&sort=updated"
        batch = get_json(url)
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
    return [r for r in repos if not r.get("archived") and not r.get("fork")]


def load_manifest(repo: dict):
    name = repo.get("name", "")
    branch = repo.get("default_branch") or "main"
    if not name:
        return None
    raw = f"https://raw.githubusercontent.com/{OWNER}/{urllib.parse.quote(name)}/{urllib.parse.quote(branch)}/{MANIFEST}"
    try:
        return get_json(raw)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def manifest_items(manifest) -> list[dict]:
    if isinstance(manifest, list):
        return [x for x in manifest if isinstance(x, dict)]
    if isinstance(manifest, dict):
        items = manifest.get("items")
        if isinstance(items, list):
            return [x for x in items if isinstance(x, dict)]
        if manifest.get("title"):
            return [manifest]
    return []


def normalize_item(raw: dict, repo_name: str) -> dict | None:
    if not raw.get("active", True):
        return None
    title = clean(raw.get("title"))
    url = clean(raw.get("url"))
    if not title or not url.startswith("http"):
        return None

    primary = normalize_section(raw.get("type", "")) or normalize_section(raw.get("category", "")) or "Novedades"
    sections = []
    for value in raw.get("sections", []) if isinstance(raw.get("sections"), list) else []:
        section = normalize_section(value)
        if section and section not in sections:
            sections.append(section)
    if primary not in sections:
        sections.insert(0, primary)

    image = clean(raw.get("image"))
    if not image:
        image = discover_og_image(url)
    if not image:
        image = FALLBACK_IMAGES[primary]

    kind_label = {
        "Ventas": "Venta",
        "Reviews": "Review",
        "Vídeos": "Vídeo",
        "Consejos": "Consejo",
        "Ofertas": "Oferta",
        "Novedades": "Novedad",
    }[primary]

    tags = raw.get("tags") if isinstance(raw.get("tags"), list) else []
    return {
        "id": int(raw.get("id")) if str(raw.get("id", "")).isdigit() else stable_id(url + "|" + title),
        "title": title,
        "summary": clean(raw.get("summary")) or f"Contenido propio de Te Equipamos · {kind_label}.",
        "details": clean(raw.get("details")) or clean(raw.get("summary")) or "Contenido propio publicado por Te Equipamos.",
        "category": primary,
        "sections": sections,
        "source": clean(raw.get("source")) or f"Te Equipamos · {kind_label}",
        "time": clean(raw.get("time")) or kind_label,
        "url": url,
        "image": image,
        "featured": bool(raw.get("featured", False)),
        "score": int(raw.get("score", 80)),
        "owned": True,
        "direct": bool(raw.get("direct", True)),
        "kind": clean(raw.get("type")) or primary,
        "tags": [clean(x) for x in tags if clean(x)],
        "source_repo": f"{OWNER}/{repo_name}",
        "published": clean(raw.get("published")),
    }


def deduplicate(items: list[dict]) -> list[dict]:
    by_url: dict[str, dict] = {}
    for item in items:
        key = item["url"].rstrip("/").lower()
        if key not in by_url:
            by_url[key] = item
            continue
        current = by_url[key]
        merged_sections = current.get("sections", []) + item.get("sections", [])
        current["sections"] = list(dict.fromkeys(merged_sections))
        if item.get("score", 0) > current.get("score", 0):
            keep_sections = current["sections"]
            by_url[key] = item
            by_url[key]["sections"] = keep_sections
    return list(by_url.values())


def sort_key(item: dict):
    published = item.get("published", "")
    try:
        date_score = datetime.fromisoformat(published.replace("Z", "+00:00")).timestamp() if published else 0
    except Exception:
        date_score = 0
    return (1 if item.get("featured") else 0, date_score, item.get("score", 0))


def main() -> None:
    errors = []
    collected = []
    try:
        repos = list_public_repositories()
    except Exception as exc:
        repos = []
        errors.append(f"No se pudo listar GitHub: {exc}")

    # Garantiza que el manifiesto del propio portal se pueda usar incluso si GitHub API falla.
    local_manifest = ROOT / MANIFEST
    if local_manifest.exists():
        try:
            manifest = json.loads(local_manifest.read_text(encoding="utf-8"))
            for raw in manifest_items(manifest):
                item = normalize_item(raw, "te-equipamos-arpenaz-27l")
                if item:
                    collected.append(item)
        except Exception as exc:
            errors.append(f"Manifiesto local: {exc}")

    for repo in repos:
        name = repo.get("name", "")
        if name == "te-equipamos-arpenaz-27l":
            continue
        manifest = load_manifest(repo)
        if not manifest:
            continue
        for raw in manifest_items(manifest):
            try:
                item = normalize_item(raw, name)
                if item:
                    collected.append(item)
            except Exception as exc:
                errors.append(f"{name}: {exc}")

    items = deduplicate(collected)
    items.sort(key=sort_key, reverse=True)

    # La portada necesita hasta cuatro destacados. Respeta los elegidos y completa si faltan.
    featured_count = sum(1 for x in items if x.get("featured"))
    if featured_count < 4:
        for item in items:
            if not item.get("featured"):
                item["featured"] = True
                featured_count += 1
                if featured_count >= 4:
                    break

    if not items:
        raise RuntimeError("No se encontró ningún contenido Te Equipamos con te-equipamos.json")

    DATA_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    counts = {section: 0 for section in VALID_SECTIONS}
    for item in items:
        for section in item.get("sections", [item.get("category")]):
            if section in counts:
                counts[section] += 1

    print(f"Te Equipamos Hub: {len(items)} contenidos propios detectados desde GitHub.")
    print("Menús:", ", ".join(f"{k}={v}" for k, v in counts.items()))
    repos_used = sorted({x.get("source_repo", "") for x in items})
    print("Repositorios usados:", ", ".join(repos_used))
    if errors:
        print("Avisos no bloqueantes:")
        for error in errors:
            print(" -", error)


if __name__ == "__main__":
    main()

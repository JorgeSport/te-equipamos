from __future__ import annotations

from pathlib import Path
from datetime import datetime
from html import unescape
import hashlib
import json
import re
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
DATA_FILE = BASE / "news-data.json"
OWNER = "JorgeSport"
MANIFEST = "te-equipamos.json"

HEADERS = {
    "User-Agent": "TeEquipamosHub/4.0 (+https://jorgesport.github.io/te-equipamos/)"
}

TYPE_TO_SECTION = {
    "sale": "Ventas", "venta": "Ventas", "ventas": "Ventas",
    "review": "Reviews", "reviews": "Reviews",
    "video": "Vídeos", "videos": "Vídeos", "vídeo": "Vídeos", "vídeos": "Vídeos",
    "tip": "Consejos", "tips": "Consejos", "consejo": "Consejos", "consejos": "Consejos",
    "offer": "Ofertas", "oferta": "Ofertas", "ofertas": "Ofertas",
    "news": "Novedades", "novedad": "Novedades", "novedades": "Novedades",
}
VALID_SECTIONS = ["Ventas", "Reviews", "Vídeos", "Consejos", "Ofertas", "Novedades"]

# IDs internos estables. Los textos visibles se resuelven en la interfaz.
ACTIVITY_ALIASES = {
    "senderismo": "senderismo", "hiking": "senderismo",
    "trekking": "trekking",
    "running": "running", "correr": "running",
    "trail running": "trail-running", "trail-running": "trail-running", "trail": "trail-running",
    "ciclismo": "ciclismo", "bicicleta": "ciclismo", "bike": "ciclismo", "mtb": "ciclismo",
    "natacion": "natacion", "natación": "natacion", "swimming": "natacion",
    "travel": "travel", "viaje": "travel", "viajes": "travel", "backpacking": "travel",
    "alpinismo": "alpinismo",
    "escalada": "escalada", "climbing": "escalada",
    "camping": "camping",
    "esqui": "esqui", "esquí": "esqui", "nieve": "esqui", "snowboard": "esqui",
    "kayak": "kayak", "remo": "kayak",
    "surf": "surf",
    "fitness": "fitness", "gimnasio": "fitness", "entrenamiento": "fitness",
}

FALLBACK_IMAGES = {
    "Ventas": "https://images.unsplash.com/photo-1551632811-561732d1e306?auto=format&fit=crop&w=1200&q=82",
    "Reviews": "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?auto=format&fit=crop&w=1200&q=82",
    "Vídeos": "https://images.unsplash.com/photo-1526481280695-3c687fd643ed?auto=format&fit=crop&w=1200&q=82",
    "Consejos": "https://images.unsplash.com/photo-1464822759844-d150baec0494?auto=format&fit=crop&w=1200&q=82",
    "Ofertas": "https://images.unsplash.com/photo-1501555088652-021faa106b9b?auto=format&fit=crop&w=1200&q=82",
    "Novedades": "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=82",
}

PRODUCT_TYPES = [
    ("mochila", ["mochila", "backpack"]),
    ("bolso", ["bolso", "duffel"]),
    ("sandalias", ["sandalia"]),
    ("zapatillas", ["zapatilla", "calzado"]),
    ("camiseta", ["camiseta"]),
    ("chaqueta", ["chaqueta", "raincut", "plumón", "plumon"]),
    ("sombrero", ["sombrero", "gorra"]),
    ("pantalon", ["pantalón", "pantalon"]),
    ("short", ["short"]),
]


def get_json(url: str):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8-sig"))


def get_text(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as response:
        return response.read().decode("utf-8", errors="replace")


def stable_id(value: str) -> int:
    return int(hashlib.sha1(value.encode("utf-8")).hexdigest()[:8], 16)


def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def plain(value) -> str:
    text = unicodedata.normalize("NFKD", clean(value).lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def slug(value) -> str:
    return re.sub(r"[^a-z0-9]+", "-", plain(value)).strip("-")


def normalize_section(value: str) -> str | None:
    text = clean(value)
    if text in VALID_SECTIONS:
        return text
    return TYPE_TO_SECTION.get(text.lower())


def normalize_activity(value: str) -> str:
    text = clean(value).lower()
    if not text:
        return ""
    return ACTIVITY_ALIASES.get(text) or ACTIVITY_ALIASES.get(plain(text)) or slug(text)


def infer_activities(raw: dict) -> list[str]:
    values = []
    tags = raw.get("tags") if isinstance(raw.get("tags"), list) else []
    haystack = plain(" ".join([clean(raw.get("title")), clean(raw.get("summary")), " ".join(map(str, tags))]))
    patterns = [
        ("trail-running", ["trail running", "trail-running"]),
        ("senderismo", ["senderismo", "hiking", "sendero"]),
        ("trekking", ["trekking"]),
        ("running", ["running", "correr"]),
        ("ciclismo", ["ciclismo", "bicicleta", " mtb "]),
        ("natacion", ["natacion", "swimming"]),
        ("travel", ["travel", "viaje", "backpacking"]),
        ("alpinismo", ["alpinismo"]),
        ("escalada", ["escalada", "climbing"]),
        ("camping", ["camping"]),
        ("esqui", ["esqui", "nieve", "snowboard"]),
        ("kayak", ["kayak", "remo"]),
        ("surf", ["surf"]),
        ("fitness", ["fitness", "gimnasio", "entrenamiento"]),
    ]
    for activity, words in patterns:
        if any(word in haystack for word in words) and activity not in values:
            values.append(activity)
    return values


def infer_product_type(raw: dict) -> str:
    tags = raw.get("tags") if isinstance(raw.get("tags"), list) else []
    haystack = plain(" ".join([clean(raw.get("title")), clean(raw.get("summary")), " ".join(map(str, tags))]))
    for product_type, words in PRODUCT_TYPES:
        if any(plain(word) in haystack for word in words):
            return product_type
    return "equipamiento"


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
            schema_version = int(manifest.get("schema_version") or 1)
            return [{**x, "_schema_version": schema_version} for x in items if isinstance(x, dict)]
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
        "Ventas": "Venta", "Reviews": "Review", "Vídeos": "Vídeo",
        "Consejos": "Consejo", "Ofertas": "Oferta", "Novedades": "Novedad",
    }[primary]

    tags = raw.get("tags") if isinstance(raw.get("tags"), list) else []
    declared_activities = raw.get("activities") if isinstance(raw.get("activities"), list) else []
    activities = []
    for value in declared_activities:
        activity = normalize_activity(value)
        if activity and activity not in activities:
            activities.append(activity)
    inferred = False
    if not activities:
        activities = infer_activities(raw)
        inferred = bool(activities)

    product_type = slug(raw.get("product_type")) if clean(raw.get("product_type")) else infer_product_type(raw)

    card_title = clean(raw.get("card_title")) or title
    seo_title = clean(raw.get("seo_title")) or title
    seo_description = clean(raw.get("seo_description")) or clean(raw.get("summary"))
    seo_keywords = raw.get("seo_keywords") if isinstance(raw.get("seo_keywords"), list) else []
    schema_version = int(raw.get("_schema_version") or 1)

    return {
        "id": int(raw.get("id")) if str(raw.get("id", "")).isdigit() else stable_id(url + "|" + title),
        "title": title,
        "card_title": card_title,
        "seo_title": seo_title,
        "seo_description": seo_description,
        "seo_keywords": [clean(value) for value in seo_keywords if clean(value)],
        "schema_version": schema_version,
        "seo_ready": bool(
            clean(raw.get("card_title"))
            and clean(raw.get("seo_title"))
            and clean(raw.get("seo_description"))
            and seo_keywords
        ),
        "summary": clean(raw.get("summary")) or f"Contenido propio de Te Equipamos · {kind_label}.",
        "details": clean(raw.get("details")) or clean(raw.get("summary")) or "Contenido propio publicado por Te Equipamos.",
        "category": primary,
        "content_label": clean(raw.get("content_label")),
        "sections": sections,
        "activities": activities,
        "activities_inferred": inferred,
        "product_type": product_type,
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
        "published_at": clean(raw.get("published_at")) or clean(raw.get("published")),
        "published": clean(raw.get("published_at")) or clean(raw.get("published")),
    }



def discover_local_published_pages() -> list[dict]:
    """Descubre landings ya publicadas dentro de gh-pages como respaldo local.

    Esto evita que el Hub quede vacío si GitHub limita temporalmente la API o
    si un repositorio externo todavía no expone su manifiesto.
    """
    published_root = BASE.parent
    ignored = {"news", "read", "studio", "kalenji", "arpenaz-100-27l"}
    items = []
    for page in sorted(published_root.glob("*/index.html")):
        folder = page.parent.name
        if folder in ignored:
            continue
        try:
            html = page.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        title_match = re.search(r"<title>(.*?)</title>", html, flags=re.I | re.S)
        title = clean(re.sub(r"<[^>]+>", " ", title_match.group(1))) if title_match else folder.replace("-", " ").title()
        title = re.sub(r"\s*[|·—-]\s*Te Equipamos.*$", "", title, flags=re.I).strip() or title

        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', html, flags=re.I)
        if not desc_match:
            desc_match = re.search(r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']', html, flags=re.I)
        summary = unescape(desc_match.group(1)).strip() if desc_match else f"Contenido propio de Te Equipamos sobre {title}."

        image = ""
        for pattern in [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
        ]:
            match = re.search(pattern, html, flags=re.I)
            if match:
                image = unescape(match.group(1)).strip()
                break

        inferred_type = "review" if "review" in plain(title + " " + folder) else "sale"
        raw = {
            "title": title,
            "summary": summary,
            "details": summary,
            "url": f"https://jorgesport.github.io/te-equipamos/{folder}/",
            "image": image,
            "type": inferred_type,
            "activities": infer_activities({"title": title, "summary": summary, "tags": []}),
            "product_type": infer_product_type({"title": title, "summary": summary, "tags": []}),
            "source": "Te Equipamos",
            "direct": True,
            "active": True,
            "score": 82,
        }
        if not raw["activities"]:
            raw["activities"] = ["senderismo"]
        item = normalize_item(raw, "te-equipamos")
        if item:
            items.append(item)
    return items


def deduplicate(items: list[dict]) -> list[dict]:
    by_url: dict[str, dict] = {}
    for item in items:
        key = item["url"].rstrip("/").lower()
        if key not in by_url:
            by_url[key] = item
            continue
        current = by_url[key]
        current["sections"] = list(dict.fromkeys(current.get("sections", []) + item.get("sections", [])))
        current["activities"] = list(dict.fromkeys(current.get("activities", []) + item.get("activities", [])))
        current["tags"] = list(dict.fromkeys(current.get("tags", []) + item.get("tags", [])))
        if item.get("score", 0) > current.get("score", 0):
            keep_sections = current["sections"]
            keep_activities = current["activities"]
            keep_tags = current["tags"]
            by_url[key] = item
            by_url[key]["sections"] = keep_sections
            by_url[key]["activities"] = keep_activities
            by_url[key]["tags"] = keep_tags
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

    local_manifest = ROOT / MANIFEST
    if local_manifest.exists():
        try:
            manifest = json.loads(local_manifest.read_text(encoding="utf-8-sig"))
            for raw in manifest_items(manifest):
                item = normalize_item(raw, "te-equipamos")
                if item:
                    collected.append(item)
        except Exception as exc:
            errors.append(f"Manifiesto local: {exc}")

    # Respaldo local: las landings ya presentes en gh-pages siempre alimentan el Hub.
    collected.extend(discover_local_published_pages())

    for repo in repos:
        name = repo.get("name", "")
        if name == "te-equipamos":
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
    activity_counts: dict[str, int] = {}
    for item in items:
        for section in item.get("sections", [item.get("category")]):
            if section in counts:
                counts[section] += 1
        for activity in item.get("activities", []):
            activity_counts[activity] = activity_counts.get(activity, 0) + 1

    print(f"Te Equipamos Hub: {len(items)} contenidos propios detectados desde GitHub.")
    print("Menús:", ", ".join(f"{k}={v}" for k, v in counts.items()))
    print("Actividades:", ", ".join(f"{k}={v}" for k, v in sorted(activity_counts.items())))
    repos_used = sorted({x.get("source_repo", "") for x in items})
    print("Repositorios usados:", ", ".join(repos_used))
    inferred = [x for x in items if x.get("activities_inferred")]
    if inferred:
        print(f"Aviso: {len(inferred)} contenidos usan actividades inferidas; conviene declararlas en su te-equipamos.json.")
    if errors:
        print("Avisos no bloqueantes:")
        for error in errors:
            print(" -", error)


if __name__ == "__main__":
    main()

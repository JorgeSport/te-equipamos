from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
DATA = BASE / "news-data.json"
MAX_TITLE = 155

PREFIXES = {
    "Outdoor": [
        "Lo que conviene saber: ",
        "En el radar outdoor: ",
        "Para seguir de cerca: ",
    ],
    "Deportes": [
        "La jornada deja esto: ",
        "Para seguir de cerca: ",
        "Lo que está marcando el día: ",
    ],
    "Novedades": [
        "Lo nuevo que merece atención: ",
        "Una novedad para mirar de cerca: ",
        "Esto entra en el radar: ",
    ],
    "Tecnología": [
        "Tecnología outdoor: esto es lo nuevo: ",
        "Lo que conviene mirar de cerca: ",
        "En el radar tecnológico: ",
    ],
    "España": [
        "En el radar outdoor de España: ",
        "Lo que está pasando en España: ",
        "Para seguir de cerca en España: ",
    ],
    "Internacional": [
        "En el radar outdoor internacional: ",
        "Para seguir de cerca: ",
        "Lo que conviene saber fuera de España: ",
    ],
}

EDITORIAL_MARKERS = (
    "por qué ", "qué ", "cómo ", "claves ", "lo que ", "todo lo que ",
    "la historia ", "estas son ", "esto es ", "así ", "¿", "¡"
)


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def trim(value: str, limit: int) -> str:
    value = norm(value)
    if len(value) <= limit:
        return value
    cut = value[: max(1, limit - 1)].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:") + "…"


def already_editorial(title: str) -> bool:
    low = title.lower().lstrip()
    return "?" in title or any(low.startswith(marker) for marker in EDITORIAL_MARKERS)


def strategic_title(title: str, category: str) -> str:
    base = norm(title)
    if not base or already_editorial(base):
        return trim(base, MAX_TITLE)

    choices = PREFIXES.get(category, ["Para seguir de cerca: ", "Lo que conviene saber: "])
    key = hashlib.sha1(base.encode("utf-8")).digest()[0]
    prefix = choices[key % len(choices)]
    room = MAX_TITLE - len(prefix)
    return prefix + trim(base, room)


def main() -> None:
    items = json.loads(DATA.read_text(encoding="utf-8"))
    changed = 0

    for item in items:
        # Los productos ya tienen titulares comerciales trabajados a mano.
        if item.get("kind") == "product" or item.get("direct"):
            continue

        base = item.get("original_title") or item.get("title", "")
        if not base:
            continue

        item["original_title"] = base
        new_title = strategic_title(base, item.get("category", "Outdoor"))
        if new_title != item.get("title"):
            item["title"] = new_title
            changed += 1

    DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Titulares estratégicos aplicados a {changed} contenidos informativos.")


if __name__ == "__main__":
    main()

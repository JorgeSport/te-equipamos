from __future__ import annotations

from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
import html
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = Path(__file__).resolve().parent / "news-data.json"
OUTPUT = ROOT / "newsletter-feed.xml"

SITE_URL = "https://jorgesport.github.io/te-equipamos/"
FEED_URL = SITE_URL + "newsletter-feed.xml"
TITLE = "Te Equipamos - Novedades"
DESCRIPTION = "Nuevos productos, ofertas, reviews, comparativas y contenidos de Te Equipamos."

ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
ET.register_namespace("content", "http://purl.org/rss/1.0/modules/content/")
ET.register_namespace("media", "http://search.yahoo.com/mrss/")
ET.register_namespace("te", "https://jorgesport.github.io/te-equipamos/ns/newsletter")

ATOM = "{http://www.w3.org/2005/Atom}"
CONTENT = "{http://purl.org/rss/1.0/modules/content/}"
MEDIA = "{http://search.yahoo.com/mrss/}"
TE = "{https://jorgesport.github.io/te-equipamos/ns/newsletter}"


def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def parse_date(value: str) -> datetime | None:
    value = clean(value)
    if not value:
        return None
    try:
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def section_of(item: dict) -> str:
    sections = item.get("sections")
    if isinstance(sections, list) and sections:
        return clean(sections[0])
    return clean(item.get("category")) or "Novedades"


def item_kind(item: dict) -> str:
    raw = clean(item.get("kind") or item.get("type")).lower()
    section = section_of(item).lower()
    if raw in {"sale", "venta", "ventas"} or section == "ventas":
        return "producto"
    if raw in {"offer", "oferta", "ofertas"} or section == "ofertas":
        return "oferta"
    if raw in {"review", "reviews"} or section == "reviews":
        return "review"
    if raw in {"tip", "consejo", "consejos"} or section == "consejos":
        return "consejo"
    if raw in {"video", "videos", "vídeo", "vídeos"} or section in {"videos", "vídeos"}:
        return "video"
    return "novedad"


def main() -> None:
    items = json.loads(DATA_FILE.read_text(encoding="utf-8-sig"))
    if not isinstance(items, list):
        raise RuntimeError("news-data.json no contiene una lista")

    prepared = []
    skipped_without_date = 0

    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("owned") is False:
            continue

        url = clean(item.get("url"))
        title = clean(item.get("card_title") or item.get("title"))
        summary = clean(item.get("summary"))
        published_raw = clean(item.get("published_at") or item.get("published"))
        published = parse_date(published_raw)

        if not url.startswith("http") or not title:
            continue
        if not published:
            skipped_without_date += 1
            continue

        prepared.append((published, item, title, summary, url))

    prepared.sort(key=lambda row: row[0], reverse=True)
    prepared = prepared[:30]

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = TITLE
    ET.SubElement(channel, "link").text = SITE_URL
    ET.SubElement(channel, "description").text = DESCRIPTION
    ET.SubElement(channel, "language").text = "es"
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.now(timezone.utc))
    ET.SubElement(
        channel,
        ATOM + "link",
        {"href": FEED_URL, "rel": "self", "type": "application/rss+xml"},
    )

    for published, item, title, summary, url in prepared:
        node = ET.SubElement(channel, "item")
        ET.SubElement(node, "title").text = title
        ET.SubElement(node, "link").text = url
        ET.SubElement(node, "guid", {"isPermaLink": "true"}).text = url
        ET.SubElement(node, "pubDate").text = format_datetime(published)

        section = section_of(item)
        kind = item_kind(item)
        product_type = clean(item.get("product_type")) or "equipamiento"
        activities = item.get("activities") if isinstance(item.get("activities"), list) else []

        ET.SubElement(node, "category").text = section
        ET.SubElement(node, TE + "kind").text = kind
        ET.SubElement(node, TE + "section").text = section
        ET.SubElement(node, TE + "product_type").text = product_type
        ET.SubElement(node, TE + "activities").text = ", ".join(clean(x) for x in activities if clean(x))

        ET.SubElement(node, "description").text = summary

        image = clean(item.get("image"))
        if image:
            ET.SubElement(node, "enclosure", {"url": image, "length": "0", "type": "image/jpeg"})
            ET.SubElement(node, MEDIA + "content", {"url": image, "medium": "image"})
            ET.SubElement(node, TE + "image").text = image

        rich = (
            f'<p><strong>{html.escape(title)}</strong></p>'
            f'<p>{html.escape(summary)}</p>'
            f'<p><a href="{html.escape(url, quote=True)}">Ver en Te Equipamos</a></p>'
        )
        ET.SubElement(node, CONTENT + "encoded").text = rich

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)

    print(f"Newsletter RSS: {len(prepared)} contenidos con fecha publicados.")
    if skipped_without_date:
        print(f"Newsletter RSS: {skipped_without_date} contenidos antiguos sin published_at se omiten para no reenviarlos como nuevos.")
    print(f"Feed generado: {OUTPUT}")


if __name__ == "__main__":
    main()

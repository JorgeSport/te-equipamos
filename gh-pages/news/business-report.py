from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import json

NEWS = Path(__file__).resolve().parent
ROOT = NEWS.parent
items = json.loads((NEWS / 'news-data.json').read_text(encoding='utf-8'))
analytics = json.loads((NEWS / 'analytics-config.json').read_text(encoding='utf-8'))
sponsors = json.loads((NEWS / 'sponsored-campaigns.json').read_text(encoding='utf-8'))

sections = Counter()
activities = Counter()
owned = 0
for item in items:
    if item.get('owned'):
        owned += 1
    for section in item.get('sections') or []:
        sections[str(section)] += 1
    for activity in item.get('activities') or []:
        activities[str(activity)] += 1

# El portal usa internamente la sección "Ventas" y la muestra al público como "Productos".
# Se cuenta esa clasificación real, con kind=product como respaldo para futuras fichas.
product_ids = {
    item.get('id') for item in items
    if item.get('kind') == 'product' or 'Ventas' in (item.get('sections') or [])
}
products = len(product_ids)

active_sponsors = sum(1 for x in sponsors if isinstance(x, dict) and x.get('active') is True)
report = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'content': {
        'total': len(items),
        'owned': owned,
        'products': products,
        'sections': dict(sorted(sections.items())),
        'activities': dict(sorted(activities.items())),
    },
    'commercial': {
        'active_sponsored_campaigns': active_sponsors,
        'media_kit': (NEWS / 'media-kit/index.html').exists(),
        'advertising_page': (NEWS / 'anunciate/index.html').exists(),
        'sponsor_system_ready': (ROOT / 'sponsored-content.js').exists(),
    },
    'measurement': {
        'provider': analytics.get('provider', 'none'),
        'enabled': bool(analytics.get('enabled')),
        'requires_consent': bool(analytics.get('requires_consent', True)),
        'event_layer_ready': (ROOT / 'te-business-analytics.js').exists(),
        'provider_loader_ready': (ROOT / 'te-analytics-provider.js').exists(),
    },
    'seo': {
        'sitemap_ready': (ROOT / 'sitemap.xml').exists(),
        'robots_ready': (ROOT / 'robots.txt').exists(),
    },
    'legal': {
        'privacy_page_ready': (NEWS / 'privacidad/index.html').exists(),
        'cookies_page_ready': (NEWS / 'cookies/index.html').exists(),
        'legal_identity_complete': False,
        'note': 'Faltan datos jurídicos reales del titular antes de considerar cerrada la documentación legal.'
    },
    'content_gaps': {
        'sections_without_content': [s for s in ['Consejos','Vídeos'] if sections.get(s, 0) == 0],
        'activities_with_0_or_1': [a for a in ['senderismo','trekking','running','ciclismo','natacion','travel','fitness'] if activities.get(a, 0) <= 1],
    },
}
(NEWS / 'business-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print('RADIOGRAFÍA BUSINESS READY · ' + json.dumps(report, ensure_ascii=False, separators=(',', ':')))

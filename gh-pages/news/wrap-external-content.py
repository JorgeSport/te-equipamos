from pathlib import Path
from urllib.parse import urlparse
import html
import json

base = Path(__file__).resolve().parent
root = base.parent
data_path = base / 'news-data.json'
items = json.loads(data_path.read_text(encoding='utf-8'))

central_prefix = '/te-equipamos-arpenaz-27l/'
home_url = 'https://jorgesport.github.io/te-equipamos-arpenaz-27l/news/'
wrapped = 0

for item in items:
    url = str(item.get('url') or '')
    parsed = urlparse(url)
    if not url.startswith('http'):
        continue
    if parsed.netloc == 'jorgesport.github.io' and parsed.path.startswith(central_prefix):
        continue

    item_id = str(item.get('id'))
    if not item_id:
        continue

    original = url
    wrapper_dir = root / 'read' / item_id
    wrapper_dir.mkdir(parents=True, exist_ok=True)
    wrapper_url = f'https://jorgesport.github.io/te-equipamos-arpenaz-27l/read/{item_id}/'

    title = html.escape(str(item.get('title') or 'Contenido Te Equipamos'))
    source = html.escape(original, quote=True)
    page = f'''<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>{title} | Te Equipamos</title>
<style>*{{box-sizing:border-box}}html,body{{margin:0;background:#fff}}.reader{{width:100%;border:0;display:block;min-height:100vh}}.reader-fallback{{display:none;padding:24px;font-family:Arial,sans-serif}}footer{{padding:20px;text-align:center;font:13px Arial,sans-serif;color:#777;border-top:1px solid #eee}}footer a{{color:#1a73e8;text-decoration:none;font-weight:700}}</style></head><body>
<iframe id="teFullContent" class="reader" src="{source}" title="{title}" loading="eager"></iframe>
<div class="reader-fallback"><a href="{source}">Abrir contenido original →</a></div>
<footer><a href="{home_url}">← Volver a Te Equipamos</a></footer>
<script>
(function(){{
 const HOME={json.dumps(home_url)};
 const frame=document.getElementById('teFullContent');
 function wireBrand(){{
   try{{
     const d=frame.contentDocument;if(!d)return;
     d.querySelectorAll('a').forEach(a=>{{
       const label=(a.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
       if(label==='te equipamos'||label==='teequipamos'||(a.classList&&a.classList.contains('brand')&&label.includes('te equipamos'))){{
         a.href=HOME;
         a.target='_top';
         a.setAttribute('aria-label','Ir al inicio de Te Equipamos');
       }}
     }});
   }}catch(e){{}}
 }}
 function fit(){{try{{const d=frame.contentDocument;if(!d)return;const h=Math.max(d.body.scrollHeight,d.documentElement.scrollHeight);if(h>400)frame.style.height=h+'px';}}catch(e){{}}}}
 frame.addEventListener('load',function(){{wireBrand();fit();try{{const d=frame.contentDocument;new ResizeObserver(function(){{wireBrand();fit();}}).observe(d.documentElement);}}catch(e){{}}setTimeout(function(){{wireBrand();fit();}},500);setTimeout(function(){{wireBrand();fit();}},1500);}});
 window.addEventListener('resize',fit);
}})();
</script></body></html>'''
    (wrapper_dir / 'index.html').write_text(page, encoding='utf-8')
    item['source_url'] = original
    item['url'] = wrapper_url
    item['wrapped'] = True
    wrapped += 1

data_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Lectores Te Equipamos creados para {wrapped} contenidos externos y marca enlazada al Hub oficial.')

from pathlib import Path

path = Path(__file__).resolve().parent / "index.html"
html = path.read_text(encoding="utf-8")

old = "if(a){e.preventDefault();openArticle(a.dataset.article);return}"
new = "if(a){e.preventDefault();const n=NEWS.find(x=>x.id===Number(a.dataset.article));if(n&&n.direct&&n.url){location.assign(n.url);return}openArticle(a.dataset.article);return}"

if old in html:
    html = html.replace(old, new, 1)
elif new not in html:
    raise RuntimeError("No se encontró el manejador de clic de las tarjetas")

path.write_text(html, encoding="utf-8")
print("Tarjetas de producto: imagen y título abren directamente la landing")

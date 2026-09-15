from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

old = """  function enhanceCards(root=document){
    const scope=root&&root.querySelectorAll?root:document;
    scope.querySelectorAll('.card').forEach(card=>{
"""
new = """  function enhanceCards(root=document){
    const scope=root&&root.querySelectorAll?root:document;
    const cards=[];
    if(scope.matches&&scope.matches('.card'))cards.push(scope);
    cards.push(...scope.querySelectorAll('.card'));
    cards.forEach(card=>{
"""

if old in html:
    html = html.replace(old, new, 1)
elif "if(scope.matches&&scope.matches('.card'))cards.push(scope);" not in html:
    raise RuntimeError('No se pudo reforzar el comparador para tarjetas dinámicas')

path.write_text(html, encoding='utf-8')
print('Comparador reforzado para filtros y reconstrucciones dinámicas del feed')

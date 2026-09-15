from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

for sid, closing in [('teProductComparatorCss', '</style>'), ('teProductComparatorScript', '</script>')]:
    tag = '<style' if closing == '</style>' else '<script'
    start = html.find(f'{tag} id="{sid}">')
    if start != -1:
        end = html.find(closing, start)
        if end != -1:
            html = html[:start] + html[end + len(closing):]

css = r'''<style id="teProductComparatorCss">/* TE_PRODUCT_COMPARATOR */
.teCompareButton{appearance:none;border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:999px;padding:7px 11px;font-size:11px;font-weight:800;cursor:pointer;white-space:nowrap;transition:background .16s ease,color .16s ease,border-color .16s ease}
.teCompareButton:hover{background:var(--soft);border-color:color-mix(in srgb,var(--accent) 38%,var(--line));color:var(--accent)}
.teCompareButton[aria-pressed="true"]{background:var(--soft);border-color:color-mix(in srgb,var(--accent) 45%,var(--line));color:var(--accent)}
.teCompareSlot{display:flex;align-items:center;gap:8px;margin-top:10px}
.teCompareTray{position:fixed;z-index:126;left:50%;bottom:20px;transform:translate(-50%,18px);width:min(760px,calc(100vw - 32px));display:flex;align-items:center;gap:12px;padding:12px 14px;background:color-mix(in srgb,var(--surface) 94%,transparent);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 48px rgba(14,18,15,.18);backdrop-filter:blur(16px);opacity:0;visibility:hidden;pointer-events:none;transition:opacity .2s ease,transform .2s ease,visibility .2s ease}
.teCompareTray.open{opacity:1;visibility:visible;pointer-events:auto;transform:translate(-50%,0)}
.teCompareTrayText{min-width:0;flex:1}.teCompareTrayText strong{display:block;font-size:13px}.teCompareTrayText span{display:block;margin-top:3px;color:var(--muted);font-size:11px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.teCompareTrayClear,.teCompareTrayOpen{appearance:none;border:0;border-radius:999px;min-height:40px;padding:0 14px;font-size:12px;font-weight:850;cursor:pointer}
.teCompareTrayClear{background:transparent;color:var(--muted)}.teCompareTrayOpen{background:var(--accent);color:var(--surface)}.teCompareTrayOpen:disabled{opacity:.42;cursor:not-allowed}
.teCompareOverlay{position:fixed;inset:0;z-index:150;background:rgba(8,10,8,.52);display:flex;align-items:center;justify-content:center;padding:28px;opacity:0;visibility:hidden;pointer-events:none;transition:opacity .2s ease,visibility .2s ease}
.teCompareOverlay.open{opacity:1;visibility:visible;pointer-events:auto}
.teCompareDialog{width:min(1120px,100%);max-height:min(820px,calc(100dvh - 56px));overflow:auto;overscroll-behavior:contain;background:var(--surface);color:var(--text);border:1px solid var(--line);border-radius:24px;box-shadow:0 28px 90px rgba(8,10,8,.28)}
.teCompareTop{position:sticky;top:0;z-index:2;display:flex;align-items:center;justify-content:space-between;gap:18px;padding:20px 22px;background:color-mix(in srgb,var(--surface) 96%,transparent);border-bottom:1px solid var(--line);backdrop-filter:blur(12px)}
.teCompareTop div{min-width:0}.teCompareTop span{display:block;color:var(--accent);font-size:10px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}.teCompareTop h2{margin:4px 0 0;font-size:25px;letter-spacing:-.035em}.teCompareClose{width:42px;height:42px;display:grid;place-items:center;border:0;border-radius:50%;background:var(--surface2);color:var(--text);font-size:24px;cursor:pointer}
.teCompareBody{padding:22px}.teCompareGrid{display:grid;grid-template-columns:160px repeat(var(--te-compare-count),minmax(220px,1fr));border:1px solid var(--line);border-radius:18px;overflow:hidden}.teCompareCell{padding:15px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);min-width:0}.teCompareCell:nth-child(calc(var(--te-compare-count) + 1n)){ }.teCompareCellLabel{background:var(--surface2);font-size:11px;font-weight:850;color:var(--muted);text-transform:uppercase;letter-spacing:.055em}.teCompareCell:last-child{border-right:0}.teCompareProduct{padding:0;background:var(--surface)}.teCompareProduct img{width:100%;height:150px;object-fit:cover;background:var(--surface2)}.teCompareProductCopy{padding:14px 16px 17px}.teCompareProductCopy small{display:block;color:var(--accent);font-size:10px;font-weight:850;text-transform:uppercase;letter-spacing:.06em}.teCompareProductCopy strong{display:block;margin-top:5px;font-size:16px;line-height:1.26}.teCompareProductCopy a{display:inline-flex;margin-top:10px;color:var(--accent);font-size:12px;font-weight:800;text-decoration:none}.teCompareValue{font-size:13px;line-height:1.45}.teCompareMissing{color:var(--muted)}.teCompareHint{margin:15px 2px 0;color:var(--muted);font-size:11px;line-height:1.5}
body.teCompareLocked{overflow:hidden}
@media(max-width:760px){
  .teCompareSlot{margin-top:8px}.teCompareButton{min-height:40px;padding:8px 12px}
  .teCompareTray{bottom:max(10px,env(safe-area-inset-bottom));width:calc(100vw - 20px);padding:10px 11px;border-radius:16px;gap:7px}.teCompareTrayClear{display:none}.teCompareTrayOpen{padding:0 12px}.teCompareTrayText span{max-width:48vw}
  .teCompareOverlay{padding:0;align-items:flex-end}.teCompareDialog{width:100%;height:94dvh;max-height:none;border-radius:22px 22px 0 0;border-left:0;border-right:0;border-bottom:0}.teCompareTop{padding:17px 16px}.teCompareTop h2{font-size:22px}.teCompareBody{padding:14px 12px max(26px,env(safe-area-inset-bottom));overflow-x:auto}.teCompareGrid{min-width:760px;grid-template-columns:130px repeat(var(--te-compare-count),minmax(210px,1fr))}.teCompareProduct img{height:132px}.teCompareCell{padding:13px 14px}
}
@media(prefers-reduced-motion:reduce){.teCompareButton,.teCompareTray,.teCompareOverlay{transition:none!important}}
</style>'''
html = html.replace('</head>', css + '</head>', 1)

script = r'''<script id="teProductComparatorScript">/* TE_PRODUCT_COMPARATOR_JS */
(function(){
  const VERIFIED={
    920001:{group:'Equipaje',capacity:'27 L',use:'Rutas, escapadas y uso diario',features:'Tres colores disponibles'},
    920002:{group:'Ropa',use:'Caminatas y trekking',features:'Tejido transpirable · secado rápido'},
    920003:{group:'Calzado',protection:'Tejido perlante',features:'Tacos de 3 mm · amortiguación en talón · suela flexible'},
    920004:{group:'Equipaje',capacity:'25 L',use:'Trabajo, gimnasio y día a día',features:'4 bolsillos'},
    920005:{group:'Equipaje',capacity:'16–20 L',use:'Ciudad, viajes y senderos',features:'Rolltop · capacidad ampliable'},
    920006:{group:'Ropa',protection:'Impermeabilidad 5000 mm · protección frente al viento',features:'Ventilación en la espalda'},
    920007:{group:'Equipaje',capacity:'5 L',weight:'150 g',use:'Mochila infantil',features:'Espalda acolchada'},
    920008:{group:'Ropa',materials:'75 % plumón / 25 % pluma en el torso',features:'Aislamiento técnico en brazos y capucha',status:'Segunda mano · poco uso · indicada como intacta'},
    920009:{group:'Calzado',materials:'Piel · amortiguación EVA',features:'Tacos de 4 mm · refuerzos',use:'Senderismo'},
    920010:{group:'Accesorios',protection:'UPF50+',features:'Ala de 7 cm · ventilación · cordón de ajuste',use:'Trekking'},
    920011:{group:'Calzado',materials:'Plantilla EVA extraíble',features:'Doble ajuste · construcción ligera',use:'Senderismo de verano'},
    920012:{group:'Calzado',materials:'Upper de mesh ventilable',use:'Urbano y casual',features:'Construcción ligera'},
    920013:{group:'Equipaje',capacity:'10 L',weight:'45 g',use:'Viajes y trekking',features:'Plegable sobre sí misma'},
    920014:{group:'Equipaje',capacity:'20 L',use:'Ciudad y senderismo ocasional',features:'5 bolsillos · espacio para portátil'}
  };
  const ROWS=[['capacity','Capacidad'],['weight','Peso'],['protection','Protección'],['materials','Materiales'],['features','Características'],['use','Uso indicado'],['status','Estado / disponibilidad']];
  const esc=v=>String(v??'').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[s]));
  const items=()=>typeof NEWS!=='undefined'&&Array.isArray(NEWS)?NEWS:[];
  const productById=id=>items().find(n=>Number(n.id)===Number(id)&&n.owned&&n.kind==='product');
  function heuristicGroup(p){const t=String(p&&p.title||'').toLowerCase();if(/mochila|bolso/.test(t))return'Equipaje';if(/zapatilla|sandalia/.test(t))return'Calzado';if(/camiseta|chaqueta|chubasquero/.test(t))return'Ropa';if(/sombrero|gorra/.test(t))return'Accesorios';return'Productos'}
  function spec(p){const v=VERIFIED[Number(p.id)]||{};return {...v,group:v.group||heuristicGroup(p),status:v.status||String(p.time||'Consultar disponibilidad'),use:v.use||String(p.summary||'')}}
  let selected=[];
  try{selected=JSON.parse(sessionStorage.getItem('teCompareSelection')||'[]').map(Number).filter(Boolean).slice(0,3)}catch(e){selected=[]}
  selected=selected.filter(id=>!!productById(id));
  function save(){sessionStorage.setItem('teCompareSelection',JSON.stringify(selected))}
  function toast(msg){if(typeof showToast==='function'){showToast(msg);return}let t=document.getElementById('teCompareToast');if(!t){t=document.createElement('div');t.id='teCompareToast';t.className='toast';document.body.appendChild(t)}t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1800)}
  function ensureUi(){
    if(!document.getElementById('teCompareTray')){
      const tray=document.createElement('div');tray.id='teCompareTray';tray.className='teCompareTray';tray.setAttribute('aria-live','polite');tray.innerHTML='<div class="teCompareTrayText"><strong>Comparador</strong><span id="teCompareTrayNames"></span></div><button type="button" class="teCompareTrayClear" id="teCompareClear">Limpiar</button><button type="button" class="teCompareTrayOpen" id="teCompareOpen">Comparar</button>';document.body.appendChild(tray)
    }
    if(!document.getElementById('teCompareOverlay')){
      const overlay=document.createElement('div');overlay.id='teCompareOverlay';overlay.className='teCompareOverlay';overlay.setAttribute('aria-hidden','true');overlay.innerHTML='<section class="teCompareDialog" role="dialog" aria-modal="true" aria-labelledby="teCompareTitle"><header class="teCompareTop"><div><span>TE EQUIPAMOS</span><h2 id="teCompareTitle">Comparar productos</h2></div><button class="teCompareClose" id="teCompareClose" type="button" aria-label="Cerrar comparador">×</button></header><div class="teCompareBody" id="teCompareBody"></div></section>';document.body.appendChild(overlay)
    }
  }
  function cardProduct(card){const trigger=card.querySelector('[data-article]');return trigger?productById(trigger.dataset.article):null}
  function enhanceCards(root=document){
    const scope=root&&root.querySelectorAll?root:document;
    scope.querySelectorAll('.card').forEach(card=>{
      const p=cardProduct(card);if(!p)return;
      let slot=card.querySelector('.teCompareSlot');if(!slot){slot=document.createElement('div');slot.className='teCompareSlot';const host=card.querySelector('.cardMeta')||card.querySelector('div');if(host)host.insertAdjacentElement('beforebegin',slot)}
      if(!slot||slot.querySelector('.teCompareButton'))return;
      const btn=document.createElement('button');btn.type='button';btn.className='teCompareButton';btn.dataset.compareId=String(p.id);btn.textContent='Comparar';slot.appendChild(btn)
    });
    syncButtons()
  }
  function syncButtons(){
    document.querySelectorAll('.teCompareButton[data-compare-id]').forEach(btn=>{const on=selected.includes(Number(btn.dataset.compareId));btn.setAttribute('aria-pressed',on?'true':'false');btn.textContent=on?'✓ Comparando':'Comparar'});
    const tray=document.getElementById('teCompareTray'),names=document.getElementById('teCompareTrayNames'),open=document.getElementById('teCompareOpen');if(!tray)return;
    const ps=selected.map(productById).filter(Boolean);tray.classList.toggle('open',ps.length>0);if(names)names.textContent=ps.map(p=>p.title).join(' · ');if(open){open.disabled=ps.length<2;open.textContent=ps.length<2?'Elige otro':'Comparar '+ps.length}
  }
  function toggle(id){
    const p=productById(id);if(!p)return;
    if(selected.includes(Number(id))){selected=selected.filter(x=>x!==Number(id));save();syncButtons();return}
    if(selected.length>=3){toast('Puedes comparar hasta 3 productos');return}
    if(selected.length){const first=productById(selected[0]);if(first&&spec(first).group!==spec(p).group){toast('Para una comparación útil, elige productos del mismo tipo');return}}
    selected.push(Number(id));save();syncButtons();if(selected.length===1)toast('Elige otro producto del mismo tipo')
  }
  function cell(value){return `<div class="teCompareCell teCompareValue ${value?'':'teCompareMissing'}">${value?esc(value):'No indicado en la ficha'}</div>`}
  function openCompare(){
    const ps=selected.map(productById).filter(Boolean);if(ps.length<2)return;ensureUi();const body=document.getElementById('teCompareBody'),overlay=document.getElementById('teCompareOverlay');if(!body||!overlay)return;
    const count=ps.length;let out=`<div class="teCompareGrid" style="--te-compare-count:${count}"><div class="teCompareCell teCompareCellLabel">Producto</div>`;
    out+=ps.map(p=>`<article class="teCompareCell teCompareProduct"><img src="${esc(p.image)}" alt="${esc(p.title)}" loading="lazy" decoding="async"><div class="teCompareProductCopy"><small>${esc(spec(p).group)}</small><strong>${esc(p.title)}</strong><a href="${esc(p.url)}" target="_blank" rel="noopener noreferrer">Ver producto →</a></div></article>`).join('');
    for(const [key,label] of ROWS){out+=`<div class="teCompareCell teCompareCellLabel">${esc(label)}</div>`;out+=ps.map(p=>cell(spec(p)[key])).join('')}
    out+='</div><p class="teCompareHint">Solo mostramos datos presentes en las fichas actuales de Te Equipamos. Cuando un dato no está documentado, se indica expresamente en lugar de estimarlo.</p>';
    body.innerHTML=out;overlay.classList.add('open');overlay.setAttribute('aria-hidden','false');document.body.classList.add('teCompareLocked');setTimeout(()=>document.getElementById('teCompareClose')?.focus(),20)
  }
  function closeCompare(){const overlay=document.getElementById('teCompareOverlay');if(!overlay)return;overlay.classList.remove('open');overlay.setAttribute('aria-hidden','true');document.body.classList.remove('teCompareLocked')}
  function clear(){selected=[];save();syncButtons();closeCompare()}
  function start(){ensureUi();enhanceCards();const obs=new MutationObserver(records=>{for(const r of records)for(const n of r.addedNodes)if(n.nodeType===1)enhanceCards(n)});obs.observe(document.body,{childList:true,subtree:true});syncButtons()}
  document.addEventListener('click',e=>{
    const btn=e.target.closest&&e.target.closest('[data-compare-id]');if(btn){e.preventDefault();e.stopPropagation();toggle(btn.dataset.compareId);return}
    if(e.target.closest&&e.target.closest('#teCompareOpen')){e.preventDefault();openCompare();return}
    if(e.target.closest&&e.target.closest('#teCompareClear')){e.preventDefault();clear();return}
    if(e.target.closest&&e.target.closest('#teCompareClose')){e.preventDefault();closeCompare();return}
    if(e.target.id==='teCompareOverlay'){closeCompare()}
  },true);
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.getElementById('teCompareOverlay')?.classList.contains('open'))closeCompare()});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start,{once:true});else start();
})();
</script>'''
html = html.replace('</body>', script + '</body>', 1)

for marker in ['/* TE_PRODUCT_COMPARATOR */','/* TE_PRODUCT_COMPARATOR_JS */','VERIFIED={']:
    if marker not in html:
        raise RuntimeError('No se instaló correctamente el comparador: ' + marker)

path.write_text(html, encoding='utf-8')
print('Comparador de productos instalado: máximo 3, solo datos documentados y productos del mismo tipo')

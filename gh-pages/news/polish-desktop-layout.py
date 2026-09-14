from pathlib import Path

path = Path(__file__).resolve().parent / 'index.html'
html = path.read_text(encoding='utf-8')

css = r'''/* TE_DESKTOP_POLISH */
.teDesktopUtility,.teRailExtra{display:none}
@media(min-width:1101px){
  .row{max-width:1600px;margin:0 auto;grid-template-columns:220px minmax(440px,820px) 1fr;gap:18px;padding:0 28px}
  .cats{max-width:1600px;margin:0 auto;padding-left:292px;gap:6px}
  .chip{padding:9px 16px}
  .shell{max-width:1600px;grid-template-columns:190px minmax(0,1fr) 300px;gap:24px;padding:28px 28px 70px}
  .side .nav{display:none!important}
  .teDesktopUtility{display:grid;gap:18px;position:sticky;top:136px;height:max-content}
  .teDeskBlock{display:grid;gap:8px}
  .teDeskEyebrow{font-size:10px;line-height:1;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);padding:0 8px 4px}
  .teDeskAction{width:100%;border:0;background:transparent;color:var(--muted);border-radius:12px;min-height:38px;padding:8px 10px;display:flex;align-items:center;justify-content:space-between;gap:10px;text-align:left;cursor:pointer;font-size:13px}
  .teDeskAction:hover{background:var(--surface2);color:var(--text)}
  .teDeskAction strong{font-size:12px;color:var(--accent);background:var(--soft);border-radius:999px;padding:3px 7px;min-width:24px;text-align:center}
  .teDeskTags{display:flex;flex-wrap:wrap;gap:6px;padding:0 4px}
  .teDeskTags .tagPill{font-size:9px;padding:6px 8px}
  .main>.section{margin-top:24px}
  .feed{border-radius:16px}
  .feed .card{position:relative;display:block!important;padding:18px 56px 18px 22px!important;min-height:0!important;gap:0!important}
  .feed .card>.thumb{display:none!important}
  .feed .card>div:first-child{padding:0!important;min-width:0}
  .feed .card .title{font-size:21px;line-height:1.22;margin:5px 0 8px;letter-spacing:-.012em}
  .feed .card:first-child .title{font-size:23px}
  .feed .card .summary{font-size:13.5px;line-height:1.46;margin:0 0 9px;max-width:920px}
  .feed .card .tagRow{margin:7px 0 8px}
  .feed .card .tagPill{font-size:9px;padding:5px 8px}
  .feed .card .cardShare{gap:6px;margin:7px 0 8px}
  .feed .card .cardShareBtn{width:30px;height:30px}
  .feed .card .cardShareBtn svg{width:17px;height:17px}
  .feed .card .cardMeta{font-size:11.5px;gap:6px;min-height:18px}
  .feed .card .save{position:absolute;top:17px;right:18px;margin:0;width:30px;height:30px;font-size:19px;border-radius:50%}
  .feed .card .save:hover{background:var(--surface2)}
  .rail{position:sticky;top:132px;height:max-content;max-height:calc(100vh - 150px);overflow:auto;padding-bottom:14px;scrollbar-width:thin}
  .rail .teLegacyRail{display:none!important}
  .teRailExtra{display:block}
  .teRailExtra h3{margin:4px 0 12px;font-size:17px}
  .teRailTags{display:flex;flex-wrap:wrap;gap:6px}
  .teRailTags .tagPill{font-size:9px;padding:6px 8px}
  .teRailList{display:grid;gap:0}
  .teRailItem{width:100%;border:0;border-bottom:1px solid var(--line);background:transparent;text-align:left;padding:10px 0;cursor:pointer;color:var(--text)}
  .teRailItem:last-child{border-bottom:0;padding-bottom:0}
  .teRailItem small{display:block;color:var(--accent);font-size:9px;font-weight:900;text-transform:uppercase;margin-bottom:4px}
  .teRailItem b{display:block;font-size:12px;line-height:1.35}
  .teRailSavedRow{display:flex;align-items:center;justify-content:space-between;gap:12px}
  .teRailSavedRow strong{font-size:26px;color:var(--accent)}
  .teRailSavedRow span{font-size:12px;line-height:1.4;color:var(--muted)}
  .teRailOpen{margin-top:12px;border:0;background:transparent;color:var(--accent);font-size:11px;font-weight:900;cursor:pointer;padding:0}
}
@media(min-width:1400px){
  .shell{grid-template-columns:200px minmax(0,1fr) 310px;gap:28px}
  .feed .card{padding-left:24px!important;padding-right:60px!important}
}
'''

if '/* TE_DESKTOP_POLISH */' not in html:
    html = html.replace('</style>', css + '</style>', 1)

js = r'''<script id="teDesktopPolish">
(function(){
  const mq=window.matchMedia('(min-width:1101px)');
  function recentIds(){
    if(typeof teRecentIds==='function') return teRecentIds();
    try{return JSON.parse(localStorage.getItem('teRecentItems')||'[]').map(Number).filter(Boolean)}catch(e){return[]}
  }
  function topTags(limit){
    const counts=new Map();
    (window.NEWS||NEWS||[]).forEach(n=>(n.tags||[]).forEach(t=>{const k=String(t||'').trim();if(k)counts.set(k,(counts.get(k)||0)+1)}));
    return [...counts.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0],'es')).slice(0,limit).map(x=>x[0]);
  }
  function savedCount(){return window.state&&state.saved&&typeof state.saved.size==='number'?state.saved.size:0}
  function toneClass(t){return typeof tagTone==='function'?`tone-${tagTone(t)}`:'tone-neutral'}
  function escText(v){return typeof esc==='function'?esc(String(v||'')):String(v||'').replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[s]))}
  function ensureLeft(){
    const side=document.querySelector('.side'); if(!side)return null;
    let box=document.getElementById('teDesktopUtility');
    if(!box){box=document.createElement('div');box.id='teDesktopUtility';box.className='teDesktopUtility';side.appendChild(box)}
    return box;
  }
  function renderLeft(){
    const box=ensureLeft(); if(!box)return;
    const recent=recentIds().length, saved=savedCount();
    const tags=topTags(7);
    box.innerHTML=`<section class="teDeskBlock"><div class="teDeskEyebrow">Tu espacio</div><button class="teDeskAction" type="button" data-desk-action="saved"><span>★ Guardados</span><strong>${saved}</strong></button><button class="teDeskAction" type="button" data-desk-action="recent"><span>◷ Visto recientemente</span><strong>${recent}</strong></button></section><section class="teDeskBlock"><div class="teDeskEyebrow">Explorar</div><div class="teDeskTags">${tags.map(t=>`<button type="button" class="tagPill ${toneClass(t)}" data-tag-filter="${escText(t)}">${escText(t)}</button>`).join('')}</div></section>`;
  }
  function ensureRail(){
    const rail=document.querySelector('.rail'); if(!rail)return null;
    const legacy=[...rail.querySelectorAll(':scope > .railCard')][1]; if(legacy)legacy.classList.add('teLegacyRail');
    let topics=document.getElementById('teRailTopics');
    if(!topics){topics=document.createElement('section');topics.id='teRailTopics';topics.className='railCard teRailExtra';rail.appendChild(topics)}
    let recent=document.getElementById('teRailRecent');
    if(!recent){recent=document.createElement('section');recent.id='teRailRecent';recent.className='railCard teRailExtra';rail.appendChild(recent)}
    let saved=document.getElementById('teRailSaved');
    if(!saved){saved=document.createElement('section');saved.id='teRailSaved';saved.className='railCard teRailExtra';rail.appendChild(saved)}
    return {topics,recent,saved};
  }
  function renderRail(){
    const parts=ensureRail(); if(!parts)return;
    const tags=topTags(8);
    parts.topics.innerHTML=`<span class="kicker">Explorar</span><h3>Temas</h3><div class="teRailTags">${tags.map(t=>`<button type="button" class="tagPill ${toneClass(t)}" data-tag-filter="${escText(t)}">${escText(t)}</button>`).join('')}</div>`;
    const recents=recentIds().map(id=>(window.NEWS||NEWS).find(n=>Number(n.id)===Number(id))).filter(Boolean).slice(0,3);
    parts.recent.classList.toggle('hidden',!recents.length);
    if(recents.length)parts.recent.innerHTML=`<span class="kicker">Continúa</span><h3>Visto recientemente</h3><div class="teRailList">${recents.map(n=>`<button type="button" class="teRailItem" data-article="${n.id}"><small>${escText((n.sections||[])[0]||n.category||'Te Equipamos')}</small><b>${escText(n.title)}</b></button>`).join('')}</div>`;
    const count=savedCount();
    parts.saved.innerHTML=`<span class="kicker">Tu selección</span><h3>Guardados</h3><div class="teRailSavedRow"><strong>${count}</strong><span>${count?`contenido${count===1?'':'s'} para volver cuando quieras.`:'Usa la estrella para guardar productos y reviews.'}</span></div><button class="teRailOpen" type="button" data-desk-action="saved">Ver guardados →</button>`;
  }
  function refresh(){if(!mq.matches)return;renderLeft();renderRail()}
  function openRecent(){
    const ids=recentIds();
    if(!ids.length){if(typeof toast==='function')toast('Aún no has abierto contenidos recientemente');return}
    if(typeof setCat==='function')setCat('Todas');
    setTimeout(()=>{if(typeof renderRecent==='function')renderRecent();const r=document.getElementById('recentSection');if(r)r.scrollIntoView({behavior:'smooth',block:'start'})},80);
  }
  document.addEventListener('click',e=>{
    const a=e.target.closest&&e.target.closest('[data-desk-action]');
    if(a){e.preventDefault();const action=a.dataset.deskAction;if(action==='saved'&&typeof setCat==='function')setCat('Siguiendo');if(action==='recent')openRecent();setTimeout(refresh,80);return}
    if(e.target.closest&&e.target.closest('.save,[data-article],[data-tag-filter]'))setTimeout(refresh,120);
  },true);
  window.addEventListener('pageshow',()=>setTimeout(refresh,60));
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh()});
  mq.addEventListener&&mq.addEventListener('change',refresh);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',refresh,{once:true});else refresh();
})();
</script>'''

if 'id="teDesktopPolish"' in html:
    a = html.find('<script id="teDesktopPolish">')
    b = html.find('</script>', a)
    if a != -1 and b != -1:
        html = html[:a] + js + html[b+9:]
else:
    html = html.replace('</body>', js + '</body>', 1)

path.write_text(html, encoding='utf-8')
print('Escritorio pulido: navegación complementaria, tarjetas editoriales y lateral útil')

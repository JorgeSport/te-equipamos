(function(){
  'use strict';
  if (!window.NEWS || !Array.isArray(window.NEWS)) return;

  const VIEW_KEY = 'teContentViewsV1';
  const escHtml = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'
  }[ch]));
  const publicSection = section => section === 'Ventas' ? 'Productos' : (section || 'Te Equipamos');

  function readViews(){
    try {
      const raw = JSON.parse(localStorage.getItem(VIEW_KEY) || '{}');
      return raw && typeof raw === 'object' ? raw : {};
    } catch (_) { return {}; }
  }

  function bumpView(id){
    id = String(id || '');
    if (!id) return;
    const views = readViews();
    views[id] = Math.min(9999, Number(views[id] || 0) + 1);
    try { localStorage.setItem(VIEW_KEY, JSON.stringify(views)); } catch (_) {}
  }

  function curatedSelection(){
    const owned = NEWS.filter(n => n && n.owned).sort((a,b) => Number(b.score || 0) - Number(a.score || 0));
    if (!owned.length) return [];
    const picks = [];
    ['Reviews','Ofertas','Ventas'].forEach(section => {
      const item = owned.find(n => (n.sections || []).includes(section) && !picks.includes(n));
      if (item) picks.push(item);
    });
    owned.forEach(n => { if (picks.length < 3 && !picks.includes(n)) picks.push(n); });
    return picks.slice(0,3);
  }

  function ensureSelection(){
    let section = document.getElementById('teEditorialSelection');
    if (section) return section;
    const hero = document.getElementById('hero');
    if (!hero || !hero.parentNode) return null;
    section = document.createElement('section');
    section.id = 'teEditorialSelection';
    section.className = 'section te-editorial-selection hidden';
    hero.insertAdjacentElement('afterend', section);
    return section;
  }

  function renderSelection(){
    const section = ensureSelection();
    if (!section) return;
    const portal = document.getElementById('portal');
    const show = portal && !portal.classList.contains('hidden') && window.state && state.cat === 'Todas' && !state.q;
    section.classList.toggle('hidden', !show);
    if (!show) return;

    const picks = curatedSelection();
    if (!picks.length) { section.classList.add('hidden'); return; }
    const main = picks[0];
    const rest = picks.slice(1);
    const itemHref = item => String(item.url || '#');
    const itemMeta = item => publicSection((item.sections || [])[0] || item.category || 'Te Equipamos');

    section.innerHTML = `
      <div class="head te-editorial-head">
        <div><span class="te-editorial-eyebrow">SELECCIÓN TE EQUIPAMOS</span><h2>Elegido por nuestro criterio editorial</h2><p>Tres contenidos propios que merece la pena tener a mano.</p></div>
      </div>
      <div class="te-editorial-grid">
        <a class="te-editorial-main" href="${escHtml(itemHref(main))}" data-editorial-id="${escHtml(main.id)}">
          <img src="${escHtml(main.image || '')}" alt="">
          <div class="te-editorial-main-copy">
            <small>${escHtml(itemMeta(main))}</small>
            <h3>${escHtml(main.title || '')}</h3>
            <p>${escHtml(main.summary || '')}</p>
            <span>Ver selección →</span>
          </div>
        </a>
        <div class="te-editorial-side">
          ${rest.map(item => `
            <a class="te-editorial-side-item" href="${escHtml(itemHref(item))}" data-editorial-id="${escHtml(item.id)}">
              <img src="${escHtml(item.image || '')}" alt="">
              <div><small>${escHtml(itemMeta(item))}</small><strong>${escHtml(item.title || '')}</strong><span>Explorar →</span></div>
            </a>`).join('')}
        </div>
      </div>`;
  }

  function adaptiveTrendRows(){
    const views = readViews();
    const viewed = NEWS
      .map(n => ({n, count:Number(views[String(n.id)] || 0)}))
      .filter(row => row.count > 0)
      .sort((a,b) => b.count - a.count || Number(b.n.score || 0) - Number(a.n.score || 0));
    if (viewed.length >= 2) return {title:'Más visto por ti', rows:viewed.slice(0,5).map(row => row.n)};
    return {title:'Selección del momento', rows:[...NEWS].sort((a,b) => Number(b.score || 0) - Number(a.score || 0)).slice(0,5)};
  }

  function renderAdaptiveTrend(){
    const list = document.getElementById('trend');
    if (!list) return;
    const card = list.closest('.railCard');
    const heading = card && card.querySelector('h3');
    const {title, rows} = adaptiveTrendRows();
    if (heading) heading.textContent = title;
    list.innerHTML = rows.map(n => `<li data-article="${escHtml(n.id)}"><span>${escHtml(n.title || '')}</span></li>`).join('');
  }

  function ensureProgress(){
    let bar = document.getElementById('teHubReadingProgress');
    if (bar) return bar;
    bar = document.createElement('div');
    bar.id = 'teHubReadingProgress';
    bar.className = 'te-hub-reading-progress';
    bar.setAttribute('aria-hidden','true');
    document.body.appendChild(bar);
    return bar;
  }

  let progressTick = false;
  function updateProgress(){
    progressTick = false;
    const bar = ensureProgress();
    const view = document.getElementById('articleView');
    const article = document.getElementById('article');
    if (!view || view.classList.contains('hidden') || !article) {
      bar.classList.remove('show');
      bar.style.transform = 'scaleX(0)';
      return;
    }
    const rect = article.getBoundingClientRect();
    const top = window.scrollY + rect.top;
    const end = top + article.scrollHeight - window.innerHeight;
    if (end <= top + 260) {
      bar.classList.remove('show');
      return;
    }
    const ratio = Math.max(0, Math.min(1, (window.scrollY - top) / (end - top)));
    bar.style.transform = `scaleX(${ratio})`;
    bar.classList.add('show');
  }

  function scheduleProgress(){
    if (progressTick) return;
    progressTick = true;
    requestAnimationFrame(updateProgress);
  }

  if (typeof window.renderTrend === 'function') {
    window.renderTrend = function(){ renderAdaptiveTrend(); };
  }
  if (typeof window.renderPortal === 'function') {
    const base = window.renderPortal;
    window.renderPortal = function(){ const result = base.apply(this, arguments); renderSelection(); renderAdaptiveTrend(); scheduleProgress(); return result; };
  }
  if (typeof window.renderFeed === 'function') {
    const base = window.renderFeed;
    window.renderFeed = function(){ const result = base.apply(this, arguments); renderSelection(); return result; };
  }
  if (typeof window.setCat === 'function') {
    const base = window.setCat;
    window.setCat = function(){ const result = base.apply(this, arguments); renderSelection(); return result; };
  }
  if (typeof window.renderArticle === 'function') {
    const base = window.renderArticle;
    window.renderArticle = function(){ const result = base.apply(this, arguments); setTimeout(scheduleProgress, 0); return result; };
  }

  document.addEventListener('click', event => {
    const item = event.target.closest && event.target.closest('[data-editorial-id],[data-article],[data-suggest-id]');
    if (!item) return;
    const id = item.getAttribute('data-editorial-id') || item.getAttribute('data-article') || item.getAttribute('data-suggest-id');
    if (id) {
      bumpView(id);
      setTimeout(renderAdaptiveTrend, 0);
    }
  }, true);

  window.addEventListener('scroll', scheduleProgress, {passive:true});
  window.addEventListener('resize', scheduleProgress, {passive:true});
  window.addEventListener('popstate', () => setTimeout(() => { renderSelection(); renderAdaptiveTrend(); scheduleProgress(); }, 0));

  renderSelection();
  renderAdaptiveTrend();
  scheduleProgress();
})();

document.addEventListener('DOMContentLoaded', async function () {
  try {
    const BASE = '/te-equipamos-arpenaz-27l/news/';
    const response = await fetch(BASE + 'news-data.json');
    if (!response.ok) return;
    const items = await response.json();
    if (!Array.isArray(items) || !items.length) return;

    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
    }[ch]));
    const norm = value => String(value || '').replace(/\/$/, '').toLowerCase();
    const here = norm(location.origin + location.pathname);
    const current = items.find(x => norm(x.url) === here);
    const footer = document.querySelector('footer');
    const mount = node => footer ? footer.parentNode.insertBefore(node, footer) : document.body.appendChild(node);
    const publicSection = section => section === 'Ventas' ? 'Productos' : (section || 'Te Equipamos');
    const sectionUrl = section => BASE + '?section=' + encodeURIComponent(section);
    const itemImage = item => esc(item && item.image || '');
    const itemUrl = item => esc(item && item.url || BASE);
    const itemTitle = item => esc(item && item.title || 'Te Equipamos');
    const itemMeta = item => esc(publicSection((item && item.sections || [])[0] || item && item.category || 'Te Equipamos'));

    if (current) {
      const engage = document.createElement('section');
      engage.className = 'te-engage';
      engage.innerHTML = `
        <div class="te-engage-wrap">
          <div class="te-share-strip" aria-label="Compartir esta ficha">
            <button type="button" class="te-social" data-social="whatsapp" aria-label="Compartir por WhatsApp" title="WhatsApp">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11.7 11.7 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.6 6L0 24l6.4-1.7a11.8 11.8 0 0 0 5.7 1.5h.1C18.7 23.8 24 18.5 24 12c0-3.2-1.2-6.2-3.5-8.5ZM12.2 21.8h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.8 1 1-3.7-.2-.4a9.7 9.7 0 0 1-1.5-5.3A9.9 9.9 0 0 1 12.1 2c2.6 0 5.1 1 7 2.9a9.8 9.8 0 0 1 2.9 7c0 5.5-4.4 9.9-9.8 9.9Zm5.4-7.4c-.3-.2-1.8-.9-2.1-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-.9 1.2-.2.2-.4.2-.7.1-1.7-.8-2.8-1.5-3.9-3.4-.3-.6.3-.5.8-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.7-.6-.6-.9-.6h-.7c-.2 0-.6.1-.9.4-.3.4-1.2 1.2-1.2 2.9s1.3 3.4 1.4 3.6c.2.2 2.5 3.8 6 5.3.8.4 1.5.6 2 .7.9.3 1.7.3 2.3.2.7-.1 1.8-.7 2.1-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4Z"/></svg>
            </button>
            <button type="button" class="te-social" data-social="facebook" aria-label="Compartir en Facebook" title="Facebook">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.1C24 5.4 18.6 0 12 0S0 5.4 0 12.1C0 18.1 4.4 23 10.1 24v-8.4h-3V12h3V9.3c0-3 1.8-4.7 4.6-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.6h-2.9V24C19.6 23 24 18.1 24 12.1Z"/></svg>
            </button>
            <button type="button" class="te-social" data-social="telegram" aria-label="Compartir por Telegram" title="Telegram">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.9 2.1 2.8 9.5c-1.3.5-1.3 1.2-.2 1.5l4.9 1.5 1.9 5.8c.2.7.1 1 .9 1 .6 0 .9-.3 1.2-.6l2.7-2.6 5.6 4.1c1 .6 1.8.3 2-.9L25 3.6c.4-1.5-.6-2.2-1.6-1.8l-1.5.3Zm-2.6 3.4-9.8 8.8-.4 4.1-1.3-4.9 11.5-8c.5-.3 1-.1 0 .7Z"/></svg>
            </button>
            <button type="button" class="te-social" data-social="copy" aria-label="Copiar enlace" title="Copiar enlace">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.6 13.4a1 1 0 0 0 1.4 0l4-4a3 3 0 1 0-4.2-4.2l-2.3 2.3a1 1 0 0 1-1.4-1.4l2.3-2.3a5 5 0 1 1 7.1 7.1l-4 4a1 1 0 0 1-1.4 0 1 1 0 0 1 0-1.5Zm2.8-2.8a1 1 0 0 0-1.4 0l-4 4a3 3 0 0 0 4.2 4.2l2.3-2.3a1 1 0 1 1 1.4 1.4l-2.3 2.3a5 5 0 0 1-7.1-7.1l4-4a1 1 0 0 1 1.4 0 1 1 0 0 1 0 1.5Z"/></svg>
            </button>
          </div>
        </div>`;
      mount(engage);

      const title = String(current.title || document.title || 'Te Equipamos');
      const url = String(current.url || location.href);
      const text = 'Mira esto en Te Equipamos: ' + title;
      engage.addEventListener('click', async event => {
        const button = event.target.closest('[data-social]');
        if (!button) return;
        const social = button.dataset.social;
        if (social === 'whatsapp') {
          window.open('https://wa.me/?text=' + encodeURIComponent(text + '\n' + url), '_blank', 'noopener,noreferrer');
          return;
        }
        if (social === 'facebook') {
          window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url), '_blank', 'noopener,noreferrer');
          return;
        }
        if (social === 'telegram') {
          window.open('https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(text), '_blank', 'noopener,noreferrer');
          return;
        }
        if (social === 'copy') {
          try {
            if (navigator.clipboard && navigator.clipboard.writeText) await navigator.clipboard.writeText(url);
            else throw new Error('clipboard');
          } catch (err) {
            const area = document.createElement('textarea');
            area.value = url;
            area.style.position = 'fixed';
            area.style.opacity = '0';
            document.body.appendChild(area);
            area.select();
            document.execCommand('copy');
            area.remove();
          }
          button.classList.add('copied');
          setTimeout(() => button.classList.remove('copied'), 1400);
        }
      });
    }

    if (items.length < 2) return;

    const currentTags = new Set((current && current.tags || []).map(x => String(x).toLowerCase()));
    const currentSections = current && current.sections || [];
    const currentActivities = new Set((current && current.activities || []).map(x => String(x).toLowerCase()));

    const ranked = items
      .filter(x => norm(x.url) !== here)
      .map(x => {
        const tags = (x.tags || []).map(t => String(t).toLowerCase());
        const sharedTags = tags.filter(t => currentTags.has(t)).length;
        const sharedSection = currentSections.some(s => (x.sections || []).includes(s)) ? 1 : 0;
        const sharedActivities = (x.activities || []).filter(a => currentActivities.has(String(a).toLowerCase())).length;
        return { x, score: sharedTags * 10 + sharedSection * 5 + sharedActivities * 4 + Number(x.score || 0) / 20 };
      })
      .sort((a, b) => b.score - a.score);

    const related = ranked.slice(0, 8).map(row => row.x);
    if (!related.length) return;

    const availableSections = ['Ventas', 'Reviews', 'Ofertas', 'Consejos', 'Novedades', 'Vídeos']
      .filter(section => items.some(x => (x.sections || []).includes(section)));

    function compact(rows) {
      return `<section class="te-rel-module te-rel-compact">
        <div class="te-rel-module-head"><span>SELECCIÓN EDITORIAL</span><h3>También te puede interesar</h3></div>
        <div class="te-rel-list">${rows.slice(0, 4).map(x => `
          <a class="te-rel-row" href="${itemUrl(x)}">
            <img src="${itemImage(x)}" alt="">
            <div><small>${itemMeta(x)}</small><strong>${itemTitle(x)}</strong><p>${esc(x.summary || '')}</p></div>
            <b aria-hidden="true">›</b>
          </a>`).join('')}</div>
      </section>`;
    }

    function continueReading(rows) {
      return `<section class="te-rel-module te-rel-continue">
        <div class="te-rel-module-head"><span>CONTINÚA</span><h3>Seguir leyendo</h3></div>
        <div class="te-rel-textlist">${rows.slice(0, 4).map(x => `
          <a href="${itemUrl(x)}"><div><strong>${itemTitle(x)}</strong><p>${esc(x.summary || '')}</p></div><b aria-hidden="true">›</b></a>`).join('')}</div>
      </section>`;
    }

    function visual(rows) {
      return `<section class="te-rel-module te-rel-visual">
        <div class="te-rel-module-head"><span>DESCUBRE</span><h3>Más para explorar</h3></div>
        <div class="te-rel-visual-grid">${rows.slice(0, 3).map(x => `
          <a href="${itemUrl(x)}"><img src="${itemImage(x)}" alt=""><small>${itemMeta(x)}</small><strong>${itemTitle(x)}</strong></a>`).join('')}</div>
      </section>`;
    }

    function featured(rows) {
      const main = rows[0], rest = rows.slice(1, 4);
      if (!main) return '';
      return `<section class="te-rel-module te-rel-featured">
        <div class="te-rel-module-head"><span>SELECCIÓN DESTACADA</span><h3>Una recomendación para seguir</h3></div>
        <a class="te-rel-feature-main" href="${itemUrl(main)}">
          <img src="${itemImage(main)}" alt="">
          <div><small>${itemMeta(main)}</small><strong>${itemTitle(main)}</strong><p>${esc(main.summary || '')}</p><span>Ver contenido →</span></div>
        </a>
        <div class="te-rel-feature-minis">${rest.map(x => `
          <a href="${itemUrl(x)}"><img src="${itemImage(x)}" alt=""><strong>${itemTitle(x)}</strong></a>`).join('')}</div>
      </section>`;
    }

    function topic(rows) {
      const topic = publicSection(currentSections[0] || current && current.category || 'este tema');
      return `<section class="te-rel-module te-rel-topic">
        <div class="te-rel-module-head te-rel-inline-head"><div><span>MÁS SOBRE</span><h3>${esc(topic)}</h3></div><a href="${sectionUrl(currentSections[0] || '')}">Ver más →</a></div>
        <div class="te-rel-topic-grid">${rows.slice(0, 4).map(x => `
          <a href="${itemUrl(x)}"><img src="${itemImage(x)}" alt=""><strong>${itemTitle(x)}</strong><small>${itemMeta(x)}</small></a>`).join('')}</div>
      </section>`;
    }

    function intent() {
      const sections = availableSections
        .filter(s => !currentSections.includes(s))
        .slice(0, 4);
      if (sections.length < 2) return '';
      const labels = {
        Ventas: ['Productos relacionados', 'Explora el catálogo'],
        Reviews: ['Leer más reviews', 'Compara antes de elegir'],
        Ofertas: ['Ver ofertas activas', 'Oportunidades actuales'],
        Consejos: ['Descubrir guías', 'Aprende a elegir mejor'],
        Novedades: ['Ver novedades', 'Lo más reciente'],
        Vídeos: ['Ver vídeos', 'Contenido para ver']
      };
      return `<section class="te-rel-module te-rel-intent">
        <div class="te-rel-module-head"><span>SIGUE EXPLORANDO</span><h3>Elige cómo continuar</h3></div>
        <div class="te-rel-intent-grid">${sections.map(s => `
          <a href="${sectionUrl(s)}"><span>${esc(labels[s][0])}</span><small>${esc(labels[s][1])}</small><b aria-hidden="true">→</b></a>`).join('')}</div>
      </section>`;
    }

    function circleTopics(rows) {
      const seen = new Map();
      rows.concat(items.slice(0, 12)).forEach(item => {
        const labels = (item.activities && item.activities.length ? item.activities : item.sections || []);
        labels.forEach(label => {
          const key = String(label || '').toLowerCase();
          if (!key || seen.has(key) || !item.image || norm(item.url) === here) return;
          seen.set(key, { label: publicSection(label), item });
        });
      });
      const circles = [...seen.values()].slice(0, 6);
      if (circles.length < 4) return '';
      return `<section class="te-rel-module te-rel-circles">
        <div class="te-rel-module-head"><span>EXPLORA</span><h3>Otros temas para descubrir</h3></div>
        <div class="te-rel-circle-row">${circles.map(entry => `
          <a href="${itemUrl(entry.item)}"><img src="${itemImage(entry.item)}" alt=""><strong>${esc(entry.label)}</strong></a>`).join('')}</div>
      </section>`;
    }

    const primary = currentSections[0] || (current && current.category) || '';
    let modules = [];
    if (currentSections.includes('Reviews') || primary === 'Reviews') {
      modules = [featured(related), intent()];
    } else if (currentSections.includes('Ventas') || primary === 'Ventas') {
      modules = [intent(), visual(related)];
    } else if (currentSections.includes('Ofertas') || primary === 'Ofertas') {
      modules = [intent(), compact(related)];
    } else if (currentSections.includes('Consejos') || primary === 'Consejos') {
      modules = [continueReading(related), circleTopics(related) || topic(related)];
    } else if (currentSections.includes('Novedades') || primary === 'Novedades') {
      modules = [visual(related), circleTopics(related) || compact(related)];
    } else if (currentSections.includes('Vídeos') || primary === 'Vídeos') {
      modules = [visual(related), continueReading(related)];
    } else {
      modules = [compact(related), circleTopics(related) || continueReading(related)];
    }
    modules = modules.filter(Boolean).slice(0, 2);

    const block = document.createElement('section');
    block.className = 'te-related';
    block.innerHTML = `<div class="te-related-wrap">
      <div class="te-related-title"><span>TE EQUIPAMOS</span><h2>Sigue descubriendo</h2><p>Contenido relacionado, presentado según lo que estás viendo.</p></div>
      <div class="te-rel-modules">${modules.join('')}</div>
      <a class="te-related-more" href="${BASE}">Ver todo en Te Equipamos →</a>
    </div>`;
    mount(block);
  } catch (e) {
    console.warn('Te Equipamos related content:', e);
  }
});
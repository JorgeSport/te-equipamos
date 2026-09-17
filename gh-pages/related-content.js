document.addEventListener('DOMContentLoaded', async function () {
  const BASE = '/te-equipamos-arpenaz-27l/news/';
  const GENERIC_TAGS = new Set(['senderismo', 'trekking', 'travel', 'urbano', 'outdoor']);
  const BRAND_TAGS = new Set(['quechua', 'forclaz', 'kalenji', 'simond', 'wedze', 'kiprun']);
  const PRODUCT_FAMILIES = {
    mochila: 'carga', bolso: 'carga', riñonera: 'carga',
    zapatillas: 'calzado', sandalias: 'calzado', botas: 'calzado',
    chaqueta: 'ropa', camiseta: 'ropa', pantalon: 'ropa', short: 'ropa', legging: 'ropa',
    sombrero: 'accesorios', gorra: 'accesorios', guantes: 'accesorios',
    'editorial-running': 'calzado'
  };

  const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, character => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[character]));
  const normalize = value => String(value || '').trim().toLowerCase();
  const normalizeUrl = value => normalize(value).replace(/\/$/, '');
  const asArray = value => Array.isArray(value) ? value : [];
  const asSet = value => new Set(asArray(value).map(normalize).filter(Boolean));
  const intersects = (left, right) => [...left].filter(value => right.has(value));
  const publicSection = section => section === 'Ventas' ? 'Productos' : (section || 'Te Equipamos');
  const sectionUrl = section => BASE + '?section=' + encodeURIComponent(section || '');
  const familyOf = item => PRODUCT_FAMILIES[normalize(item && item.product_type)] || normalize(item && item.product_type) || 'general';
  const imageOf = item => escapeHtml(item && item.image || '');
  const urlOf = item => escapeHtml(item && item.url || BASE);
  const titleOf = item => escapeHtml(item && (item.card_title || item.title) || 'Te Equipamos');
  const summaryOf = item => escapeHtml(item && item.summary || '');
  const metaOf = item => escapeHtml(publicSection(asArray(item && item.sections)[0] || item && item.category || 'Te Equipamos'));
  const isRecent = item => {
    const raw = String(item && item.published_at || '').trim();
    if (!raw) return false;
    const published = new Date(raw);
    if (Number.isNaN(published.getTime())) return false;
    const age = Date.now() - published.getTime();
    return age >= 0 && age < 7 * 24 * 60 * 60 * 1000;
  };
  const freshBadge = item => isRecent(item) ? '<span class="te-rel-fresh">Recién publicado</span>' : '';
  const imageMarkup = (item, className = '') => item && item.image
    ? `<img class="${className}" src="${imageOf(item)}" alt="" loading="lazy" decoding="async">`
    : `<span class="${className} te-rel-image-fallback" aria-hidden="true"></span>`;

  try {
    const response = await fetch(BASE + 'news-data.json', { credentials: 'same-origin' });
    if (!response.ok) return;
    const items = await response.json();
    if (!Array.isArray(items) || items.length < 2) return;

    const here = normalizeUrl(location.origin + location.pathname);
    const current = items.find(item => normalizeUrl(item.url) === here);
    const footer = document.querySelector('footer');
    const mount = node => footer ? footer.parentNode.insertBefore(node, footer) : document.body.appendChild(node);

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

      const shareTitle = String(current.title || document.title || 'Te Equipamos');
      const shareUrl = String(current.url || location.href);
      const shareText = 'Mira esto en Te Equipamos: ' + shareTitle;
      engage.addEventListener('click', async event => {
        const button = event.target.closest('[data-social]');
        if (!button) return;
        const social = button.dataset.social;
        if (social === 'whatsapp') window.open('https://wa.me/?text=' + encodeURIComponent(shareText + '\n' + shareUrl), '_blank', 'noopener,noreferrer');
        if (social === 'facebook') window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(shareUrl), '_blank', 'noopener,noreferrer');
        if (social === 'telegram') window.open('https://t.me/share/url?url=' + encodeURIComponent(shareUrl) + '&text=' + encodeURIComponent(shareText), '_blank', 'noopener,noreferrer');
        if (social === 'copy') {
          try {
            if (!navigator.clipboard || !navigator.clipboard.writeText) throw new Error('clipboard-unavailable');
            await navigator.clipboard.writeText(shareUrl);
          } catch (error) {
            const area = document.createElement('textarea');
            area.value = shareUrl;
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

    const currentTags = asSet(current && current.tags);
    const currentActivities = asSet(current && current.activities);
    const currentSections = asSet(current && current.sections);
    const currentType = normalize(current && current.product_type);
    const currentFamily = familyOf(current);

    const ranked = items
      .filter(item => normalizeUrl(item.url) !== here)
      .map(item => {
        const itemTags = asSet(item.tags);
        const sharedTags = intersects(itemTags, currentTags);
        const sharedActivities = intersects(asSet(item.activities), currentActivities);
        const sharedSections = intersects(asSet(item.sections), currentSections);
        const itemType = normalize(item.product_type);
        const exactTypeScore = currentType && itemType === currentType ? 60 : 0;
        const familyScore = currentFamily !== 'general' && familyOf(item) === currentFamily && itemType !== currentType ? 30 : 0;
        const activityScore = Math.min(sharedActivities.length, 2) * 8;
        const specificTagScore = sharedTags.filter(tag => !GENERIC_TAGS.has(tag) && !BRAND_TAGS.has(tag)).length * 6;
        const genericTagScore = sharedTags.filter(tag => GENERIC_TAGS.has(tag)).length * 2;
        const brandScore = sharedTags.filter(tag => BRAND_TAGS.has(tag)).length * 2;
        const sectionScore = sharedSections.length ? 3 : 0;
        const editorialScore = Number(item.score || 0) / 100;
        return { item, score: exactTypeScore + familyScore + activityScore + specificTagScore + genericTagScore + brandScore + sectionScore + editorialScore };
      })
      .sort((left, right) => right.score - left.score || Number(right.item.score || 0) - Number(left.item.score || 0));

    const related = ranked.slice(0, 8).map(entry => entry.item);
    if (!related.length) return;
    const moduleHeader = (eyebrow, title) => `<div class="te-rel-module-head"><span>${escapeHtml(eyebrow)}</span><h3>${escapeHtml(title)}</h3></div>`;

    function zigzag(rows) {
      if (!rows.length) return '';
      return `<section class="te-rel-module te-rel-zigzag">${moduleHeader('SELECCIÓN RELACIONADA', 'Más para descubrir')}<div class="te-rel-zigzag-list">${rows.slice(0, 4).map((item, index) => `<a class="te-rel-zigzag-row${index % 2 ? ' is-reverse' : ''}" href="${urlOf(item)}">${imageMarkup(item, 'te-rel-zigzag-image')}<div class="te-rel-zigzag-copy"><small>${metaOf(item)}</small>${freshBadge(item)}<strong>${titleOf(item)}</strong><p>${summaryOf(item)}</p></div><b aria-hidden="true">→</b></a>`).join('')}</div></section>`;
    }

    function bordered(rows) {
      if (!rows.length) return '';
      return `<section class="te-rel-module te-rel-bordered">${moduleHeader('CONTENIDO ELEGIDO', 'También te puede interesar')}<div class="te-rel-bordered-grid">${rows.slice(0, 3).map(item => {
        const sections = asSet(item.sections);
        const isOffer = sections.has('ofertas') || normalize(item.category) === 'ofertas' || normalize(item.kind) === 'offer';
        const label = isOffer ? 'OFERTA' : sections.has('reviews') ? 'REVIEW' : metaOf(item);
        return `<a class="te-rel-bordered-card${isOffer ? ' is-offer' : ' is-review'}" href="${urlOf(item)}"><div><small>${label}</small>${freshBadge(item)}<strong>${titleOf(item)}</strong><p>${summaryOf(item)}</p></div>${imageMarkup(item, 'te-rel-bordered-image')}</a>`;
      }).join('')}</div></section>`;
    }

    function bento(rows) {
      const main = rows[0];
      if (!main) return '';
      return `<section class="te-rel-module te-rel-bento">${moduleHeader('DESTACADO', 'Una lectura para continuar')}<a class="te-rel-bento-main" href="${urlOf(main)}">${imageMarkup(main, 'te-rel-bento-main-image')}<span class="te-rel-bento-shade" aria-hidden="true"></span><div><small>${metaOf(main)}</small>${freshBadge(main)}<strong>${titleOf(main)}</strong><span>Ver contenido →</span></div></a><div class="te-rel-bento-compact">${rows.slice(1, 3).map(item => `<a href="${urlOf(item)}">${imageMarkup(item, 'te-rel-bento-thumb')}<div><small>${metaOf(item)}</small>${freshBadge(item)}<strong>${titleOf(item)}</strong></div><b aria-hidden="true">→</b></a>`).join('')}</div></section>`;
    }

    function frameless(rows) {
      if (!rows.length) return '';
      return `<section class="te-rel-module te-rel-frameless">${moduleHeader('LECTURA EDITORIAL', 'Historias que amplían el tema')}<div class="te-rel-frameless-grid">${rows.slice(0, 3).map(item => `<a href="${urlOf(item)}">${imageMarkup(item, 'te-rel-frameless-image')}<div><small>${metaOf(item)}</small>${freshBadge(item)}<strong>${titleOf(item)}</strong><p>${summaryOf(item)}</p><b aria-hidden="true">→</b></div></a>`).join('')}</div></section>`;
    }

    function ranking(rows) {
      if (!rows.length) return '';
      return `<section class="te-rel-module te-rel-ranking">${moduleHeader('SELECCIÓN TE EQUIPAMOS', 'Para seguir leyendo')}<div class="te-rel-ranking-list">${rows.slice(0, 3).map((item, index) => `<a href="${urlOf(item)}"><span>${String(index + 1).padStart(2, '0')}</span><div><small>${metaOf(item)}</small>${freshBadge(item)}<strong>${titleOf(item)}</strong></div><b aria-hidden="true">→</b></a>`).join('')}</div></section>`;
    }

    const primarySection = normalize(asArray(current && current.sections)[0] || current && current.category);
    const primaryRows = related.slice(0, 4);
    const secondaryRows = related.slice(4, 8).length ? related.slice(4, 8) : related.slice(0, 4);
    let modules;
    if (primarySection === 'reviews') modules = [bento(primaryRows), ranking(secondaryRows)];
    else if (primarySection === 'ventas') modules = [zigzag(primaryRows), bordered(secondaryRows)];
    else if (primarySection === 'ofertas') modules = [bordered(primaryRows), zigzag(secondaryRows)];
    else if (primarySection === 'consejos') modules = [frameless(primaryRows), ranking(secondaryRows)];
    else if (primarySection === 'novedades') modules = [frameless(primaryRows), zigzag(secondaryRows)];
    else if (primarySection === 'vídeos' || primarySection === 'videos') modules = [bento(primaryRows), frameless(secondaryRows)];
    else modules = [zigzag(primaryRows), ranking(secondaryRows)];

    const block = document.createElement('section');
    block.className = 'te-related';
    block.innerHTML = `<div class="te-related-wrap"><div class="te-related-title"><span>TE EQUIPAMOS</span><h2>Sigue explorando</h2><p>Contenido seleccionado según el producto o artículo que estás viendo.</p></div><div class="te-rel-modules">${modules.filter(Boolean).join('')}</div><a class="te-related-more" href="${BASE}">Ver todo en Te Equipamos →</a></div>`;
    mount(block);
  } catch (error) {
    console.warn('Te Equipamos related content:', error);
  }
});

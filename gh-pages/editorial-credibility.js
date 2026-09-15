document.addEventListener('DOMContentLoaded', async function () {
  try {
    if (location.pathname.includes('/news/')) return;
    const BASE = '/te-equipamos-arpenaz-27l/news/';
    const response = await fetch(BASE + 'news-data.json', { cache: 'no-store' });
    if (!response.ok) return;
    const items = await response.json();
    if (!Array.isArray(items) || !items.length) return;

    const norm = value => String(value || '').replace(/\/$/, '').toLowerCase();
    const esc = value => String(value ?? '').replace(/[&<>"']/g, ch => ({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'
    }[ch]));
    const current = items.find(item => norm(item && item.url) === norm(location.origin + location.pathname));
    if (!current || !current.owned || document.querySelector('.te-credibility-strip')) return;

    const section = String((current.sections || [])[0] || current.category || 'Te Equipamos') === 'Ventas'
      ? 'Productos'
      : String((current.sections || [])[0] || current.category || 'Te Equipamos');
    const activityLabels = {
      senderismo:'Senderismo', trekking:'Trekking', running:'Running', 'trail-running':'Trail running',
      ciclismo:'Ciclismo', natacion:'Natación', travel:'Travel', alpinismo:'Alpinismo', escalada:'Escalada',
      camping:'Camping', esqui:'Esquí y nieve', kayak:'Kayak y remo', surf:'Surf', fitness:'Fitness', urbano:'Urbano'
    };
    const activities = (current.activities || []).slice(0, 2).map(value => activityLabels[String(value).toLowerCase()] || String(value).replace(/-/g,' '));
    let published = '';
    if (current.published) {
      const date = new Date(current.published);
      if (!Number.isNaN(date.getTime())) {
        published = new Intl.DateTimeFormat('es-ES', {day:'numeric', month:'long', year:'numeric'}).format(date);
      }
    }

    const strip = document.createElement('section');
    strip.className = 'te-credibility-strip';
    strip.innerHTML = `<div class="te-credibility-wrap">
      <div class="te-credibility-copy">
        <span>CONTENIDO PROPIO</span>
        <strong>Te Equipamos</strong>
        <p>${esc(section)}${activities.length ? ' · ' + esc(activities.join(' · ')) : ''}</p>
      </div>
      <div class="te-credibility-actions">
        ${published ? `<small>Publicado ${esc(published)}</small>` : ''}
        <a href="${BASE}metodologia/">Cómo trabajamos →</a>
      </div>
    </div>`;

    const footer = document.querySelector('footer');
    if (footer && footer.parentNode) footer.parentNode.insertBefore(strip, footer);
    else document.body.appendChild(strip);
  } catch (error) {
    console.warn('Te Equipamos editorial credibility:', error);
  }
});

document.addEventListener('DOMContentLoaded', async function () {
  try {
    const response = await fetch('/te-equipamos-arpenaz-27l/news/news-data.json');
    if (!response.ok) return;
    const items = await response.json();
    if (!Array.isArray(items) || !items.length) return;

    const here = (location.origin + location.pathname).replace(/\/$/, '').toLowerCase();
    const current = items.find(x => String(x.url || '').replace(/\/$/, '').toLowerCase() === here);
    const footer = document.querySelector('footer');

    if (current) {
      const engage = document.createElement('section');
      engage.className = 'te-engage';
      engage.innerHTML = '<div class="te-engage-wrap"><div class="te-share-strip" aria-label="Compartir esta ficha"><button type="button" class="te-social te-social-wa" data-social="whatsapp" aria-label="Compartir por WhatsApp" title="WhatsApp"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11.7 11.7 0 0 0 12.1 0C5.6 0 .3 5.3.3 11.8c0 2.1.6 4.2 1.6 6L0 24l6.4-1.7a11.8 11.8 0 0 0 5.7 1.5h.1C18.7 23.8 24 18.5 24 12c0-3.2-1.2-6.2-3.5-8.5ZM12.2 21.8h-.1a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.8 1 1-3.7-.2-.4a9.7 9.7 0 0 1-1.5-5.3A9.9 9.9 0 0 1 12.1 2c2.6 0 5.1 1 7 2.9a9.8 9.8 0 0 1 2.9 7c0 5.5-4.4 9.9-9.8 9.9Zm5.4-7.4c-.3-.2-1.8-.9-2.1-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-.9 1.2-.2.2-.4.2-.7.1-1.7-.8-2.8-1.5-3.9-3.4-.3-.6.3-.5.8-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.7-.6-.6-.9-.6h-.7c-.2 0-.6.1-.9.4-.3.4-1.2 1.2-1.2 2.9s1.3 3.4 1.4 3.6c.2.2 2.5 3.8 6 5.3.8.4 1.5.6 2 .7.9.3 1.7.3 2.3.2.7-.1 1.8-.7 2.1-1.5.3-.7.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4Z"/></svg></button><button type="button" class="te-social te-social-fb" data-social="facebook" aria-label="Compartir en Facebook" title="Facebook"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.1C24 5.4 18.6 0 12 0S0 5.4 0 12.1C0 18.1 4.4 23 10.1 24v-8.4h-3V12h3V9.3c0-3 1.8-4.7 4.6-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9V12h3.4l-.5 3.6h-2.9V24C19.6 23 24 18.1 24 12.1Z"/></svg></button><button type="button" class="te-social te-social-tg" data-social="telegram" aria-label="Compartir por Telegram" title="Telegram"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21.9 2.1 2.8 9.5c-1.3.5-1.3 1.2-.2 1.5l4.9 1.5 1.9 5.8c.2.7.1 1 .9 1 .6 0 .9-.3 1.2-.6l2.7-2.6 5.6 4.1c1 .6 1.8.3 2-.9L25 3.6c.4-1.5-.6-2.2-1.6-1.8l-1.5.3Zm-2.6 3.4-9.8 8.8-.4 4.1-1.3-4.9 11.5-8c.5-.3 1-.1 0 .7Z"/></svg></button><button type="button" class="te-social te-social-link" data-social="copy" aria-label="Copiar enlace" title="Copiar enlace"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.6 13.4a1 1 0 0 0 1.4 0l4-4a3 3 0 1 0-4.2-4.2l-2.3 2.3a1 1 0 0 1-1.4-1.4l2.3-2.3a5 5 0 1 1 7.1 7.1l-4 4a1 1 0 0 1-1.4 0 1 1 0 0 1 0-1.5Zm2.8-2.8a1 1 0 0 0-1.4 0l-4 4a3 3 0 0 0 4.2 4.2l2.3-2.3a1 1 0 1 1 1.4 1.4l-2.3 2.3a5 5 0 0 1-7.1-7.1l4-4a1 1 0 0 1 1.4 0 1 1 0 0 1 0 1.5Z"/></svg></button></div></div>';
      if (footer) footer.parentNode.insertBefore(engage, footer);
      else document.body.appendChild(engage);

      const title = String(current.title || document.title || 'Te Equipamos');
      const url = String(current.url || location.href);
      const text = 'Mira esto en Te Equipamos: ' + title;
      engage.addEventListener('click', async function (event) {
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

    const related = items
      .filter(x => String(x.url || '').replace(/\/$/, '').toLowerCase() !== here)
      .map(x => {
        const tags = (x.tags || []).map(t => String(t).toLowerCase());
        const sharedTags = tags.filter(t => currentTags.has(t)).length;
        const sharedSection = currentSections.some(s => (x.sections || []).includes(s)) ? 1 : 0;
        return {x, score: sharedTags * 10 + sharedSection * 5 + Number(x.score || 0) / 20};
      })
      .sort((a, b) => b.score - a.score)
      .slice(0, 6)
      .map(row => row.x);

    if (!related.length) return;

    const block = document.createElement('section');
    block.className = 'te-related';
    block.innerHTML = '<div class="te-related-wrap"><div class="te-related-title"><span>SIGUE DESCUBRIENDO</span><h2>También te puede interesar</h2><p>Más contenido de Te Equipamos relacionado con lo que acabas de ver.</p></div><div class="te-related-grid">' + related.map(x => '<a class="te-related-card" href="' + x.url + '"><img src="' + x.image + '" alt=""><div><span>' + (x.category || 'Te Equipamos') + '</span><h3>' + x.title + '</h3><small>' + (x.source || 'Te Equipamos') + '</small></div></a>').join('') + '</div><a class="te-related-more" href="/te-equipamos-arpenaz-27l/news/">Ver más contenido en Te Equipamos →</a></div>';

    if (footer) footer.parentNode.insertBefore(block, footer);
    else document.body.appendChild(block);
  } catch (e) {}
});
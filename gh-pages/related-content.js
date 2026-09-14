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
      engage.innerHTML = '<div class="te-engage-wrap"><div class="te-engage-copy"><span>COMPARTIR</span><h2>¿Conoces a alguien a quien le pueda interesar?</h2><p>Envíale esta ficha con su imagen, titular y enlace, o continúa descubriendo más contenido de Te Equipamos.</p></div><div class="te-engage-actions"><button type="button" id="teShareCurrent"><span class="te-share-socials"><i>W</i><i>f</i><i>M</i></span><span>Compartir en redes</span></button><a href="/te-equipamos-arpenaz-27l/news/">Seguir explorando Te Equipamos →</a></div></div>';
      if (footer) footer.parentNode.insertBefore(engage, footer);
      else document.body.appendChild(engage);

      const shareButton = engage.querySelector('#teShareCurrent');
      const originalShare = shareButton.innerHTML;
      shareButton.addEventListener('click', async function () {
        const title = String(current.title || document.title || 'Te Equipamos');
        const url = String(current.url || location.href);
        const text = 'Mira esto en Te Equipamos: ' + title;
        try {
          if (navigator.share) {
            await navigator.share({title, text, url});
            return;
          }
          if (navigator.clipboard && navigator.clipboard.writeText) {
            await navigator.clipboard.writeText(title + '\n' + url);
            shareButton.textContent = '✓ Enlace copiado';
            setTimeout(() => shareButton.innerHTML = originalShare, 1800);
            return;
          }
        } catch (err) {
          if (err && err.name === 'AbortError') return;
        }
        const area = document.createElement('textarea');
        area.value = title + '\n' + url;
        area.style.position = 'fixed';
        area.style.opacity = '0';
        document.body.appendChild(area);
        area.select();
        document.execCommand('copy');
        area.remove();
        shareButton.textContent = '✓ Enlace copiado';
        setTimeout(() => shareButton.innerHTML = originalShare, 1800);
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
(function(){
  'use strict';
  const bar = document.createElement('div');
  bar.className = 'te-page-reading-progress';
  bar.setAttribute('aria-hidden','true');
  document.body.appendChild(bar);
  let ticking = false;
  function update(){
    ticking = false;
    const footer = document.querySelector('footer');
    const end = footer ? footer.offsetTop : document.documentElement.scrollHeight;
    const max = end - window.innerHeight;
    if (max < window.innerHeight * .65) {
      bar.classList.remove('show');
      bar.style.transform = 'scaleX(0)';
      return;
    }
    const ratio = Math.max(0, Math.min(1, window.scrollY / max));
    bar.style.transform = `scaleX(${ratio})`;
    bar.classList.add('show');
  }
  function schedule(){ if (ticking) return; ticking = true; requestAnimationFrame(update); }
  window.addEventListener('scroll', schedule, {passive:true});
  window.addEventListener('resize', schedule, {passive:true});
  schedule();
})();

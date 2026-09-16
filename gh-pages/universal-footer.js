(function(){
  'use strict';

  const HOME='https://jorgesport.github.io/te-equipamos/';
  const LINKS=[
    ['Cómo trabajamos',HOME+'news/metodologia/'],
    ['Anúnciate',HOME+'news/anunciate/'],
    ['Media Kit',HOME+'news/media-kit/'],
    ['Privacidad',HOME+'news/privacidad/'],
    ['Cookies',HOME+'news/cookies/']
  ];

  if(!customElements.get('te-equipamos-footer')){
    customElements.define('te-equipamos-footer',class extends HTMLElement{
      connectedCallback(){
        if(this.shadowRoot)return;
        const root=this.attachShadow({mode:'open'});
        const year=new Date().getFullYear();
        const nav=LINKS.map(([label,url])=>`<a href="${url}">${label}</a>`).join('');
        root.innerHTML=`
          <style>
            :host{display:block;clear:both;color-scheme:light;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}
            *{box-sizing:border-box}
            footer{margin:0;background:#F7F6F2;color:#1D1D1F;border-top:1px solid #DDDCD7}
            .wrap{max-width:1180px;margin:0 auto;padding:44px 28px 34px}
            .brand{display:inline-block;color:#1D1D1F;text-decoration:none;font-size:28px;line-height:1;font-weight:780;letter-spacing:-.045em}
            .brand:focus-visible,.links a:focus-visible{outline:2px solid #355345;outline-offset:4px;border-radius:3px}
            .tagline{max-width:560px;margin:15px 0 0;color:#6C6B67;font-size:15px;line-height:1.55}
            .links{display:flex;flex-wrap:wrap;gap:14px 30px;margin-top:32px}
            .links a{color:#6C6B67;text-decoration:none;font-size:15px;line-height:1.35;transition:color .18s ease}
            .links a:hover{color:#355345}
            .bottom{display:flex;align-items:center;justify-content:space-between;gap:20px;margin-top:34px;padding-top:20px;border-top:1px solid #E5E3DE;color:#8A8882;font-size:12px;line-height:1.4}
            .signature{color:#6C6B67}
            @media(max-width:680px){
              .wrap{padding:36px 22px 28px}
              .brand{font-size:25px}
              .tagline{font-size:14px}
              .links{gap:13px 22px;margin-top:28px}
              .links a{font-size:14px}
              .bottom{align-items:flex-start;flex-direction:column;gap:7px;margin-top:28px}
            }
          </style>
          <footer aria-label="Te Equipamos">
            <div class="wrap">
              <a class="brand" href="${HOME}" aria-label="Ir a Te Equipamos">Te Equipamos</a>
              <p class="tagline">Outdoor, producto y contenido útil para elegir mejor.</p>
              <nav class="links" aria-label="Información de Te Equipamos">${nav}</nav>
              <div class="bottom"><span>© ${year} Te Equipamos</span><span class="signature">Contenido, producto y aventura.</span></div>
            </div>
          </footer>`;
      }
    });
  }

  function install(){
    if(document.querySelector('te-equipamos-footer'))return;
    const footers=[...document.querySelectorAll('footer')];
    const current=footers.length?footers[footers.length-1]:null;
    const universal=document.createElement('te-equipamos-footer');
    universal.setAttribute('data-te-universal-footer','');
    if(current)current.replaceWith(universal);
    else document.body.appendChild(universal);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();

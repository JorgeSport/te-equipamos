(function(){
  'use strict';

  const HOME='https://jorgesport.github.io/te-equipamos/';
  const LOGO=HOME+'logo-te-equipamos.png';
  const NEWSLETTER_CSS=HOME+'newsletter.css';
  const NEWSLETTER_JS=HOME+'newsletter.js';
  const LINKS=[
    ['Cómo trabajamos',HOME+'news/metodologia/'],
    ['Anúnciate',HOME+'news/anunciate/'],
    ['Media Kit',HOME+'news/media-kit/'],
    ['Privacidad',HOME+'news/privacidad/'],
    ['Cookies',HOME+'news/cookies/']
  ];

  function isMainHub(){
    const p=(location.pathname.replace(/\/+$/,'')||'/')+'/';
    return p==='/te-equipamos/' || p.startsWith('/te-equipamos/news/');
  }

  function installBrandStyles(){
    if(document.querySelector('style[data-te-universal-brand-style]'))return;
    const style=document.createElement('style');
    style.setAttribute('data-te-universal-brand-style','');
    style.textContent=`
      .te-universal-brand-link{display:inline-flex!important;align-items:center!important;justify-content:flex-start!important;flex:0 0 auto!important;line-height:0!important;text-decoration:none!important;color:inherit!important;min-width:0!important}
      .te-universal-brand-link:focus-visible{outline:2px solid #355345!important;outline-offset:4px!important;border-radius:3px!important}
      .te-universal-brand-image{display:block!important;width:auto!important;height:32px!important;max-width:min(190px,44vw)!important;object-fit:contain!important;object-position:left center!important}
      .te-universal-brand-link[data-te-brand-dark="true"] .te-universal-brand-image{filter:invert(1) brightness(1.08)}
      @media(max-width:680px){.te-universal-brand-image{height:27px!important;max-width:42vw!important}}
    `;
    document.head.appendChild(style);
  }

  function parseBackground(value){
    if(!value || value==='transparent')return null;
    const m=value.match(/rgba?\(([^)]+)\)/i);
    if(!m)return null;
    const parts=m[1].split(',').map(v=>Number.parseFloat(v.trim()));
    if(parts.length<3 || parts.some((n,i)=>i<3 && !Number.isFinite(n)))return null;
    if(parts.length>3 && parts[3]<0.12)return null;
    return parts.slice(0,3);
  }

  function isDarkAround(el){
    let node=el;
    while(node && node!==document.documentElement){
      const rgb=parseBackground(getComputedStyle(node).backgroundColor);
      if(rgb){
        const [r,g,b]=rgb;
        const luminance=(0.2126*r)+(0.7152*g)+(0.0722*b);
        return luminance<118;
      }
      node=node.parentElement;
    }
    return false;
  }

  function findBrandTarget(){
    const preferred=[
      'header a.brand','nav a.brand','.site-header a.brand',
      'header .brand','nav .brand','.site-header .brand',
      'header a.logo','nav a.logo','.site-header a.logo',
      'header .logo','nav .logo','.site-header .logo'
    ];
    for(const selector of preferred){
      const el=document.querySelector(selector);
      if(el)return el;
    }
    const img=document.querySelector('header img[alt*="Equipamos" i],nav img[alt*="Equipamos" i],.site-header img[alt*="Equipamos" i]');
    if(img)return img.closest('a')||img;
    const candidates=[...document.querySelectorAll('header a,header div,header span,nav a,nav div,nav span,.site-header a,.site-header div,.site-header span')];
    return candidates.find(el=>el.children.length===0 && el.textContent.trim().toUpperCase()==='TE EQUIPAMOS')||null;
  }

  function installBrand(){
    if(isMainHub() || document.documentElement.hasAttribute('data-te-brand-disabled'))return;
    installBrandStyles();
    const target=findBrandTarget();
    if(!target)return;

    let link;
    if(target.tagName==='A'){
      link=target;
    }else if(target.tagName==='IMG' && target.closest('a')){
      link=target.closest('a');
    }else{
      link=document.createElement('a');
      while(target.firstChild)target.removeChild(target.firstChild);
      target.appendChild(link);
    }

    link.href=HOME;
    link.setAttribute('aria-label','Te Equipamos, ir al inicio');
    link.classList.add('te-universal-brand-link');
    link.removeAttribute('target');
    link.removeAttribute('rel');

    // Blindaje contra estilos heredados de botones de cada landing.
    // Algunas cabeceras antiguas aplican fondo, padding y radio a todos los enlaces del nav.
    // El logo universal debe conservar siempre su aspecto limpio.
    [['background','transparent'],['background-color','transparent'],['padding','0'],['border','0'],['border-radius','0'],['box-shadow','none'],['min-height','0']].forEach(([prop,value])=>{
      link.style.setProperty(prop,value,'important');
    });

    let img=link.querySelector('img');
    if(!img){
      img=document.createElement('img');
      link.replaceChildren(img);
    }
    img.src=LOGO;
    img.alt='Te Equipamos';
    img.decoding='async';
    img.classList.add('te-universal-brand-image');
    img.addEventListener('error',()=>{
      link.textContent='TE EQUIPAMOS';
      link.style.lineHeight='1';
      link.style.fontWeight='800';
      link.style.letterSpacing='-.04em';
    },{once:true});

    const dark=isDarkAround(link);
    link.dataset.teBrandDark=dark?'true':'false';
    img.style.setProperty('filter',dark?'invert(1) brightness(1.08)':'none','important');
  }

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
            footer{margin:0;background:#F1F1EF;color:#1D1D1F;border-top:1px solid #DDDCD7}
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

  function installFooter(){
    if(document.querySelector('te-equipamos-footer'))return;
    const footers=[...document.querySelectorAll('footer')];
    const current=footers.length?footers[footers.length-1]:null;
    const universal=document.createElement('te-equipamos-footer');
    universal.setAttribute('data-te-universal-footer','');
    if(current)current.replaceWith(universal);
    else document.body.appendChild(universal);
  }

  function installNewsletterAssets(){
    if(isMainHub())return;
    if(!document.querySelector('link[data-te-newsletter-style]')){
      const link=document.createElement('link');
      link.rel='stylesheet';
      link.href=NEWSLETTER_CSS;
      link.setAttribute('data-te-newsletter-style','');
      document.head.appendChild(link);
    }
    if(!document.querySelector('script[data-te-newsletter-loader]')){
      const script=document.createElement('script');
      script.src=NEWSLETTER_JS;
      script.defer=true;
      script.setAttribute('data-te-newsletter-loader','');
      document.head.appendChild(script);
    }
  }

  function install(){
    installBrand();
    installFooter();
    installNewsletterAssets();
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();

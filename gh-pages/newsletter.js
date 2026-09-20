(function(){
  'use strict';

  const CONFIG_URL='https://jorgesport.github.io/te-equipamos/newsletter-config.json';
  const NEWS_DATA_URL='https://jorgesport.github.io/te-equipamos/news/news-data.json';

  const normalizeUrl=value=>String(value||'').toLowerCase().replace(/\/$/,'');
  const escapeHtml=value=>String(value??'').replace(/[&<>"']/g,ch=>({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'
  }[ch]));

  async function loadJson(url){
    const response=await fetch(url,{credentials:'same-origin',cache:'no-store'});
    if(!response.ok)throw new Error('request-failed');
    return response.json();
  }

  function isHubHome(){
    const path=location.pathname.replace(/\/+$/,'/');
    return path==='/te-equipamos/' || path==='/te-equipamos/news/' || path==='/';
  }

  async function allowedPlacement(config){
    if(isHubHome())return (config.placements||[]).includes('hub_home');

    let items=[];
    try{items=await loadJson(NEWS_DATA_URL);}catch(_){return false;}
    if(!Array.isArray(items))return false;

    const here=normalizeUrl(location.origin+location.pathname);
    const current=items.find(item=>normalizeUrl(item.url)===here);
    if(!current)return false;

    const sections=Array.isArray(current.sections)?current.sections.map(x=>String(x).toLowerCase()):[];
    const excluded=(config.excluded_sections||[]).map(x=>String(x).toLowerCase());
    if(sections.some(section=>excluded.includes(section)))return false;

    return (config.placements||[]).includes('editorial');
  }

  function render(config){
    if(document.querySelector('[data-te-newsletter]'))return;
    const copy=config.copy||{};
    const section=document.createElement('section');
    section.className='te-newsletter';
    section.dataset.teNewsletter='true';
    section.innerHTML=`
      <div class="te-newsletter__card">
        <div>
          <span class="te-newsletter__eyebrow">${escapeHtml(copy.eyebrow||'TE EQUIPAMOS')}</span>
          <h2>${escapeHtml(copy.title||'Recibe las novedades de Te Equipamos')}</h2>
          <p>${escapeHtml(copy.text||'Nuevos productos, reviews, ofertas y consejos directamente en tu correo.')}</p>
          <small class="te-newsletter__legal">Suscripción con confirmación por email. Puedes darte de baja cuando quieras. <a href="${escapeHtml(config.privacy_url||'#')}">Privacidad</a>.</small>
        </div>
        <a class="te-newsletter__cta" href="${escapeHtml(config.form_url)}" target="_blank" rel="noopener noreferrer sponsored">${escapeHtml(copy.cta||'Quiero suscribirme')}</a>
      </div>`;

    const footer=document.querySelector('footer');
    if(footer&&footer.parentNode)footer.parentNode.insertBefore(section,footer);
    else document.body.appendChild(section);
  }

  async function install(){
    try{
      const config=await loadJson(CONFIG_URL);
      if(!config || config.enabled!==true || !String(config.form_url||'').trim())return;
      if(config.double_opt_in_required!==true)return;
      if(!await allowedPlacement(config))return;
      render(config);
    }catch(error){
      console.warn('Te Equipamos newsletter:',error);
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();

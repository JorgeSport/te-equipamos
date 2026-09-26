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
    const type=String(current.type||'').toLowerCase();
    const commercial=sections.some(section=>['ventas','ofertas'].includes(section))
      || ['sale','offer','product'].includes(type)
      || current.direct===true;

    if(commercial)return (config.placements||[]).includes('commercial');
    return (config.placements||[]).includes('editorial');
  }

  function ensureKlaviyo(config){
    const key=String(config.klaviyo_public_key||'').trim();
    if(!key)return;
    window._klOnsite=window._klOnsite||[];
    if(document.querySelector('script[data-te-klaviyo]'))return;
    const script=document.createElement('script');
    script.async=true;
    script.dataset.teKlaviyo='true';
    script.src='https://static.klaviyo.com/onsite/js/'+encodeURIComponent(key)+'/klaviyo.js';
    document.head.appendChild(script);
  }

  function openKlaviyoForm(config){
    const formId=String(config.klaviyo_form_id||'').trim();
    if(!formId)return false;
    window._klOnsite=window._klOnsite||[];
    window._klOnsite.push(['openForm',formId]);
    return true;
  }

  function render(config){
    if(document.querySelector('[data-te-newsletter]'))return;
    const copy=config.copy||{};
    const section=document.createElement('section');
    section.className='te-newsletter';
    section.dataset.teNewsletter='true';
    const chips=Array.isArray(copy.chips)?copy.chips.slice(0,4):['Ofertas','Reviews','Consejos'];

    const action='<button class="te-newsletter__cta" type="button" data-te-klaviyo-trigger>'+escapeHtml(copy.cta||'Quiero suscribirme')+'</button>';

    section.innerHTML=`
      <div class="te-newsletter__card">
        <div class="te-newsletter__content">
          <span class="te-newsletter__eyebrow">${escapeHtml(copy.eyebrow||'TE EQUIPAMOS')}</span>
          <h2>${escapeHtml(copy.title||'Lo nuevo de Te Equipamos, directo a tu correo')}</h2>
          <p>${escapeHtml(copy.text||'Nuevos productos, reviews, ofertas y consejos seleccionados para seguir disfrutando del outdoor.')}</p>
          <div class="te-newsletter__chips" aria-label="Contenido de la suscripción">
            ${chips.map(chip=>`<span class="te-newsletter__chip">${escapeHtml(chip)}</span>`).join('')}
          </div>
          <small class="te-newsletter__legal">Suscripción con doble confirmación. Puedes darte de baja cuando quieras. <a href="${escapeHtml(config.privacy_url||'#')}">Privacidad</a>.</small>
        </div>
        <div class="te-newsletter__action">
          <span class="te-newsletter__icon" aria-hidden="true">
            <svg viewBox="0 0 24 24"><path d="M4 6.5h16v11H4z"/><path d="m4.5 7 7.5 6 7.5-6"/></svg>
          </span>
          <strong>${escapeHtml(copy.action_title||'Recibe solo lo que merece la pena abrir.')}</strong>
          ${action}
          <span class="te-newsletter__trust">Doble confirmación · Baja cuando quieras</span>
        </div>
      </div>`;

    const trigger=section.querySelector('[data-te-klaviyo-trigger]');
    if(trigger)trigger.addEventListener('click',()=>openKlaviyoForm(config));

    function placeBeforeFooter(){
      const footer=document.querySelector('te-equipamos-footer,[data-te-universal-footer],#teBusinessFooter,footer');
      if(footer&&footer.parentNode){
        if(section.parentNode!==footer.parentNode || section.nextElementSibling!==footer){
          footer.parentNode.insertBefore(section,footer);
        }
        return true;
      }
      return false;
    }
    if(!placeBeforeFooter()){
      document.body.appendChild(section);
      const observer=new MutationObserver(()=>{
        if(placeBeforeFooter())observer.disconnect();
      });
      observer.observe(document.body,{childList:true,subtree:true});
      setTimeout(()=>observer.disconnect(),2500);
    }
  }

  async function install(){
    try{
      const config=await loadJson(CONFIG_URL);
      if(!config || config.enabled!==true)return;
      if(config.double_opt_in_required!==true)return;
      if(String(config.provider||'').toLowerCase()!=='klaviyo')return;
      if(!String(config.klaviyo_public_key||'').trim() || !String(config.klaviyo_form_id||'').trim())return;
      if(!await allowedPlacement(config))return;

      ensureKlaviyo(config);
      render(config);
    }catch(error){
      console.warn('Te Equipamos newsletter:',error);
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();

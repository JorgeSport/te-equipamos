(function(){
  'use strict';

  const HOME='https://jorgesport.github.io/te-equipamos/';
  const WHATSAPP='51920807184';

  function productName(){
    return (document.documentElement.dataset.teProduct||document.querySelector('meta[name="te:product"]')?.content||document.title||'este producto').trim();
  }

  function track(event,props={}){
    const payload={event,...props,ts:Date.now()};
    window.teDataLayer=window.teDataLayer||[];
    window.teDataLayer.push(payload);
    document.dispatchEvent(new CustomEvent('te:analytics',{detail:payload}));
  }

  function bindWhatsApp(){
    const product=productName();
    document.querySelectorAll('[data-te-whatsapp]').forEach(link=>{
      const message=(link.dataset.teMessage||`Hola, quiero información sobre ${product}.`).trim();
      link.href=`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(message)}`;
      link.target='_blank';
      link.rel='noopener';
      link.addEventListener('click',()=>track('contact_click',{
        channel:'whatsapp',
        product,
        page_location:location.href
      }));
    });
  }

  function bindShare(){
    document.querySelectorAll('[data-te-share]').forEach(button=>{
      button.addEventListener('click',async()=>{
        const data={title:document.title,text:document.querySelector('meta[name="description"]')?.content||'',url:location.href};
        try{
          if(navigator.share)await navigator.share(data);
          else if(navigator.clipboard)await navigator.clipboard.writeText(location.href);
          track('share_click',{product:productName(),page_location:location.href});
        }catch(err){
          if(err?.name!=='AbortError')console.warn('Te Equipamos: no se pudo compartir',err);
        }
      });
    });
  }

  function install(){
    bindWhatsApp();
    bindShare();
    track('page_view',{
      product:productName(),
      page_title:document.title,
      page_location:location.href,
      source:'te-landing-template'
    });
  }

  window.TeEquipamosLanding=Object.freeze({HOME,WHATSAPP,track});

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();

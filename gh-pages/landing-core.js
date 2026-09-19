(function(){
  'use strict';

  const HOME='https://jorgesport.github.io/te-equipamos/';
  const WHATSAPP='51920807184';

  function productName(){
    return (document.documentElement.dataset.teProduct||document.querySelector('meta[name="te:product"]')?.content||document.title||'este producto').trim();
  }

  function productPrice(){
    return (document.querySelector('meta[name="te:price"]')?.content||'').trim();
  }

  function productUrl(){
    return location.href;
  }

  function priceUpdatedDate(){
    const value=(document.querySelector('meta[name="te:price-updated"]')?.content||'').trim();
    if(!value||/REEMPLAZAR_/i.test(value))return '';
    const match=value.match(/^(\d{4})-(\d{2})-(\d{2})$/);
    return match?`${match[3]}/${match[2]}/${match[1]}`:value;
  }

  function installPriceReference(root=document){
    const price=productPrice();
    if(!price||/REEMPLAZAR_/i.test(price))return;

    let targets=[...root.querySelectorAll('[data-te-price]')];
    if(!targets.length)targets=[...root.querySelectorAll('.price')];

    const updated=priceUpdatedDate();
    targets.forEach(target=>{
      if(target.dataset.tePriceReferenceBound==='true')return;
      target.dataset.tePriceReferenceBound='true';

      const note=document.createElement('div');
      note.className='te-price-reference';
      note.setAttribute('role','note');
      note.innerHTML='<span>Precio referencial sujeto a cambios y disponibilidad. Confirma el precio final antes de realizar tu compra.</span>'+
        (updated?`<small>Precio actualizado: ${updated}</small>`:'');
      target.insertAdjacentElement('afterend',note);
    });
  }

  function track(event,props={}){
    const payload={event,...props,ts:Date.now()};
    window.teDataLayer=window.teDataLayer||[];
    window.teDataLayer.push(payload);
    document.dispatchEvent(new CustomEvent('te:analytics',{detail:payload}));
  }

  function defaultWhatsAppMessage(){
    const product=productName();
    const price=productPrice();
    const pricePart=price?` Precio: ${price}.`:'';
    return `Hola Te Equipamos, deseo consultar por ${product}.${pricePart} Quisiera confirmar disponibilidad.\n\nEnlace del producto: ${productUrl()}`;
  }

  function messageWithProductLink(message){
    const clean=String(message||'').trim();
    if(!clean)return defaultWhatsAppMessage();
    if(/REEMPLAZAR_/i.test(clean))return defaultWhatsAppMessage();
    if(/Enlace del producto:/i.test(clean))return clean;
    return `${clean}\n\nEnlace del producto: ${productUrl()}`;
  }

  function buildWhatsAppUrl(message){
    return `https://wa.me/${WHATSAPP}?text=${encodeURIComponent(messageWithProductLink(message))}`;
  }

  function refreshWhatsApp(root=document){
    const product=productName();
    root.querySelectorAll('[data-te-whatsapp]').forEach(link=>{
      const custom=(link.dataset.teMessage||'').trim();
      link.href=buildWhatsAppUrl(custom||defaultWhatsAppMessage());
      link.target='_blank';
      link.rel='noopener';
      if(link.dataset.teWhatsappBound==='true')return;
      link.dataset.teWhatsappBound='true';
      link.addEventListener('click',()=>track('contact_click',{
        channel:'whatsapp',
        product,
        page_location:location.href
      }));
    });
  }

  function sharePayload(){
    const product=productName();
    return {
      title:document.title,
      text:`Mira esto en Te Equipamos: ${product}`,
      url:productUrl()
    };
  }

  async function share(action='native'){
    const data=sharePayload();
    const channel=String(action||'native').toLowerCase();
    try{
      if(channel==='whatsapp'){
        window.open(`https://wa.me/?text=${encodeURIComponent(data.text+'\n'+data.url)}`,'_blank','noopener,noreferrer');
      }else if(channel==='facebook'){
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(data.url)}`,'_blank','noopener,noreferrer');
      }else if(channel==='telegram'){
        window.open(`https://t.me/share/url?url=${encodeURIComponent(data.url)}&text=${encodeURIComponent(data.text)}`,'_blank','noopener,noreferrer');
      }else if(channel==='copy'){
        if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(`${data.title}\n${data.url}`);
      }else if(navigator.share){
        await navigator.share(data);
      }else if(navigator.clipboard?.writeText){
        await navigator.clipboard.writeText(`${data.title}\n${data.url}`);
      }
      track('share_click',{channel,product:productName(),page_location:location.href});
    }catch(err){
      if(err?.name!=='AbortError')console.warn('Te Equipamos: no se pudo compartir',err);
    }
  }

  function bindShare(){
    document.querySelectorAll('[data-te-share]').forEach(button=>{
      if(button.dataset.teShareBound==='true')return;
      button.dataset.teShareBound='true';
      button.addEventListener('click',event=>{
        event.preventDefault();
        share(button.dataset.teShare||'native');
      });
    });
  }

  function install(){
    refreshWhatsApp();
    bindShare();
    installPriceReference();
    track('page_view',{
      product:productName(),
      page_title:document.title,
      page_location:location.href,
      source:'te-landing-template'
    });
  }

  window.TeEquipamosLanding=Object.freeze({
    HOME,
    WHATSAPP,
    track,
    productName,
    productPrice,
    priceUpdatedDate,
    installPriceReference,
    buildWhatsAppUrl,
    refreshWhatsApp,
    share
  });

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install,{once:true});
  else install();
})();

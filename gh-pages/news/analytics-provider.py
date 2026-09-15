from pathlib import Path

NEWS = Path(__file__).resolve().parent
ROOT = NEWS.parent

loader = r'''(function(){
  const CONFIG='/te-equipamos-arpenaz-27l/news/analytics-config.json';
  function injectStyle(){if(document.getElementById('teConsentStyle'))return;const s=document.createElement('style');s.id='teConsentStyle';s.textContent='.teConsent{position:fixed;z-index:220;left:50%;bottom:max(14px,env(safe-area-inset-bottom));transform:translateX(-50%);width:min(720px,calc(100vw - 24px));background:#181B18;color:#F5F5F2;border:1px solid #303630;border-radius:18px;padding:16px 17px;box-shadow:0 22px 70px rgba(0,0,0,.3);font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}.teConsent strong{display:block;font-size:14px;margin-bottom:4px}.teConsent p{margin:0;color:#C6CBC5}.teConsentActions{display:flex;gap:8px;justify-content:flex-end;margin-top:12px}.teConsent button{border:0;border-radius:999px;min-height:40px;padding:0 14px;font:inherit;font-weight:800;cursor:pointer}.teConsentReject{background:transparent;color:#D9DDD8;border:1px solid #434A43!important}.teConsentAccept{background:#A6B9AD;color:#111310}@media(max-width:560px){.teConsentActions{display:grid;grid-template-columns:1fr 1fr}.teConsent button{width:100%}}';document.head.appendChild(s)}
  function banner(onAccept,onReject){injectStyle();if(document.getElementById('teConsent'))return;const el=document.createElement('aside');el.id='teConsent';el.className='teConsent';el.setAttribute('role','dialog');el.setAttribute('aria-label','Preferencias de analítica');el.innerHTML='<strong>Ayúdanos a mejorar Te Equipamos</strong><p>Podemos activar medición de uso y rendimiento. No se carga el proveedor de analítica hasta que aceptes.</p><div class="teConsentActions"><button class="teConsentReject" type="button">Rechazar</button><button class="teConsentAccept" type="button">Aceptar analítica</button></div>';document.body.appendChild(el);el.querySelector('.teConsentAccept').onclick=()=>{localStorage.setItem('teAnalyticsConsent','granted');el.remove();onAccept()};el.querySelector('.teConsentReject').onclick=()=>{localStorage.setItem('teAnalyticsConsent','denied');el.remove();onReject&&onReject()}}
  function validGa(id){return /^G-[A-Z0-9]+$/i.test(String(id||''))}
  function loadGa4(id){
    if(!validGa(id)||window.__teGaLoaded)return;window.__teGaLoaded=true;
    window.dataLayer=window.dataLayer||[];window.gtag=window.gtag||function(){window.dataLayer.push(arguments)};
    window.gtag('js',new Date());window.gtag('consent','update',{analytics_storage:'granted'});window.gtag('config',id,{send_page_view:false,anonymize_ip:true});
    const s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(id);document.head.appendChild(s);
    const send=p=>{if(!p||!p.event)return;const props={...p};delete props.event;delete props.ts;window.gtag('event',p.event,props)};
    (window.teDataLayer||[]).forEach(send);document.addEventListener('te:analytics',e=>send(e.detail));
  }
  fetch(CONFIG,{cache:'no-store'}).then(r=>r.ok?r.json():null).then(c=>{
    if(!c||c.enabled!==true)return;
    if(c.provider!=='ga4'||!validGa(c.measurement_id))return;
    if(c.requires_consent===false){loadGa4(c.measurement_id);return}
    const choice=localStorage.getItem('teAnalyticsConsent');
    if(choice==='granted')loadGa4(c.measurement_id);else if(choice!=='denied')banner(()=>loadGa4(c.measurement_id));
  }).catch(()=>{});
})();'''
(ROOT / 'te-analytics-provider.js').write_text(loader, encoding='utf-8')

tag = '<script defer id="teAnalyticsProvider" src="/te-equipamos-arpenaz-27l/te-analytics-provider.js"></script>'
count=0
for page in ROOT.rglob('index.html'):
    txt=page.read_text(encoding='utf-8')
    low=txt.lower()
    if 'noindex' in low or '<meta http-equiv="refresh"' in low or 'te-business-analytics.js' not in txt:
        continue
    if 'id="teAnalyticsProvider"' not in txt and '</body>' in txt:
        txt=txt.replace('</body>',tag+'</body>',1)
        page.write_text(txt,encoding='utf-8')
        count+=1

print(f'Proveedor de analítica preparado con consentimiento: {count} páginas listas; permanece inactivo hasta configurar GA4')

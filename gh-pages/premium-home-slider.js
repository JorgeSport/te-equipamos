
(function(){
  'use strict';
  let index=0,timer=null;

  function escHtml(v){
    return String(v==null?'':v).replace(/[&<>"']/g,function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c];
    });
  }
  function items(){
    if(typeof NEWS==='undefined'||!Array.isArray(NEWS))return [];
    const pool=NEWS.slice().sort(function(a,b){
      return ((b.featured?1:0)-(a.featured?1:0))||((b.score||0)-(a.score||0));
    });
    const seen=new Set(),out=[];
    pool.forEach(function(n){
      const key=String(n.url||n.title||n.id||'');
      if(!key||seen.has(key)||out.length>=5)return;
      seen.add(key);out.push(n);
    });
    return out;
  }
  function label(n){
    if(typeof cardLabel==='function')return cardLabel(n);
    return (n.sections&&n.sections[0])||n.category||'Te Equipamos';
  }
  function title(n){
    if(typeof cardTitle==='function')return cardTitle(n);
    return n.card_title||n.title||'Te Equipamos';
  }
  function meta(n){
    if(typeof cardMeta==='function')return cardMeta(n);
    return '';
  }
  function fresh(n){
    if(typeof freshBadge==='function')return freshBadge(n);
    return '';
  }
  function media(n){
    const video=String(n.video_url||n.video||'').trim();
    if(video){
      return '<video muted playsinline preload="metadata" poster="'+escHtml(n.image||'')+'" aria-label="'+escHtml(n.title||'')+'"><source src="'+escHtml(video)+'"></video>';
    }
    return '<img src="'+escHtml(n.image||'')+'" alt="'+escHtml(n.title||'')+'" loading="eager">';
  }
  function restart(){
    const root=document.getElementById('hero');
    if(!root)return;
    clearTimeout(timer);
    root.classList.remove('isPlaying');
    const reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(reduce||root.matches(':hover')||root.contains(document.activeElement))return;
    requestAnimationFrame(function(){root.classList.add('isPlaying');});
    timer=setTimeout(function(){show(index+1);},6000);
  }
  function show(i){
    const root=document.getElementById('hero');
    if(!root)return;
    const slides=[].slice.call(root.querySelectorAll('.teHeroSlide'));
    const dots=[].slice.call(root.querySelectorAll('.teHeroDot'));
    if(!slides.length)return;
    index=(i+slides.length)%slides.length;
    slides.forEach(function(el,j){
      el.classList.toggle('isActive',j===index);
      el.setAttribute('aria-hidden',j===index?'false':'true');
      const v=el.querySelector('video');
      if(v){if(j===index){v.currentTime=0;v.play().catch(function(){});}else{v.pause();}}
    });
    dots.forEach(function(el,j){
      el.classList.toggle('isActive',j===index);
      el.setAttribute('aria-current',j===index?'true':'false');
    });
    const counter=root.querySelector('.teHeroCounter');
    if(counter)counter.textContent=(index+1)+' / '+slides.length;
    restart();
  }
  function render(){
    const root=document.getElementById('hero');
    const data=items();
    if(!root||!data.length)return;
    root.className='teHeroSlider';
    root.setAttribute('aria-label','Destacados de Te Equipamos');

    const slides=data.map(function(n,i){
      const own=n.owned?' · Te Equipamos':'';
      return '<article class="teHeroSlide '+(i===0?'isActive':'')+'" aria-hidden="'+(i===0?'false':'true')+'">'+
        '<div class="teHeroMedia" data-article="'+escHtml(n.id)+'">'+media(n)+'</div>'+
        '<div class="teHeroContent">'+
          '<span class="teHeroEyebrow">'+escHtml(label(n))+own+'</span>'+
          '<h2 class="teHeroTitle"><a href="?id='+escHtml(n.id)+'" data-article="'+escHtml(n.id)+'">'+escHtml(title(n))+'</a></h2>'+
          '<p class="teHeroSummary">'+escHtml(n.summary||'')+'</p>'+
          '<div class="teHeroMeta">'+escHtml(meta(n))+fresh(n)+'</div>'+
          '<a class="teHeroAction" href="?id='+escHtml(n.id)+'" data-article="'+escHtml(n.id)+'">Ver contenido →</a>'+
        '</div>'+
      '</article>';
    }).join('');

    const dots=data.map(function(_,i){
      return '<button class="teHeroDot '+(i===0?'isActive':'')+'" type="button" data-hero-dot="'+i+'" aria-label="Ir al destacado '+(i+1)+'" aria-current="'+(i===0?'true':'false')+'"></button>';
    }).join('');

    root.innerHTML='<div class="teHeroStage">'+slides+'</div>'+
      '<div class="teHeroControls"><div class="teHeroArrows">'+
      '<button class="teHeroArrow" type="button" data-hero-prev aria-label="Anterior">‹</button>'+
      '<button class="teHeroArrow" type="button" data-hero-next aria-label="Siguiente">›</button>'+
      '</div><div class="teHeroDots">'+dots+'<span class="teHeroCounter">1 / '+data.length+'</span></div></div>'+
      '<div class="teHeroProgress"><span></span></div>';

    root.addEventListener('mouseenter',function(){clearTimeout(timer);root.classList.remove('isPlaying');});
    root.addEventListener('mouseleave',restart);
    root.addEventListener('focusin',function(){clearTimeout(timer);root.classList.remove('isPlaying');});
    root.addEventListener('focusout',function(){setTimeout(restart,0);});
    index=0;restart();
  }

  document.addEventListener('click',function(e){
    const prev=e.target.closest&&e.target.closest('[data-hero-prev]');
    if(prev){e.preventDefault();show(index-1);return;}
    const next=e.target.closest&&e.target.closest('[data-hero-next]');
    if(next){e.preventDefault();show(index+1);return;}
    const dot=e.target.closest&&e.target.closest('[data-hero-dot]');
    if(dot){e.preventDefault();show(Number(dot.getAttribute('data-hero-dot')||0));}
  },true);

  function boot(){setTimeout(render,0);}
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot,{once:true});
  else boot();
})();

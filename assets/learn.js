(() => {
  'use strict';
  const ko = document.documentElement.lang === 'ko';
  const t = (en, kr) => ko ? kr : en;
  const storeKey = 'players-codex-start-v1';
  const updateQuery = pairs => {
    const url = new URL(location.href);
    pairs.forEach(([key,value]) => value ? url.searchParams.set(key,value) : url.searchParams.delete(key));
    history.replaceState(null,'',url);
    const lang = document.querySelector('.lang');
    if (lang) { const other = new URL(lang.href); other.search = url.search; other.hash = url.hash; lang.href = other.href; }
  };
  document.querySelector('[data-layout-route]')?.addEventListener('change', event => {
    const base = document.body.dataset.base;
    for (const [title, prefix] of [['English mobile preview',''],['Korean mobile preview','ko/']]) {
      document.querySelector(`iframe[title="${title}"]`).src = base + prefix + event.target.value;
    }
  });
  const journey = document.querySelector('[data-journey]');
  if (journey) {
    const buttons = [...journey.querySelectorAll('[data-journey-stage]')];
    const checks = [...journey.querySelectorAll('[data-start-task]')];
    let completed = [];
    try { const saved = JSON.parse(localStorage.getItem(storeKey) || '[]'); if (Array.isArray(saved)) completed = saved.filter(x => typeof x === 'string'); } catch { /* Storage is optional. */ }
    checks.forEach(input => { input.checked = completed.includes(input.dataset.startTask); });
    function progress() {
      journey.querySelector('[data-start-progress]').textContent = t(`${checks.filter(c => c.checked).length} / ${checks.length} checked`, `${checks.filter(c => c.checked).length} / ${checks.length} 완료`);
    }
    function select(key) {
      buttons.forEach(b => b.setAttribute('aria-pressed',String(b.dataset.journeyStage === key)));
      journey.querySelectorAll('[data-journey-panel]').forEach(p => { p.hidden = p.dataset.journeyPanel !== key; });
      updateQuery([['step',key]]);
    }
    const stage = new URLSearchParams(location.search).get('step');
    if (buttons.some(b => b.dataset.journeyStage === stage)) select(stage);
    buttons.forEach(b => b.addEventListener('click',() => select(b.dataset.journeyStage)));
    function save() { progress(); try { localStorage.setItem(storeKey,JSON.stringify(checks.filter(c=>c.checked).map(c=>c.dataset.startTask))); } catch { journey.querySelector('[data-start-progress]').textContent += t(' · this visit only',' · 이번 방문에만 저장'); } }
    checks.forEach(input=>input.addEventListener('change',save));
    journey.querySelector('[data-reset-start]')?.addEventListener('click',()=>{checks.forEach(c=>{c.checked=false;}); save();});
    progress();
  }
  // One visible explanation per selection, all explanations remain in the HTML.
  function picker(container, buttonAttr, panelAttr) {
    const area=document.querySelector(container); if (!area) return;
    const buttons=[...area.querySelectorAll(`[${buttonAttr}]`)];
    buttons.forEach(b=>b.addEventListener('click',()=>{
      buttons.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
      area.querySelectorAll(`[${panelAttr}]`).forEach(p=>{p.hidden=p.getAttribute(panelAttr)!==b.getAttribute(buttonAttr);});
    }));
  }
  picker('[data-item-reader]','data-item-part','data-item-panel');
  picker('[data-stats]','data-stat','data-stat-panel');
  picker('[data-maps]','data-map-goal','data-map-goal-panel');
  const maps=document.querySelector('[data-maps]');
  if (maps) {
    const zone=maps.querySelector('[data-map-zone]');
    const options=[...zone.options];
    const frame=maps.querySelector('[data-map-frame]');
    const query=new URLSearchParams(location.search);
    const requested=options.find(o=>o.value===query.get('zone'));
    let faction=requested?.dataset.faction || (query.get('faction')==='asmodian'?'asmodian':'elyos');
    zone.value=requested?.value || (faction==='elyos'?'Poeta':'Ishalgen');
    function render() {
      options.forEach(o=>{o.hidden=o.dataset.faction!==faction;o.disabled=o.hidden;});
      maps.querySelectorAll('button[data-faction]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.faction===faction)));
      const src=`https://aion2.th.gl/embed/maps/${encodeURIComponent(zone.value)}`;
      if (frame.getAttribute('src')!==src) frame.src=src;
      frame.title=t('Interactive AION 2 map — ','아이온 2 인터랙티브 지도 — ')+zone.selectedOptions[0].textContent.split(' · ')[0];
      maps.querySelector('[data-map-external]').href=`https://aion2.th.gl/maps/${encodeURIComponent(zone.value)}`;
      maps.querySelector('[data-map-route]').textContent=faction==='elyos'?t('Elyos  /  Poeta → Verteron','천족  /  포에타 → 베르테론'):t('Asmodian  /  Ishalgen → Altgard','마족  /  이스할겐 → 알트가르드');
      updateQuery([['faction',faction],['zone',zone.value]]);
    }
    maps.querySelectorAll('button[data-faction]').forEach(b=>b.addEventListener('click',()=>{faction=b.dataset.faction;zone.value=faction==='elyos'?'Poeta':'Ishalgen';render();}));
    zone.addEventListener('change',render);
    render();
  }
  const library=document.querySelector('[data-skill-library]');
  if (library) {
    const cls=library.querySelector('[data-skill-class-filter]');
    const search=library.querySelector('[data-skill-search-input]');
    const cards=[...library.querySelectorAll('.skill-card')];
    const q=new URLSearchParams(location.search);
    cls.value=[...cls.options].some(o=>o.value===q.get('class'))?q.get('class'):'all';
    search.value=q.get('q')||'';
    function filter() {
      const term=search.value.trim().toLocaleLowerCase();let count=0;
      cards.forEach(c=>{c.hidden=!( (cls.value==='all'||c.dataset.skillClass===cls.value) && (!term||c.dataset.skillSearch.toLocaleLowerCase().includes(term)));if(!c.hidden)count++;});
      library.querySelector('[data-skill-count]').textContent=t(`${count} skills`,`${count}개 스킬`);
      library.querySelector('[data-skill-empty]').hidden=count!==0;
      updateQuery([['class',cls.value==='all'?'':cls.value],['q',search.value]]);
    }
    cls.addEventListener('change',filter);search.addEventListener('input',filter);filter();
  }
  const dialog=document.querySelector('[data-skill-dialog]');
  if (dialog && typeof dialog.showModal==='function') {
    const data=JSON.parse(document.getElementById('skill-data').textContent);
    let opener;
    document.addEventListener('click',event=>{
      const link=event.target.closest('a[data-skill]');
      if (!link||!data[link.dataset.skill]||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0) return;
      event.preventDefault();opener=link;
      dialog.querySelector('[data-skill-content]').innerHTML=data[link.dataset.skill];
      dialog.showModal();dialog.scrollTop=0;dialog.querySelector('[data-close-skill]').focus();
    });
    dialog.querySelector('[data-close-skill]').addEventListener('click',()=>dialog.close());
    dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
    dialog.addEventListener('close',()=>{opener?.focus();});
  }
  const media=[...document.querySelectorAll('[data-mechanic-media]')];
  function stop(box) {
    const mount=box.querySelector('[data-media-mount]');
    mount.replaceChildren();mount.hidden=true;
    box.querySelector('[data-video-start]').hidden=false;
    box.querySelector('[data-stop-media]').hidden=true;
  }
  function prepare(box) {
    media.forEach(stop);
    box.querySelector('[data-video-start]').hidden=true;
    box.querySelector('[data-stop-media]').hidden=false;
    const mount=box.querySelector('[data-media-mount]');mount.hidden=false;return mount;
  }
  function play(box) {
    const trigger=box.querySelector('[data-video-start]');
    const mount=prepare(box);const frame=document.createElement('iframe');
    frame.src=`https://www.youtube-nocookie.com/embed/${trigger.dataset.videoId}?start=${trigger.dataset.videoStart}&autoplay=1&rel=0&playsinline=1`;
    frame.title=trigger.getAttribute('aria-label');
    frame.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';frame.allowFullscreen=true;
    frame.referrerPolicy='strict-origin-when-cross-origin';mount.append(frame);
  }
  media.forEach(box=>{
    box.querySelector('[data-video-start]').addEventListener('click',()=>play(box));
    box.querySelector('[data-replay-video]').addEventListener('click',()=>play(box));
    box.querySelector('[data-stop-media]').addEventListener('click',()=>{stop(box);box.querySelector('[data-video-start]').focus();});
    box.querySelector('[data-kr-clip]')?.addEventListener('click',event=>{
      const mount=prepare(box);const img=document.createElement('img');img.src=event.currentTarget.dataset.krClip;
      img.alt=t('Original KR gameplay loop — Nirr / Inven','한국판 실제 플레이 반복 장면 — Nirr / 인벤');
      img.addEventListener('error',()=>{mount.textContent=t('Clip could not load. Use the linked source or YouTube chapter.','장면을 불러오지 못했어요. 원문 또는 YouTube 챕터를 이용하세요.');});mount.append(img);
    });
  });
  document.addEventListener('codex:mechanic-change',()=>media.filter(box=>box.closest('[hidden]')).forEach(stop));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)media.forEach(stop);});
})();

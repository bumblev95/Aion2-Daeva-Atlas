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
  const dialog=document.querySelector('[data-skill-dialog]');
  if (dialog && typeof dialog.showModal==='function') {
    const data=JSON.parse(document.getElementById('skill-data').textContent);
    let opener;
    document.addEventListener('click',event=>{
      const link=event.target.closest('a[data-skill]');
      if (!link||!data[link.dataset.skill]||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0) return;
      event.preventDefault();opener=link;
      dialog.querySelector('[data-skill-content]').innerHTML=data[link.dataset.skill];
      document.dispatchEvent(new CustomEvent("codex:skill-open",{detail:dialog}));dialog.showModal();dialog.scrollTop=0;dialog.querySelector('[data-close-skill]').focus();
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

  });
  document.addEventListener('codex:mechanic-change',()=>media.filter(box=>box.closest('[hidden]')).forEach(stop));
  document.addEventListener('visibilitychange',()=>{if(document.hidden)media.forEach(stop);});
})();

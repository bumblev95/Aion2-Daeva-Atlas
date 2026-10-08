(() => {
  'use strict';
  const ko = document.documentElement.lang === 'ko';
  document.addEventListener('keydown', e => { if(e.key === '/' && !e.ctrlKey && !e.metaKey && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName) && !document.activeElement.isContentEditable) { const target=document.querySelector('.header-search');if(target){e.preventDefault();location.href=target.href;} } });
  document.querySelectorAll('.toc a').forEach(a=>a.addEventListener('click',()=>{const d=document.querySelector(a.getAttribute('href'));if(d?.tagName==='DETAILS')d.open=true;}));
  const t = (en, kr) => ko ? kr : en;
  const base = document.body.dataset.base;
  document.querySelector('[data-clear-local]')?.addEventListener('click',()=>{try{localStorage.removeItem('players-codex-dps-v1');}catch{}});
  const sideTools = document.querySelector('.side-bottom');
  if (sideTools) {
    const prefix=base+(ko?'ko/':'');
    [['updates/',t('News & patch changes','뉴스·패치 변경사항')],['tools/dps/',t('Build & eDPS calculator','빌드·eDPS 계산기')],['screenshots/',t('Gameplay screenshots','인게임 스크린샷')]].forEach(([route,label])=>{
      const a=document.createElement('a');a.href=prefix+route;a.textContent=label;
      if(location.pathname===a.pathname||(route==='updates/'&&location.pathname.startsWith(a.pathname)))a.setAttribute('aria-current','page');
      sideTools.append(a);
    });
  }
  const menu = document.querySelector('[data-menu]');
  const sidebar = document.querySelector('#main-nav');
  const backdrop = document.querySelector('[data-menu-close]');
  const narrow = window.matchMedia('(max-width: 850px)');
  function setMenu(open, focus = false) {
    if (!menu || !sidebar) return;
    menu.setAttribute('aria-expanded', String(open));
    sidebar.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    if (backdrop) backdrop.hidden = !open;
    if (focus) (open ? sidebar.querySelector('a') : menu)?.focus();
  }
  menu?.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true', true));
  backdrop?.addEventListener('click', () => setMenu(false, true));
  sidebar?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  narrow.addEventListener?.('change', () => setMenu(false));
  document.addEventListener('keydown', e => {
    if (menu?.getAttribute('aria-expanded') !== 'true') return;
    if (e.key === 'Escape') { e.preventDefault(); setMenu(false, true); }
    if (e.key === 'Tab') {
      const stops = [menu, ...sidebar.querySelectorAll('a[href]')];
      const i = stops.indexOf(document.activeElement);
      if (e.shiftKey && i <= 0) { e.preventDefault(); stops.at(-1).focus(); }
      if (!e.shiftKey && (i === stops.length - 1 || i < 0)) { e.preventDefault(); menu.focus(); }
    }
  });
  // All three sections remain readable without JavaScript. Enhance into URL-aware tabs.
  const hub = document.querySelector('[data-guide-hub]');
  if (hub) {
    const tabs = [...hub.querySelectorAll('[data-guide-tab]')];
    const panels = [...hub.querySelectorAll('[data-guide-view]')];
    hub.querySelector('[data-guide-tabs]').setAttribute('role', 'tablist');
    tabs.forEach(tab => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels.find(p => p.dataset.guideView === tab.dataset.guideTab).id);
    });
    panels.forEach(panel => { panel.setAttribute('role', 'tabpanel'); panel.tabIndex = 0; });
    function selectView(key) {
      if (!panels.some(p => p.dataset.guideView === key)) key = 'basics';
      panels.forEach(p => p.hidden = p.dataset.guideView !== key);
      tabs.forEach(tab => {
        const selected = tab.dataset.guideTab === key;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
      });
    }
    function syncView() {
      let id = '';
      try { id = decodeURIComponent(location.hash.slice(1)); } catch {}
      const target = id ? document.getElementById(id) : null;
      const panel = target?.closest('[data-guide-view]');
      const params = new URLSearchParams(location.search);
      selectView(panel?.dataset.guideView || params.get('view') || (params.has('step') ? 'growth' : 'basics'));
      const detail = target?.closest('details');
      if (detail) detail.open = true;
      // An anchor may have been hidden at the instant the browser tried to scroll.
      if (target) requestAnimationFrame(() => target.scrollIntoView?.({block:'start'}));
      const other = document.querySelector('.lang');
      if (other) { const u = new URL(other.href); u.search = location.search; u.hash = location.hash; other.href = u.href; }
    }
    function activate(tab) {
      const u = new URL(location.href);
      u.searchParams.set('view', tab.dataset.guideTab);
      u.hash = tab.hash;
      history.pushState(null, '', u);
      syncView();
    }
    tabs.forEach((tab, i) => {
      tab.addEventListener('click', e => { if(e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return; e.preventDefault(); activate(tab); });
      tab.addEventListener('keydown', e => {
        let next;
        if (e.key === 'ArrowRight') next = (i + 1) % tabs.length;
        if (e.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
        if (e.key === 'Home') next = 0;
        if (e.key === 'End') next = tabs.length - 1;
        if (next !== undefined) { e.preventDefault(); tabs[next].focus(); activate(tabs[next]); }
        if (e.key === ' ') { e.preventDefault(); activate(tab); }
      });
    });
    window.addEventListener('hashchange', syncView);
    window.addEventListener('popstate', syncView);
    syncView();
  }
  const filters = document.querySelectorAll('[data-class-filter]');
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
    const chosen = button.dataset.classFilter;
    let count = 0;
    document.querySelectorAll('[data-class-card]').forEach(card => {
      card.hidden = chosen !== 'all' && card.dataset.role !== chosen;
      if (!card.hidden) count++;
    });
    const status = document.querySelector('[data-filter-status]');
    if (status) status.textContent = t(`${count} classes shown`,`${count}개 직업 표시`);
  }));
  const glossary = document.querySelector('[data-glossary-search]');
  if (glossary) glossary.addEventListener('input', () => {
    const query = glossary.value.normalize('NFKC').toLowerCase().trim();
    let count = 0;
    document.querySelectorAll('[data-term]').forEach(row => {
      row.hidden = !row.textContent.normalize('NFKC').toLowerCase().includes(query);
      if (!row.hidden) count++;
    });
    document.querySelector('[data-glossary-count]').textContent = t(`${count} terms`,`${count}개 용어`);
    document.querySelector('[data-glossary-empty]').hidden = count > 0;
  });
  const search = document.querySelector('[data-site-search]');
  if (search) {
    const output = document.querySelector('[data-search-results]');
    const status = document.querySelector('[data-search-status]');
    let index = [];
    const render = () => {
      const query = search.value.normalize('NFKC').toLowerCase().trim();
      const matches = index.filter(r => r.lang === (ko ? 'ko':'en') && (!query || `${r.title} ${r.description} ${r.keywords}`.normalize('NFKC').toLowerCase().includes(query)));
      output.replaceChildren();
      status.textContent = t(`${matches.length} results`,`${matches.length}개 결과`);
      if (!matches.length) {
        const p = document.createElement('p'); p.className='no-results';p.textContent=t('No results. Try a class name, “PvP”, or “Korean”.','검색 결과가 없습니다. 직업명, PvP, 한국 등으로 검색해보세요.');output.append(p);return;
      }
      matches.forEach(r => {
        const a=document.createElement('a');a.className='result';a.style.display='block';a.href=base+r.path+(r.anchor?'#'+encodeURIComponent(r.anchor):'');
        const tag=document.createElement('span');tag.className='tag';tag.textContent=r.category;
        const h=document.createElement('h2');h.textContent=r.title;
        const p=document.createElement('p');p.textContent=r.description;
        a.append(tag,h,p);output.append(a);
      });
    };
    search.disabled=true;
    fetch(base+'search-index.json').then(r=>{if(!r.ok)throw Error('index');return r.json();}).then(data=>{
      index=data;search.disabled=false;
      search.value=new URLSearchParams(location.search).get('q')||'';render();
      search.addEventListener('input',render);
      document.querySelector('[data-search-form]').addEventListener('submit',e=>{e.preventDefault();const u=new URL(location.href);if(search.value)u.searchParams.set('q',search.value);else u.searchParams.delete('q');history.replaceState(null,'',u);render();});
    }).catch(()=>{status.textContent=t('Search could not load. Use the Guides or Classes navigation to browse every page.','검색을 불러오지 못했습니다. 공략·직업 메뉴에서 모든 글을 볼 수 있습니다.');});
  }
  const comparison = document.querySelector('[data-comparison]');
  if (comparison) {
    const data=JSON.parse(document.querySelector('#class-data').textContent);
    const selects=[document.querySelector('#class-a'),document.querySelector('#class-b')];
    const query=new URLSearchParams(location.search);
    selects.forEach((s,i)=>{const v=query.get(i===0?'a':'b');if(data.some(c=>c.id===v))s.value=v;});
    const label=(key)=>({tank:t('Tank','탱커'),healer:t('Healer','회복'),support:t('Support','지원'),damage:t('Damage','공격'),melee:t('Melee','근접'),ranged:t('Ranged','원거리')}[key]);
    const render=()=>{
      comparison.replaceChildren();
      selects.forEach(s=>{
        const c=data.find(v=>v.id===s.value); const panel=document.createElement('section');panel.className='compare-panel';
        const title=document.createElement('h2');title.textContent=ko?c.ko:c.en;
        const tag=document.createElement('span');tag.className='tag';tag.textContent=`${label(c.role)} · ${label(c.range)}`;panel.append(tag,title);const art=document.createElement('div');art.className='compare-visual';const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 48 48');svg.setAttribute('class','icon');svg.setAttribute('aria-hidden','true');const use=document.createElementNS(svg.namespaceURI,'use');use.setAttribute('href',base+'assets/icons.svg#'+c.icon);svg.append(use);art.append(svg);panel.append(art);
        [[t('Playstyle','플레이스타일'),c.identity],[t('A good fit if…','이런 분에게'),c.fit],[t('Consider the trade-off','고려할 점'),c.trade],[t('Try this first','첫 연습'),c.practice]].forEach(([name,text])=>{const h=document.createElement('h3');h.textContent=name;const p=document.createElement('p');p.textContent=text[ko?1:0];panel.append(h,p);});
        const a=document.createElement('a');a.className='text-link';a.href=base+(ko?'ko/':'')+'classes/'+c.id+'/';a.textContent=t('Read the class guide →','직업 가이드 읽기 →');panel.append(a);comparison.append(panel);
      });
      const u=new URL(location.href);u.searchParams.set('a',selects[0].value);u.searchParams.set('b',selects[1].value);history.replaceState(null,'',u);
      const languageLink=document.querySelector('.lang');
      if(languageLink){const translated=new URL(languageLink.href);translated.search=u.search;languageLink.href=translated.href;}
      document.querySelector('[data-compare-status]').textContent=selects[0].value===selects[1].value?t('Both selections are the same. Choose another class to compare.','같은 직업을 선택했습니다. 다른 직업과 비교해보세요.'):t('Comparison updated.','비교를 업데이트했습니다.');
    };
    selects.forEach(s=>s.addEventListener('change',render));render();
    const share=document.querySelector('[data-share]');
    share.addEventListener('click',async()=>{const status=document.querySelector('[data-share-status]');try{await navigator.clipboard.writeText(location.href);status.textContent=t('Link copied','링크를 복사했습니다');}catch{status.textContent=t('Copy the current URL from your address bar.','주소창의 현재 주소를 복사하세요.');}});
  }
  const planner=document.querySelector('[data-planner]');
  if(planner){
    const KEY='daeva-atlas-planner-v1';
    const status=document.querySelector('[data-planner-status]');
    const defaults=[['Confirm my region, faction and server','지역·종족·서버 확인하기'],['Check controls and party visibility','조작과 파티 정보 표시 확인하기'],['Practise one familiar encounter','익숙한 전투 한 가지 연습하기'],['Write one goal for the next session','다음 접속 목표 하나 적기']];
    const initial=()=>defaults.map((v,i)=>({id:'default-'+i,text:v,done:false}));
    let tasks=initial();let canSave=true;
    try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(Array.isArray(saved)&&saved.length<=50&&saved.every(x=>x&&typeof x.id==='string'&&typeof x.done==='boolean'&&(typeof x.text==='string'||(Array.isArray(x.text)&&x.text.length===2&&x.text.every(v=>typeof v==='string')))))tasks=saved;}
    catch{canSave=false;status.textContent=t('Browser storage unavailable. Your list will only last for this visit.','브라우저 저장소를 사용할 수 없어 이번 방문에만 유지됩니다.');}
    const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(tasks));canSave=true;status.textContent=t('Saved on this browser','이 브라우저에 저장했습니다');}catch{canSave=false;status.textContent=t('Could not save. Export your list before leaving.','저장하지 못했습니다. 나가기 전에 목록을 내보내세요.');}};
    const render=()=>{
      const list=document.querySelector('[data-task-list]');list.replaceChildren();
      tasks.forEach((task,i)=>{
        const row=document.createElement('div');row.className='task'+(task.done?' completed':'');
        const input=document.createElement('input');input.type='checkbox';input.checked=task.done;input.id='task-'+i;
        const label=document.createElement('label');label.htmlFor=input.id;label.textContent=Array.isArray(task.text)?task.text[ko?1:0]:task.text;
        const remove=document.createElement('button');remove.type='button';remove.className='delete-task';remove.textContent='×';remove.setAttribute('aria-label',t('Remove task: ','할 일 삭제: ')+label.textContent);
        input.addEventListener('change',()=>{task.done=input.checked;save();row.classList.toggle('completed',task.done);updateProgress();});
        remove.addEventListener('click',()=>{tasks=tasks.filter(x=>x!==task);save();render();});
        row.append(input,label,remove);list.append(row);
      });updateProgress();
    };
    function updateProgress(){const done=tasks.filter(t=>t.done).length;document.querySelector('[data-progress-text]').textContent=t(`${done} of ${tasks.length} complete`,`${tasks.length}개 중 ${done}개 완료`);document.querySelector('[data-progress-fill]').style.width=(tasks.length?done/tasks.length*100:0)+'%';}
    document.querySelector('[data-task-form]').addEventListener('submit',e=>{e.preventDefault();const input=document.querySelector('#new-task');const value=input.value.trim();if(!value)return;if(tasks.length>=50){status.textContent=t('Limit: 50 tasks. Remove a task before adding another.','최대 50개입니다. 기존 항목을 지운 뒤 추가하세요.');return;}tasks.push({id:'custom-'+Date.now()+'-'+Math.random().toString(36).slice(2,6),text:value.slice(0,160),done:false});input.value='';save();render();input.focus();});
    document.querySelector('[data-reset-checks]').addEventListener('click',()=>{tasks.forEach(x=>x.done=false);save();render();});
    document.querySelector('[data-export]').addEventListener('click',()=>{const text=tasks.map(x=>`${x.done?'[x]':'[ ]'} ${Array.isArray(x.text)?x.text[ko?1:0]:x.text}`).join('\n');const url=URL.createObjectURL(new Blob(['PLAYER’S CODEX — personal session plan\n\n'+text],{type:'text/plain;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download='players-codex-plan.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);});
    document.querySelectorAll('[data-budget]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('[data-budget]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));const total=Number(b.dataset.budget);const plan=[[5,t('Review your goal and settings','목표와 설정 확인')],[total-10,t('Practise or progress toward one chosen goal','정한 목표 하나를 연습하거나 진행')],[5,t('Record what worked and your next step','도움이 된 점과 다음 목표 기록')]];const target=document.querySelector('[data-session-plan]');target.replaceChildren();plan.forEach(([minutes,label])=>{const row=document.createElement('div');row.className='session-block';const time=document.createElement('strong');time.textContent=minutes+'′';const p=document.createElement('p');p.textContent=label;row.append(time,p);target.append(row);});}));
    render();document.querySelector('[data-budget="30"]').click();
    if(canSave)status.textContent=t('Saved only in this browser. No account needed.','이 브라우저에만 저장됩니다. 계정은 필요하지 않습니다.');
  }
  document.querySelector('[data-clear-local]')?.addEventListener('click',()=>{try{localStorage.removeItem('daeva-atlas-planner-v1');localStorage.removeItem('raidnote-aion2-class-v1');localStorage.removeItem('players-codex-start-v1');localStorage.removeItem('players-codex-map-v1');localStorage.removeItem('players-codex-lessons-v1');document.querySelector('[data-clear-status]').textContent=t('Your saved planner, lessons, map checks and class have been deleted from this browser.','이 브라우저의 저장된 플래너·학습·지도 완료 표시·직업을 삭제했습니다.');}catch{document.querySelector('[data-clear-status]').textContent=t('Use your browser settings to clear site data.','브라우저 설정에서 사이트 데이터를 삭제하세요.');}});
})();

(function () {
  'use strict';
  const root=document.querySelector('[data-news-desk]'),detail=document.querySelector('[data-news-detail]');
  if(!root&&!detail)return;
  const surface=root||detail,ko=surface.dataset.lang==='ko',t=(a,b)=>ko?b:a;
  const base=document.body.dataset.base,local=base+(ko?'ko/':'');
  const labels={buff:t('Buff','버프'),nerf:t('Nerf','너프'),adjustment:t('Adjustment','조정'),fix:t('Bug fix','버그 수정'),tooltip:t('Tooltip','툴팁 수정'),system:t('Other change','기타 변경')};
  const marks={buff:'↑',nerf:'↓',adjustment:'↔',fix:'✓',tooltip:'i',system:'•'};
  function element(tag,text,css) {const e=document.createElement(tag);if(text)e.textContent=text;if(css)e.className=css;return e;}
  function badge(kind) {kind=Object.hasOwn(labels,kind)?kind:'system';return element('span',marks[kind]+' '+labels[kind],'change-badge '+kind);}
  function officialLink(url,copy,css) {
    const u=new URL(url);
    if(u.protocol!=='https:'||u.hostname!=='aion2.plaync.com')throw new Error('Invalid notice URL');
    const a=element('a',copy,css);a.href=u.href;a.target='_blank';a.rel='noopener';return a;
  }
  function reviewLabel(x) {
    if(x.reviewState==='reviewed'&&x.detail?.coverage==='complete')return t('Full change list reviewed','전체 항목 검토 완료');
    if(x.reviewState==='reviewed')return t('Summary reviewed','요약 검토 완료');
    if(x.reviewState==='revised')return t('Source revised · reviewing','원문 수정 · 재검토 중');
    return t('Review pending','검토 중');
  }
  let running=false;
  async function fetchFeed() {
    const response=await fetch(surface.dataset.feed+'?t='+Math.floor(Date.now()/300000),{cache:'no-store',signal:AbortSignal.timeout(12000)});
    if(!response.ok)throw new Error('Feed unavailable');const data=await response.json();
    if(!Array.isArray(data.sources)||!data.checkedAt)throw new Error('Invalid feed');return data;
  }
  if(detail) {
    async function checkRevision() {
      if(running)return;running=true;
      try {
        const data=await fetchFeed(),x=data.sources.flatMap(s=>s.items||[]).find(i=>i.id===detail.dataset.itemId);
        if(x&&(x.contentHash!==detail.dataset.contentHash||x.reviewState!=='reviewed')) {
          const note=detail.querySelector('[data-detail-revision]');
          note.textContent=t('This notice has been revised. Read the current official source or reload once the new review is published.','이 공지가 수정됐습니다. 최신 공식 원문을 확인하거나 새 검토가 반영된 뒤 페이지를 새로고침하세요.');
          note.hidden=false;detail.querySelector('[data-detail-content]').hidden=true;
          detail.querySelector('.patch-detail-head>p').hidden=true;
          detail.querySelector('.review-badge').textContent=t('Source changed · reload required','원문 변경 · 새로고침 필요');
        }
      }catch{/* Keep the dated reviewed page on a connection failure. */}
      finally{running=false;}
    }
    checkRevision();setInterval(()=>{if(!document.hidden)checkRevision();},300000);return;
  }
  const q=s=>root.querySelector(s),region=q('[data-news-region]'),kind=q('[data-news-kind]'),cls=q('[data-news-class]');
  const classes=JSON.parse(document.querySelector('#pc-patch-classes').textContent);
  const query=new URLSearchParams(location.search);
  [[region,'region'],[kind,'kind'],[cls,'class']].forEach(([select,key])=>{if([...select.options].some(o=>o.value===query.get(key)))select.value=query.get(key);});
  function filter(save=false) {
    let count=0;
    root.querySelectorAll('.patch-summary').forEach(e=>{
      const ids=e.dataset.classIds.split(' '),isClass=ids.some(Boolean);
      e.hidden=!((region.value==='all'||e.dataset.region===region.value)&&(kind.value==='all'||kind.value===e.dataset.kind||(kind.value==='class'&&isClass))&&(cls.value==='all'||ids.includes(cls.value)||ids.includes('all')));
      if(!e.hidden)count++;
    });q('[data-news-empty]').hidden=count>0;
    if(save){const url=new URL(location.href);url.searchParams.set('region',region.value);url.searchParams.set('kind',kind.value);if(cls.value==='all')url.searchParams.delete('class');else url.searchParams.set('class',cls.value);history.replaceState(null,'',url);}
  }
  function card(x) {
    const groups=CodexPatch.groups(x,classes),isPatch=x.kind==='patch';
    const e=element('article',null,'patch-card patch-summary');e.dataset.region=x.region;e.dataset.kind=x.kind;e.dataset.classIds=groups.map(g=>g.classId).join(' ');e.dataset.review=x.reviewState||'pending';
    const header=element('header'),date=element('time',(x.publishedAt||'').slice(0,10));date.dateTime=x.publishedAt||'';
    header.append(element('span',x.region==='NA'?t('NA · US / Canada','북미 · 미국 / 캐나다'):t('Korea','한국'),'tag'),date,element('span',reviewLabel(x),'review-badge'));
    const h=element('h2'),url=isPatch?local+CodexPatch.detailPath(x):x.url;
    const a=isPatch?element('a',x.displayTitle?.[ko?'ko':'en']||x.title,'patch-title-link'):officialLink(x.url,x.title);
    if(isPatch)a.href=url;h.append(a);
    e.append(header,h,element('p',x.summary?.[ko?'ko':'en']||t('The new notice is awaiting an editorial review.','새 공지를 수집했습니다. 변경 내용을 검토하고 있습니다.'),'patch-summary-copy'));
    if(groups.length){
      const chips=element('div',null,'patch-impact-chips');
      groups.forEach(g=>{
        const chip=element('a',null,'patch-impact-chip');chip.href=url+'#class-'+g.classId;
        if(!['all','brawler'].includes(g.classId)){const img=element('img',null,'patch-chip-image');img.src=base+'assets/classes/'+g.classId+'.webp';img.alt='';img.width=460;img.height=920;img.loading='lazy';chip.append(img);}
        chip.append(element('strong',g.info[ko?'ko':'en']),badge(g.type));chips.append(chip);
      });e.append(chips);
    }
    const footer=element('footer');
    if(isPatch){const read=element('a',t('Read full change list','전체 패치 보기')+' →','text-link patch-read-link');read.href=url;footer.append(read);}
    else footer.append(officialLink(x.url,t('Read official notice','공식 공지 보기')+' ↗','text-link'));
    footer.append(officialLink(x.url,t('NC source','NC 원문')+' ↗','patch-source-link'));e.append(footer);return e;
  }
  async function refresh() {
    if(running)return;running=true;
    try {
      const data=await fetchFeed(),items=data.sources.flatMap(s=>s.items||[]).sort((a,b)=>(b.publishedAt||'').localeCompare(a.publishedAt||''));
      if(!items.length)throw new Error('Empty feed');
      const cards=items.map(card);q('[data-news-items]').replaceChildren(...cards);
      const failures=data.sources.filter(s=>s.status!=='ready').length;
      q('[data-news-status]').textContent=t('Source check: ','원문 확인: ')+data.checkedAt+' · '+t('hourly collection','매시간 수집')+(failures?' · '+t('Some sources unavailable; previous entries retained.','일부 원문 수집 실패 · 기존 자료 유지'):'');
      q('[data-source-health]').replaceChildren(...data.sources.map(s=>element('p',s.id+' · '+s.status+' · '+t('Last success: ','마지막 정상 확인: ')+(s.lastSuccessAt||'—'))));filter();
    }catch{q('[data-news-status]').textContent=t('Refresh failed. The previously displayed items and source dates are retained.','재확인에 실패했습니다. 표시 중인 자료와 실제 원문 날짜를 유지합니다.');}
    finally{running=false;}
  }
  [region,kind,cls].forEach(e=>e.addEventListener('change',()=>filter(true)));
  q('[data-news-refresh]').addEventListener('click',refresh);filter();
  setInterval(()=>{if(!document.hidden)refresh();},300000);
})();

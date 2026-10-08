(function () {
  'use strict';
  const root=document.querySelector('[data-news-desk]');if(!root)return;
  const ko=root.dataset.lang==='ko',t=(a,b)=>ko?b:a,q=s=>root.querySelector(s);
  const region=q('[data-news-region]'),kind=q('[data-news-kind]'),cls=q('[data-news-class]');
  let running=false;
  function element(tag,text,css) {const e=document.createElement(tag);if(text)e.textContent=text;if(css)e.className=css;return e;}
  function filter() {
    let count=0;
    root.querySelectorAll('.patch-card').forEach(e=>{
      const classes=e.dataset.classIds.split(' '),isClass=classes.some(Boolean);
      e.hidden=!((region.value==='all'||e.dataset.region===region.value)&&(kind.value==='all'||kind.value===e.dataset.kind||(kind.value==='class'&&isClass))&&(cls.value==='all'||classes.includes(cls.value)||classes.includes('all')));
      if(!e.hidden)count++;
    });q('[data-news-empty]').hidden=count>0;
  }
  function card(x) {
    const e=element('article',null,'patch-card');e.dataset.region=x.region;e.dataset.kind=x.kind;e.dataset.classIds=(x.changes||[]).map(c=>c.classId||'').join(' ');
    const header=element('header');header.append(element('span',x.region==='NA'?t('NA · US / Canada','북미 · 미국 / 캐나다'):t('Korea','한국'),'tag'),element('time',(x.publishedAt||'').slice(0,10)+' UTC'));
    header.append(element('span',x.reviewState==='reviewed'?t('Reviewed summary','요약 검토 완료'):x.reviewState==='revised'?t('Source revised · review pending','원문 수정 · 재검토 중'):t('Review pending','요약 검토 중'),'review-badge'));
    e.append(header,element('h2',x.title),element('p',x.summary?.[ko?'ko':'en']||t('New source item. Editorial summary is awaiting review.','새 원문이 수집됐습니다. 변경 요약을 검토 중입니다.')));
    const list=element('ul',null,'patch-changes');
    const labels={buff:t('Buff','버프'),nerf:t('Nerf','너프'),adjustment:t('Adjustment','조정'),fix:t('Bug fix','버그 수정'),system:t('System','시스템')};
    (x.changes||[]).forEach(c=>{const li=element('li'),copy=element('div');copy.append(element('strong',c.subject?.[ko?'ko':'en']),element('p',c.description?.[ko?'ko':'en']));li.append(element('span',labels[c.type]||t('Review','검토'),'change-badge '+(Object.hasOwn(labels,c.type)?c.type:'system')),copy);list.append(li);});e.append(list);
    if(x.classScopeReviewed&&!(x.changes||[]).some(c=>c.classId))e.append(element('p',t('No class-specific balance changes listed in this reviewed patch.','검토한 이 패치에는 클래스별 밸런스 변경이 기재되지 않았습니다.'),'class-scope'));
    const footer=element('footer'),a=element('a','NC · '+t('Original notice','공식 원문')+' ↗','text-link');
    try {const url=new URL(x.url);if(url.protocol!=='https:'||url.hostname!=='aion2.plaync.com')throw new Error('url');a.href=url.href;a.target='_blank';a.rel='noopener';footer.append(a);}catch{}
    footer.append(element('span',t('Source updated','원문 수정')+' '+(x.sourceUpdatedAt||'').slice(0,16).replace('T',' ')+' UTC'));e.append(footer);return e;
  }
  async function refresh() {
    if(running)return;running=true;
    try {
      const response=await fetch(root.dataset.feed+'?t='+Math.floor(Date.now()/300000),{cache:'no-store',signal:AbortSignal.timeout(12000)});
      if(!response.ok)throw new Error('feed');const data=await response.json();
      if(!Array.isArray(data.sources)||!data.checkedAt)throw new Error('schema');
      const items=data.sources.flatMap(s=>s.items||[]).sort((a,b)=>(b.publishedAt||'').localeCompare(a.publishedAt||''));
      if(!items.length)throw new Error('empty');
      q('[data-news-items]').replaceChildren(...items.map(card));
      const failures=data.sources.filter(s=>s.status!=='ready').length;
      q('[data-news-status]').textContent=t('Source check: ','원문 확인: ')+data.checkedAt+' · '+t('hourly collection','매시간 수집')+(failures?' · '+t('Some sources unavailable; last successful entries retained.','일부 원문 수집 실패 · 기존 자료 유지'):'');
      q('[data-source-health]').replaceChildren(...data.sources.map(s=>element('p',s.id+' · '+s.status+' · '+t('Last success: ','마지막 정상 확인: ')+(s.lastSuccessAt||'—'))));filter();
    }catch {q('[data-news-status]').textContent=t('Refresh failed. The previously displayed items and source dates are retained.','재확인에 실패했습니다. 표시 중인 자료와 실제 원문 날짜를 유지합니다.');}
    finally {running=false;}
  }
  [region,kind,cls].forEach(e=>e.addEventListener('change',filter));
  q('[data-news-refresh]').addEventListener('click',refresh);filter();
  setInterval(()=>{if(!document.hidden)refresh();},300000);
})();

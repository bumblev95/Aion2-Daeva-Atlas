(function () {
  'use strict';
  const root = document.querySelector('[data-dps-lab]');
  if (!root) return;
  const ko = root.dataset.lang === 'ko', t = (a,b) => ko ? b : a, q = s => root.querySelector(s);
  const form = q('[data-dps-form]'), tbody = q('[data-dps-skills]'), error = q('[data-dps-error]');
  const format = n => new Intl.NumberFormat(ko?'ko-KR':'en-US',{maximumFractionDigits:1}).format(n);
  const esc = x => String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let db, current, custom=0, comparisons=[], result, input, dirty=false, latestFeed, activeSnapshot;
  const param = key => q('[data-param="'+key+'"]');
  try {
    const saved=JSON.parse(localStorage.getItem('players-codex-dps-v1')||'[]');
    if(Array.isArray(saved))comparisons=saved.slice(0,8).filter(x=>x?.input&&Array.isArray(x.input.skills)&&x.input.skills.length<=40);
  } catch { comparisons=[]; }
  function saveComparisons() {try{localStorage.setItem('players-codex-dps-v1',JSON.stringify(comparisons));}catch{/* The calculator remains usable without browser storage. */}}
  function fail(message) {error.textContent=message; error.hidden=!message;}
  function numeric(key,value,min,max,step='any') {
    return '<input type="number" data-skill-param="'+key+'" value="'+esc(value)+'" min="'+min+'" max="'+max+'" step="'+step+'" aria-label="'+esc(key)+'" required>';
  }
  function row(s,manual=false) {
    const el=document.createElement('tr');el.dataset.id=s.id;el.dataset.name=s[ko?'ko':'en']||s.name;
    el.innerHTML='<td><input type="checkbox" data-enabled checked aria-label="'+esc(t('Include skill','스킬 사용'))+'"><button type="button" data-up aria-label="'+esc(t('Move skill up','우선순위 올리기'))+'">↑</button><button type="button" data-down aria-label="'+esc(t('Move skill down','우선순위 내리기'))+'">↓</button><button type="button" data-remove aria-label="'+esc(t('Remove skill','스킬 삭제'))+'">×</button></td><th scope="row">'+(s.icon?'<img src="'+esc(s.icon)+'" width="30" height="30" alt="" loading="lazy">':'')+(manual?'<input data-custom-name value="'+esc(el.dataset.name)+'" maxlength="60" aria-label="'+esc(t('Custom skill name','직접 추가한 스킬 이름'))+'">':'<a href="'+esc(s.url)+'" target="_blank" rel="noopener">'+esc(el.dataset.name)+'</a>')+'</th><td>'+numeric('flat',s.flat,0,100000000)+'</td><td>'+numeric('coefficient',s.coefficient,0,100000)+'</td><td>'+numeric('hits',s.hits,1,1000,'1')+'</td><td>'+numeric('cast',s.cast,.05,120)+'</td><td>'+numeric('cooldown',s.cooldown,0,3600)+'</td><td>'+numeric('delta',0,-100,1000)+'</td><td>'+numeric('afterCooldown',s.cooldown,0,3600)+'</td>';
    tbody.append(el);
  }
  function loadClass() {
    if(!db)return;
    current=db.classes.find(c=>c.id===q('[data-dps-class]').value);
    tbody.replaceChildren();dirty=false;
    activeSnapshot={sourceHash:db.sourceHash,sourceDate:db.sourceDate,model:db.version};
    const kr=param('region').value==='KR';
    current.skills.forEach(s=>row(kr?{...s,flat:0,coefficient:0,cooldown:0}:s));
    param('patch').value=kr?'KR / '+t('enter client reference','클라이언트 기준 직접 입력'):'Global / tooltip '+db.sourceDate;
    q('[data-dps-omitted]').textContent=t('Base-1 direct damage only. '+current.omitted+' active-skill entries, all passives, Stigmas, procs, pets and higher-level effects are not seeded. Enter your final build values and measured action time before using the result.','기본 1레벨 직접 피해만 초기 입력합니다. 액티브 '+current.omitted+'개와 패시브·스티그마·발동 효과·펫·레벨 상승 효과는 미반영입니다. 최종빌드 수치와 측정한 동작 시간을 입력해야 해당 세팅을 비교할 수 있습니다.');
    q('[data-dps-results]').replaceChildren();result=null;
    patchState();calculate();
  }
  function read() {
    const out={}; root.querySelectorAll('[data-param]').forEach(el=>out[el.dataset.param]=el.value);
    out.classId=current.id;out.sourceHash=activeSnapshot.sourceHash;out.sourceDate=activeSnapshot.sourceDate;out.model=activeSnapshot.model;
    out.name=out.name.trim()||current[ko?'ko':'en']+t(' / tooltip model',' / 툴팁 모델');
    out.skills=Array.from(tbody.rows).map(el=>{
      const s={id:el.dataset.id,name:el.querySelector('[data-custom-name]')?.value||el.dataset.name,enabled:el.querySelector('[data-enabled]').checked};
      el.querySelectorAll('[data-skill-param]').forEach(x=>s[x.dataset.skillParam]=x.value);return s;
    });return out;
  }
  function graph(events,duration) {
    if (!events.length) return '';
    const max=events[events.length-1].total||1;
    let points='0,120';
    // Sample the staircase without changing results.
    const stride=Math.max(1,Math.ceil(events.length/150));
    events.filter((e,i)=>i%stride===0||i===events.length-1).forEach(e=>points+=' '+(e.time/duration*600).toFixed(2)+','+(120-e.total/max*110).toFixed(2));
    return '<svg viewBox="0 0 600 130" role="img" aria-label="'+esc(t('Cumulative modeled damage over the fight','전투 시간별 누적 기대 피해'))+'"><path d="M0 120H600" stroke="#464b60"/><polyline points="'+points+'" fill="none" stroke="#83d8c1" stroke-width="2.5"/></svg>';
  }
  function calculate() {
    if (!db) return false;
    try {
      if (!form.checkValidity()) throw new Error('invalid form');
      input=read();const before=window.CodexDPS.simulate(input),after=window.CodexDPS.simulate(input,true);result={before,after};
      const delta=before.edps?((after.edps/before.edps-1)*100):null;
      const skillRows=before.breakdown.map((s,i)=>'<tr><th scope="row">'+esc(s.name)+'</th><td>'+s.casts+'</td><td>'+format(s.damage)+'</td><td>'+format(before.total?s.damage/before.total*100:0)+'%</td><td>'+format(after.breakdown[i].damage)+'</td></tr>').join('');
      q('[data-dps-results]').innerHTML='<h2>'+t('Calculated model result','입력 조건의 계산 결과')+'</h2><div class="dps-metrics"><div><span>eDPS</span><strong>'+format(before.edps)+'</strong><small>'+t('Whole fight denominator','전체 전투 시간 기준')+'</small></div><div><span>'+t('After scenario','변경 시나리오 eDPS')+'</span><strong>'+format(after.edps)+'</strong><small>'+(delta===null?t('No baseline damage','기준 피해 없음'):((delta>0?'+':'')+format(delta))+'%')+'</small></div><div><span>'+t('Attackable-window DPS','공격 가능 구간 DPS')+'</span><strong>'+format(before.activeDps)+'</strong><small>'+format(before.activeTime)+' / '+input.duration+'s</small></div></div>'+graph(before.events,Number(input.duration))+'<p class="small muted">'+t('Cumulative expected damage · selected inputs only','누적 기대 피해 · 선택한 입력만 계산')+'</p><div class="dps-table-scroll"><table><thead><tr>'+[t('Skill','스킬'),t('Casts','사용 횟수'),t('Damage','기대 피해'),t('Share','기여도'),t('After damage','변경 후 피해')].map(x=>'<th scope="col">'+x+'</th>').join('')+'</tr></thead><tbody>'+skillRows+'</tbody></table></div>';
      fail('');return true;
    } catch (e) {
      result=null;q('[data-dps-results]').replaceChildren();
      fail(t('Check the numeric limits and downtime format (e.g. 30-40, 90-100). Include at least one skill.','숫자 범위와 공격 불가 구간 형식(예: 30-40, 90-100)을 확인하고 스킬을 하나 이상 선택하세요.'));return false;
    }
  }
  function patchState() {
    const el=q('[data-dps-patch-state]');
    if (!latestFeed) {el.textContent=t('Patch feed unavailable. Verify the input version on the patch desk.','패치 피드 확인 전입니다. 패치 화면에서 입력 버전을 확인하세요.');return;}
    const source=latestFeed.sources.find(s=>s.region===param('region').value&&s.kind==='patch');
    const patch=source?.items?.slice().sort((a,b)=>(b.publishedAt||'').localeCompare(a.publishedAt||''))[0];
    const affected=patch?.changes?.some(c=>c.classId===current?.id||c.classId==='all');
    let message=param('region').value==='KR'?t('KR values require manual input; Global tooltip values are cleared. ','한국판은 직접 입력해야 하므로 글로벌 툴팁 수치를 비웠습니다. '):t('Input snapshot: '+activeSnapshot.sourceDate+'. ','입력 툴팁 확인일: '+activeSnapshot.sourceDate+'. ');
    const changed=activeSnapshot.sourceHash!==db.sourceHash||activeSnapshot.model!==db.version;
    if(changed) message+=t('New inputs are available. Your edits retain their original data version; change class or reload to apply the new defaults. ','새 입력 자료가 있습니다. 직접 수정한 빌드의 기존 버전을 유지했습니다. 직업 변경이나 화면 새로고침으로 최신 초기값을 적용하세요. ');
    if (source?.status!=='ready') message+=t('Source collection failed; last successful snapshot is retained. ','원문 수집 실패 · 마지막 정상 자료를 유지합니다. ');
    message+=affected||patch?.reviewState!=='reviewed'?t('Latest patch affects this class or is unreviewed. Recheck final values; no percentage was guessed.','최신 패치에 해당 직업 변경이 있거나 요약을 검토 중입니다. 최종 수치를 다시 확인해야 하며 변경률을 추정하지 않았습니다.'):t('No class-specific numerical change in the latest reviewed notice.','최근 검토한 공지에는 클래스별 수치 변경이 기재되지 않았습니다.');
    el.textContent=message;el.classList.toggle('needs-review',Boolean(changed||affected||patch?.reviewState!=='reviewed'));
  }
  function compare() {
    const area=q('[data-dps-comparisons]');
    if (!comparisons.length) {area.textContent=t('No builds added.','아직 추가한 빌드가 없습니다.');return;}
    if(!db) {area.textContent=t('Loading saved comparison…','저장한 비교 불러오는 중…');return;}
    comparisons=comparisons.filter(x=>{try{x.edps=window.CodexDPS.simulate(x.input).edps;return true;}catch{return false;}});
    if(!comparisons.length){area.textContent=t('No valid saved builds.','유효한 저장 빌드가 없습니다.');saveComparisons();return;}
    const savedList=comparisons.map((x,i)=>'<p><button type="button" class="text-link" data-dps-restore="'+i+'">'+esc(x.input.name||t('Saved build','저장 빌드'))+' · '+t('Load inputs','입력 불러오기')+'</button></p>').join('');
    if(comparisons.some(x=>x.input.sourceHash!==db.sourceHash||x.input.model!==db.version)) {area.innerHTML='<p>'+t('Saved inputs use an earlier data or calculation version. Load and review them before adding a current comparison.','저장 입력의 데이터 또는 계산 버전이 다릅니다. 입력을 불러와 검토한 후 현재 기준의 비교를 추가하세요.')+'</p>'+savedList;return;}
    const keys=new Set(comparisons.map(x=>window.CodexDPS.conditionKey(x.input)+'/'+x.input.sourceHash+'/'+x.input.model));
    if (keys.size>1) {area.innerHTML='<p>'+t('Conditions or input versions differ. Clear and add builds under identical conditions to rank them.','비교 조건 또는 입력 데이터 버전이 다릅니다. 초기화한 뒤 같은 조건으로 빌드를 추가하면 순위를 표시합니다.')+'</p>'+savedList;return;}
    if (comparisons.length<2) {area.innerHTML='<p>'+esc(comparisons[0].input.name)+' · '+format(comparisons[0].edps)+' eDPS · '+t('Add another build.','다른 빌드를 추가하세요.')+'</p>'+savedList;return;}
    const sorted=comparisons.slice().sort((a,b)=>b.edps-a.edps),best=sorted[0].edps||1;
    area.innerHTML=sorted.map((x,i)=>'<div class="dps-ranking"><span class="rank-number">'+(i+1)+'</span><div><strong>'+esc(x.input.name)+'</strong><div class="rank-track"><span style="width:'+(x.edps/best*100).toFixed(2)+'%"></span></div></div><b>'+format(x.edps)+' eDPS</b><span>'+format(x.edps/best*100)+' / 100</span></div>').join('')+savedList;
  }
  async function fetchJSON(url) {
    const response=await fetch(url+'?t='+Math.floor(Date.now()/300000),{cache:'no-store',signal:AbortSignal.timeout(10000)});
    if (!response.ok) throw new Error('fetch');return response.json();
  }
  async function refresh(initial=false) {
    const results=await Promise.allSettled([fetchJSON(root.dataset.catalog),fetchJSON(root.dataset.feed)]);
    if (results[1].status==='fulfilled') latestFeed=results[1].value;
    if (results[0].status==='fulfilled') {
      const next=results[0].value;
      if (!db||next.sourceHash!==db.sourceHash||next.version!==db.version||next.sourceDate!==db.sourceDate) {
        const changed=Boolean(db);db=next;
        if (!changed||!dirty) loadClass();
      }
    } else if (initial) fail(t('Unable to load the calculator inputs. Retry by refreshing this page.','계산 입력 자료를 불러오지 못했습니다. 화면을 새로고침해 다시 시도하세요.'));
    if (db) {patchState();compare();}
  }
  form.addEventListener('submit',event=>{event.preventDefault();calculate();});
  form.addEventListener('input',event=>{
    dirty=true;
    const row=event.target.closest('tr');
    if (event.target.dataset.skillParam==='cooldown'&&row) row.querySelector('[data-skill-param="afterCooldown"]').value=event.target.value;
    calculate();
  });
  q('[data-dps-class]').addEventListener('change',loadClass);
  param('region').addEventListener('change',loadClass);
  tbody.addEventListener('click',event=>{
    const el=event.target.closest('tr');if (!el)return;
    if (event.target.closest('[data-up]')&&el.previousElementSibling) tbody.insertBefore(el,el.previousElementSibling);
    else if (event.target.closest('[data-down]')&&el.nextElementSibling) tbody.insertBefore(el.nextElementSibling,el);
    else if (event.target.closest('[data-remove]')) el.remove();else return;
    dirty=true;calculate();
  });
  q('[data-dps-add]').addEventListener('click',()=>{if(tbody.rows.length>=40){fail(t('Maximum 40 skill inputs.','스킬 입력은 최대 40개입니다.'));return;}row({id:'custom-'+(++custom),name:t('Custom skill','추가 스킬')+' '+custom,flat:0,coefficient:0,hits:1,cast:1,cooldown:0},true);dirty=true;calculate();});
  q('[data-dps-confirm-version]').addEventListener('click',()=>{
    if(!db||!calculate())return;
    activeSnapshot={sourceHash:db.sourceHash,sourceDate:db.sourceDate,model:db.version};
    dirty=true;calculate();patchState();
  });
  q('[data-dps-compare]').addEventListener('click',()=>{if(calculate()){if(comparisons.length>=8){fail(t('Maximum eight builds. Clear the comparison to start again.','빌드는 최대 8개입니다. 비교를 초기화해 다시 추가하세요.'));return;}comparisons.push({input:structuredClone(input),edps:result.before.edps});saveComparisons();compare();}});
  q('[data-dps-clear]').addEventListener('click',()=>{comparisons=[];saveComparisons();compare();});
  q('[data-dps-comparisons]').addEventListener('click',event=>{
    const button=event.target.closest('[data-dps-restore]');if(!button)return;
    const saved=comparisons[Number(button.dataset.dpsRestore)]?.input;
    const cls=db?.classes.find(c=>c.id===saved?.classId);if(!cls)return;
    current=cls;q('[data-dps-class]').value=cls.id;
    activeSnapshot={sourceHash:saved.sourceHash,sourceDate:saved.sourceDate,model:saved.model};
    root.querySelectorAll('[data-param]').forEach(el=>{if(saved[el.dataset.param]!==undefined)el.value=saved[el.dataset.param];});
    tbody.replaceChildren();saved.skills.forEach(s=>{row(s,true);const el=tbody.lastElementChild;el.querySelector('[data-enabled]').checked=Boolean(s.enabled);el.querySelector('[data-skill-param="delta"]').value=s.delta;el.querySelector('[data-skill-param="afterCooldown"]').value=s.afterCooldown;});
    dirty=true;calculate();patchState();q('[data-dps-results]').scrollIntoView({block:'nearest'});
  });
  q('[data-dps-export]').addEventListener('click',()=>{
    if (!calculate()) return;
    const safe=s=>'"'+String(s).replace(/^[=+@-]/,"'").replace(/"/g,'""')+'"';
    const rows=[...Object.entries(input).filter(([k])=>k!=='skills'),['eDPS',result.before.edps],['scenario_eDPS',result.after.edps],[],['skill','enabled','base','coefficient_pct','hits','cast_s','cooldown_s','damage_delta_pct','after_cooldown_s']];
    input.skills.forEach(s=>rows.push([s.name,s.enabled,s.flat,s.coefficient,s.hits,s.cast,s.cooldown,s.delta,s.afterCooldown]));
    const url=URL.createObjectURL(new Blob(['\uFEFF'+rows.map(x=>x.map(safe).join(',')).join('\r\n')],{type:'text/csv;charset=utf-8'}));
    const a=document.createElement('a');a.href=url;a.download='players-codex-dps.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  compare();refresh(true);
  setInterval(()=>{if(!document.hidden)refresh();},300000);
})();

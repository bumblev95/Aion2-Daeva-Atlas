(function () {
  'use strict';
  const root = document.querySelector('[data-dps-lab]');
  if (!root) return;
  const ko = root.dataset.lang === 'ko', t = (a,b) => ko ? b : a, q = s => root.querySelector(s);
  const form = q('[data-dps-form]'), tbody = q('[data-dps-skills]'), error = q('[data-dps-error]');
  const format = n => new Intl.NumberFormat(ko?'ko-KR':'en-US',{maximumFractionDigits:1}).format(n);
  const esc = x => String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let db, current, custom=0, comparisons=[], result, input, dirty=false, latestFeed, activeSnapshot;
  const conditionDefaults={conditionMode:'tooltip',targetControl:'unknown',fireMarkEnabled:'yes',
    resourceMode:'unverified',mpStart:'0',mpMax:'1000',mpRegen:'0',elementsStart:'0',elementEvents:''};
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
  const stateName=id=>{const s=db?.states.find(x=>x.id===id);return s?.[ko?'ko':'en']||id;};
  function ruleText(s) {
    const parts=[];
    if(s.requires?.length)parts.push(t('Needs: ','필요: ')+s.requires.map(stateName).join(t(' OR ',' 또는 ')));
    if(s.elementCost)parts.push(t('Spend 4 element stacks','정령 원소 4중첩 소모'));
    if(s.effects?.length)parts.push(t('Provides: ','제공: ')+s.effects.map(e=>stateName(e.state)+' '+(e.duration??'?')+'s').join(', '));
    return parts.join(' · ')||t('No base activation condition found','기본 발동 선행 조건 없음');
  }
  function row(s,manual=false) {
    const el=document.createElement('tr');el.dataset.id=s.id;el.dataset.name=s[ko?'ko':'en']||s.name;
    // Source rules survive edits, saves and restore. An old saved row cannot
    // turn a known conditional source skill into an unconditional custom hit.
    const source=current?.candidates?.find(x=>x.id===s.id);
    const r=source||s;
    el.skillRules=structuredClone({requires:r.requires||[],effects:r.effects||[],consumeStates:r.consumeStates||[],
      elementCost:r.elementCost||0,conditionRegion:r.conditionRegion,source:r.source});
    el.innerHTML='<td><input type="checkbox" data-enabled checked aria-label="'+esc(t('Include skill','스킬 사용'))+'"><button type="button" data-up aria-label="'+esc(t('Move skill up','우선순위 올리기'))+'">↑</button><button type="button" data-down aria-label="'+esc(t('Move skill down','우선순위 내리기'))+'">↓</button><button type="button" data-remove aria-label="'+esc(t('Remove skill','스킬 삭제'))+'">×</button></td><th scope="row">'+(s.icon?'<img src="'+esc(s.icon)+'" width="30" height="30" alt="" loading="lazy">':'')+(manual?'<input data-custom-name value="'+esc(el.dataset.name)+'" maxlength="60" aria-label="'+esc(t('Custom skill name','직접 추가한 스킬 이름'))+'">':'<a href="'+esc(s.url)+'" target="_blank" rel="noopener">'+esc(el.dataset.name)+'</a>')+'</th><td>'+numeric('flat',s.flat,0,100000000)+'</td><td>'+numeric('coefficient',s.coefficient,0,100000)+'</td><td>'+numeric('hits',s.hits,1,1000,'1')+'</td><td>'+numeric('cast',s.cast,.05,120)+'</td><td>'+numeric('cooldown',s.cooldown,0,3600)+'</td><td>'+numeric('delta',0,-100,1000)+'</td><td>'+numeric('afterCooldown',s.cooldown,0,3600)+'</td>';
    const cell=document.createElement('td');cell.className='skill-condition';
    cell.innerHTML='<small>'+esc(ruleText(el.skillRules))+'</small>'+(s.setupOnly?'<small class="needs-review">'+t('Setup only · damage is zero until entered','선행 기술 전용 · 피해 입력 전에는 0')+'</small>':'')+
      (!source?'<label>'+t('Activation condition','발동 조건')+'<select data-custom-condition><option value="">'+t('None declared','지정하지 않음')+'</option>'+db.states.map(x=>'<option value="'+esc(x.id)+'">'+esc(x[ko?'ko':'en'])+'</option>').join('')+'<option value="slow|root">'+t('Slow OR Root','이동 둔화 또는 속박')+'</option><option value="elements">'+t('4 element stacks','원소 4중첩')+'</option></select></label>':'')+
      (r.consumeStates?.length?'<label>'+t('Trigger use','연계 사용')+'<select data-chain-mode><option value="once">'+t('Once per trigger · assumption','발동당 1회 · 가정')+'</option><option value="window">'+t('Throughout window · assumption','구간 내 재사용 · 가정')+'</option></select></label>':'');
    el.append(cell);
    const cost=document.createElement('td');cost.innerHTML='<input type="number" data-skill-param="mpCost" value="'+esc(s.mpCost??'')+'" min="0" max="10000000" step="any" placeholder="'+t('Unknown','미검증')+'" aria-label="'+esc(t('MP cost · blank is unknown','MP 소모 · 빈칸은 미검증'))+'">';el.append(cost);
    const gain=document.createElement('td');gain.innerHTML=numeric('mpGain',s.mpGain??0,0,10000000);el.append(gain);
    if(el.querySelector('[data-chain-mode]'))el.querySelector('[data-chain-mode]').value=s.chainMode||'once';
    if(el.querySelector('[data-custom-condition]'))el.querySelector('[data-custom-condition]').value=s.elementCost?'elements':(s.requires||[]).join('|');
    tbody.append(el);
  }
  function conditionUI() {
    const windows=q('[data-state-windows]');
    if(!windows.children.length)windows.innerHTML=db.states.map(s=>'<label>'+esc(s[ko?'ko':'en'])+'<input data-state-window="'+esc(s.id)+'" placeholder="'+t('e.g. 0-5, 20-25','예: 0-5, 20-25')+'" aria-label="'+esc(s[ko?'ko':'en']+t(' available seconds',' 사용 가능 시간'))+'"></label>').join('');
    const picker=q('[data-dps-source-skill]');
    picker.innerHTML=current.candidates.map(s=>'<option value="'+esc(s.id)+'">'+esc(s[ko?'ko':'en'])+'</option>').join('');
    const audit=current.conditionAudit;
    const knownMP=audit.filter(s=>s.mpCost!==null).length;
    q('[data-condition-audit]').innerHTML='<p>'+esc(t('Condition review: ','조건 확인일: ')+db.conditionReviewDate)+' · '+t('Numeric MP costs: '+knownMP+' / 12. Remaining costs are unverified.','숫자로 확인한 MP 소모: '+knownMP+' / 12. 나머지는 미검증입니다.')+'</p><p>'+t('Reviewed '+audit.length+' active tooltips. Specializations, passive damage and Stigmas remain outside the base damage model.','액티브 '+audit.length+'개 설명을 검토했습니다. 특화·패시브 피해·스티그마는 기본 피해 모델에 포함하지 않습니다.')+'</p><ul>'+audit.filter(s=>s.requires.length||s.elementCost||s.categories.includes('provider')).map(s=>'<li><a href="'+esc(s.source)+'" target="_blank" rel="noopener">'+esc(s[ko?'ko':'en'])+'</a>: '+esc(s.requires.length?s.requires.map(stateName).join(t(' OR ',' 또는 ')):s.elementCost?t('4 stacks consumed; provide spirit-skill times','4중첩 소모 · 정령 기술 시각 입력 필요'):t('Provides a prerequisite','선행 상태·연계 제공'))+(s.unknownTrigger?' · '+t('Trigger timing unverified; enter observed windows','발동 구간 미검증 · 확인한 시간 입력'):'')+'</li>').join('')+'</ul><p>'+t('Conditional extra damage and MP-on-crit are effects, not automatically base-skill restrictions. For example, Drill Dart’s critical-hit wording affects MP restoration; no critical-hit activation gate is inferred from it.','조건부 추가 피해나 치명타 시 MP 회복은 효과이며 기본 스킬의 사용 조건으로 자동 해석하지 않습니다. 예를 들어 Drill Dart의 치명타 문구는 MP 회복에 붙으므로 기본 피해에 치명타 선행 조건을 임의로 추가하지 않습니다.')+'</p>';
  }
  function loadClass() {
    if(!db)return;
    current=db.classes.find(c=>c.id===q('[data-dps-class]').value);
    tbody.replaceChildren();dirty=false;
    activeSnapshot={sourceHash:db.sourceHash,sourceDate:db.sourceDate,model:db.version,conditionsVerified:db.conditionsVerified};
    const kr=param('region').value==='KR';
    conditionUI();
    current.skills.forEach(s=>row(kr?{...s,flat:0,coefficient:0,cooldown:0,mpCost:null,mpGain:0}:s));
    param('patch').value=kr?'KR / '+t('enter client reference','클라이언트 기준 직접 입력'):'Global / tooltip '+db.sourceDate;
    q('[data-dps-omitted]').textContent=t(current.directCount+' / 12 active skills have seeded direct damage. '+current.omitted+' direct-damage inputs, passive damage, Stigmas, procs, pets and higher-level effects remain missing. Setup-only rows have zero damage. Enter measured action times and final build values.','액티브 12개 중 '+current.directCount+'개에 직접 피해 초기값이 있습니다. '+current.omitted+'개의 직접 피해 입력과 패시브 피해·스티그마·발동 피해·펫·레벨 상승 효과는 미반영입니다. 선행 기술 전용 행의 피해는 0입니다. 측정한 동작 시간과 최종빌드 수치를 입력하세요.');
    q('[data-dps-results]').replaceChildren();result=null;
    patchState();calculate();
  }
  function read() {
    const out={}; root.querySelectorAll('[data-param]').forEach(el=>out[el.dataset.param]=el.value);
    out.classId=current.id;out.sourceHash=activeSnapshot.sourceHash;out.sourceDate=activeSnapshot.sourceDate;out.model=activeSnapshot.model;
    out.conditionsVerified=activeSnapshot.conditionsVerified??db.conditionsVerified;
    out.name=out.name.trim()||current[ko?'ko':'en']+t(' / tooltip model',' / 툴팁 모델');
    out.stateWindows={};root.querySelectorAll('[data-state-window]').forEach(el=>out.stateWindows[el.dataset.stateWindow]=el.value);
    out.skills=Array.from(tbody.rows).map(el=>{
      const s={...structuredClone(el.skillRules),id:el.dataset.id,name:el.querySelector('[data-custom-name]')?.value||el.dataset.name,enabled:el.querySelector('[data-enabled]').checked,
        chainMode:el.querySelector('[data-chain-mode]')?.value||'once'};
      const customCondition=el.querySelector('[data-custom-condition]')?.value;
      if(customCondition!==undefined){s.requires=customCondition&&customCondition!=='elements'?customCondition.split('|'):[];s.elementCost=customCondition==='elements'?4:0;}
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
      const reasons=x=>x.map(v=>v.startsWith('state:')?t('Needs ','필요: ')+v.slice(6).split('|').map(stateName).join(t(' OR ',' 또는 ')):({'mp-unverified':t('MP cost unverified','MP 소모 미검증'),mp:t('Insufficient MP','MP 부족'),elements:t('Needs 4 element stacks','원소 4중첩 필요')})[v]||v).join(' · ');
      const skillRows=before.breakdown.map((s,i)=>'<tr><th scope="row">'+esc(s.name)+'</th><td>'+s.casts+'</td><td>'+format(s.damage)+'</td><td>'+format(before.total?s.damage/before.total*100:0)+'%</td><td>'+format(after.breakdown[i].damage)+'</td><td>'+esc(reasons(s.blocked))+'</td></tr>').join('');
      q('[data-dps-results]').innerHTML='<h2>'+t('Calculated model result','입력 조건의 계산 결과')+'</h2><div class="dps-metrics"><div><span>eDPS</span><strong>'+format(before.edps)+'</strong><small>'+t('Whole fight denominator','전체 전투 시간 기준')+'</small></div><div><span>'+t('After scenario','변경 시나리오 eDPS')+'</span><strong>'+format(after.edps)+'</strong><small>'+(delta===null?t('No baseline damage','기준 피해 없음'):((delta>0?'+':'')+format(delta))+'%')+'</small></div><div><span>'+t('Attackable-window DPS','공격 가능 구간 DPS')+'</span><strong>'+format(before.activeDps)+'</strong><small>'+format(before.activeTime)+' / '+input.duration+'s</small></div></div>'+graph(before.events,Number(input.duration))+'<p class="small muted">'+t('Cumulative expected damage · selected inputs only','누적 기대 피해 · 선택한 입력만 계산')+'</p><div class="dps-table-scroll"><table><thead><tr>'+[t('Skill','스킬'),t('Casts','사용 횟수'),t('Damage','기대 피해'),t('Share','기여도'),t('After damage','변경 후 피해')].map(x=>'<th scope="col">'+x+'</th>').join('')+'</tr></thead><tbody>'+skillRows+'</tbody></table></div>';
      const tableHead=q('[data-dps-results] thead tr');
      tableHead.insertAdjacentHTML('beforeend','<th scope="col">'+t('Restrictions encountered','계산 중 사용 제한')+'</th>');
      const labels={
        'resources-unverified':t('MP limits are not calculated. Enable the MP budget and enter unknown costs to test resource sufficiency.','MP 제한을 계산하지 않았습니다. MP 계산을 켜고 미검증 소모량을 입력해야 자원 부족을 검증할 수 있습니다.'),
        'target-control-unverified':t('Automatic control effects are blocked unless you confirm that the target accepts control. Observed windows can be entered separately.','대상이 상태이상을 허용하는지 확인하기 전에는 둔화·속박 등을 자동 적용하지 않습니다. 확인한 상태 구간을 별도로 입력할 수 있습니다.'),
        'probabilistic-hit-effects':t('Hit chance is below 100%. Damage still uses expected value; successful status applications require observed windows.','적중 확률이 100% 미만입니다. 기대 피해는 계산하지만 상태 적용 성공은 가정하지 않으므로 확인한 구간을 입력하세요.'),
        'probabilistic-mp-gain':t('MP gained on a hit is not granted automatically at less than 100% hit chance.','적중률이 100% 미만이면 적중 시 MP 회복을 자동 지급하지 않습니다.'),
        'uncertain-state-effect':t('An unknown duration or uncertain proc was not applied automatically.','지속 시간 또는 발동 확률이 불확실한 효과는 자동 적용하지 않았습니다.'),
        'global-only-conditions':t('Global prerequisite providers are not automatically applied to a KR build. Enter confirmed KR windows.','글로벌 선행 효과를 한국판 빌드에 자동 적용하지 않습니다. 확인한 한국판 구간을 입력하세요.'),
        'dot-lifetime-assumption':t('Chain of Torment has a 10s DoT tooltip, but the usable Condemnation window is not independently measured. Enter its confirmed state window.','고통의 연쇄의 지속 피해는 10초지만 Condemnation 사용 가능 구간은 별도 실측이 없습니다. 확인한 선행 상태 구간을 입력하세요.'),
        'chain-consumption-assumption':t('Trigger consumption is an editable assumption: one follow-up per opener by default.','연계 소모 방식은 수정 가능한 가정입니다. 기본값은 선행 발동당 후속 기술 1회입니다.')};
      const allWarnings=[...new Set([...before.warnings,...after.warnings])];
      const notice=document.createElement('div');notice.className='condition-notices';
      notice.innerHTML='<p><strong>'+t('Condition coverage','조건 반영 범위')+'</strong> · '+t('A cooldown being ready does not make a conditional skill available. Missing conditions produce zero casts or limited casts.','쿨타임이 끝나도 선행 조건이 없으면 사용할 수 없습니다. 조건이 빠지면 사용 횟수가 0이 되거나 제한됩니다.')+'</p>'+allWarnings.map(w=>'<p>'+esc(labels[w]||w)+'</p>').join('');
      q('[data-dps-results]').prepend(notice);
      fail('');return true;
    } catch (e) {
      result=null;q('[data-dps-results]').replaceChildren();
      if(e.message==='condition-snapshot'){fail(t('Skill data changed after the condition audit. Calculations are blocked until the activation rules are re-reviewed.','조건 조사 후 스킬 자료가 변경됐습니다. 발동 조건을 다시 검토하기 전에는 계산하지 않습니다.'));return false;}
      fail(t('Check numbers and state/downtime windows (e.g. 30-40, 90-100), within the fight duration. MP start must not exceed its maximum. Include at least one skill.','숫자와 상태·공격 불가 구간(예: 30-40, 90-100)이 전투 시간 안에 있는지 확인하세요. 시작 MP는 최대 MP 이하여야 하며 스킬을 하나 이상 선택해야 합니다.'));return false;
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
  q('[data-dps-add]').addEventListener('click',()=>{if(tbody.rows.length>=40){fail(t('Maximum 40 skill inputs.','스킬 입력은 최대 40개입니다.'));return;}do{custom++;}while(Array.from(tbody.rows).some(x=>x.dataset.id==='custom-'+custom));row({id:'custom-'+custom,name:t('Custom skill','추가 스킬')+' '+custom,flat:0,coefficient:0,hits:1,cast:1,cooldown:0},true);dirty=true;calculate();});
  q('[data-dps-add-source]').addEventListener('click',()=>{
    const s=current?.candidates.find(x=>x.id===q('[data-dps-source-skill]').value);if(!s)return;
    if(Array.from(tbody.rows).some(el=>el.dataset.id===s.id)){fail(t('This source skill is already in the rotation. Edit its existing row.','이미 회전에 있는 기술입니다. 기존 행을 수정하세요.'));return;}
    if(tbody.rows.length>=40){fail(t('Maximum 40 skill inputs.','스킬 입력은 최대 40개입니다.'));return;}
    row(param('region').value==='KR'?{...s,mpCost:null,mpGain:0,cooldown:0}:s);dirty=true;calculate();
  });
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
    conditionUI();
    activeSnapshot={sourceHash:saved.sourceHash,sourceDate:saved.sourceDate,model:saved.model};
    root.querySelectorAll('[data-param]').forEach(el=>{
      const value=saved[el.dataset.param]??conditionDefaults[el.dataset.param];
      if(value!==undefined)el.value=value;
    });
    root.querySelectorAll('[data-state-window]').forEach(el=>el.value=saved.stateWindows?.[el.dataset.stateWindow]||'');
    tbody.replaceChildren();saved.skills.forEach(s=>{row(s,true);const el=tbody.lastElementChild;el.querySelector('[data-enabled]').checked=Boolean(s.enabled);el.querySelector('[data-skill-param="delta"]').value=s.delta;el.querySelector('[data-skill-param="afterCooldown"]').value=s.afterCooldown;});
    dirty=true;calculate();patchState();q('[data-dps-results]').scrollIntoView({block:'nearest'});
  });
  q('[data-dps-export]').addEventListener('click',()=>{
    if (!calculate()) return;
    const url=URL.createObjectURL(new Blob([window.CodexDPS.exportCSV(input,result)],{type:'text/csv;charset=utf-8'}));
    const a=document.createElement('a');a.href=url;a.download='players-codex-dps.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  compare();refresh(true);
  setInterval(()=>{if(!document.hidden)refresh();},300000);
})();

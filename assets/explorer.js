(() => {
  'use strict';
  const root = document.querySelector('[data-explorer]');
  if (!root) return;
  const ko = document.documentElement.lang === 'ko';
  const t = (en, kr) => ko ? kr : en;
  const data = JSON.parse(document.getElementById('explorer-data').textContent);
  const base = document.body.dataset.base;
  const route = base + (ko ? 'ko/' : '');
  const query = new URLSearchParams(location.search);
  const valid = id => data.some(c => c.id === id);
  let saved = '';
  try { saved = localStorage.getItem('raidnote-aion2-class-v1') || ''; } catch {}
  // A class profile must keep its own class; bookmarks only select the hub default.
  const isProfile = /\/classes\/[^/]+\/$/.test(location.pathname);
  let selected = isProfile ? root.dataset.initialClass : valid(query.get('class')) ? query.get('class') : valid(saved) ? saved : root.dataset.initialClass;
  let mode = query.get('mode') === 'pvp' ? 'pvp' : 'pve';
  let view = ['overview','practice','gear','community'].includes(query.get('view')) ? query.get('view') : 'overview';
  const $ = s => root.querySelector(s);
  const label = key => ({damage:t('Damage','공격'),tank:t('Tank','탱커'),healer:t('Healer','회복'),support:t('Support','지원'),melee:t('Melee','근접'),ranged:t('Ranged','원거리')}[key]);
  const goals = {
    gladiator: [t('Close-range pressure','근접 공격 유지'),t('Commit with an exit','퇴로를 정하고 진입')],
    templar: [t('Control enemy facing','적의 정면 방향 관리'),t('Stay with your group','파티와 함께 움직이기')],
    assassin: [t('Pick a safe opening','안전한 공격 기회'),t('Choose your moment','진입 타이밍 선택')],
    ranger: [t('Keep a clear line','시야와 거리 확보'),t('Protect your spacing','유리한 간격 유지')],
    sorcerer: [t('Find a casting window','안전한 시전 시간'),t('Use a short opening','짧은 기회 활용')],
    spiritmaster: [t('Watch both positions','자신과 정령 위치'),t('Track target changes','대상 변경 확인')],
    cleric: [t('Watch party health','파티 상태 확인'),t('Protect your own position','내 안전 위치 확보')],
    chanter: [t('Support near the group','파티 가까이서 지원'),t('Cover your teammates','동료 지원 유지')],
  };
  const tips = {
    damage: [t('Find a safe angle. Move when the encounter demands it.','안전한 공격 각도를 잡고, 패턴에 맞춰 이동하세요.'), t('Keep a way out before committing to a target.','대상에게 진입하기 전에 퇴로를 확보하세요.')],
    tank: [t('Control facing; keep frontal danger away from the group.','적의 방향을 관리하고 정면 위험을 파티에서 돌리세요.'), t('Watch your group’s position as well as the opponent.','상대뿐 아니라 아군의 위치도 함께 보세요.')],
    healer: [t('Keep the party in reach while staying clear of danger.','파티를 지원할 수 있는 거리에서 위험을 피하세요.'), t('Stay connected to teammates who can cover you.','도움을 줄 수 있는 동료와 떨어지지 마세요.')],
    support: [t('Balance safe melee positioning with party support.','안전한 근접 위치와 파티 지원을 함께 챙기세요.'), t('Follow the team’s opening, then recover together.','파티의 진입에 맞추고 함께 재정비하세요.')],
  };
  function svgIcon(name, css='icon') {
    const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');
    svg.setAttribute('viewBox','0 0 48 48');svg.setAttribute('class',css);svg.setAttribute('aria-hidden','true');
    const use=document.createElementNS(svg.namespaceURI,'use');use.setAttribute('href',base+'assets/icons.svg#'+name);svg.append(use);return svg;
  }
  function line(tag, text, cls='') {const e=document.createElement(tag);e.textContent=text;if(cls)e.className=cls;return e;}
  function updateUrl() {
    const u=new URL(location.href);
    if(!isProfile)u.searchParams.set('class',selected);
    u.searchParams.set('mode',mode);u.searchParams.set('view',view);
    history.replaceState(null,'',u);
    const language=document.querySelector('.lang');
    if(language){const translated=new URL(language.href);translated.search=u.search;language.href=translated.href;}
  }
  function render() {
    const c=data.find(x=>x.id===selected);const name=ko?c.ko:c.en;const m=mode==='pvp'?1:0;
    $('.explorer-panel').style.setProperty('--class-color',c.color);
    root.querySelectorAll('[data-pick]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.pick===selected)));
    root.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===mode)));
    root.querySelectorAll('[data-view]').forEach(b=>{const active=b.dataset.view===view;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1;});
    root.querySelectorAll('[data-panel]').forEach(p=>p.hidden=p.dataset.panel!==view);
    $('[data-profile-name]').textContent=name;
    $('[data-profile-role]').textContent=label(c.role)+' / '+label(c.range);
    $('[data-profile-identity]').textContent=c.identity[ko?1:0];
    $('[data-profile-glyph]').replaceChildren(svgIcon(c.icon,'class-glyph'));
    const facts=$('[data-quick-facts]');facts.replaceChildren();
    [[t('ROLE','역할'),label(c.role)],[t('RANGE','거리'),label(c.range)],[t('FOCUS','전투 목표'),goals[c.id][m]]].forEach(([key,value])=>{const item=line('div','');item.append(line('small',key),line('strong',value));facts.append(item);});
    $('[data-class-advice]').textContent=c.fit[ko?1:0];
    const loop=$('[data-combat-loop]');loop.replaceChildren();
    const steps=mode==='pve' ? [[c.icon,t('Position','위치')],['target',t('Act','행동')],['shield',t('React','대응')],['check',t('Review','복기')]] : [['target',t('Observe','관찰')],[c.icon,t('Engage','진입')],['shield',t('Exit','이탈')],['check',t('Reset','재정비')]];
    steps.forEach(([ic,txt],i)=>{const step=line('div','','loop-step');step.append(line('small','0'+(i+1)),svgIcon(ic),line('strong',txt));loop.append(step);});
    $('[data-practice-note]').textContent=mode==='pvp'?c.trade[ko?1:0]:c.practice[ko?1:0];
    const checks=$('[data-gear-checks]');checks.replaceChildren();
    const checksData=[['swords',t('Weapon','무기'),t('Class requirement & equipped item','직업 제한·현재 착용 장비')],['shield',t('Protection','방어'),mode==='pvp'?t('PvP wording & restrictions','PvP 적용·제한 조건'):t('Encounter requirements','콘텐츠 입장·생존 조건')],['spark',t('Investment','투자'),t('Cost, binding & replacement','비용·귀속·교체 계획')]];
    checksData.forEach(([ic,title,desc],i)=>{const row=document.createElement('label');row.className='gear-check';const input=document.createElement('input');input.type='checkbox';input.name=selected+'-'+mode+'-'+i;input.checked=gearChecks.has(input.name);input.addEventListener('change',()=>{if(input.checked)gearChecks.add(input.name);else gearChecks.delete(input.name);});const txt=line('span','');txt.append(line('strong',title),line('small',desc));row.append(svgIcon(ic),txt,input);checks.append(row);});
    $('[data-profile-link]').href=route+'classes/'+c.id+'/';
    $('[data-profile-skills]').href=route+'skills/?class='+c.id;
    $('[data-profile-compare]').href=route+'tools/compare/?a='+c.id+'&b='+(c.id==='templar'?'gladiator':'templar');
    $('[data-save-class]').setAttribute('aria-pressed',String(saved===c.id));
    const position=mode==='pvp'? (c.range==='ranged'?[295,199]:[260,164]) : c.role==='tank'?[200,48]:c.range==='ranged'?[290,201]:[232,175];
    $('[data-player-token]').setAttribute('transform',`translate(${position[0]} ${position[1]})`);
    $('[data-player-line]').setAttribute('d',`M${position[0]} ${position[1]} Q${position[0]+15} 145 226 115`);
    $('[data-player-label]').textContent=name;
    $('[data-map-mode]').textContent=mode==='pvp'?'PvP':'PvE';
    $('[data-enemy-label]').textContent=mode==='pvp'?t('OPPONENT','상대'):t('ENEMY','적');
    $('[data-map-tip]').textContent=tips[c.role][m];
    $('[data-explorer-status]').textContent=saved===c.id?t('Your saved class','내 직업으로 저장됨'):'';
    let noteCount = 0;
    root.querySelectorAll('[data-class-notes] [data-note]').forEach(n=>{n.hidden=!n.dataset.classes.split(' ').includes(selected)||n.dataset.activity!==mode;if(!n.hidden)noteCount++;});
    $('[data-class-note-empty]').hidden=noteCount>0;
    $('[data-all-class-notes]').href=route+'insights/?class='+selected+(mode==='pvp'?'&topic=pvp':'');
    $('.combat-visual').hidden=view==='community';
    $('.explorer-content').classList.toggle('reading-notes',view==='community');
    updateUrl();
  }
  const gearChecks=new Set();
  root.querySelectorAll('[data-pick]').forEach(b=>b.addEventListener('click',()=>{if(isProfile){location.href=route+'classes/'+b.dataset.pick+'/?mode='+mode+'&view='+view;return;}selected=b.dataset.pick;render();}));
  root.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;render();}));
  const tabs=[...root.querySelectorAll('[data-view]')];
  tabs.forEach((b,i)=>{
    b.addEventListener('click',()=>{view=b.dataset.view;render();});
    b.addEventListener('keydown',e=>{let n;if(e.key==='ArrowRight')n=(i+1)%tabs.length;if(e.key==='ArrowLeft')n=(i+tabs.length-1)%tabs.length;if(e.key==='Home')n=0;if(e.key==='End')n=tabs.length-1;if(n!==undefined){e.preventDefault();tabs[n].click();tabs[n].focus();}});
  });
  $('[data-save-class]').addEventListener('click',()=>{
    try{saved=saved===selected?'':selected;if(saved)localStorage.setItem('raidnote-aion2-class-v1',saved);else localStorage.removeItem('raidnote-aion2-class-v1');render();$('[data-explorer-status]').textContent=saved?t('Class saved in this browser','이 브라우저에 내 직업을 저장했습니다'):t('Saved class removed','저장된 직업을 해제했습니다');}
    catch{$('[data-explorer-status]').textContent=t('Saving is unavailable in this browser.','이 브라우저에서는 저장할 수 없습니다.');}
  });
  render();
})();

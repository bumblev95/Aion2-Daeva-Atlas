(() => {
 'use strict';
 const ko=document.documentElement.lang==='ko',t=(e,k)=>ko?k:e;
 const clamp=x=>Math.min(1,Math.max(0,x)), lerp=(a,b,v)=>a+(b-a)*clamp(v), ease=v=>{v=clamp(v);return v*v*(3-2*v);};
 const circle=(x,y,r,fill,stroke='',extra='')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" ${stroke?`stroke="${stroke}" stroke-width="2"`:''} ${extra}/>`;
 const txt=(x,y,s,c='#bbc9e1',size=14)=>`<text x="${x}" y="${y}" text-anchor="middle" fill="${c}" font-size="${size}" font-family="system-ui,sans-serif">${s}</text>`;
 const player=(x,y,n='1',jump=0,green=false)=>`<g>${circle(x,y+9,15,'#05091499')}${circle(x,y-jump,15,green?'#183f3b':'#263c62',green?'#7de4bb':'#b7d0ff')}${txt(x,y+5-jump,n,'#f8fbff',13)}${jump>12?`<path d="M${x} ${y}v-${jump-12}" stroke="#74ddbd" stroke-dasharray="3 3"/>`:''}</g>`;
 const boss=(x,y,opacity=1)=>`<g opacity="${opacity}" transform="translate(${x} ${y})"><path d="M0-27 25-14 20 17 0 29-20 17-25-14Z" fill="#54273e" stroke="#f893a6" stroke-width="2"/><path d="m-10-5 6 5m8-5-6 5m-6 11h10" stroke="#ffd6de" stroke-width="3"/></g>`;
 const line=(x,y,a,b,color='#86dabc')=>`<path d="M${x} ${y}L${a} ${b}" stroke="${color}" stroke-width="2" stroke-dasharray="6 6" fill="none"/>`;
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 const states=[...document.querySelectorAll('[data-animation]')].map(box=>({box,kind:box.dataset.animation,p:0,speed:1,playing:!motion.matches,visible:true,captions:JSON.parse(box.dataset.captions)}));
 function paint(s){
  const p=s.p, move=ease((p-.2)/.42),hit=clamp((p-.68)/.18),k=s.kind,phase=Math.min(2,Math.floor(p*3));let draw='';
  const blue='#8fbaf5',red='#f17f94',green='#7de4bb';
  const arena=`<rect width="640" height="390" fill="#0d1624"/><g stroke="#526889" stroke-opacity=".13">${Array.from({length:13},(_,i)=>`<path d="M${i*50} 0v390M0 ${i*34}h640"/>`).join('')}</g><ellipse cx="320" cy="194" rx="280" ry="172" fill="#132137" fill-opacity=".5" stroke="#46597d"/><ellipse cx="320" cy="194" rx="230" ry="138" fill="none" stroke="#718cb6" stroke-opacity=".12"/>`;
  if(k==='cover'){
   draw=boss(320,82)+circle(320,82,hit*355,'#e95d7620')+`<path d="m291 185 8-38 23-12 29 37-8 28Z" fill="#6a5939" stroke="#f4cc7a" stroke-width="3"/>`+txt(401,168,t('ROCK','바위'),'#edc878');
   const x=lerp(490,320,move),y=lerp(285,224,move);draw+=player(x,y,'1',0,p>.67);if(p>.67)draw+=circle(x,y,25,'none','#f6da83',`opacity="${.5+Math.sin(p*80)*.3}"`)+txt(320,278,t('Protection buff','보호 버프'),'#ffe2a2');
  } else if(k==='out'){
   const spin=s.box.dataset.encounter==='berk-spin',repeat=s.box.dataset.encounter==='kromede-bow';
   // Conceptual chase only: no measured boss route or radius is asserted.
   const bx=spin?lerp(290,395,ease((p-.58)/.32)):290;
   const by=spin?lerp(166,223,ease((p-.58)/.32)):166;
   draw=boss(bx,by)+circle(bx,by,100,'#dc5b7826',red,`stroke-dasharray="7 6"`)+line(350,215,522,303)+player(lerp(350,522,move),lerp(215,303,move),'1',0,p>.95);
   if(spin){
    for(let i=0;i<8;i++){const a=i*Math.PI/4+p*12;draw+=circle(bx+Math.cos(a)*35,by+Math.sin(a)*35,3,red);}
    draw+=txt(320,52,t('SPIN CAN CHASE','회전 중 추격 가능'),red);
   } else if(repeat){
    draw+=`<path d="M284 118q35 17 15 42m-1-25v28l-7-9m7 9 8-9" stroke="#f1ca85" stroke-width="3" fill="none"/>`;
    const bursts=[clamp(1-Math.abs(p-.53)/.07),clamp(1-Math.abs(p-.81)/.07)];
    bursts.forEach((v,i)=>{if(v>0)draw+=circle(bx,by,v*101,'#f6679760')+txt(290,316,`${t('BURST','공격')} ${i+1} / 2`,red);});
    draw+=txt(320,52,t('LOW HP: TWO BURSTS','저체력: 두 번 연속'),red);
   }
  } else if(k==='stagger'){
   draw=boss(320,140)+`<rect x="200" y="196" width="240" height="15" rx="7" fill="#49304e"/><rect x="203" y="199" width="${234*(1-clamp((p-.25)/.5))}" height="9" rx="4" fill="#d5a1f1"/>`+txt(320,235,p<.25?t('LOCKED','잠김'):t('STAGGER','그로기'),'#d5b5f2');
   [230,405].forEach((x,i)=>{draw+=player(x,304,String(i+1));if(p>.3&&p<.8)draw+=line(x,288,320,166,'#d3acfb')+circle(lerp(x,320,(p*7+i)%1),lerp(287,165,(p*7+i)%1),5,'#d3acfb');});
  } else if(k==='jump'){
   const vak=s.box.dataset.encounter==='vakron-rings',waves=vak?3:2;
   draw=(vak?'<ellipse data-red-floor cx="320" cy="194" rx="280" ry="172" fill="#e7617b22"/>':'')+boss(320,135);let jump=0;
   if(vak){
    // Example lanes, not the game's measured angles or number of spokes.
    [-.46,.46,1.57].forEach(a=>{draw+=line(320,135,320+Math.sin(a)*250,135+Math.cos(a)*214,red);});
    draw+=txt(320,42,t('LINES: SIDESTEP','직선 공격: 옆으로 이동'),red);
   }
   for(let i=0;i<waves;i++){
    const w=(p-.08-i*(vak?.19:.27))/(vak?.18:.25);
    if(w>0&&w<1.2){draw+=`<ellipse data-wave="${i+1}" cx="320" cy="135" rx="${w*285}" ry="${w*170}" fill="none" stroke="${red}" stroke-width="4" opacity="${w<1?1:0}"/>`;jump=Math.max(jump,Math.max(0,1-Math.abs(w-.64)*5)*49);}
   }
   if(vak&&p>.75){draw+=`<ellipse data-binding-follow-up cx="320" cy="194" rx="280" ry="172" fill="#ffc47730" stroke="#ffc477"/>`;jump=Math.max(jump,Math.max(0,1-Math.abs(p-.83)*9)*55);}
   const px=vak?lerp(320,374,ease((p-.03)/.18)):320;
   draw+=player(px,vak?256:lerp(256,205,ease((p-.75)/.18)),'1',jump,jump>0);
   draw+=txt(475,327,vak?(p>.75?t('FOLLOW-UP: JUMP','후속타: 다시 점프'):t('3 RINGS','고리 3번')):t('RINGS → STAGGER','고리 → 그로기'),green);
   if(!vak&&p>.78)draw+=`<rect x="241" y="166" width="158" height="8" fill="#4a3152"/><rect x="243" y="168" width="${154*(1-clamp((p-.8)/.19))}" height="4" fill="#d5a1f1"/>`;
  } else if(k==='track'){
   // Observation lesson: no invented underwater path or return location.
   draw=`<ellipse cx="320" cy="180" rx="240" ry="133" fill="#2473a824"/>`+boss(320,167,p>.25?.27:1)+player(218,283)+txt(320,60,t('OBSERVE, DO NOT PREDICT A ROUTE','방향 관찰, 고정 경로 아님'),blue);
   if(p>.25)draw+=`<ellipse cx="320" cy="167" rx="37" ry="20" fill="none" stroke="${blue}" stroke-dasharray="5 5"/>`+txt(320,222,t('LOOK BELOW THE SURFACE','수면 아래 윤곽 확인'),blue);
  } else if(k==='stack'||k==='spread'){
   draw=boss(320,86);const stack=k==='stack',from=stack?[[190,225],[455,285],[465,166]]:[[295,240],[326,240],[310,273]],to=stack?[[295,245],[338,245],[316,278]]:[[144,220],[481,210],[328,332]];
   if(stack)draw+=txt(320,42,t('AIRBORNE BOSS · RED MARK','보스 비상 · 붉은 징표'),red)+circle(320,250,55,'#ea628222',red)+player(320,220,'1',0,hit>0);
   const cloneHit=clamp(1-Math.min(Math.abs(p-.70),Math.abs(p-.89))/.06);
   from.forEach((a,i)=>{const x=lerp(a[0],to[i][0],move),y=lerp(a[1],to[i][1],move);draw+=line(...a,...to[i])+player(x,y,String(i+(stack?2:1)),0,move>.98);if(!stack){draw+=boss(x,y-72,.5);if(cloneHit>0)draw+=circle(x,y,cloneHit*47,'#ef769930',red);}});if(stack)draw+=circle(320,250,hit*56,'#ef769960');
   if(!stack)draw+=txt(320,52,t('TWO CLONE HITS: STAY SPREAD','분신 두 공격: 산개 유지'),red);
  } else if(k==='fan'){
   draw=boss(295,110)+`<path d="M295 135 170 325H420Z" fill="#e45b7624" stroke="${red}" stroke-dasharray="6 6"/>`+player(lerp(325,490,move),lerp(263,277,move),'1',0,move>.95);
   if(p>.6)for(let i=0;i<5;i++){let f=clamp((p-.6)/.25);draw+=line(lerp(295,184+i*54,f),lerp(138,316,f),lerp(295,184+i*54,f)+3,lerp(138,316,f)+13,red);}
  } else if(k==='rescue'){
   draw=boss(320,75)+player(377,220,'1',0,p>.83)+player(lerp(183,284,move),lerp(282,243,move),'2');
   if(p<.84)draw+=`<rect x="351" y="181" width="52" height="6" rx="3" fill="#86d29f"/>`+txt(377,157,t('MARKED','대상 지정'),'#b3db79');
   if(p<.34)draw+=circle(377,220,57,'#e45b7624',red,`stroke-dasharray="5 5"`);
   if(p>.34&&p<.84)draw+=circle(377,220,42,'#a5c95120','#adce71')+`<path d="m354 201 47 38m-44 0 42-41m-21-11 2 64" stroke="#b3db79" stroke-width="4"/>`;
   if(p>.5&&p<.85)draw+=line(288,240,362,223,green)+circle(lerp(288,362,(p*6)%1),lerp(240,223,(p*6)%1),5,green);
  } else if(k==='prison'){
   draw=boss(320,181)+txt(320,49,t('STAGGER LOCKED','그로기 잠김'),'#d5b5f2');
   for(let i=0;i<12;i++){
    const angle=i/12*Math.PI*2,redRock=i===3,x=320+Math.cos(angle)*116,y=200+Math.sin(angle)*110;
    if(redRock&&p>.57)continue;
    draw+=`<rect data-rock="${redRock?'red':'ordinary'}" x="${x-15}" y="${y-17}" width="30" height="34" rx="7" fill="${redRock?'#9b465b':'#3c4c65'}" stroke="${redRock?'#ffb0b8':'#6a7f9b'}" stroke-width="3"/>`;
   }
   if(p>.28&&p<.57)draw+=line(320,263,320,293,red)+txt(468,293,t('BREAK RED','붉은 바위 파괴'),red);
   if(p>.57)draw+=line(320,267,320,353)+txt(469,315,t('THIS OPENING','여기 생긴 틈'),green);
   draw+=player(320,lerp(252,352,ease((p-.62)/.25)),'1',0,p>.88);
  } else if(k==='walls'){
   draw=boss(320,62);
   const x=p<.48?lerp(320,230,ease((p-.05)/.23)):lerp(230,410,ease((p-.5)/.23));
   [[230,.10],[410,.53]].forEach(([gap,start],i)=>{
    const w=(p-start)/.43;
    if(w>=0&&w<=1){const y=lerp(84,381,w);draw+=`<path data-wall="${i+1}" data-gap="${gap}" d="M75 ${y}H${gap-45}M${gap+45} ${y}H565" stroke="#ec8a65" stroke-width="15" opacity=".82"/>`;}
   });
   if(p>.65)draw+=circle(125,184,8,'#ec8a6588')+circle(525,215,8,'#ec8a6588')+txt(320,120,t('LOW HP: ALSO WATCH PROJECTILES','저체력: 추가 투사체도 확인'),red);
   draw+=player(x,294,'1')+txt(320,365,t('NEXT WALL, NEW GAP','다음 불벽, 새로운 틈'),green);
  } else if(k==='intercept'){
   draw=boss(112,185)+line(145,185,518,185,red)+player(520,185,'1')+circle(520,185,26,'none',red)+player(310,lerp(303,185,move),'2',0,move>.98);
   if(p>.65)draw+=boss(lerp(145,280,clamp((p-.65)/.18)),185,.7);if(p>.83)draw+=txt(310,123,t('NEXT: SWITCH','다음은 교대'),'#ffe0a0');
  } else if(k==='circles'){
   draw+=circle(174,192,107,'#e35d7822',red)+circle(463,192,59,'#b485ef20','#c7a2f5')+player(174,192,'1')+player(463,171,'2')+player(lerp(305,440,move),lerp(307,209,move),'3',0,move>.98)+player(lerp(574,481,move),lerp(306,209,move),'4',0,move>.98)+txt(174,51,t('LARGE: SOLO','큰 원: 혼자'),red)+txt(463,51,t('SMALL: TOGETHER','작은 원: 함께'),'#d0b2f6');if(hit)draw+=circle(174,192,hit*107,'#ed719333')+circle(463,192,hit*59,'#c397ef33');
  } else if(k==='orb'){
   draw=boss(100,182)+circle(317,182,66,'#05091488',red)+circle(317,182,38,'#4763b055',blue)+line(131,182,533,182,blue)+player(lerp(495,542,move),lerp(307,182,move),'1',0,move>.98)+txt(317,277,t('DARK ZONE: KEEP OUT','검은 범위: 들어가지 않기'),red);
   draw+=`<rect x="${lerp(495,542,move)-26}" y="${lerp(307,182,move)-39}" width="52" height="6" rx="3" fill="#86d29f"/>`;
   draw+=txt(320,48,t('GOAL: 3 HITS / 4 OPPORTUNITIES','목표: 네 번의 기회 중 세 번 적중'),'#ffdfb8');
   draw+=txt(445,117,t('RE-ALIGN EACH SHOT','매번 다시 정렬'),green);
   // One example shot after alignment, not an invented four-shot timeline.
   if(p>.65&&p<.9){const shot=(p-.65)/.25;draw+=circle(lerp(132,317,shot),182,8,'#ffc29f');}
  }
  s.box.querySelector('[data-battle-scene]').innerHTML=arena+draw;
  s.box.querySelector('[data-animation-caption]').textContent=s.captions[phase];s.box.querySelector('[data-animation-phase]').textContent=`0${phase+1} / 03`;
  const seek=s.box.querySelector('[data-animation-seek]');seek.value=Math.floor(p*1000);seek.setAttribute('aria-valuetext',`${phase+1} / 3: ${s.captions[phase]}`);s.box.dataset.stage=String(phase);
 }
 function sync(s){const btn=s.box.querySelector('[data-animation-toggle]');btn.textContent=s.playing?'Ⅱ':'▶';btn.setAttribute('aria-label',s.playing?t('Pause animation','애니메이션 일시정지'):t('Play animation','애니메이션 재생'));s.box.dataset.playing=String(s.playing);}
 states.forEach(s=>{s.box.querySelector('[data-animation-toggle]').addEventListener('click',()=>{s.playing=!s.playing;sync(s);});s.box.querySelector('[data-animation-replay]').addEventListener('click',()=>{s.p=0;s.playing=true;sync(s);paint(s);});s.box.querySelector('[data-animation-speed]').addEventListener('change',e=>s.speed=Number(e.target.value));s.box.querySelector('[data-animation-seek]').addEventListener('input',e=>{s.p=clamp(Number(e.target.value)/1000);s.playing=false;sync(s);paint(s);});sync(s);paint(s);});
 motion.addEventListener?.('change',e=>{if(e.matches)states.forEach(s=>{s.playing=false;sync(s);});});
 const observer='IntersectionObserver' in window?new IntersectionObserver(entries=>entries.forEach(e=>{const s=states.find(s=>s.box===e.target);s.visible=e.isIntersecting;}),{threshold:.05}):null;states.forEach(s=>observer?.observe(s.box));
 document.addEventListener('codex:mechanic-change',()=>states.forEach(s=>{if(!s.box.closest('[hidden]')){s.p=0;paint(s);}}));
 let last=0;function tick(now){const dt=Math.min(70,now-last)/1000;last=now;states.forEach(s=>{if(s.playing&&s.visible&&!document.hidden&&!s.box.closest('[hidden]')){s.p=(s.p+dt*s.speed/10)%1;paint(s);}});requestAnimationFrame(tick);}if(states.length)requestAnimationFrame(tick);
})();

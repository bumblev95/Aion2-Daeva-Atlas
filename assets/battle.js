(() => {
 'use strict';
 const ko=document.documentElement.lang==='ko',t=(e,k)=>ko?k:e;
 const clamp=x=>Math.min(1,Math.max(0,x)), lerp=(a,b,v)=>a+(b-a)*clamp(v), ease=v=>{v=clamp(v);return v*v*(3-2*v);};
 const circle=(x,y,r,fill,stroke='',extra='')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" ${stroke?`stroke="${stroke}" stroke-width="2"`:''} ${extra}/>`;
 const txt=(x,y,s,c='#bbc9e1',size=14)=>`<text x="${x}" y="${y}" text-anchor="middle" fill="${c}" font-size="${size}" font-family="system-ui,sans-serif">${s}</text>`;
 const player=(x,y,n='1',jump=0,green=false)=>`<g>${circle(x,y+9,15,'#05091499')}${circle(x,y-jump,15,green?'#183f3b':'#263c62',green?'#7de4bb':'#b7d0ff')}${txt(x,y+5-jump,n,'#f8fbff',13)}${jump?`<path d="M${x} ${y}v-${jump-12}" stroke="#74ddbd" stroke-dasharray="3 3"/>`:''}</g>`;
 const boss=(x,y,opacity=1)=>`<g opacity="${opacity}" transform="translate(${x} ${y})"><path d="M0-27 25-14 20 17 0 29-20 17-25-14Z" fill="#54273e" stroke="#f893a6" stroke-width="2"/><path d="m-10-5 6 5m8-5-6 5m-6 11h10" stroke="#ffd6de" stroke-width="3"/></g>`;
 const line=(x,y,a,b,color='#86dabc')=>`<path d="M${x} ${y}L${a} ${b}" stroke="${color}" stroke-width="2" stroke-dasharray="6 6" fill="none"/>`;
 const states=[...document.querySelectorAll('[data-animation]')].map(box=>({box,kind:box.dataset.animation,p:0,speed:1,playing:!matchMedia('(prefers-reduced-motion: reduce)').matches,visible:true,last:0,captions:JSON.parse(box.dataset.captions)}));
 function paint(s){
  const p=s.p, move=ease((p-.2)/.42),hit=clamp((p-.68)/.18),k=s.kind,phase=Math.min(2,Math.floor(p*3));let draw='';
  const blue='#8fbaf5',red='#f17f94',green='#7de4bb';
  const arena=`<rect width="640" height="390" fill="#0d1624"/><g stroke="#526889" stroke-opacity=".13">${Array.from({length:13},(_,i)=>`<path d="M${i*50} 0v390M0 ${i*34}h640"/>`).join('')}</g><ellipse cx="320" cy="194" rx="280" ry="172" fill="#132137" fill-opacity=".5" stroke="#46597d"/><ellipse cx="320" cy="194" rx="230" ry="138" fill="none" stroke="#718cb6" stroke-opacity=".12"/>`;
  if(k==='cover'){
   draw=boss(320,82)+circle(320,82,hit*355,'#e95d7620')+`<path d="m291 185 8-38 23-12 29 37-8 28Z" fill="#6a5939" stroke="#f4cc7a" stroke-width="3"/>`+txt(401,168,t('ROCK','바위'),'#edc878');
   const x=lerp(490,320,move),y=lerp(285,224,move);draw+=player(x,y,'1',0,move>.98);if(p>.55)draw+=circle(x,y,25,'none','#f6da83',`opacity="${.5+Math.sin(p*80)*.3}"`)+txt(320,278,t('Protection buff','보호 버프'),'#ffe2a2');
  } else if(k==='out'){
   draw=boss(290,166)+circle(290,166,113,'#dc5b7826',red,`stroke-dasharray="7 6"`)+circle(290,166,hit*115,'#f6679760')+line(350,215,490,297)+player(lerp(350,490,move),lerp(215,297,move),'1',0,move>.98)+txt(298,52,t('MOVE OUT','범위 밖으로'),red);
  } else if(k==='stagger'){
   draw=boss(320,140)+`<rect x="200" y="196" width="240" height="15" rx="7" fill="#49304e"/><rect x="203" y="199" width="${234*(1-clamp((p-.25)/.5))}" height="9" rx="4" fill="#d5a1f1"/>`+txt(320,235,p<.25?t('LOCKED','잠김'):t('STAGGER','그로기'),'#d5b5f2');
   [230,405].forEach((x,i)=>{draw+=player(x,304,String(i+1));if(p>.3&&p<.8)draw+=line(x,288,320,166,'#d3acfb')+circle(lerp(x,320,(p*7+i)%1),lerp(287,165,(p*7+i)%1),5,'#d3acfb');});
  } else if(k==='jump'){
   const vak=s.box.dataset.encounter==='vakron-rings',waves=vak?4:1;
   draw=boss(320,135);let jump=0;
   for(let i=0;i<waves;i++){const w=(p-.1-i*(vak?.2:0))/(vak?.19:.6);if(w>0&&w<1.2){draw+=`<ellipse cx="320" cy="135" rx="${w*285}" ry="${w*170}" fill="none" stroke="${vak&&i===3?'#ffc477':red}" stroke-width="${vak&&i===3?8:4}" opacity="${w<1?1:0}"/>`;jump=Math.max(jump,Math.max(0,1-Math.abs(w-.72)*5)*49);}}
   draw+=player(320,vak?256:lerp(256,205,ease((p-.76)/.18)),'1',jump,jump>0)+txt(485,306,vak?(p>.7?t('FINAL BLAST','마지막 후속타'):t('3 RINGS','고리 3번')):t('JUMP','점프'),green);
  } else if(k==='track'){
   draw=`<ellipse cx="320" cy="180" rx="240" ry="133" fill="#2473a824"/>`+line(230,165,470,190,blue)+boss(lerp(215,456,move),lerp(148,177,move),p>.25&&p<.8?.35:1)+player(lerp(195,445,move),lerp(286,283,move)) +txt(320,60,t('FOLLOW THE HEAD','머리 방향을 따라'),blue);
   for(let i=0;i<3;i++)draw+=circle(lerp(215,456,move)-i*20,lerp(148,177,move),6,'#93caff40');
  } else if(k==='stack'||k==='spread'){
   draw=boss(320,86);const stack=k==='stack',from=stack?[[190,225],[455,285],[465,166]]:[[295,240],[326,240],[310,273]],to=stack?[[295,245],[338,245],[316,278]]:[[144,220],[481,210],[328,332]];
   if(stack)draw+=circle(320,250,55,'#ea628222',red)+player(320,220,'1',0,hit>0);
   from.forEach((a,i)=>{const x=lerp(a[0],to[i][0],move),y=lerp(a[1],to[i][1],move);draw+=line(...a,...to[i])+player(x,y,String(i+(stack?2:1)),0,move>.98);if(!stack)draw+=circle(x,y,hit*47,'#ef769930',red);});if(stack)draw+=circle(320,250,hit*56,'#ef769960');
  } else if(k==='fan'){
   draw=boss(295,110)+`<path d="M295 135 170 325H420Z" fill="#e45b7624" stroke="${red}" stroke-dasharray="6 6"/>`+player(lerp(325,490,move),lerp(263,277,move),'1',0,move>.95);
   if(p>.6)for(let i=0;i<5;i++){let f=clamp((p-.6)/.25);draw+=line(lerp(295,184+i*54,f),lerp(138,316,f),lerp(295,184+i*54,f)+3,lerp(138,316,f)+13,red);}
  } else if(k==='rescue'){
   draw=boss(320,75)+player(377,220,'1',0,p>.83)+player(lerp(183,284,move),lerp(282,243,move),'2');
   if(p>.18&&p<.84)draw+=circle(377,220,42,'#a5c95120','#adce71')+`<path d="m354 201 47 38m-44 0 42-41m-21-11 2 64" stroke="#b3db79" stroke-width="4"/>`;
   if(p>.5&&p<.85)draw+=line(288,240,362,223,green)+circle(lerp(288,362,(p*6)%1),lerp(240,223,(p*6)%1),5,green);
  } else if(k==='prison'){
   draw=boss(320,200);for(let i=0;i<10;i++){const angle=i/10*Math.PI*2,redRock=i===2,x=320+Math.cos(angle)*116,y=200+Math.sin(angle)*110;if(redRock&&p>.57)continue;draw+=`<rect x="${x-15}" y="${y-17}" width="30" height="34" rx="7" fill="${redRock?'#9b465b':'#3c4c65'}" stroke="${redRock?'#ffb0b8':'#6a7f9b'}" stroke-width="3"/>`;}
   if(p>.64)draw+=circle(320,200,hit*111,'#ee618044');draw+=player(lerp(353,368,ease((p-.6)/.21)),lerp(252,352,ease((p-.6)/.21)),'1',0,p>.8);if(p>.28&&p<.57)draw+=line(354,265,357,292,red);
  } else if(k==='walls'){
   draw=boss(320,62);const x=lerp(320,230,ease((p-.12)/.35)),y=lerp(100,350,ease((p-.15)/.7));
   draw+=`<path d="M75 ${y}H185M275 ${y}H565" stroke="#ec8a65" stroke-width="15" opacity=".82"/>`;
   if(p>.85)draw+=`<path d="M75 95H365M455 95H565" stroke="#ec8a65" stroke-width="12" opacity=".4"/>`;
   draw+=player(x,294,'1')+txt(320,365,t('MOVE THROUGH THE GAP','빈틈으로 통과'),green);
  } else if(k==='intercept'){
   draw=boss(112,185)+line(145,185,518,185,red)+player(520,185,'1')+circle(520,185,26,'none',red)+player(310,lerp(303,185,move),'2',0,move>.98);
   if(p>.65)draw+=boss(lerp(145,280,clamp((p-.65)/.18)),185,.7);if(p>.83)draw+=txt(310,123,t('NEXT: SWITCH','다음은 교대'),'#ffe0a0');
  } else if(k==='circles'){
   draw+=circle(174,192,107,'#e35d7822',red)+circle(463,192,59,'#b485ef20','#c7a2f5')+player(174,192,'1')+player(463,171,'2')+player(lerp(305,440,move),lerp(307,209,move),'3',0,move>.98)+player(lerp(574,481,move),lerp(306,209,move),'4',0,move>.98)+txt(174,51,t('LARGE: SOLO','큰 원: 혼자'),red)+txt(463,51,t('SMALL: TOGETHER','작은 원: 함께'),'#d0b2f6');if(hit)draw+=circle(174,192,hit*107,'#ed719333')+circle(463,192,hit*59,'#c397ef33');
  } else if(k==='orb'){
   draw=boss(100,182)+circle(317,182,38,'#4763b055',blue)+line(131,182,533,182,blue)+player(lerp(495,542,move),lerp(307,182,move),'1',0,move>.98)+txt(317,245,t('ENERGY','에너지'),blue);
   if(p>.5){const shot=((p-.5)*6)%1;draw+=circle(lerp(132,317,shot),182,8,'#ffc29f');draw+=txt(445,117,`${Math.min(3,Math.floor((p-.5)*6)+1)} / 3`, '#ffdfb8');}
  }
  s.box.querySelector('[data-battle-scene]').innerHTML=arena+draw;
  s.box.querySelector('[data-animation-caption]').textContent=s.captions[phase];s.box.querySelector('[data-animation-phase]').textContent=`0${phase+1} / 03`;s.box.querySelector('[data-animation-seek]').value=Math.floor(p*1000);s.box.dataset.stage=String(phase);
 }
 function sync(s){const btn=s.box.querySelector('[data-animation-toggle]');btn.textContent=s.playing?'Ⅱ':'▶';btn.setAttribute('aria-label',s.playing?t('Pause animation','애니메이션 일시정지'):t('Play animation','애니메이션 재생'));s.box.dataset.playing=String(s.playing);}
 states.forEach(s=>{s.box.querySelector('[data-animation-toggle]').addEventListener('click',()=>{s.playing=!s.playing;sync(s);});s.box.querySelector('[data-animation-replay]').addEventListener('click',()=>{s.p=0;s.playing=true;sync(s);paint(s);});s.box.querySelector('[data-animation-speed]').addEventListener('change',e=>s.speed=Number(e.target.value));s.box.querySelector('[data-animation-seek]').addEventListener('input',e=>{s.p=Number(e.target.value)/1000;s.playing=false;sync(s);paint(s);});sync(s);paint(s);});
 const observer='IntersectionObserver' in window?new IntersectionObserver(entries=>entries.forEach(e=>{const s=states.find(s=>s.box===e.target);s.visible=e.isIntersecting;}),{threshold:.05}):null;states.forEach(s=>observer?.observe(s.box));
 document.addEventListener('codex:mechanic-change',()=>states.forEach(s=>{if(!s.box.closest('[hidden]')){s.p=0;paint(s);}}));
 let last=0;function tick(now){const dt=Math.min(70,now-last)/1000;last=now;states.forEach(s=>{if(s.playing&&s.visible&&!document.hidden&&!s.box.closest('[hidden]')){s.p=(s.p+dt*s.speed/10)%1;paint(s);}});requestAnimationFrame(tick);}if(states.length)requestAnimationFrame(tick);
})();

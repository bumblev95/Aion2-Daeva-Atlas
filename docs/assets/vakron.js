/* Original response-order illustrations. Geometry and timing are not measured. */
(() => {
 'use strict';
 window.vakronFrame = (kind,p,ko) => {
  const t=(en,kr)=>ko?kr:en,green='#7de4bb',red='#ff9aac',blue='#b7d0ff';
  const txt=(x,y,s,c=blue)=>`<text x="${x}" y="${y}" text-anchor="middle" fill="${c}" font-size="32" font-family="system-ui,sans-serif">${s}</text>`;
  const dot=(x,y,n,c=green)=>`<circle cx="${x}" cy="${y}" r="24" fill="#18313d" stroke="${c}" stroke-width="3"/>${txt(x,y+10,n,c)}`;
  const boss=(x,y)=>`<path d="M${x} ${y-34}l32 18v34l-32 20-32-20v-34Z" fill="#54273e" stroke="${red}" stroke-width="3"/>`;
  const arrow=(d)=>`<path d="${d}" fill="none" stroke="${green}" stroke-width="5" marker-end="url(#vk-arrow)"/>`;
  let draw='<defs><marker id="vk-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7de4bb"/></marker></defs>';
  const phase=Math.min(2,Math.floor(p*3));
  if(kind==='vk-debuff'){
   draw+=txt(320,65,t('STACKS → STONE','중첩 → 정령석'));
   [0,1,2].forEach(i=>{draw+=`<rect x="${170+i*55}" y="100" width="40" height="30" rx="8" fill="${phase===2?'#243249':red}"/>`;});
   if(phase<2)draw+=`<path d="M425 130l35 55-35 55-35-55Z" fill="#337b77" stroke="${green}" stroke-width="4"/>`+arrow('M150 185H378')+dot(150+Math.min(1,p*1.5)*270,185,'1');
   else draw+=dot(170,245,'2')+arrow('M208 238L342 219')+dot(380,210,'1',blue)+txt(320,346,t('HIT ALLY TO FREE','동료 공격으로 구출'));
  }else if(kind==='vk-hands'){
   const switched=p>.66;
   draw+=`<path d="${switched?'M320 82H568V324H320Z':'M72 82H320V324H72Z'}" fill="#e7617b40" stroke="${red}" stroke-dasharray="9 8"/>`+boss(320,175)+txt(320,48,t('HAND UP: MOVE','손을 들면 이동'),red);
   const x=switched?440-(p-.66)/.34*245:185+Math.min(1,p/.5)*245;
   draw+=`<path d="M320 142L${switched?380:260} 92" stroke="${red}" stroke-width="14" stroke-linecap="round"/>`+dot(x,265,'1')+arrow(switched?'M440 215H185':'M185 215H440');
   draw+=txt(320,355,t('NEXT HAND → OTHER HALF','다음 손 → 반대쪽'),green);
  }else if(kind==='vk-flowers'){
   draw+=boss(320,164);
   if(phase===0){draw+=`<circle cx="320" cy="266" r="28" fill="#ae5579" stroke="${red}" stroke-width="4"/>`+txt(320,55,t('BREAK FLOWER','꽃 파괴'),red);}
   else{
    const angle=-Math.PI/2+Math.max(0,(p-.4)/.6)*Math.PI*1.25;
    const x=320+Math.cos(angle)*190,y=208+Math.sin(angle)*112;
    for(let i=0;i<5;i++){
     const a=-Math.PI/2+i*.32;
     if(a<angle-.20)draw+=`<circle data-puddle cx="${320+Math.cos(a)*190}" cy="${208+Math.sin(a)*112}" r="30" fill="#ed87985a" stroke="${red}"/>`;
     
    }
    draw+=`<circle cx="${x}" cy="${y}" r="39" fill="#18313d" stroke="${green}" stroke-width="4"/>`+txt(x,y+10,'5',green)+arrow('M370 86Q566 119 523 248')+txt(320,55,t('CLOCKWISE TOGETHER','함께 시계 방향'),green);
   }

  }else if(kind==='vk-glide'){
   draw+=`<path d="M45 300H195V340H45ZM445 225H592V270H445Z" fill="#345b56" stroke="${green}" stroke-width="3"/>`+arrow('M158 282Q280 73 476 210');
   draw+=dot(155+p*335,285-75*p-Math.sin(p*Math.PI)*120,'1');
   draw+=txt(320,56,t('CURRENT → GLIDE','상승 기류 → 활강'),green)+txt(320,355,t('RELEASE W / NO DODGE','W 놓기 / 공중 회피 금지'),red);
  }else if(kind==='vk-petrify'){
   draw+=boss(320,110)+dot(405,246,'1',phase<2?'#d2c7ae':green);
   if(phase<2)draw+=`<circle cx="405" cy="246" r="48" fill="#acb5c328" stroke="${red}" stroke-dasharray="8 6"/>`;
   draw+=dot(155+p*120,274,'2')+arrow('M290 270L364 250');
   draw+=txt(320,54,t('PETRIFIED ALLY','석화된 동료'),red)+txt(320,355,t('HIT BEFORE THE SLAM','내려찍기 전에 공격'),green);
  }else if(kind==='vk-shield'){
   const magic=phase===2,color=magic?'#d6b2ff':red;
   draw+=boss(320,185)+`<circle cx="320" cy="185" r="75" fill="${color}20" stroke="${color}" stroke-width="5"/>`+txt(320,54,magic?t('PURPLE SHIELD','보라 보호막'):t('RED SHIELD','빨강 보호막'),color);
   draw+=txt(320,320,magic?t('STOP MAGIC','마법 공격 중단'):t('STOP PHYSICAL','물리 공격 중단'),color);
   draw+=txt(320,363,t('MATCHING HITS HEAL','해당 피해는 보스 회복'),red);
  }else if(kind==='vk-elements'){
   draw+=txt(320,50,t('MATCH 1 → 1, 2 → 2…','같은 원소끼리 배치'),green);
   [0,1,2,3].forEach(i=>{const x=115+i*135;draw+=dot(x,125,String(i+1),blue)+arrow(`M${x} 165V240`)+`<rect x="${x-38}" y="262" width="76" height="62" rx="8" fill="#1e4543" stroke="${green}" stroke-width="3"/>`+txt(x,304,String(i+1),green);});
   draw+=txt(320,369,t('SCHEMATIC, NOT A MAP','대응 순서 · 실제 지도 아님'));
  }else if(kind==='vk-jumps'){
   draw+=boss(320,154)+`<ellipse cx="320" cy="194" rx="270" ry="155" fill="#e7617b30" stroke="${red}"/>`;
   const wave=(p*3)%1,n=Math.min(3,Math.floor(p*3)+1),a=-1+p*2.5;
   const x=320+Math.cos(a)*178,y=208+Math.sin(a)*98,jump=Math.sin(wave*Math.PI)*55;
   draw+=`<ellipse cx="320" cy="194" rx="${wave*270}" ry="${wave*155}" fill="none" stroke="${red}" stroke-width="4"/>`+dot(x,y-jump,'1')+arrow('M400 99Q542 155 470 257');
   draw+=txt(320,52,t('JUMP','점프')+' '+n+' / 3',green)+txt(320,357,t('THIRD: WATCH CAST BAR','세 번째: 시전 바 확인'),green);
  }else if(kind==='vk-rock'){
   const escaped=p>.7;
   for(let i=0;i<8;i++){
    const target=i===2,a=i*Math.PI/4,x=320+Math.cos(a)*105,y=210+Math.sin(a)*95;
    if(target&&p>.60)continue;
    draw+=`<rect data-vk-rock="${target?'red':'ordinary'}" x="${x-23}" y="${y-22}" width="46" height="44" rx="7" fill="${target?'#9b465b':'#3c4c65'}" stroke="${target?red:blue}" stroke-width="3"/>`;
   }
   draw+=dot(320,escaped?260+(p-.7)*270:230,'1')+txt(320,52,t('BREAK YOUR RED ROCK','내 붉은 바위 파괴'),red);
   if(p>.6)draw+=arrow('M320 263V353');
  }
  return draw;
 };
 function reveal(){
  const target=document.getElementById(location.hash.slice(1));
  if(!target?.closest('.vk-guide'))return;
  const stage=target.closest('.vk-stage');
  if(stage){stage.open=true;target.scrollIntoView({block:'start'});}
 }
 document.addEventListener('DOMContentLoaded',()=>{reveal();document.querySelector('[data-vakron-guide]').dataset.ready='true';});
 window.addEventListener('hashchange',reveal);
})();

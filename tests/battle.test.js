// Exercise the shipped player and renderer without loading a browser or media.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync('assets/battle.js','utf8');
const html = fs.readFileSync('docs/dungeons/index.html','utf8');
const decode = s => s.replace(/&quot;/g,'"').replace(/&#x27;/g,"'").replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
const fixtures = [...html.matchAll(/data-animation="([^"]+)" data-encounter="([^"]+)" data-captions="([^"]+)"/g)]
  .map(([,kind,id,captions])=>({kind,id,captions:decode(captions)}));
assert.equal(fixtures.length,16,'Test the real generated set of 16 lessons');

class Node {
  constructor(){this.attrs={};this.listeners={};this.value='';this.textContent='';this.innerHTML='';}
  setAttribute(k,v){this.attrs[k]=String(v);}
  addEventListener(event,fn){this.listeners[event]=fn;}
  emit(event,value){this.listeners[event]({target:{value}});}
}
function start({reduced=false,lang='en'}={}) {
  let raf,observe,motionChange;
  const handlers={};
  const boxes=fixtures.map(f=>{
    const box=new Node();
    box.dataset={animation:f.kind,encounter:f.id,captions:f.captions};
    box.hidden=false;
    box.nodes={};
    for(const name of ['battle-scene','animation-caption','animation-phase','animation-seek','animation-toggle','animation-replay','animation-speed'])box.nodes[name]=new Node();
    box.querySelector=selector=>box.nodes[selector.slice(6,-1)];
    box.closest=()=>box.hidden?box:null;
    return box;
  });
  const document={documentElement:{lang},hidden:false,querySelectorAll:()=>boxes,addEventListener:(event,fn)=>handlers[event]=fn};
  const motion={matches:reduced,addEventListener:(event,fn)=>motionChange=fn};
  class Observer {constructor(fn){observe=fn;}observe(){}}
  vm.runInNewContext(source,{document,window:{IntersectionObserver:Observer},IntersectionObserver:Observer,
    matchMedia:()=>motion,requestAnimationFrame:fn=>raf=fn});
  const box=id=>boxes.find(b=>b.dataset.encounter===id);
  const seek=(id,p)=>{const b=box(id);b.nodes['animation-seek'].emit('input',p*1000);return b.nodes['battle-scene'].innerHTML;};
  return {boxes,box,seek,document,handlers,tick:time=>raf(time),
    visibility:(id,visible)=>observe([{target:box(id),isIntersecting:visible}]),
    reduce:()=>motionChange({matches:true})};
}

let run=start();
for(const b of run.boxes){
  assert.equal(b.dataset.playing,'true','Default autoplay remains on');
  assert.equal(b.nodes['animation-toggle'].attrs['aria-label'],'Pause animation');
  const id=b.dataset.encounter;
  for(let step=0;step<=100;step++){
    const svg=run.seek(id,step/100);
    assert.ok(svg.includes('<ellipse'),'Every frame includes the arena');
    assert.ok(!/NaN|undefined|Infinity|v--/.test(svg),`${id}: no invalid geometry at ${step}`);
    assert.equal(b.dataset.playing,'false','Scrubbing pauses');
    assert.ok(b.nodes['animation-seek'].attrs['aria-valuetext'].includes('/ 3:'),'Progress has a readable phase description');
  }
}

assert.ok(!run.seek('berk-cover',.63).includes('Protection buff'),'Reaching the rock does not immediately establish protection');
assert.ok(run.seek('berk-cover',.72).includes('Protection buff'),'Protection is checked before the blast');
assert.ok(run.seek('auldor-stack',.1).includes('AIRBORNE BOSS · RED MARK'),'The landing lesson identifies both real cues');

const ringIds=new Set();
let followUp=false;
for(let step=0;step<100;step++){
  const svg=run.seek('vakron-rings',step/100);
  for(const [,n] of svg.matchAll(/data-wave="(\d+)"/g))ringIds.add(n);
  followUp ||= svg.includes('data-binding-follow-up');
  assert.ok(svg.includes('LINES: SIDESTEP'),'Rings also show line avoidance');
  assert.ok(svg.includes('data-red-floor'),'The lesson shows the red-floor cue');
}
assert.deepEqual([...ringIds].sort(),['1','2','3']);
assert.ok(followUp,'A separate arena-wide follow-up follows the third ring');
assert.ok(!run.seek('vakron-rings',.83).includes('data-wave="4"'),'Follow-up is not a fourth ring');

const before=run.seek('vakron-prison',.52),opened=run.seek('vakron-prison',.60),after=run.seek('vakron-prison',.95);
assert.ok(before.includes('data-rock="red"'));
assert.ok(!opened.includes('data-rock="red"'),'The exit opens before movement');
assert.ok(opened.includes('cx="320" cy="252"'),'Player waits inside until the rock is gone');
assert.ok(after.includes('cx="320" cy="352"'),'Exit is through the destroyed rock, not another wall');
assert.ok(after.includes('STAGGER LOCKED'),'Do not promise stagger unlock at an invented time');

assert.ok(run.seek('kromede-bow',.53).includes('BURST 1 / 2'));
assert.ok(run.seek('kromede-bow',.81).includes('BURST 2 / 2'));
assert.ok(run.seek('kromede-clones',.8).includes('TWO CLONE HITS: STAY SPREAD'));
for(const [wall,start] of [[1,.10],[2,.53]]){
  const crossing=start+.43*(294-84)/(381-84);
  const svg=run.seek('kromede-walls',crossing);
  const gap=Number(svg.match(new RegExp(`data-wall="${wall}" data-gap="([0-9]+)"`))[1]);
  const playerX=Number([...svg.matchAll(/<circle cx="([0-9.]+)" cy="294"/g)].at(-1)[1]);
  assert.ok(Math.abs(playerX-gap)+15<45,'Player must fit in each gap when the wall reaches them');
}
const orb=run.seek('nuakum-orb',.75);
assert.ok(orb.includes('3 HITS / 4 OPPORTUNITIES'));
assert.ok(orb.includes('RE-ALIGN EACH SHOT'));
assert.ok(orb.includes('DARK ZONE: KEEP OUT'));
for(const p of [.1,.5,.9])assert.ok(run.seek('bakarma-dive',p).includes('transform="translate(320 167)"'),'The observation lesson must not animate an invented dive path');

run=start();
const normal=run.box('berk-cover'),fast=run.box('berk-spin');
fast.nodes['animation-speed'].emit('change','2');
run.tick(50);
const position=b=>Number(b.nodes['animation-seek'].value);
assert.equal(position(fast),position(normal)*2,'Speed control changes playback rate');
normal.nodes['animation-toggle'].emit('click');
const paused=position(normal);run.tick(100);
assert.equal(position(normal),paused,'Pause stops progress');
assert.equal(normal.nodes['animation-toggle'].attrs['aria-label'],'Play animation');
normal.nodes['animation-replay'].emit('click');
assert.equal(position(normal),0);assert.equal(normal.dataset.playing,'true');
run.visibility('berk-cover',false);run.tick(150);
assert.equal(position(normal),0,'Offscreen playback does not advance');
run.visibility('berk-cover',true);normal.hidden=true;run.tick(200);
assert.equal(position(normal),0,'Hidden tabs do not advance');
normal.hidden=false;run.document.hidden=true;run.tick(250);
assert.equal(position(normal),0,'Background documents do not advance');
run.document.hidden=false;run.tick(300);assert.ok(position(normal)>0);
run.handlers['codex:mechanic-change']();assert.equal(position(normal),0,'Selecting a mechanic restarts its lesson');

run=start({reduced:true,lang:'ko'});
for(const b of run.boxes)assert.equal(b.dataset.playing,'false','Reduced motion disables initial autoplay');
run.tick(50);assert.equal(position(run.box('berk-cover')),0);
assert.equal(run.box('berk-cover').nodes['animation-toggle'].attrs['aria-label'],'애니메이션 재생');
run.box('berk-cover').nodes['animation-toggle'].emit('click');
run.tick(100);assert.ok(position(run.box('berk-cover'))>0,'Explicit playback remains available');
run.reduce();assert.equal(run.box('berk-cover').dataset.playing,'false','New reduced-motion preference pauses existing playback');

console.log('PASS: all 16 renderers, wave/follow-up separation, exit geometry, repeated hits, moving gaps, orb goal, controls, visibility and reduced motion.');

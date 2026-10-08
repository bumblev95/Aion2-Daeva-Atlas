const assert = require('node:assert/strict');
const {simulate,downtime,conditionKey,exportCSV} = require('../assets/dps-engine.js');
const skill=(x={})=>({id:'a',name:'A',enabled:true,flat:100,coefficient:0,hits:1,cast:1,cooldown:0,afterCooldown:0,delta:0,...x});
const model=(x={})=>({region:'NA',patch:'test',duration:10,attack:100,crit:0,critMultiplier:1.5,accuracy:100,factor:1,downtime:'',skills:[skill()],...x});

// Exactly ten completed casts fit into ten seconds; no free hit at t=0.
assert.equal(simulate(model()).total,1000);
assert.equal(simulate(model()).edps,100);
assert.equal(simulate(model({crit:50,accuracy:80,factor:2,skills:[skill({coefficient:100,hits:2})]})).edps,800);
// Downtime reduces whole-fight eDPS, while overlaps count only once.
assert.deepEqual(downtime('2-4, 3-5, 5-6',10),[[2,6]]);
let r=simulate(model({downtime:'2-4, 3-5, 5-6'}));
assert.equal(r.total,600);assert.equal(r.edps,60);assert.equal(r.activeDps,100);assert.equal(r.activeTime,6);
r=simulate(model({downtime:'0-10'}));assert.equal(r.total,0);assert.equal(r.activeDps,0);
// Casts crossing an invulnerability window are excluded; cooldown clocks continue.
r=simulate(model({downtime:'2-4',skills:[skill({cast:3,cooldown:6})]}));
assert.deepEqual(r.events.map(e=>e.time),[7]);
// Two skills share one action timeline. A prioritized cooldown attack uses filler between casts.
r=simulate(model({skills:[skill({flat:300,cooldown:3,afterCooldown:3}),skill({id:'b',flat:100})]}));
assert.deepEqual(r.breakdown.map(x=>x.casts),[4,6]);assert.equal(r.total,1800);
// A 50% nerf applies to that skill, not to the entire class. Cooldown changes rerun the timeline.
const patch=model({skills:[skill({flat:300,cooldown:3,afterCooldown:5,delta:-50}),skill({id:'b'})]});
assert.equal(simulate(patch).total,1800);assert.equal(simulate(patch,true).total,1100);
assert.equal(simulate(model({skills:[skill({delta:-100})]}),true).total,0);
for(const bad of [{duration:0},{crit:101},{downtime:'8-7'},{downtime:'0-11'},{downtime:'garbage'},{skills:[]},{skills:[skill({cast:0})]},{attack:NaN}])assert.throws(()=>simulate(model(bad)));
assert.equal(conditionKey(model({downtime:'3-5,2-4'})),conditionKey(model({downtime:'2-5'})));
assert.notEqual(conditionKey(model()),conditionKey(model({patch:'other'})));
assert.notEqual(conditionKey(model()),conditionKey(model({region:'KR'})));
// Actual source catalog regressions: no prerequisite is equivalent to no casts,
// even if the cooldown, attack and critical probabilities are otherwise ready.
const db=require('../docs/data/dps.json');
const source=id=>{const s=db.classes.flatMap(c=>c.candidates).find(x=>x.id===id);return skill({...s,name:s.en,flat:100});};
for(const id of ['burst-arrow','condemnation','blaze','judgment','dark-crush','heart-gore','dimensional-control','elemental-fusion']) {
  assert.equal(simulate(model({skills:[source(id)]})).total,0,id+' must not cast without its prerequisite');
}
for(const state of ['slow','root']) {
  r=simulate(model({stateWindows:{[state]:'2-3'},skills:[source('burst-arrow')]}));
  assert.deepEqual(r.events.map(e=>e.time),[3],state+' satisfies the OR condition');
}
assert.equal(simulate(model({stateWindows:{stun:'0-10'},skills:[source('burst-arrow')]})).total,0);
// Start is inclusive, expiry is exclusive. Conditions are checked at cast start.
const gated=skill({requires:['slow']});
r=simulate(model({stateWindows:{slow:'2-4'},skills:[gated]}));
assert.deepEqual(r.events.map(e=>e.time),[3,4]);
assert.equal(simulate(model({stateWindows:{slow:'0-2'},downtime:'0-3',skills:[gated]})).total,0);
const slow=skill({id:'setup',flat:0,cooldown:10,afterCooldown:10,effects:[{state:'slow',duration:2,chance:100,on:'hit'}]});
r=simulate(model({targetControl:'susceptible',skills:[gated,slow]}));
assert.deepEqual(r.events.filter(e=>e.skill==='a').map(e=>e.time),[2,3]);
for(const x of [{targetControl:'unknown'},{targetControl:'immune'},{targetControl:'susceptible',accuracy:99},{targetControl:'susceptible',conditionMode:'windows'}]) {
  assert.equal(simulate(model({...x,skills:[gated,slow]})).breakdown[0].casts,0);
}
// A verified external window can be used at partial hit chance; it is an input,
// not a state manufactured from expected hit probability.
assert.equal(simulate(model({accuracy:50,stateWindows:{slow:'0-2'},skills:[gated]})).total,100);
for(const badEffect of [{duration:null,chance:100},{duration:2,chance:null},{duration:2,chance:50}]) {
  const setup=skill({...slow,effects:[{state:'slow',on:'use',...badEffect}]});
  assert.equal(simulate(model({skills:[gated,setup]})).breakdown[0].casts,0);
}
// Source duration 5s can enable Blaze after a Fire hit, but Blaze cannot bootstrap
// its own prerequisite. The passive's 20% extra-damage proc is never added.
const fire=source('flame-arrow'),blaze=source('blaze');
r=simulate(model({skills:[blaze,fire]}));assert.ok(r.breakdown[0].casts>0);assert.equal(r.events[0].skill,'flame-arrow');
assert.equal(simulate(model({fireMarkEnabled:'no',skills:[blaze,fire]})).breakdown[0].casts,0);
assert.equal(simulate(model({region:'KR',skills:[blaze,fire]})).breakdown[0].casts,0);
assert.equal(simulate(model({conditionMode:'windows',stateWindows:{'fire-mark':'3-4'},skills:[blaze]})).events[0].time,4);
// Chain windows need an opener, expire during downtime, and are not merely CDs.
const opener=source('shield-smite'),follow=skill({...source('judgment'),cooldown:0,afterCooldown:0});
r=simulate(model({duration:5,skills:[follow,opener]}));assert.equal(r.breakdown[0].casts,1);
r=simulate(model({duration:5,skills:[skill({...follow,chainMode:'window'}),opener]}));assert.equal(r.breakdown[0].casts,2);
r=simulate(model({duration:5,downtime:'1-3',skills:[follow,opener]}));assert.equal(r.breakdown[0].casts,0);
const chainPatch=model({duration:10,skills:[follow,skill({...opener,afterCooldown:4})]});
assert.ok(simulate(chainPatch,true).breakdown[0].casts>simulate(chainPatch).breakdown[0].casts);
const torment=source('chain-of-torment'),condemnation=source('condemnation');
assert.equal(simulate(model({skills:[condemnation,torment]})).breakdown[0].casts,0,'DoT lifetime is not verified prerequisite lifetime');
assert.ok(simulate(model({stateWindows:{'chain-of-torment':'1-6'},skills:[condemnation,torment]})).breakdown[0].casts>0);
// MP costs are checked before cast, restoration cannot fund the same cast,
// and unknown costs never silently become zero when a budget is enabled.
const budget={resourceMode:'budget',mpStart:100,mpMax:100,mpRegen:0};
r=simulate(model({...budget,skills:[skill({mpCost:60})]}));assert.equal(r.breakdown[0].casts,1);assert.equal(r.mp,40);
r=simulate(model({...budget,mpStart:0,mpRegen:10,skills:[skill({mpCost:20})]}));assert.deepEqual(r.events.map(e=>e.time),[3,5,7,9]);
r=simulate(model({...budget,mpStart:0,mpRegen:10,downtime:'2-8',skills:[skill({mpCost:20})]}));assert.deepEqual(r.events.map(e=>e.time),[9,10]);
r=simulate(model({...budget,skills:[skill({mpCost:null})]}));assert.equal(r.total,0);assert.deepEqual(r.breakdown[0].blocked,['mp-unverified']);
assert.equal(simulate(model({...budget,mpStart:0,skills:[skill({mpCost:10,mpGain:100})]})).total,0);
r=simulate(model({...budget,mpStart:0,skills:[skill({mpCost:50}),skill({id:'filler',flat:0,mpCost:0,mpGain:50})]}));assert.equal(r.events[0].skill,'filler');assert.ok(r.breakdown[0].casts>0);
r=simulate(model({...budget,mpStart:0,accuracy:50,skills:[skill({mpCost:50}),skill({id:'filler',flat:0,mpCost:0,mpGain:50})]}));assert.equal(r.breakdown[0].casts,0);
assert.ok(simulate(model()).warnings.includes('resources-unverified'));
// Spirit timings are explicit inputs. Four events enable one Fusion, and each
// cast spends all four; stacks cap at four and excess events are not banked.
const fusion=source('elemental-fusion');
r=simulate(model({elementEvents:'0,1,2,3,4,5,6,7',skills:[fusion]}));assert.deepEqual(r.events.map(e=>e.time),[4,8]);
r=simulate(model({elementsStart:4,skills:[fusion]}));assert.equal(r.breakdown[0].casts,1);assert.equal(r.elements,0);
r=simulate(model({elementEvents:'0,0,0,0,0',skills:[fusion]}));assert.equal(r.breakdown[0].casts,1);
for(const bad of [{stateWindows:{slow:'8-7'}},{stateWindows:{slow:'0-11'}},{elementEvents:'bad'},{elementEvents:'11'},
  {conditionsVerified:false},{elementsStart:1.5},{resourceMode:'budget',mpStart:101,mpMax:100,mpRegen:0},
  {...budget,skills:[skill({mpCost:-1})]}, {...budget,skills:[skill({mpCost:NaN})]}])assert.throws(()=>simulate(model(bad)));
// Optional extra effects must not turn an ordinary direct hit into a gated hit.
for(const id of ['drill-dart','ambush','marking-shot','suppressing-arrow'])assert.deepEqual(source(id).requires,[]);
// Common comparison conditions include all external windows and resource
// assumptions, normalized independently of object order and overlapping windows.
assert.equal(conditionKey(model({stateWindows:{slow:'3-5,2-4',root:''}})),conditionKey(model({stateWindows:{slow:'2-5'}})));
assert.notEqual(conditionKey(model()),conditionKey(model({stateWindows:{slow:'0-5'}})));
assert.notEqual(conditionKey(model()),conditionKey(model(budget)));
assert.notEqual(conditionKey(model(budget)),conditionKey(model({...budget,mpStart:50})));
assert.notEqual(conditionKey(model()),conditionKey(model({targetControl:'susceptible'})));
assert.notEqual(conditionKey(model()),conditionKey(model({elementEvents:'1,2,3,4'})));
// CSV retains reconstructable condition metadata and safe quoted labels.
const csvInput=model({...budget,stateWindows:{slow:'0-5'},skills:[skill({name:'=unsafe',requires:['slow'],mpCost:60})]});
const csv=exportCSV(csvInput,{before:simulate(csvInput),after:simulate(csvInput,true)});
assert.ok(csv.startsWith('\uFEFF'));assert.ok(csv.includes('"stateWindows","{""slow"":""0-5""}"'));
assert.ok(csv.includes('"\'=unsafe"'));assert.ok(csv.includes('requires_any'));assert.ok(csv.includes('"[""slow""]"'));
assert.ok(csv.includes('before_casts'));assert.ok(csv.includes('mp_cost'));
console.log('DPS tests passed: original damage math plus state, chain, uncertain hit/proc, MP, stack, comparison and CSV regressions.');

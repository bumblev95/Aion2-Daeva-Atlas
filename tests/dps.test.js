const assert = require('node:assert/strict');
const {simulate,downtime,conditionKey} = require('../assets/dps-engine.js');
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
console.log('DPS tests passed: shared timeline, boundaries, downtime, patch effects and comparison conditions.');

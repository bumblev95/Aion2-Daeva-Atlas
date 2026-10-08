'use strict';
const assert = require('node:assert/strict');
const {simulate,conditionKey,exportCSV} = require('../assets/dps-engine.js');
const skill=(x={})=>({id:'dot',name:'DoT',enabled:true,flat:100,coefficient:0,hits:1,cast:1,
  cooldown:100,afterCooldown:100,delta:0,periodic:[{flat:10,coefficient:0,interval:1,duration:5,firstTick:1}],...x});
const input=(x={})=>({duration:10,attack:100,crit:0,critMultiplier:1.5,accuracy:100,factor:1,
  downtime:'',periodicMode:'inputs',periodicRefresh:'replace',periodicCrit:'none',skills:[skill()],...x});
let r=simulate(input());
assert.equal(r.total,150);assert.equal(r.breakdown[0].ticks,5);
assert.deepEqual(r.events.map(e=>e.time),[1,2,3,4,5,6]);
assert.equal(r.breakdown[0].directDamage,100);assert.equal(r.breakdown[0].periodicDamage,50);
assert.equal(r.edps,15);
r=simulate(input({duration:3.5}));assert.equal(r.total,120,'No tail damage after fight end');
r=simulate(input({duration:6}));assert.equal(r.total,150,'A final tick at fight end counts once');
r=simulate(input({downtime:'3-5'}));assert.equal(r.total,130,'Ticks are lost during invulnerability, not delayed');
assert.deepEqual(r.events.map(e=>e.time),[1,2,5,6]);
assert.equal(r.activeTime,8);assert.equal(r.activeDps,130/8);
const refreshed=input({skills:[skill({cooldown:3,afterCooldown:3})]});
r=simulate(refreshed);assert.equal(r.total,490);assert.equal(r.breakdown[0].ticks,9);
r=simulate({...refreshed,periodicRefresh:'stack'});assert.equal(r.total,530);assert.equal(r.breakdown[0].ticks,13);
r=simulate(input({skills:[skill({periodic:[{flat:10,coefficient:0,interval:1,duration:5,firstTick:0}]})]}));
assert.equal(r.total,160);assert.deepEqual(r.events.slice(0,2).map(e=>e.time),[1,1]);
assert.equal(simulate(input({periodicMode:'omit'})).total,100);
assert.equal(simulate(input({accuracy:50})).total,50,'Unknown application/refresh cannot be approximated by a free DoT');
assert(simulate(input({accuracy:50})).warnings.includes('periodic-hit-unverified'));
assert.equal(simulate(input({crit:100,periodicCrit:'normal'})).total,225);
assert.equal(simulate(input({crit:100,periodicCrit:'none'})).total,200);
assert.equal(simulate(input({skills:[skill({delta:100})]}),true).total,300,'Patch damage changes direct and tick terms');
assert.equal(simulate(input({skills:[skill({requires:['slow']})]})).total,0,'Unavailable skills create no direct hit or periodic damage');
assert.equal(simulate(input({skills:[skill({mpCost:100})],resourceMode:'budget',mpStart:0,mpMax:100,mpRegen:0})).total,0);
assert.equal(simulate(input({region:'KR',skills:[skill({conditionRegion:'Global'})]})).total,100,'Global DoT does not silently enter KR');
assert.throws(()=>simulate(input({damageVerified:false})),/damage-snapshot/);
assert.throws(()=>simulate(input({skills:[skill({periodic:[{flat:10,coefficient:0,interval:0,duration:5}]})]})),/interval/);
assert.throws(()=>simulate(input({skills:[skill({periodic:[{flat:10,coefficient:0,interval:1,duration:5,firstTick:6}]})]})),/first tick/);
// Policy callbacks cannot change snapshotted damage or global tick options.
const mutable=input();r=simulate(mutable,false,ctx=>{
  mutable.skills[0].periodic[0].flat=100000;mutable.periodicCrit='normal';return ctx.feasible[0].index;
});assert.equal(r.total,150);
// A source charge/summon/trigger is unavailable until its input is confirmed.
for(const extra of [{charge:{},chargeConfirmed:false},{damageInputRequired:true,damageConfirmed:false}]) {
  assert.equal(simulate(input({skills:[skill(extra)]})).total,0);
  assert.throws(()=>simulate(input({skills:[skill(extra),skill({id:'filler',periodic:[],cooldown:0})]}),false,()=>0),/policy action/);
}
assert.equal(simulate(input({skills:[skill({charge:{},chargeConfirmed:true})]})).total,150);
// Source Insignia terms scale the Explosion at cast start; gain follows a
// confirmed hit, expires independently and does not grant a critical trigger.
const variants=Array.from({length:6},(_,stacks)=>({stacks,flat:100+stacks*10,coefficient:0}));
const insignia=input({duration:2,periodicMode:'omit',insigniaMode:'consume',skills:[
  skill({id:'engrave',flat:1,periodic:[],cooldown:100,insigniaGain:1,insigniaDuration:10}),
  skill({id:'explode',periodic:[],insigniaDamage:variants})]});
r=simulate(insignia);assert.equal(r.total,111);assert.equal(r.insignias,0);
assert.equal(simulate({...insignia,insigniaMode:'retain'}).insignias,1);
assert.equal(simulate({...insignia,insigniaMode:'unverified'}).total,1);
assert.equal(simulate({...insignia,accuracy:50}).total,50.5);
const expired={...insignia,skills:[{...insignia.skills[0],insigniaDuration:.5},insignia.skills[1]],duration:3};
r=simulate(expired,false,ctx=>ctx.time===1?{waitUntil:2}:ctx.feasible[0].index);
assert.equal(r.total,101,'Waiting cannot preserve expired Insignias');
const npc=input({duration:2,periodicMode:'omit',targetControl:'susceptible',skills:[
  skill({id:'opener',periodic:[],cooldown:0,afterCooldown:0,effects:[{state:'stun',duration:3,on:'hit',chance:60,npcChance:100}]}),
  skill({id:'followup',periodic:[],flat:1000,requires:['stun']})]});
const followupFirst=ctx=>ctx.feasible.find(x=>x.id==='followup')?.index??ctx.feasible[0].index;
assert.equal(simulate({...npc,targetType:'npc'},false,followupFirst).total,1100);
assert.equal(simulate({...npc,targetType:'player'},false,followupFirst).total,200);
assert.equal(simulate({...npc,targetType:'npc',targetControl:'immune'},false,followupFirst).total,200);
assert.equal(simulate({...npc,targetType:'npc',accuracy:50},false,followupFirst).total,100);
for(const change of [{periodicMode:'omit'},{periodicCrit:'normal'},{periodicRefresh:'stack'},
                    {insigniaMode:'consume'},{targetType:'npc'},{fireMarkEnabled:'no'}]) {
  assert.notEqual(conditionKey(input()),conditionKey(input(change)),'Comparison rejects different mechanics assumptions');
}
const csvInput=input(), before=simulate(csvInput), after=simulate(csvInput,true);
assert(exportCSV(csvInput,{before,after}).includes('before_periodic_damage'));
console.log('DPS math passed: exact ticks, refresh, downtime, truncation, conditional application, charge/summon input, Insignia and fair comparisons.');

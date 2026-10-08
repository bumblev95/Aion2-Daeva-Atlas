'use strict';
const assert = require('node:assert/strict');
const {simulate} = require('../assets/dps-engine.js');
const learning = require('../research/rotation-learning/train.js');
const skill = (x={}) => ({id:'basic',name:'Basic',enabled:true,flat:100,coefficient:0,hits:1,
  cast:1,cooldown:0,afterCooldown:0,delta:0,...x});
const raw = (x={}) => ({region:'NA',patch:'test',duration:10,attack:100,crit:0,critMultiplier:1.5,
  accuracy:100,factor:1,downtime:'',skills:[skill()],...x});

// A learned policy cannot create a prerequisite, MP or element stack.
for (const gated of [
  {requires:['slow']},
  {requires:['chain-of-torment']},
  {requires:['fire-mark']},
  {elementCost:4},
  {mpCost:100}
]) {
  const input = raw({resourceMode:'budget',mpStart:0,mpMax:0,mpRegen:0,
    skills:[skill({id:'conditional',mpCost:0,...gated}),skill({mpCost:0})]});
  assert.throws(() => simulate(input,false,() => 0), /policy action/);
  const result = learning.simulatePolicy(input,{order:['conditional','basic'],holdSeconds:2});
  assert.equal(result.breakdown[0].casts,0);
  assert.equal(result.total,1000);
}
const closed = raw({accuracy:50,skills:[
  skill({id:'provider',cooldown:5,effects:[{state:'slow',duration:2,chance:100,on:'hit'}]}),
  skill({id:'conditional',requires:['slow'],flat:10000})]});
assert.equal(learning.simulatePolicy(closed,{order:['conditional','provider'],holdSeconds:0}).breakdown[1].casts,0);
const expiry=raw({stateWindows:{root:'0-0.7'},skills:[skill({id:'conditional',cast:0.25,cooldown:2,requires:['root']}),skill()]});
assert.equal(learning.simulatePolicy(expiry,{order:['conditional','basic'],holdSeconds:2}).breakdown[0].casts,1,'Waiting cannot extend an expired prerequisite');
const frozenOptions=raw({fireMarkEnabled:'no',skills:[
  skill({id:'conditional',requires:['fire-mark']}),
  skill({id:'provider',effects:[{state:'fire-mark',duration:5,chance:100,on:'hit',passive:'fire-mark'}]})]});
let result=simulate(frozenOptions,false,ctx=>{frozenOptions.fireMarkEnabled='yes';return ctx.feasible[0].index;});
assert.equal(result.breakdown[0].casts,0,'A policy cannot change snapshotted effect options');

// Explicit waiting is idle time, not a free hit, and cannot skip a gap boundary.
result = simulate(raw(),false,ctx => ctx.time < 4 ? {waitUntil:4} : ctx.feasible[0].index);
assert.equal(result.total,600);
assert.equal(result.events[0].time,5);
assert.throws(() => simulate(raw({downtime:'4-6'}),false,() => ({waitUntil:5})),/policy wait/);
for (const decision of [{waitUntil:0},{waitUntil:Infinity},{waitUntil:-1},999,null]) {
  assert.throws(() => simulate(raw(),false,() => decision));
}
assert.throws(() => simulate(raw(),false,ctx => {ctx.feasible[0].index=9;return 0;}),TypeError);

const burst = skill({id:'burst',cast:0.5,cooldown:2,afterCooldown:2,flat:500});
const filler = skill({id:'filler',cast:1.7,flat:1});
const toyClass = {id:'toy',skills:[burst,filler]};
const curriculum = {base:raw(),holdSeconds:[0,0.5,1,2],
  training:[{id:'train-a',duration:10.5},{id:'train-b',duration:14.5}],
  validation:[{id:'validation',duration:12.5}],test:[{id:'test',duration:22.5}]};
const settings = {seed:7,generations:8,population:64,eliteFraction:0.15,learningRate:0.65,pseudocount:0.5};
const evaluate = learning.evaluator(toyClass,curriculum);
const trained = learning.learn(toyClass,curriculum,[],settings,evaluate);
assert.equal(trained.policy.holdSeconds,2);
assert(trained.trainingScore > 1.15, 'Learn a useful hold beyond the initial greedy order');
assert.equal(trained.trainingScore,learning.restrictedOracle(toyClass,curriculum,evaluate).score);
assert.deepEqual(trained,learning.learn(toyClass,curriculum,[],settings));
assert(trained.trace.every((entry,i,array) => i===0 || entry.bestTrainingScore >= array[i-1].bestTrainingScore));
const poison = structuredClone(curriculum);
poison.validation[0].duration=1;
poison.test[0].duration=1;
assert.deepEqual(trained,learning.learn(toyClass,poison,[],settings),'Held-out values must not influence learning');
const moving = {...learning.buildInput(toyClass,curriculum,{duration:22.5,downtime:'4.1-8.4,14-16'})};
result=learning.simulatePolicy(moving,trained.policy);
for (const event of result.events) {
  const start=event.time-moving.skills.find(s=>s.id===event.skill).cast;
  assert(![[4.1,8.4],[14,16]].some(([a,b])=>start < b-1e-8 && event.time > a+1e-8));
}
assert.throws(() => learning.validatePolicy({order:['burst','burst'],holdSeconds:0},['burst','filler'],[0]),/exactly once/);
assert.throws(() => learning.validatePolicy({order:['burst','foreign'],holdSeconds:0},['burst','filler'],[0]),/foreign/);

const inputs=learning.loadInputs();
learning.validateInputs(inputs);
const assessment=learning.tierAssessment(inputs.catalog);
assert.equal(assessment.canPublishTiers,false);
assert.equal(assessment.tiers,null);
assert.deepEqual(assessment.directDamageCoverage,{included:72,active:96,omitted:24});
assert.deepEqual(assessment.remainingDamageAudit,{noDirectAttack:13,chargeInputRequired:4,summonOrTriggerInputRequired:7,knownPeriodicSkills:4});
for (const c of inputs.catalog.classes) {
  assert.deepEqual(learning.projectedHints(c,inputs.claims,false),[],'Unverified guides require explicit research opt-in');
  for (const scenario of inputs.curriculum.test) {
    const input=learning.buildInput(c,inputs.curriculum,scenario);
    const original=simulate(input);
    const sameOrder=learning.simulatePolicy(input,{order:c.skills.map(s=>s.id),holdSeconds:0});
    for (const key of ['total','edps','activeDps','activeTime','mp','elements','events','warnings']) {
      assert.deepEqual(sameOrder[key],original[key],`Preserve ${key} for ${c.id}`);
    }
    assert.deepEqual(sameOrder.breakdown.map(s=>[s.id,s.casts,s.damage]),original.breakdown.map(s=>[s.id,s.casts,s.damage]));
  }
}
const bad=structuredClone(inputs);
bad.claims.classes[0].rules[0].skills.push('condemnation');
assert.throws(()=>learning.validateInputs(bad),/Wrong class/);
for(const override of [{attack:2000},{crit:0},{periodicCrit:'normal'},{insigniaMode:'retain'}]) {
  const changed=structuredClone(inputs);Object.assign(changed.curriculum.training[0],override);
  assert.throws(()=>learning.validateInputs(changed),/Scenario changes shared build/);
}
const highLevel=structuredClone(inputs);highLevel.catalog.classes[0].skills[0].skillLevel=20;
assert.throws(()=>learning.validateInputs(highLevel),/Skill level mismatch/);
const staleDamage=structuredClone(inputs);staleDamage.catalog.damageVerified=false;
assert.throws(()=>learning.validateInputs(staleDamage),/damage audit/);
const leakage=structuredClone(inputs);
leakage.curriculum.test[0]=structuredClone(leakage.curriculum.training[0]);
assert.throws(()=>learning.validateInputs(leakage),/overlap/);
const annotations=structuredClone(inputs.claims);
for (const c of annotations.classes) for (const rule of c.rules) if (rule.reportedHoldSeconds) rule.reportedHoldSeconds=[100,200];
for (const c of inputs.catalog.classes) assert.deepEqual(learning.projectedHints(c,annotations,true),learning.projectedHints(c,inputs.claims,true),'Author timing annotations must not become simulator timings');
console.log('Rotation learning tests passed: constrained actions/waits, unchanged math, deterministic learning, useful hold, no held-out leakage, opt-in hints and blocked tiers.');

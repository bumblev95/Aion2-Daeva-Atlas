'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const backend = require('../scripts/build_dps_rankings.js');
const read = file => JSON.parse(fs.readFileSync(file,'utf8'));
const inputs=backend.loadInputs(), model=read('data/dps-ranking-model.json');
backend.validateInputs(inputs);

// Unequal fight lengths must not become an unweighted mean of per-fight DPS.
const metric=(totalDamage,duration)=>({totalDamage,duration,directDamage:totalDamage*.8,
  periodicDamage:totalDamage*.2,activeSeconds:duration,ticks:0});
const combined=backend.aggregate([metric(100,10),metric(100,100)]);
assert.equal(combined.dps,200/110);
assert.notEqual(combined.dps,(10+1)/2);
assert.equal(combined.directDamage+combined.periodicDamage,combined.totalDamage);
assert.throws(()=>backend.aggregate([metric(1,0)]));
assert.throws(()=>backend.aggregate([metric(Infinity,10)]));

const row=(classId,dps,extra={})=>({classId,dps,seconds:100,totalDamage:dps*100,...extra});
let ranked=backend.rankRows([row('big-improvement',10,{improvement:100}),row('higher-dps',20,{improvement:0})]);
assert.equal(ranked[0].classId,'higher-dps','Rank absolute damage/time, never within-class gains');
ranked=backend.rankRows([row('a',99.991),row('z',99.994)]);
assert.equal(ranked[0].classId,'z','Do not sort rounded display values');
ranked=backend.rankRows([row('z',20),row('a',20),row('b',10)]);
assert.deepEqual(ranked.map(r=>[r.classId,r.rank]),[['a',1],['z',1],['b',3]]);
assert.throws(()=>backend.rankRows([row('same',10),row('same',20)]),/duplicate/);
for(const dps of [NaN,Infinity,-1])assert.throws(()=>backend.rankRows([row('bad',dps)]),/number/);
assert.throws(()=>backend.rankRows([row('bad',10,{totalDamage:200})]),/mismatch/);

// A visitor payload cannot alter the common profile, add free states, swap a
// class or use a stale unreviewed formula. Inputs are repository-owned only.
for(const override of [{attack:2000},{stateWindows:{stun:'0-100'}},{skills:[]}]) {
  const changed=structuredClone(inputs);Object.assign(changed.benchmark.test[0],override);
  assert.throws(()=>backend.validateInputs(changed),/common build/);
}
for(const prop of ['cast','skillLevel']) {
  const changed=structuredClone(inputs);changed.catalog.classes[0].skills[0][prop]+=1;
  assert.throws(()=>backend.validateInputs(changed),/Unequal/);
}
let changed=structuredClone(inputs);changed.catalog.classes.push(changed.catalog.classes[0]);
assert.throws(()=>backend.validateInputs(changed),/Duplicate/);
changed=structuredClone(inputs);changed.catalog.damageVerified=false;
assert.throws(()=>backend.validateInputs(changed),/Review changed source damage/);
let modified=structuredClone(model);modified.provenance.catalogSha256='tampered';
assert.throws(()=>backend.verifyModel(inputs,modified),/Stale ranking policy/);
modified=structuredClone(model);modified.classes[0].runs[0].trainingScore+=100;
assert.throws(()=>backend.verifyModel(inputs,modified),/mismatch/);

// Training reward has no path to validation/test outcomes.
const c=inputs.catalog.classes[0], b=structuredClone(inputs.benchmark);
const policy=model.classes.find(x=>x.id===c.id).policy;
const score=backend.evaluator(c,b).score(policy).score;
b.test[0].duration=1;b.validation[0].duration=1;
assert.equal(backend.evaluator(c,b).score(policy).score,score);

const result=backend.compute(inputs,model);
assert.deepEqual(result,read('data/dps-rankings.json'),'Published JSON must reproduce from backend math and policy');
assert.equal(backend.csv(result),fs.readFileSync('data/dps-rankings.csv','utf8'));
assert.equal(result.overall.length,8);
assert.equal(result.scenarios.length,2);
assert(result.overall.every(r=>r.seconds===420));
for (const c of result.classes) {
  assert.equal(c.totalDamage,c.test.reduce((sum,m)=>sum+m.totalDamage,0));
  assert.equal(c.dps,c.totalDamage/c.seconds);
  assert(!c.policy.order.some(id=>c.damageCoverage.unresolved.some(s=>s.id===id)));
  for(const fight of c.test) {
    const damage=fight.skills.reduce((sum,s)=>sum+s.damage,0);
    assert(Math.abs(damage-fight.totalDamage)<1e-7);
  }
}
assert.equal(result.scope.canDescribeAsEndgameTier,false);
assert.equal(result.methodology.noClientSimulation,true);
console.log('Backend DPS passed: weighted totals, absolute/unrounded ranks, ties, common conditions, source/policy integrity, no held-out leakage and reproducible JSON/CSV.');

'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {simulate,conditionKey} = require('../assets/dps-engine.js');
const learning = require('../research/rotation-learning/train.js');
const kr = require('../research/kr-20261111/audit.js');
const data = kr.load();
const root = path.resolve(__dirname,'..');
const beforeBytes = Object.fromEntries(Object.keys(data.review.protectedInputs).map(file=>[
  file,fs.readFileSync(path.join(root,file))]));
const beforeData = structuredClone(data);
const query = {purpose:'research-only',region:'KR',effectiveAt:'2026-11-11',
  sourceHash:data.review.sourceHash,skillId:'shield-smite',field:'cooldownSeconds'};

assert.equal(kr.resolveOfficial(data,query).value,7);
for (const bad of [{purpose:undefined},{region:'NA'},{region:'Global'},{region:undefined},
  {effectiveAt:'2026-11-10'},{effectiveAt:'2026-11-12'},{effectiveAt:undefined},
  {sourceHash:'0'.repeat(64)},{skillId:'not-a-skill'},{skillId:'brawler'},
  {field:'actualDamage'},{field:'toString'}]) {
  assert.throws(()=>kr.resolveOfficial(data,{...query,...bad}));
}
const table = kr.resolveOfficial(data,{...query,skillId:'insignia-explosion',field:'pveDamageByStacksPercent'});
table.value['5']=999999;
assert.equal(data.review.officialInputs['insignia-explosion'].pveDamageByStacksPercent['5'],500);
for (const change of [
  d=>{d.snapshot.officialOverrides.find(o=>o.region==='KR').skills['shield-smite'].cooldownSeconds=8;},
  d=>{d.review.sourceHash='0'.repeat(64);},
  d=>{d.review.canPublishTiers=true;},
  d=>{d.review.canSeedLiveCalculator=true;},
  d=>{d.review.classReviews.pop();},
  d=>{d.review.classReviews[0].skillIds.push('condemnation');},
  d=>{d.catalog.classes.push({id:'brawler'});},
  d=>{d.snapshot.officialOverrides.push(structuredClone(d.snapshot.officialOverrides.find(o=>o.region==='KR')));},
  d=>{d.review.protectedInputs['data/skills.json']='0'.repeat(64);}
]) {
  const stale = structuredClone(data);change(stale);assert.throws(()=>kr.validate(stale));
}
const result = kr.run(data);
assert.deepEqual(result,kr.run(data),'Deterministic offline experiments');
assert.equal(result.actualKrDps,null);
assert.equal(result.canPublishTiers,false);
assert.deepEqual(result.coverage.missingClasses,['brawler']);
assert.equal(result.classPriorities.length,9);
assert.equal(result.inputComparison.length,17);
assert(result.inputComparison.every(r=>r.appliedToGlobal === false));
assert(result.inputComparison.every(r=>r.cooldownBeforeMatchesGlobal !== false));
assert.equal(result.inputComparison.find(r=>r.id==='summon-fire-spirit').includedInTraining,false);
assert.equal(result.inputComparison.find(r=>r.id==='shield-smite').globalCalculatorCooldownSeconds,10);
const timing = result.experiments.timing;
assert.deepEqual(timing.map(r=>[r.beforeOpportunities,r.afterOpportunities]),[[6,9],[6,9],[12,15],[4,2]]);
assert(timing.every(r=>r.actualDamage === null));
assert.deepEqual(result.experiments.pveHitArithmetic.map(r=>r.normalizedAfterHit),[65,350]);
assert.deepEqual(result.experiments.insigniaMpCeiling.budget.map(r=>[r.actions,r.remainingMp]),[[2,100],[5,0]]);
assert.equal(result.experiments.insigniaStackArithmetic[4].ratio,3.125);

// KR activation windows must not be manufactured from the Global target-debuff gate.
const follow = kr.fixture({id:'condemnation',cooldown:3,requires:['condemnation-ready']});
assert.equal(kr.runToy([follow],{duration:12}).total,0);
assert.equal(kr.runToy([follow],{duration:12,stateWindows:{'chain-of-torment':'0-12'}}).total,0);
for (const seconds of [2,3]) {
  const window = {'condemnation-ready':`1-${1+seconds}`};
  assert.deepEqual(kr.runToy([follow],{duration:12,stateWindows:window}).events.map(e=>e.time),[2]);
  assert.equal(kr.runToy([follow],{duration:12,downtime:`0-${1+seconds}`,stateWindows:window}).total,0,
    'Expired activation cannot survive downtime or an inclusive end boundary');
}
// Source review does not grant permission to import Global-only DoTs/providers into KR.
const globalProvider = kr.fixture({conditionRegion:'Global',flat:0,
  effects:[{state:'condemnation-ready',duration:3,on:'use',chance:100}]});
const blocked = kr.runToy([follow,globalProvider],{duration:12});
assert.equal(blocked.breakdown[0].casts,0);
assert(blocked.warnings.includes('global-only-conditions'));

// Replaying all existing held-out policies before/after the audit gives identical outputs.
const inputs = learning.loadInputs();
const savedModel = JSON.parse(fs.readFileSync(path.join(root,'research/rotation-learning/model.json'),'utf8'));
const replays = () => inputs.catalog.classes.flatMap(c=>inputs.curriculum.test.map(s=>{
  const input = learning.buildInput(c,inputs.curriculum,s);
  const savedClass = savedModel.classes.find(row=>row.id === c.id);
  const policy = savedClass.runs.find(row=>row.seed === savedClass.selectedSeed).policy;
  return {condition:conditionKey(input),baseline:simulate(input),policy:learning.simulatePolicy(input,policy)};
}));
const globalBefore = replays();kr.run(data);
assert.deepEqual(replays(),globalBefore);
assert.deepEqual(data,beforeData,'No mutation of snapshot/catalog/reviews');
for (const [file,bytes] of Object.entries(beforeBytes)) assert.deepEqual(fs.readFileSync(path.join(root,file)),bytes,file);
console.log('KR patch tests passed: explicit region/version/hash, stale inputs, nine-class audit, arithmetic, gates, unchanged Global replays/files.');

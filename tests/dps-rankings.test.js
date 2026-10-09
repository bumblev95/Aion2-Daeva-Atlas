'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const backend = require('../scripts/build_dps_rankings.js');
const inputs = backend.loadInputs();
backend.validateInputs(inputs);
const result = backend.compute(inputs);
assert.deepEqual(result,JSON.parse(fs.readFileSync('data/dps-rankings.json','utf8')));
assert.equal(backend.csv(result),fs.readFileSync('data/dps-rankings.csv','utf8'));
assert.equal(result.comparisons.length,7);
assert.equal(result.scope.usesTooltipSimulation,false);
assert.equal(result.scope.rawFightDpsRecomputed,false);
assert.equal(result.scope.canDescribeAsEndgameTier,false);
assert.equal(result.scope.healingAddedToDamage,false);
assert.equal(result.methodology.noClientSimulation,true);
assert(!('overall' in result),'Different regions, bosses and metrics cannot become one overall DPS');
assert(!('commonConditions' in result),'No fabricated one-second final-build profile');

// Numeric public values, not website row order, community tiers, role or gains.
const row=(classId,value)=>({classId,value});
let ranked=backend.rankRows([row('cleric',200),row('ranger',100)]);
assert.equal(ranked[0].classId,'cleric','Measured healer damage is not forcibly capped');
ranked=backend.rankRows([row('ranger',200),row('cleric',100)]);
assert.equal(ranked[0].classId,'ranger');
ranked=backend.rankRows([row('ranger',90),row('cleric',90),row('assassin',80)]);
assert.deepEqual(ranked.map(r=>r.rank),[1,1,3],'Equal source precision shares a place');
assert.throws(()=>backend.rankRows([row('cleric',1),row('cleric',2)]),/Duplicate/);
for(const value of [NaN,Infinity,-1,null])assert.throws(()=>backend.rankRows([row('cleric',value)]));

const global=result.comparisons.find(d=>d.id==='global-balance');
const korea=result.comparisons.find(d=>d.id==='kr-balance');
assert.equal(global.status,'observed');
assert.equal(korea.status,'insufficient');
assert(korea.rows.every(r=>r.rank===null && r.value===null));
assert(global.rows.findIndex(r=>r.classId==='gladiator')<global.rows.findIndex(r=>r.classId==='assassin'),
  'The source lists Gladiator 90 after Assassin 88; backend must sort numeric medians itself');
for(const change of [d=>d.sourceWithheld=true,d=>d.commonBand=null,d=>d.rows[0].value=null,
  d=>d.rows[0].characterWeeks=99,d=>d.rows[0].uploaders=9,d=>d.rows[0].uploaders=null,
  d=>d.rows[0].bosses=2]){
  const d=structuredClone(global);change(d);assert.equal(backend.balanceEligible(d),false);
}

for(const mutate of [x=>x.datasets[0].region='KR',x=>x.datasets[0].window='all-time',
  x=>x.datasets[0].rows.pop(),x=>x.datasets[0].rows[0].classId='cleric',
  x=>x.datasets[0].rows[0].healerMultiplier=.5,x=>x.datasets[0].sameEquipment=true,
  x=>x.datasets[2].bossId='123',
  x=>x.datasets[2].rows[0].value=Infinity,x=>x.datasets[2].rows[0].resolution=.01,
  x=>x.datasets[2].rows[0].value+=1,x=>x.datasets[2].metric='normalized-index',
  x=>x.datasets[0].rows[0].parses=1]){
  const x=structuredClone(inputs);mutate(x);
  assert.throws(()=>backend.validateInputs(x));
}
for(const d of result.comparisons.filter(d=>d.kind==='record')){
  assert.equal(d.region,'KR');assert.equal(d.patchId,null);assert.equal(d.sameEquipment,false);
  assert(d.rows.every(r=>r.publishedRecords>0 && !('totalDamage' in r)));
  assert(d.rows.every(r=>!('seconds' in r)),'Do not invent a duration to reverse-calculate damage');
}
const weekly=result.comparisons.find(d=>d.kind==='weekly');
assert.equal(weekly.status,'provisional');assert.equal(weekly.region,'UNSPECIFIED');
assert.equal(weekly.regionVerified,false);
for(const kind of ['weekly','band']){
  const d=structuredClone(result.comparisons.find(d=>d.kind===kind));
  d.rows[0].sampleCount=kind==='weekly'?49:19;assert.equal(backend.eligible(d),false);
}
let changed=structuredClone(inputs);changed.datasets.find(d=>d.kind==='weekly').region='KR';
assert.throws(()=>backend.validateInputs(changed),/UNSPECIFIED/);
console.log('PASS: numeric source order, source precision/ties, no role caps, regional/boss/metric separation, sample gates, no invented damage/time and reproducible JSON/CSV.');

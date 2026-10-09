'use strict';
// Backend only. Public pages receive these computed numbers, never a form or engine.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {execFileSync} = require('node:child_process');
const {conditionKey, downtime} = require('../assets/dps-engine.js');
const {buildInput, simulatePolicy, learn, validatePolicy} = require('../research/rotation-learning/train.js');
const ROOT = path.resolve(__dirname, '..');
const CLASS_IDS = ['gladiator','templar','assassin','ranger','sorcerer','spiritmaster','cleric','chanter'];
const SOURCE_FILES = ['assets/dps-engine.js','scripts/build_dps_rankings.js','research/rotation-learning/train.js',
  'dpsmath.py','dpsrules.py','dpslevels.py','data/skills.json','data/dps-resources.json',
  'data/skill-snapshot.json','data/dps-skill-levels.json','data/dps-benchmark.json'];
const MODEL_FILE = 'data/dps-ranking-model.json', RESULT_FILE = 'data/dps-rankings.json', CSV_FILE = 'data/dps-rankings.csv';
const read = file => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const jsonText = value => JSON.stringify(value, null, 2) + '\n';
const unique = values => new Set(values).size === values.length;
const close = (a,b) => assert(Math.abs(a-b) <= 1e-8 * Math.max(1,Math.abs(a),Math.abs(b)), `Damage mismatch: ${a}, ${b}`);
const finite = n => {assert(Number.isFinite(n) && n >= 0, 'Invalid ranking number');return n;};

function loadInputs() {
  const catalog = JSON.parse(execFileSync(process.env.PYTHON || 'python', ['-c',
    'import json, liveops; print(json.dumps(liveops.catalog(skill_level=20), ensure_ascii=False))'],
    {cwd:ROOT,encoding:'utf8',maxBuffer:4*1024*1024}));
  return {catalog, benchmark:read('data/dps-benchmark.json')};
}
function validateInputs({catalog, benchmark:b}) {
  assert.equal(catalog.damageVerified,true,'Review changed source damage first');
  assert.equal(catalog.conditionsVerified,true,'Review changed source conditions first');
  assert.equal(b.kind,'controlled-class-benchmark');
  assert.equal(b.isCombatMeasurement,false);assert.equal(b.actualEquipmentVerified,false);
  assert.equal(b.currentPatchEquivalent,false);
  assert.equal(b.skillLevel,20);assert.equal(b.actionSeconds,1);
  assert.deepEqual(b.specializations,[]);assert.deepEqual(b.stigmas,[]);
  assert.equal(b.passiveDamageIncluded,false);assert.equal(b.base.region,'NA');
  assert.equal(b.base.conditionsVerified,true);assert.equal(b.base.damageVerified,true);
  assert.deepEqual(b.base.stateWindows,{},'No free external prerequisite windows');
  assert.equal(b.base.elementEvents,'');assert.equal(b.base.elementsStart,0);
  assert(unique(catalog.classes.map(c=>c.id)),'Duplicate class');
  assert.deepEqual(catalog.classes.map(c=>c.id).sort(),[...CLASS_IDS].sort(),'Rank all eight classes');
  const ids = [], conditions = [];
  for (const split of ['training','validation','test']) {
    assert(b[split].length > 0);
    for (const scenario of b[split]) {
      assert(Object.keys(scenario).every(k=>['id','en','ko','duration','downtime','targetControl'].includes(k)),
        'A scenario cannot change the common build or grant states/resources');
      ids.push(scenario.id);conditions.push(conditionKey({...b.base,...scenario}));
    }
  }
  assert(unique(ids) && unique(conditions),'Training and held-out fights must be separate');
  assert(unique(b.learning.seeds));assert(b.learning.seeds.length >= 3);
  assert(unique(b.holdSeconds) && b.holdSeconds.includes(0));
  assert(b.holdSeconds.every(n=>Number.isFinite(n) && n >= 0 && n <= 10));
  for (const c of catalog.classes) {
    assert(c.skills.length > 0 && unique(c.skills.map(s=>s.id)));
    assert.equal(c.candidates.length,12);
    for (const s of c.skills) {
      assert.equal(s.skillLevel,b.skillLevel,'Unequal skill levels');
      assert.equal(s.cast,b.actionSeconds,'Unequal action time assumptions');
      assert.equal(s.damageStatus,'direct','Unresolved charges/pets cannot enter the ranking');
      assert(!s.charge && !s.damageInputRequired);
      for (const scenario of b.test) {
        assert.equal(conditionKey(buildInput(c,b,scenario)), conditionKey({...b.base,...scenario}));
      }
    }
  }
}
function provenance(inputs) {
  return {files:Object.fromEntries(SOURCE_FILES.map(file=>[file,hash(fs.readFileSync(path.join(ROOT,file)))])),
    catalogSha256:hash(Buffer.from(jsonText(inputs.catalog)))};
}
function measure(c, b, scenario, policy) {
  const result = simulatePolicy(buildInput(c,b,scenario),policy);
  const direct = result.breakdown.reduce((sum,s)=>sum+s.directDamage,0);
  const periodic = result.breakdown.reduce((sum,s)=>sum+s.periodicDamage,0);
  close(result.total,direct+periodic);close(result.edps,result.total/scenario.duration);
  finite(result.total);finite(result.edps);
  for (const s of result.breakdown) close(s.damage,s.directDamage+s.periodicDamage);
  return {scenario:scenario.id,duration:scenario.duration,activeSeconds:result.activeTime,
    totalDamage:result.total,directDamage:direct,periodicDamage:periodic,dps:result.edps,
    ticks:result.breakdown.reduce((sum,s)=>sum+s.ticks,0),warnings:result.warnings,
    skills:result.breakdown.map(s=>({...s,en:c.skills.find(x=>x.id===s.id).en,ko:c.skills.find(x=>x.id===s.id).ko}))};
}
function aggregate(metrics) {
  assert(metrics.length > 0);
  for (const m of metrics) {
    finite(m.totalDamage);finite(m.duration);assert(m.duration > 0);
    close(m.totalDamage,m.directDamage+m.periodicDamage);
  }
  const totalDamage = metrics.reduce((sum,m)=>sum+m.totalDamage,0);
  const seconds = metrics.reduce((sum,m)=>sum+m.duration,0);
  const directDamage = metrics.reduce((sum,m)=>sum+m.directDamage,0);
  const periodicDamage = metrics.reduce((sum,m)=>sum+m.periodicDamage,0);
  return {totalDamage,seconds,dps:totalDamage/seconds,directDamage,periodicDamage,
    activeSeconds:metrics.reduce((sum,m)=>sum+m.activeSeconds,0),
    ticks:metrics.reduce((sum,m)=>sum+m.ticks,0)};
}
function evaluator(c,b) {
  const cache = new Map();
  return {cache,score(policy) {
    validatePolicy(policy,c.skills.map(s=>s.id),b.holdSeconds);
    const key = JSON.stringify(policy);
    if (!cache.has(key)) cache.set(key,{policy,score:aggregate(b.training.map(s=>measure(c,b,s,policy))).dps});
    return cache.get(key);
  }};
}
function compareRuns(a,b) {
  return b.trainingScore-a.trainingScore || a.policy.holdSeconds-b.policy.holdSeconds ||
    JSON.stringify(a.policy).localeCompare(JSON.stringify(b.policy)) || a.seed-b.seed;
}
function train(inputs) {
  validateInputs(inputs);
  const {catalog,benchmark:b}=inputs;
  return {schema:1,kind:'backend-dps-ranking-policy',benchmark:b.id,provenance:provenance(inputs),
    objective:'sum training damage / sum training fight seconds',selectionSplit:'training',
    strategy:'Categorical cross-entropy search of static priorities and declared hold times. No global-optimum claim.',
    classes:catalog.classes.map(c=>{
      const evaluate=evaluator(c,b);
      const runs=b.learning.seeds.map(seed=>learn(c,b,[],{...b.learning,seed},evaluate)).sort(compareRuns);
      console.log('Trained '+c.en+' across '+runs.length+' seeds; selected on training fights only.');
      return {id:c.id,selectedSeed:runs[0].seed,policy:runs[0].policy,trainingDps:runs[0].trainingScore,runs};
    })};
}
function verifyModel(inputs,model) {
  validateInputs(inputs);
  assert.equal(model.kind,'backend-dps-ranking-policy');assert.equal(model.benchmark,inputs.benchmark.id);
  assert.equal(model.selectionSplit,'training');
  assert.equal(model.objective,'sum training damage / sum training fight seconds');
  assert.deepEqual(model.provenance,provenance(inputs),'Stale ranking policy: retrain after changing math or data');
  assert(unique(model.classes.map(c=>c.id)));
  assert.deepEqual(model.classes.map(c=>c.id).sort(),[...CLASS_IDS].sort());
  for (const row of model.classes) {
    const c=inputs.catalog.classes.find(c=>c.id===row.id), evaluate=evaluator(c,inputs.benchmark);
    assert.deepEqual(row.runs.map(r=>r.seed).sort((a,b)=>a-b),[...inputs.benchmark.learning.seeds].sort((a,b)=>a-b));
    for (const run of row.runs) {
      validatePolicy(run.policy,c.skills.map(s=>s.id),inputs.benchmark.holdSeconds);
      close(run.trainingScore,evaluate.score(run.policy).score);
    }
    const selected=[...row.runs].sort(compareRuns)[0];
    assert.equal(row.selectedSeed,selected.seed);assert.deepEqual(row.policy,selected.policy);
    close(row.trainingDps,selected.trainingScore);
  }
}
function rankRows(rows) {
  assert(rows.length > 0 && unique(rows.map(r=>r.classId)),'No duplicate ranking rows');
  rows.forEach(r=>{finite(r.dps);finite(r.totalDamage);finite(r.seconds);assert(r.seconds>0);close(r.dps,r.totalDamage/r.seconds);});
  const sorted=rows.map(r=>({...r})).sort((a,b)=>b.dps-a.dps || a.classId.localeCompare(b.classId));
  sorted.forEach((row,i)=>{
    row.rank=i && row.dps===sorted[i-1].dps ? sorted[i-1].rank : i+1;
    row.leaderPercent=sorted[0].dps>0?row.dps/sorted[0].dps*100:0;
  });
  return sorted;
}
function compute(inputs,model) {
  verifyModel(inputs,model);
  const {catalog,benchmark:b}=inputs;
  const classes=catalog.classes.map(c=>{
    const row=model.classes.find(x=>x.id===c.id);
    const test=b.test.map(s=>measure(c,b,s,row.policy));
    return {classId:c.id,en:c.en,ko:c.ko,color:c.color,...aggregate(test),policy:row.policy,
      selectedSeed:row.selectedSeed,trainingDps:row.trainingDps,
      validation:b.validation.map(s=>measure(c,b,s,row.policy)),test,
      damageCoverage:{modeled:c.skills.length,active:c.candidates.length,
        unresolved:c.candidates.filter(s=>['input-required','charge-input-required'].includes(s.damageStatus))
          .map(s=>({id:s.id,en:s.en,ko:s.ko,status:s.damageStatus,source:s.source,missing:s.mathUnverified})),
        nonOffensive:c.candidates.filter(s=>s.damageStatus==='non-offensive').map(s=>({id:s.id,en:s.en,ko:s.ko}))}};
  });
  const summary = row => Object.fromEntries(['classId','en','ko','color','dps','totalDamage','seconds','activeSeconds',
    'directDamage','periodicDamage','ticks'].map(key=>[key,row[key]]));
  const overall=rankRows(classes.map(summary));
  const scenarios=b.test.map(s=>({id:s.id,en:s.en,ko:s.ko,duration:s.duration,downtime:s.downtime,
    unavailableSeconds:downtime(s.downtime,s.duration).reduce((sum,[a,z])=>sum+z-a,0),targetControl:s.targetControl,
    rows:rankRows(classes.map(c=>{
      const m=c.test.find(x=>x.scenario===s.id);
      return {...summary(c),...aggregate([m])};
    }))}));
  return {schema:1,kind:'server-computed-dps-ranking',benchmark:b.id,sourceReviewedAt:catalog.sourceDate,
    scope:{region:'Global',skillLevel:b.skillLevel,isCombatMeasurement:false,actualEquipmentVerified:false,
      canDescribeAsEndgameTier:false,currentPatchEquivalent:false,specializations:[],stigmas:[],passiveDamageIncluded:false},
    commonConditions:{...b.base,actionSeconds:b.actionSeconds},
    methodology:{aggregation:'sum held-out damage / sum held-out fight seconds',ranking:'unrounded absolute DPS',
      trainingSeeds:b.learning.seeds,selectionSplit:'training',noExternalStateWindows:true,
      noUserInputs:true,noClientSimulation:true},
    provenance:{...provenance(inputs),modelSha256:hash(Buffer.from(jsonText(model)))},
    overall,scenarios,classes};
}
function csv(result) {
  const quote=value=>{
    const s=String(value);
    return '"'+(/^[=+\-@]/.test(s)?"'"+s:s).replace(/"/g,'""')+'"';
  };
  const head=['benchmark','source_reviewed_at','region','skill_level','scenario','rank','class','dps',
    'total_damage','fight_seconds','direct_damage','periodic_damage','attack','crit_percent','crit_multiplier',
    'hit_percent','action_seconds','downtime_seconds','target_control','resource_mode','periodic_crit',
    'periodic_refresh','insignia_mode','dot_state_mode','verified_endgame_tier','model_sha256'];
  const conditions=result.commonConditions;
  const controlTypes=[...new Set(result.scenarios.map(s=>s.targetControl))];
  const rows=[['overall',result.overall],...result.scenarios.map(s=>[s.id,s.rows])].flatMap(([id,rows])=>rows.map(r=>[
    result.benchmark,result.sourceReviewedAt,result.scope.region,result.scope.skillLevel,id,r.rank,r.en,
    r.dps,r.totalDamage,r.seconds,r.directDamage,r.periodicDamage,conditions.attack,conditions.crit,
    conditions.critMultiplier,conditions.accuracy,conditions.actionSeconds,r.seconds-r.activeSeconds,
    result.scenarios.find(s=>s.id===id)?.targetControl || (controlTypes.length===1?controlTypes[0]:'mixed'),
    conditions.resourceMode,conditions.periodicCrit,conditions.periodicRefresh,conditions.insigniaMode,
    conditions.dotStateMode,result.scope.canDescribeAsEndgameTier,result.provenance.modelSha256]));
  return [head,...rows].map(row=>row.map(quote).join(',')).join('\n')+'\n';
}
function main() {
  const flag=process.argv[2];
  assert(process.argv.length===3 && ['--train','--build','--verify'].includes(flag),'Use --train, --build or --verify');
  const inputs=loadInputs();
  const model=flag==='--train'?train(inputs):read(MODEL_FILE);
  if (flag==='--train') fs.writeFileSync(path.join(ROOT,MODEL_FILE),jsonText(model));
  const result=compute(inputs,model), resultText=jsonText(result), csvText=csv(result);
  if (flag==='--verify') {
    assert.equal(fs.readFileSync(path.join(ROOT,RESULT_FILE),'utf8'),resultText,'Stale or modified ranking result');
    assert.equal(fs.readFileSync(path.join(ROOT,CSV_FILE),'utf8'),csvText,'Stale ranking CSV');
  } else {
    fs.writeFileSync(path.join(ROOT,RESULT_FILE),resultText);
    fs.writeFileSync(path.join(ROOT,CSV_FILE),csvText);
  }
  console.log('Backend rankings '+(flag==='--verify'?'verified':'computed')+': all 8 classes, common level-20 conditions, held-out scoring, absolute DPS.');
}
if(require.main===module) main();
module.exports={loadInputs,validateInputs,aggregate,evaluator,train,verifyModel,rankRows,compute,csv};

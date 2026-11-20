'use strict';
// Research only. No live calculator import and no writer outside this directory.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {simulate} = require('../../assets/dps-engine.js');
const ROOT = path.resolve(__dirname, '../..');
const read = file => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));
const digest = data => crypto.createHash('sha256').update(data).digest('hex');
const json = value => JSON.stringify(value, null, 2) + '\n';
const INPUT = 'research/kr-20261111/inputs.json';
const OUTPUT = path.join(__dirname, 'results.json');
const CLASSES = ['gladiator','templar','assassin','brawler','chanter','ranger','sorcerer','spiritmaster','cleric'];

function load() {
  return {review:read(INPUT), snapshot:read('data/skill-snapshot.json'),
    catalog:read('docs/data/dps.json'), skills:read('data/skills.json'),
    patchReviews:read('data/patch-reviews.json')};
}
function validate(data) {
  const {review:r, snapshot, catalog, skills, patchReviews} = data;
  assert.equal(r.schema, 1);
  assert.equal(r.purpose, 'research-only-kr-input-validation');
  assert.equal(r.region, 'KR');
  assert.equal(r.effectiveAt, '2026-11-11');
  assert.equal(r.canPublishTiers, false);
  assert.equal(r.canSeedLiveCalculator, false);
  assert.equal(r.source, 'https://aion2.plaync.com/ko-kr/board/update/view?articleId=6af370b8577e8c01355e047b');
  assert.match(r.sourceHash, /^[a-f0-9]{64}$/);
  const overrides = snapshot.officialOverrides.filter(o => o.region === r.region && o.effectiveAt === r.effectiveAt);
  assert.equal(overrides.length, 1, 'Ambiguous/missing regional input version');
  const o = overrides[0];
  assert.equal(o.source, r.source);
  assert.equal(o.sourceHash, r.sourceHash, 'Official input source changed; re-review');
  assert.deepEqual(o.skills, r.officialInputs, 'Numeric inputs differ from the source-reviewed fixture');
  assert.equal(patchReviews['6af370b8577e8c01355e047b'].contentHash, r.sourceHash);
  assert.equal(snapshot.region, 'Global');
  assert.deepEqual(r.classReviews.map(c=>c.classId).sort(), [...CLASSES].sort());
  const skillIds = new Map(skills.map(s=>[s.id,s.cls]));
  for (const c of r.classReviews) {
    assert(['P0','P1'].includes(c.priority));
    assert(c.officialSummaryKo && c.currentAssumptionKo && c.unverifiedKo);
    for (const id of c.skillIds) assert.equal(skillIds.get(id), c.classId, 'Wrong skill/class mapping: '+id);
  }
  for (const id of Object.keys(r.officialInputs)) assert(skillIds.has(id), 'Unmapped official skill: '+id);
  assert(!catalog.classes.some(c=>c.id === 'brawler'), 'Brawler coverage changed; renew the audit');
  assert.equal(catalog.classes.length, 8);
  for (const [file, hash] of Object.entries(r.protectedInputs)) {
    assert.equal(digest(fs.readFileSync(path.join(ROOT,file))), hash, 'Baseline changed; re-review: '+file);
  }
  return data;
}

// Returns a COPY of a published scalar/table, never a Global skill with a KR label.
// Exact version and source selection intentionally rejects future dates/other regions.
function resolveOfficial(data, query) {
  validate(data);
  const r = data.review;
  assert.equal(query.purpose, 'research-only', 'Explicit research opt-in required');
  assert.equal(query.region, r.region, 'Wrong region');
  assert.equal(query.effectiveAt, r.effectiveAt, 'Unknown patch version');
  assert.equal(query.sourceHash, r.sourceHash, 'Wrong source hash');
  const skill = r.officialInputs[query.skillId];
  assert(skill && Object.hasOwn(skill, query.field), 'Missing/unverified official input');
  return {region:r.region, effectiveAt:r.effectiveAt, source:r.source, sourceHash:r.sourceHash,
    skillId:query.skillId, field:query.field, value:structuredClone(skill[query.field]),
    evidence:'official-note; live combat unverified', canSeedLiveCalculator:false};
}
function comparison(data) {
  const candidates = new Map(data.catalog.classes.flatMap(c=>c.candidates.map(s=>[s.id,s])));
  const skills = new Map(data.skills.map(s=>[s.id,s]));
  return Object.entries(data.review.officialInputs).map(([id, official]) => {
    const s = skills.get(id), c = candidates.get(id);
    const match = /^([\d.]+)s$/.exec(s.cooldown);
    const cd = match ? Number(match[1]) : null;
    return {id, nameKo:s.ko, classId:s.cls, kind:s.kind,
      globalSourceCooldownSeconds:cd, globalCalculatorCooldownSeconds:c?.cooldown ?? null,
      globalMpCost:c?.mpCost ?? null, includedInTraining:data.catalog.classes.some(c=>c.skills.some(s=>s.id===id)),
      officialKr:structuredClone(official), appliedToGlobal:false,
      cooldownBeforeMatchesGlobal:Object.hasOwn(official,'beforeCooldownSeconds') ? cd === official.beforeCooldownSeconds : null,
      compatibility:'Numeric agreement does not verify KR damage, conditions, skill level or timing.'};
  });
}

// Completely artificial fixed-stat action, used to test input arithmetic in the real engine.
function fixture(extra={}) {
  return {id:'toy',name:'Normalized action',enabled:true,flat:100,coefficient:0,hits:1,
    cast:1,cooldown:0,afterCooldown:0,delta:0,mpCost:0,conditionRegion:'KR',...extra};
}
function runToy(skills, extra={}) {
  return simulate({region:'KR',patch:'kr-20261111-normalized-fixture',duration:60,
    attack:0,crit:0,critMultiplier:1.5,accuracy:100,factor:1,downtime:'',
    resourceMode:'budget',mpStart:100000,mpMax:100000,mpRegen:0,
    targetType:'npc',targetControl:'immune',skills,...extra});
}
function experiments(data) {
  const q = (skillId, field) => resolveOfficial(data, {purpose:'research-only',region:'KR',
    effectiveAt:data.review.effectiveAt,sourceHash:data.review.sourceHash,skillId,field}).value;
  const timing = (id, cast) => {
    const before = runToy([fixture({id,cast,flat:0,cooldown:q(id,'beforeCooldownSeconds')})]);
    const after = runToy([fixture({id,cast,flat:0,cooldown:q(id,'cooldownSeconds')})]);
    return {skillId:id, durationSeconds:60, assumedActionSeconds:cast,
      beforeCooldown:q(id,'beforeCooldownSeconds'), afterCooldown:q(id,'cooldownSeconds'),
      beforeOpportunities:before.breakdown[0].casts, afterOpportunities:after.breakdown[0].casts,
      actualDamage:null, scope:'Cooldown-only opportunities; no conditions, resources, summons or damage prediction.'};
  };
  const scalar = (id) => ({skillId:id, normalizedBeforeHit:100,
    normalizedAfterHit:100*(1+q(id,'pveDamageChangePercent')/100),
    actualDamage:null, scope:'One artificial unbuffed PvE hit only. No Global coefficient is imported.'});
  const mp = {resourceMode:'budget',mpStart:500,mpMax:500,mpRegen:0};
  const budget = ['before','after'].map(phase=>{
    const old = phase === 'before';
    const result = runToy([fixture({id:'insignia-explosion',flat:0,
      cooldown:q('insignia-explosion',old?'beforeCooldownSeconds':'cooldownSeconds'),
      mpCost:q('insignia-explosion',old?'beforeMpCost':'mpCost')})],mp);
    return {phase,actions:result.breakdown[0].casts,remainingMp:result.mp};
  });
  const activation = Object.entries(data.review.additionalOfficialInputs.cleric.condemnationWindowsSeconds).map(([opener, seconds])=>{
    const follow = fixture({id:'condemnation',cooldown:3,requires:['condemnation-ready']});
    const provider = fixture({id:opener,flat:0,cooldown:30,
      effects:[{state:'condemnation-ready',duration:seconds,on:'use',chance:100}]});
    const result = runToy([follow,provider],{duration:12});
    const boundary = runToy([follow],{duration:12,conditionMode:'windows',
      stateWindows:{'condemnation-ready':`1-${1+seconds}`}});
    return {opener,windowSeconds:seconds,assumedOpenerCompletion:1,
      conditionalHitTimes:result.events.filter(e=>e.skill === 'condemnation').map(e=>e.time),
      externalWindowHitTimes:boundary.events.map(e=>e.time),
      scope:'Window wiring only. Assumes activation at cast completion, 1s actions and 3s follow-up cooldown; all timings unmeasured.'};
  });
  return {kind:'normalized-input-micro-experiments',isCombatMeasurement:false,
    timing:[timing('shield-smite',1),timing('shield-smite',1.5),timing('drill-dart',1),timing('summon-fire-spirit',1)],
    pveHitArithmetic:[scalar('elemental-fusion'),scalar('winters-shackles')],
    insigniaMpCeiling:{durationSeconds:60,mpStart:500,mpRegen:0,budget,
      scope:'Budget ceiling without stack generation. Not a playable Insignia rotation.'},
    insigniaStackArithmetic:Object.entries(q('insignia-explosion','pveDamageByStacksPercent')).map(([stacks,after])=>{
      const before = data.review.additionalOfficialInputs.assassin.beforePveDamageByStacksPercent[stacks];
      return {stacks:Number(stacks),beforePercent:before,afterPercent:after,ratio:after/before,
        scope:'Published stack multiplier only; unchanged normalized baseline assumed, not an Attack coefficient.'};
    }),
    condemnationActivation:activation,
    excludedFromFullRotation:['Judgment charges/resets and removed providers','Frenzy','Insignia ownership/RNG',
      'Precision/Resonance','pet cadence and elements','Spirit Descent/delayed damage',
      'Brawler catalog','party/self buffs','level-55 build','measured action times and MP']};
}
function run(data=load()) {
  validate(data);
  return {schema:1,purpose:'research-only',region:'KR',effectiveAt:data.review.effectiveAt,
    baseCommit:data.review.baseCommit,source:data.review.source,sourceHash:data.review.sourceHash,
    provenance:Object.fromEntries([INPUT,'research/kr-20261111/audit.js',...Object.keys(data.review.protectedInputs)].map(file=>[
      file,digest(fs.readFileSync(path.join(ROOT,file)))])),
    canPublishTiers:false,canSeedLiveCalculator:false,actualKrDps:null,globalResultsModified:false,
    coverage:{officialClasses:9,catalogClasses:8,missingClasses:['brawler'],directSkillsIncluded:72,activeSkillsInExistingCatalog:96,
      note:'72/96 describes the existing eight-class catalog, not all nine KR classes.'},
    classPriorities:data.review.classReviews,
    inputComparison:comparison(data), experiments:experiments(data)};
}
if (require.main === module) {
  const mode = process.argv.slice(2);
  assert(mode.length <= 1 && (!mode.length || ['--verify','--write'].includes(mode[0])), 'Use --write or --verify');
  const output = json(run());
  if (mode[0] === '--write') fs.writeFileSync(OUTPUT,output);
  else if (mode[0] === '--verify') assert.equal(fs.readFileSync(OUTPUT,'utf8'),output,'KR experiment results are stale');
  console.log(mode[0] === '--verify' ? 'KR inputs/results verified; Global inputs unchanged.' : output);
}
module.exports = {load,validate,resolveOfficial,comparison,fixture,runToy,experiments,run};

'use strict';
// Research only: categorical cross-entropy policy search, not combat-log training.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const {simulate, conditionKey} = require('../../assets/dps-engine.js');
const ROOT = path.resolve(__dirname, '../..');
const FILES = ['assets/dps-engine.js', 'docs/data/dps.json', 'data/skills.json',
  'research/gameplay-evidence.json', 'research/rotation-learning/claims.json',
  'research/rotation-learning/scenarios.json', 'research/rotation-learning/train.js',
  'liveops.py','dpsmath.py','dpsrules.py','data/dps-resources.json','data/skill-snapshot.json'];
const EPS = 1e-8;
const read = file => JSON.parse(fs.readFileSync(path.join(ROOT, file), 'utf8'));
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const jsonText = value => JSON.stringify(value, null, 2) + '\n';
const unique = values => new Set(values).size === values.length;

function loadInputs() {
  return {catalog:read(FILES[1]), skillbook:read(FILES[2]), evidence:read(FILES[3]),
    claims:read(FILES[4]), curriculum:read(FILES[5])};
}
function provenance() {
  return Object.fromEntries(FILES.map(file => [file, hash(fs.readFileSync(path.join(ROOT, file)))]));
}
function validateInputs({catalog, skillbook, evidence, claims, curriculum}) {
  assert.equal(catalog.conditionsVerified, true, 'Renew the condition audit first');
  assert.equal(catalog.damageVerified, true, 'Renew the damage audit first');
  assert.equal(claims.purpose, 'research-only');
  assert.equal(claims.canSeedLiveCalculator, false);
  assert.equal(curriculum.kind, 'synthetic-simulator-curriculum');
  assert.equal(curriculum.isCombatMeasurement, false);
  assert.equal(evidence.rankVerified, false);
  const profile = curriculum.sharedBuild;
  assert(profile && profile.equipmentMode === 'shared-stat-inputs', 'Declare the common equipment/stat profile');
  assert.equal(profile.actualEquipmentVerified, false);
  assert.equal(profile.skillLevel, 1, 'Only source-backed base-1 math is audited');
  assert.deepEqual(profile.specializations, []);assert.deepEqual(profile.stigmas, []);
  assert.equal(profile.passiveDamageIncluded, false);
  assert.deepEqual(profile.activationPassives, ['fire-mark']);
  assert.equal(profile.actionSeconds, 1);assert.equal(profile.actionTimesMeasured, false);
  assert.deepEqual(Object.keys(profile.stats).sort(),['accuracy','attack','crit','critMultiplier','factor'].sort());
  assert.deepEqual(Object.keys(profile.mechanicsAssumptions).sort(),['region','patch','conditionMode','resourceMode',
    'fireMarkEnabled','elementsStart','elementEvents','periodicMode','periodicCrit','periodicRefresh','insigniaMode','targetType'].sort());
  for (const [key,value] of Object.entries({...profile.stats,...profile.mechanicsAssumptions})) {
    assert.deepEqual(curriculum.base[key],value,'Shared profile mismatch: '+key);
  }
  const classIds = catalog.classes.map(c => c.id);
  for(const c of catalog.classes)for(const s of c.skills) {
    assert.equal(s.skillLevel,profile.skillLevel,'Skill level mismatch: '+s.id);
    assert.equal(s.cast,profile.actionSeconds,'Action time mismatch: '+s.id);
  }
  assert(unique(classIds));
  assert(unique(claims.classes.map(c => c.id)));
  assert.deepEqual([...classIds].sort(), claims.classes.map(c => c.id).sort());
  const sources = new Map(evidence.sources.map(s => [s.id, s]));
  assert.equal(sources.size, evidence.sources.length);
  const skills = new Map(skillbook.map(s => [s.id, s]));
  const ruleIds = [];
  for (const c of claims.classes) for (const rule of c.rules) {
    ruleIds.push(rule.id);
    const source = sources.get(rule.sourceId);
    assert(source && source.class === c.id, `Invalid source: ${rule.id}`);
    assert(source.publishedAt <= claims.reviewedAt, `Future source: ${rule.id}`);
    assert.equal(source.fullFightVerified, false);
    assert(rule.ko && rule.en && rule.context && rule.requiresFeatures.length);
    assert(unique(rule.skills));
    for (const id of rule.skills) assert.equal(skills.get(id)?.cls, c.id, `Wrong class/name: ${id}`);
    if (rule.order) {
      assert.equal(rule.type, 'priority');
      assert(unique(rule.order));
      assert(rule.order.every(id => rule.skills.includes(id)));
    }
  }
  assert(unique(ruleIds));
  const ids = [];
  const conditions = [];
  for (const split of ['training', 'validation', 'test']) {
    assert(curriculum[split].length > 0);
    for (const scenario of curriculum[split]) {
      for(const key of Object.keys({...profile.stats,...profile.mechanicsAssumptions})) {
        assert(!Object.hasOwn(scenario,key) || scenario[key] === curriculum.base[key], 'Scenario changes shared build: '+key);
      }
      assert(!Object.hasOwn(scenario,'skills'), 'Scenario cannot replace the common skill model');
      ids.push(scenario.id);
      const input = {...curriculum.base, ...scenario};
      conditions.push(conditionKey(input));
      assert(input.duration >= 1 && input.duration <= 600);
    }
  }
  assert(unique(ids), 'Split IDs must not overlap');
  assert(unique(conditions), 'No identical conditions across splits');
  assert(unique(curriculum.holdSeconds));
  assert(curriculum.holdSeconds.includes(0));
  assert(curriculum.holdSeconds.every(n => Number.isFinite(n) && n >= 0 && n <= 10));
}
function buildInput(c, curriculum, scenario) {
  return {...curriculum.base, ...scenario, skills:c.skills.map(s => ({...s,
    name:s.ko, enabled:true, afterCooldown:s.cooldown, delta:0}))};
}
function validatePolicy(policy, ids, holdValues) {
  assert(unique(policy.order), 'A policy must contain each skill exactly once');
  assert.deepEqual([...policy.order].sort(), [...ids].sort(), 'No missing or foreign skills');
  assert(holdValues.includes(policy.holdSeconds), 'Hold value is outside the declared search space');
}
function selector(policy) {
  const rank = new Map(policy.order.map((id, i) => [id, i]));
  return context => {
    const current = [...context.feasible].sort((a, b) => rank.get(a.id) - rank.get(b.id))[0];
    assert(current && rank.has(current.id), 'Unknown policy action');
    // Waiting never grants a status, reset or resource. Eligibility is checked
    // again by the engine after the wait, including expiry and downtime.
    const upcoming = context.cooldowns.filter(s => s.requirementsMet &&
      rank.get(s.id) < rank.get(current.id) && s.readyAt > context.time + EPS &&
      s.readyAt - context.time <= policy.holdSeconds + EPS &&
      s.readyAt + s.cast <= context.end + EPS);
    if (upcoming.length) return {waitUntil:Math.min(...upcoming.map(s => s.readyAt))};
    return current.index;
  };
}
function simulatePolicy(input, policy) {
  validatePolicy(policy, input.skills.filter(s => s.enabled).map(s => s.id), [policy.holdSeconds]);
  assert(Number.isFinite(policy.holdSeconds) && policy.holdSeconds >= 0 && policy.holdSeconds <= 10);
  return simulate(input, false, selector(policy));
}
function projectedHints(c, claims, allowHints) {
  if (!allowHints) return [];
  const ids = c.skills.map(s => s.id);
  return claims.classes.find(x => x.id === c.id).rules.filter(r => r.type === 'priority' && r.order)
    .map(rule => ({ruleId:rule.id, present:rule.order.filter(id => ids.includes(id))}))
    .filter(h => h.present.length >= 2)
    .map(h => ({ruleId:h.ruleId, policy:{order:[...h.present, ...ids.filter(id => !h.present.includes(id))], holdSeconds:0}}));
}
function rng(seed) {
  let state = seed >>> 0;
  return () => {
    state = (state + 0x6D2B79F5) >>> 0;
    let n = Math.imul(state ^ (state >>> 15), 1 | state);
    n ^= n + Math.imul(n ^ (n >>> 7), 61 | n);
    return ((n ^ (n >>> 14)) >>> 0) / 4294967296;
  };
}
function normalized(weights) {
  const sum = weights.reduce((a, b) => a + b, 0);
  return weights.map(n => n / sum);
}
function pick(weights, random) {
  let draw = random() * weights.reduce((a, b) => a + b, 0);
  for (let i = 0; i < weights.length; i++) {draw -= weights[i]; if (draw < 0) return i;}
  return weights.length - 1;
}
function samplePolicy(ids, ranks, holds, holdWeights, random) {
  const remaining = ids.map((id, i) => i), order = [];
  for (let pos = 0; pos < ids.length; pos++) {
    const ix = pick(remaining.map(i => ranks[pos][i]), random);
    order.push(ids[remaining.splice(ix, 1)[0]]);
  }
  return {order, holdSeconds:holds[pick(holdWeights, random)]};
}
const policyKey = p => JSON.stringify(p);
function compareCandidates(a, b) {
  const difference = b.score - a.score;
  if (Math.abs(difference) > 1e-12) return difference;
  return a.policy.holdSeconds - b.policy.holdSeconds || policyKey(a.policy).localeCompare(policyKey(b.policy));
}
function evaluator(c, curriculum) {
  const inputs = curriculum.training.map(s => buildInput(c, curriculum, s));
  const baseline = inputs.map(input => simulate(input).edps);
  assert(baseline.every(n => n > 0), 'A normalized training baseline must be positive');
  const cache = new Map();
  return {cache, score(policy) {
    const key = policyKey(policy);
    if (!cache.has(key)) {
      validatePolicy(policy, c.skills.map(s => s.id), curriculum.holdSeconds);
      const score = inputs.reduce((sum, input, i) => sum + simulatePolicy(input, policy).edps / baseline[i], 0) / inputs.length;
      cache.set(key, {policy, score});
    }
    return cache.get(key);
  }};
}
function greedyPolicy(c, attack) {
  const value = s => (s.flat + s.coefficient / 100 * attack) * s.hits / s.cast;
  return {order:[...c.skills].sort((a, b) => value(b) - value(a) || a.id.localeCompare(b.id)).map(s => s.id), holdSeconds:0};
}
function learn(c, curriculum, hints, settings, evaluate = evaluator(c, curriculum)) {
  const ids = c.skills.map(s => s.id), holds = curriculum.holdSeconds;
  const random = rng(settings.seed);
  let ranks = ids.map(() => ids.map(() => 1));
  let holdWeights = normalized(holds.map(() => 1));
  // Text annotations only influence an initial proposal distribution. Mechanics
  // and damage still come entirely from the reviewed catalog and scenario input.
  for (const hint of hints) hint.policy.order.forEach((id, pos) => ranks[pos][ids.indexOf(id)] += 2);
  ranks = ranks.map(normalized);
  const baseline = {order:ids, holdSeconds:0};
  const starts = [baseline, greedyPolicy(c, curriculum.base.attack), ...hints.map(h => h.policy)];
  let best = starts.map(p => evaluate.score(p)).sort(compareCandidates)[0];
  const trace = [];
  for (let iteration = 0; iteration < settings.generations; iteration++) {
    const batch = [best, ...starts.map(p => evaluate.score(p))];
    while (batch.length < settings.population) batch.push(evaluate.score(samplePolicy(ids, ranks, holds, holdWeights, random)));
    batch.sort(compareCandidates);
    if (compareCandidates(batch[0], best) < 0) best = batch[0];
    const elite = batch.slice(0, Math.max(2, Math.floor(settings.population * settings.eliteFraction)));
    const counts = ids.map(() => ids.map(() => settings.pseudocount));
    const holdCounts = holds.map(() => settings.pseudocount);
    for (const member of elite) {
      member.policy.order.forEach((id, pos) => counts[pos][ids.indexOf(id)]++);
      holdCounts[holds.indexOf(member.policy.holdSeconds)]++;
    }
    ranks = counts.map((row, pos) => normalized(row).map((n, i) =>
      (1 - settings.learningRate) * ranks[pos][i] + settings.learningRate * n));
    const nextHolds = normalized(holdCounts);
    holdWeights = holdWeights.map((n, i) => (1 - settings.learningRate) * n + settings.learningRate * nextHolds[i]);
    trace.push({generation:iteration + 1, bestTrainingScore:best.score, uniqueEvaluations:evaluate.cache.size});
  }
  return {seed:settings.seed, policy:best.policy, trainingScore:best.score,
    rankPositionProbabilities:ranks, holdProbabilities:holdWeights, trace};
}
function permutations(ids) {
  if (ids.length === 0) return [[]];
  return ids.flatMap((id, i) => permutations(ids.filter((x, j) => j !== i)).map(tail => [id, ...tail]));
}
function restrictedOracle(c, curriculum, evaluate) {
  const ids = c.skills.map(s => s.id);
  // A certificate is deliberately confined to this small policy family.
  if (ids.length > 6) return {status:'not-enumerated', reason:'policy space exceeds the research limit'};
  const candidates = permutations(ids).flatMap(order => curriculum.holdSeconds.map(holdSeconds => evaluate.score({order, holdSeconds})));
  const best = candidates.sort(compareCandidates)[0];
  return {status:'enumerated-training-space', policyCount:candidates.length, score:best.score,
    policy:best.policy, scope:'Only declared static priorities and cooldown-hold values, under training scenarios; not a global gameplay optimum.'};
}
function splitMetrics(c, curriculum, split, policy) {
  return curriculum[split].map(scenario => {
    const input = buildInput(c, curriculum, scenario);
    const baseline = simulate(input);
    const result = simulatePolicy(input, policy);
    return {scenario:scenario.id, baselineEdps:baseline.edps, policyEdps:result.edps,
      changePercent:baseline.edps > 0 ? (result.edps / baseline.edps - 1) * 100 : null,
      baselineCasts:Object.fromEntries(baseline.breakdown.map(s => [s.id, s.casts])),
      casts:Object.fromEntries(result.breakdown.map(s => [s.id, s.casts])),
      baselineDamage:Object.fromEntries(baseline.breakdown.map(s=>[s.id,{direct:s.directDamage,periodic:s.periodicDamage,ticks:s.ticks}])),
      damage:Object.fromEntries(result.breakdown.map(s=>[s.id,{direct:s.directDamage,periodic:s.periodicDamage,ticks:s.ticks}])),
      blocked:Object.fromEntries(result.breakdown.filter(s => s.blocked.length).map(s => [s.id, s.blocked])),
      warnings:result.warnings};
  });
}
const meanChange = metrics => metrics.reduce((sum, m) => sum + m.changePercent, 0) / metrics.length;
function assumptionSensitivity(c, curriculum, policy) {
  const cases=[['direct-only',{periodicMode:'omit',insigniaMode:'unverified'}],
    ['overlapping-dots',{periodicRefresh:'stack'}],['critical-dots',{periodicCrit:'normal'}],
    ['retained-insignias',{insigniaMode:'retain'}]];
  return cases.map(([id,overrides])=>{
    // Fixed selected policy; no held-out alternative changes training/selection.
    const changed={...curriculum,base:{...curriculum.base,...overrides}};
    const metrics=splitMetrics(c,changed,'test',policy);
    return {id,overrides,usedForSelection:false,meanChangePercent:meanChange(metrics),
      meanPolicyEdps:metrics.reduce((sum,m)=>sum+m.policyEdps,0)/metrics.length};
  });
}
function tierAssessment(catalog) {
  const direct = catalog.classes.reduce((sum, c) => sum + c.directCount, 0);
  const active = catalog.classes.reduce((sum, c) => sum + c.conditionAudit.length, 0);
  const audits=catalog.classes.flatMap(c=>c.damageAudit);
  return {canPublishTiers:false, tiers:null, directDamageCoverage:{included:direct, active, omitted:active-direct},
    remainingDamageAudit:{noDirectAttack:audits.filter(s=>s.status==='non-offensive').length,
      chargeInputRequired:audits.filter(s=>s.status==='charge-input-required').length,
      summonOrTriggerInputRequired:audits.filter(s=>s.status==='input-required').length,
      knownPeriodicSkills:audits.filter(s=>s.periodic.length).length},
    blockersKo:[
      `직접 피해 수치 ${direct}/${active}개를 반영했습니다. 나머지는 비공격 기술·차징·소환·덫으로 구분했으며 미확인 피해를 0인 실측 값으로 취급하지 않습니다.`,
      '기본 동작 시간은 임시 값으로, 실제 모션과 평타 캔슬을 측정하지 않았습니다.',
      '공통 능력치·기본 1레벨·특화/스티그마 없음으로 통일했지만 실제 동일 장비의 최종빌드를 측정하지 않았습니다.',
      '확인한 지속 피해 수치는 포함했고 첫 틱·치명·갱신·문양 소모는 연구 가정입니다. 정령 공격·버프/방어·차징·확률 초기화는 아직 미완성입니다.',
      'MP는 미검증 모드이며, 제공한 상태 구간은 실제 유지율을 측정한 값이 아닙니다.',
      '한국 공략과 현재 Global의 조건 대응이 미검증이고, 실전 피해 정답 데이터가 없습니다.',
      '검증·테스트에도 같은 불완전한 엔진을 쓰므로 실제 게임의 정확도가 검증된 것은 아닙니다.'
    ],
    blockers:[
      `${direct}/${active} active direct terms are modeled; remaining non-attacks, charges, summons and trap triggers are separately audited rather than measured zero damage.`,
      'Default action durations are placeholders, not measured animation/cancel times.',
      'A common stat budget, base-1 level and no-specialization/Stigma profile is enforced; actual identical equipment/endgame builds are not measured.',
      'Known DoT numbers are included with explicit tick/crit/refresh and Insignia consumption assumptions; pets, buff/defense composition, charges and resets remain incomplete.',
      'MP mode is explicitly unverified; synthetic availability windows are not measured uptime.',
      'KR guide mapping to current Global rules remains unverified; no measured combat target labels exist.',
      'Held-out simulator scenarios share the same incomplete engine; they cannot validate live-game damage.'
    ]};
}
function runResearch(inputs, allowHints) {
  validateInputs(inputs);
  const {catalog, claims, curriculum} = inputs;
  const settings = {generations:10, population:96, eliteFraction:0.15, learningRate:0.65, pseudocount:0.5, seeds:[7,19,41]};
  const model = {schema:2, kind:'categorical-cross-entropy-policy-search', purpose:'research-only',
    trainingReward:'Mean within-class eDPS ratio to the existing catalog priority, over training scenarios only.',
    trainedOnCombatLogs:false, trainedOnCopiedArticleText:false, currentPatchEquivalent:false,
    authorHintsOptedIn:allowHints, commonBuildProfile:structuredClone(curriculum.sharedBuild), provenance:provenance(), settings, classes:[]};
  const results = {schema:2, purpose:'research-only', scenarioKind:curriculum.kind,
    commonBuildProfile:structuredClone(curriculum.sharedBuild),
    selection:'Training reward only; validation and test never choose a policy or seed.',
    tierAssessment:tierAssessment(catalog), classes:[]};
  for (const c of catalog.classes) {
    const hints = projectedHints(c, claims, allowHints);
    const evaluate = evaluator(c, curriculum);
    const runs = settings.seeds.map(seed => learn(c, curriculum, hints, {...settings, seed}, evaluate));
    const selected = [...runs].sort((a, b) => compareCandidates(
      {policy:a.policy,score:a.trainingScore}, {policy:b.policy,score:b.trainingScore}) || a.seed-b.seed)[0];
    const oracle = restrictedOracle(c, curriculum, evaluate);
    const rules = claims.classes.find(x => x.id === c.id).rules;
    model.classes.push({id:c.id, skillIds:c.skills.map(s => s.id), eligibleHintRuleIds:hints.map(h => h.ruleId),
      selectedSeed:selected.seed, runs});
    const validation = splitMetrics(c, curriculum, 'validation', selected.policy);
    const test = splitMetrics(c, curriculum, 'test', selected.policy);
    results.classes.push({id:c.id, ko:c.ko, directCount:c.directCount, activeCount:c.conditionAudit.length,
      zeroDamageSetupSkills:c.skills.filter(s => s.flat === 0 && s.coefficient === 0).map(s => s.id),
      policy:selected.policy, trainingScore:selected.trainingScore,
      restrictedOracle:oracle, trainingGapToRestrictedOracle:oracle.score === undefined ? null : oracle.score-selected.trainingScore,
      uniqueTrainingEvaluations:evaluate.cache.size, training:splitMetrics(c, curriculum, 'training', selected.policy),
      validation, test, validationMeanChangePercent:meanChange(validation), testMeanChangePercent:meanChange(test),
      greedyTrainingScore:evaluate.score(greedyPolicy(c,curriculum.base.attack)).score,
      projectedHints:hints.map(h => ({ruleId:h.ruleId, policy:h.policy, trainingScore:evaluate.score(h.policy).score})),
      unsupportedFeatures:[...new Set(rules.flatMap(r => r.requiresFeatures))].sort(),
      replicaTestMeanChanges:runs.map(r => ({seed:r.seed,changePercent:meanChange(splitMetrics(c,curriculum,'test',r.policy))})),
      assumptionSensitivity:assumptionSensitivity(c,curriculum,selected.policy),
      learningStatus:c.skills.length < 2 ? 'no-order-choice-in-partial-catalog' : 'partial-model-policy-search'});
  }
  return {model, results};
}
function report(results) {
  const coverage=results.tierAssessment.directDamageCoverage, audit=results.tierAssessment.remainingDamageAudit;
  const lines=['# 공통 조건 재학습 / Controlled-profile rotation learning', '',
    '공략 후보를 이용해 **부분 시뮬레이터 안에서** 다시 학습했습니다. 실제 고수의 전투 로그 학습이나 검증된 최적 DPS·직업 티어가 아닙니다.', '',
    '## 동일한 입력 조건 / Common build profile', '',
    results.commonBuildProfile.descriptionKo, '', results.commonBuildProfile.descriptionEn, '',
    '모든 기술 동작은 1초인 합성 입력입니다. MP 제한은 미검증 모드이며 파티 버프·방어/증폭 합성·실측 장비는 없습니다. 지속 피해는 첫 틱이 한 주기 후, 치명 없음, 재적용 시 기존 효과 교체로 가정합니다. 문양은 각 중첩의 개별 10초 만료와 폭발 시 전체 소모를 가정합니다. 고통의 연쇄 사용 구간은 명시한 합성 외부 구간이며 지속 피해 시간으로 자동 대체하지 않습니다.', '',
    '## 보완한 피해 수학 / Damage coverage', '',
    '직접 피해 초기값은 26개에서 '+coverage.included+'/'+coverage.active+'개로 늘었습니다. 별도 확률 효과·MP 회복·지속 피해 문구 때문에 직접 피해를 버리던 필터를 제거했습니다. 방패 강타·타격쇄·고통의 연쇄의 준비 기술도 실제 직접 피해를 계산합니다.', '',
    '- 직접 공격이 없는 회복/해제/버프: '+audit.noDirectAttack+'개. 누락된 공격 피해로 계산하지 않습니다.',
    '- 차징: '+audit.chargeInputRequired+'개. 최소/최대 피해만 확인했으며 중간 단계·충전 시간은 미검증입니다. 학습에 넣지 않았습니다.',
    '- 정령/신성한 기운/혹한의 바람/덫: '+audit.summonOrTriggerInputRequired+'개. 공격 빈도·발동 시각이 확인될 때까지 자동 피해를 지급하지 않습니다.',
    '- 지속 피해: '+audit.knownPeriodicSkills+'개. 송곳 화살·협공 저주·약화의 낙인·고통의 연쇄의 수치/주기를 별도 시간축으로 계산합니다. 협공 저주의 5초는 공통 Curse 효과 문구에서 해석한 입력이며 별도 지속 시간 검증이 필요합니다.', '',
    '각 틱은 전투 종료까지만 계산합니다. 공격 불가 구간에도 효과 시간은 흐르며 그 구간의 피해는 사라집니다. 같은 스킬의 갱신 방식과 치명 규칙은 입력 가정이며 적중률 100% 미만에서는 확률적 적용·갱신을 임의로 지급하지 않습니다. 문양 0–5중첩 피해표를 적용하되 소모·갱신 방식은 아직 가정입니다. 원문과 전 항목 조사는 [생성 카탈로그](../../docs/data/dps.json) 및 [계산 규칙](../../dpsmath.py)에 연결됩니다.', '',
    '## 학습 결과 / Learned policies', '',
    '각 변화율은 같은 직업·같은 입력에서 기존 우선순위와 비교한 값입니다. 다른 직업끼리 실제 전투력을 비교한 순위가 아닙니다. 학습 시드 3개와 분리한 학습/검증/테스트를 사용하며 학습 점수로만 정책과 시드를 선택합니다. 원문은 사람이 주석 처리한 정성적 순서 후보로만 사용합니다.', '',
    '| 직업 | 직접 피해 수치 | 검증 평균 변화 | 테스트 평균 변화 | 학습 공간 전수 비교 |',
    '| --- | --- | --- | --- | --- |'];
  for(const c of results.classes)lines.push(`| ${c.ko} | ${c.directCount}/${c.activeCount} | ${c.validationMeanChangePercent.toFixed(2)}% | ${c.testMeanChangePercent.toFixed(2)}% | ${c.trainingGapToRestrictedOracle===null?'공간이 커서 미실시':c.trainingGapToRestrictedOracle.toFixed(8)} |`);
  lines.push('', '0%는 개선을 찾지 못했다는 뜻이고 음수는 테스트 입력에서 손해를 봤다는 뜻입니다. 모든 실패도 그대로 보존합니다. 현재 6–11개 기술의 정적 우선순위를 탐색합니다. 전수 비교 한도(6개)를 넘는 공간은 전수 검증하지 않으며 최적해를 보장하지 않습니다.', '',
    '고통의 연쇄의 직접/지속 피해를 넣었으므로 이전 보고서의 “피해 0 준비기를 건너뛰어 얻은 개선”을 그대로 재사용하지 않습니다. 신규 결과에는 기존/학습 회전의 사용 횟수·직접 피해·지속 피해·틱 수가 모두 보존됩니다. 정령성은 직접 공격 7개가 들어갔지만 소환 공격 및 실제 원소 획득 시간축은 없어서 융합을 자동 사용할 수 없습니다.', '',
    '## 미검증 규칙의 민감도 / Assumption sensitivity', '',
    '아래는 학습한 정책을 그대로 두고 가정만 바꾼 테스트 평균 변화입니다. 재학습이나 시드 선택에는 쓰지 않았습니다. 가정에 따라 변화율이 크게 바뀌면 실제 최적 패턴으로 확정할 수 없습니다.', '',
    '| 직업 | 직접 피해만 | 지속 피해 독립 중첩 | 지속 피해 치명 허용 | 문양 소모 없음 |',
    '| --- | --- | --- | --- | --- |');
  for(const c of results.classes)lines.push('| '+c.ko+' | '+c.assumptionSensitivity.map(x=>x.meanChangePercent.toFixed(2)+'%').join(' | ')+' |');
  lines.push('', 'English: source-backed base-1 direct terms increased from 26 to 72. Four DoT formulas have real tick scheduling, fight-end truncation and invulnerability suppression. First-tick phase, critical behavior, refresh and Insignia consumption are explicit research assumptions. Charges/summons/traps stay unavailable without verified timing inputs; non-attacks are separately classified. All eight classes share the declared stat and skill-level profile. Categorical proposal distributions are fitted only to training rewards; held-out and sensitivity results never select policies. No independent combat targets, measured gear loadouts or complete damage/animation models exist, so class tiers remain blocked.', '',
    '## 최종 티어가 아직 차단되는 이유 / Tier blockers', '');
  results.tierAssessment.blockers.forEach((blocker,i)=>lines.push('- '+results.tierAssessment.blockersKo[i]+' / '+blocker));
  lines.push('', '재현과 출처: [README](README.md), [claims](claims.json), [공통 입력](scenarios.json), [model](model.json), [results](results.json). 코드와 입력 SHA-256이 바뀌면 저장 결과를 재학습해야 검증을 통과합니다.', '');
  return lines.join('\n');
}
function closeNumber(actual, expected) {
  assert(Math.abs(actual-expected) <= 1e-9*Math.max(1,Math.abs(expected)), `Stale metric: ${actual} != ${expected}`);
}
function verifyArtifacts(inputs, model, results) {
  validateInputs(inputs);
  assert.equal(model.kind, 'categorical-cross-entropy-policy-search');
  assert.equal(model.purpose, 'research-only');
  assert.equal(results.purpose, 'research-only');
  assert.equal(results.scenarioKind, inputs.curriculum.kind);
  assert.deepEqual(model.provenance, provenance(), 'Input/code changed; retrain before using saved results');
  assert.equal(model.trainedOnCombatLogs, false);
  assert.equal(model.currentPatchEquivalent, false);
  assert.equal(results.modelSha256, hash(Buffer.from(jsonText(model))));
  assert.deepEqual(results.tierAssessment, tierAssessment(inputs.catalog));
  assert.deepEqual(model.commonBuildProfile,inputs.curriculum.sharedBuild);
  assert.deepEqual(results.commonBuildProfile,inputs.curriculum.sharedBuild);
  assert.deepEqual(model.classes.map(c => c.id), inputs.catalog.classes.map(c => c.id));
  assert.deepEqual(results.classes.map(c => c.id), inputs.catalog.classes.map(c => c.id));
  for (const c of inputs.catalog.classes) {
    const saved = model.classes.find(x => x.id === c.id);
    const row = results.classes.find(x => x.id === c.id);
    const evaluate = evaluator(c, inputs.curriculum);
    const hints = projectedHints(c, inputs.claims, model.authorHintsOptedIn);
    assert.deepEqual(saved.skillIds, c.skills.map(s => s.id));
    assert.deepEqual(saved.eligibleHintRuleIds, hints.map(h => h.ruleId));
    assert.deepEqual(saved.runs.map(r => r.seed), model.settings.seeds);
    for (const run of saved.runs) {
      validatePolicy(run.policy, c.skills.map(s => s.id), inputs.curriculum.holdSeconds);
      closeNumber(run.trainingScore, evaluate.score(run.policy).score);
      assert.equal(run.rankPositionProbabilities.length, c.skills.length);
      assert(run.rankPositionProbabilities.every(row => row.length === c.skills.length));
      assert.equal(run.holdProbabilities.length, inputs.curriculum.holdSeconds.length);
      for (const probabilities of [...run.rankPositionProbabilities, run.holdProbabilities]) {
        assert(probabilities.every(p => Number.isFinite(p) && p > 0 && p <= 1));
        closeNumber(probabilities.reduce((a,b) => a+b,0), 1);
      }
    }
    const selected = saved.runs.find(r => r.seed === saved.selectedSeed);
    const best = [...saved.runs].sort((a,b) => compareCandidates(
      {policy:a.policy,score:a.trainingScore}, {policy:b.policy,score:b.trainingScore}) || a.seed-b.seed)[0];
    assert.equal(selected.seed, best.seed, 'Selection must use training reward only');
    assert.deepEqual(row.policy, selected.policy);
    closeNumber(row.trainingScore, selected.trainingScore);
    const oracle = restrictedOracle(c, inputs.curriculum, evaluate);
    assert.deepEqual(row.restrictedOracle, oracle);
    if (oracle.score !== undefined) closeNumber(row.trainingGapToRestrictedOracle, oracle.score-selected.trainingScore);
    closeNumber(row.greedyTrainingScore, evaluate.score(greedyPolicy(c,inputs.curriculum.base.attack)).score);
    assert.deepEqual(row.projectedHints, hints.map(h => ({ruleId:h.ruleId,policy:h.policy,trainingScore:evaluate.score(h.policy).score})));
    assert.deepEqual(row.replicaTestMeanChanges, saved.runs.map(r => ({seed:r.seed,changePercent:meanChange(splitMetrics(c,inputs.curriculum,'test',r.policy))})));
    assert.deepEqual(row.assumptionSensitivity,assumptionSensitivity(c,inputs.curriculum,selected.policy));
    for (const split of ['training','validation','test']) {
      const metrics = splitMetrics(c, inputs.curriculum, split, selected.policy);
      assert.equal(row[split].length, metrics.length);
      row[split].forEach((old, i) => {
        assert.equal(old.scenario, metrics[i].scenario);
        closeNumber(old.baselineEdps, metrics[i].baselineEdps);
        closeNumber(old.policyEdps, metrics[i].policyEdps);
        closeNumber(old.changePercent, metrics[i].changePercent);
        assert.deepEqual(old.casts, metrics[i].casts);
        assert.deepEqual(old.baselineCasts, metrics[i].baselineCasts);
        assert.deepEqual(old.damage, metrics[i].damage);
        assert.deepEqual(old.baselineDamage, metrics[i].baselineDamage);
        assert.deepEqual(old.blocked, metrics[i].blocked);
        assert.deepEqual(old.warnings, metrics[i].warnings);
      });
      if (split !== 'training') closeNumber(row[split+'MeanChangePercent'], meanChange(metrics));
    }
  }
  assert.equal(fs.readFileSync(path.join(__dirname, 'REPORT.md'),'utf8'), report(results), 'Stale report');
}
if (require.main === module) {
  const flags = new Set(process.argv.slice(2));
  assert([...flags].every(f => ['--verify','--allow-unverified-guide-priors'].includes(f)), 'Unknown option');
  const inputs = loadInputs();
  if (flags.has('--verify')) {
    verifyArtifacts(inputs, read('research/rotation-learning/model.json'), read('research/rotation-learning/results.json'));
    console.log('Rotation research artifacts verified: provenance, constrained policies, held-out metrics and blocked tiers.');
  } else {
    const {model, results} = runResearch(inputs, flags.has('--allow-unverified-guide-priors'));
    const modelText = jsonText(model);
    results.modelSha256 = hash(Buffer.from(modelText));
    fs.writeFileSync(path.join(__dirname, 'model.json'), modelText);
    fs.writeFileSync(path.join(__dirname, 'results.json'), jsonText(results));
    fs.writeFileSync(path.join(__dirname, 'REPORT.md'), report(results));
    console.log('Saved research-only policies for '+model.classes.length+' classes; tiers remain blocked.');
    for (const c of results.classes) console.log(c.ko+': synthetic test change '+c.testMeanChangePercent.toFixed(2)+'%; training-space gap '+c.trainingGapToRestrictedOracle);
  }
}
module.exports = {validateInputs, validatePolicy, loadInputs, buildInput, selector, simulatePolicy,
  projectedHints, evaluator, learn, restrictedOracle, runResearch, tierAssessment, verifyArtifacts};

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
  'research/rotation-learning/scenarios.json', 'research/rotation-learning/train.js'];
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
  assert.equal(claims.purpose, 'research-only');
  assert.equal(claims.canSeedLiveCalculator, false);
  assert.equal(curriculum.kind, 'synthetic-simulator-curriculum');
  assert.equal(curriculum.isCombatMeasurement, false);
  assert.equal(evidence.rankVerified, false);
  const classIds = catalog.classes.map(c => c.id);
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
      blocked:Object.fromEntries(result.breakdown.filter(s => s.blocked.length).map(s => [s.id, s.blocked])),
      warnings:result.warnings};
  });
}
const meanChange = metrics => metrics.reduce((sum, m) => sum + m.changePercent, 0) / metrics.length;
function tierAssessment(catalog) {
  const direct = catalog.classes.reduce((sum, c) => sum + c.directCount, 0);
  const active = catalog.classes.reduce((sum, c) => sum + c.conditionAudit.length, 0);
  return {canPublishTiers:false, tiers:null, directDamageCoverage:{included:direct, active, omitted:active-direct},
    blockersKo:[
      `액티브 ${active}개 중 ${active-direct}개의 기본 직접 피해가 없으며, 준비 기술의 0 피해는 실측 결과가 아닙니다.`,
      '기본 동작 시간은 임시 값으로, 실제 모션과 평타 캔슬을 측정하지 않았습니다.',
      '동일 장비 예산·스킬 레벨·특화·패시브를 갖춘 실제 빌드를 비교하지 않았습니다.',
      '지속 피해·정령 공격·파티 버프·차징 단계·확률 초기화가 보상 모델에서 빠져 있습니다.',
      'MP는 미검증 모드이며, 제공한 상태 구간은 실제 유지율을 측정한 값이 아닙니다.',
      '한국 공략과 현재 Global의 조건 대응이 미검증이고, 실전 피해 정답 데이터가 없습니다.',
      '검증·테스트에도 같은 불완전한 엔진을 쓰므로 실제 게임의 정확도가 검증된 것은 아닙니다.'
    ],
    blockers:[
      `${active-direct}/${active} active skills have no default direct-damage seed; helper zero damage is not a measured total.`,
      'Default action durations are placeholders, not measured animation/cancel times.',
      'Equipment, skill levels, specializations and passives are not calibrated to comparable real builds.',
      'DoT, pet attacks, party buffs, charge stages and reset probabilities remain outside this partial reward model.',
      'MP mode is explicitly unverified; synthetic availability windows are not measured uptime.',
      'KR guide mapping to current Global rules remains unverified; no measured combat target labels exist.',
      'Held-out simulator scenarios share the same incomplete engine; they cannot validate live-game damage.'
    ]};
}
function runResearch(inputs, allowHints) {
  validateInputs(inputs);
  const {catalog, claims, curriculum} = inputs;
  const settings = {generations:10, population:96, eliteFraction:0.15, learningRate:0.65, pseudocount:0.5, seeds:[7,19,41]};
  const model = {schema:1, kind:'categorical-cross-entropy-policy-search', purpose:'research-only',
    trainingReward:'Mean within-class eDPS ratio to the existing catalog priority, over training scenarios only.',
    trainedOnCombatLogs:false, trainedOnCopiedArticleText:false, currentPatchEquivalent:false,
    authorHintsOptedIn:allowHints, provenance:provenance(), settings, classes:[]};
  const results = {schema:1, purpose:'research-only', scenarioKind:curriculum.kind,
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
      learningStatus:c.skills.length < 2 ? 'no-order-choice-in-partial-catalog' : 'partial-model-policy-search'});
  }
  return {model, results};
}
function report(results) {
  const coverage = results.tierAssessment.directDamageCoverage;
  const lines = ['# 공략 기반 회전 학습 연구 / Guide-informed rotation learning', '',
    '이 결과는 공략의 우선순위 후보를 이용해 **부분 시뮬레이터 안에서** 학습한 회전입니다. 실제 전투 로그를 학습하거나 검증된 최적 DPS·직업 티어를 얻은 결과가 아닙니다.', '',
    '현재 직접 피해 입력은 '+coverage.included+'/'+coverage.active+' 액티브이며 '+coverage.omitted+'개가 빠져 있습니다. 동작 시간도 임시 입력입니다. 아래 개선률은 같은 직업·같은 입력에서 기존 우선순위와 비교한 값이며, 서로 다른 직업의 실제 전투력 차이가 아닙니다.', '',
    '텍스트는 사람이 검토해 규칙으로 주석 처리했습니다. 원문을 대량 복제하거나 언어 모델을 미세조정하지 않았습니다. 선택적 공략 후보로 탐색을 시작하고, 좋은 후보를 낸 우선순위 위치·대기 값의 확률을 반복 갱신했습니다. 학습 시드 3개와 별도 검증/테스트 시나리오를 사용했습니다. 모델·결과 JSON에 코드와 입력 파일의 SHA-256을 기록합니다.', '',
    '| 직업 | 직접 피해 범위 | 검증 시나리오 평균 변화 | 테스트 시나리오 평균 변화 | 학습 공간 최적값과의 차이 |',
    '| --- | --- | --- | --- | --- |'];
  for (const c of results.classes) lines.push(`| ${c.ko} | ${c.directCount}/${c.activeCount} | ${c.validationMeanChangePercent.toFixed(2)}% | ${c.testMeanChangePercent.toFixed(2)}% | ${c.trainingGapToRestrictedOracle === null ? '미확인' : c.trainingGapToRestrictedOracle.toFixed(8)} |`);
  lines.push('', '0%는 개선을 찾지 못했다는 뜻이며 최적의 실제 직업이라는 뜻이 아닙니다. 정령성은 현재 피해 입력이 냉기 충격 한 개뿐이어서 기술 간 순서를 배울 수 없습니다. 테스트 변화가 음수이면 그대로 실패 결과로 남깁니다.', '',
    '치유성 개선에는 외부에서 합성 고통의 연쇄 구간이 주어진 상황에서, 피해 0으로 처리된 고통의 연쇄 준비기를 덜 써서 시간을 절약하는 효과가 포함됩니다. 실제 고통의 연쇄의 피해·직접 유지·디버프 가치가 빠져 있으므로 이를 실제 최적 회전이나 향상률로 해석할 수 없습니다. 결과 JSON은 기존/학습 회전의 사용 횟수를 함께 보존해 이 효과를 드러냅니다.', '',
    '전수 비교의 범위는 현재 들어 있는 기술의 고정 우선순위와 선언된 쿨타임 대기 값뿐입니다. 버프 배율·평타 캔슬·상황별 오프닝·정령 공격·확률 초기화를 포함한 전체 게임의 최적해를 보장하지 않습니다. 살성의 버프 정렬이나 마도성의 차징 대기는 주장 데이터에 기록했지만 현재 보상 함수에 구현하지 않았습니다.', '',
    'These are learned policies in a partial synthetic simulator, not measured expert rotations or live-game tiers. Text was manually annotated; categorical proposal probabilities were fitted to training rewards. Three seeds and distinct validation/test conditions are retained, including regressions. Exhaustive comparison certifies only the declared static-priority/cooldown-hold family on training scenarios. The same incomplete engine generates every split, so this is robustness testing, not independent combat validation.', '',
    '## 최종 티어가 아직 차단되는 이유 / Tier blockers', '');
  results.tierAssessment.blockers.forEach((blocker,i) => lines.push('- '+results.tierAssessment.blockersKo[i]+' / '+blocker));
  lines.push('', '다음 입력은 직업별 동일 장비 예산·스킬 레벨·특화, 실제 동작/적중 시각, MP 수지, 버프·DoT·정령의 공격 시간축, 초기화 반복 실험입니다. 그 입력으로 공략 후보를 다시 학습하고 실제 로그의 사용 횟수·피해 분포를 재현한 뒤 티어를 평가해야 합니다.', '',
    'Full inputs and independently measured replay targets are required before comparing class tiers. See [claims](claims.json), [model](model.json), [results](results.json), and [reproduction instructions](README.md).', '');
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

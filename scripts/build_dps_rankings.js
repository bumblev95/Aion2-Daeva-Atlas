'use strict';
// Build-time publication only. Partial tooltip simulations never enter this path.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const assert = require('node:assert/strict');
const ROOT = path.resolve(__dirname, '..');
const CLASS_META = {
  gladiator: ['Gladiator','검성','#eeab66','damage'], templar: ['Templar','수호성','#79b6fb','tank'],
  assassin: ['Assassin','살성','#d895ed','damage'], ranger: ['Ranger','궁성','#8ecd91','damage'],
  sorcerer: ['Sorcerer','마도성','#ac9df3','damage'], spiritmaster: ['Spiritmaster','정령성','#ef927b','damage'],
  cleric: ['Cleric','치유성','#76d5ba','healer'], chanter: ['Chanter','호법성','#e5c779','support']
};
const IDS = Object.keys(CLASS_META);
const jsonText = value => JSON.stringify(value,null,2)+'\n';
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const read = file => JSON.parse(fs.readFileSync(path.join(ROOT,file),'utf8'));
const number = n => assert(Number.isFinite(n) && n>=0,'Invalid observation number');
const integer = n => {number(n);assert(Number.isSafeInteger(n),'Invalid observation count');};
const FIELDS = ['scripts/build_dps_rankings.js','scripts/review_dps_observations.py','data/dps-observations.json'];

function validateInputs(input) {
  assert.equal(input.schema,1);assert.equal(input.kind,'reviewed-public-combat-summaries');
  assert.deepEqual(input.publishers,['AionFlex','JaMeter']);assert.equal(input.launchClassCount,8);
  assert(/^\d{4}-\d{2}-\d{2}$/.test(input.reviewedAt));
  assert(!Number.isNaN(Date.parse(input.collectedAt)));
  assert(new Set(input.datasets.map(d=>d.id)).size===input.datasets.length,'Duplicate scope');
  assert.deepEqual(input.datasets.map(d=>d.id).sort(),['basilus','global-balance','griosa','jameter-complete','jameter-current','kr-balance','turgen']);
  for(const d of input.datasets) {
    assert(Object.keys(d).every(k=>['id','kind','publisher','region','regionVerified','window','source',
      'sourceHtmlSha256','metric','patchId','sameEquipment','rawFightTotalsAvailable','rows','sourceAsOf',
      'commonBand','sourceWithheld','bossId','en','ko','instance','difficulty','periodStart','periodEnd',
      'provisional'].includes(k)),'Unknown comparison condition');
    assert(['balance','record','weekly','band'].includes(d.kind),'Unsupported metric');
    const url=new URL(d.source);
    if(['weekly','band'].includes(d.kind)) {
      assert.equal(d.publisher,'JaMeter');assert.equal(url.origin,'https://jameter.net');
      assert.equal(d.region,'UNSPECIFIED');assert.equal(d.regionVerified,false,'Do not invent a report region');
      assert.equal(d.window,'source-week');assert.equal(d.sourceAsOf,null);
      assert.equal(url.pathname,'/report/week/'+d.periodStart);
      assert.equal(Date.parse(d.periodEnd)-Date.parse(d.periodStart),7*86400000);
      assert.equal(d.metric,d.kind==='weekly'?'boss-cp-ratio-index':'cp-band-median-dps');
      assert.equal(typeof d.provisional,'boolean');
      if(d.kind==='band')assert.equal(d.provisional,false,'Matched comparison is the completed week');
    } else {
      assert.equal(d.publisher,'AionFlex');assert.equal(d.regionVerified,true);
      assert(['GLOBAL','KR'].includes(d.region),'Do not combine service regions');
      assert.equal(url.origin,'https://aionflex.gg');assert.equal(url.searchParams.get('region'),d.region.toLowerCase());
    }
    assert(/^[a-f0-9]{64}$/.test(d.sourceHtmlSha256),'Missing source hash');
    assert.equal(d.rawFightTotalsAvailable,false,'Review raw-log DPS separately');
    assert.equal(d.sameEquipment,false,'Do not claim identical builds');assert.equal(d.patchId,null);
    assert.deepEqual(d.rows.map(r=>r.classId).sort(),[...IDS].sort(),'Incomplete or duplicate classes');
    if(d.kind==='record') {
      assert.equal(d.region,'KR');assert.equal(d.window,'all-time');
      assert.equal(d.metric,'published-record-dps');assert.equal(d.difficulty,'hard');
      assert.equal(d.instance,'DaevaCitadel');assert(/^\d+$/.test(d.bossId));
      assert(url.pathname.startsWith('/rankings/boss/'+d.bossId+'-'),'Wrong boss source');
    } else if(d.kind==='balance') {
      assert.equal(d.window,'30d');assert.equal(url.searchParams.get('window'),'30d');
      assert.equal(url.pathname,'/meta/classes');assert.equal(d.metric,'normalized-index');
      assert(!Number.isNaN(Date.parse(d.sourceAsOf)));
    }
    for(const r of d.rows) {
      assert(Object.keys(r).every(k=>['classId','value','resolution','topEnd','characterWeeks','parses',
        'characters','uploaders','bosses','publishedRecords','publishedDps','sampleCount'].includes(k)),
        'No role weights, fabricated builds or source rank');
      if(r.value!==null)number(r.value);
      number(r.resolution);assert(r.resolution>0);
      if(d.kind==='record'||d.kind==='band') {
        if(d.kind==='record'){integer(r.publishedRecords);assert(r.publishedRecords>0);}
        else {integer(r.sampleCount);assert(r.sampleCount>0);}
        const match=d.kind==='record'?/^(\d+(?:\.\d+)?)([KM]?)\/s$/.exec(r.publishedDps):/^(\d+(?:\.\d+)?)(만)$/.exec(r.publishedDps);
        assert(match,'Unknown source precision');
        const scale={'':1,K:1000,M:1000000,'만':10000}[match[2]];
        assert.equal(r.value,Number(match[1])*scale,'Published DPS/value mismatch');
        assert.equal(r.resolution,scale/(10**((match[1].split('.')[1]||'').length)),'Invented precision');
      } else if(d.kind==='balance') {
        for(const field of ['characterWeeks','parses','characters','bosses'])integer(r[field]);
        if(r.uploaders!==null)integer(r.uploaders);
        if(r.topEnd!==null)number(r.topEnd);
        assert.equal(r.resolution,1,'Public indices are rounded to whole points');
        assert(r.parses>=r.characterWeeks && r.characterWeeks>=r.characters,'Inconsistent source counts');
      } else {
        integer(r.sampleCount);assert.equal(r.resolution,.01);
        if(r.value!==null)assert.equal(Math.round(r.value*100)/100,r.value,'Invented weekly index precision');
      }
    }
  }
}

function balanceEligible(d) {
  return !d.sourceWithheld && Boolean(d.commonBand) && d.rows.every(r=>r.value!==null && r.topEnd!==null &&
    r.characterWeeks>=100 && r.uploaders!==null && r.uploaders>=10 && r.bosses>=3);
}

function eligible(d) {
  if(d.kind==='balance')return balanceEligible(d);
  if(d.kind==='record')return true;
  return !d.sourceWithheld && (d.kind!=='band'||Boolean(d.commonBand)) &&
    d.rows.every(r=>r.value!==null && r.sampleCount>=(d.kind==='weekly'?50:20));
}

function rankRows(rows, enabled=true) {
  assert(new Set(rows.map(r=>r.classId)).size===rows.length,'Duplicate class');
  const ordered=rows.map(r=>{
    assert(CLASS_META[r.classId],'Unknown class');
    if(enabled)number(r.value);
    const [en,ko,color,role]=CLASS_META[r.classId];
    return {...r,en,ko,color,role,rank:null};
  });
  if(!enabled)return ordered.sort((a,b)=>IDS.indexOf(a.classId)-IDS.indexOf(b.classId));
  // Publication precision limits ordering. Equal public values share a place;
  // no unseen decimals, role caps or healer-specific penalties are added.
  ordered.sort((a,b)=>b.value-a.value||a.classId.localeCompare(b.classId));
  for(let i=0;i<ordered.length;i++)ordered[i].rank=i && ordered[i].value===ordered[i-1].value?ordered[i-1].rank:i+1;
  return ordered;
}

function compute(input) {
  validateInputs(input);
  return {
    schema:2,kind:'server-published-observed-dps-comparison',sourceReviewedAt:input.reviewedAt,
    collectedAt:input.collectedAt,publishers:input.publishers,
    scope:{canDescribeAsEndgameTier:false,canDescribeAsCurrentPatchRanking:false,
      rawFightDpsRecomputed:false,usesTooltipSimulation:false,healingAddedToDamage:false,
      partyBuffDamageAttributedToHealer:false,launchClassCount:8},
    methodology:{noUserInputs:true,noClientSimulation:true,
      sort:'descending published metric within one region / metric / time window / boss scope',
      precision:'retain published precision; equal public values share a place',
      normalizedIndexSource:input.methodologySource,
      observations:'Public aggregate and record summaries, not raw fights or controlled final builds'},
    provenance:{files:Object.fromEntries(FIELDS.map(f=>[f,hash(fs.readFileSync(path.join(ROOT,f)))]))},
    comparisons:input.datasets.map(d=>{
      const ranked=eligible(d);
      return {...d,status:ranked?(d.provisional?'provisional':'observed'):'insufficient',orderedBy:d.metric,
        rankMeaning:d.kind==='record'?'published record order':'published summary metric order',
        rows:rankRows(d.rows,ranked)};
    })
  };
}

function csv(result) {
  const columns=['scope','publisher','region','region_verified','window','period_start','period_end','provisional','boss','metric','place','class','published_value','resolution',
    'top_end_index','published_records','sample_count','character_weeks','parses','uploaders','bosses','status',
    'same_equipment','patch_id','raw_dps_recomputed','reviewed_at','source_as_of','source'];
  const cell=v=>{let s=v===null||v===undefined?'':String(v);if(/^[=+@-]/.test(s))s="'"+s;
    return /[\n\r,\"]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
  return [columns,...result.comparisons.flatMap(d=>d.rows.map(r=>[
    d.id,d.publisher,d.region,d.regionVerified,d.window,d.periodStart,d.periodEnd,d.provisional,d.bossId||'',d.metric,r.rank,r.classId,r.value,r.resolution,r.topEnd,
    r.publishedRecords,r.sampleCount,r.characterWeeks,r.parses,r.uploaders,r.bosses,d.status,false,'',false,
    result.sourceReviewedAt,d.sourceAsOf,d.source]))].map(row=>row.map(cell).join(',')).join('\n')+'\n';
}

function run(mode) {
  const result=compute(read('data/dps-observations.json'));
  const files={'data/dps-rankings.json':jsonText(result),'data/dps-rankings.csv':csv(result)};
  for(const [file,text]of Object.entries(files)) {
    if(mode==='--verify')assert.equal(fs.readFileSync(path.join(ROOT,file),'utf8'),text,'Stale public comparison: '+file);
    else fs.writeFileSync(path.join(ROOT,file),text);
  }
  console.log('Observed DPS: regional/sample gates, source precision and read-only JSON/CSV verified.');
}
if(require.main===module) {
  const mode=process.argv[2]||'--build';
  assert(['--build','--verify'].includes(mode),'Use --build or --verify. Tooltip training cannot publish class rankings.');
  run(mode);
}
module.exports={validateInputs,balanceEligible,eligible,rankRows,compute,csv,
  loadInputs:()=>read('data/dps-observations.json')};

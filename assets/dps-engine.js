/* Deterministic conditional rotation. Expected damage is not a sampled hit/proc. */
(function (host) {
  'use strict';
  function number(value, name, min, max) {
    if (value === null || value === undefined || String(value).trim() === '') throw new Error(name);
    const n = Number(value);
    if (!Number.isFinite(n) || n < min || n > max) throw new Error(name);
    return n;
  }
  function downtime(text, duration) {
    if (!String(text || '').trim()) return [];
    const intervals = String(text).split(',').map(part => {
      const match = part.trim().match(/^(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)$/);
      if (!match) throw new Error('downtime');
      const a = number(match[1], 'downtime', 0, duration), b = number(match[2], 'downtime', 0, duration);
      if (b <= a) throw new Error('downtime');
      return [a, b];
    }).sort((a, b) => a[0] - b[0]);
    const merged = [];
    intervals.forEach(x => {
      const last = merged[merged.length - 1];
      if (last && x[0] <= last[1]) last[1] = Math.max(last[1], x[1]); else merged.push(x.slice());
    });
    return merged;
  }
  const EPS = 1e-8;
  const control = new Set(['slow','root','stun','knockdown','frost','stagger']);
  function stateId(id) {
    if (typeof id !== 'string' || !/^[a-z][a-z0-9:-]{0,79}$/.test(id)) throw new Error('state');
    return id;
  }
  function stateWindows(raw, duration) {
    if (raw === undefined) return {};
    if (!raw || typeof raw !== 'object' || Array.isArray(raw)) throw new Error('state windows');
    return Object.fromEntries(Object.keys(raw).sort().map(id => [stateId(id),downtime(raw[id],duration)]).filter(([,v])=>v.length));
  }
  function elementTimes(raw, duration) {
    if (!String(raw || '').trim()) return [];
    return String(raw).split(',').map(x=>number(x,'element times',0,duration)).sort((a,b)=>a-b);
  }
  function simulate(raw, patch = false, choose = null) {
    if (choose !== null && typeof choose !== 'function') throw new Error('policy');
    if (raw.conditionsVerified === false) throw new Error('condition-snapshot');
    if (raw.damageVerified === false) throw new Error('damage-snapshot');
    const duration = number(raw.duration, 'duration', 1, 600);
    const attack = number(raw.attack, 'attack', 0, 10000000);
    const crit = number(raw.crit, 'crit', 0, 100) / 100;
    const critMultiplier = number(raw.critMultiplier, 'critMultiplier', 1, 10);
    const accuracy = number(raw.accuracy, 'accuracy', 0, 100) / 100;
    const factor = number(raw.factor, 'factor', 0, 100);
    const gaps = downtime(raw.downtime, duration);
    const windows = stateWindows(raw.stateWindows, duration);
    const resourceMode = raw.resourceMode || 'unverified';
    if (!['unverified','budget'].includes(resourceMode)) throw new Error('resource mode');
    const mpMax = resourceMode === 'budget' ? number(raw.mpMax,'MP maximum',0,10000000) : 0;
    const mpRegen = resourceMode === 'budget' ? number(raw.mpRegen,'MP regeneration',0,100000) : 0;
    let mp = resourceMode === 'budget' ? number(raw.mpStart,'MP start',0,mpMax) : 0;
    let elements = number(raw.elementsStart ?? 0,'element stacks',0,4);
    if (!Number.isInteger(elements)) throw new Error('element stacks');
    const elementEvents = elementTimes(raw.elementEvents, duration);
    const conditionMode = raw.conditionMode || 'tooltip';
    const targetControl = raw.targetControl || 'unknown';
    const targetType = raw.targetType || 'unknown';
    if (!['unknown','npc','player'].includes(targetType)) throw new Error('target type');
    const region = raw.region, fireMarkEnabled = raw.fireMarkEnabled;
    const periodicMode = raw.periodicMode || 'omit', periodicCrit = raw.periodicCrit || 'none';
    const periodicRefresh = raw.periodicRefresh || 'replace', insigniaMode = raw.insigniaMode || 'unverified';
    const dotStateMode = raw.dotStateMode || 'omit';
    if (!['omit','inputs'].includes(periodicMode) || !['none','normal'].includes(periodicCrit) ||
        !['replace','stack'].includes(periodicRefresh) || !['unverified','consume','retain'].includes(insigniaMode)) throw new Error('damage options');
    if (!['omit','duration'].includes(dotStateMode)) throw new Error('dot state mode');
    if (!['tooltip','windows'].includes(conditionMode) || !['unknown','susceptible','immune'].includes(targetControl)) throw new Error('condition mode');
    const warnings = new Set(resourceMode === 'unverified' ? ['resources-unverified'] : []);
    const skills = raw.skills.filter(s => s.enabled).map(s => ({
      ...s, flat: number(s.flat, 'flat', 0, 100000000), coefficient: number(s.coefficient, 'coefficient', 0, 100000) / 100,
      hits: number(s.hits, 'hits', 1, 1000), cast: number(s.cast, 'cast', .05, 120),
      cooldown: number(patch ? s.afterCooldown : s.cooldown, 'cooldown', 0, 3600),
      delta: patch ? number(s.delta, 'delta', -100, 1000) / 100 : 0,
      requires: (s.requires || []).map(stateId), consumeStates: (s.consumeStates || []).map(stateId),
      effects: (s.effects || []).map(e=>({...e,state:stateId(e.state),
        duration:e.duration == null ? null : number(e.duration,'state duration',.001,3600),
        chance:e.chance == null ? null : number(e.chance,'state chance',0,100),
        npcChance:e.npcChance == null ? null : number(e.npcChance,'NPC state chance',0,100),
        requiresState:e.requiresState ? stateId(e.requiresState) : null})),
      mpCost: s.mpCost == null || String(s.mpCost).trim() === '' ? null : number(s.mpCost,'MP cost',0,10000000),
      mpGain: number(s.mpGain ?? 0,'MP gain',0,10000000),
      elementCost: number(s.elementCost ?? 0,'element cost',0,4),
      charge: Boolean(s.charge), chargeConfirmed: s.chargeConfirmed === true,
      damageInputRequired:s.damageInputRequired === true, damageConfirmed:s.damageConfirmed === true,
      periodic: (s.periodic || []).map(p=>{const result={flat:number(p.flat,'periodic flat',0,100000000),
        coefficient:number(p.coefficient,'periodic coefficient',0,100000)/100,
        interval:number(p.interval,'periodic interval',.05,600), duration:number(p.duration,'periodic duration',.05,600),
        firstTick:number(p.firstTick ?? p.interval,'first tick',0,600)};
        if(result.firstTick>result.duration+EPS)throw new Error('first tick');return result;}),
      insigniaGain:number(s.insigniaGain ?? 0,'insignia gain',0,5),
      insigniaDuration:number(s.insigniaDuration ?? 10,'insignia duration',.05,600),
      insigniaDamage:s.insigniaDamage ? s.insigniaDamage.map((v,i)=>{
        if (v.stacks !== i) throw new Error('insignia damage');
        return {flat:number(v.flat,'insignia flat',0,100000000),coefficient:number(v.coefficient,'insignia coefficient',0,100000)/100};
      }) : null
    }));
    if (skills.some(s=>s.insigniaDamage && s.insigniaDamage.length !== 6)) throw new Error('insignia damage');
    if (!skills.length) throw new Error('skills');
    let time = 0, total = 0, iterations = 0;
    let clock = 0, elementIndex = 0;
    const states = new Map(), consumedWindows = new Set();
    const ready = skills.map(() => 0), breakdown = skills.map(s => ({id:s.id,name:s.name,casts:0,damage:0,directDamage:0,periodicDamage:0,ticks:0,blocked:[]})), events = [];
    const insignias = [], periodicQueue = [], periodicTokens = new Map();
    let token = 0;
    if (skills.some(s=>s.periodic.length)) warnings.add(periodicMode === 'omit' ? 'periodic-omitted' : 'periodic-timing-assumption');
    if (skills.some(s=>s.insigniaGain || s.insigniaDamage) && insigniaMode !== 'unverified') warnings.add('insignia-consumption-assumption');
    function resourcesTo(to) {
      if (resourceMode === 'budget') mp = Math.min(mpMax,mp + (to-clock)*mpRegen);
      while (elementIndex < elementEvents.length && elementEvents[elementIndex] <= to + EPS) {
        elements = Math.min(4,elements+1); elementIndex++;
      }
      clock = to;
    }
    function advance(to) {
      while (periodicQueue.length && periodicQueue[0].time <= to + EPS) {
        const tick = periodicQueue.shift();
        resourcesTo(tick.time);
        if (periodicRefresh === 'replace' && periodicTokens.get(tick.key) !== tick.token) continue;
        // Invulnerability suppresses a scheduled tick, without pausing its
        // lifetime or banking damage for the next attackable window.
        if (gaps.some(g=>tick.time >= g[0]-EPS && tick.time < g[1]-EPS)) continue;
        total += tick.damage; breakdown[tick.index].damage += tick.damage;
        breakdown[tick.index].periodicDamage += tick.damage; breakdown[tick.index].ticks++;
        events.push({time:tick.time,damage:tick.damage,total,skill:skills[tick.index].id,
          kind:'periodic',mp:resourceMode==='budget'?mp:null,elements});
      }
      resourcesTo(to); time = to;
      while (insignias.length && insignias[0] <= time + EPS) insignias.shift();
    }
    function available(id) {
      if (targetControl === 'immune' && control.has(id)) return false;
      if ((states.get(id) ?? -Infinity) > time + EPS) return true;
      return (windows[id] || []).some((w,i)=>time >= w[0]-EPS && time < w[1]-EPS && !consumedWindows.has(id+':'+i));
    }
    function blocked(s) {
      if (s.requires.length && !s.requires.some(available)) return 'state:'+s.requires.join('|');
      if (s.elementCost > elements + EPS) return 'elements';
      if (resourceMode === 'budget' && s.mpCost === null) return 'mp-unverified';
      if (resourceMode === 'budget' && s.mpCost > mp + EPS) return 'mp';
      if (s.charge && !s.chargeConfirmed) return 'charge-unverified';
      if (s.damageInputRequired && !s.damageConfirmed) return 'damage-unverified';
      if (s.insigniaDamage && insigniaMode === 'unverified') return 'insignia-unverified';
      return null;
    }
    advance(0);
    while (time < duration - 1e-8) {
      if (++iterations > 30000) throw new Error('iteration limit');
      const currentGap = gaps.find(g => time >= g[0] - 1e-8 && time < g[1] - 1e-8);
      if (currentGap) {advance(currentGap[1]); continue;}
      const nextGap = gaps.find(g => g[0] > time + 1e-8);
      const end = nextGap ? nextGap[0] : duration;
      const feasible = [];
      skills.some((s, ix) => {
        if (ready[ix] > time + EPS || time + s.cast > end + EPS) return false;
        const reason = blocked(s);
        if (reason && !breakdown[ix].blocked.includes(reason)) breakdown[ix].blocked.push(reason);
        if (!reason) feasible.push(ix);
        return !choose && !reason;
      });
      let i = feasible.length ? feasible[0] : -1;
      if (i < 0) {
        const future = [duration,...ready.filter(v=>v>time+EPS),
          ...Object.values(windows).flat().map(w=>w[0]).filter(v=>v>time+EPS)];
        if (nextGap) future.push(nextGap[0]);
        if (elementIndex < elementEvents.length) future.push(elementEvents[elementIndex]);
        if (mpRegen > 0) skills.forEach(s=>{
          if (s.mpCost !== null && s.mpCost > mp + EPS && s.mpCost <= mpMax) future.push(time+(s.mpCost-mp)/mpRegen);
        });
        advance(Math.min(...future.filter(v=>v>time+EPS)));
        continue;
      }
      if (choose) {
        // Research policies can select feasible actions or wait. All mechanics,
        // damage, resource changes and cooldown clocks remain owned by this engine.
        const describe = ix => Object.freeze({index:ix,id:skills[ix].id,cast:skills[ix].cast,
          readyAt:ready[ix],requirementsMet:!blocked(skills[ix])});
        const context = Object.freeze({time,end,duration,
          feasible:Object.freeze(feasible.map(describe)),
          cooldowns:Object.freeze(skills.map((s,ix)=>describe(ix)))});
        const decision = choose(context);
        if (decision && typeof decision === 'object' && Object.hasOwn(decision,'waitUntil')) {
          const until = number(decision.waitUntil,'policy wait',0,duration);
          if (until <= time + EPS || until > end + EPS) throw new Error('policy wait');
          advance(Math.min(until,end));
          continue;
        }
        if (!Number.isInteger(decision) || !feasible.includes(decision)) throw new Error('policy action');
        i = decision;
      }
      const s = skills[i], finish = time + s.cast;
      const terms = s.insigniaDamage ? s.insigniaDamage[insignias.length] : s;
      const damage = (terms.flat + terms.coefficient * attack) * s.hits * (1 + crit * (critMultiplier - 1)) * accuracy * factor * (1 + s.delta);
      // Damage uses stacks at cast start; consumption/expiry refresh are
      // explicitly selected assumptions, never inferred from tooltip wording.
      if (s.insigniaDamage && insigniaMode === 'consume') insignias.length = 0;
      ready[i] = time + s.cooldown; // Explicit model assumption: cooldown begins at cast start.
      if (resourceMode === 'budget') mp = Math.max(0,mp-s.mpCost);
      elements -= s.elementCost;
      if (s.chainMode !== 'window') s.consumeStates.forEach(id=>{
        states.delete(id);
        (windows[id] || []).forEach((w,ix)=>{if(time>=w[0]-EPS && time<w[1]-EPS) consumedWindows.add(id+':'+ix);});
      });
      if (s.consumeStates.length) warnings.add('chain-consumption-assumption');
      advance(finish);
      s.effects.forEach(e=>{
        if (conditionMode !== 'tooltip') return;
        if (region === 'KR' && s.conditionRegion === 'Global') {warnings.add('global-only-conditions');return;}
        if (e.passive === 'fire-mark' && fireMarkEnabled === 'no') return;
        if (e.on !== 'hit' && e.on !== 'use') throw new Error('effect trigger');
        const chance = targetType === 'npc' && e.npcChance !== null ? e.npcChance : e.chance;
        if (e.duration === null || chance !== 100) {warnings.add('uncertain-state-effect');return;}
        if (e.requiresState && !available(e.requiresState)) {warnings.add('conditional-state-effect');return;}
        if (e.on === 'hit' && accuracy !== 1) {warnings.add('probabilistic-hit-effects');return;}
        if (control.has(e.state) && targetControl !== 'susceptible') {warnings.add('target-control-unverified');return;}
        if (e.assumption === 'dot-lifetime') {
          warnings.add('dot-lifetime-assumption');
          // Server benchmarks may explicitly use the applied DoT's duration.
          // This never grants independent, externally scheduled status windows.
          if (dotStateMode !== 'duration' || periodicMode !== 'inputs' ||
              !s.periodic.some(p=>Math.abs(p.duration-e.duration)<EPS)) return;
        }
        states.set(e.state,Math.max(states.get(e.state) || 0,finish+e.duration));
      });
      if (resourceMode === 'budget' && s.mpGain) {
        if (accuracy === 1) mp = Math.min(mpMax,mp+s.mpGain);
        else warnings.add('probabilistic-mp-gain');
      }
      if (s.insigniaGain && insigniaMode !== 'unverified') {
        if (accuracy === 1 && !(region === 'KR' && s.conditionRegion === 'Global')) {
          for (let n=0;n<s.insigniaGain && insignias.length<5;n++) insignias.push(finish+s.insigniaDuration);
          insignias.sort((a,b)=>a-b);
        } else warnings.add('insignia-application-unverified');
      }
      total += damage; breakdown[i].casts++; breakdown[i].damage += damage; breakdown[i].directDamage += damage;
      events.push({time:finish,damage,total,skill:s.id,mp:resourceMode==='budget'?mp:null,elements});
      if (periodicMode === 'inputs') s.periodic.forEach((p,j)=>{
        if (accuracy !== 1) {warnings.add('periodic-hit-unverified');return;}
        if (region === 'KR' && s.conditionRegion === 'Global') {warnings.add('global-only-periodic');return;}
        const key = i+':'+j, serial = ++token;
        periodicTokens.set(key,serial);
        const amount = (p.flat+p.coefficient*attack) *
          (periodicCrit === 'normal' ? 1+crit*(critMultiplier-1) : 1) * factor * (1+s.delta);
        if (p.firstTick > p.duration+EPS) throw new Error('first tick');
        for (let n=0;;n++) {
          const at=finish+p.firstTick+n*p.interval;
          if (at > Math.min(duration,finish+p.duration)+EPS) break;
          periodicQueue.push({time:Math.min(at,duration),damage:amount,index:i,key,token:serial});
          if (periodicQueue.length > 30000) throw new Error('periodic event limit');
        }
        periodicQueue.sort((a,b)=>a.time-b.time || a.token-b.token);
      });
      // A user-entered zero first tick is resolved after the application hit.
      advance(finish);
    }
    advance(duration); // Resolve surviving DoT ticks even after the last action.
    const activeTime = duration - gaps.reduce((a, g) => a + g[1] - g[0], 0);
    return {total,edps:total/duration,activeDps:activeTime > 0 ? total/activeTime : 0,activeTime,breakdown,events,warnings:[...warnings],mp:resourceMode==='budget'?mp:null,elements,insignias:insignias.length};
  }
  function conditionKey(x) {
    const duration = Number(x.duration), budget = x.resourceMode === 'budget';
    return JSON.stringify([x.region,x.patch,...['duration','attack','crit','critMultiplier','accuracy','factor'].map(k=>Number(x[k])),
      downtime(x.downtime,duration),x.conditionMode||'tooltip',x.targetControl||'unknown',
      stateWindows(x.stateWindows,duration),x.resourceMode||'unverified',
      budget?[Number(x.mpStart),Number(x.mpMax),Number(x.mpRegen)]:null,
      Number(x.elementsStart||0),elementTimes(x.elementEvents,duration),x.fireMarkEnabled||'yes',
      x.periodicMode||'omit',x.periodicCrit||'none',x.periodicRefresh||'replace',x.insigniaMode||'unverified',x.targetType||'unknown',x.dotStateMode||'omit']);
  }
  function exportCSV(input, result) {
    const value = v => typeof v === 'object' && v !== null ? JSON.stringify(v) : (v ?? '');
    const safe = v => {let s=String(value(v));if(/^[=+\-@]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';};
    const rows = [...Object.entries(input).filter(([k])=>k!=='skills'),['eDPS',result.before.edps],['scenario_eDPS',result.after.edps],
      ['warnings',result.before.warnings],[],['skill','enabled','base','coefficient_pct','hits','cast_s','cooldown_s','damage_delta_pct','after_cooldown_s',
      'id','requires_any','effects','consume_states','chain_mode','mp_cost','mp_gain','element_cost','before_casts','after_casts','blocked',
      'periodic_terms','before_direct_damage','before_periodic_damage','before_ticks','charge_confirmed','insignia_variants',
      'charge_reference','damage_input_required','damage_input_confirmed','insignia_gain','insignia_duration','skill_level']];
    input.skills.forEach(s=>{
      const b=result.before.breakdown.find(x=>x.id===s.id),a=result.after.breakdown.find(x=>x.id===s.id);
      rows.push([s.name,s.enabled,s.flat,s.coefficient,s.hits,s.cast,s.cooldown,s.delta,s.afterCooldown,s.id,s.requires||[],s.effects||[],s.consumeStates||[],s.chainMode||'once',
        s.mpCost,s.mpGain||0,s.elementCost||0,b?.casts||0,a?.casts||0,b?.blocked||[],
        s.periodic||[],b?.directDamage||0,b?.periodicDamage||0,b?.ticks||0,s.chargeConfirmed||false,s.insigniaDamage||[],
        s.charge||null,s.damageInputRequired||false,s.damageConfirmed||false,s.insigniaGain||0,s.insigniaDuration||10,s.skillLevel??1]);
    });
    return '\uFEFF'+rows.map(row=>row.map(safe).join(',')).join('\r\n');
  }
  const api = {simulate,downtime,conditionKey,exportCSV};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  host.CodexDPS = api;
})(typeof window === 'undefined' ? globalThis : window);

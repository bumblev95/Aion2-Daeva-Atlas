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
  function simulate(raw, patch = false) {
    if (raw.conditionsVerified === false) throw new Error('condition-snapshot');
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
        chance:e.chance == null ? null : number(e.chance,'state chance',0,100)})),
      mpCost: s.mpCost == null || String(s.mpCost).trim() === '' ? null : number(s.mpCost,'MP cost',0,10000000),
      mpGain: number(s.mpGain ?? 0,'MP gain',0,10000000),
      elementCost: number(s.elementCost ?? 0,'element cost',0,4)
    }));
    if (!skills.length) throw new Error('skills');
    let time = 0, total = 0, iterations = 0;
    let clock = 0, elementIndex = 0;
    const states = new Map(), consumedWindows = new Set();
    const ready = skills.map(() => 0), breakdown = skills.map(s => ({id:s.id,name:s.name,casts:0,damage:0,blocked:[]})), events = [];
    function advance(to) {
      if (resourceMode === 'budget') mp = Math.min(mpMax,mp + (to-clock)*mpRegen);
      while (elementIndex < elementEvents.length && elementEvents[elementIndex] <= to + EPS) {
        elements = Math.min(4,elements+1); elementIndex++;
      }
      clock = to; time = to;
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
      return null;
    }
    advance(0);
    while (time < duration - 1e-8) {
      if (++iterations > 30000) throw new Error('iteration limit');
      const currentGap = gaps.find(g => time >= g[0] - 1e-8 && time < g[1] - 1e-8);
      if (currentGap) {advance(currentGap[1]); continue;}
      const nextGap = gaps.find(g => g[0] > time + 1e-8);
      const end = nextGap ? nextGap[0] : duration;
      const i = skills.findIndex((s, ix) => {
        if (ready[ix] > time + EPS || time + s.cast > end + EPS) return false;
        const reason = blocked(s);
        if (reason && !breakdown[ix].blocked.includes(reason)) breakdown[ix].blocked.push(reason);
        return !reason;
      });
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
      const s = skills[i], finish = time + s.cast;
      const damage = (s.flat + s.coefficient * attack) * s.hits * (1 + crit * (critMultiplier - 1)) * accuracy * factor * (1 + s.delta);
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
        if (raw.region === 'KR' && s.conditionRegion === 'Global') {warnings.add('global-only-conditions');return;}
        if (e.passive === 'fire-mark' && raw.fireMarkEnabled === 'no') return;
        if (e.on !== 'hit' && e.on !== 'use') throw new Error('effect trigger');
        if (e.duration === null || e.chance !== 100) {warnings.add('uncertain-state-effect');return;}
        if (e.on === 'hit' && accuracy !== 1) {warnings.add('probabilistic-hit-effects');return;}
        if (control.has(e.state) && targetControl !== 'susceptible') {warnings.add('target-control-unverified');return;}
        if (e.assumption === 'dot-lifetime') {warnings.add('dot-lifetime-assumption');return;}
        states.set(e.state,Math.max(states.get(e.state) || 0,finish+e.duration));
      });
      if (resourceMode === 'budget' && s.mpGain) {
        if (accuracy === 1) mp = Math.min(mpMax,mp+s.mpGain);
        else warnings.add('probabilistic-mp-gain');
      }
      total += damage; breakdown[i].casts++; breakdown[i].damage += damage;
      events.push({time:finish,damage,total,skill:s.id,mp:resourceMode==='budget'?mp:null,elements});
    }
    const activeTime = duration - gaps.reduce((a, g) => a + g[1] - g[0], 0);
    return {total,edps:total/duration,activeDps:activeTime > 0 ? total/activeTime : 0,activeTime,breakdown,events,warnings:[...warnings],mp:resourceMode==='budget'?mp:null,elements};
  }
  function conditionKey(x) {
    const duration = Number(x.duration), budget = x.resourceMode === 'budget';
    return JSON.stringify([x.region,x.patch,...['duration','attack','crit','critMultiplier','accuracy','factor'].map(k=>Number(x[k])),
      downtime(x.downtime,duration),x.conditionMode||'tooltip',x.targetControl||'unknown',
      stateWindows(x.stateWindows,duration),x.resourceMode||'unverified',
      budget?[Number(x.mpStart),Number(x.mpMax),Number(x.mpRegen)]:null,
      Number(x.elementsStart||0),elementTimes(x.elementEvents,duration)]);
  }
  function exportCSV(input, result) {
    const value = v => typeof v === 'object' && v !== null ? JSON.stringify(v) : (v ?? '');
    const safe = v => {let s=String(value(v));if(/^[=+\-@]/.test(s))s="'"+s;return '"'+s.replace(/"/g,'""')+'"';};
    const rows = [...Object.entries(input).filter(([k])=>k!=='skills'),['eDPS',result.before.edps],['scenario_eDPS',result.after.edps],
      ['warnings',result.before.warnings],[],['skill','enabled','base','coefficient_pct','hits','cast_s','cooldown_s','damage_delta_pct','after_cooldown_s',
      'id','requires_any','effects','consume_states','chain_mode','mp_cost','mp_gain','element_cost','before_casts','after_casts','blocked']];
    input.skills.forEach(s=>{
      const b=result.before.breakdown.find(x=>x.id===s.id),a=result.after.breakdown.find(x=>x.id===s.id);
      rows.push([s.name,s.enabled,s.flat,s.coefficient,s.hits,s.cast,s.cooldown,s.delta,s.afterCooldown,s.id,s.requires||[],s.effects||[],s.consumeStates||[],s.chainMode||'once',
        s.mpCost,s.mpGain||0,s.elementCost||0,b?.casts||0,a?.casts||0,b?.blocked||[]]);
    });
    return '\uFEFF'+rows.map(row=>row.map(safe).join(',')).join('\r\n');
  }
  const api = {simulate,downtime,conditionKey,exportCSV};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  host.CodexDPS = api;
})(typeof window === 'undefined' ? globalThis : window);

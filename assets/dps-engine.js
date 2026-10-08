/* A conditional rotation model. No game defense, proc or buff formula is implied. */
(function (host) {
  'use strict';
  function number(value, name, min, max) {
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
  function simulate(raw, patch = false) {
    const duration = number(raw.duration, 'duration', 1, 600);
    const attack = number(raw.attack, 'attack', 0, 10000000);
    const crit = number(raw.crit, 'crit', 0, 100) / 100;
    const critMultiplier = number(raw.critMultiplier, 'critMultiplier', 1, 10);
    const accuracy = number(raw.accuracy, 'accuracy', 0, 100) / 100;
    const factor = number(raw.factor, 'factor', 0, 100);
    const gaps = downtime(raw.downtime, duration);
    const skills = raw.skills.filter(s => s.enabled).map(s => ({
      ...s, flat: number(s.flat, 'flat', 0, 100000000), coefficient: number(s.coefficient, 'coefficient', 0, 100000) / 100,
      hits: number(s.hits, 'hits', 1, 1000), cast: number(s.cast, 'cast', .05, 120),
      cooldown: number(patch ? s.afterCooldown : s.cooldown, 'cooldown', 0, 3600),
      delta: patch ? number(s.delta, 'delta', -100, 1000) / 100 : 0
    }));
    if (!skills.length) throw new Error('skills');
    let time = 0, total = 0, iterations = 0;
    const ready = skills.map(() => 0), breakdown = skills.map(s => ({id:s.id,name:s.name,casts:0,damage:0})), events = [];
    while (time < duration - 1e-8) {
      if (++iterations > 30000) throw new Error('iteration limit');
      const currentGap = gaps.find(g => time >= g[0] - 1e-8 && time < g[1] - 1e-8);
      if (currentGap) {time = currentGap[1]; continue;}
      const nextGap = gaps.find(g => g[0] > time + 1e-8);
      const end = nextGap ? nextGap[0] : duration;
      const i = skills.findIndex((s, ix) => ready[ix] <= time + 1e-8 && time + s.cast <= end + 1e-8);
      if (i < 0) {
        const future = ready.filter((v, ix) => v > time + 1e-8 && v + skills[ix].cast <= end + 1e-8);
        time = future.length ? Math.min(...future) : (nextGap ? nextGap[1] : duration);
        continue;
      }
      const s = skills[i], finish = time + s.cast;
      const damage = (s.flat + s.coefficient * attack) * s.hits * (1 + crit * (critMultiplier - 1)) * accuracy * factor * (1 + s.delta);
      ready[i] = time + s.cooldown; // Explicit model assumption: cooldown begins at cast start.
      total += damage; breakdown[i].casts++; breakdown[i].damage += damage;
      events.push({time:finish,damage,total,skill:s.id}); time = finish;
    }
    const activeTime = duration - gaps.reduce((a, g) => a + g[1] - g[0], 0);
    return {total,edps:total/duration,activeDps:activeTime > 0 ? total/activeTime : 0,activeTime,breakdown,events};
  }
  function conditionKey(x) {
    return JSON.stringify([x.region,x.patch,x.duration,x.attack,x.crit,x.critMultiplier,x.accuracy,x.factor,downtime(x.downtime,Number(x.duration))]);
  }
  const api = {simulate,downtime,conditionKey};
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  host.CodexDPS = api;
})(typeof window === 'undefined' ? globalThis : window);

/* Small learning tools; no account connection or third-party requests. */
(() => {
  'use strict';
  const all = (root, selector) => Array.from(root.querySelectorAll(selector));
  const reveal = root => all(root, '[data-ag-controls]').forEach(node => { node.hidden = false; });
  all(document, '[data-option-demo]').forEach(root => {
    const buttons = all(root, '[data-option-mode]');
    const choose = key => {
      buttons.forEach(node => node.setAttribute('aria-pressed', String(node.dataset.optionMode === key)));
      all(root, '[data-option-panel]').forEach(node => { node.hidden = node.dataset.optionPanel !== key; });
    };
    buttons.forEach(node => node.addEventListener('click', () => choose(node.dataset.optionMode)));
    choose('sync'); reveal(root);
  });
  all(document, '[data-stigma-planner]').forEach(root => {
    const ko = root.dataset.lang === 'ko';
    const costs = JSON.parse(root.dataset.costs);
    const from = root.querySelector('[data-stigma-from]');
    const to = root.querySelector('[data-stigma-to]');
    const result = root.querySelector('[data-stigma-result]');
    const update = () => {
      const valid = Number(to.value) >= Number(from.value) && costs[to.value] !== undefined && costs[from.value] !== undefined;
      to.setAttribute('aria-invalid', String(!valid));
      if (!valid) {
        result.textContent = ko ? '목표 레벨을 현재 레벨 이상으로 선택하세요.' : 'Choose a target at or above the current level.';
        return;
      }
      const amount = costs[to.value] - costs[from.value];
      result.textContent = from.value + ' → ' + to.value + (ko ? '레벨에 샤드 ' + amount + '개가 필요합니다.' : ' needs ' + amount + ' Shards.');
    };
    [from, to].forEach(node => node.addEventListener('change', update));
    update(); reveal(root);
  });
  all(document, '[data-pendant-planner]').forEach(root => {
    const ko = root.dataset.lang === 'ko';
    const chances = JSON.parse(root.dataset.chances), bonuses = JSON.parse(root.dataset.bonuses);
    const level = root.querySelector('[data-pendant-level]');
    const failures = root.querySelector('[data-pendant-failures]');
    const chance = root.querySelector('[data-pendant-chance]');
    const bar = root.querySelector('[data-pendant-bar]');
    const result = root.querySelector('[data-pendant-result]');
    const update = () => {
      const count = failures.valueAsNumber;
      const valid = failures.value.trim() !== '' && failures.validity.valid && Number.isSafeInteger(count);
      failures.setAttribute('aria-invalid', String(!valid));
      bar.parentElement.hidden = !valid;
      if (!valid) {
        chance.textContent = '—';
        result.textContent = ko ? '실패 횟수는 0~100 사이의 정수로 입력하세요.' : 'Enter a whole failure count from 0 to 100.';
        return;
      }
      const i = Number(level.value), value = Math.min(100, chances[i] + count * bonuses[i]);
      chance.textContent = value + '%'; bar.style.width = value + '%';
      result.textContent = chances[i] + '% + ' + (ko ? '실패 ' : '') + count + (ko ? '회' : ' failures') + ' × ' + bonuses[i] + '%p = ' + value + '%.';
    };
    level.addEventListener('change', () => { failures.value = '0'; update(); });
    failures.addEventListener('input', update);
    update(); reveal(root);
  });
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  all(document, '[data-raid-lesson]').forEach(root => {
    const ko = root.dataset.lang === 'ko';
    const steps = all(root, '.ag-raid-steps li');
    const play = root.querySelector('[data-raid-play]');
    const next = root.querySelector('[data-raid-next]');
    const speed = root.querySelector('[data-raid-speed]');
    let phase = 0, playing = !reduced.matches, visible = false, elapsed = 0, previous = performance.now();
    const draw = () => {
      root.dataset.phase = String(phase);
      root.dataset.playing = String(playing);
      root.querySelector('[data-raid-label]').textContent = steps[phase].textContent;
      steps.forEach((node, i) => node.classList.toggle('is-active', phase === i));
      play.setAttribute('aria-pressed', String(playing));
      play.textContent = playing ? (ko ? '일시정지' : 'Pause') : (ko ? '재생' : 'Play');
    };
    play.addEventListener('click', () => { playing = !playing; elapsed = 0; draw(); });
    next.addEventListener('click', () => { playing = false; phase = (phase + 1) % steps.length; elapsed = 0; draw(); });
    reduced.addEventListener('change', () => { if (reduced.matches) { playing = false; draw(); } });
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting; elapsed = 0;
    }, {threshold: 0.15}).observe(root);
    else visible = true;
    setInterval(() => {
      const now = performance.now(), delta = Math.min(500, now - previous); previous = now;
      if (!playing || !visible || document.hidden) return;
      elapsed += delta * Number(speed.value);
      if (elapsed >= 3000) { phase = (phase + 1) % steps.length; elapsed = 0; draw(); }
    }, 250);
    draw(); reveal(root);
  });
})();

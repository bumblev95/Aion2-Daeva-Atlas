/* Progressive enhancement: diagrams, target picking and illustrative Kinah costs. */
(() => {
  'use strict';
  const all = (root, selector) => [...root.querySelectorAll(selector)];
  const revealControls = root => all(root, '[data-viz-controls]').forEach(n => { n.hidden = false; });

  function drawEdges(root) {
    const diagram = root.querySelector('.viz-diagram');
    const svg = diagram?.querySelector('.viz-edges');
    if (!svg || getComputedStyle(svg).display === 'none') return;
    const bounds = diagram.getBoundingClientRect();
    svg.setAttribute('viewBox', `0 0 ${bounds.width} ${bounds.height}`);
    all(svg, 'path[data-from]').forEach(path => {
      const from = document.getElementById(path.dataset.from)?.getBoundingClientRect();
      const to = document.getElementById(path.dataset.to)?.getBoundingClientRect();
      if (!from || !to) return;
      const x1 = from.right - bounds.left + 3, y1 = from.top + from.height / 2 - bounds.top;
      const x2 = to.left - bounds.left - 5, y2 = to.top + to.height / 2 - bounds.top;
      const mid = (x1 + x2) / 2;
      path.setAttribute('d', `M${x1},${y1} C${mid},${y1} ${mid},${y2} ${x2},${y2}`);
    });
  }

  all(document, '[data-viz="routes"]').forEach(root => {
    const buttons = all(root, '[data-viz-choice]');
    const choose = value => {
      if (!buttons.some(b => b.dataset.vizChoice === value)) return;
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.vizChoice === value)));
      all(root, '[data-viz-routes]').forEach(n => n.classList.toggle('is-selected', n.dataset.vizRoutes.split(' ').includes(value)));
      all(root, '[data-viz-panel]').forEach(n => { n.hidden = n.dataset.vizPanel !== value; });
      drawEdges(root);
    };
    buttons.forEach(b => b.addEventListener('click', () => choose(b.dataset.vizChoice)));
    // Internal fragments continue to work when they point into a selected detail.
    const followHash = () => {
      let target;
      try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
      if (!target || !root.contains(target)) return;
      const panel = target.closest('[data-viz-panel]');
      const route = target.closest('[data-viz-routes]');
      choose(panel?.dataset.vizPanel || route?.dataset.vizRoutes.split(' ')[0] || root.dataset.default);
    };
    choose(root.dataset.default);
    root.dataset.vizReady = 'true';
    revealControls(root);
    if ('ResizeObserver' in window) new ResizeObserver(() => drawEdges(root)).observe(root);
    window.addEventListener('hashchange', followHash);
    followHash();
  });

  all(document, '[data-viz="dungeons"]').forEach(root => {
    let gate = '700', slot = 'weapon';
    const buttons = all(root, '[data-viz-filter]');
    const panels = all(root, '[data-dungeon-panel]');
    const render = () => {
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.value === (b.dataset.vizFilter === 'gate' ? gate : slot))));
      panels.forEach(panel => { panel.hidden = panel.dataset.gate !== gate || panel.dataset.slot !== slot; });
      all(root, '[data-tier]').forEach(tier => { tier.hidden = tier.dataset.tier !== gate; });
      root.querySelector('[data-viz-status]').textContent = panels.find(p => !p.hidden)?.dataset.result || '';
    };
    const followHash = () => {
      let target;
      try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch { return; }
      if (!target || !root.contains(target)) return;
      const panel = target.closest('[data-dungeon-panel]');
      const tier = target.closest('[data-tier]');
      if (panel) { gate = panel.dataset.gate; slot = panel.dataset.slot; }
      else if (tier) gate = tier.dataset.tier;
      else return;
      render();
      requestAnimationFrame(() => target.scrollIntoView({block:'start', behavior:'instant'}));
    };
    buttons.forEach(b => b.addEventListener('click', () => {
      if (b.dataset.vizFilter === 'gate') gate = b.dataset.value;
      else slot = b.dataset.value;
      render();
    }));
    render();
    revealControls(root);
    window.addEventListener('hashchange', followHash);
    followHash();
  });

  all(document, '[data-viz="wallet"]').forEach(root => {
    const ko = root.dataset.lang === 'ko';
    const t = (en, kr) => ko ? kr : en;
    const format = new Intl.NumberFormat(ko ? 'ko-KR' : 'en-US');
    const num = n => format.format(n);
    const inputs = all(root, '[data-wallet-input]');
    const buttons = all(root, '[data-viz-choice]');
    const result = root.querySelector('[data-wallet-label="result"]');
    const status = root.querySelector('[data-wallet-status]');
    const bar = root.querySelector('.viz-cost-bar');
    let mode = 'all';
    function render() {
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.vizChoice === mode)));
      const valid = inputs.every(n => n.value.trim() !== '' && n.validity.valid && Number.isSafeInteger(n.valueAsNumber));
      root.querySelector('[data-wallet-error]').hidden = valid;
      inputs.forEach(n => n.setAttribute('aria-invalid', String(!n.validity.valid || n.value.trim() === '')));
      if (!valid) {
        all(root, '[data-wallet-value]').forEach(n => { n.textContent = '—'; });
        result.textContent = t('Check the amounts', '입력값 확인');
        status.textContent = t('Enter valid balances and a cost to update the example.', '올바른 잔액과 비용을 입력하면 예시를 계산합니다.');
        bar.hidden = true;
        return;
      }
      bar.hidden = false;
      const values = Object.fromEntries(inputs.map(n => [n.dataset.walletInput, n.valueAsNumber]));
      const {bound, unbound, cost} = values;
      const coveredBound = mode === 'all' ? Math.min(bound, cost) : 0;
      const coveredUnbound = Math.min(unbound, cost - coveredBound);
      const shortfall = cost - coveredBound - coveredUnbound;
      // A shortfall does not model a successful purchase: leave both balances intact.
      const usedBound = shortfall ? 0 : coveredBound;
      const usedUnbound = shortfall ? 0 : coveredUnbound;
      Object.assign(values, {usedBound, usedUnbound, leftBound:bound-usedBound, leftUnbound:unbound-usedUnbound});
      all(root, '[data-wallet-value]').forEach(n => { n.textContent = num(values[n.dataset.walletValue]); });
      const allCost = mode === 'all';
      root.querySelector('.viz-bound').classList.toggle('is-unavailable', !allCost);
      root.querySelector('[data-wallet-label="bound"]').textContent = allCost ? t('Use first for combined costs', '합산 비용에 먼저 사용') : t('Unavailable for Market purchases', '거래소 결제에 사용 불가');
      root.querySelector('[data-wallet-label="unbound"]').textContent = allCost ? t('Covers the remaining combined cost', '합산 비용의 부족분 사용') : t('Pays the Market cost', '거래소 비용 결제');
      result.textContent = shortfall ? t('Not enough for this cost', '비용이 부족해요') : t('Cost covered', '비용 충당 가능');
      status.textContent = shortfall
        ? t(`Short by ${num(shortfall)}. No purchase is modeled; both balances stay unchanged.`, `${num(shortfall)} 부족합니다. 결제가 성립하지 않아 두 잔액을 그대로 표시합니다.`)
        : t(`Example: spend ${num(usedBound)} bound + ${num(usedUnbound)} unbound. ${num(values.leftUnbound)} remains for Market purchases.`, `예시: 귀속 ${num(usedBound)} + 거래 가능 ${num(usedUnbound)} 사용. 거래소에서 쓸 돈은 ${num(values.leftUnbound)} 남습니다.`);
      for (const [key,amount] of Object.entries({bound:coveredBound,unbound:coveredUnbound,shortfall})) root.querySelector(`[data-wallet-bar="${key}"]`).style.width = `${cost ? amount / cost * 100 : 0}%`;
    }
    inputs.forEach(n => n.addEventListener('input', render));
    buttons.forEach(b => b.addEventListener('click', () => { mode = b.dataset.vizChoice; render(); }));
    render();
    revealControls(root);
  });
})();

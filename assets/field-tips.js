(() => {
  'use strict';
  const section = document.querySelector('[data-field-tips]');
  if (!section) return;
  const ko = document.documentElement.lang === 'ko';
  const t = (en, kr) => ko ? kr : en;
  section.querySelectorAll('[data-tip-toggle]').forEach(button => {
    const card = button.closest('[data-field-tip]');
    const original = button.textContent;
    button.addEventListener('click', () => {
      const active = button.getAttribute('aria-pressed') !== 'true';
      button.setAttribute('aria-pressed', String(active));
      card.querySelectorAll('[data-tip-effect]').forEach(effect => { effect.hidden = !active; });
      button.textContent = active ? t('Reset the example', '연습 초기화') : original;
      card.classList.toggle('is-active', active);
    });
  });
  const hp = section.querySelector('[data-tip-hp]');
  const buff = section.querySelector('[data-tip-buff]');
  const result = section.querySelector('[data-tip-hp-result]');
  function update() {
    const threshold = Number(hp.value);
    const potion = 45 < threshold;
    result.textContent = t(
      `Practice: HP 45% is ${potion ? 'below' : 'above'} ${threshold}%. Potion condition ${potion ? 'met' : 'not met'}. Buff scope: ${buff.checked ? 'combat only' : 'not limited to combat'}.`,
      `연습: 생명력 45%는 ${threshold}%보다 ${potion ? '낮아' : '높아'} 물약 조건을 ${potion ? '만족해요' : '만족하지 않아요'}. 버프: ${buff.checked ? '전투 중에만' : '전투 중으로 제한하지 않음'}.`
    );
  }
  hp.addEventListener('change', update);
  buff.addEventListener('change', update);
  update();
})();

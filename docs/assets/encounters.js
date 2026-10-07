(() => {
  'use strict';
  const ko = document.documentElement.lang === 'ko';
  const t = (en, kr) => ko ? kr : en;
  function syncLanguage(url) {
    const link = document.querySelector('.lang');
    if (!link) return;
    const other = new URL(link.href);
    other.search = url.search;
    other.hash = url.hash;
    link.href = other.href;
  }
  const lab = document.querySelector('[data-boss-lab]');
  if (lab) {
    const panels = [...lab.querySelectorAll('[data-boss-panel]')];
    const query = new URLSearchParams(location.search);
    const fixed = lab.dataset.fixedBoss;
    let boss = fixed || (panels.some(p => p.dataset.bossPanel === query.get('boss')) ? query.get('boss') : panels[0].dataset.bossPanel);
    let mechanic = query.get('mechanic');
    let stage = ['0', '1', '2'].includes(query.get('stage')) ? query.get('stage') : '2';
    function render() {
      const current = panels.find(p => p.dataset.bossPanel === boss);
      const choices = [...current.querySelectorAll('[data-mechanic-choice]')];
      if (!choices.some(b => b.dataset.mechanicChoice === mechanic)) mechanic = choices[0].dataset.mechanicChoice;
      panels.forEach(p => { p.hidden = p !== current; });
      lab.querySelectorAll('[data-boss-choice]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.bossChoice === boss)));
      choices.forEach(b => {
        const active = b.dataset.mechanicChoice === mechanic;
        b.setAttribute('aria-selected', String(active));
        b.tabIndex = active ? 0 : -1;
      });
      current.querySelectorAll('[data-mechanic-panel]').forEach(p => {
        p.hidden = p.dataset.mechanicPanel !== mechanic;
        if (!p.hidden) {
          p.querySelector('[data-stage]').dataset.stage = stage;
          p.querySelectorAll('[data-stage-choice]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.stageChoice === stage)));
        }
      });
      lab.querySelectorAll('[data-copy-status]').forEach(s => { s.textContent = ''; });
      const u = new URL(location.href);
      if (!fixed) u.searchParams.set('boss', boss); else u.searchParams.delete('boss');
      u.searchParams.set('mechanic', mechanic);
      u.searchParams.set('stage', stage);
      history.replaceState(null, '', u);
      syncLanguage(u);
    }
    lab.querySelectorAll('[data-boss-choice]').forEach(b => b.addEventListener('click', () => {
      boss = b.dataset.bossChoice; mechanic = ''; stage = '2'; render();
    }));
    panels.forEach(panel => {
      const tabs = [...panel.querySelectorAll('[data-mechanic-choice]')];
      tabs.forEach((b, i) => {
        b.addEventListener('click', () => { mechanic = b.dataset.mechanicChoice; stage = '2'; render(); });
        b.addEventListener('keydown', event => {
          let next;
          if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
          if (event.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
          if (event.key === 'Home') next = 0;
          if (event.key === 'End') next = tabs.length - 1;
          if (next !== undefined) { event.preventDefault(); tabs[next].click(); tabs[next].focus(); }
        });
      });
    });
    lab.querySelectorAll('[data-stage-choice]').forEach(b => b.addEventListener('click', () => { stage = b.dataset.stageChoice; render(); }));
    lab.querySelectorAll('[data-copy-fight]').forEach(b => b.addEventListener('click', async () => {
      const status = b.parentElement.querySelector('[data-copy-status]');
      try {
        await navigator.clipboard.writeText(location.href);
        status.textContent = t('Link copied', '링크를 복사했습니다');
      } catch {
        status.textContent = t('Copy the address bar to share this mechanic.', '주소창의 주소를 복사하면 이 기믹을 공유할 수 있어요.');
      }
    }));
    render();
  }
  const insights = document.querySelector('[data-insights]');
  if (insights) {
    const cards = [...insights.querySelectorAll('[data-note]')];
    const classInput = insights.querySelector('[data-insight-class]');
    const search = insights.querySelector('[data-insight-search]');
    const topics = [...insights.querySelectorAll('[data-insight-topic]')];
    const query = new URLSearchParams(location.search);
    classInput.value = [...classInput.options].some(o => o.value === query.get('class')) ? query.get('class') : 'all';
    let topic = topics.some(b => b.dataset.insightTopic === query.get('topic')) ? query.get('topic') : 'all';
    search.value = query.get('q') || '';
    // A direct search-result anchor always reveals its own card.
    if (cards.some(c => '#' + c.id === location.hash)) { classInput.value = 'all'; topic = 'all'; search.value = ''; }
    function render(changed = false) {
      const term = search.value.trim().toLocaleLowerCase();
      let count = 0;
      cards.forEach(card => {
        const classes = card.dataset.classes.split(' ').filter(Boolean);
        const matchClass = classInput.value === 'all' || (classInput.value === 'general' ? classes.length === 0 : classes.includes(classInput.value));
        const matchTopic = topic === 'all' || (topic === 'pvp' ? card.dataset.activity === 'pvp' : card.dataset.topic === topic);
        card.hidden = !(matchClass && matchTopic && (!term || card.textContent.toLocaleLowerCase().includes(term)));
        if (!card.hidden) count++;
      });
      topics.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.insightTopic === topic)));
      insights.querySelector('[data-insight-count]').textContent = t(`${count} notes`, `${count}개 팁`);
      insights.querySelector('[data-insight-empty]').hidden = count !== 0;
      const u = new URL(location.href);
      for (const [key, value] of [['class', classInput.value], ['topic', topic], ['q', search.value]]) {
        if (value && value !== 'all') u.searchParams.set(key, value); else u.searchParams.delete(key);
      }
      if (changed) u.hash = '';
      history.replaceState(null, '', u);
      syncLanguage(u);
    }
    classInput.addEventListener('change', () => render(true));
    search.addEventListener('input', () => render(true));
    topics.forEach(b => b.addEventListener('click', () => { topic = b.dataset.insightTopic; render(true); }));
    render();
  }
})();

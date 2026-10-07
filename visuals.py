"""Compact, bilingual interactive views. Diagrams are editorial teaching aids."""
import html
import json
from content import CLASSES
from fieldnotes import NOTES
from encounters import note_card, boss_teaser


def esc(value):
    return html.escape(str(value), quote=True)


def glyph(base, name, css='icon'):
    return f'<svg class="{css}" aria-hidden="true" viewBox="0 0 48 48"><use href="{base}assets/icons.svg#{name}"/></svg>'


def explorer(lang, base, selected='gladiator'):
    k = lang == 'ko'
    t = lambda a, b: b if k else a
    root = base + ('ko/' if k else '')
    current = next(c for c in CLASSES if c['id'] == selected)
    name = current['ko' if k else 'en']
    roles = {'damage':t('DAMAGE','공격'), 'tank':t('TANK','탱커'), 'healer':t('HEALER','회복'), 'support':t('SUPPORT','지원')}
    picks = ''.join(f'''<button class="class-pick" data-pick="{c['id']}" aria-pressed="{str(c['id']==selected).lower()}" style="--class-color:{c['color']}">
      <span class="class-emblem">{glyph(base,c['icon'],'class-glyph')}</span><strong>{c['ko' if k else 'en']}</strong><small>{roles[c['role']]}</small></button>''' for c in CLASSES)
    data = json.dumps(CLASSES, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<section class="class-explorer" id="class-explorer" data-explorer data-initial-class="{selected}">
      <div class="section-heading compact"><div><span class="section-kicker">01 / {t('CLASS SELECT','직업 선택')}</span><h2>{t('Pick your playstyle.','어떤 직업으로 시작할까요?')}</h2></div><a class="text-link" href="{root}tools/compare/">{t('Compare classes','직업 비교')} ↗</a></div>
      <div class="class-roster" aria-label="{t('Choose a class','직업 선택')}">{picks}</div>
      <div class="explorer-panel" style="--class-color:{current['color']}">
        <div class="explorer-toolbar"><div class="view-tabs" role="tablist" aria-label="{t('Class information','직업 정보')}">
          <button role="tab" id="view-overview" aria-controls="panel-overview" aria-selected="true" data-view="overview">{glyph(base,'book')}{t('Overview','한눈에 보기')}</button>
          <button role="tab" id="view-practice" aria-controls="panel-practice" aria-selected="false" tabindex="-1" data-view="practice">{glyph(base,'swords')}{t('Combat','전투 흐름')}</button>
          <button role="tab" id="view-gear" aria-controls="panel-gear" aria-selected="false" tabindex="-1" data-view="gear">{glyph(base,'shield')}{t('Gear check','장비 점검')}</button>
        <button role="tab" id="view-community" aria-controls="panel-community" aria-selected="false" tabindex="-1" data-view="community">{glyph(base,'book')}{t('KR tips','KR 실전 팁')}</button></div><div class="mode-switch" aria-label="{t('Activity','콘텐츠')}"><button data-mode="pve" aria-pressed="true">PvE</button><button data-mode="pvp" aria-pressed="false">PvP</button></div></div>
        <div class="explorer-content">
          <div class="class-summary">
            <div class="profile-heading"><span class="profile-glyph" data-profile-glyph>{glyph(base,current['icon'],'class-glyph')}</span><div><span class="section-kicker" data-profile-role>{roles[current['role']]} / {t('MELEE','근접') if current['range']=='melee' else t('RANGED','원거리')}</span><h3 data-profile-name>{name}</h3><p data-profile-identity>{esc(current['identity'][int(k)])}</p></div></div>
            <div role="tabpanel" id="panel-overview" aria-labelledby="view-overview" data-panel="overview"><div class="quick-facts" data-quick-facts></div><p class="class-advice" data-class-advice>{esc(current['fit'][int(k)])}</p></div>
            <div role="tabpanel" id="panel-practice" aria-labelledby="view-practice" data-panel="practice" hidden><span class="micro-label">{t('PRACTICE LOOP','연습 순서')}</span><div class="combat-loop" data-combat-loop></div><p class="class-advice" data-practice-note></p></div>
            <div role="tabpanel" id="panel-gear" aria-labelledby="view-gear" data-panel="gear" hidden><span class="micro-label">{t('BEFORE YOUR NEXT RUN','다음 전투 전에')}</span><div class="gear-checks" data-gear-checks></div><p class="tiny muted">{t('Personal checks for your current client.','현재 클라이언트에서 확인할 개인 점검표.')}</p></div>
            <div role="tabpanel" id="panel-community" aria-labelledby="view-community" data-panel="community" hidden><p class="tiny muted">{t('Korean player suggestions · source-era builds · Global not checked','한국 유저 제안 · 원문 시점 세팅 · 글로벌 미확인')}</p><div data-class-notes>{''.join(note_card(n,lang) for n in NOTES if n['classes'])}</div><p class="class-note-empty" data-class-note-empty hidden>{t('No sourced PvP note for this class yet. Explore its PvE notes or the full collection.','이 직업의 PvP 팁은 아직 정리되지 않았어요. PvE 팁이나 전체 목록을 확인하세요.')}</p><a class="text-link" data-all-class-notes href="{root}insights/?class={selected}">{t('All community notes','커뮤니티 팁 전체 보기')} ↗</a></div>
            <div class="profile-actions"><a class="btn primary" data-profile-link href="{root}classes/{selected}/">{t('Class guide','직업 공략')} →</a><a class="btn" data-profile-compare href="{root}tools/compare/?a={selected}&amp;b=templar">{t('Compare','비교')} {glyph(base,'compare')}</a><button class="bookmark-btn" data-save-class aria-label="{t('Save this class','내 직업으로 저장')}" aria-pressed="false">{glyph(base,'bookmark')}</button></div>
            <p class="tiny status" data-explorer-status role="status"></p>
          </div>
          <div class="combat-visual"><div class="visual-heading"><span class="micro-label">{t('POSITIONING BASICS','전투 위치 이해하기')}</span><span class="tiny" data-map-mode>PvE</span></div>
            <svg class="battle-map" viewBox="0 0 400 255" role="img" aria-label="{t('Illustrative combat positioning','전투 위치 개념도')}">
              <defs><pattern id="battle-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#ffffff" stroke-opacity=".05"/></pattern><radialGradient id="arena-glow"><stop stop-color="#323554" stop-opacity=".6"/><stop offset="1" stop-color="#121620" stop-opacity="0"/></radialGradient></defs>
              <rect width="400" height="255" fill="url(#battle-grid)"/><ellipse cx="200" cy="134" rx="177" ry="119" fill="url(#arena-glow)"/>
              <ellipse cx="200" cy="128" rx="155" ry="98" fill="none" stroke="#465067" stroke-dasharray="4 7"/>
              <path d="M200 110 144 22Q200 4 256 22Z" fill="#ee6879" fill-opacity=".15" stroke="#e66c7a" stroke-opacity=".5"/>
              <text x="200" y="15" text-anchor="middle" fill="#fb92a3" font-size="9" letter-spacing="1.2" data-danger-label>{t('FRONT','정면')}</text>
              <circle cx="200" cy="110" r="26" fill="#34242c" stroke="#e77e8a"/><path d="m188 107 7-6 5 7 5-7 7 6-7 14h-10Z" fill="none" stroke="#f0959e" stroke-width="2"/>
              <text x="200" y="151" text-anchor="middle" fill="#bdacb8" font-size="9" data-enemy-label>{t('ENEMY','적')}</text>
              <path data-player-line d="M220 172Q244 155 229 128" fill="none" stroke="var(--class-color)" stroke-dasharray="4 5" stroke-opacity=".65"/>
              <g data-player-token transform="translate(225 185)"><circle r="25" fill="var(--class-color)" opacity=".12"/><circle r="16" fill="#1a202e" stroke="var(--class-color)" stroke-width="2"/><path d="m0-7 6 12H-6Z" fill="var(--class-color)"/><text y="36" text-anchor="middle" fill="#ffffff" font-size="10" data-player-label>{name}</text></g>
              <g transform="translate(113 192)" data-party-token><circle r="12" fill="#1b3436" stroke="#59bda0"/><path d="M-5 0H5M0-5V5" stroke="#77dab6" stroke-width="2"/><text y="28" text-anchor="middle" fill="#9aa8b8" font-size="9">{t('PARTY','파티')}</text></g>
            </svg><p class="map-tip" data-map-tip></p><span class="map-caption">{t('Role concept · not a boss mechanic or distance scale','역할 개념도 · 특정 보스 패턴·실제 거리 아님')}</span>
          </div>
        </div>
      </div><noscript><p>{t('Open a class profile to read without interactive controls.','자바스크립트 없이 직업별 공략을 읽을 수 있습니다.')}</p><div class="fallback-classes">{''.join(f'<a href="{root}classes/{c["id"]}/">{c["ko" if k else "en"]}</a>' for c in CLASSES)}</div></noscript>
      <script id="explorer-data" type="application/json">{data}</script>
    </section>'''


def dashboard(lang, base):
    k = lang == 'ko'
    t = lambda a, b: b if k else a
    root = base + ('ko/' if k else '')
    tiles = [
      ('swords','classes/',t('Classes','직업 공략'),t('Find your main','내 직업 찾기'),'purple'),
      ('boss','dungeons/',t('Boss mechanics','보스 기믹'),t('Cues, positions, actions','전조·위치·대응'),'red'),
      ('spark','guides/upgrade-decisions/',t('Progression','장비·성장'),t('Before you upgrade','강화 전 확인'),'gold'),
      ('book','insights/',t('KR insights','한국 유저 팁'),t('Community field notes','직업별 실전 팁'),'blue'),
      ('check','tools/planner/',t('My checklist','나의 체크리스트'),t('Keep your next goal','오늘의 목표 저장'),'green'),
      ('book','glossary/',t('KR ↔ EN','한영 용어'),t('Search game terminology','게임 용어 검색'),'teal')]
    tile_html = ''.join(f'<a class="destination {color}" href="{root}{url}"><span class="destination-icon">{glyph(base,ic)}</span><span><strong>{title}</strong><small>{desc}</small></span><span class="destination-arrow">↗</span></a>' for ic,url,title,desc,color in tiles)
    return f'''<div class="wrap hub-home"><section class="game-banner"><div class="game-banner-content"><span class="game-eyebrow">PLAYER’S CODEX / MMORPG</span><h1>AION <span>2</span></h1><p>{t('Choose your class. Plan your next run.','직업을 고르고, 다음 전투를 준비하세요.')}</p><div class="banner-actions"><a class="btn primary" href="#class-explorer">{t('Explore classes','직업 살펴보기')} ↓</a><a class="btn glass" href="{root}guides/first-session/">{t('New player? Start here','처음이라면 여기부터')} →</a></div></div><span class="art-credit">{t('AION 2 artwork © NC','AION 2 아트워크 © NC')}</span></section>
    <nav class="destination-grid" aria-label="{t('Quick navigation','공략 바로가기')}">{tile_html}</nav>
    {explorer(lang,base)}
    {boss_teaser(lang,base)}
    <section class="quick-resources"><div class="section-heading compact"><div><span class="section-kicker">03 / {t('NEXT UP','다음 단계')}</span><h2>{t('A shortcut to your next goal.','다음 목표로 바로 가기.')}</h2></div><a class="text-link" href="{root}guides/">{t('All guides','전체 공략')} ↗</a></div><div class="resource-grid">
    <a class="resource-card" href="{root}guides/first-session/"><div class="mini-route"><span>01</span><i></i><span>02</span><i></i><span>03</span></div><span class="section-kicker">{t('GET STARTED','초보 시작')}</span><h3>{t('Your first session','첫 접속 순서')}</h3><p>{t('Set up → Choose → Play','설정 → 직업 선택 → 플레이')}</p><span class="resource-arrow">↗</span></a>
    <a class="resource-card" href="{root}insights/"><div class="translation-art"><b>한</b><span>⇄</span><b>EN</b></div><span class="section-kicker">{t('KOREA TO GLOBAL','한국에서 글로벌로')}</span><h3>{t('Korean community insights','한국 커뮤니티 인사이트')}</h3><p>{t('Filter by class and activity','직업·콘텐츠별 팁 골라보기')}</p><span class="resource-arrow">↗</span></a>
    <a class="resource-card community-card" href="https://questlog.gg/aion-2/en-nc/skill-builder" target="_blank" rel="noopener"><div class="mini-slots">{''.join(glyph(base,i) for i in ['swords','flame','shield','spark'])}</div><span class="section-kicker">{t('EXTERNAL TOOL · QUESTLOG','외부 도구 · QUESTLOG')}</span><h3>{t('Community skill builds','커뮤니티 스킬 빌드')}</h3><p>{t('Browse builds on Questlog','Questlog에서 빌드 찾아보기')}</p><span class="resource-arrow">↗</span></a>
    </div></section></div>'''


GUIDE_STEPS = {
 'choose-your-class': [('shield','Choose a role','역할 선택'),('swords','Pick two classes','후보 두 직업'),('compare','Try both','같은 조건 비교')],
 'first-session': [('settings','Set up','설정 확인'),('swords','Choose a class','직업 선택'),('check','Set one goal','목표 하나')],
 'first-group-dungeon': [('shield','Prepare','전투 준비'),('boss','Read the fight','패턴 관찰'),('check','Review the run','전투 복기')],
 'upgrade-decisions': [('target','Find the bottleneck','막힌 이유'),('shield','Check the cost','비용 확인'),('check','Decide','투자 결정')],
 'pvp-context': [('target','Choose the mode','전투 규모'),('compare','Match conditions','조건 비교'),('swords','Practise one thing','한 가지 연습')],
 'read-korean-guides': [('book','Match the region','지역 확인'),('settings','Check the patch','패치 확인'),('compare','Compare skill text','스킬 설명 비교')],
}


def guide_visual(lang, base, slug):
    k = lang == 'ko'
    return '<div class="guide-route">'+''.join(f'<div><span class="route-icon">{glyph(base,ic)}</span><small>0{i+1}</small><strong>{ko if k else en}</strong></div>' for i,(ic,en,ko) in enumerate(GUIDE_STEPS[slug]))+'</div>'

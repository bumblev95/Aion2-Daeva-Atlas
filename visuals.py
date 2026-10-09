"""Compact, bilingual interactive views. Diagrams are editorial teaching aids."""
import html
import json
from content import CLASSES
from fieldnotes import NOTES
from encounters import note_card, boss_teaser
from onboarding import journey


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
            <div role="tabpanel" id="panel-community" aria-labelledby="view-community" data-panel="community" hidden><p class="tiny muted">{t('Korean player suggestions · source-era builds · Global not checked','한국 유저 제안 · 원문 시점 세팅 · 글로벌 미확인')}</p><div data-class-notes>{''.join(note_card(n,lang,base) for n in NOTES if n['classes'])}</div><p class="class-note-empty" data-class-note-empty hidden>{t('No sourced PvP note for this class yet. Explore its PvE notes or the full collection.','이 직업의 PvP 팁은 아직 정리되지 않았어요. PvE 팁이나 전체 목록을 확인하세요.')}</p><a class="text-link" data-all-class-notes href="{root}insights/?class={selected}">{t('All community notes','커뮤니티 팁 전체 보기')} ↗</a></div>
            <a class="skill-shortcut" data-profile-skills href="{root}skills/?class={selected}">{t("Skill dictionary · EN ↔ KO", "스킬 문서 · 한국어 ↔ 영어")} ↗</a><div class="profile-actions"><a class="btn primary" data-profile-link href="{root}classes/{selected}/">{t('Class guide','직업 공략')} →</a><a class="btn" data-profile-compare href="{root}tools/compare/?a={selected}&amp;b=templar">{t('Compare','비교')} {glyph(base,'compare')}</a><button class="bookmark-btn" data-save-class aria-label="{t('Save this class','내 직업으로 저장')}" aria-pressed="false">{glyph(base,'bookmark')}</button></div>
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
    from liveops import home_strip
    k=lang=='ko';t=lambda a,b:b if k else a;r=base+('ko/' if k else '')
    topics=[
        ('book','skills/',t('Spend skill points','스킬 포인트 투자'),t('Skills, specializations and class priorities','내 직업 주력기·특화·투자 순서')),
        ('target','maps/',t('Find a growth location','내실 위치 찾기'),t('Sealed Dungeons and nearby travel points','봉인 던전과 가까운 이동 거점')),
        ('check','start/?view=settings#field-tips',t('Useful settings','편의 설정'),t('Useful settings and party shorthand','편의 설정과 파티 모집글 읽는 법')),
    ]
    cards=''.join(f'<a class="topic-card" href="{r}{url}"><span class="topic-icon">{glyph(base,ic)}</span><div><h3>{title}</h3><p>{desc}</p></div><span class="topic-arrow" aria-hidden="true">→</span></a>' for ic,url,title,desc in topics)
    classlinks=''.join(f'<a class="home-class" href="{r}classes/{c["id"]}/" style="--class-color:{c["color"]}">{glyph(base,c["icon"])}<span>{c["ko" if k else "en"]}</span></a>' for c in CLASSES)
    return f'''<div class="wrap hub-home home-clear"><section class="welcome-hero"><div class="welcome-copy"><span class="eyebrow">AION 2 · PLAYER’S CODEX</span><h1>{t('Grow stronger.<br>Clear the next boss.','내실을 채우고,<br>다음 보스를 잡으세요.')}</h1><p>{t('Growth priorities, boss responses and equipment enhancement.<br>Choose the guide for what you want to do now.','내실·성장 순서, 보스 대응, 장비 강화.<br>지금 하려는 일부터 찾아보세요.')}</p></div><span class="art-credit">AION 2 artwork © NC</span></section>
<section class="home-stages rpg-home-goals" aria-label="{t('Your next RPG goal','지금 필요한 공략')}"><a class="home-stage endgame" data-rpg-goal="growth" href="{r}endgame/#after-story"><span class="stage-kicker">01 / {t('GROWTH','내실·성장')}</span><h2>{t('How do I get stronger?','내실은 뭐부터 할까?')} <span aria-hidden="true">→</span></h2><p>{t('Sealed Dungeons, feathers and point investment after the story.','스토리 이후 봉인 던전·깃털·스킬 포인트·데바니온 투자')}</p><span class="stage-detail">{t('Priority → location → reward use','우선순위 → 위치 → 보상 사용처')}</span></a><a class="home-stage" data-rpg-goal="boss" href="{r}endgame/#boss-guides"><span class="stage-kicker">02 / {t('BOSS FIGHTS','보스 공략')}</span><h2>{t('How do I beat this boss?','이 보스는 어떻게 잡지?')} <span aria-hidden="true">→</span></h2><p>{t('Choose the boss and learn its cue, safe position and response.','잡을 보스를 고르고 전조·안전 위치·대응 방법 확인')}</p><span class="stage-detail">{t('Cue → movement → attack window','전조 → 이동·기믹 대응 → 공격 기회')}</span></a><a class="home-stage" data-rpg-goal="enhancement" href="{r}gear/#upgrade"><span class="stage-kicker">03 / {t('ENHANCEMENT','장비 강화')}</span><h2>{t('How do I enhance this item?','이 장비는 어떻게 강화하지?')} <span aria-hidden="true">→</span></h2><p>{t('Find the right material, its sources and the enhancement steps.','장비별 재료·획득처·강화 순서와 투자 범위 확인')}</p><span class="stage-detail">{t('Material → source → enhancement','필요 재료 → 획득처 → 강화 순서')}</span></a></section>
<nav class="home-stage-nav" aria-label="{t('Guides by stage','진행 단계별 공략')}"><a href="{r}start/">{t('Still following the story? Early-game guide','아직 스토리 진행 중이라면 초반 공략')} →</a><a href="{r}endgame/">{t('Full endgame guide','엔드게임 공략 전체')} →</a></nav>
<section class="home-topics" aria-labelledby="topics-heading"><div class="section-heading"><div><h2 id="topics-heading">{t('References for your next upgrade','성장에 필요한 자료')}</h2><p>{t('Skills, locations and settings that support the guides above.','스킬 투자와 목적지 찾기에 필요한 자료입니다.')}</p></div></div><div class="topic-grid">{cards}</div></section>
<section class="home-classes" id="class-explorer" aria-labelledby="home-classes-heading"><div class="section-heading"><h2 id="home-classes-heading">{t('Go straight to my class','내 직업 바로 보기')}</h2><a class="text-link" href="{r}tools/compare/">{t('Compare two classes','두 직업 비교하기')} →</a></div><div class="home-class-list">{classlinks}</div></section>
{home_strip(lang,base)}
<nav class="home-utility" aria-label="{t('More resources','더 찾아보기')}"><a href="{r}insights/"><strong>{t('Player tips','유저 팁')}</strong><span>{t('Practical community notes','한국 커뮤니티의 실전 노하우')} →</span></a><a href="{r}glossary/"><strong>{t('KR ↔ EN glossary','한영 용어집')}</strong><span>{t('Look up an unfamiliar word','낯선 게임 용어 찾아보기')} →</span></a><a href="{r}tools/planner/"><strong>{t('My checklist','나의 체크리스트')}</strong><span>{t('Keep track of today’s goals','오늘 할 일 간단히 정리하기')} →</span></a></nav></div>'''


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

"""Server-rendered boss schematics and community cards, progressively enhanced."""
import html
from fieldnotes import BOSSES, NOTES, KR_SOURCES, REVIEW_DATE
from content import CLASSES

def e(value): return html.escape(str(value), quote=True)
def tr(value, lang): return value[lang == 'ko']
def root_url(base, lang): return base + ('ko/' if lang == 'ko' else '')

def source_details(key, lang):
    s = KR_SOURCES[key]
    t = lambda a, b: b if lang == 'ko' else a
    kind = {'guide':t('Reported guide','공략 기사'), 'player':t('Player suggestion','유저 제안'), 'report':t('Single clear report','단일 플레이 후기')}[s['kind']]
    updated = f' · {t("stated revision", "명시된 수정")} {s["updated"]}' if s.get('updated') else ''
    return f'''<details class="evidence"><summary>{e(s['publisher'])} · {e(s['author'])} · {s['date']} <span>{t('Source & scope','출처·범위')} ↗</span></summary>
      <a href="{e(s['url'])}" target="_blank" rel="noopener noreferrer">{e(s['title'])} ↗</a><p>{kind} · {e(s['scope'])}{updated}</p><p>{t('Read', '본문 확인')} {REVIEW_DATE} · {t('Source date is not a current patch guarantee. Global behaviour not checked.','작성일은 현행 패치 확인일이 아닙니다. 글로벌 적용 미확인.')}</p></details>'''

def diagram(kind, lang, uid, mini=False):
    """Positions and phase drawings are qualitative editorial examples only."""
    t = lambda a, b: b if lang == 'ko' else a
    def text(x,y,s,color='#bdc7d8',size=12):
        return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{color}" font-size="{size}">{e(s)}</text>'
    def dot(x,y,n='1',safe=False):
        return f'<g transform="translate({x} {y})"><circle r="13" fill="{("#15473c" if safe else "#263249")}" stroke="{("#7ce0b8" if safe else "#c7d3ea")}" stroke-width="2"/>{text(0,4,n,"#fff",11)}</g>'
    def boss(x=200,y=95):
        return f'<g transform="translate({x} {y})"><path d="M0-23 23-10 19 16 0 26-19 16-23-10Z" fill="#3b2735" stroke="#ed8492" stroke-width="2"/><path d="m-11-5 6 6m10-6-6 6m-8 10h10" stroke="#f6b8c0" stroke-width="3"/></g>'
    def arrow(d):
        return f'<path d="{d}" fill="none" stroke="#93e8ca" stroke-width="2.5" stroke-dasharray="5 5" marker-end="url(#{uid}-arrow)"/>'
    fixed = ''; before = ''; moving = ''; after = ''
    if kind == 'cover':
        fixed = boss(200,65) + '<circle cx="200" cy="65" r="70" fill="#ec657c" fill-opacity=".08" stroke="#b14d63" stroke-dasharray="4 5"/><path d="m183 131 10-15 19 2 12 22-7 17h-37Z" fill="#665734" stroke="#e9c476" stroke-width="2"/>' + text(265,142,t('ROCK','바위'),'#ecc77e')
        before=dot(318,220); moving=arrow('M310 207Q263 207 208 188'); after=dot(200,188,safe=True)+'<circle cx="200" cy="188" r="23" fill="none" stroke="#f0cf7e" stroke-width="3"/>'+text(200,237,t('CHECK PROTECTION','보호 효과 확인'),'#9fe6cd')
    elif kind == 'out':
        fixed=boss(200,126)+'<circle cx="200" cy="126" r="79" fill="#c84461" fill-opacity=".16" stroke="#ea7b91" stroke-dasharray="5 6"/>'+text(200,26,t('DANGER ZONE','위험 범위'),'#eea0ab')
        before=dot(243,157);moving=arrow('M257 170 322 220');after=dot(340,225,safe=True)+text(328,259,t('OUT','이탈'),'#9fe6cd')
    elif kind == 'stagger':
        fixed=boss(200,110)+'<rect x="110" y="155" width="180" height="13" rx="6" fill="#503046"/><path d="M116 161H263" stroke="#dca2f9" stroke-width="6" stroke-linecap="round"/>'+text(200,192,t('STAGGER BAR OPEN','그로기 게이지 해제'),'#d7b5f3')
        before=dot(125,232)+dot(275,232,'2');moving=arrow('M130 215 182 139')+arrow('M270 215 218 139');after=dot(147,215,safe=True)+dot(254,215,'2',True)+text(200,50,t('USE SAVED SKILLS','아껴둔 스킬 집중'),'#9fe6cd')
    elif kind == 'jump':
        fixed=boss(200,92)+''.join(f'<ellipse cx="200" cy="92" rx="{r}" ry="{r*.55}" fill="none" stroke="#ed8798" opacity="{op}" stroke-width="2"/>' for r,op in [(67,.35),(117,.6),(160,.9)])
        before=dot(200,205);moving=arrow('M172 208Q200 135 228 208');after=dot(200,170,safe=True)+text(200,238,t('JUMP · RECHECK THE NEXT WAVE','점프 · 다음 파동 확인'),'#9fe6cd',11)
    elif kind == 'track':
        fixed='<ellipse cx="200" cy="150" rx="166" ry="80" fill="#497eaa" fill-opacity=".12" stroke="#5d85a9" stroke-dasharray="5 5"/>'+boss(255,128)+text(200,36,t('WATCH THE DIVE HEADING','잠수하는 머리 방향'),'#a0c8eb')
        before=dot(98,220);moving=arrow('M113 216Q180 235 261 198');after=dot(275,200,safe=True)+'<path d="M187 144Q221 127 249 129" fill="none" stroke="#88b7d8" stroke-width="9" opacity=".3"/>'
    elif kind == 'stack':
        fixed=boss(200,60)+'<circle cx="200" cy="193" r="46" fill="#d65b76" fill-opacity=".13" stroke="#ed8f9f" stroke-dasharray="5 4"/>'+text(200,264,t('MARKED PLAYER','징표 대상'),'#f5b1b7')
        before=dot(200,193)+dot(93,210,'2')+dot(310,205,'3')+dot(290,127,'4');moving=arrow('M107 206 176 195')+arrow('M296 201 227 195')+arrow('M281 140 219 171');after=dot(200,177,safe=True)+dot(180,201,'2',True)+dot(219,201,'3',True)+dot(200,221,'4',True)
    elif kind == 'fan':
        fixed=boss(200,90)+'<path d="m200 110-95 123h190Z" fill="#d54a63" fill-opacity=".15" stroke="#d27483" stroke-dasharray="5 5"/>' + ''.join(f'<path d="M200 111 {x} 213" stroke="#dd8b9a" stroke-width="3"/>' for x in (135,180,222,262))
        before=dot(215,198);moving=arrow('M234 202 323 215');after=dot(343,219,safe=True)+text(200,263,t('DODGE · SHOCK REMOVAL IF HIT','회피 · 피격 시 충격 해제'),'#a5e3ce',11)
    elif kind == 'rescue':
        fixed=boss(200,67)+'<circle cx="234" cy="187" r="38" fill="#94b844" fill-opacity=".12" stroke="#b1ca6a" stroke-dasharray="3 5"/><path d="m218 177 31 21m-33-1 32-20m-17-7 4 37" stroke="#b1ca6a" stroke-width="3"/>'+dot(234,187)+text(239,256,t('BREAK VINES','덩굴 공격'),'#d6e695')
        before=dot(93,224,'2');moving=arrow('M109 219 194 194');after=dot(172,205,'2',True)+text(200,126,t('RESCUE','구출'),'#9fe6cd')
    elif kind == 'prison':
        fixed=boss(200,100)+''.join(f'<rect x="{x}" y="{y}" width="29" height="30" rx="6" fill="#343b4b" stroke="#72819a" transform="rotate({a} {x+15} {y+15})"/>' for x,y,a in [(118,123,-25),(133,199,30),(193,214,0),(254,193,-30),(259,128,30)])+'<rect x="177" y="50" width="43" height="28" rx="6" fill="#854051" stroke="#fa98a7" stroke-width="3"/>'
        before=dot(200,187);moving=arrow('M196 170 160 114 193 85');after=dot(200,30,safe=True)+text(84,72,t('BREAK RED','붉은 바위 파괴'),'#f4aab5',11)
    elif kind == 'spread':
        fixed=boss(200,113)
        before=dot(178,193)+dot(210,193,'2')+dot(195,223,'3');moving=arrow('M165 195 77 204')+arrow('M225 196 325 202')+arrow('M196 238 196 263');after=dot(62,206,safe=True)+dot(343,206,'2',True)+dot(197,270,'3',True)+text(200,40,t('SEPARATE CLONE HITS','분신 공격을 따로 받기'),'#9fe6cd')
    elif kind == 'walls':
        fixed=boss(200,45)+''.join(f'<path d="M35 {y}H{gap-33}M{gap+33} {y}H365" stroke="#e87966" stroke-width="14" opacity=".65"/>' for y,gap in [(100,150),(161,250),(223,180)])
        before=dot(180,274);moving=arrow('M180 255V213Q180 180 250 171V149Q250 123 150 117V86');after=dot(151,77,safe=True)+text(330,282,t('GAPS','빈틈'),'#9fe6cd')
    elif kind == 'intercept':
        fixed=boss(63,144)+dot(336,145,'1')+'<path d="M88 145H318" stroke="#e78399" stroke-width="3" stroke-dasharray="8 6"/>'+text(329,178,t('TARGET','대상'),'#f1acb8')
        before=dot(196,249,'2');moving=arrow('M196 231V172');after=dot(196,145,'2',True)+text(196,95,t('UNMARKED BLOCKER','상처 없는 담당자'),'#9fe6cd')
    elif kind == 'circles':
        fixed='<circle cx="107" cy="148" r="77" fill="#df6078" fill-opacity=".12" stroke="#e6889a"/><circle cx="305" cy="148" r="42" fill="#a97ade" fill-opacity=".14" stroke="#bf9ae9"/>'+text(107,42,t('LARGE → SOLO','큰 원 → 혼자'),'#f1acb8')+text(302,42,t('SMALL → SHARE','작은 원 → 함께'),'#cdb2ed')
        before=dot(107,148)+dot(305,148);moving=arrow('M57 236 32 192')+arrow('M367 219 325 177');after=dot(107,148,safe=True)+dot(286,150,'2',True)+dot(319,135,'3',True)+dot(317,164,'4',True)+text(200,268,t('READ THE CIRCLE SIZE','원 크기부터 확인'),'#9fe6cd')
    elif kind == 'orb':
        fixed=boss(66,143)+'<circle cx="206" cy="143" r="32" fill="#6b8ddd" fill-opacity=".22" stroke="#8eb2f5" stroke-width="3"/><path d="M94 143H336" stroke="#dd8294" stroke-width="2" stroke-dasharray="6 5"/>'+text(206,195,t('ENERGY','에너지'),'#a5c3fa')
        before=dot(316,243);moving=arrow('M323 225Q353 200 347 163');after=dot(349,143,safe=True)+text(200,38,t('BOSS → ENERGY → TARGET','보스 → 에너지 → 대상'),'#9fe6cd')
    return f'''<svg class="mechanic-map" viewBox="0 0 400 300" role="img" aria-label="{t('Schematic mechanic positions; not to scale','기믹 위치 개념도, 실제 거리 아님')}"><defs><pattern id="{uid}-grid" width="25" height="25" patternUnits="userSpaceOnUse"><path d="M25 0H0V25" fill="none" stroke="#7181a8" stroke-opacity=".09"/></pattern><marker id="{uid}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="m0 0 10 5-10 5Z" fill="#93e8ca"/></marker></defs><rect width="400" height="300" rx="12" fill="#111924"/><rect width="400" height="300" fill="url(#{uid}-grid)"/>{fixed}<g class="map-before">{before}</g><g class="map-moving">{moving}</g><g class="map-after">{after}</g></svg>'''

def mechanic_panel(boss, m, lang, first):
    t=lambda a,b: b if lang=='ko' else a
    uid=boss['id']+'-'+m['id']
    return f'''<article class="mechanic-panel" id="mechanic-{uid}" data-mechanic-panel="{m['id']}" role="tabpanel" aria-labelledby="pick-{uid}" {'hidden' if not first else ''}>
      <div class="mechanic-split"><div class="mechanic-figure" data-stage="2"><div class="figure-top"><span class="micro-label">{t('POSITION MAP','기믹 위치도')}</span><span class="tiny">{t('SCHEMATIC','개념도')}</span></div>{diagram(m['diagram'],lang,uid)}
      <div class="stage-controls" aria-label="{t('Diagram stage','그림 단계')}">{''.join(f'<button data-stage-choice="{i}" aria-pressed="{str(i==2).lower()}"><small>0{i+1}</small>{label}</button>' for i,label in enumerate([t('Cue','전조'),t('Move','이동'),t('Respond','대응')]))}</div>
      <p class="diagram-caption">{t('Numbered circles = players · schematic positions, not measured geometry or timings.','숫자 원 = 플레이어 · 실제 거리·타이밍이 아닌 위치 설명입니다.')}</p></div>
      <div class="mechanic-brief"><span class="section-kicker">{t('THE QUICK READ','이것만 기억')}</span><h3>{e(tr(m['title'],lang))}</h3><div class="mechanic-line"><span>{t('CUE','전조')}</span><p>{e(tr(m['cue'],lang))}</p></div><div class="mechanic-line action"><span>{t('DO','대응')}</span><p>{e(tr(m['action'],lang))}</p></div><div class="mechanic-mistake"><b>×</b><div><small>{t('COMMON TRAP','놓치기 쉬운 점')}</small><p>{e(tr(m['mistake'],lang))}</p></div></div>{source_details(m['source'],lang)}</div></div></article>'''

def boss_lab(lang, base, selected=None):
    t=lambda a,b:b if lang=='ko' else a
    root=root_url(base,lang)
    active=selected or BOSSES[0]['id']
    visible=BOSSES if not selected else [b for b in BOSSES if b['id']==selected]
    picks=''.join((f'<a class="boss-pick {"selected" if b["id"]==active else ""}" href="{root}dungeons/{b["slug"]}/" aria-current="{"page" if b["id"]==active else "false"}" style="--boss-color:{b["color"]}"><span>0{i+1}</span><strong>{e(tr(b["dungeon"],lang))}</strong><small>{e(tr(b["name"],lang))}</small></a>' if selected else f'<button class="boss-pick" data-boss-choice="{b["id"]}" aria-pressed="{str(b["id"]==active).lower()}" style="--boss-color:{b["color"]}"><span>0{i+1}</span><strong>{e(tr(b["dungeon"],lang))}</strong><small>{e(tr(b["name"],lang))}</small></button>') for i,b in enumerate(BOSSES))
    panels=''
    for b in visible:
        tabs=''.join(f'<button role="tab" data-mechanic-choice="{m["id"]}" id="pick-{b["id"]}-{m["id"]}" aria-controls="mechanic-{b["id"]}-{m["id"]}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}"><span>0{i+1}</span>{e(tr(m["title"],lang))}</button>' for i,m in enumerate(b['mechanics']))
        panels+=f'''<section class="boss-panel" data-boss-panel="{b['id']}" style="--boss-color:{b['color']}" {'hidden' if b['id']!=active else ''}><div class="boss-title"><div><span class="section-kicker">{e(tr(b['dungeon'],lang))}</span><h2>{e(tr(b['name'],lang))}</h2></div><span class="scope-chip">KR · {t('Conquest','정복')}<small>{t('Source-era mechanics','원문 시점 기믹')}</small></span></div><div class="mechanic-tabs" role="tablist" aria-label="{t('Choose a mechanic','기믹 선택')}">{tabs}</div>{''.join(mechanic_panel(b,m,lang,i==0) for i,m in enumerate(b['mechanics']))}<div class="boss-foot"><a href="{root}dungeons/{b['slug']}/">{t('Boss permalink','보스 고정 주소')} ↗</a><button class="text-link" data-copy-fight>{t('Copy selected mechanic','선택한 기믹 링크 복사')} ↗</button><span role="status" data-copy-status></span></div></section>'''
    return f'''<div class="boss-lab" data-boss-lab data-fixed-boss="{selected or ''}"><div class="boss-picker" aria-label="{t('Choose a dungeon','던전 선택')}">{picks}</div><p class="scope-line">{t('KR Conquest source archive · 2025–2026 · Global and other difficulties not verified.','한국판 정복 공략 자료 · 2025–2026 · 글로벌·다른 난이도 적용 미확인.')}</p>{panels}<noscript><p>{t('Open a boss page, then read all mechanics below.','보스별 페이지에서 모든 기믹을 읽을 수 있습니다.')}</p><style>.boss-lab [hidden]{{display:block!important}}.stage-controls,.mechanic-tabs{{display:none}}</style></noscript></div>'''

def note_card(n, lang):
    t=lambda a,b:b if lang=='ko' else a
    topics={'combat':t('Combat','전투'),'gear':t('Gear','성장'),'party':t('Party','파티'),'dungeon':t('Dungeon','던전')}
    names=[tr((c['en'],c['ko']),lang) for c in CLASSES if c['id'] in n['classes']]
    return f'''<article class="insight-card" id="note-{n['id']}" data-note data-classes="{' '.join(n['classes'])}" data-topic="{n['topic']}" data-activity="{n['mode']}"><div class="insight-meta"><span>{e(' / '.join(names) or t('All classes','공통'))}</span><span>{n['mode'].upper()} · {topics[n['topic']]}</span></div><h3>{e(tr(n['title'],lang))}</h3><p>{e(tr(n['body'],lang))}</p>{source_details(n['source'],lang)}</article>'''

def insights(lang, base):
    t=lambda a,b:b if lang=='ko' else a
    options=''.join(f'<option value="{c["id"]}">{c["ko" if lang=="ko" else "en"]}</option>' for c in CLASSES)
    return f'''<section data-insights><div class="insight-controls"><label>{t('Class','직업')}<select data-insight-class><option value="all">{t('All classes','전체 직업')}</option>{options}<option value="general">{t('General / dungeon','공통·던전')}</option></select></label><label>{t('Search tips','팁 검색')}<input data-insight-search type="search" placeholder="{t('Buff, healing, cover…','버프, 회복, 엄폐…')}"></label></div><div class="insight-filters" aria-label="{t('Filter topic','주제 필터')}">{''.join(f'<button class="filter" data-insight-topic="{key}" aria-pressed="{str(key=="all").lower()}">{label}</button>' for key,label in [('all',t('All','전체')),('combat',t('Combat','전투')),('gear',t('Gear','성장')),('party',t('Party','파티')),('dungeon',t('Dungeon','던전')),('pvp','PvP')])}</div><p class="scope-line">{t('Attributed player suggestions and KR guides. Dates and context travel with each card.','유저 제안과 한국판 공략 요약입니다. 카드마다 작성자·날짜·적용 범위를 확인하세요.')}</p><p class="tiny muted" data-insight-count role="status">{len(NOTES)} {t('notes','개 팁')}</p><div class="insight-grid">{''.join(note_card(n,lang) for n in NOTES)}</div><p data-insight-empty hidden>{t('No matching notes. Try another class or clear the filters.','일치하는 팁이 없습니다. 직업을 바꾸거나 필터를 해제해보세요.')}</p></section>'''

def boss_teaser(lang,base):
    t=lambda a,b:b if lang=='ko' else a
    root=root_url(base,lang)
    cards=''.join(f'<a class="boss-teaser-card" style="--boss-color:{b["color"]}" href="{root}dungeons/{b["slug"]}/"><span class="boss-mini" data-stage="2">{diagram(b["mechanics"][0]["diagram"],lang,"teaser-"+b["id"],True)}</span><small>{e(tr(b["dungeon"],lang))}</small><h3>{e(tr(b["name"],lang))} <span>↗</span></h3><p>{e(tr(b["hook"],lang))}</p></a>' for b in BOSSES)
    return f'<section class="boss-teasers"><div class="section-heading compact"><div><span class="section-kicker">02 / BOSS MECHANICS</span><h2>{t("See the mechanic. Know the move.","기믹을 보고, 움직임을 익히세요.")}</h2></div><a class="text-link" href="{root}dungeons/">{t("All bosses","모든 보스")} ↗</a></div><div class="boss-teaser-grid">{cards}</div></section>'

def source_registry(lang):
    t=lambda a,b:b if lang=='ko' else a
    rows=''.join(f'<li><a href="{e(s["url"])}">{e(s["title"])}</a><small>{e(s["publisher"])} · {e(s["author"])} · {s["date"]} · {e(s["scope"])}</small></li>' for s in KR_SOURCES.values())
    return f'<h2>{t("Korean community reading list","한국 커뮤니티 조사 목록")}</h2><p>{t("Short summaries link to their original authors. Player reports are not official balance data. English skill and boss labels are editorial aids; check Korean names against your client.","짧은 요약마다 원 작성자의 글을 연결합니다. 유저 제안은 공식 밸런스 자료가 아닙니다. 영문 스킬·보스 표기는 이해를 돕는 번역이며 한국어 이름과 클라이언트를 대조하세요.")}</p><ul class="source-registry">{rows}</ul>'

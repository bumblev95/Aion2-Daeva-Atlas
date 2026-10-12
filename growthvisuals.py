"""Original visual explanations; all reward routes remain readable without JS.

Dungeon data is supplied by progression.py so selectors and reference tables
cannot disagree. Diagrams explain relationships, not a live character state.
"""
from html import escape as e


GLYPHS = {
    'soul': '<path d="M32 6c-9 12-19 20-19 32a19 19 0 0 0 38 0C51 26 41 18 32 6Z"/><path d="M26 30c-5 6-7 14-1 18m9-21 5 9-7 11"/>',
    'pet': '<path d="m15 26-4-17 17 9m8 0L53 9l-4 17M17 25c7-9 23-9 30 0 14 20 2 31-15 31S3 45 17 25Z"/><path d="m22 34 3 1m14 0 3-1m-14 9 4 3 4-3"/>',
    'crystal': '<path d="m32 5 19 19-8 30H21l-8-30L32 5Zm0 0-9 19 9 30 9-30L32 5ZM13 24h38"/>',
    'stats': '<path d="M11 53h42M18 44V31h7v13m7 0V23h7v21m7 0V12h7v32M12 22 24 11l10 5L49 5"/>',
    'analysis': '<circle cx="28" cy="28" r="19"/><path d="m42 42 13 13M19 27l7 7 12-14"/>',
    'sword': '<path d="m21 40 3-18L51 7l6 6-15 27-18 3m3-4L50 16M14 32l18 18M11 53l10-10M6 52l6 6"/>',
    'armor': '<path d="m23 9-15 8 5 16 8-3-2 24h26l-2-24 8 3 5-16-15-8c-3 9-15 9-18 0Z"/><path d="M24 33h16m-8-11v22"/>',
    'gate': '<path d="M9 56h46M17 56V28a15 15 0 0 1 30 0v28M25 56V29a7 7 0 0 1 14 0v27M12 35h5m30 0h5M25 7l7-4 7 4"/>',
    'feather': '<path d="M13 55 42 20M18 47C-2 23 27 2 53 7c6 26-13 49-35 40Zm9-11 1-17m8 7 1-13M20 44l20-2"/>',
    'monolith': '<path d="m24 8 15-4 7 46H17l7-42ZM11 56h42M28 20h8m-9 8h10m-11 8h12"/>',
    'amulet': '<path d="M14 7c1 20 6 27 18 27S49 27 50 7M27 34l-8 13 13 12 13-12-8-13Z"/><circle cx="32" cy="46" r="4"/>',
    'book': '<path d="M9 12h18l5 5 5-5h18v40H37l-5 5-5-5H9V12Zm23 5v40M15 23h10m-10 9h10m14-9h10m-10 9h10"/>',
    'board': '<path d="m15 13 17 19 17-19M15 51l17-19 17 19"/><circle cx="15" cy="13" r="6"/><circle cx="49" cy="13" r="6"/><circle cx="32" cy="32" r="7"/><circle cx="15" cy="51" r="6"/><circle cx="49" cy="51" r="6"/>',
    'wallet': '<path d="M9 18h42v34H9V18Zm0 0 35-9v9m-2 11h14v13H42V29Z"/><circle cx="48" cy="35" r="1"/>',
    'market': '<path d="M12 27v29h40V27M8 14h48l-4 13H12L8 14Zm5-8h38M26 56V39h13v17"/>',
    'title': '<path d="m18 6 14 19L46 6M18 6h10l4 10 4-10h10"/><circle cx="32" cy="40" r="17"/><path d="m32 30 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1 3-6Z"/>',
    'extract': '<path d="m9 18 23-10 23 10-23 12L9 18Zm0 0v26l23 12 23-12V18M32 30v26M41 7l9 5m-3-6-3 9"/>',
}


def icon(name, css='viz-icon'):
    return f'<svg class="{css}" viewBox="0 0 64 64" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{GLYPHS[name]}</svg>'


class Text:
    def __init__(self, lang, base):
        self.k = lang == 'ko'
        self.r = base + ('ko/' if self.k else '')
    def t(self, en, ko):
        return ko if self.k else en
    def p(self, pair):
        return e(pair[self.k])
    def a(self, route, label, css=''):
        return f'<a class="{css}" href="{self.r+route}">{label} →</a>'


def heading(v, number, title, note):
    return f'<header class="viz-heading"><span class="viz-kicker">VISUAL GUIDE / {number}</span><h3>{v.p(title)}</h3><p>{v.p(note)}</p></header>'


def choices(v, items, label):
    buttons = ''.join(f'<button type="button" data-viz-choice="{key}" aria-pressed="false">{v.p(name)}</button>' for key, name in items)
    return f'<div class="viz-controls" data-viz-controls hidden role="group" aria-label="{v.p(label)}">{buttons}</div>'


def node(v, key, glyph, title, note, routes, css=''):
    return f'<article class="viz-node {css}" id="{key}" data-viz-routes="{routes}">{icon(glyph)}<div><h4>{v.p(title)}</h4><p>{v.p(note)}</p></div></article>'


def edges(id, pairs):
    paths = ''.join(f'<path data-from="{a}" data-to="{b}" data-viz-routes="{routes}" marker-end="url(#{id}-arrow)"/>' for a,b,routes in pairs)
    return f'<svg class="viz-edges" aria-hidden="true"><defs><marker id="{id}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M1 1 9 5 1 9" fill="none" stroke="context-stroke" stroke-width="1.5"/></marker></defs>{paths}</svg>'


def pet(v):
    title = heading(v, '01', ('One soul, two different routes', '모은 영혼, 지금 어디에 쓸까?'),
                    ('Follow the branch that matches this pet’s Insight. Genus analysis is a separate expense.', '해당 펫의 개별 이해도에 따라 경로가 갈립니다. 종족 분석은 별도의 비용이 드는 성장입니다.'))
    controls = choices(v, [('grow', ('Still growing', '개별 이해도를 올리는 중')), ('surplus', ('Insight capped', '개별 이해도 상한 달성'))], ('Pet growth stage', '펫 성장 상태'))
    diagram = (
        node(v,'pet-v-soul','soul',('Collected souls','획득한 영혼'),('Field monsters / Growth Pet Chests','필드 몬스터·성장 펫 상자'),'grow surplus','pet-v-soul')+
        node(v,'pet-v-insight','pet',('Raise individual Insight','개별 이해도 올리기'),('Before the cap · also builds genus progress','상한에 도달하기 전 · 종족 이해도도 누적'),'grow','pet-v-insight')+
        node(v,'pet-v-owned','stats',('Owned bonuses','보유 효과 성장'),('Applies even with another pet equipped','다른 펫을 꺼내도 적용'),'grow','pet-v-owned')+
        node(v,'pet-v-crystal','crystal',('Convert spare souls','남는 영혼을 결정으로'),('After this pet’s cap · matching genus crystals','해당 펫 상한 이후 · 같은 종족의 영혼 결정'),'surplus','pet-v-crystal')+
        node(v,'pet-v-analysis','analysis',('Genus analysis','종족 옵션 분석'),('Crystals + Kinah · slots depend on genus progress','결정 + 키나 · 슬롯은 종족 성장에 따라 개방'),'surplus','pet-v-analysis'))
    lines = edges('pet-v', [('pet-v-soul','pet-v-insight','grow'),('pet-v-insight','pet-v-owned','grow'),('pet-v-soul','pet-v-crystal','surplus'),('pet-v-crystal','pet-v-analysis','surplus')])
    details = (
        f'<div class="viz-insight" data-viz-panel="grow"><strong>{v.t("Next: choose a missing pet", "다음 행동: 미보유 펫부터 선택")}</strong><p>{v.t("Set a collection goal before hunting. Review that pet’s owned effect and the next Insight reward.", "사냥 전에 수집 목표를 정하고 해당 펫의 보유 효과·다음 이해도 보상을 확인하세요.")}</p>{v.a("guides/pet-growth/#pet-farming",v.t("Find its soul source", "펫 영혼 사냥터"))}</div>'+
        f'<div class="viz-insight" data-viz-panel="surplus"><strong>{v.t("Next: set an analysis budget", "다음 행동: 분석 예산부터 설정")}</strong><p>{v.t("Locking options raises costs. A grade-based auto-stop does not guarantee your desired stat.", "옵션을 잠글수록 비용이 늘어납니다. 자동 분석의 등급 정지는 원하는 능력치까지 보장하지 않습니다.")}</p>{v.a("guides/pet-growth/#pet-spending",v.t("Plan crystals and Kinah", "결정·키나 사용 순서"))}</div>')
    return f'<section class="growth-viz" id="pet-visual" data-viz="routes" data-default="grow">{title}{controls}<div class="viz-canvas"><div class="viz-diagram viz-pet">{lines}{diagram}</div></div>{details}<p class="viz-footnote">{v.t("Sources: the pet systems and KR family references below. No simulated stat gains or drop rates.", "아래 펫 시스템·한국 종족 자료를 바탕으로 관계를 그렸습니다. 임의의 능력치 상승량·드롭률을 표시하지 않습니다.")}</p></section>'


def dungeon_picker(v, dungeons, mode='gear'):
    t=v.t
    id = mode+'-visual'
    title=heading(v, '02 / 03', ('Pick a slot. Find the run.', '부위를 고르면, 갈 던전이 보여요'),
                  ('Global Conquest · character level 45. Entry total and reward item level measure different things.', '글로벌 정복 · 캐릭터 45레벨 기준. 입장 종합 수치와 보상 장비의 레벨은 서로 다른 값입니다.'))
    gates=''.join(f'<button type="button" data-viz-filter="gate" data-value="{gate}" aria-pressed="false">{gate:,}</button>' for gate in [700,1400,2100])
    slots=''.join(f'<button type="button" data-viz-filter="slot" data-value="{slot}" aria-pressed="false">{icon(glyph)}{t(en,ko)}</button>' for slot,glyph,en,ko in [('weapon','sword','Weapon / accessory','무기·장신구'),('armor','armor','Armor / guard','방어구·수호패')])
    controls=f'<div class="viz-picker-controls" data-viz-controls hidden><fieldset><legend>{t("1. Target entry total", "1. 목표 입장 종합 수치")}</legend><div>{gates}</div></fieldset><fieldset><legend>{t("2. Missing slot", "2. 필요한 장비 부위")}</legend><div>{slots}</div></fieldset></div>'
    panels=''
    for gate,tier in [(700,54),(1400,70),(2100,86)]:
        pair=''
        for n,d in enumerate([d for d in dungeons if d['gate']==gate]):
            b=d['encounter'];slot='weapon' if n==0 else 'armor';glyph='sword' if n==0 else 'armor'
            panelid=f'{mode}-pick-{b["id"]}'
            pair+=f'''<article class="viz-loot-panel" id="{panelid}" data-dungeon-panel data-gate="{gate}" data-slot="{slot}" data-result="{v.p(b['dungeon'])} · {v.p(d['loot'])}">
<div class="viz-loot-map"><div class="viz-entry"><span>{t('CHARACTER TOTAL','캐릭터 종합 수치')}</span><strong>{gate:,}</strong><small>{t('Lv 45 · entry requirement','45레벨 · 입장 기준')}</small></div><span class="viz-direction" aria-hidden="true">→</span><div class="viz-destination">{icon('gate')}<h4>{v.p(b['dungeon'])}</h4><span>{t('Conquest','정복')}</span></div><span class="viz-direction" aria-hidden="true">→</span><div class="viz-target">{icon(glyph)}<span>{t('REWARD ITEM LEVEL','보상 장비 레벨')}</span><strong>{tier}</strong><small>{v.p(d['goal'])}</small></div></div>
<div class="viz-loot-caption"><div><span class="viz-kicker">{t('POSSIBLE LOOT','목표 드롭 후보')}</span><strong>{v.p(d['loot'])}</strong><p>{t('Drops vary per run. Check available reward claims and energy before entering.','매번 확정 획득은 아닙니다. 입장 전 남은 보상 횟수와 에너지를 확인하세요.')}</p></div><div class="viz-links">{v.a('guides/dungeon-rewards/#dungeon-'+b['slug'],t('Rewards & use','보상·사용처'))}{v.a('dungeons/'+b['slug']+'/',t('Animated boss guide','움직이는 보스 공략'))}</div></div></article>'''
        anchor=f'gear-tier-{tier}' if mode=='gear' else f'dungeon-tier-{tier}'
        panels+=f'<div id="{anchor}" class="viz-tier" data-tier="{gate}">{pair}</div>'
    return f'<section class="growth-viz" id="{id}" data-viz="dungeons">{title}{controls}<p class="viz-status sr-only" role="status" aria-live="polite" data-viz-status></p>{panels}<p class="viz-footnote">{t("Global reward snapshot · reviewed 2026-10-12. Boss diagrams use the separately credited KR guides.", "글로벌 보상 자료 · 2026.10.12 검토. 보스 그림은 별도로 표시한 한국 공략을 참고합니다.")}</p></section>'


def wallet(v):
    t=v.t
    title=heading(v, '04', ('Two balances. Different buying power.', '같은 키나라도, 쓸 수 있는 곳이 달라요'),
                  ('Change the example balances and cost to see which funds would be used. This does not read your account.', '예시 잔액과 비용을 바꾸면 어떤 돈이 쓰이는지 보여줍니다. 실제 캐릭터 정보를 가져오지는 않습니다.'))
    controls=choices(v,[('all',('Enhancement · Kina (All)','강화 · 합산 비용')),('market',('Market purchase','거래소 구매'))],('Purchase type','비용 종류'))
    fields=''.join(f'<label for="wallet-{key}"><span>{t(en,ko)}</span><input id="wallet-{key}" data-wallet-input="{key}" type="number" min="0" max="1000000000000" step="1" value="{value}" inputmode="numeric" required></label>' for key,en,ko,value in [('bound','Bound balance','귀속 잔액',550000),('unbound','Unbound balance','거래 가능 잔액',200000),('cost','Cost to pay','결제할 비용',600000)])
    status=t('Example: spend 550,000 bound + 50,000 unbound. 150,000 remains for Market purchases.', '예시: 귀속 550,000 + 거래 가능 50,000 사용. 거래소에서 쓸 돈은 150,000 남습니다.')
    return f'''<section class="growth-viz" id="kinah-visual" data-viz="wallet" data-lang="{'ko' if v.k else 'en'}">{title}{controls}<div class="viz-wallet-inputs" data-viz-controls hidden>{fields}</div><p class="viz-input-error" data-wallet-error hidden>{t('Enter whole numbers from 0 to 1,000,000,000,000 in all three fields.', '세 칸에 0~1,000,000,000,000 사이의 정수를 입력하세요.')}</p><div class="viz-wallet-map">
<article class="viz-purse viz-bound">{icon('wallet')}<h4>{t('Bound Kinah','귀속 키나')}</h4><p>{t('Duties · Daily Dungeon rewards','사명·일일 던전 보상')}</p><strong data-wallet-value="bound">550,000</strong><span data-wallet-label="bound">{t('Use first for combined costs','합산 비용에 먼저 사용')}</span><dl><div><dt>{t('Used','사용')}</dt><dd data-wallet-value="usedBound">550,000</dd></div><div><dt>{t('Left','남음')}</dt><dd data-wallet-value="leftBound">0</dd></div></dl></article>
<article class="viz-purse viz-unbound">{icon('market')}<h4>{t('Unbound Kinah','거래 가능 키나')}</h4><p>{t('Completed sales of tradable items','거래 가능한 아이템의 판매 수입')}</p><strong data-wallet-value="unbound">200,000</strong><span data-wallet-label="unbound">{t('Covers the remaining combined cost','합산 비용의 부족분 사용')}</span><dl><div><dt>{t('Used','사용')}</dt><dd data-wallet-value="usedUnbound">50,000</dd></div><div><dt>{t('Left for the Market','거래소 사용 가능')}</dt><dd data-wallet-value="leftUnbound">150,000</dd></div></dl></article>
<div class="viz-wallet-result"><span aria-hidden="true">↓</span><strong data-wallet-label="result">{t('Cost covered','비용 충당 가능')}</strong><div class="viz-cost-bar" aria-hidden="true"><i data-wallet-bar="bound" style="width:91.6667%"></i><i data-wallet-bar="unbound" style="width:8.3333%"></i><i data-wallet-bar="shortfall" style="width:0%"></i></div><p data-wallet-status role="status" aria-live="polite">{status}</p><small>{t('Mint = bound used · gold = unbound used · stripes = shortfall', '민트 = 귀속 사용 · 금색 = 거래 가능 사용 · 빗금 = 부족분')}</small></div></div><p class="viz-footnote">{t('Illustration before any additional fees. “Kina (All)” uses bound first; Market purchases cannot use bound Kinah.', '추가 수수료를 제외한 사용 예시입니다. Kina (All)은 귀속분을 먼저 쓰며 거래소 구매에는 귀속 키나를 쓸 수 없습니다.')}</p></section>'''


def overview(lang, base):
    v=Text(lang,base);t=v.t
    title=heading(v, 'START', ('A reward is only the beginning.', '받은 보상, 이렇게 능력치가 됩니다'),
                  ('Choose a reward and trace it to the upgrade it funds.', '보상을 선택하면 실제 성장으로 바꾸는 경로가 이어집니다.'))
    rows=[
        ('feathers','feather',('Feathers','깃털 · 주신의 흔적'),('Collect in the field','필드에서 수집'),'monolith',('Monolith resonance','모노리스 공명'),('Turn in traces and claim scrolls','흔적 반납·주문서 수령'),'amulet',('Revelation Amulet','계시의 아뮬렛'),('Matching scrolls → enhance','전용 주문서로 강화'),'endgame/#after-story-feathers',('See collection route','수집 경로 보기')),
        ('wisdom','crystal',('Wisdom Stones','지혜의 돌'),('Check the activity’s reward list','콘텐츠 보상 목록 확인'),'book',('Use the item','가방에서 사용'),('Gain skill points','스킬 포인트 획득'),'stats',('Skill investment','스킬 성장'),('Spend on useful skills','주력 스킬에 포인트 투자'),'skills/',('Choose skill priorities','스킬 투자 순서')),
        ('daevanion','crystal',('Daevanion Crystals','데바니온 결정'),('Check the activity’s reward list','콘텐츠 보상 목록 확인'),'board',('Use the item','가방에서 사용'),('Gain Daevanion points','데바니온 포인트 획득'),'stats',('Board nodes','데바니온 노드'),('Invest in useful nodes','필요한 능력치·스킬 노드 투자'),'endgame/#after-story-spend-points',('Review points and boards','포인트 사용 안내')),
    ]
    controls=choices(v,[(row[0],row[2]) for row in rows],('Reward to trace','사용처를 볼 보상'))
    nodes='';lines=[];details=''
    for key,a,at,an,b,bt,bn,c,ct,cn,url,label in rows:
        for n,glyph,name,note in [(1,a,at,an),(2,b,bt,bn),(3,c,ct,cn)]:
            nodes+=node(v,f'growth-v-{key}-{n}',glyph,name,note,key,f'viz-map-{key} viz-map-col-{n}')
        lines.extend([(f'growth-v-{key}-1',f'growth-v-{key}-2',key),(f'growth-v-{key}-2',f'growth-v-{key}-3',key)])
        details+=f'<div class="viz-insight" data-viz-panel="{key}">{v.a(url,v.p(label))}</div>'
    scope=t('Global guide note: feathers no longer grant skill points. The older KR feather guide is linked for locations.', '글로벌 공략 기준: 깃털은 현재 스킬 포인트를 주지 않습니다. 예전 한국 깃털 글은 위치 참고용으로 연결합니다.')
    return f'<section class="growth-viz" id="growth-visual" data-viz="routes" data-default="feathers">{title}{controls}<div class="viz-canvas"><div class="viz-diagram viz-reward-map">{edges("growth-v",lines)}{nodes}</div></div>{details}<p class="viz-footnote">{scope} <a href="https://mobalytics.gg/gamebase/guides/aion-2-beginner-guide" target="_blank" rel="noopener noreferrer">Mobalytics · 2026.10.11 ↗</a> · <a href="#growth-sources">{t("Item sources", "아이템 근거")}</a></p></section>'


def small_wins(v):
    rows=[
        ('title',('Titles & achievements','칭호·업적'),('Claim completed rewards and check available title bonuses.', '완료 보상을 수령하고 열린 칭호의 보너스를 확인하세요.')),
        ('crystal',('Power Shards','Power Shard · 공격 소모품'),('Stronger shards use Enhance Stones too. Reserve your equipment budget first.', '상위 샤드 변환에도 강화석이 듭니다. 장비 강화 예산부터 남기세요.')),
        ('extract',('Unwanted equipment','남는 장비 추출'),('Extraction recovers resources and unlocks appearances. Check crafting and voucher needs first.', '추출하면 재료와 외형을 회수합니다. 제작·교환에 쓸 장비인지 먼저 확인하세요.')),
    ]
    return '<div class="viz-small-wins">'+''.join(f'<article>{icon(glyph)}<div><h3>{v.p(title)}</h3><p>{v.p(note)}</p></div></article>' for glyph,title,note in rows)+'</div>'

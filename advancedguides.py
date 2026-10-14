"""Dated practical guides: original diagrams, with regional evidence kept explicit."""
from html import escape as e
import json

REVIEWED = '2026-10-13'
GUIDES = [
    dict(slug='gear-options', group='gear', region='GLOBAL', title=('Gear options & transfers', '장비 옵션·영혼 부여·계승'), description=('Choose between Sync, Bind, Reset and a transfer.', '옵션 변경·수치 상승·전체 재설정·계승을 상황에 맞게 선택합니다.')),
    dict(slug='shugo-festival', group='routines', region='GLOBAL', title=('Shugo Festival: play, keys & purchases', '페스타 종목·열쇠·상점 공략'), description=('Choose an activity, a reward claim and your next purchase.', '종목을 고르고, 보상 열쇠를 쓰고, 성장 재료로 교환하는 순서.')),
    dict(slug='stigma-growth', group='gear', region='GLOBAL / KR', title=('Stigma Shards: sources & spending', '스티그마 샤드 획득·투자'), description=('Separate Global purchases from dated KR stock and level costs.', '글로벌 구매 참고와 한국 상점 한도·레벨별 소모량을 구분합니다.')),
    dict(slug='endgame-crafts', group='gear', region='GLOBAL', title=('Endgame crafting goals', '팔찌·아르카나 제작 목표'), description=('Match one useful craft to its materials and reward routes.', '필요한 완성품 하나를 정하고 재료·보상 획득처를 연결합니다.')),
    dict(slug='kr-pendant', group='gear', region='KR', title=('KR Draconic Pendant enhancement', '한국 펜던트 강화·실패 보정'), description=('Read the next attempt and understand increasing failure compensation.', '유일 펜던트의 다음 시도 확률과 실패 보정을 이해합니다.')),
    dict(slug='kr-bitan', group='boss', region='KR', title=('KR Snowfield of Grief: raid movement', '한국 비탄의 설원·파티 이동 공략'), description=('Orb assignments, below-50% movement and the October 14 change.', '구슬 역할 분담·체력 50% 이하 이동·10월 14일 변경 사항.')),
]
SOURCES = {
    'gear': ('https://mobalytics.gg/gamebase/guides/aion-2-endgame-gear', 'Mobalytics · Ulfhednar / Oli · 2026-10-12', 'Global play guide'),
    'festival': ('https://mobalytics.gg/gamebase/guides/aion-2-shugo-festival', 'Mobalytics · Ulvier · 2026-10-13', 'Global play guide'),
    'arcana': ('https://metabot.gg/en/aion-2/arcana', 'MetaBot · Global Arcana client table', 'Global client reference'),
    'arcana-guide': ('https://metabot.gg/en/aion-2/guides/arcana-guide', 'MetaBot · Arcana crafting reference', 'Global client reference'),
    'shards': ('https://www.inven.co.kr/board/aion2/6444/2337', 'Inven · 퓨리허브 · 2026-10-07', 'KR community shop snapshot'),
    'pendant-old': ('https://www.inven.co.kr/board/aion2/6444/2037', 'Inven · Roah · 2026-07-03', 'KR community enhancement table'),
    'pendant-new': ('https://www.inven.co.kr/board/aion2/6444/2344', 'Inven · 다주패뿌 · 2026-10-13', 'KR community enhancement chart'),
    'orbs': ('https://www.inven.co.kr/board/aion2/6444/2340', 'Inven · 모뮤 · 2026-10-09', 'KR proposed raid strategy'),
    'movement': ('https://www.inven.co.kr/board/aion2/6444/2338', 'Inven · 깔개수호 · 2026-10-08', 'KR raid strategy'),
    'patch': ('https://aion2.plaync.com/ko-kr/board/update/view?articleId=6ace86b86cfe4756db5b8d81', 'NC · KR · 2026-10-14 (07:02 revision)', 'Official regional patch'),
}
# Base probability and compensation agree across both KR tables. Costs do not.
PENDANT_CHANCES = [75, 50, 33, 33, 25, 25, 25, 20, 20, 20, 15, 10, 10, 8, 6, 5, 4, 3, 2, 1]
PENDANT_BONUS = [5]*5 + [4]*5 + [3]*5 + [2]*5
STIGMA_COST = {0: 0, 5: 5, 10: 15, 15: 35, 20: 75}
FESTIVAL_GAMES = [
    ('Jump Jump', ('Dodge lasers; collect balloons.', '레이저를 피하며 풍선 수집'), '2:55', 'spark'),
    ('Mysterious Track', ('Race your mount; collect boosts.', '탑승물 경주·가속 아이템 수집'), '5:00', 'target'),
    ('Odyle Flight Frenzy', ('Collect drops; use flight rings.', '비행하며 오드 수집·가속 고리 통과'), '3:30', 'spark'),
    ('Defend Shugo Merchants', ('Defend merchants against waves.', '웨이브를 막고 상인 보호'), '5:00', 'shield'),
    ('Not This Tile?', ('Remember the safe tile pattern.', '보여준 타일 경로 기억'), '3:15', 'grid'),
    ('Wraith Evasion', ('Collect drops without being caught.', '망령을 피해 오드 수집'), '5:00', 'boss'),
    ('Hidden Lugi', ('Hide as Lugi; find Lugi as Shugo.', '루기는 숨고, 슈고는 찾기'), '3:30', 'search'),
    ('Goldrin’s Treasure', ('Follow light beams to treasure.', '빛기둥을 따라 보물 찾기'), '3:50', 'book'),
    ('Up! Up! Up!', ('Climb moving platforms to checkpoints.', '움직이는 발판을 올라 체크포인트 도달'), '5:00', 'spark'),
]


class View:
    def __init__(self, lang, base):
        self.k = lang == 'ko'
        self.lang, self.base = lang, base
        self.root = base + ('ko/' if self.k else '')
    def t(self, en, ko): return ko if self.k else en
    def p(self, pair): return pair[self.k]
    def link(self, slug, label): return f'<a href="{self.root}{slug}">{e(label)} →</a>'
    def icon(self, name):
        return f'<svg class="ag-icon" aria-hidden="true" viewBox="0 0 48 48"><use href="{self.base}assets/icons.svg#{name}"/></svg>'
    def section(self, id, title, body, intro=''):
        return f'<section class="ag-section" id="{id}"><header><h2>{e(self.p(title))}</h2>{("<p>"+e(intro)+"</p>") if intro else ""}</header>{body}</section>'
    def cards(self, rows):
        return '<div class="ag-cards">'+''.join(f'<article>{self.icon(glyph)}<h3>{e(self.p(title))}</h3><p>{e(self.p(text))}</p></article>' for glyph,title,text in rows)+'</div>'
    def sources(self, keys):
        return '<details class="ag-sources" id="ag-sources"><summary>'+self.t('Sources & scope','출처·적용 범위')+'</summary><ul>'+''.join(f'<li><a href="{e(SOURCES[key][0])}" target="_blank" rel="noopener noreferrer">{e(SOURCES[key][1])} ↗</a><small>{e(SOURCES[key][2])}</small></li>' for key in keys)+'</ul></details>'
    def steps(self, rows):
        return '<ol class="ag-steps">'+''.join(f'<li><strong>{e(self.p(title))}</strong><span>{e(self.p(text))}</span></li>' for title,text in rows)+'</ol>'


def gateway(lang, base, group):
    v=View(lang,base)
    slugs={'gear':['gear-options','stigma-growth','endgame-crafts'], 'endgame':['stigma-growth','endgame-crafts'], 'routines':['shugo-festival','stigma-growth'], 'boss':['kr-bitan'], 'gear-targets':['gear-options','endgame-crafts','kr-pendant'], 'dungeon-rewards':['endgame-crafts','kr-bitan']}
    entries=[g for slug in slugs.get(group,[]) for g in GUIDES if g['slug']==slug]
    if not entries:return ''
    return '<nav class="ag-related" aria-label="'+v.t('More practical guides','다음 성장 상세 공략')+'">'+''.join(f'<a href="{v.root}guides/{g["slug"]}/" data-practical-guide="{g["slug"]}"><small>{g["region"]}</small><strong>{e(v.p(g["title"]))}</strong><span aria-hidden="true">→</span></a>' for g in entries)+'</nav>'


def gear(v):
    # These are illustrative option labels, not numerical game rolls.
    controls=''.join(f'<button type="button" data-option-mode="{key}" aria-pressed="{str(key=="sync").lower()}">{label}</button>' for key,label in [('sync',v.t('Sync · one line','Sync · 옵션 하나')),('bind',v.t('Bind · values','Bind · 수치')),('reset',v.t('Reset · all lines','Reset · 전체'))])
    labels=[('Keep a useful bonus','남길 옵션'),('Keep another useful bonus','남길 옵션'),('Change this unwanted bonus','바꿀 옵션')]
    before=''.join(f'<li>{e(v.p(label))}</li>' for label in labels)
    panels=''
    for key,title,desc in [
        ('sync',('One unwanted line','불필요한 옵션 하나'),('Only the selected line is rerolled. Check eligible material gear first.', '선택한 옵션을 다시 뽑습니다. 재료로 쓸 장비 조건부터 확인하세요.')),
        ('bind',('Good lines, low values','좋은 옵션·낮은 수치'),('Raise the binding rate after settling the lines.', '옵션 종류를 정한 뒤 영혼 부여율을 올립니다.')),
        ('reset',('Wrong combination','옵션 조합 전체가 아쉬울 때'),('Reset rerolls every line and uses rare books.', '전체 옵션을 다시 뽑으며 희귀 초기화 재료를 씁니다.')),
    ]:
        panels+=f'<article data-option-panel="{key}"><h3>{e(v.p(title))}</h3><div class="ag-option-flow"><div class="ag-item"><span>{v.t("Before · illustration","변경 전 · 개념 예시")}</span><ul>{before}</ul></div><b aria-hidden="true">→</b><div class="ag-item ag-item-result ag-mode-{key}"><span>{v.t("What changes","바뀌는 부분")}</span><ul><li>{v.t("Same line" if key!="reset" else "New roll","기존 옵션" if key!="reset" else "새 조합")}{(" ↑" if key=="bind" else "")}</li><li>{v.t("Same line" if key!="reset" else "New roll","기존 옵션" if key!="reset" else "새 조합")}{(" ↑" if key=="bind" else "")}</li><li class="ag-changed">{v.t("New roll" if key!="bind" else "Same line ↑","새 옵션 추첨" if key!="bind" else "기존 옵션 ↑")}</li></ul></div></div><p>{e(v.p(desc))}</p></article>'
    diagram=f'<div class="ag-option-demo" data-option-demo><div class="ag-controls" data-ag-controls hidden>{controls}</div>{panels}</div>'
    transfer=v.steps([
        (('Choose the receiving item','계속 쓸 장비 선택'),('Compare the useful lines on the receiving and source items.', '받을 장비와 재료 장비의 유용한 옵션을 비교합니다.')),
        (('Read the preview','계승 미리보기 확인'),('Review resulting lines, eligible source and required materials.', '바뀔 옵션·재료 장비 조건·필요 수량을 함께 봅니다.')),
        (('Prepare the recipe','물질 변환 재료 준비'),('Use the recipe and quantity shown for your region.', '현재 서버의 계승 재료 레시피와 필요 수량을 따릅니다.')),
    ])
    patch='<div class="ag-note"><strong>'+v.t('KR · October 14 material change','한국 · 10월 14일 재료 변경')+'</strong><p>'+v.t('KR merges slot-specific Transfer Stones into Unique/Heroic Transfer Flames. Old stones and fragments have conversion recipes. This change is not asserted for Global.', '한국은 부위별 계승석을 유일·영웅 계승의 불꽃으로 통합합니다. 기존 계승석·조각은 물질 변환으로 바꿉니다. 글로벌 적용 여부는 별도로 확인합니다.')+'</p></div>'
    decisions=v.cards([
        ('shield',('Before extracting a drop','드랍 장비를 추출하기 전'),('Compare its rolls with your kept gear. A spare can be a useful source.', '계속 쓸 장비와 옵션을 비교하세요. 여분 장비도 계승 재료 후보가 됩니다.')),
        ('check',('Set a stopping point','투자 한도 정하기'),('Our advice: decide which improvement matters and what you can spend before opening the reroll menu.', '우리의 투자 기준: 필요한 변화와 쓸 재료 한도를 먼저 정하고 옵션 변경을 시작하세요.')),
    ])
    return [(('options',('Choose a menu','메뉴 선택')),v.section('option-choice',('Which menu changes what?','어떤 메뉴를 써야 할까?'),diagram)),
            (('transfer',('Transfer','계승 순서')),v.section('transfer-route',('Preview, then transfer','바뀔 옵션을 확인한 뒤 계승'),transfer+patch)),
            (('budget',('Keep or spend','남길 장비·투자')),v.section('option-budget',('Decide before spending','재료를 쓰기 전에 결정하기'),decisions+v.link('guides/gear-targets/',v.t('Choose your target item','목표 장비 고르기'))))],['gear','patch']


def festival(v):
    games='<div class="ag-game-grid">'+''.join(f'<article>{v.icon(icon)}<h3>{e(name)}</h3><p>{e(v.p(goal))}</p><small>{time} · {v.t("reported play window","공략의 플레이 제한 시간")}</small></article>' for name,goal,time,icon in FESTIVAL_GAMES)+'</div>'
    play=v.steps([
        (('Unlock the Festival','페스타 열기'),('Lv 10 + Visions in Smoke (Elyos) / Urgent Pursuit (Asmodian).', '10레벨·천족 Visions in Smoke / 마족 Urgent Pursuit 퀘스트 이후 해금.')),
        (('Watch the event menu','열리는 종목 확인'),('The Global guide reports hourly openings and a 3-minute entry window; follow the client countdown.', '글로벌 공략은 정각·3분 입장을 설명합니다. 현재 게임의 남은 시간을 기준으로 참여하세요.')),
    ])
    rewards=v.cards([
        ('check',('Placement → picks','순위 → 보상 선택 수'),('Better placement offers more picks; claims spend keys.', '높은 순위일수록 선택 수가 늘며, 보상 수령에 열쇠를 씁니다.')),
        ('book',('Practice → decide','연습 → 수령 판단'),('You can participate without a key. Declining the cube pick preserves keys.', '열쇠 없이도 참여할 수 있고, 큐브 선택을 포기하면 열쇠를 보존합니다.')),
        ('spark',('Shared key cap','서버 공유 열쇠 상한'),('Reported cap: 12, or 21 with membership. Refill stops at the cap.', '공략 기준 상한은 기본 12·멤버십 21개입니다. 상한에서는 충전이 멈춥니다.')),
    ])
    shop=v.steps([
        (('Choose a growth goal','교환 목표 하나 정하기'),('Our advice: pick skills, board growth or a collection goal before spending tokens.', '우리의 선택 기준: 스킬·데바니온·수집 중 필요한 성장부터 정하세요.')),
        (('Read the limit','구매 제한 읽기'),('Monthly stock resets; lifetime stock does not.', '월간 한도와 초기화되지 않는 누적 한도를 구분합니다.')),
        (('Start with a named purchase','필요한 품목부터 구매'),('Global guide: 35 Stigma Shards total 10,500 tokens. Compare the current listing.', '글로벌 공략의 샤드 35개 비용은 토큰 10,500개입니다. 현재 상점 표기도 비교하세요.')),
    ])
    return [(('play',('Games','종목 고르기')),v.section('festival-games',('Find a game you can finish','내가 완주할 종목 고르기'),play+games)),
            (('keys',('Reward keys','열쇠·보상')),v.section('festival-keys',('Decide when to claim','언제 보상을 받을까?'),rewards)),
            (('shop',('Shop','상점 사용')),v.section('festival-shop',('Turn tokens into growth','모은 토큰을 성장에 쓰기'),shop+v.link('guides/stigma-growth/',v.t('Stigma purchase guide','스티그마 구매 공략'))))],['festival']


def stigma(v):
    global_card=v.cards([
        ('spark',('Global Festival purchase','글로벌 페스타 구매 참고'),('The Oct 13 guide lists 35 lifetime Stigma Shards for 10,500 tokens.', '10월 13일 글로벌 공략은 샤드 35개·토큰 10,500개 누적 한도를 설명합니다.')),
        ('check',('Read the item and reset','품목·초기화 확인'),('Check full Shards versus fragments, character/server scope and the next refresh.', '완성 샤드와 조각, 캐릭터·서버 한도, 초기화 여부를 확인하세요.')),
    ])
    stock=[
        (('Shugo Festival','슈고 페스타'), '300', '35', '10,500', ('Festival currency','페스타 재화')),
        (('Nightmare','악몽'), '1,500', '35', '52,500', ('Nightmare currency','악몽 재화')),
        (('Abyss tier 1','어비스 1단계'), '10,000', '50', '500,000', ('AP','어비스 포인트')),
        (('Abyss tier 2','어비스 2단계'), '15,000', '50', '750,000', ('AP','어비스 포인트')),
        (('Abyss tier 3','어비스 3단계'), '20,000', '50', '1,000,000', ('AP','어비스 포인트')),
    ]
    table='<div class="ag-table"><table><thead><tr>'+''.join(f'<th>{label}</th>' for label in [v.t('KR listing','한국 상점'),v.t('Each','개당 비용'),v.t('Stock','누적 한도'),v.t('Full stock cost','한도까지 비용')])+'</tr></thead><tbody>'+''.join(f'<tr><th>{e(v.p(name))}</th><td data-label="{v.t("Each","개당 비용")}">{price} {e(v.p(unit))}</td><td data-label="{v.t("Stock","누적 한도")}">{limit}</td><td data-label="{v.t("Full stock cost","한도까지 비용")}">{total} {e(v.p(unit))}</td></tr>' for name,price,limit,total,unit in stock)+'</tbody></table></div>'
    note='<p class="ag-note">'+v.t('KR Oct 7 snapshot: these character limits do not reset weekly. Currency amounts are game currency, not cash prices. Abyss tiers are separate from the old 25,000-AP listing.', '한국 10월 7일 자료: 위 캐릭터별 한도는 주간 초기화되지 않습니다. 비용은 게임 재화이며 현금 가격이 아닙니다. 어비스 단계별 상품과 기존 25,000포인트 상품도 구분하세요.')+'</p>'
    milestones='<div class="ag-milestones">'+''.join(f'<div><strong>0 → {level}</strong><span>{cost} {v.t("Shards","샤드")}</span></div>' for level,cost in STIGMA_COST.items() if level)+'</div>'
    select=lambda name,values,selected:'<select data-stigma-'+name+'>'+''.join(f'<option value="{n}"'+(' selected' if n==selected else '')+f'>{n}</option>' for n in values)+'</select>'
    calc=f'<div class="ag-calculator" data-stigma-planner data-costs="{e(json.dumps(STIGMA_COST))}" data-lang="{v.lang}"><div class="ag-controls" data-ag-controls hidden><label>{v.t("Current level","현재 레벨")}{select("from",STIGMA_COST,0)}</label><label>{v.t("Target level","목표 레벨")}{select("to",list(STIGMA_COST)[1:],15)}</label></div><p class="ag-calc-result" data-stigma-result aria-live="polite">{v.t("0 → 15 needs 35 Shards.","0 → 15레벨에 샤드 35개가 필요합니다.")}</p><p class="ag-small">{v.t("KR cost reference for one Stigma, through level 20. Equipment bonuses and higher-level materials are separate.","스티그마 하나의 20레벨 이하 한국 소모량입니다. 장비 보너스·상위 레벨 전용 재료는 별개입니다.")}</p></div>'
    return [(('global',('Global route','글로벌 구매')),v.section('stigma-global',('A named purchase, not every weekly task','필요한 구매부터 정하기'),global_card+v.link('routines/#routine-nightmare',v.t('Nightmare reward route','악몽 보상 경로')))),
            (('kr-shop',('KR shop limits','한국 상점 한도')),v.section('stigma-kr-stock',('KR stock that does not reset','매주 다시 살 수 없는 한국 상품'),note+table)),
            (('levels',('KR level budget','한국 레벨 예산')),v.section('stigma-levels',('Budget one skill at a time','스킬 하나씩 투자량 계산'),milestones+calc+v.link('skills/',v.t('Compare Stigma effects','스티그마 효과 비교'))))],['festival','shards']


def crafts(v):
    bracelet=v.cards([
        ('shield',('Abyssal Bracelet','Abyssal Bracelet · 팔찌'),('Global play guide recipe: 3 Ludra Gear Vouchers (Bound) + 5,000,000 Kina.', '글로벌 플레이 공략의 제작 재료: Ludra Gear Voucher (Bound) 3개 + 키나 5,000,000.')),
        ('boss',('Collect raid rewards','레이드 보상 모으기'),('Follow the Ludra reward route; keep vouchers for the intended craft.', '루드라 보상에서 교환권을 모으고 제작용으로 남깁니다.')),
    ])
    arcana=v.cards([
        ('book',('Base Unique Arcana','기본 유일 아르카나 제작'),('Global table: 5 Mysterious Crystals + 2,000,000 Kina. Extra selected options add costs.', '글로벌 표의 기본 제작은 Mysterious Crystal 5개 + 키나 2,000,000. 추가 선택 옵션에는 비용이 더 듭니다.')),
        ('spark',('Choose the right card','필요한 카드부터 선택'),('Chalice, Parchment, Compass, Bell and Mirror occupy different slots. Compare the skill/passive bonus before crafting.', '성배·양피지·나침반·종·거울은 슬롯이 다릅니다. 제작 전에 필요한 스킬·패시브 보너스를 비교하세요.')),
    ])
    route=v.steps([
        (('Choose the finished item','완성품 하나 선택'),('Our advice: name the slot or skill you want to improve.', '우리의 선택 기준: 보완할 부위나 주력 스킬을 먼저 정하세요.')),
        (('Reserve useful cards','쓸 카드는 먼저 남기기'),('Crystals have season reward and Arcana extraction routes; do not extract a card you still need.', '결정은 시즌 보상·아르카나 추출 경로를 확인합니다. 쓸 카드를 먼저 남기세요.')),
        (('Review the full recipe','총 제작 비용 확인'),('Base crafting and optional picks are different budgets. Keep enough Kinah for the next useful upgrade.', '기본 제작과 추가 선택 비용을 구분하고 다음 성장에 쓸 키나도 남깁니다.')),
    ])
    return [(('bracelet',('Bracelet','팔찌')),v.section('craft-bracelet',('A raid reward with a purpose','목표를 정하고 레이드 보상 모으기'),bracelet)),
            (('arcana',('Arcana','아르카나')),v.section('craft-arcana',('Craft for a skill you use','자주 쓰는 스킬을 위한 제작'),arcana)),
            (('materials',('Material route','재료 모으기')),v.section('craft-materials',('Keep, collect, then craft','남길 것·모을 것·만들 것'),route+v.link('routines/#routine-transcendence',v.t('Arcana reward route','아르카나 보상 경로'))+v.link('guides/kinah-farming/',v.t('Plan your Kinah','키나 예산 준비'))))],['gear','arcana','arcana-guide']


def pendant(v):
    rows='<div class="ag-table"><table><thead><tr>'+''.join(f'<th>{s}</th>' for s in [v.t('Unique step','유일 강화 단계'),v.t('Base chance','기본 확률'),v.t('Per failure','실패 1회 보정')])+'</tr></thead><tbody>'+''.join(f'<tr><th>{i} → {i+1}</th><td data-label="{v.t("Base chance","기본 확률")}">{chance}%</td><td data-label="{v.t("Per failure","실패 1회 보정")}">+{PENDANT_BONUS[i]}%p</td></tr>' for i,chance in enumerate(PENDANT_CHANCES))+'</tbody></table></div>'
    controls=f'<div class="ag-controls" data-ag-controls hidden><label>{v.t("Current Unique level","현재 유일 강화 단계")}<select data-pendant-level>'+''.join(f'<option value="{i}">+{i} → +{i+1}</option>' for i in range(20))+'</select></label><label>'+v.t('Failures at this same step','현재 단계에서 실패한 횟수')+'<input data-pendant-failures type="number" min="0" max="100" step="1" value="0" inputmode="numeric"></label></div>'
    calc=f'<div class="ag-calculator" data-pendant-planner data-chances="{e(json.dumps(PENDANT_CHANCES))}" data-bonuses="{e(json.dumps(PENDANT_BONUS))}" data-lang="{v.lang}">{controls}<div class="ag-probability"><span>{v.t("Next attempt · reference","다음 시도 · 참고표")}</span><strong data-pendant-chance>75%</strong><div class="ag-meter"><i data-pendant-bar style="width:75%"></i></div></div><p data-pendant-result aria-live="polite">{v.t("75% + 0 × 5%p = 75%.","75% + 실패 0회 × 5%p = 75%.")}</p><p class="ag-small">{v.t("Same-step explanation from KR community data, capped at 100%. It does not predict your result or read your account.","한국 커뮤니티 표의 동일 단계 설명이며 최대 100%로 제한합니다. 성공 결과를 예측하거나 계정 상태를 읽는 도구가 아닙니다.")}</p></div>'
    materials=v.steps([
        (('Confirm the item grade','펜던트 등급 확인'),('Rare and Epic quest tracks use different essences from the Unique track.', '희귀·전승 퀘스트 구간과 유일 구간은 사용하는 정수가 다릅니다.')),
        (('Follow the material name','표시된 재료 이름 따라가기'),('KR references move from Dragon Essence to Splendent Dragon Essence in the later Unique steps.', '한국 자료의 유일 초반 용족의 정수와 후반 찬란한 용족의 정수를 구분합니다.')),
        (('Use the current cost preview','현재 강화 창의 비용 확인'),('The July and October sources disagree on some quantities, Kinah and Amplify Stones. Their market-value totals are not a current budget.', '7월·10월 자료는 일부 수량·키나·돌파석 소모가 다릅니다. 과거 거래소 단가를 포함한 총액은 현재 예산으로 쓰지 않습니다.')),
    ])
    return [(('chance',('Next attempt','다음 시도 확률')),v.section('pendant-next',('Understand failure compensation','실패 보정을 그림으로 이해하기'),calc)),
            (('table',('Probability table','단계별 확률')),v.section('pendant-table',('Matching values in two KR references','두 한국 자료가 일치하는 확률·보정'),rows)),
            (('materials',('Materials & budget','재료·예산')),v.section('pendant-materials',('Prepare the materials for this attempt','이번 시도에 필요한 재료 준비'),materials))],['pendant-old','pendant-new']


def raid(v, kind):
    if kind=='orbs':
        steps=[('Agree four DPS assignments','딜러 4명 담당 구역 합의'),('Break only your assigned cold orbs','자기 구역 냉기 구슬만 파괴'),('Keep the rings apart; leave warmth intact','고리끼리 간격 유지·온기 보존'),('Tanks coordinate breath directions','탱커끼리 브레스 방향 합의')]
        tokens=''.join(f'<circle cx="{x}" cy="{y}" r="9" class="ag-cold"/>' for x,y in [(160,43),(240,43),(297,105),(297,185),(240,247),(160,247),(103,185),(103,105)])
        tokens+='<circle cx="200" cy="145" r="22" class="ag-warm"/><text x="200" y="150" text-anchor="middle">'+v.t('Warmth','온기')+'</text>'
        tokens+=''.join(f'<g class="ag-orb-player ag-player-{i}"><circle cx="{x}" cy="{y}" r="13"/><circle cx="{x}" cy="{y}" r="25" class="ag-ring"/><text x="{x}" y="{y+4}" text-anchor="middle">{i}</text></g>' for i,(x,y) in enumerate([(140,80),(260,80),(260,210),(140,210)],1))
    else:
        steps=[('Keep large hazards on the outside','큰 장판을 외곽에 배치'),('Resolve spin and jump on the outside','회전·점프 베기를 외곽에서 처리'),('Return the tank at the agreed moment','합의한 타이밍에 탱커 복귀'),('The next targeted move brings the boss in','다음 위치 추적 공격으로 보스 중앙 유도')]
        tokens='<circle cx="72" cy="110" r="23" class="ag-hazard"/><circle cx="318" cy="215" r="23" class="ag-hazard"/><line x1="325" y1="145" x2="200" y2="145" class="ag-pull"/><g class="ag-tank"><circle r="13"/><text y="4" text-anchor="middle">T</text></g><g class="ag-raid-boss"><circle r="21"/><text y="4" text-anchor="middle">B</text></g>'
    transcript='<ol class="ag-raid-steps">'+''.join(f'<li>{e(v.p(step))}</li>' for step in steps)+'</ol>'
    buttons=f'<div class="ag-controls" data-ag-controls hidden><button type="button" data-raid-play aria-pressed="true">{v.t("Pause","일시정지")}</button><button type="button" data-raid-next>{v.t("Next step","다음 동작")}</button><label>{v.t("Playback speed","설명 재생 속도")}<select data-raid-speed><option value="1">1×</option><option value="0.5">0.5×</option><option value="1.5">1.5×</option></select></label></div>'
    return f'<figure class="ag-raid" data-raid-lesson="{kind}" data-phase="0" data-lang="{v.lang}">{buttons}<svg viewBox="0 0 400 290" role="img" aria-label="{v.t("Illustrative raid positions","공대 위치 설명도")}"><circle cx="200" cy="145" r="123" class="ag-arena"/><circle cx="200" cy="145" r="55" class="ag-center"/><text x="200" y="25" text-anchor="middle">12</text><text x="349" y="150">3</text><text x="200" y="278" text-anchor="middle">6</text><text x="47" y="150">9</text>{tokens}</svg><figcaption><strong data-raid-label>{e(v.p(steps[0]))}</strong><small>{v.t("Schematic positions and playback time, not measured game distances or timings.","위치·재생 시간은 설명용이며 실제 거리·시전 시간을 측정한 그림이 아닙니다.")}</small></figcaption>{transcript}</figure>'


def bitan(v):
    orb=raid(v,'orbs')+'<p class="ag-note">'+v.t('Oct 9 proposal: four assigned DPS each handle two cold orbs. This is one raid strategy, not a universal party convention.', '10월 9일 제안: 담당 딜러 4명이 냉기 구슬 2개씩 맡는 방식입니다. 특정 공대의 제안이며 모든 파티의 공통 규칙으로 단정하지 않습니다.')+'</p>'
    movement=raid(v,'movement')+v.cards([
        ('target',('Order A','순서 A'),('Central ground → large hazards + spin → targeted teleport slash. The guide uses an ally pull after the outside jump.', '중앙 장판 → 큰 장판·회전 → 순간이동 베기. 공략은 외곽 점프 뒤 아군 끌어당기기를 사용합니다.')),
        ('target',('Order B','순서 B'),('Teleport slash → spin → large hazards + central move. Return timing differs; agree before the pull.', '순간이동 베기 → 회전 → 큰 장판·중앙 이동. 복귀 타이밍이 다르므로 끌어당기기 전에 합의합니다.')),
    ])
    patch=v.cards([
        ('boss',('October 14 · KR','10월 14일 · 한국'),('NC reduces Deltras’s Ice Wedge HP by 50%. Recheck who can break it; the Oct 8 strategy predates this adjustment.', 'NC는 델트라스 얼음 쐐기 체력을 50% 낮춥니다. 쐐기 담당을 재검토하세요. 10월 8일 이동 공략은 이 조정 이전 자료입니다.')),
        ('check',('Before joining','입장 전 파티 합의'),('Agree assignments, the selected movement order and assistance skills. These KR raid lessons do not establish Global availability.', '담당 구역·선택한 이동 순서·보조 스킬을 합의합니다. 이 한국 레이드 공략이 글로벌 콘텐츠 적용을 뜻하지는 않습니다.')),
    ])
    return [(('orbs',('Orb assignments','구슬 역할')),v.section('bitan-orbs',('Keep assignments and rings separate','담당 구역·고리 간격 유지'),orb)),
            (('movement',('Below 50%','체력 50% 이하')),v.section('bitan-movement',('Bring the boss back safely','보스를 안전하게 중앙으로 유도'),movement)),
            (('patch',('Patch & party','패치·파티 준비')),v.section('bitan-patch',('Use the current raid rules','현재 레이드 규칙으로 준비하기'),patch))],['orbs','movement','patch']


RENDERERS={'gear-options':gear,'shugo-festival':festival,'stigma-growth':stigma,'endgame-crafts':crafts,'kr-pendant':pendant,'kr-bitan':bitan}


def render(slug, lang, base):
    from guidebrowse import reader
    v=View(lang,base);g=next(g for g in GUIDES if g['slug']==slug)
    entries,keys=RENDERERS[slug](v)
    source=''.join(body for _,body in entries)+v.sources(keys)
    # Every panel owns a full section, preserving bookmarked IDs and native details.
    from guidebrowse import Fragments
    panels=[(key,title,[next(iter(Fragments(body).ids))]) for (key,title),body in entries]
    scope=v.t('Dated source guidance; confirm the material and reward preview for your region.', '출처 날짜가 있는 공략입니다. 재료·보상은 자신의 서버 미리보기와 맞춰 확인하세요.')
    lead=f'<div class="ag-scope"><span class="ag-region">{g["region"]}</span><span>{v.t("Reviewed","검토")} {REVIEWED}</span><p>{scope}</p></div>'
    return '<div class="advanced-guide" data-practical-page="'+slug+'">'+reader(lang,slug,source,panels,tail=['ag-sources'],lead=lead)+'</div>'


def search_entries(lang, base):
    v=View(lang,base)
    aliases={'gear-options':'Sync Bind Reset Soul Binding Transfer 동기화 초기화 영혼 부여 계승 불꽃', 'shugo-festival':'Shugo Festival Centuryroot Tokens Reward Keys 페스타 열쇠 보상 종목', 'stigma-growth':'Stigma Shards 샤드 스티그마 어비스 악몽 상점 누적 한도', 'endgame-crafts':'Ludra Abyssal Bracelet Arcana Chalice of Vigor 팔찌 아르카나 제작', 'kr-pendant':'Draconic Pendant KR 펜던트 실패 보정 확률 유일', 'kr-bitan':'Snowfield Grief Deltras KR 비탄 델트라스 구슬 쐐기 50%'}
    return [dict(lang=lang,path=('ko/' if v.k else '')+'guides/'+g['slug']+'/',title=v.p(g['title']),description=v.p(g['description']),category=g['region']+' · '+v.t('Practical guide','성장 상세 공략'),keywords=aliases[g['slug']]) for g in GUIDES]

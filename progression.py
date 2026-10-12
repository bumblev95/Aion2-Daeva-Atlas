"""Four practical growth guides with dated, regional source attribution.

Reward targets describe the reviewed Global client. Encounter lessons reuse the
existing KR-source collection; they are not claims of Global gameplay testing.
"""
from html import escape as e
from fieldnotes import BOSSES, KR_SOURCES

REVIEWED = '2026-10-12'
ROOT = 'guides/'
GUIDES = [
    ('pet-growth', ('Pet growth & farming', '펫 내실·영혼 파밍'),
     ('Choose a pet family, find its souls and turn collection progress into stats.', '펫 종족별 능력치, 천족·마족 사냥터, 영혼과 이해도 결정의 사용 순서.')),
    ('gear-targets', ('Target gear & enhancement', '목표 장비 획득·강화'),
     ('Pick the dungeon for your missing slot, then decide how far to enhance.', '필요한 장비 부위로 던전을 고르고 강화·돌파·교환에 쓸 재료를 정하세요.')),
    ('dungeon-rewards', ('Dungeon rewards & boss plans', '던전별 공략·보상'),
     ('Six Conquest dungeons: entry gates, target loot, key mechanics and reward uses.', '정복 던전 6종의 입장 기준·목표 보상·핵심 기믹과 클리어 후 사용처.')),
    ('kinah-farming', ('Kinah farming & spending', '키나 파밍·사용처'),
     ('Earn enhancement funds and Market money through the activities that pay each kind.', '강화 비용과 거래소 구매 자금을 구분하고 사명·일일 던전·판매 재료로 모으세요.')),
]

# Each small source summary is original; large source tables are not reproduced.
SOURCES = {
    'pet-system': ('https://space4games.com/en/games-en/aion-2-pets-guide/',
        ('Space4Games · pet systems', 'Space4Games · 펫 성장 시스템'),
        ('Global play guide; updated 2026-10-10. Owned effects, Insight and Genus Analysis.', '글로벌 플레이 공략 · 2026.10.10 수정. 보유 효과·개별 이해도·종족 분석.')),
    'pet-stats': ('https://www.inven.co.kr/board/aion2/6444/1077',
        ('Inven · Nirr · pet stats', '인벤 Nirr · 펫 능력치·이해도'),
        ('KR community reference; 2026-01-14 revision. Family bonuses, not Global level caps.', '한국 커뮤니티 자료 · 2026.01.14 수정. 종족별 보너스 참고, 글로벌 단계 상한과 구분.')),
    'pet-spawns': ('https://www.inven.co.kr/board/aion2/6444/689',
        ('Inven · Rokah · pet soul locations', '인벤 Rokah · 펫 영혼 획득처 DB'),
        ('KR field locations; 2026-01-16 revision. Six examples, with KR names retained for lookup.', '한국 필드 획득처 · 2026.01.16 수정. 사냥터 6곳을 선별했으며 서버별 명칭·배치는 다를 수 있음.')),
    'odium': ('https://metabot.gg/en/aion-2/dungeons/odylium-repository',
        ('MetaBot · Odylium Repository', 'MetaBot · 오디움 저장소'),
        ('Global client reward reference; Growth Pet Chests. Shared Daily Dungeon entry pool.', '글로벌 클라이언트 보상 자료. 성장 펫 상자·일일 던전 공통 입장 횟수.')),
    'gear': ('https://metabot.gg/en/aion-2/guides/gear-progression-guide',
        ('MetaBot · gear progression', 'MetaBot · 장비 성장 경로'),
        ('Global reference; updated 2026-10-07. Item tiers, crafting and voucher conversions.', '글로벌 참고 · 2026.10.07 수정. 장비 단계·제작·교환권 변환.')),
    'enhance': ('https://metabot.gg/en/aion-2/guides/gear-enhancement-guide',
        ('MetaBot · enhancement', 'MetaBot · 강화·돌파'),
        ('Global client curves reviewed 2026-10-12. Ordinary equipment, not Clash Rune rules.', '2026.10.12 검토한 글로벌 강화표. 일반 장비와 충돌 룬의 실패 규칙 구분.')),
    'entries': ('https://metabot.gg/en/aion-2/guides/dungeon-guide',
        ('MetaBot · dungeon modes and gates', 'MetaBot · 던전 모드·입장 기준'),
        ('Global reference reviewed 2026-10-12. Gates are character totals; reward item levels are different.', '글로벌 참고 · 2026.10.12 검토. 입장 기준은 캐릭터 종합 수치이며 보상 장비 자체의 레벨과 다름.')),
    'kinah': ('https://metabot.gg/en/aion-2/guides/kinah-farming-guide',
        ('MetaBot · Kinah sources and currency types', 'MetaBot · 키나 획득처·화폐 구분'),
        ('Global reference; updated 2026-10-10. Fixed rewards and tradable materials; no live Market prices.', '글로벌 참고 · 2026.10.10 수정. 정해진 보상·판매 가능한 재료, 실시간 거래소 시세 아님.')),
    'depository': ('https://metabot.gg/en/aion-2/dungeons/crobakhis-secret-depository',
        ("MetaBot · Crobakhi’s Secret Depository", 'MetaBot · 크로파킨 비밀 보관소'),
        ('Global score table: 300,000 bound Kinah at 10,000 score; lower scores pay less.', '글로벌 점수별 보상표. 1만 점에 귀속 키나 30만, 낮은 점수는 보상 감소.')),
    'duties': ('https://metabot.gg/en/aion-2/guides/daily-weekly-checklist',
        ('MetaBot · daily and weekly counters', 'MetaBot · 일일·주간 횟수'),
        ('Global reference; updated 2026-10-07. Duty Missions and the shared Daily Dungeon pool.', '글로벌 참고 · 2026.10.07 수정. 사명 횟수·일일 던전 공통 입장 횟수.')),
    'game8': ('https://game8.co/games/Aion-2',
        ('Game8 · AION 2 guide index', 'Game8 · AION 2 공략 목록'),
        ('Public index/search summaries used to discover topics. Full articles were not accessible (HTTP 402); details above use the readable sources.', '공개 목록·검색 요약으로 주제를 찾았습니다. 본문은 HTTP 402로 열리지 않아 세부 내용은 위 열람 가능한 출처로 확인했습니다.')),
}

# Both the gear route and boss pages use these same reviewed reward targets.
DUNGEONS = [
    dict(boss='berk', gate=700, tier=54, db='krao-cave',
         loot=('Rupture weapons · accessories', '크라오 무기·장신구'),
         example='Rupture Claymore', goal=('Weapon / accessory', '무기·장신구'),
         use=('Build your first Conquest weapon; reserve its voucher for a missing slot.', '첫 정복 무기 후보를 확보하고 교환권은 부족한 부위를 채우는 데 남깁니다.')),
    dict(boss='bakarma', gate=700, tier=54, db='draupnir',
         loot=('Bakarma armor · guard', '바카르마 방어구·수호패'),
         example='Bakarma Guard', goal=('Armor / guard', '방어구·수호패'),
         use=('Replace weak armor slots; compare the guard conversion before repeating for one drop.', '낮은 방어구 부위를 교체합니다. 수호패가 안 나오면 교환권 변환도 비교하세요.')),
    dict(boss='auldor', gate=1400, tier=70, db='urugugu-canyon',
         loot=('Aulamus weapons · accessories', '우루구구 무기·장신구'),
         example='Aulamus Greatsword', goal=('Weapon / accessory', '무기·장신구'),
         use=('Upgrade the damage side of your set; keep Wrathful materials for crafting or a Market sale.', '무기·장신구를 다음 단계로 올립니다. 제작 재료는 직접 제작과 거래소 판매 중 목적을 정하세요.')),
    dict(boss='vakron', gate=1400, tier=70, db='vakron-sky-island',
         loot=('Vakron armor · guard', '바크론 방어구·수호패'),
         example='Vakron Guard', goal=('Armor / guard', '방어구·수호패'),
         use=('Fill armor gaps beside the Urugugu weapon route; target the slot you are still wearing at a lower tier.', '우루구구 무기 파밍과 병행해 방어구를 채웁니다. 아직 낮은 단계인 부위부터 교체하세요.')),
    dict(boss='kromede', gate=2100, tier=86, db='fire-temple',
         loot=('Enraged Kromede weapons · accessories', '분노한 크로메데 무기·장신구'),
         example='Enraged Kromede Claymore', goal=('Weapon / accessory', '무기·장신구'),
         use=('Keep a weapon you intend to enhance further; Wrathful Ego also feeds high-tier Dragon Lord crafts.', '오래 사용할 무기를 고르고 강화 계획을 세웁니다. Wrathful Ego는 상위 용제 제작에도 쓰입니다.')),
    dict(boss='nuakum', gate=2100, tier=86, db='ferocious-horn-den',
         loot=('Nuakum armor · guard', '누아쿰 방어구·수호패'),
         example='Nuakum Guard', goal=('Armor / guard', '방어구·수호패'),
         use=('Complete the armor side of this tier; compare a voucher conversion with another random drop.', '같은 단계의 방어구를 완성합니다. 필요한 부위는 추가 파밍과 교환권 변환을 함께 비교하세요.')),
]
for d in DUNGEONS:
    d['encounter'] = next(b for b in BOSSES if b['id'] == d['boss'])
    SOURCES[d['db']] = ('https://metabot.gg/en/aion-2/dungeons/'+d['db'],
        ('MetaBot · '+d['encounter']['dungeon'][0], 'MetaBot · '+d['encounter']['dungeon'][1]),
        ('Global Conquest loot reference; reviewed 2026-10-12. Listed drops are not guaranteed.', '글로벌 정복 보상 자료 · 2026.10.12 검토. 목록에 있는 장비가 매번 확정 지급되지는 않음.'))

PET_ROUTES = [
    ('elyos', 'lupilini', ('Modified Lupilini', '개조된 루필리니'), 'Cogni',
     ('Kuraka Hill Path · NE', '쿠라카 언덕길 · 천족 2시'), ('Lupilini Test Subject', '루필리니 실험체')),
    ('elyos', 'birota', ('Birota', '비로타'), 'Cogni',
     ('Eastern Tolbas Forest · SW', '톨바스 숲 동부 · 천족 8시'), ('Wandering Birota', '방랑 비로타')),
    ('elyos', 'kalnip', ('Modified Kalnip', '개조된 칼니프'), 'Fera',
     ('Verteron Fortress Ruins · central west', '베르테론 요새 폐허 · 천족 중앙 9시'), ('Fierce Kalnip', '난폭한 칼니프')),
    ('asmodian', 'manduri', ('Manduri Fighter', '만두리 싸움꾼'), 'Cogni',
     ('Black Claw Village · SE', '검은발톱 부락 · 마족 5시'), ('Black Claw Manduri Fighter', '검은발톱 만두리 전투병')),
    ('asmodian', 'mumu', ('Mumu Worker', '무무 일꾼'), 'Cogni',
     ('Dranaktus · NE', '드라낙투스 · 마족 1시'), ('Mumu Worker', '무무 일꾼')),
    ('asmodian', 'spider', ('Dry Branch Spider', '마른 가지 거미'), 'Fera',
     ('Nameless Graveyard · NW', '이름없는 묘지 · 마족 11시'), ('Dry Branch Spider', '마른 가지 거미')),
]

WALKTHROUGHS = {
    'berk': ('Left boss → right boss → central Seal Guardian → final room; fly across the gap.', '왼쪽 보스 → 오른쪽 보스 → 중앙 봉인 수호자 → 최종 방. 낙사 구간은 비행해서 건넙니다.'),
    'bakarma': ('Open the entrance control, glide left to the first boss, then use updrafts and the activated wind path.', '입구 제어장치 작동 후 왼쪽 보스로 활강합니다. 이후 용오름과 활성화한 바람길로 진행합니다.'),
    'auldor': ('Upper boss → lower boss → defeat the Wind Mage → follow the wind paths to Auldor.', '위쪽 보스 → 아래쪽 보스 → 바람술사 처치 → 열린 바람길을 따라 아울도르로 이동합니다.'),
    'vakron': ('Break the rock barrier, defeat the Odyle Rock Spirit and follow the wind route; place four elements at the final altar.', '돌벽·오드 바위 정령 구간을 지나 바람길로 이동합니다. 마지막 제단에는 원소 4개를 모아 올립니다.'),
    'kromede': ('Bring cleansing potions for burns. Agree who activates the cooling controls before regrouping at bosses.', '화상 해제용 치유 물약을 준비합니다. 냉각수 제어기를 작동할 인원을 나눈 뒤 보스 앞에서 합류합니다.'),
    'nuakum': ('Bomb the wall → first boss → break the left wall → totem → necromancer → updraft to the final boss.', '폭탄으로 벽 파괴 → 첫 보스 → 왼쪽 벽 파괴 → 토템 → 강령술사 → 용오름으로 최종 보스에 도착합니다.'),
}

SECTION_NAV = {
    'pet-growth': [('pet-families', ('Which pet?', '어떤 펫?')), ('pet-farming', ('Farming locations', '사냥터')), ('pet-spending', ('Spend materials', '재료 사용'))],
    'gear-targets': [('gear-ladder', ('Target gear', '목표 장비')), ('gear-investment', ('Enhancement order', '강화 순서')), ('gear-materials', ('Materials', '재료 획득처')), ('gear-fallbacks', ('Vouchers & crafting', '교환·제작'))],
    'dungeon-rewards': [('dungeon-plans', ('Dungeon plans', '던전별 공략')), ('dungeon-after', ('Use the rewards', '보상 사용'))],
    'kinah-farming': [('kinah-types', ('Currency types', '키나 종류')), ('kinah-fixed', ('Fixed rewards', '보상 수입')), ('kinah-market', ('Market sales', '판매 재료')), ('kinah-plan', ('Today’s plan', '오늘 할 일'))],
}


class View:
    def __init__(self, lang, base):
        self.k = lang == 'ko'
        self.r = base + ('ko/' if self.k else '')
    def t(self, en, ko):
        return ko if self.k else en
    def p(self, pair):
        return e(pair[self.k])
    def a(self, route, label, css=''):
        return f'<a class="{css}" href="{self.r+route}">{label} →</a>'
    def cite(self, *keys):
        return '<p class="progress-cite">'+self.t('Sources: ', '출처: ')+ ' · '.join(f'<a href="#growth-source-{key}">{self.p(SOURCES[key][1])}</a>' for key in keys)+'</p>'
    def section(self, id, title, intro, body):
        return f'<section class="progress-section" id="{id}"><header><h2>{self.p(title)}</h2><p>{self.p(intro)}</p></header>{body}</section>'
    def cards(self, items):
        return '<div class="progress-cards">'+''.join(f'<article><h3>{self.p(title)}</h3><p>{self.p(copy)}</p></article>' for title, copy in items)+'</div>'
    def sources(self, keys):
        return f'<details class="progress-sources" id="growth-sources"><summary>{self.t("Sources, region and review date", "출처·적용 서버·검토일")} · {REVIEWED}</summary><p>{self.t("Priorities are editorial suggestions. Global database values and dated KR field reports are labelled separately. This is not a live account tracker.", "우선순위는 자료를 종합한 편집상 제안입니다. 글로벌 DB 수치와 한국 플레이 공략의 적용 범위를 나눠 표시했으며 실시간 캐릭터 정보는 아닙니다.")}</p><ul>'+''.join(f'<li id="growth-source-{key}"><a href="{e(SOURCES[key][0])}" target="_blank" rel="noopener noreferrer">{self.p(SOURCES[key][1])} ↗</a><p>{self.p(SOURCES[key][2])}</p></li>' for key in dict.fromkeys([*keys, 'game8']))+'</ul></details>'


def gateway(lang, base):
    v = View(lang, base)
    return f'<section class="growth-guide-links" aria-label="{v.t("Four growth guides", "성장 상세 공략 4가지")}"><h2>{v.t("Make your next upgrade concrete", "다음 성장 목표, 구체적으로 골라보세요")}</h2><div>'+''.join(f'<a data-growth-guide="{slug}" href="{v.r}{ROOT}{slug}/"><span>0{i}</span><strong>{v.p(title)}</strong><small>{v.p(desc)}</small></a>' for i,(slug,title,desc) in enumerate(GUIDES,1))+'</div></section>'


def banner(lang, base, slug):
    v = View(lang, base)
    _, title, desc = next(g for g in GUIDES if g[0] == slug)
    return f'<a class="endgame-gateway growth-gateway" href="{v.r}{ROOT}{slug}/"><strong>{v.p(title)}</strong><span>{v.p(desc)} →</span></a>'


def pet_guide(v):
    t = v.t
    systems = v.cards([
        (('1. Collect and grow individual pets', '1. 펫 수집·개별 이해도'),
         ('Souls unlock pets and raise their Insight. Owned bonuses work even when another pet is equipped.', '영혼으로 펫을 얻고 개별 이해도를 올립니다. 다른 펫을 꺼내도 보유 효과는 적용됩니다.')),
        (('2. Build the family’s progress', '2. 종족 이해도와 분석 슬롯'),
         ('Growing pets also advances their genus. Its level determines which analysis slots and grades are available.', '여러 펫을 성장시키면 해당 종족의 이해도도 쌓입니다. 종족 단계에 따라 분석 슬롯·등급이 열립니다.')),
        (('3. Spend crystals on analysis', '3. 결정·키나로 옵션 분석'),
         ('After a pet reaches its Insight cap, spare souls can become genus Soul Crystals. Analysis spends crystals and Kinah.', '개별 이해도 상한 이후의 남는 영혼은 해당 종족의 영혼 결정으로 바꿉니다. 종족 분석에는 결정과 키나를 씁니다.')),
    ])
    family_rows = [
        ('Cogni · 지성', ('HP · Critical Hit', '생명력·치명타'), ('Start here when improving offensive collection stats.', '치명타 내실을 채우려면 우선 검토')),
        ('Fera · 야성', ('Ground mount speed · Accuracy', '탑승물 지상 이동 속도·명중'), ('Prioritize missing pets when attacks miss.', '공격이 빗나간다면 미보유 펫부터 검토')),
        ('Natura · 자연', ('SP · Critical Resistance', '정신력·치명타 저항'), ('Fill after your immediate combat-stat gaps.', '급한 공격 능력치를 채운 뒤 수집 확대')),
        ('Varian · 변형', ('Mount sprint SP cost · Evasion', '탑승물 질주 정신력 소모·회피'), ('A collection and utility branch to build alongside other routes.', '다른 동선과 함께 챙길 수집·편의 성장')),
    ]
    rows = ''.join(f'<tr><th scope="row">{e(name)}</th><td data-label="{t("Bonus family", "보너스 방향")}">{v.p(bonus)}</td><td data-label="{t("Our priority", "선택 기준")}">{v.p(why)}</td></tr>' for name,bonus,why in family_rows)
    families = f'<div class="progress-table"><table><thead><tr><th>{t("Genus", "펫 종족")}</th><th>{t("Owned bonuses as pets grow", "성장하며 얻는 보유 효과")}</th><th>{t("Which to work on", "어떤 상황에 챙길까")}</th></tr></thead><tbody>{rows}</tbody></table></div>'+v.cite('pet-stats')
    farms = ''
    for faction, label, zone in [('elyos', ('Elyos', '천족'), 'Verteron'), ('asmodian', ('Asmodian', '마족'), 'Altgard')]:
        cards = ''
        for _, id, pet, family, place, monster in [p for p in PET_ROUTES if p[0] == faction]:
            korean = '' if v.k else f'<small class="progress-alias">KR: {e(pet[1])} · {e(place[1])} · {e(monster[1])}</small>'
            cards += f'<article id="pet-{id}"><span class="progress-chip">{family} · {t("KR location", "한국 위치 참고")}</span><h4>{v.p(pet)}</h4><dl><div><dt>{t("Go to", "사냥터")}</dt><dd>{v.p(place)}</dd></div><div><dt>{t("Defeat", "대상 몬스터")}</dt><dd>{v.p(monster)}</dd></div><div><dt>{t("You gain", "얻는 것")}</dt><dd>{v.p(pet)} {t("souls → pet Insight", "영혼 → 개별 이해도")}</dd></div></dl>{korean}</article>'
        farms += f'<section class="pet-faction" id="pet-{faction}"><div class="progress-subhead"><h3>{v.p(label)}</h3>{v.a("maps/?zone="+zone,t("Open region map", "지역 지도 열기"))}</div><div class="progress-cards">{cards}</div></section>'
    farms += '<p class="progress-note">'+t('These are dated KR spawn references, not measured farming routes. English pet/location labels here are reading aids; use the retained KR names with the original DB. Our region map shows travel points, not pet-spawn pins.', '위치는 한국 공략의 사냥터 예시입니다. 시간당 수급량을 측정한 최적 동선은 아닙니다. 지역 지도는 이동 거점 확인용이며 펫 출현 좌표를 표시하지 않습니다.')+'</p>'+v.cite('pet-spawns')
    budget = v.cards([
        (('Souls first; expensive rerolls later', '영혼 수집부터, 고비용 재분석은 나중에'),
         ('Pick one missing pet or the next Insight level before hunting. Leave when that goal is reached; add another family when it addresses your current stat gap.', '사냥 전에 미보유 펫 하나나 다음 이해도 단계를 목표로 잡으세요. 목표를 채우면 다른 펫으로 옮겨 부족한 능력치를 넓게 보완합니다.')),
        (('Lock only a roll worth keeping', '남길 옵션을 정한 뒤 잠그기'),
         ('Locked slots raise analysis costs. Decide the stat and a Kinah/crystal limit before rerolling; an automatic grade stop does not guarantee the stat you wanted.', '옵션을 잠글수록 분석 비용이 늘어납니다. 원하는 능력치와 결정·키나 한도를 먼저 정하세요. 자동 분석의 등급 정지는 원하는 능력치까지 보장하지 않습니다.')),
        (('Use a dungeon when souls are the goal', '일일 던전도 펫 성장에 사용'),
         ('Odylium Repository awards Growth Pet Chests. It shares entries with the stone and Kinah dungeons, so choose it when pets are your next upgrade.', '오디움 저장소의 성장 펫 상자로 영혼을 보충합니다. 강화석·키나 던전과 입장 횟수를 공유하니 오늘 필요한 보상으로 선택하세요.')),
    ])+v.a('routines/#daily-choice-odium',t('Compare Daily Dungeon rewards', '일일 던전 보상 비교'),'progress-action')+v.cite('pet-system','odium')
    return (
        v.section('pet-growth-loop', ('Souls → Insight → permanent growth', '영혼을 모으면 무엇이 오를까?'),
                  ('Collection bonuses and analysis rolls are separate sources of growth.', '펫을 모아 얻는 보유 효과와 분석으로 뽑는 옵션은 별개의 성장입니다.'), systems+v.cite('pet-system'))+
        v.section('pet-families', ('Choose the stat you are missing', '부족한 능력치로 종족 선택'),
                  ('Bonus families below follow the KR guide. Do not carry its numerical level caps into another region.', '아래는 한국 자료의 보너스 방향입니다. 단계별 수치·상한을 다른 서버에 그대로 적용하지 않습니다.'), families)+
        v.section('pet-farming', ('Where to get the souls', '어디서 누구를 잡을까?'),
                  ('Start with reachable home-faction locations. Each target below names both the pet and the monster that supplies its soul.', '먼저 이동 가능한 자기 진영 필드부터 고르세요. 키울 펫과 영혼을 주는 몬스터를 함께 적었습니다.'),
                  f'<nav class="progress-jumps" aria-label="{t("Pet farming faction", "펫 사냥터 진영")}"><a href="#pet-elyos">{t("Elyos locations", "천족 사냥터")}</a><a href="#pet-asmodian">{t("Asmodian locations", "마족 사냥터")}</a></nav>'+farms)+
        v.section('pet-spending', ('Turn materials into useful stats', '모은 재료를 성장으로 바꾸는 순서'),
                  ('Global play reports reviewed here show individual Insight capped at 3; the dated KR guide describes levels up to 5. Use your region’s track.', '확인한 글로벌 플레이 공략은 개별 이해도 3단계, 한국 자료는 5단계까지 설명합니다. 자신의 서버 성장 단계를 기준으로 진행하세요.'), budget)+
        v.sources(['pet-system','pet-stats','pet-spawns','odium']))


def gear_guide(v):
    t=v.t
    tiers=''
    for i,(gate,tier) in enumerate([(700,54),(1400,70),(2100,86)],1):
        pair=[d for d in DUNGEONS if d['tier']==tier]
        cells=''
        for d in pair:
            b=d['encounter']
            cells+=f'<div><span>{v.p(d["goal"])}</span><h4>{v.p(b["dungeon"])}</h4><p>{v.p(d["loot"])}</p><small>{t("DB item example", "DB 아이템 예시")}: {e(d["example"])}</small>{v.a(ROOT+"dungeon-rewards/#dungeon-"+b["slug"],t("Rewards & boss plan", "보상·공략 보기"))}</div>'
        tiers+=f'<article class="gear-tier" id="gear-tier-{tier}"><header><span class="progress-chip">0{i} · {t("CONQUEST", "정복")}</span><h3>{t("Entry total", "입장 종합 수치")} {gate:,}</h3><p>{t("Character Lv 45 · target Unique item level", "캐릭터 45레벨 · 목표 유일 장비 레벨")} <b>{tier}</b></p></header><div class="gear-tier-pair">{cells}</div></article>'
    ladder = tiers+v.cite('entries','gear')
    invest=v.cards([
        (('First: a useful Unique at +10', '먼저: 사용할 유일 장비 +10'),
         ('For ordinary Unique gear, +0 to +10 is guaranteed in the cited Global curve. Build the weapon you will use, then patch armor gaps that block survival or entry.', '글로벌 참고표의 일반 유일 장비는 +0~+10이 확정 구간입니다. 사용할 무기를 먼저 갖추고 생존·입장에 부족한 방어구를 보완하세요.')),
        (('Then: one long-lived weapon to +15', '다음: 오래 쓸 무기 +15'),
         ('Above +10, ordinary enhancement can fail and consume stones and Kinah. Reserve the next upgrade’s budget before committing to one weapon.', '+10 이후에는 실패하며 강화석·키나를 소모할 수 있습니다. 다음 장비를 살 비용까지 모두 쓰기 전에, 계속 쓸 무기 하나의 투자 한도를 정하세요.')),
        (('Finally: amplification and fine rolls', '그 뒤: 돌파·세부 옵션'),
         ('Eligible max-enhanced Unique gear uses Amplify Stones and Kinah. Add expensive Manastone rolls after settling on the base item.', '돌파 가능한 유일 장비를 최대 강화한 뒤 돌파석·키나를 씁니다. 마석의 고비용 옵션 투자는 오래 쓸 장비를 정한 후 진행하세요.')),
    ])+'<p class="progress-note">'+t('Ordinary failed enhancement loses materials, not levels. Clash Runes can lose a level; amulets and belts use their own scroll track. These rules are not interchangeable.', '일반 장비의 강화 실패는 재료 손실이며 강화 단계 하락은 아닙니다. 충돌 룬은 단계가 내려갈 수 있고 아뮬렛·허리띠는 별도 주문서를 쓰므로 같은 규칙으로 계산하지 마세요.')+'</p>'+v.cite('enhance')
    materials=[
        (('Enhance Stones + Kinah', '강화석 + 키나'), ('Bio-Research Base / quests + Duty Missions', '데바 생체연구기지·퀘스트 + 사명'), ('Ordinary enhancement', '일반 장비 강화'), 'routines/#daily-choice-bio'),
        (('Amplify Stone Fragments', '돌파석 조각'), ('Conquest / Transcendence / Sanctuary rewards', '정복·초월·성역의 해당 보상'), ('Substance Morph → Amplify Stones → eligible max-enhanced gear', '물질 변환으로 돌파석 → 최대 강화한 해당 장비 돌파'), 'routines/#reward-stone'),
        (('Amulet / belt scrolls', '아뮬렛·허리띠 주문서'), ('KR: Monolith resonance / garrison completion', '한국 참고: 모노리스 공명·주둔지 완료'), ('Enhance the matching special slot', '해당 특수 부위 강화'), 'gear/#enhancement-materials'),
    ]
    rows=''.join(f'<tr><th scope="row">{v.p(mat)}</th><td data-label="{t("Source", "획득처")}">{v.p(where)}</td><td data-label="{t("Use", "사용처")}">{v.p(use)}<br>{v.a(url,t("Open farming route", "획득 동선"))}</td></tr>' for mat,where,use,url in materials)
    supply=f'<div class="progress-table"><table><thead><tr><th>{t("What is missing", "부족한 재료")}</th><th>{t("Where to farm", "어디서 얻나")}</th><th>{t("Next action", "얻은 뒤 할 일")}</th></tr></thead><tbody>{rows}</tbody></table></div>'+v.cite('enhance')
    fallback=v.cards([
        (('Missing guard or armor', '수호패·방어구가 안 나올 때'),
         ('Draupnir, Vakron and Ferocious Horn vouchers have guard and armor-chest conversions. Compare the recipe’s Kinah cost with another run.', '드라웁니르·바크론·사나운 뿔 교환권은 수호패와 방어구 상자 변환에 쓰입니다. 재료와 키나 비용을 보고 추가 파밍과 비교하세요.')),
        (('Wrong weapon or missing accessory', '다른 직업 무기·부족한 장신구'),
         ('The weapon-side dungeons have accessory-chest recipes and weapon-selection conversions. A weapon swap also needs the matching dungeon weapon; a voucher alone is not a free weapon.', '무기 쪽 던전에는 장신구 상자와 무기 선택 변환이 있습니다. 무기 교환에는 해당 던전 무기도 필요하므로 교환권만으로 무기를 받는 것으로 생각하면 안 됩니다.')),
        (('Planning past this ladder', '다음 단계까지 준비할 때'),
         ('In this Global snapshot, Ludra weapons/guard and Splendent Wise or Ebony Dragon Lord crafts reach item level 102. Price the recipe chain before buying materials.', '확인한 글로벌 자료에서는 루드라 무기·수호패와 Splendent Wise / Ebony Dragon Lord 제작이 장비 레벨 102 목표입니다. 재료 구매 전 전체 제작 경로를 계산하세요.')),
    ])+v.cite('gear')
    return (
        '<div class="progress-callout"><strong>'+t('Entry total ≠ one item’s level', '입장 종합 수치 ≠ 장비 한 개의 레벨')+'</strong><p>'+t('700 / 1,400 / 2,100 are character entry gates for the Conquest pairs below. 54 / 70 / 86 are the target items’ own levels. The ladder is a Global reference, not a current KR best-in-slot list.', '아래 700·1,400·2,100은 정복 입장에 필요한 캐릭터 종합 수치, 54·70·86은 보상 장비 자체의 레벨입니다. 글로벌 성장 참고이며 현재 한국 서버의 최종 장비표가 아닙니다.')+'</p></div>'+
        v.section('gear-ladder', ('Choose the slot, then the dungeon', '필요한 부위를 정하고 던전을 고르세요'),
                  ('Each pair splits its main Unique rewards between weapons/accessories and armor/guards. Targets are possible loot, not guaranteed drops.', '각 단계에서 주요 유일 보상이 무기·장신구와 방어구·수호패로 나뉩니다. 목표 보상은 드롭 후보이며 매번 확정 획득은 아닙니다.'),ladder)+
        v.section('gear-investment', ('How far should this item go?', '이 장비에 어디까지 투자할까?'),
                  ('Our order prioritizes a usable set before expensive finishing work.', '사용 가능한 장비 구성을 갖춘 뒤 세부 강화에 투자하는 순서를 권합니다.'), invest)+
        v.section('gear-materials', ('Match each upgrade to its supply route', '강화에 필요한 재료와 획득처'), ('Go to the content that supplies the material you lack.', '부족한 재료를 주는 콘텐츠로 연결합니다.'),supply)+
        v.section('gear-fallbacks', ('When the target will not drop', '목표 장비가 안 나올 때의 대안'), ('Keep vouchers and compare conversions before discarding spare equipment.', '여분 장비를 정리하기 전에 교환권·물질 변환 재료로 쓸 수 있는지 확인하세요.'),fallback)+
        v.a(ROOT+'kinah-farming/',t('Fund this enhancement plan', '강화 비용 모으는 방법'),'progress-action')+
        v.sources(['gear','enhance','entries']))


def dungeon_brief(lang, base, boss_id):
    v=View(lang,base);t=v.t
    d=next(d for d in DUNGEONS if d['boss']==boss_id)
    return f'<aside class="dungeon-reward-brief"><span>{t("GLOBAL · CONQUEST TARGET", "글로벌 · 정복 보상 목표")}</span><h2>{v.p(d["loot"])}</h2><p>{t("Lv 45 · entry total", "45레벨 · 입장 종합 수치")} {d["gate"]:,} · {t("reward item level", "보상 장비 레벨")} {d["tier"]}</p><p>{v.p(d["use"])}</p>{v.a(ROOT+"dungeon-rewards/#dungeon-"+d["encounter"]["slug"],t("Reward details and sources", "보상 상세·출처"))}<small>{t("Reviewed 2026-10-12. Boss lessons below use the separately labelled KR source guides.", "2026.10.12 검토. 아래 보스 패턴은 별도로 표시한 한국 공략 기준입니다.")}</small></aside>'


def dungeon_guide(v):
    t=v.t
    index=''.join(f'<a href="#dungeon-{d["encounter"]["slug"]}"><strong>{v.p(d["encounter"]["dungeon"])}</strong><span>{d["gate"]:,} · {v.p(d["goal"])}</span></a>' for d in DUNGEONS)
    cards=''
    keys=['entries']
    for d in DUNGEONS:
        b=d['encounter']; keys.append(d['db'])
        # Preserve the source collection's exact cue/action pairing.
        moves=''.join(f'<li><strong>{v.p(m["cue"])}</strong><span>{v.p(m["action"])}</span></li>' for m in b['mechanics'])
        source_ids=list(dict.fromkeys(m['source'] for m in b['mechanics']))
        refs=' · '.join(f'<a href="{e(KR_SOURCES[s]["url"])}" target="_blank" rel="noopener noreferrer">{e(KR_SOURCES[s]["publisher"])} · {KR_SOURCES[s]["date"]} ↗</a>' for s in source_ids)
        cards+=f'''<article class="dungeon-plan" id="dungeon-{b['slug']}"><header><span class="progress-chip">{t('GLOBAL · CONQUEST', '글로벌 · 정복')}</span><h3>{v.p(b['dungeon'])}</h3><p>{t('Entry: Lv 45, total item level', '입장: 45레벨, 종합 아이템 레벨')} <b>{d['gate']:,}</b></p></header><div class="dungeon-plan-body"><div class="dungeon-loot"><span class="progress-label">{t('TARGET REWARD', '목표 보상')}</span><h4>{v.p(d['loot'])}</h4><p>{t('Unique · item level', '유일 · 장비 레벨')} {d['tier']}<br><small>{t('DB example', 'DB 예시')}: {e(d['example'])}</small></p><p>{v.p(d['use'])}</p>{v.cite(d['db'])}</div><div class="dungeon-response"><span class="progress-label">{t('KR CONQUEST LESSON', '한국 정복 패턴 참고')}</span><p class="dungeon-route-note"><strong>{t('Route / preparation', '동선·준비')}</strong>{v.p(WALKTHROUGHS[b['id']])}</p><h4>{v.p(b['name'])}</h4><ul>{moves}</ul>{v.a('dungeons/'+b['slug']+'/',t('Watch the patterns and movement', '패턴·이동 애니메이션 보기'),'progress-action')}<p class="progress-cite">{refs}</p></div></div></article>'''
    after=v.cards([
        (('Equip the useful drop', '목표 장비는 교체 후보로'),
         ('Compare the new base item with your enhanced equipment. A higher base tier is a reason to compare, not a reason to discard the old item immediately.', '새 장비와 현재 강화한 장비를 비교합니다. 보상 장비의 기본 단계가 높아도 지금 장비를 바로 버리기 전에 강화 비용·옵션까지 보세요.')),
        (('Keep the matching voucher', '교환권은 부족한 부위에'),
         ('Save the dungeon-specific voucher for the recipe that fills your missing slot; leave enough Kinah for conversion.', '던전별 교환권은 부족한 부위를 채우는 레시피에 사용합니다. 변환 키나도 함께 남겨두세요.')),
        (('Use or sell crafting drops', '제작 재료는 사용·판매 결정'),
         ('Keep inputs for your planned craft. Compare tradable surplus with current Market listings instead of treating every dungeon item as sellable.', '목표 제작에 필요한 재료는 보관합니다. 남은 재료는 거래 가능 여부와 거래소 시세를 비교해 판매하세요. 모든 던전 장비가 판매 가능한 것은 아닙니다.')),
    ])+v.a(ROOT+'gear-targets/#gear-fallbacks',t('Equipment and voucher routes', '장비·교환권 사용 경로'),'progress-action')+v.a(ROOT+'kinah-farming/#kinah-market',t('Tradable material examples', '판매 재료 예시'),'progress-action')+v.cite('gear','kinah')
    return (
        '<div class="progress-callout"><strong>'+t('Pick your reward before spending an entry', '입장 전에 보상부터 고르세요')+'</strong><p>'+t('Loot and entry gates below use the Global database; movement lessons come from dated KR Conquest guides. Exploration has different gates/rewards. Reward counters and cube energy are separate from these level gates.', '보상·입장 기준은 글로벌 DB, 패턴 대응은 한국 정복 공략 기준입니다. 탐험 난이도의 조건·보상과 섞지 마세요. 보상 횟수와 큐브 오드는 아래 입장 레벨과 별도로 확인합니다.')+'</p>'+v.a('routines/#routine-conquest',t('Entries and energy planning', '입장·보상 횟수와 오드 계획'))+'</div>'+
        f'<nav class="dungeon-jumps" aria-label="{t("Choose a dungeon", "던전 선택")}">{index}</nav>'+
        v.section('dungeon-plans', ('The reward and the fight, together', '보상과 공략을 함께 보기'), ('Choose the matching difficulty; the boss notes are not a verified Global replay.', '참여할 난이도에 맞춰 보세요. 한국 보스 설명을 글로벌 실측 공략으로 표시하지 않습니다.'),cards)+
        v.section('dungeon-after', ('After the clear', '클리어한 뒤 무엇을 할까?'), ('Turn the drop into the next upgrade before choosing another run.', '보상 사용처를 정한 뒤 다음 던전을 고르세요.'),after)+v.sources(keys+['gear','kinah']))


def kinah_guide(v):
    t=v.t
    money=v.cards([
        (('Bound Kinah: fund growth', '귀속 키나: 내 캐릭터 성장 비용'),
         ('Quest and Daily Dungeon payouts below are bound. They pay eligible enhancement costs but cannot buy Market listings.', '아래 퀘스트·일일 던전 보상은 귀속 키나입니다. 해당 강화 비용에 쓰지만 거래소 물건을 사는 돈으로 쓸 수는 없습니다.')),
        (('Unbound Kinah: trading funds', '거래 가능 키나: 거래소 구매 자금'),
         ('Sell eligible tradable items to other players for Market money. Keep this balance for purchases that bound Kinah cannot cover.', '거래 가능한 아이템을 거래소에서 판매해 구매 자금을 만듭니다. 귀속 키나로 결제할 수 없는 구매에 사용할 돈을 따로 남깁니다.')),
        (('A combined cost can use both', '합산 비용은 두 종류를 함께 사용'),
         ('The Global “Kina (All)” pool spends bound first, then unbound. Having enough total Kinah does not mean all of it is Market money.', '글로벌의 Kina (All) 비용은 귀속분을 먼저 쓰고 거래 가능분을 이어서 씁니다. 총 보유 키나 전체가 거래소 자금인 것은 아닙니다.')),
    ])+v.cite('kinah')
    rows=[
        (('Duty Missions', '사명'), ('50,000 bound each · 5 completed = 250,000', '1회 귀속 5만 · 5회 완료 시 25만'), ('Daily allowance', '일일 횟수'), 'routines/#routine-duties'),
        (("Crobakhi’s Secret Depository", '크로파킨 비밀 보관소'), ('Up to 300,000 bound at 10,000 score', '1만 점 달성 시 최대 귀속 30만'), ('Shared Daily Dungeon pool; not a separate daily allowance', '일일 던전 3종 공통 횟수 사용'), 'routines/#daily-choice-kinah'),
        (('Uncleared Sealed Dungeons', '아직 안 깬 봉인 던전'), ('15,000 bound in the cited clear rewards', '참고 보상표의 클리어 보상 귀속 1만 5천'), ('First-clear route; not an unlimited repeat farm', '미완료 던전 순회 · 무한 반복 수입 아님'), 'maps/?type=sealed_dungeon'),
        (('Unfinished story / District quests', '남은 스토리·지역 퀘스트'), ('Bound Kinah plus the quest’s growth rewards', '귀속 키나와 해당 퀘스트의 성장 보상'), ('One-time progression', '캐릭터별 일회성 성장'), 'endgame/#after-story'),
    ]
    table=''.join(f'<tr><th scope="row">{v.p(name)}</th><td data-label="{t("Payout", "보상")}">{v.p(reward)}</td><td data-label="{t("Repeat / route", "주기·동선")}">{v.p(cadence)}<br>{v.a(url,t("Open route", "공략으로 이동"))}</td></tr>' for name,reward,cadence,url in rows)
    fixed=f'<div class="progress-table"><table><thead><tr><th>{t("Activity", "할 일")}</th><th>{t("Bound Kinah", "귀속 키나 보상")}</th><th>{t("Repeat and route", "반복 여부·동선")}</th></tr></thead><tbody>{table}</tbody></table></div><p class="progress-note">'+t('Planning example: five 50,000-Kinah duties plus one 10,000-score depository clear = 550,000 bound Kinah, before any costs. This assumes all five duties and an available shared entry; it is not an hourly income or a guaranteed Daily Dungeon result.', '계획 예시: 5만 키나 사명 5회 + 보관소 1만 점 1회 = 비용 차감 전 귀속 키나 55만. 사명 5회 완료·공통 입장 횟수·1만 점을 전제로 한 계산이며 시간당 수입이나 무조건 받는 보상이 아닙니다.')+'</p>'+v.cite('kinah','duties','depository')
    market=v.cards([
        (('Dungeon crafting materials', '정복 던전 제작 재료'),
         ('Wrathful Mind: the six classic dungeons. Wrathful Will: Urugugu/Vakron and the higher pair. Wrathful Ego: Fire Temple/Ferocious Horn. These feed Dragon Lord crafting; sell only tradable surplus.', 'Wrathful Mind는 기본 6종, Wrathful Will은 우루구구·바크론 이상, Wrathful Ego는 불의 신전·사나운 뿔에서 노립니다. 용제 제작용 재료이며 남는 거래 가능분을 판매합니다.')),
        (('Gather along a useful route', '기존 동선에서 채집'),
         ('Compare ore, wood and Odyle listings before taking a detour. A gathered material kept for your own recipe saves a purchase; only a completed sale creates income.', '이동 동선의 광석·목재·오드 시세를 비교합니다. 직접 제작에 쓴 채집물은 구매 비용을 아끼는 것이고, 실제 판매가 성사된 것만 수입입니다.')),
        (('Price a craft from its inputs', '제작은 재료값부터 계산'),
         ('For example, Ruby Powder and Yggdrasil Paper are processed tradable inputs. Compare selling the raw material with processing it; include purchased ingredients and displayed selling fees.', 'Ruby Powder·Yggdrasil Paper 같은 가공 재료는 원재료 그대로 판매할 때와 비교합니다. 구입 재료값과 화면에 표시되는 판매 수수료를 함께 계산하세요.')),
    ])+'<div class="kinah-formula"><strong>'+t('Net proceeds = completed sale − materials bought − selling costs', '순수입 = 실제 판매대금 − 구매한 재료값 − 판매 비용')+'</strong><p>'+t('No live prices or measured Kinah-per-hour are available here. Test a small batch before spending your enhancement budget on stock.', '현재 서버 시세·시간당 수급량을 측정한 자료는 없습니다. 소량이 팔리는지 확인한 뒤 물량을 늘려 강화 예산까지 재고에 묶이지 않게 하세요.')+'</p></div>'+v.cite('kinah')
    choices=v.cards([
        (('Need stones and Kinah', '강화석과 키나가 함께 부족'),
         ('Finish duties for Kinah; choose Bio-Research Base for stones. Put both into the equipment goal you already selected.', '사명으로 키나를 모으고 데바 생체연구기지에서 강화석을 받습니다. 정해둔 목표 장비에 두 재료를 함께 투자하세요.')),
        (('Have stones; lack enhancement money', '강화석은 있는데 키나가 부족'),
         ('Use an available Daily Dungeon entry on the depository. Add unfinished field rewards before paying to redraw more tasks.', '일일 던전의 남은 횟수를 비밀 보관소에 사용합니다. 미완료 필드 보상도 챙긴 뒤 추가 비용이 드는 선택을 판단하세요.')),
        (('Saving for a Market purchase', '거래소 장비를 사고 싶은 경우'),
         ('Set the target purchase price, farm its tradable funding route, and reserve your bound balance for enhancement. Skip analysis rerolls that delay that purchase.', '목표 구매가를 정하고 거래 가능한 재료를 모아 자금을 만듭니다. 귀속분은 강화 비용으로 쓰고, 구매 시점을 늦추는 펫 재분석은 뒤로 미루세요.')),
    ])+v.a(ROOT+'gear-targets/#gear-investment',t('Choose an enhancement stopping point', '장비 강화 투자선 정하기'),'progress-action')+v.a(ROOT+'pet-growth/#pet-spending',t('Plan pet analysis spending', '펫 분석 비용 계획'),'progress-action')
    return (
        v.section('kinah-types', ('Which kind of Kinah do you need?', '지금 필요한 키나는 어떤 돈일까?'), ('Choose between funding your own upgrades and buying from another player.', '내 장비를 강화할 돈인지, 거래소에서 물건을 살 돈인지 먼저 정하세요.'),money)+
        v.section('kinah-fixed', ('Reliable reward routes', '정해진 보상부터 모으기'), ('Global reward references reviewed 2026-10-12; score and completion conditions still apply.', '2026.10.12 검토한 글로벌 보상 참고입니다. 점수·완료·입장 조건을 함께 봅니다.'),fixed)+
        v.section('kinah-market', ('What can become Market money?', '무엇을 팔아 거래소 자금을 만들까?'), ('The drop matters only if that particular item can be traded and someone buys it.', '해당 아이템이 거래 가능하고 실제 구매자가 있어야 판매 수입이 됩니다.'),market)+
        v.section('kinah-plan', ('Choose today’s money route', '오늘 할 일과 사용처 정하기'), ('A short route works best when it funds one named upgrade.', '다음 성장 목표 하나에 필요한 돈과 재료를 모으는 순서입니다.'),choices)+v.sources(['kinah','duties','depository']))


def render(slug, lang, base):
    v=View(lang,base);t=v.t
    renderers={'pet-growth':pet_guide, 'gear-targets':gear_guide, 'dungeon-rewards':dungeon_guide, 'kinah-farming':kinah_guide}
    nav=''.join(f'<a href="{v.r}{ROOT}{s}/"'+(' aria-current="page"' if s==slug else '')+f'><span>0{i}</span>{v.p(title)}</a>' for i,(s,title,_) in enumerate(GUIDES,1))
    sections=''.join(f'<a href="#{id}">{v.p(title)}</a>' for id,title in SECTION_NAV[slug])
    following=next((g for i,g in enumerate(GUIDES) if i>0 and GUIDES[i-1][0]==slug),None)
    next_link=v.a(ROOT+following[0]+'/',t('Next: ','다음: ')+v.p(following[1])) if following else ''
    return f'<div class="progress-guide" data-progression-guide="{slug}"><nav class="progress-series" aria-label="{t("Growth guide series", "성장 공략 순서")}">{nav}</nav><p class="progress-reviewed">{t("Reviewed", "자료 검토")} · {REVIEWED}</p><nav class="progress-jumps" aria-label="{t("On this page", "이 페이지에서 찾기")}">{sections}</nav>{renderers[slug](v)}<div class="progress-footer">{next_link}{v.a("routines/",t("Daily & weekly rewards", "일일·주간 숙제로 돌아가기"))}{v.a("endgame/#after-story",t("Post-story growth route", "스토리 이후 성장 순서"))}</div></div>'


def search_entries(lang, base):
    k=lang=='ko';prefix=('ko/' if k else '')+ROOT
    entries=[dict(lang=lang,path=prefix+slug+'/',title=title[k],description=desc[k],category=('Growth guides','성장 상세 공략')[k],keywords=' '.join(title+desc)) for slug,title,desc in GUIDES]
    for faction,id,pet,family,place,monster in PET_ROUTES:
        entries.append(dict(lang=lang,path=prefix+'pet-growth/',anchor='pet-'+id,title=pet[k],description=place[k]+' · '+monster[k],category=('Pet souls','펫 영혼')[k],keywords=' '.join(pet+place+monster)+' '+family+' '+faction+' 펫작 이해도 영혼 pet souls'))
    for d in DUNGEONS:
        b=d['encounter']
        entries.append(dict(lang=lang,path=prefix+'dungeon-rewards/',anchor='dungeon-'+b['slug'],title=b['dungeon'][k]+(' rewards',' 보상')[k],description=d['loot'][k],category=('Dungeon rewards','던전 보상')[k],keywords=' '.join(b['name']+b['dungeon']+d['loot'])+' '+d['example']+' '+str(d['gate'])+' '+str(d['tier'])))
    return entries

"""Reviewed daily/weekly activities, with rewards connected to actual growth uses.

Counts describe the cited snapshot, not a live integration with the game account.
Keep daily-expiry, replenishing counters and weekly-reset entries separate.
"""
from html import escape as e

REVIEWED = '2026-10-09'

SOURCES = {
    'inven': (('Inven · daily and weekly activities', '인벤 · 일일·주간 콘텐츠'),
              'https://www.inven.co.kr/webzine/news/?news=311583&site=aion2',
              ('KR launch-era article, Nov 23, 2025; reward routes only, old counts excluded.',
               '한국 출시 초기 기사 · 2025.11.23. 보상 경로 참고, 과거 횟수 제외.')),
    'kr45': (('Inven · Naptan · level-45 content guide', '인벤 납탄 · 45레벨 콘텐츠 안내'),
             'https://www.inven.co.kr/board/aion2/6444/2080',
             ('KR community guide, Jul 13, 2026; KR reward/shop examples.',
              '한국 커뮤니티 공략 · 2026.07.13. 한국 보상·상점 사례.')),
    'community': (('DCInside · returning/new-player guide', '디시인사이드 · 뉴비·복귀 가이드'),
                  'https://gall.dcinside.com/mgallery/board/view/?id=aion2&no=2638459',
                  ('KR community guide, Jul 1, 2026; weekly priorities and spending routes.',
                   '한국 커뮤니티 공략 · 2026.07.01. 주간 우선순위·보상 활용 참고.')),
    'global': (('MetaBot · Global content counters', 'MetaBot · 글로벌 콘텐츠 횟수'),
               'https://metabot.gg/en/aion-2/guides/daily-weekly-checklist',
               ('Global client reference, updated Oct 7, 2026; counters and reset rules.',
                '글로벌 클라이언트 참고 · 2026.10.07 갱신. 횟수·충전·초기화 규칙.')),
    'launch': (('MeinMMO · Global first-week checklist', 'MeinMMO · 글로벌 첫 주 숙제'),
               'https://mein-mmo.de/en/aion-2-daily-weekly-checklist-perfect-start,1589979/',
               ('Global launch guide, Sep 29, 2026; duties, orders, crafting and shops.',
                '글로벌 출시 공략 · 2026.09.29. 사명·지령·제작·상점 참고.')),
    'endgame': (('MetaBot · Global endgame systems', 'MetaBot · 글로벌 엔드게임 시스템'),
                'https://metabot.gg/en/aion-2/guides/endgame-guide',
                ('Global client reference reviewed Oct 9, 2026; modes and reward types.',
                 '글로벌 클라이언트 참고 · 2026.10.09 확인. 콘텐츠 종류·보상.')),
    'arcana': (('Inven · Arcana acquisition and equipment', '인벤 · 아르카나 획득·장착'),
               'https://www.inven.co.kr/webzine/news/?news=311909&site=aion2',
               ('KR article, Dec 6, 2025; skill/stat use, historical stage targets excluded.',
                '한국 기사 · 2025.12.06. 스킬·능력치 활용 참고, 과거 단계 목표 제외.')),
    'bio': (('MetaBot · Daeva Bio-Research Base', 'MetaBot · 데바 생체연구기지'),
            'https://metabot.gg/en/aion-2/dungeons/daeva-bio-research-base',
            ('Global build 0.0.4387.0; weekly shared counter and score rewards.',
             '글로벌 빌드 0.0.4387.0 · 공통 주간 횟수·점수 보상.')),
    'odium': (('MetaBot · Odylium Repository', 'MetaBot · 오디움 저장소'),
              'https://metabot.gg/en/aion-2/dungeons/odylium-repository',
              ('Global build 0.0.4387.0; Growth Pet Chest score rewards.',
               '글로벌 빌드 0.0.4387.0 · 성장 펫 상자 점수 보상.')),
    'kinah': (("MetaBot · Crobakhi’s Secret Depository", 'MetaBot · 크로파킨 비밀 보관소'),
              'https://metabot.gg/en/aion-2/dungeons/crobakhis-secret-depository',
              ('Global build 0.0.4387.0; bound Kinah score rewards.',
               '글로벌 빌드 0.0.4387.0 · 귀속 키나 점수 보상.')),
    'trial': (('MetaBot · Ascension Trial score rewards', 'MetaBot · 각성전 점수 보상'),
              'https://metabot.gg/en/aion-2/dungeons/nightmare-altar',
              ('Global client reference; Ascension Trial, distinct from the Nightmare ladder.',
               '글로벌 클라이언트 참고 · 각성전 자료. 악몽 보스 도전과 별개.')),
    'nightmare': (('MetaBot · Nightmare currency and shop', 'MetaBot · 악몽 재화·교환 상점'),
                  'https://metabot.gg/en/aion-2/currencies/phantasmal-fragment',
                  ('Global build 0.0.4387.0; Phantasmal Fragment purchases.',
                   '글로벌 빌드 0.0.4387.0 · Phantasmal Fragment 교환 품목.')),
    'pets': (('SPACE4GAMES · pet growth and analysis', 'SPACE4GAMES · 펫 성장·분석'),
             'https://space4games.com/en/games-en/aion-2-pets-guide/',
             ('Global gameplay guide, Oct 7, 2026; souls, Genus Insight and analysis.',
              '글로벌 플레이 공략 · 2026.10.07. 영혼·종족 이해도·분석.')),
    'ap': (('SPACE4GAMES · Abyss Point uses', 'SPACE4GAMES · 어비스 포인트 사용처'),
           'https://space4games.com/en/games-en/aion-2-abyss-points/',
           ('Global gameplay guide, Oct 7, 2026; Stigma Shards and Daevanion purchases.',
            '글로벌 플레이 공략 · 2026.10.07. 스티그마 샤드·데바니온 구매.')),
}


def activity(id, group, name, cadence, reward, use, tip, sources, link=''):
    return dict(id=id, group=group, name=name, cadence=cadence, reward=reward,
                use=use, tip=tip, sources=sources, link=link)


ACTIVITIES = [
    activity('duties', 'daily', ('Duty Missions', '사명 임무'),
             ('5 rewarded completions / day · shared per server', '보상 하루 5회 · 서버 내 캐릭터 공유'),
             ('Kinah, Abyss Points; other rewards depend on the selected mission.', '키나·어비스 포인트, 임무별 추가 보상'),
             ('Kinah funds enhancement; Abyss Points buy Stigma Shards and Daevanion growth.', '키나는 강화 비용, 어비스 포인트는 스티그마 샤드·데바니온 성장에 사용'),
             ('Choose missions with a reward you need. Watch the reroll cost.', '필요한 보상을 주는 임무를 고르고, 재설정 비용도 함께 봅니다.'),
             ['launch', 'ap'], 'skills/'),
    activity('supply', 'daily', ('Emergency Supply Requests', '긴급 보급 의뢰'),
             ('Daily · when the delivery cost is affordable', '일일 · 납품 비용이 감당될 때'),
             ('Abyss Points for delivering the requested items.', '요구 물품 납품 → 어비스 포인트'),
             ('Turn points into Stigma Shards or the Daevanion item you need.', '어비스 상점에서 스티그마 샤드·필요한 데바니온 결정으로 교환'),
             ('Compare the item price with the reward before buying materials.', '부족한 물품을 사기 전에 납품 비용과 받을 보상을 비교합니다.'),
             ['inven', 'ap']),
    activity('conquest', 'banked', ('Expedition · Conquest', '원정 · 정복'),
             ('Global: +1 reward count / 8 h, up to 21', '글로벌 참고: 보상 횟수 8시간당 1회, 최대 21회'),
             ('Dungeon equipment, Kinah and crafting materials.', '던전 장비·키나·제작 재료'),
             ('Equip an upgrade; put stones and Kinah toward the item you will keep.', '필요한 새 장비를 장착하고, 재료·키나는 계속 쓸 장비에 투자'),
             ('Check both reward counts and Odyle Energy for the cube. Choose the dungeon for the missing slot.', '보상 횟수와 큐브에 필요한 오드를 함께 확인하고, 부족한 장비 부위가 나오는 던전을 고릅니다.'),
             ['global', 'kr45'], 'dungeons/'),
    activity('transcendence', 'banked', ('Transcendence', '초월'),
             ('Global: +1 reward count / 12 h, up to 14', '글로벌 참고: 보상 횟수 12시간당 1회, 최대 14회'),
             ('Arcana cards and Kinah.', '아르카나 카드·키나'),
             ('Equip cards for useful skill levels, stats and set effects.', '주력 스킬 레벨·능력치·세트 효과에 맞는 카드를 장착'),
             ('Match the reward preview to the card slot and skill you need. Cube claims use Odyle Energy.', '필요한 카드 부위와 스킬 옵션을 보상 목록에서 확인합니다. 큐브 보상에는 오드가 필요합니다.'),
             ['global', 'arcana'], 'skills/'),
    activity('nightmare', 'banked', ('Nightmare · solo boss ladder', '악몽 · 1인 보스 도전'),
             ('Global: +2 attempts / day, up to 14', '글로벌 참고: 하루 2회 충전, 최대 14회 누적'),
             ('Nightmare currency · Global name: Phantasmal Fragment.', '악몽 교환 재화 · 글로벌명 Phantasmal Fragment'),
             ('Shop: Daevanion Crystals, Stigma Shards, Clash Rune Chests, statues or wings.', '악몽 상점에서 데바니온 결정·스티그마 샤드·격돌의 룬 상자·석상·날개로 교환'),
             ('Prioritize the next growth purchase. Check its unlock requirement and your clearable boss tier.', '다음 성장에 필요한 교환품을 정하고, 구매 해금 조건과 깰 수 있는 보스 단계를 확인합니다.'),
             ['endgame', 'nightmare']),
    activity('festival', 'banked', ('Shugo Festival', '슈고 페스타'),
             ('Daily key refill · spend near the key cap', '열쇠 일일 충전 · 상한에 가까워지면 사용'),
             ('Festival currency and reward-cube items.', '페스타 교환 재화·보상 큐브 아이템'),
             ('Use the shop for needed growth supplies; KR guides also list crafting materials.', '상점에서 필요한 성장 재료로 교환 · 한국 공략에는 제작 재료 보상도 소개'),
             ('Sources disagree on key refill amounts. Use your client’s key count and event timer.', '자료마다 열쇠 충전량이 달라 횟수는 게임 표기를 따릅니다. 열쇠 잔량·이벤트 시간을 확인하세요.'),
             ['launch', 'global', 'kr45']),
    activity('invasion', 'banked', ('Dimensional Invasion', '차원 침공'),
             ('Global: +1 reward key / day, up to 7', '글로벌 참고: 하루 열쇠 1개, 최대 7개'),
             ('Event currency and cube rewards; KR guides compare these to Festival rewards.', '이벤트 교환 재화·큐브 보상 · 한국 공략은 페스타 계열 보상으로 설명'),
             ('Exchange event currency for the supplies offered in your region.', '현재 서버의 교환 상점에서 필요한 재료 구매'),
             ('Join when the event appears during your session and you have a reward key.', '접속 중 이벤트가 열리고 보상 열쇠가 있을 때 참여합니다.'),
             ['launch', 'kr45']),
    activity('daily-dungeon', 'weekly', ('Daily Dungeon · Unknown Fissure', '일일 던전 · 미지의 틈새'),
             ('14 basic entries / week · one shared server pool', '기본 주 14회 참고 · 서버 공유 횟수'),
             ('Choose Enhance Stones, pet-growth chests or bound Kinah.', '강화석 / 펫 성장 상자 / 귀속 키나 중 필요한 보상 선택'),
             ('Enhance gear, grow pets or pay upgrade costs. See the three choices below.', '장비 강화·펫 내실·강화 비용에 사용 · 아래 3종 비교 참고'),
             ('The name says daily, but entries reset weekly. Two a day is just a way to divide the week.', '이름은 일일이지만 입장권은 주간 충전입니다. 하루 2회는 주간 14회를 나눠 쓰는 방식입니다.'),
             ['bio', 'kr45'], '#daily-dungeon-choices'),
    activity('ascension', 'weekly', ('Ascension Trial', '각성전'),
             ('3 basic entries / week · solo', '기본 주 3회 참고 · 1인'),
             ('Global: Enhance Stones, Unique Amplify Stone Fragments, pet and binding chests.', '글로벌: 강화석·유일 돌파석 조각·성장 펫 상자·각인 상자'),
             ('Use the stones for equipment growth and the pet chest for collection growth.', '강화석·돌파석 계열은 장비 성장, 펫 상자는 수집·내실에 사용'),
             ('Entries are spent on entry in the Global reference. Choose a difficulty you can finish; score changes rewards.', '글로벌 자료에서는 입장할 때 횟수가 차감됩니다. 완주할 난이도를 고르세요. 점수에 따라 보상이 달라집니다.'),
             ['endgame', 'trial'], 'gear/#upgrade'),
    activity('subjugation', 'weekly', ('Subjugation', '토벌전'),
             ('3 basic tickets / week · party', '기본 주 3회 참고 · 파티'),
             ('KR guide: Enhance Stones and Amplify Stone Fragments.', '한국 공략 참고: 강화석·돌파석 조각'),
             ('Fund equipment enhancement and the matching amplification step.', '장비 강화와 해당 장비의 돌파 재료로 사용'),
             ('The Global client reference confirms 3 tickets; its loot list is incomplete. Check the regional reward preview.', '글로벌 자료는 주 3회 티켓을 확인하지만 보상표는 불완전합니다. 현재 서버의 보상 목록을 먼저 확인합니다.'),
             ['inven', 'endgame'], 'gear/#upgrade'),
    activity('exploration', 'weekly', ('Expedition · Exploration', '원정 · 탐험'),
             ('Global: 7 reward counts / dungeon / week', '글로벌 참고: 던전별 주 7회 보상'),
             ('Early dungeon gear and enhancement supplies.', '초기 던전 장비·강화 재료'),
             ('Fill an empty or weak slot while learning the dungeon route.', '비어 있거나 약한 장비 부위를 채우며 던전 동선 익히기'),
             ('Choose this when its loot still helps; Conquest has a separate replenishing reward counter.', '보상이 성장에 도움이 되는 던전을 고릅니다. 정복의 시간 충전 보상 횟수와 구분하세요.'),
             ['endgame', 'inven'], 'dungeons/'),
    activity('orders', 'weekly', ('Town Duty Commands', '마을 지령서'),
             ('Global launch guide: up to 12 purchases / week / server', '글로벌 출시 공략: 서버당 주 12개 구매 참고'),
             ('Abyss Points and the additional rewards on the chosen command.', '어비스 포인트·선택한 지령의 추가 보상'),
             ('Points fund Stigma or Daevanion; use energy items for more dungeon reward claims.', '어비스 포인트는 스티그마·데바니온, 오드 아이템은 던전 보상 수령에 사용'),
             ('Read the command reward before purchasing. Town and Abyss commands have separate purchase limits.', '구매 전에 보상을 확인합니다. 마을 지령서와 어비스 지령서의 구매 제한은 별개입니다.'),
             ['launch', 'inven', 'ap']),
    activity('weekly-supply', 'weekly', ('Weekly Supply Requests', '주간 보급 의뢰'),
             ('Weekly · choose affordable deliveries', '주간 · 비용이 맞는 납품 선택'),
             ('Abyss Points for the listed delivery.', '요구 물품 납품 → 어비스 포인트'),
             ('Build the balance for your next Stigma or Daevanion purchase.', '다음 스티그마 샤드·데바니온 구매에 필요한 포인트 확보'),
             ('Check the weekly category. Emergency requests are daily; season requests follow a longer cycle.', '주간 항목을 확인하세요. 긴급 의뢰는 일일, 시즌 의뢰는 별도 기간입니다.'),
             ['launch', 'ap']),
    activity('morph', 'weekly', ('Odyle Energy · Substance Morph', '오드 에너지 · 물질 변환'),
             ('Weekly recipe allowance · verify the recipe in your client', '주간 제작 제한 · 현재 서버의 레시피 확인'),
             ('Odyle Energy recharge items.', '오드 에너지 충전 아이템'),
             ('Recharge energy to claim Expedition, Transcendence or Sanctuary cubes.', '오드를 충전해 원정·초월·성역의 큐브 보상 수령'),
             ('Compare material cost and remaining craft allowance. Use expiring energy items first.', '재료값·남은 제작 횟수를 비교하고, 유효기간이 짧은 오드부터 사용합니다.'),
             ['launch', 'community', 'kr45']),
    activity('shop', 'weekly', ('Weekly shop stock', '주간 상점 재고'),
             ('Shop-specific reset · membership items may be restricted', '상점별 갱신 · 멤버십 상품은 이용 조건 있음'),
             ('Energy, challenge tickets or pet materials, depending on the shop.', '상점에 따라 오드·도전권·펫 재료'),
             ('Buy only the supplies for your next upgrade or planned reward claim.', '다음 성장 목표나 보상 받을 던전에 필요한 재료 구매'),
             ('The older KR shop guide has a different reset from dungeon weeklies. Follow each shop’s countdown.', '한국 초기 공략에서는 상점 갱신이 던전 주간 초기화와 달랐습니다. 상점마다 남은 갱신 시간을 따릅니다.'),
             ['launch', 'inven']),
    activity('season', 'weekly', ('Season missions & Daeva Pass', '시즌 미션 · 데바 패스'),
             ('Weekly progress/rewards; separate from season-long objectives', '주간 진도·보상 · 시즌 전체 목표와 구분'),
             ('Claim the reward shown for your points or pass level.', '누적 점수·패스 단계의 보상 목록에서 수령'),
             ('Use claimed energy and growth items instead of leaving them unspent.', '받은 오드는 던전 보상에, 성장 아이템은 해당 시스템에 사용'),
             ('After your usual runs, check for claimable rewards and the next threshold.', '평소 던전을 마친 뒤 수령 가능한 보상과 다음 점수 기준을 확인합니다.'),
             ['global', 'inven']),
    activity('sanctuary', 'optional', ('Sanctuary raids', '성역 레이드'),
             ('Weekly attempts and reward limits vary by raid', '주간 · 레이드별 도전 횟수·보상 제한 확인'),
             ('Raid equipment, accessories and other high-tier materials.', '레이드 장비·장신구·상위 성장 재료'),
             ('Pursue a specific upgrade after meeting the entry and party requirements.', '입장 조건과 파티 준비를 갖춘 뒤 목표 장비·장신구 파밍'),
             ('An attempt, a final-boss kill and a cube claim are different counters. Check all three before joining.', '도전 횟수·최종 보스 처치 제한·큐브 보상 수령은 서로 다른 제한입니다. 입장 전에 함께 확인하세요.'),
             ['global', 'kr45'], 'endgame/#boss-guides'),
    activity('abyss', 'optional', ('Abyss · corridors · PvP', '어비스 · 회랑 · PvP'),
             ('Weekly time budget; corridor entry depends on faction control', '주간 이용 시간 · 회랑은 세력 점령 조건 있음'),
             ('Abyss Points; mode-specific rewards.', '어비스 포인트·콘텐츠별 보상'),
             ('Buy Stigma Shards, Daevanion items or the PvP progression item you need.', '스티그마 샤드·데바니온 결정·필요한 PvP 성장품 구매'),
             ('PvE players can use the shop too. Join with a clear purchase goal and manageable combat conditions.', 'PvE 유저도 어비스 상점을 활용합니다. 살 품목과 감당할 전투 조건을 정하고 참여하세요.'),
             ['ap', 'kr45'], 'guides/pvp-context/'),
]


def gateway(lang, base):
    t = lambda en, ko: ko if lang == 'ko' else en
    r = base + ('ko/' if lang == 'ko' else '')
    return f'''<a class="endgame-gateway routine-gateway" href="{r}routines/"><strong>{t('Daily & weekly: what to run, what you gain', '일일·주간 숙제: 어디서 뭘 얻고, 어디에 쓸까?')}</strong><span>{t('Duty missions · dungeon choices · reward uses', '사명·일일 던전·주간 콘텐츠 → 보상 사용처')} →</span></a>'''


def search_entries(lang, base):
    k = lang == 'ko'
    entries = [dict(lang=lang, path=('ko/' if k else '')+'routines/',
                 anchor='routine-'+a['id'], title=a['name'][k],
                 description=a['reward'][k]+' → '+a['use'][k],
                 category=('Daily & weekly' if not k else '일일·주간 숙제'),
                 keywords=' '.join(a['name']+a['reward']+a['use'])+' daily weekly 숙제 보상 사용처')
            for a in ACTIVITIES]
    for id, name, reward in [
        ('bio', ('Daeva Bio-Research Base', '데바 생체연구기지'), ('Enhance Stones', '강화석')),
        ('odium', ('Odylium Repository', '오디움 저장소'), ('Growth Pet Chests and pet souls', '성장 펫 상자·펫 영혼')),
        ('kinah', ("Crobakhi’s Secret Depository", '크로파킨 비밀 보관소'), ('Bound Kinah', '귀속 키나')),
    ]:
        entries.append(dict(lang=lang,path=('ko/' if k else '')+'routines/',
                            anchor='daily-choice-'+id,title=name[k],description=reward[k],
                            category=('Daily Dungeon' if not k else '일일 던전'),
                            keywords=' '.join(name+reward)+' 미지의 틈새 daily weekly 숙제 보상'))
    return entries


def guide(lang, base):
    k = lang == 'ko'
    t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')

    def source_links(ids):
        return ' · '.join(f'<a href="#routine-source-{s}">{e(SOURCES[s][0][k])}</a>' for s in ids)

    def row(a):
        label = t('Related guide', '관련 공략')
        url = a['link'] if a['link'].startswith('#') else r+a['link']
        link = f'<a class="routine-related" href="{url}">{label} →</a>' if a['link'] else ''
        return f'''<tr id="routine-{a['id']}"><th scope="row"><h3>{e(a['name'][k])}</h3><p class="routine-cadence">{e(a['cadence'][k])}</p></th><td><span class="routine-mobile-label">{t('You gain', '얻는 것')}</span><p>{e(a['reward'][k])}</p></td><td><span class="routine-mobile-label">{t('Use it for', '어디에 쓰나')}</span><p>{e(a['use'][k])}</p>{link}<details class="routine-detail"><summary>{t('Run notes & sources', '진행 팁·출처')}</summary><p>{e(a['tip'][k])}</p><div class="routine-citations">{source_links(a['sources'])}</div></details></td></tr>'''

    groups = [
        ('daily', ('01 / Daily reset', '01 / 매일 초기화'), ('Start with Duty Missions', '접속하면 사명부터'),
         ('Complete your five rewarded missions; decide on supplies after checking their cost.', '사명 보상 5회를 챙기고, 보급 의뢰는 납품 비용을 보고 선택합니다.')),
        ('banked', ('02 / Replenishing counters', '02 / 횟수가 쌓이는 콘텐츠'), ('Spend before the counter fills', '충전 상한에 닿기 전에 사용'),
         ('Run these around the reward you need and the remaining counters. Unlocked content can be spread across the week.', '필요한 보상과 남은 횟수에 맞춰 진행합니다. 열린 콘텐츠를 주중·주말에 나눠 처리하세요.')),
        ('weekly', ('03 / Weekly reset', '03 / 매주 초기화'), ('Finish the useful weeklies before reset', '필요한 주간 숙제를 초기화 전에'),
         ('Weekly entries refill to their cap; unused entries do not become an extra week of runs.', '주간 입장권은 상한까지 다시 채워집니다. 남은 기본 횟수가 다음 주에 추가로 쌓이지 않습니다.')),
        ('optional', ('04 / When ready', '04 / 준비되면 선택'), ('A specific raid or Abyss goal', '성역·어비스는 목표를 정해서'),
         ('Pick the equipment or shop item first, then prepare for the required group content.', '얻을 장비나 상점 품목부터 고르고, 해당 파티·전투를 준비합니다.')),
    ]
    sections = []
    for group, kicker, title, desc in groups:
        sections.append(f'''<section class="routine-section" id="routine-group-{group}" aria-labelledby="routine-heading-{group}"><header><span class="section-kicker">{e(kicker[k])}</span><h2 id="routine-heading-{group}">{e(title[k])}</h2><p>{e(desc[k])}</p></header><div class="routine-table"><table><thead><tr><th>{t('Activity / allowance', '콘텐츠·횟수')}</th><th>{t('You gain', '얻는 것')}</th><th>{t('Use it for', '어디에 쓰나')}</th></tr></thead><tbody>{''.join(row(a) for a in ACTIVITIES if a['group']==group)}</tbody></table></div></section>''')

    choices = [
        ('bio', ('Need Enhance Stones?', '강화석이 부족하다면'), ('Daeva Bio-Research Base', '데바 생체연구기지'),
         ('10,000 score → up to 10,000 Enhance Stones', '1만 점 기준 → 강화석 최대 1만 개'),
         ('Use with Kinah in normal equipment enhancement.', '키나와 함께 일반 장비 강화에 사용'), 'gear/#upgrade'),
        ('odium', ('Need pet growth?', '펫 내실을 채운다면'), ('Odylium Repository', '오디움 저장소'),
         ('10,000 score → up to 80 Growth Pet Chests', '1만 점 기준 → 성장 펫 상자 최대 80개'),
         ('Open for souls; grow the collection and Genus Insight. Analysis uses Soul Crystals and Kinah.', '상자의 영혼으로 펫 수집·종족 이해도를 키웁니다. 옵션 분석은 영혼 결정과 키나를 사용합니다.'), '#reward-pet'),
        ('kinah', ('Need upgrade money?', '강화할 키나가 부족하다면'), ("Crobakhi’s Secret Depository", '크로파킨 비밀 보관소'),
         ('10,000 score → up to 300,000 bound Kinah', '1만 점 기준 → 귀속 키나 최대 30만'),
         ('Pay eligible character upgrade costs; bound Kinah has spending restrictions.', '사용 가능한 캐릭터 성장 비용에 사용 · 귀속 키나는 사용처 제한 있음'), '#reward-kinah'),
    ]
    choice_cards = []
    for s, need, name, reward, use, link in choices:
        url = link if link.startswith('#') else r+link
        choice_cards.append(f'''<article class="routine-choice" id="daily-choice-{s}"><span class="section-kicker">{e(need[k])}</span><h3>{e(name[k])}</h3><p class="routine-reward">{e(reward[k])}</p><p>{e(use[k])}</p><div class="reference-links"><a href="{url}">{t('Reward use', '보상 활용')} →</a><a href="{e(SOURCES[s][1])}" target="_blank" rel="noopener noreferrer">{t('Score rewards', '점수별 보상 원문')} ↗</a></div></article>''')

    rewards = [
        ('stone', ('Enhance Stones / Amplify Stone Fragments', '강화석 / 돌파석 조각'),
         ('Gear upgrade materials. Match the stone type and grade to the selected item.', '장비 성장 재료입니다. 선택한 장비에 필요한 종류·등급을 맞춥니다.'), 'gear/#upgrade', ['bio', 'trial']),
        ('kinah', ('Kinah / bound Kinah', '키나 / 귀속 키나'),
         ('Funds eligible enhancement, crafting and analysis costs. Bound currency cannot be spent everywhere.', '사용 가능한 강화·제작·분석 비용에 씁니다. 귀속 키나는 모든 거래에 쓸 수 있는 돈이 아닙니다.'), 'gear/#upgrade', ['kinah', 'pets']),
        ('arcana', ('Arcana cards', '아르카나 카드'),
         ('Equip useful skill-level and stat options; compare slots and set effects.', '스킬 레벨·능력치 옵션을 보고 장착합니다. 부위와 세트 효과도 함께 비교합니다.'), 'skills/', ['arcana']),
        ('points', ('Wisdom Stones / Daevanion Crystals', '지혜의 돌 / 데바니온 결정'),
         ('Use the item, then invest the resulting skill or board points.', '아이템을 사용한 뒤 얻은 스킬 포인트·데바니온 포인트를 실제로 투자합니다.'), 'endgame/#after-story-spend-points', ['inven', 'nightmare']),
        ('ap', ('Abyss Points / Stigma Shards', '어비스 포인트 / 스티그마 샤드'),
         ('Abyss Points buy shards; use shards for Stigma points and invest them in your build.', '어비스 포인트로 샤드를 사고, 샤드를 사용해 얻은 스티그마 포인트를 빌드에 투자합니다.'), 'skills/', ['ap']),
        ('pet', ('Pet souls / Soul Crystals', '펫 영혼 / 영혼 결정'),
         ('Souls grow collection progress; Soul Crystals pay for Genus Analysis with Kinah.', '영혼은 펫 수집·성장, 영혼 결정은 키나와 함께 종족 분석에 사용합니다.'), '', ['pets']),
        ('energy', ('Odyle Energy / challenge tickets', '오드 에너지 / 도전권'),
         ('Energy pays for eligible reward cubes; a challenge ticket adds the stated entry or reward count.', '오드는 해당 큐브 보상 수령에, 도전권은 아이템에 적힌 입장·보상 횟수 충전에 씁니다.'), '#routine-conquest', ['global', 'launch']),
    ]
    reward_rows = []
    for id, name, use, link, sources in rewards:
        url = link if link.startswith('#') else r+link
        follow = f'<a href="{url}">{t("Growth guide", "성장 공략")} →</a>' if link else ''
        reward_rows.append(f'<tr id="reward-{id}"><th scope="row">{e(name[k])}</th><td>{e(use[k])} {follow}<small class="routine-citations">{source_links(sources)}</small></td></tr>')

    source_items = ''.join(f'<li id="routine-source-{id}"><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(title[k])} ↗</a><p>{e(scope[k])}</p></li>' for id, (title, url, scope) in SOURCES.items())
    nav_items = [('daily', ('Daily', '매일')), ('banked', ('Banked entries', '충전 콘텐츠')), ('weekly', ('Weekly', '매주')), ('optional', ('Raids & Abyss', '성역·어비스'))]
    return f'''<div class="routine-guide" data-routine-guide>
<div class="routine-intro"><p class="routine-reviewed">{t('Source review', '출처 검토')} · {REVIEWED}</p><p>{t('Start with five Duty Missions, keep energy and tickets from overflowing, then finish the weeklies that fund your next upgrade.', '사명 5회 → 오드·입장권 상한 확인 → 다음 성장에 필요한 주간 숙제 순서로 챙기세요.')}</p><div class="routine-summary"><a href="#routine-daily-dungeon"><strong>{t('Enhance gear', '장비 강화')}</strong><span>{t('Daily Dungeon → stones + Kinah', '일일 던전 → 강화석·키나')} →</span></a><a href="#routine-transcendence"><strong>{t('Grow skills', '스킬 성장')}</strong><span>{t('Transcendence / Nightmare → cards + growth items', '초월·악몽 → 카드·성장 아이템')} →</span></a><a href="#daily-dungeon-choices"><strong>{t('Fill out pet growth', '펫 내실')}</strong><span>{t('Odylium Repository → pet souls', '오디움 저장소 → 펫 영혼')} →</span></a></div></div>
<nav class="rpg-guide-nav" aria-label="{t('Routine sections', '숙제 안내 순서')}">{''.join(f'<a href="#routine-group-{group}">{label[k]}</a>' for group,label in nav_items)}<a href="#reward-uses">{t('Reward uses', '보상 사용처')}</a></nav>
<details class="routine-scope"><summary>{t('KR / Global counts and reset times', '한국·글로벌 횟수와 초기화 시간')}</summary><p>{t('Numbers labelled Global are community/client references reviewed on Oct 9, 2026, including North American service used in Canada. KR examples retain their source date. Membership, events and later patches can change allowances.', '글로벌 표기 숫자는 2026.10.09 확인한 커뮤니티·클라이언트 참고 자료이며, 캐나다에서 이용하는 북미 서비스도 포함합니다. 한국 사례는 출처 날짜를 함께 표시합니다. 멤버십·이벤트·후속 패치에 따라 횟수가 달라질 수 있습니다.')}</p><p>{t('Weeklies are described as Wednesday resets. Use the in-game countdown for your server; Global server-clock timezone is not verified, so this guide does not convert it to local time.', '주간 콘텐츠는 수요일 초기화로 안내됩니다. 실제 시간은 현재 서버의 게임 내 남은 시간으로 확인하세요. 글로벌 서버 시계의 시간대가 검증되지 않아 한국 시간이나 캐나다 시간으로 변환하지 않습니다.')}</p><p>{t('Basic counts, purchased tickets, boss-kill caps and reward claims are separate. These are planning references, not live remaining counts.', '기본 횟수·추가 도전권·보스 처치 제한·보상 수령은 구분해서 봅니다. 아래 숫자는 계획용 참고이며 실시간 잔여 횟수가 아닙니다.')}</p><div class="routine-citations">{source_links(['global', 'kr45'])}</div></details>
{''.join(sections[:3])}
<section class="routine-section" id="daily-dungeon-choices" aria-labelledby="routine-choices-heading"><header><span class="section-kicker">{t('CHOOSE YOUR REWARD', '필요한 보상으로 선택')}</span><h2 id="routine-choices-heading">{t('Which Daily Dungeon should I choose?', '일일 던전 3종, 어디를 갈까?')}</h2><p>{t('All three use the same Unknown Fissure entry pool. The listed maximums require 10,000 score in the cited Global client; your actual score determines the reward.', '3종은 같은 미지의 틈새 입장 횟수를 공유합니다. 아래 최대치는 확인한 글로벌 자료의 1만 점 기준이며, 실제 보상은 점수에 따라 달라집니다.')}</p></header><div class="routine-choices">{''.join(choice_cards)}</div></section>
{sections[3]}
<section class="routine-section" id="reward-uses" aria-labelledby="routine-rewards-heading"><header><span class="section-kicker">{t('AFTER THE RUN', '던전 이후')}</span><h2 id="routine-rewards-heading">{t('Turn the reward into character growth', '받은 보상, 이렇게 성장에 쓰세요')}</h2></header><div class="routine-table routine-use-table"><table><thead><tr><th>{t('Reward', '보상')}</th><th>{t('Next use', '다음에 할 일')}</th></tr></thead><tbody>{''.join(reward_rows)}</tbody></table></div><div class="reference-links"><a href="{r}endgame/#after-story">{t('Post-story growth route', '스토리 이후 내실 순서')} →</a><a href="{r}tools/planner/">{t('Save a personal task', '나의 할 일 적기')} →</a></div></section>
<details class="routine-source-list" id="routine-sources"><summary>{t('Original guides and database references · 14 sources', '원문 공략·데이터 참고 · 출처 14개')}</summary><p>{t('Priorities are our editorial synthesis. Source-based counters and reward types are attributed above; no gameplay completion times or guaranteed drops are assumed.', '우선순위는 자료를 종합한 편집상 제안입니다. 횟수·보상 종류는 각 출처로 연결했습니다. 실제 플레이 시간이나 확정 드롭을 가정하지 않습니다.')}</p><ul>{source_items}</ul></details>
</div>'''

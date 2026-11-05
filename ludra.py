"""NA launch preparation, not a reconstruction of the KR/early-access fight."""
from html import escape

REVIEWED = '2026-11-04'
ENTRY_LEVELS = {'normal': 2800, 'hard': 3000}
TIME_LIMIT_MINUTES = 60
VOUCHERS = {'normal_to_bracelet': 6, 'hard_to_bracelet': 3, 'normal_to_hard': 2}


def table(v, headings, rows):
    labels = [v.p(label) for label in headings]
    head = ''.join('<th scope="col">'+escape(label)+'</th>' for label in labels)
    body = ''
    for row in rows:
        body += '<tr><th scope="row">'+escape(v.p(row[0]))+'</th>'
        body += ''.join('<td data-label="'+escape(label, quote=True)+'">'+escape(v.p(cell))+'</td>'
                        for label, cell in zip(labels[1:], row[1:]))+'</tr>'
    return '<div class="ag-table"><table><thead><tr>'+head+'</tr></thead><tbody>'+body+'</tbody></table></div>'


def note(v, title, text):
    return '<div class="ag-note"><strong>'+escape(v.p(title))+'</strong><p>'+escape(v.p(text))+'</p></div>'


def render(v):
    entry = note(v, ('First visit? Start with Normal', '첫 도전이라면 일반부터'), (
        'Our recommendation: learn with a practice group on Normal, even if you meet the Hard gate. Normal offers the same reward types; Hard has different drop rates and is intended for highly progressed, coordinated Forces. Neither entry level guarantees a clear.',
        '공략 권장: 어려움 입장 수치를 충족해도 일반 연습 파티에서 시작하세요. 일반에서도 같은 종류의 보상을 얻을 수 있습니다. 어려움은 드롭률이 다르고 충분한 성장·숙련·협동을 요구합니다. 입장 수치만으로 클리어가 보장되지는 않습니다.'))
    entry += table(v, [('Mode', '난이도'), ('Entry / limit', '입장 / 제한'), ('Reward choice', '선택 보상')], [
        (('Normal', '일반'), (f"Character item level {ENTRY_LEVELS['normal']:,} · {TIME_LIMIT_MINUTES} minutes", f"캐릭터 아이템 레벨 {ENTRY_LEVELS['normal']:,} · {TIME_LIMIT_MINUTES}분"), ('Gear Change Voucher: Ludra (Bound)', '루드라 일반 전용 교환권(귀속)')),
        (('Hard', '어려움'), (f"Character item level {ENTRY_LEVELS['hard']:,} · {TIME_LIMIT_MINUTES} minutes", f"캐릭터 아이템 레벨 {ENTRY_LEVELS['hard']:,} · {TIME_LIMIT_MINUTES}분"), ('Gear Change Voucher: Ludra (Hard) (Bound)', '루드라 어려움 전용 교환권(귀속)')),
    ])
    entry += '<p>'+v.t('Official NA patch · Sanctuary / Bracelet. The one-hour limit is the run limit, not a verified boss-enrage timer. The gates use your character total, not an individual weapon level.', '북미 공식 패치 · Sanctuary / Bracelet 기준입니다. 1시간은 공략 제한 시간이며 보스 광폭화 시각으로 확인된 값이 아닙니다. 입장 조건은 무기 한 부위의 레벨이 아닌 캐릭터 총 아이템 레벨입니다.')+'</p>'
    entry += '<p>'+v.t('Below 2,800: improve gear first. At 2,800–2,999: Normal is available by item level. At 3,000+: both gates are met; choose Hard after your group is comfortable with the current fight. Confirm unlocks and remaining entries in the NA client.', '2,800 미만이면 먼저 장비를 보강하세요. 2,800~2,999는 일반 아이템 레벨 조건을, 3,000 이상은 두 난도의 아이템 레벨 조건을 충족합니다. 어려움 도전은 파티의 현재 전투 숙련도를 기준으로 결정하세요. 선행 해금과 남은 입장 횟수는 북미 클라이언트에서 확인해야 합니다.')+'</p>'

    prepare = note(v, ('Preparation advice · no verified stat minimums', '준비 권장 사항 · 세부 스탯 하한은 미확인'), (
        'NC has not provided a required gear set, enhancement level, Accuracy target or DPS check. Do not buy a full set just to follow an old KR or Early Access threshold.',
        'NC는 필수 장비 세트·강화 단계·명중 목표·DPS 하한을 제시하지 않았습니다. 한국이나 얼리 액세스의 과거 수치만 보고 장비 세트를 구매하지 마세요.'))
    prepare += v.steps([
        (('Improve the gear you will actually use', '계속 사용할 장비부터 보강'), ('Check your weakest slots, useful options and available enhancement budget. Keep a usable combat build while raising the entry total; compare transfer previews before replacing equipment.', '부족한 부위·유효 옵션·강화 예산을 확인하세요. 입장 수치를 올리면서 실제 전투용 구성을 유지하고, 장비를 바꾸기 전 전승 미리보기를 비교합니다.')),
        (('Prepare skills and supplies', '스킬과 소모품 준비'), ('Review your main skills, Stigma and Arcana bonuses. Put recovery items and defensive skills on accessible keys, and check food/scroll durations in your client. These are preparation suggestions, not confirmed Ludra consumable requirements.', '주력 스킬·스티그마·아르카나 보너스를 점검하세요. 회복 아이템과 방어 스킬을 누르기 편한 위치에 놓고 음식·주문서 지속 시간을 확인합니다. 이는 준비 제안이며 루드라의 필수 소모품 조건은 아닙니다.')),
        (('If you need more materials', '재료가 부족하다면'), ('The November 4 patch raises Exploration rewards in Draupnir, Vakron Sky Island and Ferocious Horn Den. Refining stones and crafting materials match Normal quantities but are Bound. Check the selected dungeon reward screen before spending entries.', '11월 4일 패치는 드라웁니르·바크론 공중섬·흉포한 뿔의 소굴 탐험 보상을 올렸습니다. 연마석·제작 재료는 일반과 같은 수량이지만 귀속입니다. 입장 횟수를 쓰기 전 선택한 던전의 보상 화면을 확인하세요.')),
        (('Agree on a practice plan', '연습 파티의 진행 방식 합의'), ('Choose a caller, clarify tank/healing responsibilities and allow time for retries within the hour. Before entry, check party requirements, reward eligibility and the displayed re-entry/resurrection rules together.', '진행 콜 담당과 탱킹·회복 역할을 정하고 1시간 안에 재도전할 시간을 남기세요. 입장 전 파티 조건·보상 자격·표시된 재입장/부활 규칙을 함께 확인합니다.')),
    ])
    prepare += v.link('guides/gear-targets/', v.t('Choose your next gear upgrade', '다음 장비 성장 선택'))
    prepare += v.link('guides/gear-options/', v.t('Options and transfers', '옵션·계승 준비'))
    prepare += v.link('guides/endgame-crafts/#craft-arcana', v.t('Arcana crafting plan', '아르카나 제작 계획'))

    combat = note(v, ('NA combat patterns: not yet verified', '북미 전투 패턴: 아직 검증되지 않음'), (
        'The official return notice promises new mechanics. The November 4 patch confirms entry, rewards and crafting, but does not document attack cues or counters. This review found KR/Early Access guides, not a verifiable post-update NA combat reference. No boss pattern, damage value, HP trigger, enrage time or revival allowance is asserted here.',
        '공식 재출시 안내는 새 기믹을 예고합니다. 11월 4일 패치는 입장·보상·제작을 확인해 주지만 공격 전조나 대응법은 설명하지 않습니다. 이번 조사에서 한국/얼리 액세스 공략은 찾았지만 업데이트 후 북미 전투를 검증할 자료는 확보하지 못했습니다. 공격 패턴·피해량·체력 발동 구간·광폭화 시각·부활 허용 횟수를 확정하지 않습니다.'))
    combat += v.steps([
        (('Before the first pull', '첫 전투 전'), ('Confirm the region, difficulty and recording date of any video your group uses. Treat older guides as background only; do not assign orb colours, safe tiles or resurrection tactics from them as NA rules.', '파티가 참고하는 영상의 지역·난도·촬영 날짜를 확인하세요. 과거 공략은 배경 참고로만 보고, 구슬 색·안전 칸·부활 전술을 북미 확정 규칙으로 배정하지 마세요.')),
        (('During practice', '연습 중'), ('Use the current on-screen warnings and your caller. If the group fails, record the warning, boss HP, player positions and outcome before changing one response at a time. This is a learning method, not a proven counter.', '현재 화면의 경고와 파티 콜을 기준으로 움직이세요. 실패했다면 경고 문구·보스 체력·파티 위치·결과를 기록하고 대응을 하나씩 바꿔봅니다. 이는 학습 방법이며 검증된 패턴 대응법은 아닙니다.')),
    ])
    combat += '<p>'+v.t('Still open: NA attack sequence and cues, safe positions, difficulty-specific mechanics, resurrection/re-entry rules, entry costs and weekly reward limits. Do not assume unlimited revives or a fixed number of clears to finish a bracelet.', '남은 확인 항목: 북미 공격 순서·전조·안전 위치·난도별 기믹·부활/재입장 규칙·입장 비용·주간 보상 한도. 무제한 부활이나 팔찌 완성에 필요한 고정 클리어 횟수를 가정하지 마세요.')+'</p>'

    rewards = table(v, [('Goal', '목표'), ('Confirmed route', '확인된 획득 경로'), ('Before spending', '소비 전 확인')], [
        (('Abyssal Bracelet (Bound)', '심연의 팔찌 (Abyssal Bracelet, 귀속)'), ('Chance drop in Normal and Hard; Amplify cap 3.', '일반·어려움 확률 획득, 돌파 상한 3.'), ('No published probability; not guaranteed per clear.', '확률은 미공개이며 매 클리어 확정 드롭이 아닙니다.')),
        (("Ludra’s Bracelet (Bound)", '루드라의 팔찌 (귀속)'), ('Substance Morph using difficulty-specific vouchers; Amplify cap 5.', '난도별 전용 교환권을 물질 변환, 돌파 상한 5.'), ('Keep the correct voucher type; see the recipe below.', '교환권 종류를 확인하고 아래 변환식을 따릅니다.')),
        (('Weapon / Guard', '무기 / 가더'), ('Ludra weapon and Guard (Bound) are listed rewards. A Gear Change Voucher can morph into an Abyssal Forge: Weapon Selection Chest (Bound).', '루드라 무기·가더(귀속)가 보상에 포함됩니다. 장비 교환권으로 Abyssal Forge: Weapon Selection Chest(귀속)를 물질 변환할 수 있습니다.'), ('The patch does not specify the weapon-chest voucher quantity or full cost.', '무기 선택 상자의 교환권 수량·전체 비용은 공지에 없습니다.')),
        (('Wings / artwork', '날개 / 명화'), ('Sealed Abyssal Waves Wings; Artwork: Abyssal Ludra.', 'Sealed Abyssal Waves Wings, Artwork: Abyssal Ludra.'), ('Listed rewards, not a promise of every item each run.', '보상 목록이며 매번 전부 지급한다는 의미는 아닙니다.')),
    ])
    rewards += note(v, ('Choose a reward for your next upgrade', '다음 성장 목표에 맞춰 보상 선택'), (
        'Both modes offer a Gear Change Voucher as a guaranteed-reward choice, including the mode-specific Ludra voucher. For a bracelet goal, check that exact name before selecting. The patch gives no per-run voucher count or reward cadence, so 6 vouchers does not mean 6 clears. Different drop rates do not establish which mode is more efficient for your group.',
        '두 난도 모두 확정 보상에서 장비 교환권을 선택할 수 있으며 난도별 루드라 전용 교환권도 안내돼 있습니다. 팔찌가 목표라면 선택 전에 정확한 이름을 확인하세요. 공지는 회당 수량·확정 보상 주기를 제시하지 않으므로 교환권 6개가 6회 클리어를 뜻하지 않습니다. 드롭률이 다르다는 사실만으로 파티별 효율을 계산할 수는 없습니다.'))
    rewards += '<p>'+v.t('Optional event goal: a Normal or Hard clear during November 4 after maintenance–November 24 before maintenance (PST) qualifies for Ludra Hunt recognition. The universal title is Ludra’s Nemesis; ranked titles are for the first 20 Hard-clear Forces per listed region, including NA East and NA West separately. Do not choose Hard solely for the universal title.', '기간 한정 목표: PST 기준 11월 4일 점검 후~11월 24일 점검 전 일반 또는 어려움 클리어는 루드라 사냥 이벤트 대상입니다. 공통 칭호는 Ludra’s Nemesis이며, 순위 칭호는 NA East·NA West를 각각 포함한 대상 지역별 어려움 선착순 20개 공격대 대상입니다. 공통 칭호만을 위해 어려움을 고를 필요는 없습니다.')+'</p>'

    materials = table(v, [('Input (Bound)', '재료 (귀속)'), ('Result (Bound)', '결과 (귀속)')], [
        ((f"Gear Change Voucher: Ludra ×{VOUCHERS['normal_to_bracelet']}", f"루드라 일반 전용 교환권 ×{VOUCHERS['normal_to_bracelet']}"), ("Ludra’s Bracelet ×1", '루드라의 팔찌 ×1')),
        ((f"Gear Change Voucher: Ludra (Hard) ×{VOUCHERS['hard_to_bracelet']}", f"루드라 어려움 전용 교환권 ×{VOUCHERS['hard_to_bracelet']}"), ("Ludra’s Bracelet ×1", '루드라의 팔찌 ×1')),
        ((f"Gear Change Voucher: Ludra ×{VOUCHERS['normal_to_hard']}", f"루드라 일반 전용 교환권 ×{VOUCHERS['normal_to_hard']}"), ('Gear Change Voucher: Ludra (Hard) ×1', '루드라 어려움 전용 교환권 ×1')),
    ])
    materials += '<p>'+v.t('These are the published voucher conversions, not complete currency-cost quotes. Six Normal vouchers also convert to three Hard vouchers, so there is no voucher saving from that detour; compare any added costs in the live preview. No reverse conversion is confirmed. Do not import the old 5,000,000 Kina recipe into this NA plan.', '위 표는 공지된 교환권 변환식이며 재화 비용 전체를 확정한 견적이 아닙니다. 일반 6개를 어려움 3개로 바꿔도 교환권 수량상 절약은 없으므로 실제 미리보기의 추가 비용을 비교하세요. 역방향 변환은 확인되지 않았습니다. 과거 5,000,000 키나 레시피를 이 북미 계획에 적용하지 마세요.')+'</p>'
    materials += table(v, [('Crafting choice', '장비 제작 선택'), ('What you trade off', '성공·보너스·귀속')], [
        (('New True Dragon / Star Dragon recipe', '신규 True Dragon / Star Dragon (진룡 / 성룡) 제작식'), ('100% success; no COMBO (Great Success); output is Bound. Bound or Unbound Artisan-to-Epic gear may be used as material.', '성공률 100%, COMBO(대성공) 없음, 결과물 귀속. 귀속·비귀속 Artisan~Epic 장비를 재료로 사용할 수 있습니다.')),
        (('Existing recipes', '기존 제작식'), ('Unchanged: failure risk remains, with the possibility of COMBO and tradable gear.', '변경 없음: 실패 위험이 있으며 대성공과 거래 가능한 장비 획득 가능성이 있습니다.')),
    ])
    materials += note(v, ('A preparation option, not a Ludra drop recipe', '준비 장비의 선택지이며 루드라 드롭 제작식은 아님'), (
        'The guaranteed Dragon recipes can help plan a predictable gear upgrade. They do not make Ludra rewards guaranteed. NC has not listed full ingredient quantities here: inspect the recipe, total Kina, binding and transfer result before consuming gear. Keep useful spare gear until you have checked its material eligibility.',
        '용계 장비의 확정 제작식은 장비 성장 계획의 선택지입니다. 루드라 보상까지 확정으로 바꾸지는 않습니다. 공지에 전체 재료 수량이 없으므로 제작 화면의 재료·총 키나·귀속·전승 결과를 확인한 뒤 장비를 소비하세요. 쓸 만한 여분 장비는 제작 재료 가능 여부를 확인할 때까지 남겨두세요.'))
    materials += v.link('guides/endgame-crafts/', v.t('Continue to endgame crafting goals', '엔드게임 제작 목표로 이어보기'))
    materials += v.link('guides/kinah-farming/', v.t('Plan the material and Kina budget', '재료·키나 예산 준비'))
    materials += '<p class="ag-small">'+v.t('Item names follow the English NA notice. Korean names are reading aids, not a separate claim about KR-server recipes.', '아이템명은 북미 영문 공지를 기준으로 합니다. 한국어 명칭은 이해를 돕는 번역이며 한국 서버 제작식의 적용을 뜻하지 않습니다.')+'</p>'

    sections = [
        ('entry', ('Choose difficulty', '난이도 선택'), ('Enter with a realistic goal', '첫 도전 목표와 입장 조건'), entry),
        ('prepare', ('Gear & party', '장비·파티 준비'), ('Before you spend an entry', '입장 횟수를 쓰기 전에'), prepare),
        ('combat', ('Combat status', '전투 확인 범위'), ('Learn the current NA fight', '현재 북미 전투를 배우는 기준'), combat),
        ('rewards', ('Choose rewards', '보상 선택'), ('Turn a clear into your next upgrade', '클리어 보상을 다음 성장으로'), rewards),
        ('materials', ('Vouchers & crafts', '교환권·제작'), ('Keep the right materials', '필요한 재료를 남기고 변환하기'), materials),
    ]
    return [((key, label), v.section('ludra-'+key, title, body)) for key, label, title, body in sections], ['ludra-na-patch', 'ludra-na-current']

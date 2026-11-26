"""NA launch preparation, not a reconstruction of the KR/early-access fight."""
from html import escape

REVIEWED = '2026-11-26'
ENTRY_LEVELS = {'easy': 2800, 'normal': 2800, 'hard': 3000}
TIME_LIMIT_MINUTES = 120
VOUCHERS = {'normal_to_bracelet': 6, 'hard_to_bracelet': 3, 'normal_to_hard': 2}
WEAPON_CHEST = {'kina': 5_000_000, 'easy_vouchers': 4, 'normal_vouchers': 2, 'hard_vouchers': 1}
GEAR_COMBINED_DROP_PERCENT = 15


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
    entry = note(v, ('First visit? Start with Easy', '첫 도전이라면 쉬움부터'), (
        'Our recommendation: learn with a practice group on Easy, even if you meet the Normal or Hard gate. Easy has Normal-mode HP, easier mechanics and unlimited personal revives. An entry level still does not guarantee a clear.',
        '공략 권장: 일반·어려움 입장 수치를 충족해도 쉬움 연습 파티에서 시작하세요. 쉬움은 일반과 같은 HP에 더 쉬운 기믹과 개인 부활 무제한을 적용합니다. 입장 수치만으로 클리어가 보장되지는 않습니다.'))
    entry += table(v, [('Mode', '난이도'), ('Entry / limit', '입장 / 제한'), ('Reward choice', '선택 보상')], [
        (('Easy', '쉬움'), (f"Character item level {ENTRY_LEVELS['easy']:,} · {TIME_LIMIT_MINUTES} minutes · unlimited personal revives", f"캐릭터 아이템 레벨 {ENTRY_LEVELS['easy']:,} · {TIME_LIMIT_MINUTES}분 · 개인 부활 무제한"), ('Ludra Weapon / Guard (Bound)', '루드라 무기 / 가더(귀속)')),
        (('Normal', '일반'), (f"Character item level {ENTRY_LEVELS['normal']:,} · {TIME_LIMIT_MINUTES} minutes", f"캐릭터 아이템 레벨 {ENTRY_LEVELS['normal']:,} · {TIME_LIMIT_MINUTES}분"), ('Gear Change Voucher: Ludra (Bound)', '루드라 일반 전용 교환권(귀속)')),
        (('Hard', '어려움'), (f"Character item level {ENTRY_LEVELS['hard']:,} · {TIME_LIMIT_MINUTES} minutes", f"캐릭터 아이템 레벨 {ENTRY_LEVELS['hard']:,} · {TIME_LIMIT_MINUTES}분"), ('Gear Change Voucher: Ludra (Hard) (Bound)', '루드라 어려움 전용 교환권(귀속)')),
    ])
    entry += '<p>'+v.t('Official NA patch · Sanctuary. The November 18 patch adds Easy while retaining the two-hour limit established on November 11. This is not a verified boss-enrage timer. The gates use your character total, not an individual weapon level.', '북미 공식 패치 · Sanctuary 기준입니다. 11월 18일 패치는 11월 11일에 정해진 2시간 제한을 유지하며 쉬움을 추가합니다. 이는 보스 광폭화 시각으로 확인된 값이 아닙니다. 입장 조건은 무기 한 부위의 레벨이 아닌 캐릭터 총 아이템 레벨입니다.')+'</p>'
    entry += '<p>'+v.t('Below 2,800: improve gear first. At 2,800–2,999: Easy and Normal meet the published item-level gate. At 3,000+: all three gates are met; choose Normal or Hard after your group is comfortable with the current fight. Confirm unlocks and remaining entries in the NA client.', '2,800 미만이면 먼저 장비를 보강하세요. 2,800~2,999는 쉬움·일반의 공식 아이템 레벨 조건을 충족합니다. 3,000 이상은 세 난도의 조건을 충족하며 현재 전투에 익숙해진 뒤 일반·어려움을 선택하세요. 선행 해금과 남은 입장 횟수는 북미 클라이언트에서 확인해야 합니다.')+'</p>'

    prepare = note(v, ('Preparation advice · no verified stat minimums', '준비 권장 사항 · 세부 스탯 하한은 미확인'), (
        'NC has not provided a required gear set, enhancement level, Accuracy target or DPS check. Do not buy a full set just to follow an old KR or Early Access threshold.',
        'NC는 필수 장비 세트·강화 단계·명중 목표·DPS 하한을 제시하지 않았습니다. 한국이나 얼리 액세스의 과거 수치만 보고 장비 세트를 구매하지 마세요.'))
    prepare += v.steps([
        (('Improve the gear you will actually use', '계속 사용할 장비부터 보강'), ('Check your weakest slots, useful options and available enhancement budget. Keep a usable combat build while raising the entry total; compare transfer previews before replacing equipment.', '부족한 부위·유효 옵션·강화 예산을 확인하세요. 입장 수치를 올리면서 실제 전투용 구성을 유지하고, 장비를 바꾸기 전 전승 미리보기를 비교합니다.')),
        (('Prepare skills and supplies', '스킬과 소모품 준비'), ('Review your main skills, Stigma and Arcana bonuses. Put recovery items and defensive skills on accessible keys, and check food/scroll durations in your client. These are preparation suggestions, not confirmed Ludra consumable requirements.', '주력 스킬·스티그마·아르카나 보너스를 점검하세요. 회복 아이템과 방어 스킬을 누르기 편한 위치에 놓고 음식·주문서 지속 시간을 확인합니다. 이는 준비 제안이며 루드라의 필수 소모품 조건은 아닙니다.')),
        (('If you need more materials', '재료가 부족하다면'), ('The November 4 patch raises Exploration rewards in Draupnir, Vakron Sky Island and Ferocious Horn Den. Refining stones and crafting materials match Normal quantities but are Bound. Check the selected dungeon reward screen before spending entries.', '11월 4일 패치는 드라웁니르·바크론 공중섬·흉포한 뿔의 소굴 탐험 보상을 올렸습니다. 연마석·제작 재료는 일반과 같은 수량이지만 귀속입니다. 입장 횟수를 쓰기 전 선택한 던전의 보상 화면을 확인하세요.')),
        (('Agree on a practice plan', '연습 파티의 진행 방식 합의'), ('Choose a caller, clarify tank/healing responsibilities and allow time for retries within the two-hour run limit. Before entry, check party requirements, reward eligibility and the displayed re-entry/resurrection rules together.', '진행 콜 담당과 탱킹·회복 역할을 정하고 2시간 제한 안에 재도전할 시간을 남기세요. 입장 전 파티 조건·보상 자격·표시된 재입장/부활 규칙을 함께 확인합니다.')),
    ])
    prepare += v.link('guides/gear-targets/', v.t('Choose your next gear upgrade', '다음 장비 성장 선택'))
    prepare += v.link('guides/gear-options/', v.t('Options and transfers', '옵션·계승 준비'))
    prepare += v.link('guides/endgame-crafts/#craft-arcana', v.t('Arcana crafting plan', '아르카나 제작 계획'))

    combat = note(v, ('NA combat patterns: not yet verified', '북미 전투 패턴: 아직 검증되지 않음'), (
        'The November 18 patch says some Ludra attack patterns are fixed and Easy has easier mechanics, but it does not name the patterns, triggers, cues or counters. This review found no verifiable post-update NA attack-by-attack reference. Easy’s unlimited personal revives are official; no Normal/Hard revival allowance, damage value, HP trigger or enrage time is asserted here.',
        '11월 18일 패치는 일부 루드라 공격 패턴을 수정하고 쉬움 기믹을 완화했다고 밝히지만 패턴명·발동·전조·대응법은 공개하지 않습니다. 업데이트 후 북미 공격별 공략을 검증할 자료도 확보하지 못했습니다. 쉬움의 개인 부활 무제한만 공식이며 일반/어려움 부활 횟수·피해량·체력 발동 구간·광폭화 시각은 확정하지 않습니다.'))
    combat += v.steps([
        (('Before the first pull', '첫 전투 전'), ('Confirm the region, difficulty and recording date of any video your group uses. Treat older guides as background only; do not assign orb colours, safe tiles or resurrection tactics from them as NA rules.', '파티가 참고하는 영상의 지역·난도·촬영 날짜를 확인하세요. 과거 공략은 배경 참고로만 보고, 구슬 색·안전 칸·부활 전술을 북미 확정 규칙으로 배정하지 마세요.')),
        (('During practice', '연습 중'), ('Use the current on-screen warnings and your caller. If the group fails, record the warning, boss HP, player positions and outcome before changing one response at a time. This is a learning method, not a proven counter.', '현재 화면의 경고와 파티 콜을 기준으로 움직이세요. 실패했다면 경고 문구·보스 체력·파티 위치·결과를 기록하고 대응을 하나씩 바꿔봅니다. 이는 학습 방법이며 검증된 패턴 대응법은 아닙니다.')),
    ])
    combat += '<p>'+v.t('Still open: NA attack sequence and cues, safe positions, the exact Easy changes, Normal/Hard resurrection and re-entry rules, entry costs and weekly reward limits. Easy alone has confirmed unlimited personal revives; do not infer that rule for Normal or Hard.', '남은 확인 항목: 북미 공격 순서·전조·안전 위치·쉬움의 정확한 변경, 일반/어려움 부활·재입장 규칙, 입장 비용·주간 보상 한도. 개인 부활 무제한은 쉬움에만 확인됐으며 일반·어려움으로 확대 적용하지 않습니다.')+'</p>'

    rewards = table(v, [('Goal', '목표'), ('Confirmed route', '확인된 획득 경로'), ('Before spending', '소비 전 확인')], [
        (('Abyssal Bracelet (Bound)', '심연의 팔찌 (Abyssal Bracelet, 귀속)'), ('Chance drop in Normal and Hard; Amplify cap 3.', '일반·어려움 확률 획득, 돌파 상한 3.'), ('No published probability; not guaranteed per clear.', '확률은 미공개이며 매 클리어 확정 드롭이 아닙니다.')),
        (("Ludra’s Bracelet (Bound)", '루드라의 팔찌 (귀속)'), ('Substance Morph using difficulty-specific vouchers; Amplify cap 5.', '난도별 전용 교환권을 물질 변환, 돌파 상한 5.'), ('Keep the correct voucher type; see the recipe below.', '교환권 종류를 확인하고 아래 변환식을 따릅니다.')),
        (('Weapon / Guard', '무기 / 가더'), (f'Ludra weapon and Guard (Bound) use a {GEAR_COMBINED_DROP_PERCENT}% combined rate on Easy, Normal and Hard. A difficulty voucher can morph into a weapon-selection chest.', f'루드라 무기·가더(귀속)는 쉬움·일반·어려움에서 합산 {GEAR_COMBINED_DROP_PERCENT}%입니다. 난도별 교환권으로 무기 선택 상자를 물질 변환할 수 있습니다.'), ('Combined rate is not a per-item guarantee; check the reward and morph previews.', '합산 확률은 개별 아이템 보장이 아니므로 보상·변환 미리보기를 확인합니다.')),
        (('Wings / artwork', '날개 / 명화'), ('Sealed Abyssal Waves Wings; Artwork: Abyssal Ludra.', 'Sealed Abyssal Waves Wings, Artwork: Abyssal Ludra.'), ('Listed rewards, not a promise of every item each run.', '보상 목록이며 매번 전부 지급한다는 의미는 아닙니다.')),
    ])
    rewards += note(v, ('Choose a reward for your next upgrade', '다음 성장 목표에 맞춰 보상 선택'), (
        'Normal and Hard offer a Gear Change Voucher as a guaranteed-reward choice, including the mode-specific Ludra voucher. For a bracelet goal, check that exact name before selecting. The patch gives no per-run voucher count or reward cadence, so 6 vouchers does not mean 6 clears. The 15% combined gear rate does not establish which mode is most efficient for your group.',
        '일반·어려움은 확정 보상에서 장비 교환권을 선택할 수 있으며 난도별 루드라 전용 교환권도 안내돼 있습니다. 팔찌가 목표라면 선택 전에 정확한 이름을 확인하세요. 공지는 회당 수량·확정 보상 주기를 제시하지 않으므로 교환권 6개가 6회 클리어를 뜻하지 않습니다. 합산 15%만으로 파티별 최적 난도를 정할 수는 없습니다.'))
    rewards += note(v, ('November 11 · Reward Group 5', '11월 11일 · 보상군 5'), (
        'The official drop rate for Reward Group 5 rises from 30% to 100%, and Wrathful Mind, Wrathful Will and Wrathful Ego (Bound) are added. The patch does not publish the quantity per clear or say that every item in the group drops together.',
        '보상군 5의 공식 드롭률은 30%에서 100%로 오르고 격노의 마음·의지·자아(귀속)가 추가됩니다. 공지는 회당 수량이나 보상군의 모든 아이템이 함께 지급되는지 공개하지 않았습니다.'))
    rewards += '<p>'+v.t('Updated event goal: the November 26 notice extends Normal/Hard clear eligibility for the Ludra’s Nemesis title through December 15 before maintenance (PST). Teams linked to RMT were removed from Ludra Hunt rankings, so ranked-title places are open again; final rankings are published after the event and RMT review. Hall of Fame review is separate: remaining teams are final victors after RMT-linked teams were removed. Do not choose Hard solely for the universal clear title.', '갱신된 기간 한정 목표: 11월 26일 공지는 일반·어려움 클리어의 Ludra’s Nemesis 칭호 기간을 PST 기준 12월 15일 점검 전까지 연장합니다. RMT 연관 팀을 루드라 사냥 순위에서 제외해 순위 칭호 자리가 다시 열렸고 최종 순위는 이벤트 종료와 RMT 검토 뒤 발표됩니다. 명예의 전당은 별도이며 RMT 연관 팀 제외 뒤 남은 팀이 최종 우승 팀입니다. 공통 클리어 칭호만을 위해 어려움을 고를 필요는 없습니다.')+'</p>'

    materials = table(v, [('Input (Bound)', '재료 (귀속)'), ('Result (Bound)', '결과 (귀속)')], [
        ((f"Gear Change Voucher: Ludra [Easy] ×{WEAPON_CHEST['easy_vouchers']} + {WEAPON_CHEST['kina']:,} Kina", f"루드라 쉬움 장비 변경권 ×{WEAPON_CHEST['easy_vouchers']} + {WEAPON_CHEST['kina']:,} 키나"), ('Abyssal Forge: Weapon Selection Chest ×1', '심연의 재련: 무기 선택 상자 ×1')),
        ((f"Gear Change Voucher: Ludra [Normal] ×{WEAPON_CHEST['normal_vouchers']} + {WEAPON_CHEST['kina']:,} Kina", f"루드라 일반 장비 변경권 ×{WEAPON_CHEST['normal_vouchers']} + {WEAPON_CHEST['kina']:,} 키나"), ('Abyssal Forge: Weapon Selection Chest ×1', '심연의 재련: 무기 선택 상자 ×1')),
        ((f"Gear Change Voucher: Ludra [Hard] ×{WEAPON_CHEST['hard_vouchers']} + {WEAPON_CHEST['kina']:,} Kina", f"루드라 어려움 장비 변경권 ×{WEAPON_CHEST['hard_vouchers']} + {WEAPON_CHEST['kina']:,} 키나"), ('Abyssal Forge: Weapon Selection Chest ×1', '심연의 재련: 무기 선택 상자 ×1')),
        ((f"Gear Change Voucher: Ludra ×{VOUCHERS['normal_to_bracelet']}", f"루드라 일반 전용 교환권 ×{VOUCHERS['normal_to_bracelet']}"), ("Ludra’s Bracelet ×1", '루드라의 팔찌 ×1')),
        ((f"Gear Change Voucher: Ludra (Hard) ×{VOUCHERS['hard_to_bracelet']}", f"루드라 어려움 전용 교환권 ×{VOUCHERS['hard_to_bracelet']}"), ("Ludra’s Bracelet ×1", '루드라의 팔찌 ×1')),
        ((f"Gear Change Voucher: Ludra ×{VOUCHERS['normal_to_hard']}", f"루드라 일반 전용 교환권 ×{VOUCHERS['normal_to_hard']}"), ('Gear Change Voucher: Ludra (Hard) ×1', '루드라 어려움 전용 교환권 ×1')),
    ])
    materials += '<p>'+v.t('The first three rows are the November 18 weapon-chest recipes: 5,000,000 Kina plus one difficulty-specific voucher amount. Bracelet conversions below retain their earlier source and may have other live costs; compare every preview before spending. Players who used a Hard weapon voucher before the adjustment are due one Hard voucher retroactively.', '앞의 세 줄은 11월 18일 무기 상자 도안으로 5,000,000 키나와 난도별 교환권 수량을 사용합니다. 아래 팔찌 변환은 기존 출처를 유지하며 실제 추가 비용이 있을 수 있으므로 소비 전 모든 미리보기를 확인하세요. 조정 전에 어려움 무기 교환권을 사용한 이용자는 어려움 교환권 1개를 소급 지급받습니다.')+'</p>'
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
    return [((key, label), v.section('ludra-'+key, title, body)) for key, label, title, body in sections], ['ludra-na-patch', 'ludra-na-nov11-patch', 'ludra-na-previous-patch', 'ludra-na-current', 'ludra-na-event-update']

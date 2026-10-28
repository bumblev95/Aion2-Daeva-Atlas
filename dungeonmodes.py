"""NA official rules, separate from existing Normal/KR encounter evidence."""
from html import escape as e

REVIEWED = '2026-10-28'
SOURCE = 'https://aion2.plaync.com/en-us/board/update/view?articleId=6ae19668577e8c01355e0210'
SOURCE_HASH = 'd9c652647a7b76997da54a193ae5e0c38c1d67842437fb17be46651ea2a8f794'
BOSSES = {'auldor': 'Urugugu', 'vakron': 'Vakron'}


def render(lang, base, boss):
    if boss not in BOSSES:
        return ''
    t = lambda en, ko: ko if lang == 'ko' else en
    root = base + ('ko/' if lang == 'ko' else '')
    fragment = BOSSES[boss]
    rows = [
        (t('Entry', '입장'),
         t('Legacy reference: Lv. 45 / total 1,400. Reviewed Oct 12; not newly confirmed by this patch.', '기존 자료: 45레벨 / 종합 1,400. 10월 12일 검토값이며 이번 공지가 재확인한 수치는 아닙니다.'),
         t('Official: item level 2,700. Other unlock requirements need a live check.', '공식: 아이템 레벨 2,700. 추가 해금 조건은 게임에서 확인해야 합니다.')),
        (t('Boss Attack', '보스 공격력'), t('−15% from previous Normal values.', '기존 일반 수치 대비 −15%.'), t('−10% from previous Hard values (category-wide adjustment).', '기존 어려움 수치 대비 −10% (난도 전체 조정).')),
        (t('Boss Damage Boost', '보스 피해 증폭'), t('No change specified here.', '이번 공지에 변경 수치 없음.'), t('−10% from previous Hard values.', '기존 어려움 수치 대비 −10%.')),
        (t('Boss HP', '보스 HP'), t('No Expedition HP change specified.', '원정 HP 변경 수치 없음.'), t('No Expedition HP change specified. −6.5% is for Transcendence stages 1–2 only.', '원정 HP 변경 수치 없음. −6.5%는 초월 1~2단계만 해당.')),
        (t('Frenzy', '광폭화'), t('Normal timer not specified in this notice.', '이번 공지에 일반 타이머 미기재.'), t('Official: 4 minutes. Timer start and encounter behavior await live verification.', '공식: 4분. 시간 측정 시작점·실제 발동은 실전 검증 대기.')),
        (t('Revives', '부활'), t('Normal limit not specified in this notice.', '이번 공지에 일반 제한 미기재.'), t('Official: 3 per player, not 3 for the party. Retry reset bug fixed; wipe/re-entry behavior awaits verification.', '공식: 파티 합산이 아닌 개인별 3회. 재도전 초기화 오류 수정 공지; 전멸·재입장 동작은 검증 대기.')),
        (t('Patterns / damage', '패턴 / 실제 피해'), t('Existing lessons retained with their original region and evidence limits.', '기존 설명의 지역·검증 범위와 애니메이션을 보존.'), t('Unverified: new patterns, order, timings, hit damage and practical difficulty. Normal animations are not Hard instructions.', '미검증: 추가 패턴·순서·타이밍·피해량·체감 난도. 일반 애니메이션을 어려움 대응법으로 사용하지 마세요.')),
        (t('Rewards', '보상'), t('Existing loot targets below are legacy references. No new Normal reward table is supplied.', '아래 기존 목표 보상은 이전 참고자료입니다. 새 일반 보상표는 공개되지 않았습니다.'), t('Official additions below. More Kina than Normal; no amount or drop rate stated.', '아래 공식 추가 보상 참고. 일반보다 키나 증가; 수량·확률 미공개.')),
    ]
    headers = [t('Compare', '비교 항목'), t('Normal · existing guide', '일반 · 기존 공략'), t('Hard · NA official rules', '어려움 · 북미 공식 규칙')]
    table = ''.join('<tr>' + f'<th scope="row">{e(label)}</th>' + ''.join(f'<td data-label="{e(head)}">{e(value)}</td>' for head, value in zip(headers[1:], [normal, hard])) + '</tr>' for label, normal, hard in rows)
    rewards = [
        t(f'Guaranteed dungeon-specific Ariel Fragment: {fragment} (Bound).', f'해당 던전의 Ariel Fragment: {fragment} (귀속) 확정 보상.'),
        t('Philosopher’s Stone: Revelation (Bound): random reward opportunity and a guaranteed selectable reward option. Do not assume both are paid on every clear.', '계시의 현자의 돌(귀속): 확률 획득 및 확정 선택 보상 항목. 매 클리어마다 두 경로를 모두 받는다고 해석하지 마세요.'),
        t('Expedition Hero Artwork: chance reward. More Kina than Normal; exact amounts and rates are not announced.', 'Expedition Hero Artwork: 확률 보상. 일반보다 키나 증가; 정확한 수량·확률 미공개.'),
        t('Unique materials: Wrathful Mind, Wrathful Will and Wrathful Ego can be obtained. Unique Skins require Hard Expedition achievements, not merely a random boss drop.', '유일 제작 재료 Wrathful Mind·Wrathful Will·Wrathful Ego 획득 가능. 유일 외형은 원정 어려움 업적 완료 보상이며 단순 보스 드롭으로 표시하지 않습니다.'),
        t('Substance Morph: 100 fragments → 1 Daevanion Crystal: Ariel (Bound), up to 30 times per character; 1 fragment → 5 Enhance Stones, with no conversion-count limit. Menus: Special → Daevanion / Consumables.', '물질 변환: 조각 100개 → Daevanion Crystal: Ariel(귀속) 1개, 캐릭터당 최대 30회. 조각 1개 → 강화석 5개는 변환 횟수 제한 없음. 메뉴: Special → Daevanion / Consumables.'),
    ]
    return f'''<section class="dungeon-modes" id="difficulty" aria-labelledby="difficulty-title" data-dungeon-modes data-region="NA" data-reviewed="{REVIEWED}">
<span class="section-kicker">NA · 2026-10-28</span><h2 id="difficulty-title">{t('Normal or Hard? Check before entering', '일반과 어려움, 입장 전에 확인하세요')}</h2>
<p>{t('Applies to North America. Official notice: Oct 27 PDT / Oct 28 CET update, reviewed Oct 28. Korean text here is a translation of NA rules, not confirmation for Korean servers.', '북미 적용. 공식 공지 제목: 10월 27일 PDT / 28일 CET 업데이트, 10월 28일 검토. 한국어 페이지도 북미 규칙을 번역한 것이며 한국 서버 적용을 뜻하지 않습니다.')}</p>
<div class="mode-facts"><div><small>{t('HARD ENTRY', '어려움 입장')}</small><strong>2,700</strong><span>{t('Item level', '아이템 레벨')}</span></div><div><small>{t('FRENZY TIMER', '광폭화 타이머')}</small><strong>4:00</strong><span>{t('Official rule · trigger untested', '공식 규칙 · 실전 발동 미검증')}</span></div><div><small>{t('PERSONAL REVIVES', '개인별 부활')}</small><strong>3</strong><span>{t('Per player', '플레이어마다')}</span></div></div>
<p class="mode-warning">{t('Percentages compare each mode with its own previous values. They do not show Hard versus Normal damage. Actual incoming damage and clear difficulty are not measured.', '감소율은 각 난도의 기존 수치 대비입니다. 어려움과 일반 사이의 피해량 비율이 아닙니다. 실제 받는 피해와 클리어 난도는 측정하지 않았습니다.')}</p>
<table><caption>{t('Official changes and limits of the existing guide', '공식 변경과 기존 공략의 검증 범위')}</caption><thead><tr>{''.join(f'<th scope="col">{h}</th>' for h in headers)}</tr></thead><tbody>{table}</tbody></table>
<details class="mode-rewards" open><summary>{t('Hard rewards · guaranteed, chance and achievement', '어려움 보상 · 확정 / 확률 / 업적 구분')}</summary><ul>{''.join(f'<li>{e(r)}</li>' for r in rewards)}</ul></details>
<details class="mode-pending"><summary>{t('Still needs a North America gameplay check', '북미 실전 확인이 필요한 항목')}</summary><p>{t('Record the server/date and selected difficulty, entry screen and prerequisites, a full boss attempt, Frenzy start, personal revive counter before/after a wipe and re-entry, and the reward selection screen. Check reward eligibility, energy/entry consumption, quantities, binding and morph limits. Do not infer extra patterns, hit damage or a recommended DPS from the four-minute timer.', '서버·날짜·선택 난도, 입장 화면과 선행조건, 보스전 전체, 광폭화 시작, 전멸·재입장 전후 개인 부활 횟수, 보상 선택 화면을 확인해야 합니다. 보상 자격·오드/입장 차감·수량·귀속·변환 제한도 대조해야 합니다. 4분 타이머만으로 추가 패턴·피해량·권장 DPS를 추정하지 않습니다.')}</p></details>
<p class="mode-source"><a href="{SOURCE}" target="_blank" rel="noopener noreferrer">NC · {t('Official patch source', '공식 패치 원문')} ↗</a> · <a href="{root}updates/na-6ae19668577e8c01355e0210/">{t('Bilingual patch review', '한영 패치 검토')}</a><small>{t('Source revision', '원문 수정')} 2026-10-28 07:25:01 UTC · SHA-256 {SOURCE_HASH}</small></p>
</section><div class="mode-legacy" id="existing-guide"><h2>{t('Existing guide · original evidence preserved', '기존 공략 · 원래 근거와 애니메이션 보존')}</h2><p>{t('The material below is not a verified NA Hard walkthrough. Vakron’s Global Normal supplement and the separately labelled KR patterns retain their original review dates.', '아래는 북미 어려움 실전 검증 공략이 아닙니다. 바크론 글로벌 일반 보강 자료와 별도 표시된 한국판 패턴의 원래 검토 날짜를 유지합니다.')}</p></div>'''

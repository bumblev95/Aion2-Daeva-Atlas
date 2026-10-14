"""Reviewed Global transfer guidance; never infer live availability from a clock."""
from html import escape as e
import json
from pathlib import Path

ROOT = 'guides/server-transfer/'
REVIEWED = '2026-10-13'
TITLE = ('Global server transfer: prepare before you move', '글로벌 서버 이전: 옮기기 전 확인할 것')
DESCRIPTION = ('Official transfer dates, regional hours, Quna costs and a pre-transfer checklist.', '공식 이전 기간·지역별 신청 시간·Quna 비용과 이전 전 체크리스트.')
SOURCES = {
    'qa': ('NC · Server Transfer Q&A · updated October 13', 'https://lounge.plaync.com/feed/83614?country=US&locale=en-US'),
    'products': ('NC · Server Transfer Products · updated October 13', 'https://aion2.plaync.com/en-us/board/notice/view?articleId=6ac932a8fa34c1011d627bc9'),
    'maintenance': ('NC · October 13/14 game maintenance', 'https://aion2.plaync.com/en-us/board/notice/view?articleId=6ace8dc0263e537d356d10c3'),
    'steam': ('Steam · official announcement feed', 'https://steamcommunity.com/app/3393110/announcements/'),
}
# PDT is printed as the primary schedule, not interpreted as a live service signal.
REGIONS = [
    ('na-east', ('North America East', '북미 동부'), '09:00–13:00 / 15:00–19:00', '18:00–22:00 / +1 00:00–04:00'),
    ('na-west', ('North America West', '북미 서부'), '09:00–13:00 / 15:00–19:00', '18:00–22:00 / +1 00:00–04:00'),
    ('europe', ('Europe', '유럽'), '03:00–07:00 / 09:00–13:00', '12:00–16:00 / 18:00–22:00'),
    ('south-america', ('South America', '남미'), '09:00–13:00 / 15:00–19:00', '18:00–22:00 / +1 00:00–04:00'),
    ('asia', ('Asia', '아시아'), '20:00–+1 00:00 / 02:00–06:00', '05:00–09:00 / 11:00–15:00'),
]


def gateway(lang, base, anchor='checklist'):
    k = lang == 'ko'; r = base + ('ko/' if k else '')
    return f'<aside class="transfer-gateway"><strong>{("Planning a Global server move?", "글로벌 서버를 옮길 예정인가요?")[k]}</strong><p>{("Check storage, shared pets and reward counters before applying.", "신청 전에 보관함·공유 펫·보상 횟수를 확인하세요.")[k]}</p><a href="{r}{ROOT}#{anchor}">{("Open the transfer checklist →", "서버 이전 체크리스트 보기 →")[k]}</a></aside>'


def render(lang, base):
    k = lang == 'ko'; t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')
    def cite(key):
        label, url = SOURCES[key]
        return f'<p class="transfer-cite"><a href="{e(url)}">{e(label)} ↗</a></p>'
    def cards(items):
        return '<div class="transfer-grid">'+''.join(f'<article><h3>{a[k]}</h3><p>{b[k]}</p></article>' for a,b in items)+'</div>'
    def panel(id, title, body, opened=False):
        return f'<details class="transfer-section" id="{id}"{(" open" if opened else "")}><summary><h2>{title}</h2></summary>{body}</details>'

    checks = [
        (('Confirm the destination with your group', '함께 갈 서버부터 확인'), ('Same region and faction; Early Access → Early Access only. One origin → one destination, once per account for the entire event.', '같은 지역·진영만 가능하며 얼리 액세스는 얼리 액세스로만 이동합니다. 전체 기간 계정당 한 번, 출발 서버 하나에서 목적지 하나로 옮깁니다.')),
        (('Count characters and destination slots', '캐릭터 수와 목적지 빈 슬롯 확인'), ('Every selected character must be level 10+. Destination slot shortfall costs 1,000 Quna each; the expansion maximum still applies.', '선택 캐릭터는 모두 10레벨 이상이어야 합니다. 목적지에서 부족한 슬롯마다 1,000 Quna가 들며 최대 확장 한도를 넘으면 신청할 수 없습니다.')),
        (('Move Server Storage items AND Kina', '서버 보관함의 아이템·키나 옮기기'), ('Put what you need in the moving character’s inventory or Character Storage. Server Storage contents stay behind.', '가져갈 것은 이전할 캐릭터의 큐브(인벤토리)나 캐릭터 보관함으로 옮기세요. 서버 보관함 안의 내용물은 남습니다.')),
        (('Consider characters staying behind', '원래 서버에 남길 캐릭터 확인'), ('Pets, skins, Quna/Mileage and Membership move under the rules below. Remaining characters lose access to transferred pets and skins; Genus Insight at origin resets.', '펫·스킨·Quna/마일리지·멤버십은 아래 규칙대로 옮겨집니다. 남은 캐릭터는 옮겨진 펫·스킨을 사용할 수 없고 출발 서버의 Genus Insight는 초기화됩니다.')),
        (('Clear Legion and active Duty Missions', '레기온·진행 중 사명 정리'), ('No Legion membership or pending application; no active Duty Missions. The applying character must be in a village, outside dungeons, Abyss and Spacetime Rifts.', '레기온 가입·가입 신청과 진행 중인 사명이 없어야 합니다. 신청 캐릭터는 던전·어비스·시공의 균열 밖, 마을에 있어야 합니다.')),
        (('Collect Market, Shop Storage and mail', '거래소·상점 보관함·우편 수령'), ('Remove sale listings and collect pending items/proceeds. Claim Shop Storage items, including Founder’s Pack, and all unclaimed mail on moving characters.', '판매 등록을 정리하고 미수령 물품·판매 대금을 받으세요. 파운더스 팩을 포함한 상점 보관함 물품과 이전 캐릭터의 미수령 우편도 받으세요.')),
        (('Check the live application screen', '실제 신청 화면에서 마지막 확인'), ('After maintenance, during your region’s hours, open In-Game Shop → Server Transfer. Check both server capacity limits, selected characters, Genus Insight choice and final Quna total. A submitted transfer cannot be canceled or reversed.', '점검 후 해당 지역 신청 시간에 인게임 상점 → 서버 이전을 여세요. 양쪽 서버의 이전 정원·선택 캐릭터·Genus Insight 선택·최종 Quna를 확인하세요. 신청 완료 후 취소·되돌리기는 불가능합니다.')),
    ]
    checklist = '<p>'+t('Preparation only. Ticking boxes does not test your account or submit a transfer; checks reset when this page reloads.', '준비용 목록입니다. 체크해도 계정 조건 검사나 이전 신청이 실행되지 않으며, 새로고침하면 체크가 초기화됩니다.')+'</p><ol class="transfer-checklist">'+''.join(f'<li><label><input type="checkbox"><span><strong>{a[k]}</strong><span>{b[k]}</span></span></label></li>' for a,b in checks)+'</ol>'+cite('products')+cite('qa')
    periods = cards([
        (('01 · Early Access servers', '01 · 얼리 액세스 서버'), ('After Oct 13 PDT / Oct 14 CEST maintenance → before Oct 20 PDT / Oct 21 CEST maintenance.', '10월 13일 PDT / 14일 CEST 점검 후 → 10월 20일 PDT / 21일 CEST 점검 전.')),
        (('02 · Launch servers', '02 · 정식 출시 서버'), ('After Oct 20 PDT / Oct 21 CEST maintenance → before Oct 27 PDT / Oct 28 CET maintenance.', '10월 20일 PDT / 21일 CEST 점검 후 → 10월 27일 PDT / 28일 CET 점검 전.')),
    ])
    region_cards = ''.join(f'<article id="region-{key}"><h3>{name[k]}</h3><dl><div><dt>PDT (UTC−07:00)</dt><dd>{pdt}</dd></div><div><dt>{t("European column as published", "공지에 적힌 유럽 시간 열")}</dt><dd>{eu} <small>CEST/CET*</small></dd></div></dl></article>' for key,name,pdt,eu in REGIONS)
    schedule = periods+'<h3>'+t('Daily application windows by server region', '서버 지역별 매일 신청 시간')+'</h3><p>'+t('Only within the matching server-type period. “+1” means the next calendar day in that time column. Asia’s 20:00 window crosses midnight; its 02:00 window is a separate early-morning window.', '해당 서버 종류의 이전 기간에만 적용됩니다. “+1”은 해당 시간 열에서 다음 날짜입니다. 아시아의 20시 구간은 자정을 넘고 02시 구간은 별도의 새벽 구간입니다.')+'</p><div class="transfer-grid">'+region_cards+'</div><aside class="transfer-warning"><strong>'+t('October 13 revision: Europe’s first window', '10월 13일 수정: 유럽 첫 신청 구간')+'</strong><p>'+t('Both notices print Oct 13, 04:00–07:00 PDT / 13:00–16:00 CEST. This conflicts with their “after Oct 13/14 maintenance” start and the maintenance notice (Oct 13, 23:30 PDT / Oct 14, 08:30 CEST; planned 4 hours). We preserve the stated exception without moving it to another date or treating it as proof that transfers are open.', '두 공지는 첫 구간을 10월 13일 04:00–07:00 PDT / 13:00–16:00 CEST로 적습니다. 이는 본문의 “13일/14일 점검 후 시작” 및 점검 공지(13일 23:30 PDT / 14일 08:30 CEST 시작, 4시간 예정)와 맞지 않습니다. 날짜를 임의로 바꾸거나 이를 서비스 개시 증거로 해석하지 않습니다.')+'</p></aside><p class="transfer-note">'+t('* The notices reuse the same European clock times under CEST/CET. These equal PDT+9 in CEST, but CET is PDT+8. The Q&A labels South America’s column CEST; Products labels it CEST/CET. Use the printed PDT schedule for comparison and recheck NC/client instructions for dates after the European clock change; no unverified CET hours are asserted here.', '* 공지는 같은 유럽 시각을 CEST/CET로 함께 표시합니다. CEST는 PDT보다 9시간, CET는 8시간 빠르므로 같은 숫자를 그대로 쓰면 맞지 않습니다. 남미 열도 Q&A는 CEST, 상품 공지는 CEST/CET입니다. 비교에는 공지의 PDT 열을 쓰고 유럽 시간 변경 이후 날짜는 NC·게임 안내를 다시 확인하세요. 검증되지 않은 CET 신청 시각은 단정하지 않습니다.')+'</p>'+cite('qa')+cite('products')+cite('maintenance')
    cost = cards([
        (('Base transfer · 0 Quna', '기본 이전 · 0 Quna'), ('Once per account across the whole transfer event, not once per character or per week.', '전체 이전 행사에서 계정당 한 번입니다. 캐릭터마다 또는 매주 한 번이 아닙니다.')),
        (('Each moving character · 0 Quna', '이전 캐릭터당 · 0 Quna'), ('No fixed character-count cap, but destination slots and eligibility constrain your selection.', '고정 이전 캐릭터 수 제한은 없지만 목적지 슬롯과 신청 조건을 충족해야 합니다.')),
        (('Each extra slot · 1,000 Quna', '추가 슬롯당 · 1,000 Quna'), ('Origin character-slot expansions stay at origin. Available destination slots determine the fee.', '출발 서버의 캐릭터 슬롯 확장은 남습니다. 목적지의 실제 빈 슬롯으로 비용을 계산합니다.')),
    ])+'<div class="transfer-example"><strong>'+t('6 characters → 4 empty slots → 2 new slots → 2,000 Quna', '캐릭터 6명 → 빈 슬롯 4개 → 2개 확장 → 2,000 Quna')+'</strong><p>'+t('With enough empty slots, total transfer cost is 0 Quna. Otherwise: max(0, moving characters − empty destination slots) × 1,000 Quna, only if those slots can still be expanded. This is a Quna cost, not a quoted USD price.', '빈 슬롯이 충분하면 총 이전 비용은 0 Quna입니다. 부족하면 max(0, 이전 캐릭터 수 − 목적지 빈 슬롯 수) × 1,000 Quna이며, 그만큼 확장할 수 있을 때만 가능합니다. 이는 Quna 비용으로, 미국 달러 가격을 뜻하지 않습니다.')+'</p></div>'+cite('products')
    storage = '<div class="transfer-flow" aria-label="'+t('Move items before transferring', '아이템 사전 이동 경로')+'"><div><b>'+t('Server Storage', '서버 보관함')+'</b><span>'+t('Contents stay here', '내용물은 남음')+'</span></div><span aria-hidden="true">→</span><div><b>'+t('Inventory / Character Storage', '인벤토리 / 캐릭터 보관함')+'</b><span>'+t('Move items and Kina here first', '아이템·키나 먼저 옮기기')+'</span></div><span aria-hidden="true">→</span><div><b>'+t('Destination', '목적지 서버')+'</b><span>'+t('Moves with the character', '캐릭터와 함께 이동')+'</span></div></div>'+cards([
        (('Character Storage', '캐릭터 보관함'), ('Items and purchased storage expansion slots move with that character.', '아이템과 구매한 캐릭터 보관함 확장 슬롯도 함께 이동합니다.')),
        (('Server Storage', '서버 보관함'), ('Items and stored Kina do not move. Only expansion records carry over, using the larger of the two servers’ expanded storage-slot counts.', '아이템·보관 중인 키나는 이전되지 않습니다. 확장 기록만 양 서버 중 더 큰 확장 슬롯 수로 적용됩니다.')),
        (('Kina / Abyss Points', '키나 / 어비스 포인트'), ('Kina in the moving character’s inventory/Character Storage moves in full. Products also marks Abyss Points and Kina/Abyss Point daily earnings as transferred.', '이전 캐릭터의 인벤토리·캐릭터 보관함 키나는 전액 이동합니다. 상품 공지는 어비스 포인트와 키나/어비스 포인트 일일 획득 기록도 이전 대상으로 표시합니다.')),
        (('Quna / Mileage', 'Quna / 마일리지'), ('The origin-server balances move in full and add to destination balances. They are moved, not copied for characters left behind.', '출발 서버 잔액 전부가 이동해 목적지 잔액에 합산됩니다. 남은 캐릭터용으로 복사되는 방식이 아닙니다.')),
        (('Membership / Daeva Pass', '멤버십 / 데바 패스'), ('Membership combines at destination and is removed from origin. Daeva Pass retains its existing progress.', '멤버십은 목적지에 합산되고 출발 서버에서 제거됩니다. 데바 패스는 기존 진행도를 유지합니다.')),
    ])+cite('qa')+cite('products')
    pets = cards([
        (('Pets, Genus Crystals and skins', '펫·Genus Crystals·스킨'), ('Merge at destination; removed at origin. Characters staying at origin can no longer equip the moved pets/skins. Pet level, collection level/rewards also carry over.', '목적지에 합쳐지고 출발 서버에서 제거됩니다. 원래 서버에 남은 캐릭터는 이동한 펫·스킨을 장착할 수 없습니다. 펫 레벨·수집 레벨/보상도 이전됩니다.')),
        (('Genus Insight choice', 'Genus Insight 진행도 선택'), ('Choose origin or destination progress, not a sum of both. If you already have a destination character, compare both before choosing. Origin Genus Insight resets whichever you choose.', '출발 또는 목적지 진행도를 선택하며 둘을 더하는 방식이 아닙니다. 목적지에 캐릭터가 있다면 두 진행도를 비교하세요. 어느 쪽을 골라도 출발 서버의 Genus Insight는 초기화됩니다.')),
        (('Duplicate shop purchases', '상점 구매 중복'), ('A duplicate Special Pet gives a Pet Reward Ticket; duplicate non-customizable decorative skins give a Skin (Single) Reward Ticket. Pass Shop duplicates of those types refund Pass Coins.', '특별 펫 중복은 Pet Reward Ticket, 커스터마이징 불가 장식 스킨 중복은 Skin (Single) Reward Ticket으로 처리됩니다. 패스 상점에서 산 해당 종류의 중복은 패스 코인으로 환급됩니다.')),
    ])+'<p>'+t('Pet tickets: request a refund through Customer Support. Skin (Single) tickets: exchange for the Shop’s 300 Quna item. Products gives expiry at Nov 24 PST / Nov 25 CET maintenance; Q&A instead labels November CEST. Confirm the deadline with NC; neither ticket works after expiry.', '펫 티켓은 고객지원에 환급을 요청하고, 스킨 티켓은 상점의 300 Quna 상품에 사용합니다. 상품 공지는 11월 24일 PST / 25일 CET 점검까지, Q&A는 11월을 CEST로 표시합니다. 정확한 마감은 NC에 확인하세요. 만료 후에는 사용할 수 없습니다.')+'</p><p>'+t('English Global names are retained where a Korean client equivalent is not verified. This is not the KR/TW transfer policy.', '한국어 클라이언트 대응 명칭을 확인하지 못한 항목은 글로벌 영문명을 함께 사용합니다. 한국·대만 서버의 이전 정책과는 구분하세요.')+'</p>'+cite('qa')+cite('products')
    rewards = cards([
        (('Dungeon reward progress is retained', '던전 보상 진행도 유지'), ('Remaining Cube reward claims and attempts left until guaranteed rewards move, including Expeditions and Transcendence. A move is not a fresh reward allowance.', '원정·초월 등을 포함한 큐브 보상 잔여 횟수와 확정 보상까지 남은 횟수가 이동합니다. 이전으로 새 보상 횟수가 생기는 것이 아닙니다.')),
        (('Character content usage moves', '캐릭터 이용 기록 이동'), ('Abyss time, Spacetime Rift time, Abyss Corridor usage and related reward counts carry over. Corridor access still requires destination-server capture.', '어비스·시공의 균열 이용 시간, 어비스 회랑 이용 기록과 관련 보상 횟수가 유지됩니다. 목적지 서버에서 회랑이 점령되지 않았다면 입장할 수 없습니다.')),
        (('Server-wide reward progress', '서버 단위 보상 진행도'), ('Daily Dungeons, Shugo Festival and Dimensional Invasion progress transfers. The Q&A says origin-server reward progress also stays unchanged; do not infer duplicate rewards.', '일일 던전·슈고 페스타·차원 침공 보상 진행도는 이전됩니다. Q&A는 출발 서버의 보상 진행도도 그대로라고 설명합니다. 추가 중복 보상을 뜻한다고 해석하지 마세요.')),
        (('Missions, rankings and shop limits', '임무·랭킹·상점 구매 제한'), ('Season missions/claim history and Supply Requests carry over. Season rank points move and are removed at origin. Character purchase counts carry over; server-limited Coin Shop counts use the higher server count, so transfer does not restore purchases.', '시즌 임무·보상 수령 기록과 보급 의뢰는 유지됩니다. 시즌 랭킹 포인트는 이동하고 출발 서버에서 제거됩니다. 캐릭터 구매 횟수는 유지되며 서버 제한 코인 상점 횟수는 양 서버 중 더 큰 값이 적용돼 구매 기회가 복구되지 않습니다.')),
    ])+'<p>'+t('During the transfer period, the Q&A says Wind Breeze Merchants’ Soul Crystals and Instant Clear Tickets (Server) shift to equivalent quantities through Substance Morph; Odyle Energy purchase limits change from server-based to character-based. Check your current client before buying.', '이전 기간에는 바람길 상인 특수 상품의 Soul Crystals와 Instant Clear Tickets (Server)가 물질 변환을 통한 같은 수량으로 바뀌며, Odyle Energy 구매 제한은 서버에서 캐릭터 단위로 바뀐다고 Q&A가 안내합니다. 구매 전에 현재 게임 안내를 확인하세요.')+'</p><p>'+t('After transfer: choose a new name (all moving characters get a temporary name, even without a collision). Friends/Blocked lists persist. Transfer processing logs the account out and blocks login until completion; NC lists a minimum of one minute with possible longer queues or temporary restrictions.', '이전 후에는 이름을 다시 정합니다. 이름 중복이 없어도 모든 이전 캐릭터에 임시 이름이 부여됩니다. 친구·차단 목록은 유지됩니다. 처리 중에는 계정이 로그아웃되고 완료까지 접속할 수 없습니다. NC는 최소 1분, 요청량에 따라 더 긴 대기나 일시 제한이 있을 수 있다고 안내합니다.')+'</p>'+cite('qa')+cite('products')
    sections = [('checklist',t('Before you apply · 7 checks','신청 전 · 7가지 확인'),checklist),('schedule',t('Dates & regional hours','기간·지역별 시간'),schedule),('cost',t('Cost & character slots','비용·캐릭터 슬롯'),cost),('storage',t('Storage & currency','보관함·재화'),storage),('pets',t('Pets & shared progress','펫·공유 진행도'),pets),('rewards',t('Dungeon rewards & after arrival','던전 보상·이전 후'),rewards)]
    nav='<nav class="transfer-jumps" aria-label="'+t('Transfer guide topics','이전 가이드 항목')+'">'+''.join(f'<a href="#{id}">{title}</a>' for id,title,_ in sections)+'</nav>'
    evidence=json.loads((Path(__file__).parent/'research/server-transfer-review.json').read_text())
    checked=evidence['checkedAt']
    status='<aside class="transfer-status"><span class="transfer-badge">'+t('Announced schedule · live eligibility unverified','공식 일정 안내 · 실제 신청 가능 여부 미확인')+'</span><p>'+t('Official schedule published; live eligibility was not verified. Recheck maintenance, regional hours and server capacity in the in-game shop. A date alone does not confirm availability.', '공식 일정 기준입니다. 실제 신청 가능 여부는 확인하지 못했습니다. 점검·신청 시간·서버 정원은 게임 내 상점에서 다시 확인하세요. 날짜만으로 개시를 단정할 수 없습니다.')+f'</p><small>{t("Sources checked at", "출처 확인 시각")} {e(checked)} (UTC)</small></aside>'
    source_list='<details class="transfer-section" id="transfer-sources"><summary><h2>'+t('Official sources & review notes','공식 출처·검토 기록')+'</h2></summary><p>'+t('NC notices were published October 9 and the transfer notices show an October 13 revision. Recheck these links before an irreversible request. The supplied Steam article URL did not expose a readable body during review; the official Steam feed corroborated both transfer notices.', 'NC 이전 공지는 10월 9일 게시됐으며 10월 13일 수정 내용이 표시됩니다. 되돌릴 수 없는 신청 전에 아래 원문을 다시 확인하세요. 제공된 Steam 개별 주소에서는 본문을 읽지 못해 공식 Steam 공지 목록으로 두 이전 공지를 대조했습니다.')+'</p>'+''.join(cite(key) for key in SOURCES)+'</details>'
    related='<nav class="transfer-related" aria-label="'+t('Related guides','관련 공략')+'">'+''.join(f'<a href="{r}{route}">{label}</a>' for route,label in [('guides/pet-growth/',t('Pet growth →','펫 성장 →')),('guides/dungeon-rewards/',t('Dungeon rewards →','던전 보상 →')),('routines/',t('Daily & weekly →','일일·주간 숙제 →')),('endgame/',t('Character growth →','내실·성장 →'))])+'</nav>'
    return '<div class="transfer-guide">'+status+nav+''.join(panel(id,title,body,id=='checklist') for id,title,body in sections)+source_list+related+'</div>'


def search_entries(lang, base):
    k=lang=='ko'; prefix=('ko/' if k else '')+ROOT
    labels=[('checklist',('Server transfer checklist','서버 이전 체크리스트')),('schedule',('Transfer dates and regional hours','서버 이전 기간·지역별 시간')),('cost',('0 Quna transfer and 1,000 Quna slots','0 Quna 이전·1,000 Quna 슬롯')),('storage',('Character/Server Storage and currency','캐릭터·서버 보관함과 재화')),('pets',('Pets, Genus Insight and skins','펫·Genus Insight·스킨')),('rewards',('Dungeon reward counts after transfer','이전 후 던전 보상 횟수'))]
    return [dict(lang=lang,path=prefix,anchor=id,title=label[k],description=DESCRIPTION[k],category=('Global transfer','글로벌 이전')[k],keywords='server transfer migration 이전 얼리 액세스 launch region PDT CEST CET Quna Kina 키나 마일리지 보관함 슬롯 펫 pets Genus Insight dungeon rewards 보상 사명 Legion 레기온 '+label[k]) for id,label in labels]

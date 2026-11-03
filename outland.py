"""KR-only participation checklist; official announcement, not gameplay testing."""
from html import escape

ROOT = 'guides/abyss-outland/'
REVIEWED = '2026-11-04'
TITLE = ('Abyss Outland: first-entry guide · Korea', '어비스 아웃랜드 초보자 참여 가이드 · 한국 서버')
DESCRIPTION = ('Check eligibility, KR server times and weekly rewards before your first solo PvP survival match.', '참여 조건·한국 서버 시간·주간 보상을 먼저 확인하고 개인 PvP 생존전에 준비하세요.')
PATCH = 'https://aion2.plaync.com/ko-kr/board/update/view?articleId=6ae0fbb828c7452635072d36'
PATCH_1104 = 'https://aion2.plaync.com/ko-kr/board/update/view?articleId=6aea36386cfe4756db5b9115'
GUIDEBOOK = 'https://aion2.plaync.com/ko-kr/guidebook/view?title=%EC%96%B4%EB%B9%84%EC%8A%A4'


def render(lang, base):
    ko = lang == 'ko'
    t = lambda en, kr: kr if ko else en
    r = base + ('ko/' if ko else '')
    def section(id, title, content):
        return f'<section id="{id}"><h2>{title}</h2>{content}</section>'
    def p(en, kr):
        return '<p>'+t(en, kr)+'</p>'
    facts = [
        (t('Character level', '캐릭터 레벨'), t('45 or higher', '45 이상')),
        (t('Item level', '아이템 레벨'), '3,000+'),
        (t('Daily · KR server time', '매일 · 한국 서버 기준'), '11:10–13:40 / 20:10–23:40'),
        (t('Opening interval', '경기 개설 간격'), t('Every 30 minutes', '30분마다')),
    ]
    body = '<div class="party-answer"><span class="eyebrow">KR ONLY · 2026-11-04</span>'+p('Meet both level requirements, then check an opening in the KR client. This English page describes Korea only; it does not announce availability on other servers.', '레벨 조건 두 가지를 모두 충족한 뒤 한국 클라이언트에서 참가 시간을 확인하세요. 한국 서버 전용 안내이며 다른 지역의 적용 여부를 뜻하지 않습니다.')+'<dl class="outland-facts">'+''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label,value in facts)+'</dl></div>'
    body += '<nav class="party-next" aria-label="'+t('On this page','바로 찾기')+'">'+''.join(f'<a href="#{id}">{label}</a>' for id,label in [('prepare',t('First-entry steps','첫 참가 순서')),('schedule',t('When to join','참가 시간')),('rules',t('November 4 changes','11월 4일 변경')),('rewards',t('Coins & weekly reset','주화·주간 초기화')),('unverified',t('Still unverified','아직 미검증'))])+'</nav>'
    body += section('purpose', t('What am I trying to do?', '무엇을 하는 콘텐츠인가요?'), p('A solo PvP survival contest: the official notice describes about 100 players competing until one remains. Ranking follows survival order. Surviving longer is the stated objective; this is not a dungeon boss clear.', '약 100명이 최후의 1인을 가릴 때까지 경쟁하는 개인 PvP 생존전입니다. 오래 살아남은 순서로 순위가 정해지므로, 공식 목표는 생존입니다. 던전 보스를 잡는 콘텐츠와는 다릅니다.'))
    steps = [
        (t('Check both numbers', '두 가지 수치 확인'), t('Check character Lv45+ and item level 3,000+. Meeting only one is insufficient. Item level is not Combat Power.', '캐릭터 45레벨 이상과 아이템 레벨 3,000 이상을 모두 확인하세요. 한 가지만 충족하면 안 됩니다. 아이템 레벨과 전투력은 다른 수치입니다.')),
        (t('Choose a daily window', '참가 시간 고르기'), t('Use the KR schedule below. Before setting aside time, check the current client notice for maintenance or changes.', '아래 한국 서버 일정에서 시간을 고르세요. 시간을 비워두기 전 현재 클라이언트 공지에서 점검·변경 여부를 확인하세요.')),
        (t('Check entry through the Abyss UI', '어비스 UI에서 입장 안내 확인'), t('The official entry route is the Abyss UI. Read the Outland entry information shown there. Exact tabs, button names, queue opening time and confirmation steps are unverified; follow the current client instructions.', '공식 입장 경로는 어비스 UI입니다. 그 안에서 아웃랜드 입장 안내를 확인하세요. 정확한 탭·버튼명, 신청 시작 시각, 확인 절차는 미검증이므로 현재 화면 안내를 따르세요.')),
        (t('Prepare for a learning run', '첫 판은 적응 목표로 준비'), t('Editorial checklist: review familiar movement and defensive skill controls before joining. Read any displayed match rules. No mandatory gear, consumable, PvP build or winning tactic is established by this guide.', '편집자 준비 팁: 참가 전 익숙한 이동·방어 스킬의 조작을 점검하고 표시되는 경기 규칙을 읽으세요. 필수 장비·소모품·PvP 빌드나 승리 전술이 검증된 것은 아닙니다.')),
        (t('Compare placement and reward', '종료 후 순위·보상 확인'), t('Check the result and actual coin award, then the remaining weekly earning allowance and exchange-shop prices. The result-screen layout and manual versus automatic reward delivery are unverified.', '결과와 실제 지급 주화를 확인한 뒤 남은 주간 획득 한도·교환 상점 가격을 확인하세요. 결과 화면 구성과 수동 수령·자동 지급 여부는 미검증입니다.')),
    ]
    body += section('prepare',t('Your first-entry checklist','처음 참가하는 순서'),'<ol class="outland-steps">'+''.join(f'<li><h3>{heading}</h3><p>{text}</p></li>' for heading,text in steps)+'</ol>')
    body += section('schedule',t('When can I participate?','언제 참여하나요?'),'<ul><li>11:10–13:40</li><li>20:10–23:40</li></ul>'+p('The November 4 KR patch moved both windows 10 minutes later. Matches are still announced every 30 minutes within those windows. These are KR server times, not your device’s local times. The interval does not establish a 30-minute match duration. Exact registration deadlines and final-slot admission need client verification.', '11월 4일 한국 패치로 두 시간대가 모두 10분씩 늦춰졌습니다. 공지된 시간대 안에서 30분 간격 개설은 유지됩니다. 휴대폰 현지 시간이 아닌 한국 서버 기준입니다. 30분은 개설 간격이며 한 경기의 길이가 30분이라는 뜻은 아닙니다. 신청 마감과 마지막 회차 접수는 게임 내 확인이 필요합니다.'))
    rule_rows = [
        t('Opening: the airship disappears when the barrier drops after the match begins.', '시작: 경기 시작 뒤 장막이 해제될 때 비공정이 사라집니다.'),
        t('Upper floor: poison appears 30 seconds later than before.', '상층: 독기가 기존보다 30초 늦게 등장합니다.'),
        t('Middle floor: the wind-route position changed; the patch does not publish coordinates.', '중층: 바람길 위치가 바뀌었으며 공지는 좌표를 공개하지 않았습니다.'),
        t('Late poison: stage-3 poison on every floor now deals the same damage; no value is published.', '후반 독기: 모든 층의 3단계 독기가 같은 피해량을 주며 수치는 공개되지 않았습니다.'),
        t('Consumables: attacking breaks potion stealth. Invincibility lasts less time, but movement and skills are allowed during it.', '소모품: 은신 물약 중 공격하면 은신이 풀립니다. 무적 시간은 줄지만 무적 중 이동·스킬 사용이 가능해집니다.'),
    ]
    body += section('rules',t('What changed on November 4?','11월 4일에 무엇이 바뀌었나요?'),'<ul>'+''.join('<li>'+x+'</li>' for x in rule_rows)+'</ul>'+p('These are official patch facts, not a tested winning route. Recheck wind-route coordinates, poison timing and damage, stealth-breaking actions, invincibility duration and usable skills in the current KR client.', '공식 패치에서 확인된 사실이며 실측 승리 동선은 아닙니다. 현재 한국 클라이언트에서 바람길 좌표·독기 타이밍/피해·은신 해제 공격·무적 지속시간·사용 가능한 스킬을 다시 확인해야 합니다.'))
    body += section('rewards',t('What do I earn, and when does the cap reset?','무엇을 받고 언제 초기화되나요?'),p('Survival placement → Traveler’s Coins (방랑자의 주화) → items in the Abyss exchange shop. The English coin name here is a guide translation, not a verified Global-client label.', '생존 순위에 따라 방랑자의 주화를 얻고, 어비스 교환 상점에서 물품을 구매할 수 있습니다.')+p('There is a weekly earning cap, reset every Wednesday at 05:00 on the KR server schedule. This resets the earning limit; the notice does not say that held coins expire. Rank payouts, the cap amount, item prices and character/account scope remain unverified.', '주간 획득 한도가 있으며 매주 수요일 05:00에 초기화됩니다. 초기화 대상은 획득 한도입니다. 보유 주화가 사라진다는 안내는 없습니다. 순위별 지급량·한도 수치·상점 가격·캐릭터/계정 적용 범위는 미검증입니다.')+p('Before spending, compare the actual shop price with your coin balance. No guaranteed weekly income or recommended purchase order is calculated here.', '사용 전 실제 상점 가격과 보유 주화를 비교하세요. 확정 주간 수입이나 추천 구매 순서를 임의로 계산하지 않았습니다.'))
    checks = [t('Matchmaking, exact player count, match duration and tie handling', '매칭 방식·실제 참여 인원·경기 시간·동순위 처리'),t('UI buttons, queue deadlines and reward-claim controls', '화면 버튼·신청 마감·보상 수령 조작'),t('Wind-route coordinates, poison timing/damage and Flame Bomb damage after the fix', '바람길 좌표·독기 타이밍/피해·수정 후 화염 폭탄 피해'),t('Stealth break conditions, invincibility duration and usable movement/skills', '은신 해제 조건·무적 지속시간·사용 가능한 이동/스킬'),t('Rank payouts, weekly cap amount, shop stock/prices and cap scope', '순위별 주화·주간 한도 수치·상점 품목/가격·한도 적용 범위')]
    body += section('unverified',t('In-game verification still needed','게임 내 검증이 필요한 항목'),'<ul>'+''.join('<li>'+x+'</li>' for x in checks)+'</ul>'+p('If entry is unavailable, recheck both requirements, the current KR time and any displayed restriction. Do not assume a hidden quest or a particular button sequence.', '입장이 안 되면 두 참여 조건·현재 한국 서버 시간·표시된 제한 안내부터 다시 확인하세요. 숨겨진 선행 퀘스트나 특정 버튼 순서를 추정하지 마세요.'))
    body += section('sources',t('Official references & evidence','공식 자료·검증 상태'),f'<ul><li><a href="{PATCH}">'+t('NC · October 28 KR update','NC · 10월 28일 한국 업데이트')+f'</a></li><li><a href="{PATCH_1104}">'+t('NC · November 4 KR update','NC · 11월 4일 한국 업데이트')+f'</a></li><li><a href="{GUIDEBOOK}">'+t('NC · Abyss guidebook (Korean)','NC · 어비스 가이드북')+'</a></li></ul>'+p('Official patch bodies were checked through November 4, 2026. The linked guidebook is the publisher’s route to detailed rules; its dynamic content and Outland screenshots were not independently verified here. No unrelated game image is presented as Outland footage. This is an announcement-based preparation guide, not a gameplay-tested walkthrough.', '2026년 11월 4일 공식 패치까지 대조했습니다. 상세 규칙은 공지가 연결한 공식 가이드북을 참고하세요. 가이드북의 동적 본문과 아웃랜드 실제 화면은 여기서 독립 확인하지 못해 첨부하지 않았습니다. 이 글은 공지 기반 준비 안내이며 직접 플레이 검증을 완료한 공략은 아닙니다.')+f'<a href="{r}updates/kr-6aea36386cfe4756db5b9115/">'+t('Read the November 4 update summary','11월 4일 업데이트 요약 보기')+'</a>')
    return '<article class="party-guide outland-guide">'+body+'</article>'

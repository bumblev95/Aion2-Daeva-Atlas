"""Short, sourced answers to observed party-search questions; no client dependency."""
from html import escape as e
from fieldnotes import BOSSES

REVIEWED = '2026-10-14'
GUIDES = [
    ('3b-meaning',
     ('What does 3b mean in AION 2? Three-boss party runs', '아이온 2 3b 뜻: 보스 3마리 모두 잡는 파티'),
     ('3b means clearing all three bosses in an AION 2 party run. Decode 200k+ / 3b / tp, compare run plans and open boss mechanics and reward guides.',
      '아이온 2 파티 모집의 3b는 보스 3마리를 모두 잡는다는 뜻입니다. 200k+·3b·tp 모집글 예시와 보스 공략·보상 확인 순서를 정리했습니다.')),
    ('commend-player',
     ('AION 2: how to commend a player & check a missing popup', '아이온 2 칭찬 방법: 조건·팝업 확인'),
     ('Choose a player and reason in the post-boss commendation popup. Read the steps, eligibility checks and dated official KR rules; Global details may differ.',
      '마지막 보스 처치 뒤 칭찬 창에서 대상과 사유를 선택합니다. 칭찬 방법·대상 조건·팝업 누락 확인법을 공식 한국 패치 기준으로 정리했습니다. 글로벌은 다를 수 있습니다.')),
]


def gateway(lang, base):
    k = lang == 'ko'; r = base + ('ko/' if k else '')
    return '<nav class="party-shortcuts" aria-label="'+('Party questions','파티 궁금증')[k]+'">'+''.join(
        f'<a href="{r}guides/{slug}/">{label[k]} →</a>' for slug, label in [
            ('3b-meaning', ('What does 3b mean?', '3b·파티 약어 뜻')),
            ('commend-player', ('How to commend a player', '플레이어 칭찬 방법'))])+'</nav>'


def render(slug, lang, base):
    k = lang == 'ko'; t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')
    def section(id, title, body):
        return f'<section id="{id}"><h2>{title}</h2>{body}</section>'
    def sources(items, scope):
        return f'<section class="party-sources"><h2>{t("Sources & scope", "출처·적용 범위")}</h2><p>{scope}</p><ul>'+''.join(f'<li><a href="{url}" rel="noopener noreferrer">{e(label)} ↗</a></li>' for url, label in items)+f'</ul><p class="small muted">{t("Reviewed", "검토")} {REVIEWED}</p></section>'
    if slug == '3b-meaning':
        answer = t('In AION 2 party recruitment, <strong>3b means clearing all three bosses</strong> in the run. The party plans to kill bosses 1, 2 and 3 before finishing.',
                   '아이온 2 파티 모집에서 <strong>3b는 보스 3마리를 모두 잡는다는 뜻</strong>입니다. 보스 1·2·3을 전부 처치하는 진행 방식으로 모집하는 파티입니다.')
        flow = '<ol class="party-flow">'+''.join(f'<li><span>{i:02}</span><strong>{t("Boss", "보스")} {i}</strong><small>{t("Defeat together", "함께 처치")}</small></li>' for i in (1,2,3))+'</ol>'
        terms = [
            ('200k+', t('Combat Power of at least 200,000 in this example. The leader sets the requirement; this is not a recommended Global cutoff.', '이 예시에서는 전투력 200,000 이상. 파티장이 정한 모집 조건이며 글로벌 권장 컷이 아닙니다.')),
            ('3b', t('All three bosses in that dungeon run.', '해당 던전의 보스 세 마리를 모두 처치.')),
            ('tp', t('Teleport shorthand. Ask which travel point or route is prepared.', '텔레포트 약어. 어떤 이동 거점·경로가 준비됐는지 확인.')),
        ]
        decoder = '<div class="party-example"><p class="eyebrow">'+t('RECRUITMENT EXAMPLE', '파티 모집글 예시')+'</p><p class="party-code">200k+ · 3b · tp</p><dl>'+''.join(f'<div><dt>{term}</dt><dd>{copy}</dd></div>' for term, copy in terms)+'</dl></div>'
        body = section('party-example', t('How to read the party listing', '모집글은 이렇게 읽어요'), decoder)
        body += section('run-plan', t('Agree on the run before entering', '입장 전에 진행 방식을 맞추기'),
            '<p>'+t('If the listing says 3b, stay for all three boss kills. A final-boss-only run has a different plan. Check the dungeon, difficulty and route with the leader before joining.', '3b로 모집했다면 세 보스를 모두 잡을 때까지 함께 진행합니다. 막보만 잡는 파티는 진행 계획이 다릅니다. 참가 전에 던전·난도·경로를 파티장과 맞춰두세요.')+'</p><p>'+t('A useful question: “All three bosses, and which teleport point are we using?”', '확인할 말: “3보스 다 잡고, 텔포는 어느 거점으로 가나요?”')+'</p>')
        body += section('rewards', t('Connect the route to your reward goal', '돌 보스와 받을 보상을 함께 확인하기'),
            '<p>'+t('A clear and a reward claim are separate checks. Match the boss drops to the item you want, then check your available entries and reward requirements. The KR source explains why its three-boss route matters for Kinah; it does not establish a fixed payout for every Global run.', '클리어와 보상 수령 조건은 따로 확인합니다. 원하는 장비의 보스를 찾고 입장 횟수·보상 조건을 확인하세요. 한국 원문은 키나를 위해 세 보스를 모두 잡는 맥락을 설명하며, 모든 글로벌 던전의 지급액을 보장하는 자료는 아닙니다.')+f'</p><a href="{r}guides/dungeon-rewards/">'+t('Compare dungeon rewards and where to use them', '던전 보상·사용처 비교하기')+' →</a>')
        bosses = ''.join(f'<a href="{r}dungeons/{b["slug"]}/">{e(b["dungeon"][k])} →</a>' for b in BOSSES)
        body += section('boss-guides', t('Prepare for the dungeon you joined', '참가한 던전의 패턴 확인하기'),
                            '<p>'+t('Open the boss cues and movement lessons for your run.', '참가한 던전의 전조·이동·안전 위치를 확인하세요.')+'</p><nav class="party-bosses">'+bosses+'</nav>')
        body += sources([('https://m.inven.co.kr/board/aion2/6444/2116', '구원의노래 · Inven · 2026-07-20 · 200k / 3b / tp')],
                        t('Party shorthand from an original KR player guide, also confirmed by reader feedback. The route above is an explanation of the term, not a measured dungeon map. Recruitment thresholds and reward rules depend on the party and service region.', '한국 유저 원문의 파티 약어와 독자 피드백을 확인했습니다. 위 그림은 약어를 설명하는 도식이며 실제 던전 지도가 아닙니다. 모집 컷·보상 규칙은 파티와 서비스 지역에 따라 다릅니다.'))
    elif slug == 'commend-player':
        answer = t('<strong>To commend a player, choose a teammate and a reason in the timed popup after the final boss.</strong> The steps below follow official Korean patch notes; check the current Global client for availability and eligible content.',
                   '<strong>마지막 보스를 잡은 뒤 제한 시간 내 칭찬 창에서 파티원과 사유를 선택합니다.</strong> 아래는 공식 한국 패치 기준입니다. 글로벌에서는 현재 클라이언트의 제공 여부·대상 콘텐츠를 확인하세요.')
        steps = [t('Defeat the final boss while remaining in the party and dungeon.', '파티·던전에 남아 마지막 보스를 처치합니다.'),
                 t('When the commendation popup appears, choose an eligible teammate.', '칭찬 창이 나타나면 선택 가능한 파티원을 고릅니다.'),
                 t('Choose the reason and submit before the popup expires.', '칭찬 사유를 선택하고 창이 닫히기 전에 완료합니다.')]
        flow = '<ol class="party-flow">'+''.join(f'<li><span>{i:02}</span><strong>{step}</strong></li>' for i, step in enumerate(steps,1))+'</ol>'
        body = section('eligibility', t('Who can give and receive a commendation?', '누가 칭찬을 주고받을 수 있나요?'),
            '<p>'+t('The September 9 KR rules cover Expedition, Transcendence, Trial and Sanctuary clears. Givers and recipients must meet the contribution requirement and still be in the party and dungeon when the final boss dies. One commendation is available per clear; totals appear in character information.', '9월 9일 한국 공지는 원정·초월·시련·성역을 대상으로 합니다. 칭찬하는 사람과 받는 사람 모두 기여도 조건을 채우고 마지막 보스 처치 시 파티·던전에 남아 있어야 합니다. 클리어당 한 번 칭찬하며 누적 횟수는 캐릭터 정보에서 확인합니다.')+'</p><p>'+t('KR changed Sanctuary recipients from your own party to the alliance on September 23. Do not assume the original party-only restriction still applies, or copy the KR update date to Global.', '한국은 9월 23일 성역 칭찬 대상을 자기 파티에서 포스까지 확대했습니다. 최초 공지의 파티 한정 조건이나 한국 적용일을 글로벌에 그대로 적용하지 마세요.')+'</p>')
        checks = [t('Was it the final boss, and is this a supported activity in your region?', '마지막 보스를 잡았고 현재 지역에서 지원하는 콘텐츠인가요?'),
                  t('Were you still inside and in the party, with the required contribution?', '처치 시 던전·파티에 남아 기여도 조건을 채웠나요?'),
                  t('Has the timed popup already closed?', '선택 제한 시간이 지나 창이 닫혔나요?')]
        body += section('missing-popup', t('If the popup or player is missing', '칭찬 창·대상이 보이지 않을 때'), '<ul>'+''.join(f'<li>{x}</li>' for x in checks)+'</ul><p>'+t('KR fixed a missing Trial popup on September 16 and death/resurrection popup closures on September 23. Those are dated fixes, not proof of a current Global bug or a hidden settings switch.', '한국은 9월 16일 시련 칭찬 창 누락, 9월 23일 사망·기본 부활로 창이 닫히는 문제를 수정했습니다. 과거 수정 이력이며 현재 글로벌 버그나 별도 설정 스위치가 있다는 의미는 아닙니다.')+'</p>')
        body += sources([('https://aion2.plaync.com/ko-kr/board/update/view?articleId='+id, label) for id, label in [
            ('6aa062386b722c561dc6a46c', 'NC · KR · 2026-09-09 · commendation rules'),
            ('6aa99cb8a279104f7d9d5c34', 'NC · KR · 2026-09-16 · Trial popup fix'),
            ('6ab2d738a279104f7d9d5d5b', 'NC · KR · 2026-09-23 · alliance eligibility and popup fixes')]],
            t('Official KR notes checked against the publisher’s public article API. Exact Global eligibility and button labels have not been independently verified.', '공식 한국 공지의 공개 본문 API와 대조했습니다. 글로벌의 세부 대상 조건·버튼 이름은 독립적으로 확인하지 못했습니다.'))
    else:
        raise ValueError('Unknown party guide: '+slug)
    related = f'<nav class="party-next" aria-label="{t("Next guides", "다음 공략")}"><a href="{r}dungeons/">{t("Animated boss mechanics", "움직이는 보스 패턴")} →</a><a href="{r}routines/">{t("Daily & weekly rewards", "일일·주간 보상")} →</a><a href="{r}endgame/">{t("After-story growth route", "스토리 이후 성장 순서")} →</a></nav>'
    return f'<article class="party-guide" data-party-topic="{slug}"><div class="party-answer"><span class="eyebrow">{t("QUICK ANSWER", "먼저 답부터")}</span><p>{answer}</p></div>{flow}{body}{related}</article>'


def search_entries(lang):
    k = lang == 'ko'; prefix = 'ko/' if k else ''
    return [dict(lang=lang, path=prefix+'guides/'+slug+'/', title=title[k], description=desc[k],
                 category=('Party guide', '파티 가이드')[k],
                 keywords=('3b 3boss 3 boss three bosses all bosses 200k tp 3보 3보스 파티 모집' if slug=='3b-meaning' else 'commend player commendation praise missing popup 칭찬 추천 팝업'))
            for slug, title, desc in GUIDES]

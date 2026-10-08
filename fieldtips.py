"""Small, source-linked practice tools inspired by a reader-submitted KR guide.

The source screenshots are inspected, linked, and never rehosted or hotlinked.
All practice UI below is original and explicitly labelled as an illustration.
"""
from html import escape

SOURCE = 'https://m.inven.co.kr/board/aion2/6444/2116'
AUTHOR = '구원의노래'
SOURCE_DATE = '2026-07-20'
REVIEW_DATE = '2026-10-08'
IMAGE_ROOT = 'https://upload3.inven.co.kr/upload/2026/07/19/bbs/'

TIPS = [
    dict(id='rear', title=('Find the boss’s back', '보스 뒤쪽 찾기'),
         path=('Settings → Information → Combat → Boss direction marker: BACK', '환경 설정 → 정보 출력 → 전투 → 보스 방향 마커 표시: BACK'),
         copy=('Turn on the marker, then find the rear. Still dodge attacks.', '후방 표시를 켜고 뒤를 찾아요. 위험한 공격은 피하세요.'),
         image='i1231953989.png'),
    dict(id='chat', title=('See when a message arrived', '채팅이 언제 왔는지 보기'),
         path=('Chat settings → Timestamp: ON', '채팅 설정 → 시간 표시: ON'),
         copy=('Timestamps help separate new messages from old ones.', '시간을 보면 새 메시지인지 구분하기 쉬워요.'),
         image='i1130386215.png'),
    dict(id='auto', title=('Check automatic consumables', '자동 사용 조건 확인하기'),
         path=('Settings → Combat → Auto Use', '환경 설정 → 전투 → 자동 사용'),
         copy=('Health conditions and combat-only buff use are separate options.', '물약의 생명력 조건과 버프의 전투 중 사용은 별도 설정이에요.'),
         image='i1520372560.png'),
    dict(id='bag', title=('Review before extracting', '추출 전에 목록 확인하기'),
         path=('Inventory → Extraction → Selection settings', '가방 → 추출 → 간편 선택 설정'),
         copy=('Inspect selected equipment first. Keep automatic extraction off while learning.', '선택된 장비를 먼저 확인하세요. 익숙해질 때까지 자동 추출은 꺼두세요.'),
         image='i1583568305.png'),
]


def source_note(lang):
    ko = lang == 'ko'
    title = '실전 팁 출처' if ko else 'Practical-tip source'
    text = ('한국 서버 유저 글과 캡처 기준입니다. 글로벌 메뉴·규칙은 다를 수 있어요.' if ko else
            'Based on KR player captures; English labels are explanatory translations. Global menus and rules may differ.')
    return f'''<details class="evidence"><summary>{title} · {AUTHOR}</summary>
<p>{text}</p><p><a href="{SOURCE}" target="_blank" rel="noopener noreferrer">구원의노래 · 아이온2 처음하는 사람들을 위한 노하우 ↗</a></p>
<p class="small muted">KR · {SOURCE_DATE} · {'검토' if ko else 'Reviewed'} {REVIEW_DATE}</p></details>'''


def panel(lang):
    ko = lang == 'ko'
    t = lambda en, kr: kr if ko else en
    cards = []
    for i, tip in enumerate(TIPS):
        key = tip['id']
        if key == 'rear':
            demo = f'''<div class="tip-arena"><span class="tip-boss">{t('BOSS','보스')}</span><span class="tip-rear" data-tip-effect hidden>▼ BACK</span><span class="tip-player">{t('YOU','나')}</span></div>
<button class="btn" data-tip-toggle aria-pressed="false">{t('Show BACK marker','후방 표시 켜보기')}</button>'''
        elif key == 'chat':
            demo = f'''<div class="tip-chat"><p><time data-tip-effect hidden>20:01</time> {t('Ready?','준비됐나요?')}</p><p><time data-tip-effect hidden>20:03</time> {t('First run, please explain.','초행이에요. 설명 부탁드려요.')}</p></div>
<button class="btn" data-tip-toggle aria-pressed="false">{t('Show timestamps','시간 표시 켜보기')}</button>'''
        elif key == 'auto':
            demo = f'''<label class="tip-control">{t('Illustrative HP threshold','연습용 생명력 기준')} <select data-tip-hp><option value="30">30%</option><option value="50" selected>50%</option><option value="70">70%</option></select></label>
<div class="tip-health" aria-hidden="true"><span></span><b>HP 45%</b></div><p class="tip-result" data-tip-hp-result role="status"></p>
<label class="tip-control"><input type="checkbox" data-tip-buff checked> {t('Buffs only during combat','버프는 전투 중에만')}</label>
<p class="tiny">{t('Example values, not recommended settings. No items are consumed.','예시 수치이며 추천값이 아니에요. 실제 아이템은 소모되지 않아요.')}</p>'''
        else:
            demo = f'''<div class="tip-bag"><span>◇<small>{t('Keep','보관')}</small></span><span>◇<small>{t('Review','확인')}</small></span><span>◇<small>{t('Review','확인')}</small></span></div>
<button class="btn" data-tip-toggle aria-pressed="false">{t('Preview the selection','선택 목록 살펴보기')}</button>
<p class="tip-result" data-tip-effect hidden>{t('Stop if an item you need is selected. Nothing was deleted here.','필요한 장비가 선택됐다면 멈추세요. 여기서는 아무것도 삭제하지 않아요.')}</p>'''
        cards.append(f'''<article class="field-tip" id="tip-{key}" data-field-tip="{key}">
<div class="tip-heading"><span>{i+1:02}</span><h3>{escape(tip['title'][ko])}</h3></div>
<p class="tip-path">{escape(tip['path'][ko])}</p><p>{escape(tip['copy'][ko])}</p>
<div class="tip-demo"><small class="tip-demo-label">{t('PRACTICE DIAGRAM · NOT A SCREENSHOT','설명용 연습 화면 · 실제 스크린샷 아님')}</small>{demo}</div>
<div class="tip-evidence"><a href="{IMAGE_ROOT}{tip['image']}?MW=800" target="_blank" rel="noopener noreferrer">{t('Open original screenshot','실제 스크린샷 원본 보기')} ↗</a><a href="{SOURCE}" target="_blank" rel="noopener noreferrer">{AUTHOR} · Inven ↗</a></div></article>''')
    terms = [
        ('200k', ('200,000 combat power. An example, not a recommended threshold.', '전투력 200,000. 해독 예시이며 권장 컷이 아니에요.')),
        ('3b', ('Three bosses. Confirm the party’s route.', '보스 세 마리. 파티의 진행 경로를 확인해요.')),
        ('tp', ('Teleport shorthand. Ask whether the travel point is ready.', '텔레포트 약어. 이동 거점 준비 여부를 물어봐요.')),
    ]
    decoder = ''.join(f'<details class="party-token"><summary>{term} <span>?</span></summary><p>{escape(text[ko])}</p></details>' for term,text in terms)
    return f'''<section class="field-tips" id="field-tips" data-field-tips>
<div class="section-heading compact"><div><span class="section-kicker">SMALL SETTINGS / EASIER PLAY</span><h2>{t('The little things nobody explained.','아무도 설명해주지 않았던 작은 팁.')}</h2></div></div>
<p class="field-tips-intro">{t('Try a control here, then use the original KR capture to find it in your game. Practice controls only affect this page.','여기서 먼저 눌러보고, 원본 캡처와 내 게임 메뉴를 비교해보세요. 연습 버튼은 이 페이지에서만 작동해요.')}</p>
<div class="field-tip-grid">{''.join(cards)}</div>
<section class="party-reader"><span class="section-kicker">READ A PARTY POST</span><h3>{t('What does this recruitment post mean?','파티 모집글, 무슨 뜻인가요?')}</h3><p class="tiny">{t('Open each part of this sample.','예시의 각 부분을 눌러보세요.')}</p><div class="party-tokens">{decoder}</div></section>
<details class="tip-local-check"><summary>{t('Check these in your own region','내 서버에서 다시 확인할 내용')}</summary><p>{t('Market prices and fees, activity resets and entry requirements change. Compare the same item and quantity; read the current game screen before spending.','거래소 가격·수수료, 콘텐츠 초기화, 입장 조건은 달라질 수 있어요. 같은 아이템·수량으로 비교하고, 소비 전 현재 게임 화면을 확인하세요.')}</p></details>
{source_note(lang)}<noscript><style>.field-tips .tip-demo{{display:none}}</style></noscript></section>'''

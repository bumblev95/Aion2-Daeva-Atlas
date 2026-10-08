"""Source-linked settings reference. Screenshots are previewed from and linked to their original source."""
from html import escape

SOURCE = 'https://m.inven.co.kr/board/aion2/6444/2116'
AUTHOR = '구원의노래'
SOURCE_DATE = '2026-07-20'
REVIEW_DATE = '2026-10-08'
IMAGE_ROOT = 'https://upload3.inven.co.kr/upload/2026/07/19/bbs/'

TIPS = [
    dict(id='rear', title=('Find the boss’s back', '보스 뒤쪽 찾기'),
         path=('Settings → Information → Combat → Boss direction marker: BACK', '환경 설정 → 정보 출력 → 전투 → 보스 방향 마커 표시: BACK'),
         copy=('A direction reference for locating the boss’s rear.', '보스의 뒤쪽 방향을 구분하는 위치 표시입니다.'),
         image='i1231953989.png'),
    dict(id='chat', title=('See when a message arrived', '채팅이 언제 왔는지 보기'),
         path=('Chat settings → Timestamp: ON', '채팅 설정 → 시간 표시: ON'),
         copy=('Timestamps help separate new messages from old ones.', '메시지가 작성된 시간을 표시해 파티 안내의 맥락을 구분합니다.'),
         image='i1130386215.png'),
    dict(id='auto', title=('Check automatic consumables', '자동 사용 조건 확인하기'),
         path=('Settings → Combat → Auto Use', '환경 설정 → 전투 → 자동 사용'),
         copy=('Health conditions and combat-only buff use are separate options.', '물약의 생명력 조건과 버프의 전투 중 사용은 별도 설정입니다.'),
         image='i1520372560.png'),
    dict(id='bag', title=('Review before extracting', '추출 전에 목록 확인하기'),
         path=('Inventory → Extraction → Selection settings', '가방 → 추출 → 간편 선택 설정'),
         copy=('Inspect selected equipment first. Keep automatic extraction off while learning.', '선택된 장비를 먼저 확인하세요. 선택 기준이 정리되기 전에는 자동 추출을 꺼두는 편이 안전합니다.'),
         image='i1583568305.png'),
]


def source_note(lang):
    ko = lang == 'ko'
    title = '실전 팁 출처' if ko else 'Practical-tip source'
    text = ('한국 서버 유저 글과 캡처 기준입니다. 글로벌 메뉴·규칙은 다를 수 있습니다.' if ko else
            'Based on KR player captures; English labels are explanatory translations. Global menus and rules may differ.')
    return f'''<details class="evidence"><summary>{title} · {AUTHOR}</summary>
<p>{text}</p><p><a href="{SOURCE}" target="_blank" rel="noopener noreferrer">구원의노래 · 아이온2 처음하는 사람들을 위한 노하우 ↗</a></p>
<p class="small muted">KR · {SOURCE_DATE} · {'검토' if ko else 'Reviewed'} {REVIEW_DATE}</p></details>'''


def panel(lang):
    ko=lang=='ko';t=lambda en,kr:kr if ko else en
    advice={
      'rear':('The BACK marker makes the rear direction easier to read. It is a position reference, not a guarantee that the area is safe.', 'BACK 표시는 보스의 뒤쪽 방향을 구분하는 기준입니다. 후방에 있다는 것과 해당 공격의 안전지대에 있다는 것은 별개입니다.'),
      'chat':('Timestamps provide context for party instructions and recruitment messages, especially when several messages arrive together.', '파티 지시나 모집 메시지가 언제 올라왔는지 구분할 수 있습니다. 여러 메시지가 섞일 때 이전 안내와 현재 안내를 확인하기 편합니다.'),
      'auto':('Potion HP thresholds and combat-only buff use are separate settings. Adjust them to the consumable and situation rather than copying the screenshot’s percentage.', '물약의 생명력 기준과 버프의 전투 중 사용 조건은 별도 설정입니다. 캡처의 퍼센트를 정답으로 복사하기보다 사용하는 소모품과 상황에 맞춰 구분합니다.'),
      'bag':('Review what the selection rules include before extraction. Keep automatic extraction off until the criteria match the equipment you intend to discard.', '간편 선택이 어떤 장비를 포함하는지 확인한 뒤 추출합니다. 보관할 장비가 섞이지 않는 기준을 정하기 전에는 자동 추출을 꺼두는 편이 안전합니다.'),
    }
    cards=[]
    for i,tip in enumerate(TIPS):
        key=tip['id']
        cards.append(f'''<article class="setting-reference" id="tip-{key}" data-field-tip="{key}"><header><span>{i+1:02}</span><h3>{escape(tip['title'][ko])}</h3></header><p class="setting-path"><span>{t('MENU','설정 위치')}</span>{escape(tip['path'][ko])}</p><p>{escape(advice[key][ko])}</p><figure class="setting-capture"><a href="{IMAGE_ROOT}{tip['image']}?MW=800" target="_blank" rel="noopener noreferrer"><img src="{IMAGE_ROOT}{tip['image']}?MW=800" alt="{escape(tip['title'][ko])} · {t('Korean game settings screenshot','한국 서버 실제 설정 화면')}" loading="lazy" decoding="async" referrerpolicy="no-referrer"></a><figcaption>{t('KR capture','한국 서버 캡처')} · {AUTHOR} / Inven · {SOURCE_DATE}</figcaption></figure><div class="setting-source"><a href="{IMAGE_ROOT}{tip['image']}?MW=800" target="_blank" rel="noopener noreferrer">{t('Open full screenshot','스크린샷 원본 크게 보기')} ↗</a><a href="{SOURCE}" target="_blank" rel="noopener noreferrer">{AUTHOR} · Inven ↗</a></div></article>''')
    terms=[('200k',('200,000 combat power. A sample recruitment condition, not a universal recommended threshold.','전투력 200,000. 모집 조건의 해독 예시이며 공통 권장 컷이 아닙니다.')),('3b',('Three bosses. Confirm which route the party intends to run.','보스 세 마리를 의미하는 약어입니다. 구체적인 진행 경로는 파티마다 확인이 필요합니다.')),('tp',('Teleport shorthand. Confirm whether the required travel point is ready.','텔레포트 약어입니다. 필요한 이동 거점의 준비 여부를 확인하는 맥락으로 읽습니다.'))]
    decoder=''.join(f'<div><dt>{term}</dt><dd>{escape(copy[ko])}</dd></div>' for term,copy in terms)
    return f'''<section class="field-tips" id="field-tips" data-field-tips><header class="start-reference-heading"><h2>{t('Useful settings and where to find them','편의 설정과 메뉴 위치')}</h2><p>{t('The setting, its purpose and the original screenshot are shown together. Menu paths follow the linked KR captures.','설정 위치·용도·실제 캡처를 함께 정리했습니다. 메뉴 경로는 연결된 한국 서버 원문 캡처 기준입니다.')}</p></header><div class="settings-reference-grid">{''.join(cards)}</div><section class="start-distinctions"><h2>{t('Reading party shorthand','파티 모집글 약어')}</h2><dl class="party-reference">{decoder}</dl></section><p class="reference-scope">{t('Prices, fees, reset schedules and entry requirements vary by region and patch. Check the current game screen for your server.','거래소 가격·수수료, 초기화 일정, 입장 조건은 서버와 패치에 따라 달라집니다. 현재 게임 화면의 조건을 기준으로 판단합니다.')}</p>{source_note(lang)}</section>'''

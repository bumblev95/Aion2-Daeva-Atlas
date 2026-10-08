"""Pattern-specific original references. No source media is copied or embedded.

Article text and its scene association were reviewed on BOSS_REVIEW_DATE.
YouTube playback was blocked by a human-verification challenge. Chapters below
are reported by the linked index, never represented as frame-verified timings.
"""
from html import escape as e
from urllib.parse import quote, urlparse
from fieldnotes import KR_SOURCES, BOSSES

BOSS_REVIEW_DATE = '2026-10-08'
CHAPTER_INDEX = 'https://couga54.github.io/aion2-guides/en/dungeons/'
CHAPTER_VIDEO = 'mMjaSbaVTjc'
VIDEOS = {'berk':('3OXxi7f1coQ','김호러 Horror'),
          'bakarma':('3OXxi7f1coQ','김호러 Horror'),
          'nuakum':('Hl0Ky59z8jg','만두집아들'),
          'auldor':(CHAPTER_VIDEO,'BIGSKALA'),
          'vakron':(CHAPTER_VIDEO,'BIGSKALA'),
          'kromede':(CHAPTER_VIDEO,'BIGSKALA')}

def scene(source, section, filename, chapter, kind='still'):
    s = KR_SOURCES[source]
    if source == 'expedition-tips':
        url = 'https://www.gamechosun.co.kr/dataroom/article/20260115/219539/' + filename
    else:
        url = 'https://static.inven.co.kr/column/' + s['date'].replace('-','/') + '/news/' + filename
    return dict(source=source, section=section, url=url, kind=kind,
                reviewed=BOSS_REVIEW_DATE, status='article-reviewed',
                global_verified=False, timing_verified=False,
                chapter=chapter, chapter_status='index-reported',
                video_verified=False)

# URLs were read from the original articles; image/loop links stay on the
# publisher's site. "Loop" describes the source format, not a replay audit.
SCENES = {
 'berk-cover': scene('expedition-tips', '전멸기', '862663_1768469037.jpg', 75),
 'berk-spin': scene('conquest-one', '✅휠윈드', 'i1777704511.png', 93),
 'berk-stagger': scene('conquest-one', '✅✅✅그로기 패턴', 'i1861547977.png', 123),
 'bakarma-wave': scene('conquest-one', '정복 드라웁니르 - 최종보스', 'i0156339433.webp', 165, 'loop'),
 'bakarma-dive': scene('expedition-tips', '버로우', '986304_1768470217.webp', 216, 'loop'),
 'auldor-stack': scene('conquest-two', '✅폭풍의 일격', 'i1581418761.png', 285),
 'auldor-feathers': scene('conquest-two', '✅깃털 뿌리기', 'i0307490781.webp', 270, 'loop'),
 'vakron-bind': scene('conquest-two', '✅바인드', 'i0197422466.webp', 423, 'loop'),
 'vakron-prison': scene('conquest-two', '✅기암 감옥', 'i1924459847.png', 465),
 'vakron-rings': scene('conquest-two', '✅솟구치는 가시', 'i0459863811.webp', 435, 'loop'),
 'kromede-bow': scene('fire-temple', '✅아래로 활 쏘기', 'i0386436973.webp', 524, 'loop'),
 'kromede-clones': scene('fire-temple', '✅분신 공격', 'i0117366601.webp', 612, 'loop'),
 'kromede-walls': scene('fire-temple', '✅불의 장벽', 'i1427011434.png', 570),
 'nuakum-intercept': scene('fierce-horn', '✅분신 패턴', 'i0464660879.webp', 768, 'loop'),
 'nuakum-circle': scene('fierce-horn', '✅분신 패턴', 'i1372398522.png', 768),
 'nuakum-orb': scene('fierce-horn', '✅파괴의 푸른 빛', 'i1834589360.png', 822),
}

def validate_evidence():
    """Fail publication if a pattern loses attribution or overstates this audit."""
    patterns = {b['id']+'-'+m['id']:m for b in BOSSES for m in b['mechanics']}
    if set(SCENES) != set(patterns):
        raise ValueError('Every boss pattern requires its own scene reference')
    for uid, m in patterns.items():
        ref = SCENES[uid]
        if ref['source'] != m['source'] or not ref['section']:
            raise ValueError(f'{uid}: scene must match the mechanic’s cited source')
        url = urlparse(ref['url'])
        if url.scheme != 'https' or url.hostname not in {'static.inven.co.kr','www.gamechosun.co.kr'}:
            raise ValueError(f'{uid}: scene must stay on its original publisher')
        if ref['status'] != 'article-reviewed' or ref['chapter_status'] != 'index-reported':
            raise ValueError(f'{uid}: unsupported verification claim')
        if any(ref[k] is not False for k in ('global_verified','timing_verified','video_verified')):
            raise ValueError(f'{uid}: this review did not verify Global or video timing')
        if ref['kind'] not in {'still','loop'} or type(ref['chapter']) is not int or ref['chapter'] < 0:
            raise ValueError(f'{uid}: invalid scene locator')
        for key in ('safe','success'):
            if len(m[key]) != 2 or not all(m[key]):
                raise ValueError(f'{uid}: bilingual {key} required')

def media(boss, m, lang):
    t = lambda a,b: b if lang == 'ko' else a
    uid = boss['id']+'-'+m['id']
    ref = SCENES[uid]
    source = KR_SOURCES[ref['source']]
    article = source['url']+'#:~:text='+quote(ref['section'], safe='')
    time = f"{ref['chapter']//60}:{ref['chapter']%60:02}"
    kind = t('original loop', '원본 움짤') if ref['kind']=='loop' else t('original screenshot','원본 스크린샷')
    video = VIDEOS[boss['id']]
    archived = ''
    if video[0] != CHAPTER_VIDEO:
        archived = f'<a href="https://www.youtube.com/watch?v={e(video[0])}" target="_blank" rel="noopener noreferrer">{e(video[1])} · {t("Existing KR walkthrough · full guide; scene timing not checked","기존 한국어 영상 · 전체 공략, 장면 시각 미확인")} ↗</a>'
    chapter_note = t('Index-reported chapter; playback and exact scene not verified.', '다른 가이드가 안내한 챕터이며 재생·정확한 장면은 검증하지 못했습니다.')
    if uid == 'bakarma-dive':
        chapter_note += ' '+t('This covers the broader dive phase, not a verified heading demonstration.', '잠수 단계 전체의 링크로, 머리 방향 관찰 장면을 확인한 링크는 아닙니다.')
    if uid == 'kromede-bow':
        chapter_note += ' '+t('This covers the broader bow phase, not a verified example of the KR low-HP repeat.', '활 패턴 전체의 링크로, 한국판 저체력 반복 공격을 확인한 링크는 아닙니다.')
    return f'''<section class="source-footage" data-scene-reference="{uid}" data-evidence-status="{ref['status']}" aria-labelledby="scene-{uid}">
      <h4 id="scene-{uid}">{t('Compare with the real scene','실제 장면과 비교')}</h4>
      <p class="scene-status">{t('Article reviewed','원문 대조')} {ref['reviewed']} · {t('Global unverified','글로벌 미확인')}</p>
      <a class="scene-original" href="{e(ref['url'])}" target="_blank" rel="noopener noreferrer">{t('Open','보기')} {kind} · {e(m['title'][lang=='ko'])} ↗</a>
      <p class="scene-credit">{e(source['author'])} · {e(source['publisher'])} · {source['date']} · {e(source['scope'])}</p>
      <a href="{e(article)}" target="_blank" rel="noopener noreferrer">{t('Original explanation','원본 설명')} · {e(ref['section'])} ↗</a>
      <p class="tiny muted">{t('Use the cue, position and success condition above to read this scene. Article text supports the response; a still image does not establish the full movement or timing.','위 전조·안전 위치·성공 조건과 함께 장면을 보세요. 대응은 원문 설명에 근거하며, 정지 화면만으로 전체 동작·타이밍을 확인한 것은 아닙니다.')}</p>
      <details class="scene-videos"><summary>{t('Video references & verification limits','영상 참고·확인 범위')}</summary>
        <a class="source-video-link" href="https://www.youtube.com/watch?v={CHAPTER_VIDEO}&amp;t={ref['chapter']}s" target="_blank" rel="noopener noreferrer">▶ BIGSKALA · {time}<small>{t('TW footage · Russian narration · not Global verification','대만 촬영 · 러시아어 음성 · 글로벌 검증 자료 아님')}</small></a>
        <p class="tiny muted">{chapter_note}</p>
        <a href="{CHAPTER_INDEX}" target="_blank" rel="noopener noreferrer">{t('Chapter index & attribution','챕터 안내·출처')} · Couga54 ↗</a>{archived}
        <p class="tiny muted">{t('YouTube playback could not be checked during this review. No measured distances, speeds, cast durations or current Global equivalence are asserted. Media remain with their creators; these are links, with our own bilingual explanations.','검토 중 YouTube 재생 확인이 제한되었습니다. 거리·속도·시전 시간이나 현재 글로벌판 일치를 보증하지 않습니다. 영상·이미지는 원 작성자의 사이트에 두고 자체 한영 설명과 링크만 제공합니다.')}</p>
      </details></section>'''

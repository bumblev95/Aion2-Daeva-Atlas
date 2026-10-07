"""Timestamped original gameplay; media is embedded, never rehosted."""
from html import escape as e

VIDEO='mMjaSbaVTjc'
INDEX='https://couga54.github.io/aion2-guides/en/dungeons/'
# Chapter positions cross-referenced to the linked walkthrough index.
TIMES={
 'berk':{'cover':75,'spin':93,'stagger':123},
 'bakarma':{'wave':165,'dive':216},
 'auldor':{'stack':285,'feathers':270},
 'vakron':{'bind':423,'prison':465,'rings':435},
 'kromede':{'bow':524,'clones':612,'walls':570},
 'nuakum':{'intercept':768,'circle':768,'orb':822},
}
POSTERS={
 'berk':'https://static.inven.co.kr/column/2025/11/25/news/i1417370873.png',
 'bakarma':'https://static.inven.co.kr/column/2025/11/25/news/i1188974282.png',
 'auldor':'https://static.inven.co.kr/column/2025/11/28/news/i1581418761.png',
 'vakron':'https://static.inven.co.kr/column/2025/11/28/news/i1924459847.png',
 'kromede':'https://static.inven.co.kr/column/2025/12/05/news/i1427011434.png',
 'nuakum':'https://static.inven.co.kr/column/2025/12/15/news/i1372398522.png',
}
CLIPS={
 ('bakarma','wave'):'2025/11/25/news/i0156339433.webp',
 ('bakarma','dive'):'2025/11/25/news/i0536516533.webp',
 ('auldor','feathers'):'2025/11/28/news/i0307490781.webp',
 ('vakron','bind'):'2025/11/28/news/i0197422466.webp',
 ('vakron','rings'):'2025/11/28/news/i0459863811.webp',
 ('kromede','bow'):'2025/12/05/news/i0386436973.webp',
 ('kromede','clones'):'2025/12/05/news/i0420796523.webp',
 ('nuakum','intercept'):'2025/12/15/news/i0464660879.webp',
}

def media(boss,m,lang):
    t=lambda a,b:b if lang=='ko' else a
    sec=TIMES[boss['id']][m['id']];stamp=f'{sec//60:02d}:{sec%60:02d}'
    title=m['title'][lang=='ko'];url=f'https://www.youtube.com/watch?v={VIDEO}&t={sec}s'
    clip=CLIPS.get((boss['id'],m['id']))
    return f'''<div class="mechanic-media" data-mechanic-media><div class="video-top"><span class="section-kicker">WATCH THE PATTERN</span><span>{stamp}</span></div><div class="video-screen" data-media-screen><button class="video-launch" data-video-start="{sec}" data-video-id="{VIDEO}" aria-label="{t('Play','재생')} {e(title)} {stamp}"><img src="{POSTERS[boss['id']]}" alt="{t('KR reference screenshot; video opens at the selected chapter','한국판 참고 스크린샷 · 영상은 선택한 패턴 시점에서 열립니다')}" loading="lazy"><span class="play-disc">▶</span><strong>{t('Watch this mechanic','이 패턴 영상 보기')}</strong><small>{stamp} · {t('Original gameplay','실제 플레이')}</small></button><div data-media-mount hidden></div></div><div class="media-controls"><button class="btn" data-replay-video>{t('↺ Restart chapter','↺ 패턴 다시 보기')}</button><button class="text-link" data-stop-media hidden>{t('Stop','재생 종료')}</button><a href="{url}" target="_blank" rel="noopener noreferrer">YouTube {stamp} ↗</a></div><p class="media-hint">{t('Pause at the cue. Use the player’s ⚙ menu for 0.5× speed. Then watch the movement again.','전조에서 일시정지하고, 플레이어 ⚙ 메뉴에서 0.5배속으로 이동을 다시 보세요.')}</p>{f'<button class="clip-toggle" data-kr-clip="https://static.inven.co.kr/column/{clip}">{t("Play the KR guide’s short loop","한국 공략의 짧은 반복 장면 보기")} ▷</button>' if clip else ''}<details class="evidence"><summary>{t('Footage & timestamps','영상·타임스탬프 출처')} ↗</summary><p>BIGSKALA · {t('TW-recorded walkthrough. Original-language audio. KR screenshots / optional loops: Nirr, Inven (2025). Not a Global recording.','대만판 촬영 공략. 음성은 원본 언어입니다. 한국 스크린샷·반복 장면: Nirr, 인벤 (2025). 글로벌판 촬영 영상은 아닙니다.')}</p><a href="{url}" target="_blank" rel="noopener noreferrer">BIGSKALA · YouTube ↗</a><a href="{INDEX}" target="_blank" rel="noopener noreferrer">{t('Chapter index used to locate these scenes','장면 위치를 찾는 데 참고한 챕터 목록')} ↗</a></details></div>'''

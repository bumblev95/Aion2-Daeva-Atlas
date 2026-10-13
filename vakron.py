"""Global-source full-run supplement. Original schematics, no copied media."""
from html import escape as e
from battlelab import animation

ARTICLE = 'https://aion2.vi.ki/vakron-sky-island-guide'
VIDEO = 'https://www.youtube.com/watch?v=jYqmiyFEdk8'
REVIEW_DATE = '2026-10-13'
# The article and YouTube title/description were read. Playback stalled at 0:05;
# no gameplay frames, complete transcript, or current-client equivalence audited.
EVIDENCE = dict(article_updated='2026-10-12', reviewed=REVIEW_DATE,
                article_reviewed=True, video_metadata_reviewed=True,
                video_verified=False, timing_verified=False, global_verified=False)

def lesson(uid, title, seconds, captions, note):
    return dict(id=uid, diagram='vk-'+uid, title=title, seconds=seconds,
                captions=captions, note=note, evidence=EVIDENCE.copy())

LESSONS = [
 lesson('debuff',('Debuff & Fog Spirit Stones','속박 디버프·안개 정령석'),5,
  [('Watch stacks','중첩 확인'),('Pass the stone','정령석 통과'),('Rescue a rooted ally','묶인 동료 구출')],
  ('Three stacks root you. Stones reset stacks; an ally’s hit frees you. Activate the Kibelisk checkpoint.',
   '3중첩이면 속박됩니다. 정령석으로 초기화하고, 묶인 동료는 공격해서 풉니다. 키벨리스크도 활성화하세요.')),
 lesson('hands',('First boss · hand cues','첫 보스 · 손 전조'),49,
  [('Raised hand: danger','들어 올린 손: 위험'),('Cross to the other half','반대쪽으로 이동'),('Stay behind the boss','보스 뒤쪽 유지')],
  ('Alternate halves for the slams. The tank faces the following swipes away from allies.',
   '양쪽 내려찍기를 번갈아 피하세요. 이후 휘두르기는 탱커가 동료 반대쪽으로 유도합니다.')),
 lesson('flowers',('First boss · flower & party movement','첫 보스 · 꽃과 파티 이동'),73,
  [('Destroy the flower','꽃 파괴'),('Gather all five','5명 집결'),('Move clockwise together','함께 시계 방향 이동')],
  ('After the flower breaks, leave persistent puddles together; keep the next clear area open.',
   '꽃을 부수면 지속 바닥이 생깁니다. 함께 이동해 다음에 설 공간을 남기세요.')),
 lesson('glide',('Route · jump & glide','이동 · 점프와 활강'),108,
  [('Jump right; break wall','오른쪽 이동·벽 파괴'),('Ride the current; release keys','상승 기류·방향키 놓기'),('Open wings when available','가능할 때 날개 펼치기')],
  ('PC reference: Space opens wings. Avoid W or midair dodge. Defeat the yellow-arrow enemy to open the next door.',
   'PC 영상 기준: 가능할 때 Space로 활강합니다. W·공중 회피를 피하고 노란 화살표 적으로 다음 문을 여세요.')),
 lesson('petrify',('Thamon · petrify & grab','Thamon · 석화와 잡기'),170,
  [('Avoid the small circle','작은 원 회피'),('Attack a petrified ally','석화된 동료 공격'),('Free them before the slam','내려찍기 전에 구출')],
  ('Also watch the grab and jump the arena-wide warning. No fixed safe side for the grab is established here.',
   '잡기를 경계하고 전체 바닥 전조에는 점프하세요. 잡기의 고정 안전 방향은 확인하지 못했습니다.')),
 lesson('shield',('Thamon · damage-type shield','Thamon · 피해 종류 보호막'),170,
  [('Read the shield','보호막 확인'),('Red: stop physical hits','빨강: 물리 공격 중단'),('Purple: stop magic hits','보라: 마법 공격 중단')],
  ('Matching damage heals Thamon. Resume after the matching shield fades.',
   '해당 종류의 피해는 보스를 회복시킵니다. 보호막이 사라진 뒤 공격을 재개하세요.')),
 lesson('elements',('Route · four elements','이동 · 네 원소'),220,
  [('Fly through the area','구역 비행'),('Collect four elements','네 원소 수집'),('Match each altar','해당 제단에 배치')],
  ('Use the in-game element and altar markings; this schematic does not map their actual locations.',
   '게임 안의 원소·제단 표시를 맞추세요. 이 그림은 실제 제단 위치 지도가 아닙니다.')),
 lesson('jumps',('Final boss · three jumps','최종 보스 · 연속 세 번 점프'),230,
  [('Arena-wide warning','전체 바닥 전조'),('Jump while moving clockwise','시계 방향 이동하며 점프'),('Third: watch the cast bar','세 번째: 시전 바 확인')],
  ('Time the last jump near cast completion. Root circles and unmarked half-arena strikes also return.',
   '마지막 점프는 시전 완료 직전에 맞춥니다. 속박 원과 바닥 표시 없는 반쪽 공격도 경계하세요.')),
 lesson('rock',('Final boss · red rock exit','최종 보스 · 붉은 바위 탈출'),273,
  [('Rocks enclose you','바위에 갇힘'),('Break your red rock','내 붉은 바위 파괴'),('Exit through its gap','생긴 틈으로 탈출')],
  ('Check your own enclosure; the red rock is not guaranteed to be on the side shown.',
   '자신의 감옥을 확인하세요. 붉은 바위가 그림과 같은 방향에 있다는 뜻은 아닙니다.')),
]

STAGES = [
 ('prepare',('Preparation','입장 준비'),['debuff']),
 ('first',('First boss','첫 보스'),['hands','flowers']),
 ('route',('Jump route','이동 구간'),['glide']),
 ('thamon',('Thamon','Thamon'),['petrify','shield']),
 ('altars',('Four elements','네 원소'),['elements']),
 ('final',('Final boss','최종 보스'),['jumps','rock']),
]

def validate():
    if len({m['id'] for m in LESSONS}) != 9:
        raise ValueError('Vakron lessons must have nine unique IDs')
    if [uid for _,_,ids in STAGES for uid in ids] != [m['id'] for m in LESSONS]:
        raise ValueError('Vakron route must preserve lesson order')
    for m in LESSONS:
        if any(m['evidence'][key] is not False for key in ('video_verified','timing_verified','global_verified')):
            raise ValueError('This review did not verify gameplay or current Global equivalence')
        if len(m['captions']) != 3 or any(len(x)!=2 or not all(x) for x in [m['title'],m['note'],*m['captions']]):
            raise ValueError('Every Vakron lesson requires bilingual text')

def reference(m, lang):
    t=lambda en,ko:ko if lang=='ko' else en
    seconds=m['seconds']; stamp=f'{seconds//60}:{seconds%60:02}'
    return f'''<p class="vk-source" data-vakron-source="{m['id']}" data-video-verified="false" data-timing-verified="false" data-global-verified="false"><a href="{VIDEO}&amp;t={seconds}s" target="_blank" rel="noopener noreferrer">NoBS Game Guides · {stamp} ↗</a> · <a href="{ARTICLE}" target="_blank" rel="noopener noreferrer">Vi.ki ↗</a><small>{t('Article-reported timestamp · scene not independently verified','원문 안내 시각 · 해당 장면 직접 검증 미완료')}</small></p>'''

def render(lang, base):
    t=lambda en,ko:ko if lang=='ko' else en
    root=base+('ko/' if lang=='ko' else '')
    nav=''.join(f'<a href="#vakron-{uid}">{i+1}. {e(title[lang=="ko"])}</a>' for i,(uid,title,_) in enumerate(STAGES))
    groups=''
    for i,(uid,title,ids) in enumerate(STAGES):
        cards=''
        for lid in ids:
            m=next(m for m in LESSONS if m['id']==lid)
            # Reuse the shipped controls and accessibility transcript. This is a
            # Global-source supplement, not a claim that the KR lesson is verified.
            player=animation({'id':'vakron-global'},m,lang)
            cards+=f'<article class="vk-lesson" id="vakron-lesson-{lid}"><h3>{e(m["title"][lang=="ko"])}</h3>{player}<p class="vk-note">{e(m["note"][lang=="ko"])}</p>{reference(m,lang)}</article>'
        groups+=f'<details class="vk-stage" id="vakron-{uid}" {"open" if i==0 else ""}><summary><span>0{i+1}</span>{e(title[lang=="ko"])}</summary><div class="vk-lessons">{cards}</div></details>'
    return f'''<section class="vk-guide" aria-labelledby="vakron-run-title" data-vakron-guide><span class="section-kicker">VAKRON · FULL RUN</span><h2 id="vakron-run-title">{t('From the first stone to the final escape','첫 정령석부터 마지막 탈출까지')}</h2><p>{t('Global Normal guide supplement · read a stage, watch the cue, then move.','글로벌 일반 난이도 공략 보강 · 구간을 열고 전조와 이동을 확인하세요.')}</p><details class="vk-evidence"><summary>{t('Source & verification limits','출처·검증 범위')}</summary><p>{t('Vi.ki article reviewed; YouTube title/description checked. Playback stalled. Gameplay, exact timing and current server equivalence remain unverified.','Vi.ki 본문과 YouTube 제목·설명을 대조했습니다. 재생이 버퍼링돼 실제 장면·정확한 타이밍·현행 서버 일치는 미검증입니다.')} {REVIEW_DATE}.</p><p><a href="{VIDEO}">NoBS Game Guides · 2026-10-04 ↗</a> · <a href="{ARTICLE}">Vi.ki · 2026-10-12 ↗</a></p><small>{t('Vi.ki text: CC BY-SA 4.0. Our adapted bilingual notes: CC BY-SA 4.0. Original teaching art; source video remains with its creator.','Vi.ki 본문 및 이를 바탕으로 작성한 한영 설명: CC BY-SA 4.0. 학습 그림은 자체 제작이며 원본 영상은 작성자에게 있습니다.')} <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0 ↗</a></small></details><nav class="vk-route" aria-label="{t('Vakron run stages','바크론 진행 구간')}">{nav}</nav>{groups}<noscript><style>.vk-guide .battle-controls{{display:none}}</style></noscript><p class="vk-legacy-note">{t('The KR archive below keeps its original three patterns, including a separate binding follow-up. The Global source describes three jumps; this is not proof of identical KR/Global sequencing.','아래 한국판 자료의 기존 3개 패턴과 별도 속박 후속타 설명은 보존했습니다. 글로벌 출처의 세 번 점프 설명만으로 두 버전의 순서가 같다고 단정하지 않습니다.')}</p><a class="text-link" href="{root}dungeons/vakron-island/?mechanic=bind#mechanic-vakron-bind">{t('Original KR final-boss patterns','기존 한국판 최종 보스 패턴')} ↓</a></section>'''

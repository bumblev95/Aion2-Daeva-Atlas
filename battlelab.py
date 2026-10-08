"""Original animated teaching scenes, based on the attributed KR encounter notes."""
from html import escape as e
import json
CAPTIONS={
 'cover': [('Yellow rocks appear','노란 바위가 올라와요'),('Move close before the blast','폭발 전에 바위로 접근해요'),('Check the protection effect','보호 버프가 생겼는지 확인해요')],
 'out':[('Watch the boss wind-up','보스의 전조를 봐요'),('Leave the nearby danger area','가까운 위험 범위에서 나와요'),('Wait for the attack to end','공격이 끝난 뒤 돌아가요')],
 'stagger':[('Wait for the locked bar to open','잠긴 그로기 게이지가 열려요'),('Use skills with stagger damage','그로기 피해가 있는 스킬을 써요'),('The party empties the bar together','파티가 함께 게이지를 깎아요')],
 'jump':[('The ring travels toward you','고리가 내 쪽으로 다가와요'),('Jump before the ring touches you','고리가 닿기 전에 점프해요'),('Read the next wave before landing','착지 후 다음 공격도 확인해요')],
 'track':[('Observe the head as it dives','잠수하는 머리 방향을 봐요'),('Look for its underwater silhouette','물속 윤곽이 있는지 살펴봐요'),('No fixed return route is established','정해진 등장 경로를 뜻하지는 않아요')],
 'stack':[('One player receives a mark','한 명에게 징표가 생겨요'),('Move toward the marked ally','징표 대상에게 모여요'),('Share the incoming hit','함께 피해를 나눠 받아요')],
 'fan':[('The boss aims forward','보스가 정면을 향해요'),('Move out of the fan','부채꼴 정면에서 벗어나요'),('If caught, use shock removal','맞아 행동이 막히면 충격 해제')],
 'rescue':[('Green health bar: keep clear','초록 체력바 대상 주변을 비워요'),('Once bound, attack the vines','묶인 뒤 덩굴을 공격해요'),('Free the ally without spreading the hit','공격에 휘말리지 않고 동료를 풀어요')],
 'prison':[('Stagger locks; rocks enclose you','그로기가 잠기고 바위에 갇혀요'),('Attack the red rock','붉은 바위를 공격해요'),('Exit through that rock’s opening','부순 붉은 바위의 틈으로 탈출해요')],
 'spread':[('The boss centres; clones target players','보스가 중앙으로 가고 분신이 붙어요'),('Spread before the clone hits','분신 공격 전에 동료와 떨어져요'),('Evade both hits without overlap','두 공격 모두 겹치지 않게 피해요')],
 'walls':[('A wall approaches with a gap','빈틈이 있는 불벽이 다가와요'),('Move sideways to line up','옆으로 움직여 빈틈에 맞춰요'),('Pass through; watch the next wall','통과하고 다음 불벽을 봐요')],
 'intercept':[('The target cannot move','징표 대상은 움직일 수 없어요'),('An unmarked ally steps into the line','상처 없는 동료가 앞을 막아요'),('Intercept, then change the blocker','막아준 뒤 다음 담당자와 교대해요')],
 'circles':[('Read the size of the circle','낙하 원의 크기를 봐요'),('Large: leave the target alone','큰 원: 대상 혼자 맞아요'),('Small: gather and share','작은 원: 동료가 모여 함께 맞아요')],
 'orb':[('Central energy; a player is marked','중앙 에너지가 생기고 대상이 정해져요'),('Re-align boss → energy → target','매번 보스 → 에너지 → 대상으로 정렬해요'),('Three hits within four opportunities','네 번의 기회 안에 세 번 적중시켜요')],
}
def animation(b,m,lang):
 t=lambda a,k:k if lang=='ko' else a
 captions=[x[lang=='ko'] for x in CAPTIONS[m['diagram']]]
 uid=b['id']+'-'+m['id']
 if uid=='berk-spin':captions=[t('Red particles: the spin is coming','붉은 가루: 회전 공격 전조예요'),t('Retreat; the spinning boss can chase','물러나요. 회전 중인 보스가 추격해요'),t('A stationary safe circle is not guaranteed','처음 범위 밖도 계속 안전하진 않아요')]
 if uid=='kromede-bow':captions=[t('Bow down: leave the boss-centred fire','활을 내리면 보스 주변 화염에서 이탈'),t('Hold outside through the attack','공격이 이어지는 동안 밖에서 기다려요'),t('Low HP can bring two bursts','저체력에는 두 번 연속 사용해요')]
 if b['id']=='bakarma' and m['id']=='wave':captions[2]=t('Land, approach and use stagger skills','착지 후 접근해서 그로기 스킬을 써요')
 if b['id']=='vakron' and m['id']=='rings':captions=[t('Red floor: rings and straight attacks','붉은 바닥: 고리와 직선 공격이에요'),t('Sidestep lines; jump each of three rings','직선을 옆으로 피하며 고리 세 번 점프'),t('Jump once more for the binding follow-up','세 번째 뒤 속박 후속타에도 한 번 더 점프')]
 transcript=''.join(f'<li>{e(caption)}</li>' for caption in captions)
 return f'''<section class="battle-player" data-animation="{m['diagram']}" data-encounter="{uid}" data-captions="{e(json.dumps(captions,ensure_ascii=False))}" data-stage="0"><div class="battle-top"><span><i></i> {t('AUTO PLAY · PATTERN LESSON','자동 재생 · 패턴 학습')}</span><b data-animation-phase>01 / 03</b></div><svg class="battle-scene" data-battle-scene viewBox="0 0 640 390" role="img" aria-describedby="lesson-{uid}" aria-label="{e(t('Animated response: ','움직이는 대응: ')+m['title'][lang=='ko'])}"><rect width="640" height="390" fill="#0e1623"/><text x="320" y="195" fill="#d9e3ff" text-anchor="middle">{e(captions[0])}</text></svg><p class="battle-caption" data-animation-caption aria-live="off">{e(captions[0])}</p><div class="battle-controls"><button data-animation-toggle aria-label="{t('Pause animation','애니메이션 일시정지')}">Ⅱ</button><button data-animation-replay aria-label="{t('Replay animation','애니메이션 처음부터')}">↺</button><input data-animation-seek type="range" min="0" max="1000" value="0" aria-label="{t('Animation progress','애니메이션 진행 위치')}"><label><span class="sr-only">{t('Playback speed','재생 속도')}</span><select data-animation-speed><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label></div><div class="battle-legend"><span><i class="you"></i>{t('You / allies','나·동료')}</span><span><i class="danger"></i>{t('Attack','공격')}</span><span><i class="safe"></i>{t('Response position','대응 위치')}</span></div><details class="battle-transcript"><summary>{t('Read the lesson steps','단계별 설명 읽기')}</summary><ol id="lesson-{uid}">{transcript}</ol></details><small class="battle-disclaimer">{t('Teaching schematic · example positions, party size and pacing, not a measured replay. Only the response order is illustrated. Use the real cue for timing; Global equivalence remains unverified.','학습 개념도 · 위치·인원·진행 속도는 예시이며 실측 재현이 아닙니다. 대응 순서만 설명합니다. 실제 전조로 타이밍을 판단하세요. 글로벌 일치 미확인.')}</small></section>'''

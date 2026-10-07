"""Original animated teaching scenes, based on the attributed KR encounter notes."""
from html import escape as e
import json
CAPTIONS={
 'cover': [('Yellow rocks appear','노란 바위가 올라와요'),('Move close before the blast','폭발 전에 바위로 접근해요'),('Check the protection effect','보호 버프가 생겼는지 확인해요')],
 'out':[('Watch the boss wind-up','보스의 전조를 봐요'),('Leave the nearby danger area','가까운 위험 범위에서 나와요'),('Wait for the attack to end','공격이 끝난 뒤 돌아가요')],
 'stagger':[('Wait for the locked bar to open','잠긴 그로기 게이지가 열려요'),('Use skills with stagger damage','그로기 피해가 있는 스킬을 써요'),('The party empties the bar together','파티가 함께 게이지를 깎아요')],
 'jump':[('The ring travels toward you','고리가 내 쪽으로 다가와요'),('Jump as the ring reaches you','고리가 닿을 때 점프해요'),('Read the next wave before landing','착지 후 다음 공격도 확인해요')],
 'track':[('Watch the head as it dives','잠수하는 머리 방향을 봐요'),('Follow the underwater silhouette','물속 윤곽을 따라가요'),('Stay ready for its return','다시 나올 때 대응을 준비해요')],
 'stack':[('One player receives a mark','한 명에게 징표가 생겨요'),('Move toward the marked ally','징표 대상에게 모여요'),('Share the incoming hit','함께 피해를 나눠 받아요')],
 'fan':[('The boss aims forward','보스가 정면을 향해요'),('Move out of the fan','부채꼴 정면에서 벗어나요'),('If controlled, use Defiance','맞아 행동이 막히면 충격 해제')],
 'rescue':[('A teammate is marked','대상 주변을 비워줘요'),('Vines hold that player','덩굴에 묶인 동료를 확인해요'),('Attack the vines to free them','동료를 묶은 덩굴을 공격해 풀어요')],
 'prison':[('You are pulled into a rock ring','바위 감옥 안으로 끌려가요'),('Attack the red rock','붉은 바위를 공격해요'),('Exit through the opening','열린 틈으로 나와 폭발을 피해요')],
 'spread':[('Personal clone attacks start','각자에게 분신 공격이 와요'),('Move away from teammates','동료와 거리를 벌려요'),('Keep the attacks from overlapping','서로의 공격 범위가 겹치지 않게 해요')],
 'walls':[('A wall approaches with a gap','빈틈이 있는 불벽이 다가와요'),('Move sideways to line up','옆으로 움직여 빈틈에 맞춰요'),('Pass through; watch the next wall','통과하고 다음 불벽을 봐요')],
 'intercept':[('The target cannot move','징표 대상은 움직일 수 없어요'),('An unmarked ally steps into the line','상처 없는 동료가 앞을 막아요'),('Intercept, then change the blocker','막아준 뒤 다음 담당자와 교대해요')],
 'circles':[('Read the size of the circle','낙하 원의 크기를 봐요'),('Large: leave the target alone','큰 원: 대상 혼자 맞아요'),('Small: gather and share','작은 원: 동료가 모여 함께 맞아요')],
 'orb':[('Energy appears in the center','중앙에 에너지가 생겨요'),('Line up boss → orb → target','보스 → 에너지 → 대상 순으로 서요'),('Guide all three shots through it','세 발을 에너지 쪽으로 유도해요')],
}
def animation(b,m,lang):
 t=lambda a,k:k if lang=='ko' else a
 captions=[x[lang=='ko'] for x in CAPTIONS[m['diagram']]]
 if b['id']=='bakarma' and m['id']=='wave':captions[2]=t('Land, approach and use stagger skills','착지 후 접근해서 그로기 스킬을 써요')
 if b['id']=='vakron' and m['id']=='rings':captions=[t('Three rings, then another blast','고리 세 번 뒤에도 끝이 아니에요'),t('Jump for each incoming ring','세 번의 고리를 각각 점프해요'),t('One more jump for the final attack','세 번째 뒤 후속 공격에도 한 번 더 점프')]
 return f'''<section class="battle-player" data-animation="{m['diagram']}" data-encounter="{b['id']}-{m['id']}" data-captions="{e(json.dumps(captions,ensure_ascii=False))}" data-stage="0"><div class="battle-top"><span><i></i> {t('AUTO PLAY · PATTERN LESSON','자동 재생 · 패턴 학습')}</span><b data-animation-phase>01 / 03</b></div><svg class="battle-scene" data-battle-scene viewBox="0 0 640 390" role="img" aria-label="{e(t('Animated response: ','움직이는 대응: ')+m['title'][lang=='ko'])}"><rect width="640" height="390" fill="#0e1623"/><text x="320" y="195" fill="#d9e3ff" text-anchor="middle">{e(captions[0])}</text></svg><p class="battle-caption" data-animation-caption>{e(captions[0])}</p><div class="battle-controls"><button data-animation-toggle aria-label="{t('Pause animation','애니메이션 일시정지')}">Ⅱ</button><button data-animation-replay aria-label="{t('Replay animation','애니메이션 처음부터')}">↺</button><input data-animation-seek type="range" min="0" max="1000" value="0" aria-label="{t('Animation progress','애니메이션 진행 위치')}"><label><span class="sr-only">{t('Playback speed','재생 속도')}</span><select data-animation-speed><option value="0.5">0.5×</option><option value="1" selected>1×</option><option value="2">2×</option></select></label></div><div class="battle-legend"><span><i class="you"></i>{t('You / allies','나·동료')}</span><span><i class="danger"></i>{t('Attack','공격')}</span><span><i class="safe"></i>{t('Response position','대응 위치')}</span></div><small class="battle-disclaimer">{t('Teaching animation · distances, speed and player count are illustrative. Use the actual boss cue for timing.','학습용 애니메이션 · 거리·속도·인원 배치는 예시예요. 실제 타이밍은 보스 전조에 맞추세요.')}</small></section>'''

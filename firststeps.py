"""Practical starting priorities without simulated gameplay or lesson gates."""
from html import escape

TOPICS = [
    ('progress', ('Main progression and travel', '메인 진행과 동선'),
     ('Use the Episode quest as your route; check prerequisites when progress stops.', '메인 에피소드를 진행 축으로 잡고, 막힌 구간에서는 선행 조건부터 확인합니다.'),
     ('Include travel points and nearby growth content in that route. Compare the reward before making a long detour.', '이동 거점과 동선 근처 성장 콘텐츠를 함께 챙기는 방식입니다. 멀리 우회할 콘텐츠는 보상을 먼저 비교합니다.'),
     ('Identify the blocked requirement before spending more time grinding.', '다음 퀘스트가 막힌 이유를 확인하지 않은 채 사냥량만 늘리는 것은 비효율적입니다.'),
     'maps/', ('Check locations on the map', '지도에서 위치 확인')),
    ('skills', ('Skill investment priorities', '스킬 투자 순서'),
     ('Start with your class’s core skills and their conditions, then decide where points go.', '주력 스킬과 발동 조건을 먼저 파악한 뒤 포인트 투자 순서를 정합니다.'),
     ('The class build guide covers early priorities, passive effects and Stigma choices. Allocated points and total skill level are separate checks.', '직업별 빌드에서 우선 투자할 기술·패시브·스티그마를 함께 확인할 수 있습니다. 직접 투자한 포인트와 합계 스킬 레벨은 구분해야 합니다.'),
     ('A rotation makes more sense when its trigger conditions, range and cooldowns are clear.', '딜 사이클만 외우기보다 어떤 조건에서 기술이 연결되는지 알아야 실제 전투에 적용하기 쉽습니다.'),
     'skills/', ('Class skills and investment order', '직업별 스킬·투자 순서')),
    ('gear', ('Equipment and enhancement', '장비 교체와 강화'),
     ('Compare the same equipment slot and the options that help your current goal.', '같은 부위의 장비를 비교하고, 현재 필요한 옵션과 교체 계획을 기준으로 강화 여부를 판단합니다.'),
     ('Separate entry requirements from survival, accuracy and damage. Identify the problem an upgrade is meant to solve before spending materials.', '입장 조건을 맞추려는 것인지, 생존·명중·피해량을 보완하려는 것인지 먼저 구분합니다. 강화 비용은 해결하려는 문제와 함께 봐야 합니다.'),
     ('A higher equipment score alone does not explain whether its options suit your build.', '장비 점수가 높다는 이유만으로 현재 세팅에 모든 옵션이 유효한 것은 아닙니다.'),
     'gear/', ('Equipment stats and upgrade decisions', '장비·스탯·강화 판단')),
    ('party', ('Preparing for a first dungeon', '첫 던전 준비'),
     ('Match the difficulty and party expectations, then review the mechanics that can end a run.', '난이도·입장 조건·파티 모집 조건을 확인한 뒤, 전멸이나 큰 손실로 이어지는 패턴부터 파악합니다.'),
     ('A useful boss guide answers three questions: what is the cue, where do I move, and what is my role?', '보스 공략은 전조가 무엇인지, 어디로 이동하는지, 내 역할이 무엇인지로 나눠 보면 핵심이 명확해집니다.'),
     ('A power figure in a recruitment post is that party’s condition, not a universal recommendation.', '모집글의 전투력 수치는 해당 파티의 조건입니다. 모든 서버·난이도에 적용되는 권장 컷으로 해석하지 않습니다.'),
     'dungeons/', ('Boss mechanics and movement', '보스별 패턴·이동 위치')),
]

def overview(lang, base):
    ko=lang=='ko';t=lambda en,kr:kr if ko else en;r=base+('ko/' if ko else '')
    cards=[]
    for i,(key,title,priority,reason,caution,url,label) in enumerate(TOPICS):
        cards.append(f'''<article class="start-topic" id="core-{key}"><div class="start-topic-title"><span>{i+1:02}</span><h3>{escape(title[ko])}</h3></div><p class="start-priority">{escape(priority[ko])}</p><p>{escape(reason[ko])}</p><p class="start-caution">{escape(caution[ko])}</p><a href="{r}{url}">{escape(label[ko])} →</a></article>''')
    distinctions=[
      (('Character level / skill level','캐릭터 레벨 / 스킬 레벨'),('Character progression and the level of an individual skill are different. Each skill has its own requirements and costs.','캐릭터의 성장 단계와 개별 기술의 레벨은 다릅니다. 스킬 투자에는 해당 기술의 조건과 비용이 따로 적용됩니다.')),
      (('Item level / useful options','아이템 레벨 / 유효 옵션'),('Equipment level, equip requirements and useful options answer different questions. Compare the same slot and purpose.','장비 수준·착용 조건·옵션의 효율은 별개입니다. 같은 부위와 목적의 장비끼리 비교해야 합니다.')),
      (('Stigma / Arcana','스티그마 / 아르카나'),('Stigma belongs to skill setup. Arcana is equipment, not a skill in a rotation.','스티그마는 스킬 세팅, 아르카나는 장비에 해당합니다. 아르카나 이름을 딜 사이클에 사용하는 기술과 혼동하지 않습니다.'))]
    terms=''.join(f'<div><dt>{escape(label[ko])}</dt><dd>{escape(copy[ko])}</dd></div>' for label,copy in distinctions)
    return f'''<section class="start-reference"><header class="start-reference-heading"><h2>{t('Four priorities for a first character','첫 캐릭터 육성의 핵심 4가지')}</h2><p>{t('Progression, skills, equipment and dungeon preparation — with a direct link to each detailed guide.','메인 진행, 스킬 투자, 장비 판단, 던전 준비를 기준으로 정리했습니다. 필요한 항목에서 상세 공략으로 이어집니다.')}</p></header><div class="start-topic-grid">{''.join(cards)}</div><section class="start-distinctions"><h2>{t('Distinctions that affect your build','세팅할 때 혼동하기 쉬운 구분')}</h2><dl>{terms}</dl></section></section>'''

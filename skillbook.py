"""A small, sourced bilingual skill dictionary; original beginner explanations."""
import html
import json
import re
from content import CLASSES

REVIEW = '2026-10-07'

def skill(slug, en, ko, cls, kind, cooldown, reach, effect, use, watch, aliases=()):
    return dict(id=slug,en=en,ko=ko,cls=cls,kind=kind,cooldown=cooldown,reach=reach,effect=effect,use=use,watch=watch,aliases=aliases,url='https://metabot.gg/en/aion-2/skills/'+slug)

SKILLS = [
 skill('leaping-slam','Leaping Slam','도약찍기','gladiator','active','15s','20m',
 ('Leap to an enemy, deal damage and contribute to stagger. Prepare for Battle is a specialization, not the base skill.','적에게 뛰어들어 피해와 그로기 피해를 줍니다. 전투 준비는 기본 효과가 아니라 특화 선택입니다.'),
 ('Close the gap after checking the landing area.','착지 지점의 장판을 확인하고 접근하세요.'),
 ('The KR buff-order tip assumes the matching specialization.','한국 버프 순서 팁은 해당 특화를 선택한 상황입니다.')),
 skill('ruinous-blow','Ruinous Blow','파멸의 맹타','gladiator','active','45s','7.5m',
 ('A rushing area attack that also grants Prepare for Battle for 20 seconds.','돌진 후 주변을 공격하고 20초간 전투 준비 효과를 얻습니다.'),
 ('Plan a safe attack window before using the buff.','버프를 활용할 수 있는 안전한 공격 시간을 먼저 확보하세요.'),
 ('Do not spend the buff while the boss is leaving.','보스가 사라지기 직전에 쓰면 버프 시간을 놓칩니다.')),
 skill('zikels-blessing',"Zikel’s Blessing",'지켈의 축복','gladiator','stigma','120s','self',
 ('Temporarily increases your Attack and Accuracy. The stagger bonus requires a specialization.','일시적으로 자신의 공격력과 명중을 높입니다. 그로기 증가 효과는 특화가 필요합니다.'),
 ('Align your damage window or a planned stagger check.','집중 공격 또는 약속한 그로기 구간에 맞추세요.'),
 ('A skill name alone does not tell you which specializations a guide uses.','스킬 이름만 같다고 공략과 같은 특화 효과를 얻는 것은 아닙니다.')),
 skill('ambush','Ambush','기습','assassin','active','10s','4m',
 ('A close attack with 30% more damage when it lands as a back attack.','근접 공격이며 후방 공격으로 적중하면 피해가 30% 증가합니다.'),
 ('Find the boss’s back after it finishes turning.','보스가 방향을 바꾼 뒤 후방을 다시 잡으세요.'),
 ('A safe position matters more than chasing the rear through a lethal attack.','치명적인 장판을 뚫고 후방 보너스를 쫓지는 마세요.')),
 skill('heart-gore','Heart Gore','심장찌르기','assassin','active','5s','4m',
 ('Becomes available after a critical hit; damages nearby enemies and restores MP.','치명타 후 활성화되며 가까운 적을 공격하고 정신력을 회복합니다.'),
 ('Watch for the activation prompt during your attack sequence.','공격 중 활성화 표시를 확인하세요.'),
 ('Critical-hit triggers and specializations change its use count.','치명타 발동과 특화에 따라 사용 횟수가 달라집니다.')),
 skill('power-of-the-storm','Power of the Storm','질풍의 권능','chanter','stigma','120s','40m',
 ('Gives combat speed and cooldown benefits to you and nearby allies. It conflicts with the Cleric’s Earth’s Blessing effect.','자신과 주변 파티원의 전투 속도·재사용 시간을 지원합니다. 치유성 대지의 은총 효과와 동시 적용 제한이 있습니다.'),
 ('Call the buff when your party is ready to attack.','파티가 공격할 수 있는 시점에 사용을 알리세요.'),
 ('Party and self effects differ; coordinate with the healer.','자신과 파티원 효과가 다르므로 치유성과 맞춰보세요.')),
 skill('impactful-crush','Impactful Crush','타격쇄','chanter','active','15s','20m',
 ('A ranged strike with a stun effect. It opens Dark Crush for two seconds.','원거리 타격과 기절 효과가 있으며 2초 동안 암격쇄를 사용할 수 있게 합니다.'),
 ('Use the follow-up prompt while you are away from melee range.','근접할 수 없을 때 후속 스킬 표시를 확인하세요.'),
 ('Boss immunity can prevent control effects.','보스의 면역 때문에 제어 효과가 적용되지 않을 수 있습니다.')),
 skill('dark-crush','Dark Crush','암격쇄','chanter','active','5s','20m',
 ('A mobile ranged follow-up opened by Impactful Crush.','타격쇄에서 이어지는 이동 가능한 원거리 후속 공격입니다.'),
 ('Follow the active chain prompt, then return to a safe position.','연계 표시가 켜졌을 때 사용하고 안전한 위치로 복귀하세요.'),
 ('Specializations can add a further chain or remove its cooldown.','추가 연계와 재사용 시간 제거는 특화 효과입니다.')),
 skill('bolt','Bolt','벽력','cleric','active','45s','20m',
 ('A wind area attack with up to three charge levels; more charging increases its damage and stagger contribution.','최대 3단계 차징하는 바람 속성 광역 공격입니다. 차징에 따라 피해와 그로기 피해가 커집니다.'),
 ('Charge when the party is stable and you can finish safely.','파티 체력이 안정적이고 시전을 마칠 수 있을 때 쓰세요.'),
 ('Keep urgent healing accessible during a damage sequence.','공격 중에도 긴급 회복기를 바로 누를 수 있게 두세요.')),
 skill('hellfire','Hellfire','지옥의 화염','sorcerer','active','45s','20m',
 ('A fire area attack with three charge levels. Casting while moving requires its movement specialization.','3단계 차징하는 화염 광역 공격입니다. 이동 시전에는 이동 가능 특화가 필요합니다.'),
 ('Start after reading the next boss movement.','보스의 다음 움직임을 확인한 뒤 차징하세요.'),
 ('A KR progression build may choose mobility over another specialization.','한국 트라이 세팅은 다른 특화 대신 이동 가능을 선택할 수 있습니다.')),
 skill('summon-ancient-spirit','Summon: Ancient Spirit','소환: 고대의 정령','spiritmaster','stigma','90s','20m',
 ('Summons an Ancient Spirit for 30 seconds. Its skills grant Four Elements to the caster.','30초 동안 고대의 정령을 소환합니다. 정령 스킬은 시전자에게 사대원소 상태를 부여합니다.'),
 ('Plan the summon around a period when the target stays available.','공격 대상을 계속 때릴 수 있는 구간에 소환하세요.'),
 ('The KR snapshotting claim is a player observation, not a confirmed Global rule.','한국 공략의 소환 시점 능력치 적용은 유저 관찰이며 글로벌 확정 규칙은 아닙니다.'),('고대의 정령','소환:고대의 정령')),
 skill('jointstrike-destructive-attack','Jointstrike: Destructive Attack','협공: 파멸의 공세','spiritmaster','stigma','60s','20m',
 ('You and your summoned spirit attack together. The spirit’s contribution depends on which spirit is active.','시전자와 소환 정령이 함께 공격합니다. 소환된 정령 종류에 따라 정령의 공격이 달라집니다.'),
 ('Check the summon is present before starting the attack.','사용하기 전에 소환 상태부터 확인하세요.'),
 ('Do not assume a two-spirit KR sequence works identically on Global.','한국의 두 정령 연계가 글로벌에서도 동일하다고 단정하지 마세요.'),('파멸의 공세','협공:파멸의 공세')),
 skill('elemental-fusion','Elemental Fusion','원소융합','spiritmaster','active','—','20m',
 ('Spirit skills build elements. Four stacks enable this attack, which consumes Four Elements.','정령 스킬로 원소를 모읍니다. 4중첩의 사대원소 상태에서 사용하며 사용 후 해당 상태를 소모합니다.'),
 ('Check the ready indicator rather than looking for a fixed rotation timer.','고정 시간표보다 사용 가능 표시를 확인하세요.'),
 ('You cannot gain more elements while Four Elements remains active.','사대원소 상태에서는 원소를 추가로 얻을 수 없습니다.')),
 skill('seize-magic','Seize Magic','마법 강탈','spiritmaster','stigma','90s','20m',
 ('An area attack that removes up to two buffs; removed buffs add damage.','범위 공격과 함께 최대 2개의 강화 효과를 제거하며 제거 수에 따라 추가 피해를 줍니다.'),
 ('Check the enemy’s remaining buffs before committing your burst.','사용 후 상대에게 남은 버프를 보고 집중 공격하세요.'),
 ('“Up to two” does not guarantee removal of a specific defensive buff.','최대 2개 제거가 원하는 방어 버프의 제거를 보장하지는 않습니다.')),
 skill('defiance-cleric','Defiance','충격 해제','cleric','active','60s','self',
 ('Removes listed control effects, including stun and airborne, and gives five seconds of status immunity.','기절·공중 속박 등 명시된 제어 효과를 제거하고 5초간 상태 이상 면역을 얻습니다.'),
 ('Keep it reachable for a dangerous control-to-damage sequence.','제어 직후 큰 피해가 이어질 때 바로 누를 수 있게 두세요.'),
 ('This entry uses the Cleric version at skill level 1. Cooldown changes with skill level.','이 문서는 치유성 버전의 스킬 1레벨 기준입니다. 스킬 레벨에 따라 재사용 시간이 달라집니다.')),
 skill('taunt','Taunt','도발','templar','stigma','30s','20m',
 ('Deals damage and raises enmity. It also weakens the target’s Attack and Accuracy.','피해와 함께 적대치를 높이고 대상의 공격력과 명중을 낮춥니다.'),
 ('Use it to support the group’s agreed tank assignment.','파티에서 합의한 탱킹 역할에 맞춰 사용하세요.'),
 ('PvP taunt is chance-based; threat is not a promise of forced boss targeting.','PvP 도발은 확률 효과이며 적대치 증가가 모든 보스의 타깃 강제를 보장하지는 않습니다.')),
 skill('snipe','Snipe','저격','ranger','active','—','20m',
 ('A ranged wind attack that restores MP.','정신력을 회복하는 원거리 바람 속성 공격입니다.'),
 ('Notice how this basic attack supports your resource flow.','기본 공격이 정신력 흐름을 어떻게 돕는지 확인하세요.'),
 ('The source lists no fixed cooldown; check your current attack controls.','출처에 고정 재사용 시간은 없습니다. 현재 조작 방식과 툴팁을 확인하세요.')),
]

def e(v): return html.escape(str(v),quote=True)
def tr(v,lang):return v[lang=='ko']
def root(base,lang):return base+('ko/' if lang=='ko' else '')

ALIASES={a:s for s in SKILLS for a in [s['ko'],s['en'],s['en'].replace('’',"'"),*s['aliases']]}
PATTERN=re.compile('|'.join(re.escape(a) for a in sorted(ALIASES,key=len,reverse=True)))

def link_skills(text,lang,base):
    """Escape ordinary text and turn known names into bilingual dictionary links."""
    out=[];cursor=0
    for m in PATTERN.finditer(text):
        s=ALIASES[m[0]];label=s['ko' if lang=='ko' else 'en']
        out.extend([e(text[cursor:m.start()]),f'<a class="skill-link" data-skill="{s["id"]}" href="{root(base,lang)}skills/{s["id"]}/" title="{e(s["en"]+" · "+s["ko"])}">{e(label)}<span aria-hidden="true"> ↗</span></a>'])
        cursor=m.end()
    out.append(e(text[cursor:]))
    return ''.join(out)

def details(s,lang,base,modal=False):
    t=lambda a,b:b if lang=='ko' else a
    c=next(c for c in CLASSES if c['id']==s['cls'])
    name=s['ko' if lang=='ko' else 'en'];other=s['en' if lang=='ko' else 'ko']
    kind=t('Stigma · equip to use','스티그마 · 장착 후 사용') if s['kind']=='stigma' else t('Active skill','액티브 스킬')
    reach=t('Self','자신') if s['reach']=='self' else s['reach']
    return f'''<div class="skill-doc" style="--class-color:{c['color']}"><span class="section-kicker">{e(c['ko' if lang=='ko' else 'en'])} / {kind}</span><h2{' id="skill-dialog-title"' if modal else ''}>{e(name)}</h2><p class="skill-other">{e(other)}</p><div class="skill-facts"><span><small>{t('BASE COOLDOWN','기본 재사용')}</small><b>{s['cooldown']}</b></span><span><small>{t('RANGE','사거리')}</small><b>{reach}</b></span><span><small>{t('REFERENCE','수치 기준')}</small><b>{t('Skill Lv. 1','스킬 1레벨')}</b></span></div><h3>{t('What it does','어떤 스킬인가요?')}</h3><p>{e(tr(s['effect'],lang))}</p><div class="skill-use"><h3>{t('When to press it','언제 누르나요?')}</h3><p>{e(tr(s['use'],lang))}</p></div><h3>{t('Before copying a build','빌드를 따라 하기 전에')}</h3><p>{e(tr(s['watch'],lang))}</p><p class="tiny muted">{t('Effects & EN name: Global client database. Usage tips: CODEX editorial. Specializations and skill levels can change the tooltip.','효과·영문명: 글로벌 클라이언트 DB. 활용법: CODEX 편집 조언. 특화·스킬 레벨에 따라 툴팁이 달라집니다.')}</p><div class="doc-links"><a href="{s['url']}" target="_blank" rel="noopener noreferrer">MetaBot · {t('full tooltip & specializations','전체 툴팁·특화')} ↗</a><a href="{root(base,lang)}insights/?class={s['cls']}">{t('Related KR tips','관련 한국 유저 팁')} →</a></div><small class="muted">{t('Reviewed','확인')} {REVIEW} · {t('Independent database, not an NC publication.','NC 공식 문서가 아닌 독립 DB입니다.')}</small>{f'<p><a class="btn" href="{root(base,lang)}skills/{s["id"]}/">{t("Open full skill page","스킬 문서 열기")} →</a></p>' if modal else ''}</div>'''

def widgets(lang,base):
    payload={s['id']:details(s,lang,base,True) for s in SKILLS}
    return f'''<dialog class="skill-dialog" data-skill-dialog aria-labelledby="skill-dialog-title"><button class="dialog-close" data-close-skill aria-label="{'닫기' if lang=='ko' else 'Close'}">×</button><div data-skill-content></div></dialog><script type="application/json" id="skill-data">{json.dumps(payload,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script>'''

def library(lang,base):
    t=lambda a,b:b if lang=='ko' else a
    opts=''.join(f'<option value="{c["id"]}">{c["ko" if lang=="ko" else "en"]}</option>' for c in CLASSES)
    cards=''.join(f'''<a class="skill-card" data-skill="{s['id']}" data-skill-class="{s['cls']}" data-skill-search="{e(' '.join([s['en'],s['ko'],*s['aliases']]))}" href="{root(base,lang)}skills/{s['id']}/"><small>{next(c['ko' if lang=='ko' else 'en'] for c in CLASSES if c['id']==s['cls'])} · {t('Stigma','스티그마') if s['kind']=='stigma' else t('Active','액티브')}</small><strong>{e(s['ko' if lang=='ko' else 'en'])}<span>↗</span></strong><span>{e(s['en' if lang=='ko' else 'ko'])}</span><p>{e(tr(s['effect'],lang))}</p></a>''' for s in SKILLS)
    return f'''<section data-skill-library><div class="insight-controls"><label>{t('Class','직업')}<select data-skill-class-filter><option value="all">{t('All classes','전체 직업')}</option>{opts}</select></label><label>{t('English or Korean skill name','영문·한국어 스킬명')}<input type="search" data-skill-search-input placeholder="Hellfire / 지옥의 화염"></label></div><p class="scope-line">{t('17 key skills · Global DB English names · click for effects, usage and specializations.','핵심 스킬 17개 · 글로벌 DB 영문명 · 눌러서 효과·사용법·특화를 확인하세요.')}</p><p class="tiny" role="status" data-skill-count></p><div class="skill-grid">{cards}</div><p data-skill-empty hidden>{t('No match. Try the other language or all classes.','결과가 없어요. 다른 언어 또는 전체 직업으로 찾아보세요.')}</p><noscript><style>.skill-dialog{{display:none}}</style></noscript></section>'''

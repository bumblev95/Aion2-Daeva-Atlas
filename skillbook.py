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

# The full 35-skill kit of each of the 8 Global launch classes.
from pathlib import Path
from growth import BUILDS, SHEET
LEGACY={s['id']:s for s in SKILLS}
SKILLS=json.loads((Path(__file__).parent/'data/skills.json').read_text())
for s in SKILLS:
    old=LEGACY.get(s['id'],{})
    s['aliases']=list(dict.fromkeys([s['ko'].replace(' ',''),s['en'].replace("'",'’'),*old.get('aliases',[]),old.get('ko',s['ko'])]))
    s['effect']=(s['en_data']['effect'],s['ko_data']['effect'])
    s['reach']=s['en_data']['reach']
    s['use']=old.get('use',('Use the activation condition in the tooltip. Check range and resources before pressing.','툴팁의 발동 조건을 확인하세요. 사거리와 자원을 보고 사용해요.'))
    s['watch']=old.get('watch',('A guide may assume extra skill levels from gear or boards.','공략은 장비·데바니온의 추가 스킬 레벨을 전제로 할 수 있어요.'))
    s['picks']=BUILDS[s['cls']]['picks'].get(s['id'],[])
BY_ID={s['id']:s for s in SKILLS}
ALIASES={a:s for s in SKILLS for a in [s['ko'],s['en'],s['en'].replace('’',"'"),*s['aliases']]}
# Existing community links keep their original class context for shared names.
for sid,old in LEGACY.items():
    for a in [old['ko'],old['en'],*old['aliases']]:ALIASES[a]=BY_ID[sid]
PATTERN=re.compile('|'.join(re.escape(a) for a in sorted(ALIASES,key=len,reverse=True)))

def link_skills(text,lang,base):
    out=[];cursor=0
    for m in PATTERN.finditer(text):
        s=ALIASES[m[0]];label=s['ko' if lang=='ko' else 'en']
        out.extend([e(text[cursor:m.start()]),f'<a class="skill-link" data-skill="{s["id"]}" href="{root(base,lang)}skills/{s["id"]}/" title="{e(s["en"]+" · "+s["ko"])}">{e(label)}<span aria-hidden="true"> ↗</span></a>']);cursor=m.end()
    out.append(e(text[cursor:]));return ''.join(out)

def skill_icon(s):
    return f'<img class="skill-icon" src="{e(s["icon"])}" alt="" width="56" height="56" loading="lazy" decoding="async">'

def skill_link(sid,lang,base,extra=''):
    s=BY_ID[sid]
    return f'<a class="build-skill" data-skill="{sid}" href="{root(base,lang)}skills/{sid}/">{skill_icon(s)}<span><b>{e(s["ko" if lang=="ko" else "en"])}</b><small>{e(s["en" if lang=="ko" else "ko"])}</small>{extra}</span><i>↗</i></a>'

def details(s,lang,base,modal=False):
    t=lambda a,b:b if lang=='ko' else a;c=next(c for c in CLASSES if c['id']==s['cls']);d=s[lang+'_data']
    kind={'active':t('Active · press to use','액티브 · 눌러서 사용'),'passive':t('Passive · learned effect','패시브 · 배운 효과 적용'),'stigma':t('Stigma · equip to use','스티그마 · 장착해서 사용')}[s['kind']]
    specs=''
    if d['specs']:
        rows=''.join(f'<li data-spec-number="{x["n"]}" data-spec-unlock="{x["level"]}"><span class="spec-number">{x["n"]}</span><div><small>Lv. {x["level"]}</small><p>{e(x["text"])}</p></div><b data-spec-status></b></li>' for x in d['specs'])
        active=s['kind']=='active'
        specs=f'<section class="specializations" data-specializations data-skill-kind="{s["kind"]}" data-recommended="{e(json.dumps(s["picks"]))}"><h3>{t("Specializations — see what to choose","특화 — 무엇을 고르나요?") if active else t("Level milestones","레벨별 추가 효과")}</h3><label class="spec-level">{t("My total skill level","내 스킬의 합계 레벨")} <select data-spec-level>'+''.join(f'<option value="{n}" {"selected" if n==8 else ""}>{n}</option>' for n in ([1,8,10,12,16,20] if active else [1,5,10,15,20]))+f'</select></label><p class="spec-status" data-spec-summary></p><ol>{rows}</ol><p class="tiny muted">'+(t('Green = CODEX learning recommendation at this level. At 8 / 12 / 20 you can equip 1 / 2 / 3 choices.','초록 표시 = 이 레벨에서의 CODEX 입문 추천. 합계 8 / 12 / 20에 각각 1 / 2 / 3개를 골라요.') if s['picks'] else (t('No preset recommendation for this skill. Read the effect before choosing.','이 기술에는 고정 추천을 정하지 않았어요. 효과를 읽고 용도에 맞춰 고르세요.') if active else t('These effects accumulate at the listed levels; they are not competing choices.','표시된 레벨에 추가되는 효과예요. 서로 택일하는 특화가 아니에요.')))+ '</p></section>'
    plan=f'<p><a href="{root(base,lang)}skills/?class={s["cls"]}#build-path">{t("See this class’s investment order","이 직업의 투자 순서 보기")} →</a></p>'
    return f'<div class="skill-doc" style="--class-color:{c["color"]}"><div class="skill-doc-head">{skill_icon(s)}<div><span class="section-kicker">{e(c["ko" if lang=="ko" else "en"])} · {kind}</span><h2'+(' id="skill-dialog-title"' if modal else '')+f'>{e(s["ko" if lang=="ko" else "en"])}</h2><p class="skill-other">{e(s["en" if lang=="ko" else "ko"])}</p></div></div><div class="skill-facts"><span><small>{t("LEARN AT","습득 캐릭터 레벨")}</small><b>Lv. {s["unlock"]}</b></span><span><small>{t("BASE COOLDOWN","1레벨 재사용")}</small><b>{e(s["cooldown"])}</b></span><span><small>{t("RANGE","사거리")}</small><b>{e(s["reach"])}</b></span></div><h3>{t("Effect at skill level 1","스킬 1레벨 효과")}</h3><p class="tooltip-effect">{e(d["effect"])}</p>'+ (f'<div class="skill-use"><h3>{t("When to use it","언제 쓰나요?")}</h3><p>{e(tr(s["use"],lang))}</p></div>' if s['kind']!='passive' else f'<p>{t("This effect works after it is learned. It is not a button in your attack sequence.","배운 뒤 적용되는 효과예요. 공격 순서에 넣고 누르는 버튼이 아니에요.")}</p>')+specs+plan+f'<details class="evidence"><summary>{t("Source and version","출처와 버전")}</summary><p>{t("Base effects, icons and both names: MetaBot client database, checked 2026-10-07. Numbers vary with skill level. Learning picks are CODEX editorial, informed by KR builds; they are not a measured Global best build.","기본 효과·아이콘·한영 이름: MetaBot 클라이언트 DB, 2026-10-07 확인. 레벨에 따라 수치가 변해요. 추천은 한국 세팅을 참고한 CODEX 입문 제안이며 글로벌 최적 딜 검증 결과가 아니에요.")}</p><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">MetaBot · {t("All levels and tooltip","전체 레벨·툴팁")} ↗</a><a href="{SHEET}" target="_blank" rel="noopener noreferrer">zxcastform · {t("Class reference sheet","직업 참고표")} ↗</a></details>'+ (f'<p><a class="btn" href="{root(base,lang)}skills/{s["id"]}/">{t("Open full skill page","스킬 문서 열기")} →</a></p>' if modal else '')+'</div>'

def widgets(lang,base,ids=None):
    payload={s['id']:details(s,lang,base,True) for s in SKILLS if ids is None or s['id'] in ids}
    return f'''<dialog class="skill-dialog" data-skill-dialog aria-labelledby="skill-dialog-title"><button class="dialog-close" data-close-skill aria-label="{'닫기' if lang=='ko' else 'Close'}">×</button><div data-skill-content></div></dialog><script type="application/json" id="skill-data">{json.dumps(payload,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script>'''

def build_paths(lang,base):
    t=lambda a,b:b if lang=='ko' else a;panels=''
    for cls,b in BUILDS.items():
        cores=''.join(f'<article class="core-pick"><small>0{i+1} / {t("FIRST PRIORITY","먼저 키우기")}</small>'+skill_link(sid,lang,base)+f'<p>{tr(b["why"][i],lang)}</p><div class="level-ladder"><span>SP <b>8 → 10</b></span><i>→</i><span>{t("TOTAL","합계")} <b>12 → 16 → 20</b></span></div></article>' for i,sid in enumerate(b['core']))
        secondary=''.join(skill_link(sid,lang,base) for sid in b['next']);passive=''.join(skill_link(sid,lang,base) for sid in b['passive']);stigmas=''.join(f'<div><small>{i+1:02}</small>'+skill_link(sid,lang,base)+'</div>' for i,sid in enumerate(b['stigma']))
        panels+=f'''<section data-build-class="{cls}" {'hidden' if cls!='gladiator' else ''}><div class="core-picks">{cores}</div><details class="build-more"><summary>{t('Next skills, passives and Stigma choices','그다음 스킬·패시브·스티그마 보기')} ↓</summary><h3>{t('03 · Add these active skills next','03 · 다음으로 볼 액티브')}</h3><div class="build-pair">{secondary}</div><h3>{t('04 · Learn these passive effects','04 · 패시브 효과 챙기기')}</h3><div class="build-pair">{passive}</div><h3>{t('05 · Stigma starting loadout','05 · 스티그마 시작 구성')}</h3><p>{t('Equip only as many as your character has slots for. Read each icon’s 5 / 10 / 15 / 20 milestones before investing more.','열린 슬롯 수만큼 순서대로 장착해요. 더 투자하기 전 아이콘을 눌러 5 / 10 / 15 / 20레벨 효과를 비교하세요.')}</p><div class="stigma-picks">{stigmas}</div>{f'<p class="scope-line">{t("Cleric: a first-party healing setup. A Chanter can overlap your buffs; agree the loadout before the run.","치유성은 첫 파티 회복 구성이에요. 호법성과 버프가 겹칠 수 있으니 입장 전 구성을 맞추세요.")}</p>' if cls=='cleric' else ''}</details><details class="evidence"><summary>{t('Why this starting path?','이 순서의 기준은?')}</summary><p>{t('CODEX PvE learning path, using skill effects and KR build references. Start with the two core skills, then extend the kit. KR target levels include gear and board bonuses.','스킬 효과와 한국 세팅을 참고한 CODEX PvE 입문 순서예요. 핵심 두 기술부터 익히고 범위를 넓혀요. 한국 공략의 목표 레벨에는 장비·보드 보너스가 포함돼요.')}</p><a href="https://www.inven.co.kr/board/aion2/{b['source']}" target="_blank" rel="noopener noreferrer">Inven · {t('KR class discussion','한국 직업 게시판 원문')} ↗</a><a href="{SHEET}" target="_blank" rel="noopener noreferrer">zxcastform · {t('Class reference sheet','직업 참고표')} ↗</a></details></section>'''
    return f'''<section class="build-path" id="build-path"><span class="section-kicker">01 / MY FIRST SKILL POINTS</span><h2>{t('Start with these two.','우선 이 두 개부터 키워요.')}</h2><p class="build-intro">{t('First raise priority 01 to 8, then 02 to 8. Next, bring each to 10 as your level and points allow. Tap the icons to choose specializations.','01번을 8 → 02번을 8 → 둘을 10 순서로, 레벨·포인트가 허용할 때 올려요. 아이콘을 누르면 특화 선택이 열려요.')}</p><div class="skill-level-explain"><b>{t('Character Lv. ≠ skill Lv.','캐릭터 레벨 ≠ 스킬 레벨')}</b><span>{t('Skill points raise a basic skill to 10. Gear, Daevanion and Arcana add levels above that. “20” is a total-level goal.','일반 스킬은 포인트로 10까지 올려요. 그 이상은 장비·데바니온·아르카나가 더해줘요. 공략의 “20”은 합계 목표예요.')}</span></div>{panels}<p data-build-all hidden>{t('Choose one class above to see its investment path.','위에서 직업 하나를 고르면 투자 순서가 나와요.')}</p></section>'''

def library(lang,base):
    t=lambda a,b:b if lang=='ko' else a
    opts=''.join(f'<option value="{c["id"]}">{c["ko" if lang=="ko" else "en"]}</option>' for c in CLASSES)
    picks=''.join(f'<button data-library-class="{c["id"]}" aria-pressed="{str(c["id"]=="gladiator").lower()}" style="--class-color:{c["color"]}"><svg viewBox="0 0 48 48" aria-hidden="true"><use href="{base}assets/icons.svg#{c["icon"]}"/></svg><b>{c["ko" if lang=="ko" else "en"]}</b><small>35</small></button>' for c in CLASSES)
    kinds={'active':t('Active','액티브'),'passive':t('Passive','패시브'),'stigma':t('Stigma','스티그마')}
    cards=''.join(f'''<a class="skill-card full-skill-card" data-skill="{s['id']}" data-skill-class="{s['cls']}" data-skill-kind="{s['kind']}" data-skill-search="{e(' '.join([s['en'],s['ko'],*s['aliases']]))}" href="{root(base,lang)}skills/{s['id']}/">{skill_icon(s)}<div><small>{kinds[s['kind']]} · Lv. {s['unlock']}</small><strong>{e(s['ko' if lang=='ko' else 'en'])}</strong><span>{e(s['en' if lang=='ko' else 'ko'])}</span></div><b>↗</b></a>''' for s in SKILLS)
    return f'''<section data-skill-library><div class="library-classes">{picks}</div><label class="sr-only">{t('Class','직업')}<select data-skill-class-filter><option value="all">{t('All classes','전체 직업')}</option>{opts}</select></label>{build_paths(lang,base)}<section class="complete-library" id="all-skills"><span class="section-kicker">02 / COMPLETE SKILLBOOK</span><h2>{t('Your entire kit, with icons.','전체 스킬을 그림으로 찾아봐요.')}</h2><p class="scope-line">{t('8 launch classes × 35 learnable skills = 280. Each kit: 12 active, 10 passive, 13 Stigma. Chain effects are described inside the parent skill.','출시 8직업 × 습득 스킬 35종 = 280개. 직업마다 액티브 12 · 패시브 10 · 스티그마 13개예요. 파생 연계 효과는 원래 스킬 문서에서 설명해요.')}</p><div class="skill-filterbar"><div class="skill-kind-filters">{''.join(f'<button data-library-kind="{key}" aria-pressed="{str(key=="all").lower()}">{label}</button>' for key,label in [('all',t('All 35','35개 전체')),*kinds.items()])}</div><label><span class="sr-only">{t('Search skill name','스킬명 검색')}</span><input type="search" data-skill-search-input placeholder="{t('English or Korean name…','한국어·영어 이름 검색…')}"></label></div><p class="tiny" role="status" data-skill-count></p><div class="skill-grid">{cards}</div><p data-skill-empty hidden>{t('No match. Clear the search or change class.','일치하는 스킬이 없어요. 검색어를 지우거나 직업을 바꿔보세요.')}</p></section></section>'''

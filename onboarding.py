"""Beginner routes, item reading and real embedded maps. All copy is bilingual."""
from html import escape as e
from firststeps import overview
from fieldtips import panel as field_tips
from poststory import teaser as post_story_teaser

SOURCES = {
 'start':('Global beginner reference','https://metabot.gg/en/aion-2/guides/beginners-guide'),
 'unlocks':('Content unlock reference','https://metabot.gg/en/aion-2/content-unlocks'),
 'stats':('Global stat definitions','https://metabot.gg/en/aion-2/stats'),
 'enhance':('Enhancement rules','https://metabot.gg/en/aion-2/guides/gear-enhancement-guide'),
 'maps':('Interactive maps · The Hidden Gaming Lair','https://aion2.th.gl/maps'),
 'embed':('Map embed documentation','https://www.th.gl/developers'),
}
def tr(v,lang):return v[lang=='ko']
def root(base,lang):return base+('ko/' if lang=='ko' else '')
def evidence(lang,*keys):
    t=lambda a,b:b if lang=='ko' else a
    return f'<details class="evidence beginner-evidence"><summary>{t("Sources · Global reference · checked Oct 7, 2026","출처 · 글로벌 참고 자료 · 2026.10.07 확인")}</summary><p>{t("Independent client databases and maps. Story prerequisites and current in-game tooltips take priority. Route order and spending advice are CODEX editorial.","독립 클라이언트 DB와 지도입니다. 퀘스트 선행 조건과 현재 게임 툴팁을 우선하세요. 진행 순서·소비 판단은 CODEX 편집 조언입니다.")}</p>'+''.join(f'<a href="{SOURCES[k][1]}" target="_blank" rel="noopener noreferrer">{SOURCES[k][0]} ↗</a>' for k in keys)+'</details>'

# Three actionable priorities per stage. Details appear only for the selected stage.
STAGES=[
 ('arrival','01–09',('First steps','첫 접속'),('Unlock the route and reduce return travel.','진행 동선과 이동 거점 확보'),[
 ('story',('Track the main Episode quest','메인 에피소드 퀘스트 추적'),('Your route to new areas and core systems.','새 지역과 기본 시스템을 여는 길입니다.'),('Quest journal → Episode','퀘스트 창 → 에피소드'),'maps/'),
 ('controls',('Set combat keys and camera sensitivity','전투 단축키·카메라 감도 설정'),('Place frequently used skills and dodging where they do not interfere with movement.','이동과 동시에 사용할 수 있도록 주력기·회피 키 배치를 정리합니다.'),('Settings → controls','설정 → 조작'),'start/?view=settings#field-tips'),
 ('travel',('Activate travel points as you pass','지나는 키벨리스크 활성화'),('Turn a long run back into a quick return.','다시 와야 할 때 이동 시간을 줄여줍니다.'),('Map → Kibelisk','지도 → 키벨리스크'),'maps/'),
 ]),
 ('foundation','10–21',('Build your basics','기본 성장'),('Collect lasting growth along your route.','동선 안에서 영구 성장 요소 확보'),[
 ('skills',('Prioritise core skill conditions','주력 스킬의 발동 조건 파악'),('Know the trigger, range and cooldown before copying a rotation.','딜 사이클을 따라 하기 전에 발동 조건·사거리·재사용 시간을 알아보세요.'),('Skill menu → tooltip','스킬 창 → 툴팁'),'skills/'),
 ('sealed',('Clear nearby Sealed Dungeons','동선 근처 봉인 던전 클리어'),('Skill-point and Daevanion materials support lasting growth.','스킬 포인트와 데바니온 재료로 기본 성장을 채웁니다.'),('Map → Sealed Dungeon','지도 → 봉인 던전'),'maps/'),
 ('item',('Compare equipment before investing','투자 전 장비 옵션 비교'),('Check the equipment slot, requirements and useful options.','착용 부위·조건·필요한 옵션부터 확인하세요.'),('Inventory → item tooltip','가방 → 아이템 툴팁'),'gear/'),
 ]),
 ('build','22–44',('Shape your build','세팅 만들기'),('Connect unlocked systems to your build.','해금된 성장 시스템을 세팅에 연결'),[
 ('stigma',('Equip an available Stigma','사용 가능한 스티그마 장착'),('Stigma opens from level 22; equipping a skill is part of the setup.','스티그마는 22레벨부터 열립니다. 스킬 장착도 세팅의 일부입니다.'),('Skill menu → Stigma','스킬 창 → 스티그마'),'skills/'),
 ('daevanion',('Check the Daevanion board','데바니온 보드 확인'),('Compare unlocked nodes with your current build before spending acquired crystals.','해금된 노드와 현재 세팅의 필요 능력치를 비교해 결정을 배분합니다.'),('Character → Daevanion','캐릭터 → 데바니온'),'gear/#materials'),
 ('keep-story',('Keep the Episode quest moving','에피소드 퀘스트 계속 진행'),('If blocked, read the quest requirement first; avoid an unfocused grind.','막히면 퀘스트 조건부터 읽고 필요한 목표를 잡으세요.'),('Tracked quest → requirement','추적 퀘스트 → 진행 조건'),'maps/'),
 ]),

 ('after-story','45+',('Story cleared','메인 완료'),('Turn exploration rewards into a stronger build.','탐험 보상을 실제 스킬·장비 성장으로 연결'),[
 ('post-points',('Use saved rewards and spend points','보상 아이템 사용·남은 포인트 투자'),('Use Wisdom Stones and Daevanion Crystals, then invest in skills and board nodes.','지혜의 돌·데바니온 결정을 사용하고 스킬·보드 노드에 투자합니다.'),('Inventory → skills / Daevanion','가방 → 스킬·데바니온'),'endgame/#after-story-spend-points'),
 ('post-sealed',('Collect unfinished Sealed Dungeon rewards','미완료 봉인 던전 보상 챙기기'),('Choose a nearby unfinished dungeon; claim its reward and use the point items.','가까운 미완료 던전의 보상을 받고 포인트 아이템을 사용합니다.'),('Map → Sealed Dungeon','지도 → 봉인 던전'),'endgame/#after-story-field-rewards'),
 ('post-feathers',('Connect feather collection to its reward','깃털 수집을 반납·성장으로 연결'),('Follow the Monolith turn-in and accessory steps in the KR reference, matching your server’s rewards.','한국 참고 자료의 모노리스 반납·장신구 성장 흐름을 현재 서버 보상에 맞춰 확인합니다.'),('Lord’s Traces → Monolith','주신의 흔적 → 모노리스'),'endgame/#after-story-feathers'),
 ]),
]

def journey(lang,base,compact=False):
    t=lambda a,b:b if lang=='ko' else a;r=root(base,lang)
    tabs=''.join(f'<button data-journey-stage="{key}" aria-pressed="{str(i==0).lower()}" aria-controls="journey-{key}"><small>{t("AFTER STORY","스토리 이후") if key=="after-story" else "LV. "+level}</small><strong>{tr(name,lang)}</strong></button>' for i,(key,level,name,heading,tasks) in enumerate(STAGES))
    panels=''
    for i,(key,level,name,heading,tasks) in enumerate(STAGES):
        cards=''.join(f'''<article class="priority-card"><div class="priority-top"><span>0{j+1}</span><label class="task-check"><input type="checkbox" data-start-task="{task}" aria-label="{e(tr(title,lang))} {t('complete','완료')}"><span>{t('Done','완료')}</span></label></div><h3>{tr(title,lang)}</h3><p>{tr(why,lang)}</p><small class="where-label">{t('WHERE','어디서')}</small><p class="task-where">{tr(where,lang)}</p><a href="{r}{url}">{t('Related guide','관련 공략')} →</a></article>''' for j,(task,title,why,where,url) in enumerate(tasks))
        panels+=f'<section id="journey-{key}" data-journey-panel="{key}" aria-label="{tr(name,lang)}" {"hidden" if i else ""}><h3 class="journey-heading">{tr(heading,lang)}</h3><div class="priority-grid">{cards}</div></section>'
    return f'''<section class="journey" data-journey><div class="section-heading compact"><div><span class="section-kicker">START HERE / GLOBAL</span><h2>{t('Early progression priorities','초반 성장 우선순위')}</h2></div><span class="tiny" role="status" data-start-progress></span></div><div class="journey-tabs" aria-label="{t('Your current stage','현재 진행 단계')}">{tabs}</div>{panels}<div class="journey-footer"><p>{t('Priorities depend on your current stage and unlocked content.','진행 단계와 콘텐츠 해금 상황에 따른 우선순위입니다.')}</p>{f'<a href="{r}start/">{t("Full beginner route","초보 가이드 전체")} →</a>' if compact else f'<button class="text-link" data-reset-start>{t("Reset checks","완료 표시 초기화")}</button>'}</div><noscript><style>[data-journey-panel][hidden]{{display:block!important}}.journey-tabs,.task-check{{display:none}}</style></noscript></section>'''

def beginner(lang,base):
    t=lambda a,b:b if lang=='ko' else a;r=root(base,lang)
    views=[('basics','basics',t('Core guide','핵심 요약'),t('Progression and decisions','진행·투자 판단')),
           ('settings','field-tips',t('Useful settings','편의 설정'),t('Settings and party terms','설정·파티 용어')),
           ('growth','growth',t('What to do next','성장 순서'),t('Priorities for your current stage','현재 단계별 우선순위'))]
    tabs=''.join(f'<a href="#{anchor}" data-guide-tab="{key}" id="guide-tab-{key}"><span class="guide-tab-number">0{i+1}</span><span><strong>{title}</strong><small>{desc}</small></span></a>' for i,(key,anchor,title,desc) in enumerate(views))
    return f'''<div class="beginner-hub" data-guide-hub data-practical-guide><div class="guide-intro"><div class="breadcrumbs"><a href="{r}">{t('Home','홈')}</a><span>/</span><span>{t('Early-game guide','초반 공략')}</span></div><h1>{t('Early-game guide.','초반 공략.')}</h1><p>{t('Quest progression, skill investment, equipment choices and useful settings for your first character.','첫 캐릭터의 육성 동선, 스킬 투자, 장비 선택과 필요한 설정을 정리했습니다.')}</p></div><nav class="stage-switch" aria-label="{t('Guide stage','공략 단계')}"><span aria-current="page">{t('Early game','초반 공략')}</span><a href="{r}endgame/">{t('Endgame','엔드게임 공략')} →</a></nav>{post_story_teaser(lang,base)}<nav class="guide-tabs" data-guide-tabs aria-label="{t('Early-game guide sections','초반 공략 주제')}">{tabs}</nav><div class="guide-views"><section id="basics" data-guide-view="basics" aria-labelledby="guide-tab-basics">{overview(lang,base)}{evidence(lang,'start','unlocks')}</section><section id="settings" data-guide-view="settings" aria-labelledby="guide-tab-settings">{field_tips(lang)}</section><section id="growth" data-guide-view="growth" aria-labelledby="guide-tab-growth">{journey(lang,base)}<a class="endgame-gateway" href="{r}endgame/#after-story"><strong>{t('After clearing the story','메인 스토리 완료 이후')}</strong><span>{t('Field rewards, point investment and dungeon farming','필드 보상·포인트 투자·던전 파밍 순서')} →</span></a>{evidence(lang,'start','unlocks')}</section></div><nav class="guide-next-links" aria-label="{t('Next guides','이어서 볼 공략')}"><span>{t('Next, explore','이어서 알아보기')}</span><a href="{r}skills/">{t('My skills & build','내 직업 스킬·빌드')} →</a><a href="{r}maps/">{t('Find a destination','지도에서 위치 찾기')} →</a><a href="{r}gear/">{t('Read my equipment','장비·능력치 읽기')} →</a></nav></div>'''

STATS=[
 ('might','Might','위력','⚔',('Attack','공격력'),('Helps attacks hit harder.','공격력을 높이는 기본 능력치입니다.')),
 ('dexterity','Dexterity','민첩','↝',('Evasion · block · critical resistance','회피 · 방패 방어 · 치명타 저항'),('A defensive stat, not an automatic ranged-damage stat.','방어 계열 능력치이며 궁성의 공격력으로 바로 해석하면 안 됩니다.')),
 ('intelligence','Intelligence','지능','✦',('Status effect chance','상태 이상 적중'),('Helps control effects land. It is not the magic-damage stat.','상태 이상이 적용될 가능성과 연결됩니다. 마법 공격력이 아닙니다.')),
 ('constitution','Constitution','체력','♥',('Maximum HP','최대 생명력'),('Builds your health pool. Survival also depends on mitigation and mechanics.','생명력의 기반입니다. 생존에는 피해 감소와 기믹 대응도 필요합니다.')),
 ('precision','Precision','정확','◎',('Accuracy · critical hit','명중 · 치명타'),('Helps attacks connect and critically hit.','공격의 명중과 치명타에 연결됩니다.')),
 ('willpower','Willpower','의지','⬡',('Status effect resistance','상태 이상 저항'),('Helps resist control effects; it does not make every boss mechanic avoidable.','상태 이상 저항을 돕습니다. 모든 보스 기믹을 무시할 수 있다는 뜻은 아닙니다.')),
]

ITEM_PARTS=[
 ('grade',('GRADE / COLOR','등급 / 색상'),('Unique','유일'),('Rarity is a category, not a complete verdict. Compare items for the same slot and purpose.','등급은 분류입니다. 같은 부위·용도의 장비끼리 실제 효과를 비교하세요.')),
 ('level',('ITEM LEVEL','아이템 레벨'),('Item level ≠ character level','아이템 레벨 ≠ 캐릭터 레벨'),('Item level describes the equipment. Equip requirements and dungeon entry requirements are separate checks.','아이템 레벨은 장비의 수준입니다. 착용 조건과 던전 입장 조건은 따로 확인하세요.')),
 ('base',('MAIN STAT','기본 능력치'),('Weapon attack / armor defense','무기 공격력 / 방어구 방어력'),('Start with the item’s main function. Then check whether an upgrade improves the problem you are trying to solve.','부위의 기본 기능부터 읽으세요. 그다음 지금 해결하려는 문제에 도움이 되는지 확인하세요.')),
 ('options',('EXTRA OPTIONS','추가 옵션'),('Accuracy · critical hit · …','명중 · 치명타 · …'),('Read each option. A higher score does not tell you whether the option helps your current build.','옵션을 하나씩 읽어보세요. 점수가 높다고 현재 세팅에 모두 유효한 옵션은 아닙니다.')),
 ('upgrade',('ENHANCEMENT','강화 수치'),('+N','+N'),('The plus number is investment on this item. Compare the cost, success chance and likely replacement before spending.','이 장비에 투자한 강화 단계입니다. 비용·성공률·교체 계획을 보고 투자하세요.')),
]

def gear(lang,base):
    t=lambda a,b:b if lang=='ko' else a
    partbuttons=''.join(f'<button data-item-part="{key}" aria-pressed="{str(i==0).lower()}" aria-controls="item-{key}"><span>0{i+1}</span><div><small>{tr(label,lang)}</small><strong>{tr(value,lang)}</strong></div><b>↗</b></button>' for i,(key,label,value,desc) in enumerate(ITEM_PARTS))
    partpanels=''.join(f'<section data-item-panel="{key}" id="item-{key}" {"hidden" if i else ""}><span class="section-kicker">0{i+1} / {tr(label,lang)}</span><h3>{tr(value,lang)}</h3><p>{tr(desc,lang)}</p></section>' for i,(key,label,value,desc) in enumerate(ITEM_PARTS))
    statbuttons=''.join(f'<button data-stat="{key}" aria-pressed="{str(i==0).lower()}" aria-controls="stat-{key}"><b>{symbol}</b><strong>{ko if lang=="ko" else en}</strong><small>{en if lang=="ko" else ko}</small></button>' for i,(key,en,ko,symbol,affects,desc) in enumerate(STATS))
    statpanels=''.join(f'<section data-stat-panel="{key}" id="stat-{key}" {"hidden" if i else ""}><span class="section-kicker">{en.upper()} →</span><h3>{tr(affects,lang)}</h3><p>{tr(desc,lang)}</p></section>' for i,(key,en,ko,symbol,affects,desc) in enumerate(STATS))
    materials=[('Kinah','키나',('Everyday currency','기본 화폐'),('Keep a budget for the next thing you need.','다음에 필요한 비용까지 생각하며 쓰세요.')),('Enhancement Stones','강화석',('Equipment enhancement','장비 강화'),('Read the preview before confirming.','확인 버튼 전에 강화 화면을 읽으세요.')),('Wisdom Stones','지혜의 돌',('Skill growth','스킬 성장'),('Check which skills you actually use.','현재 사용하는 스킬부터 확인하세요.')),('Daevanion Crystals','데바니온 결정',('Daevanion board','데바니온 보드'),('Look at available nodes on your board.','해금된 보드의 노드를 살펴보세요.'))]
    return f'''<section class="field-section" data-item-reader><div class="section-heading compact"><div><span class="section-kicker">01 / READ YOUR LOOT</span><h2>{t('What to check on equipment','장비에서 확인할 핵심 항목')}</h2></div></div><div class="item-anatomy"><div class="sample-item"><p class="tiny muted">{t('Teaching example · not a real drop or a recommended build','설명용 예시 · 실제 드롭 장비·추천 세팅이 아닙니다')}</p>{partbuttons}</div><div class="item-explainer">{partpanels}<a class="text-link" href="#stats">{t('What do these stats mean?','이 능력치는 무슨 뜻인가요?')} ↓</a></div></div></section><section class="field-section" id="stats" data-stats><div class="section-heading compact"><div><span class="section-kicker">02 / SIX BASE STATS</span><h2>{t('Familiar names. Different jobs.','익숙한 이름, 다른 역할.')}</h2></div></div><div class="stat-picker">{statbuttons}</div><div class="stat-explanation">{statpanels}</div>{evidence(lang,'stats')}</section><section class="field-section" id="upgrade"><div class="section-heading compact"><div><span class="section-kicker">03 / UPGRADE OR WAIT?</span><h2>{t('Make the cost solve a problem.','필요한 문제를 해결하는 데 투자하세요.')}</h2></div></div><div class="upgrade-path"><article><small>01</small><h3>{t('Find the bottleneck','막힌 이유 확인')}</h3><p>{t('Entry score, survival, accuracy or damage? Name the problem first.','입장 점수·생존·명중·피해량 중 지금 부족한 것을 정하세요.')}</p></article><article><small>02</small><h3>{t('Read the upgrade screen','강화 화면 읽기')}</h3><p>{t('Check the item type, success chance and exact materials. Ordinary gear and Clash Runes have different failure rules.','장비 종류·성공률·재료를 확인하세요. 일반 장비와 충돌 룬의 실패 규칙은 다릅니다.')}</p></article><article><small>03</small><h3>{t('Set a stopping point','중단선 정하기')}</h3><p>{t('Decide how much to spend before clicking. Recheck the benefit after the upgrade.','누르기 전에 사용할 재화 한도를 정하고 강화 후 효과를 다시 확인하세요.')}</p></article></div><details class="beginner-faq"><summary>{t('What happens if enhancement fails?','강화 실패 시 어떻게 되나요?')}</summary><p>{t('The Global reference lists material loss without an enhancement-level drop for ordinary weapons, armor and accessories. Clash Runes are an exception and can lose a level. Always read the confirmation for your item type.','글로벌 참고 DB상 일반 무기·방어구·장신구는 실패 시 재료를 소모하며 강화 단계가 내려가지는 않습니다. 충돌 룬은 단계가 하락할 수 있는 예외입니다. 내 아이템의 확인창을 읽으세요.')}</p></details>{evidence(lang,'enhance')}</section><section class="field-section" id="materials"><div class="section-heading compact"><div><span class="section-kicker">04 / WHAT IS IN MY BAG?</span><h2>{t('Keep these systems separate.','재료의 쓰임을 구분해보세요.')}</h2></div></div><div class="material-grid">{''.join(f'<article><span>◇</span><h3>{ko if lang=="ko" else en}</h3><small>{en if lang=="ko" else ko}</small><p><b>{tr(use,lang)}</b></p><p>{tr(tip,lang)}</p></article>' for en,ko,use,tip in materials)}</div>{evidence(lang,'start','enhance')}</section><section class="field-section beginner-faq" id="arcana"><h2>{t('Arcana is equipment, not a skill.','아르카나는 스킬이 아닌 장비입니다.')}</h2><p>{t('KR guides may call an Arcana piece 천칭 (literally “scales”). This is an equipment name, not a button in your rotation. Use the item tooltip to identify the piece; we do not treat this literal translation as a verified Global item name.','한국 공략의 천칭은 아르카나 장비 이름으로, 딜 사이클에 누르는 스킬이 아닙니다. 아이템 툴팁으로 종류를 확인하세요. 영어 Scales는 뜻을 설명하는 번역이며 검증된 글로벌 아이템명 표기가 아닙니다.')}</p></section><noscript><style>[data-item-panel][hidden],[data-stat-panel][hidden]{{display:block!important}}</style></noscript>'''

MAPS=[('Poeta','포에타','elyos','first'),('Verteron','베르테론','elyos','field'),('Ishalgen','이스할겐','asmodian','first'),('Altgard','알트가르드','asmodian','field')]
MAP_PREVIEWS={'Poeta':'World_L_Starter','Verteron':'World_L_A','Ishalgen':'World_D_Starter','Altgard':'World_D_A'}
MAP_GOALS=[
 ('story','01',('Quest route','퀘스트 동선'),('Choose your faction and current zone. Keep your tracked Episode objective as the destination; the map supplies the terrain and landmarks.','진영과 현재 지역을 고르세요. 목적지는 추적 중인 에피소드 퀘스트, 지도는 지형과 길 찾기에 활용하세요.')),
 ('travel','02',('Travel points','이동 거점'),('Find Kibelisks along your route and activate them in game. For an exact marker, use the map’s own filter menu.','동선의 키벨리스크를 찾아 게임에서 활성화하세요. 정확한 마커는 지도 안의 필터 메뉴에서 고를 수 있습니다.')),
 ('growth','03',('Growth stops','성장 포인트'),('Look for Sealed Dungeons and collectibles near your current route. Check their reward before making a long detour.','현재 동선 근처의 봉인 던전과 수집 요소를 찾아보세요. 멀리 돌아가기 전에는 보상을 확인하세요.')),
]

def maps(lang,base):
    from worldmap import render
    return render(lang,base)

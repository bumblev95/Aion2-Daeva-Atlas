"""Task-first discovery and a dependency-free, progressively enhanced reader."""
from html import escape as e
from html.parser import HTMLParser
from content import CLASSES, GUIDES
import advancedguides
import partyguide
import liveops

GOALS = [
    ('growth', 'endgame/#after-story', 'spark', ('Character growth', '내실·성장'), ('Story cleared. What next?', '스토리 이후, 무엇부터 할까?')),
    ('enhancement', 'gear/#upgrade', 'shield', ('Gear & upgrades', '장비·강화'), ('Materials, farming and upgrades', '재료·획득처·강화 순서')),
    ('boss', 'dungeons/', 'boss', ('Beat a boss', '던전·보스'), ('Cues, safe spots and movement', '전조·안전 위치·움직임')),
    ('routines', 'routines/', 'check', ('Daily & weekly', '일일·주간 숙제'), ('Choose a run by its rewards', '받을 보상으로 할 일 선택')),
    ('field', 'maps/', 'target', ('Farming map', '파밍·수집 지도'), ('Materials, traces and hidden cube candidates', '채집 재료·주신의 흔적·큐브 후보 위치')),
    ('classes', 'classes/', 'swords', ('Classes & skills', '직업·스킬'), ('Roles, builds and skill investment', '직업별 역할·빌드·스킬 투자')),
]


def icon(base, name):
    return f'<svg class="icon" aria-hidden="true" viewBox="0 0 48 48"><use href="{base}assets/icons.svg#{name}"/></svg>'


def home(lang, base):
    k=lang=='ko';t=lambda en,ko:ko if k else en;r=base+('ko/' if k else '')
    cards=''.join(f'<a class="home-stage{(" endgame" if key=="growth" else "")}" data-rpg-goal="{key}" href="{r}{route}"><span class="find-goal-icon">{icon(base,glyph)}</span><span><h2>{title[k]}</h2><p>{desc[k]}</p></span><b aria-hidden="true">↗</b></a>' for key,route,glyph,title,desc in GOALS)
    quick=[('guides/pet-growth/','pet-growth',t('Pet souls','펫 내실')),('guides/gear-targets/','gear-targets',t('Target gear','목표 장비')),('guides/dungeon-rewards/','dungeon-rewards',t('Dungeon rewards','던전 보상')),('guides/kinah-farming/','kinah-farming',t('Kinah farming','키나 파밍'))]
    shortcuts=''.join(f'<a href="{r}{route}" data-growth-guide="{key}">{label} <span aria-hidden="true">→</span></a>' for route,key,label in quick)
    classes=''.join(f'<a href="{r}classes/{c["id"]}/" style="--class-color:{c["color"]}">{icon(base,c["icon"])}<span>{c["ko" if k else "en"]}</span></a>' for c in CLASSES)
    return f'''<div class="wrap find-home">
<section class="find-hero"><span class="find-eyebrow">PLAYER’S CODEX / AION 2</span><h1>{t('AION 2 guides for your next run', '아이온 2, 지금 필요한 공략부터')}</h1><p>{t('Find your next upgrade, your next reward or the way past a boss.', '내실부터 보스 공략까지, 지금 필요한 것부터 찾아보세요.')}</p><form class="find-search" action="{r}search/" role="search"><label class="sr-only" for="home-query">{t('Search all guides', '전체 공략 검색')}</label>{icon(base,'search')}<input id="home-query" name="q" type="search" placeholder="{t('Try a boss, item or skill name…', '보스, 아이템, 스킬 이름으로 검색')}" autocomplete="off" required><button type="submit">{t('Search','검색')}</button></form><div class="find-hero-links"><a href="{r}start/">{t('New character? Start here','처음 시작한다면 초반 공략')} →</a><a href="{r}guides/">{t('Browse all guides','전체 공략 둘러보기')} →</a></div></section>
<section class="rpg-home-goals find-goals" aria-label="{t('Choose your goal','목적별 공략')}">{cards}</section>
<section class="find-shortcuts"><h2>{t('Growth guides','성장 공략 바로가기')}</h2><nav aria-label="{t('Growth shortcuts','성장 공략 바로가기')}">{shortcuts}</nav></section>
<nav class="find-utility home-stage-nav" aria-label="{t('Records and updates','실전 기록과 업데이트')}"><a href="{r}tools/dps/">{icon(base,'swords')}{t('Compare DPS records','실전 DPS 비교')}</a><a href="{r}updates/">{icon(base,'book')}{t('News & patches','뉴스·패치')}</a><a href="{r}tools/planner/">{icon(base,'check')}{t('My checklist','나의 체크리스트')}</a></nav>
<section class="find-classes" id="class-explorer"><div class="find-section-heading"><h2>{t('My class','내 직업 바로 보기')}</h2><a href="{r}skills/">{t('Skills & builds','스킬·빌드')} →</a></div><div>{classes}</div></section>
{partyguide.gateway(lang,base)}
{liveops.screenshots(lang,base,"home")}
<nav class="find-utility" aria-label="{t('More resources','다른 자료 찾기')}"><a href="{r}glossary/">{icon(base,'book')}{t('KR / EN glossary','한영 용어집')}</a><a href="{r}guides/server-transfer/" data-growth-guide="server-transfer">{t('Global server transfer','글로벌 서버 이전')}</a></nav>
</div>'''


def directory(lang, base):
    k=lang=='ko';t=lambda en,ko:ko if k else en;r=base+('ko/' if k else '')
    groups=[
        ('growth',('Growth','내실·성장'), [('endgame/',('After the story','스토리 이후 성장 순서'),('Field rewards → points → next goal','필드 보상 → 포인트 투자 → 다음 목표')),('guides/pet-growth/',('Pet growth','펫 내실·영혼 파밍'),('Collection, families and soul sources','수집·종족 효과·영혼 사냥터')),('guides/kinah-farming/',('Kinah farming','키나 파밍·사용처'),('Earn, spend and save for the Market','수입·강화 비용·거래소 자금'))]),
        ('gear',('Gear & upgrades','장비·강화'), [('gear/',('Enhancement basics','장비 강화·스탯'),('Materials and the upgrade process','필요 재료와 실제 강화 순서')),('guides/gear-targets/',('Target gear','목표 장비 획득·강화'),('Choose a slot and a dungeon','부위에 맞는 던전 선택'))]),
        ('boss',('Dungeons','던전·보스'), [('dungeons/',('Animated boss lessons','움직이는 보스 공략'),('See cues and safe movement','전조와 안전한 이동 확인')),('guides/dungeon-rewards/',('Dungeon rewards','던전별 공략·보상'),('Loot targets and how to use them','목표 보상과 성장 사용처'))]),
        ('routines',('Daily & weekly','일일·주간'), [('routines/',('Daily and weekly rewards','일일·주간 숙제와 보상'),('Counters, Daily Dungeons and reward uses','횟수·일일 던전·보상 사용처')),('tools/planner/',('My checklist','나의 체크리스트'),('Keep your own goals','나의 할 일 기록'))]),
        ('field',('Farming & collectibles','파밍·수집 지도'), [('maps/',('Farming map','재료·내실 위치 지도'),('Gathering nodes, traces and hidden cube candidates','채집 재료·주신의 흔적·히든 큐브 후보')),('endgame/#after-story-field-rewards',('Use field rewards','필드 보상으로 성장하기'),('How collectibles become character growth','수집 보상을 성장에 쓰는 방법'))]),
        ('classes',('Classes & skills','직업·스킬'), [('classes/',('Class guides','직업별 공략'),('Find your role and build','역할·스킬·직업별 공략')),('skills/',('Skill library','스킬·빌드 사전'),('Effects and class priorities','스킬 효과·직업별 투자')),('tools/dps/',('Compare DPS records','실전 DPS 비교'),('Compare the region, encounter and sample count','서버·보스·표본 조건과 함께 비교')),('tools/compare/',('Compare classes','직업 비교'),('Compare roles and play styles','역할·플레이 방식 비교'))]),
        ('start',('Getting started','초반·기초'), [('guides/3b-meaning/',('3b & party shorthand','3b·파티 약어'),('All three bosses, 200k and tp explained','보스 세 마리·200k·tp 뜻')),('guides/commend-player/',('Commend a player','플레이어 칭찬'),('Steps and missing-popup checks · KR reference','칭찬 방법·창 누락 확인 · 한국 기준')),('start/',('Early-game guide','초반 공략'),('Progression and useful settings','육성 흐름과 편의 설정')),('guides/server-transfer/',('Global server transfer','글로벌 서버 이전'),('Dates, regional hours, costs and storage checklist','이전 기간·지역별 시간·비용·보관함 체크리스트'))]),
    ]
    for key,title,entries in groups:
        entries.extend(('guides/'+g['slug']+'/',g['title'],(g['region']+' · '+g['description'][0],g['region']+' · '+g['description'][1])) for g in advancedguides.GUIDES if g['group']==key)
    filters=''.join(f'<button type="button" data-directory-filter="{key}" aria-pressed="false">{title[k]}</button>' for key,title,_ in groups)
    cards=''
    for key,title,entries in groups:
        links=''.join(f'<a href="{r}{route}"{(chr(32)+"data-growth-guide="+chr(34)+route.split("/")[1]+chr(34) if route.startswith("guides/") else "")}{(" class=\"routine-gateway\"" if route=="routines/" else "")}><strong>{name[k]}</strong><span>{desc[k]}</span><b aria-hidden="true">→</b></a>' for route,name,desc in entries)
        cards+=f'<section class="directory-group" data-directory-group="{key}"><h2>{title[k]}</h2><div>{links}</div></section>'
    reading=''.join(f'<a href="{r}guides/{g["slug"]}/"><strong>{g["title"][k]}</strong><span>{g["minutes"]} {t("min", "분")}</span></a>' for g in GUIDES)
    return f'<div class="guide-directory" data-guide-directory><div class="directory-filters" role="group" aria-label="{t("Filter by goal", "목적으로 공략 찾기")}" data-directory-controls hidden><button type="button" data-directory-filter="all" aria-pressed="true">{t("All", "전체")}</button>{filters}</div><div class="directory-grid">{cards}</div><nav class="directory-tools" aria-label="{t("News and references", "소식과 참고 자료")}"><a href="{r}updates/">{t("News & patches", "뉴스·패치")}</a><a href="{r}glossary/">{t("KR / EN glossary", "한영 용어집")}</a><a href="{r}screenshots/">{t("Gameplay screenshots", "인게임 스크린샷")}</a></nav><details class="reader-extra"><summary>{t("More reading · class choice, parties and PvP", "더 읽어보기 · 직업 선택·파티·PvP")}</summary><div class="directory-reading">{reading}</div></details></div>'


class Fragments(HTMLParser):
    """Locate complete generated elements without changing their markup or IDs."""
    VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, source):
        super().__init__(convert_charrefs=False)
        self.source=source;self.stack=[];self.ids={};self.offsets=[0]
        for line in source.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
        self.feed(source)
    def pos(self):
        line,col=self.getpos();return self.offsets[line-1]+col
    def handle_starttag(self,tag,attrs):
        start=self.pos();id=dict(attrs).get('id')
        if tag not in self.VOID:self.stack.append((tag,id,start))
        elif id:self.ids[id]=(start,start+len(self.get_starttag_text()))
    def handle_startendtag(self,tag,attrs):
        id=dict(attrs).get('id')
        if id:self.ids[id]=(self.pos(),self.pos()+len(self.get_starttag_text()))
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,-1,-1):
            if self.stack[i][0]==tag:
                _,id,start=self.stack[i];del self.stack[i:]
                if id:self.ids[id]=(start,self.source.index('>',self.pos())+1)
                break
    def get(self,id):
        if id not in self.ids:raise ValueError('Missing reader section: '+id)
        a,b=self.ids[id];return self.source[a:b]


def reader(lang, key, source, panels, tail=(), lead=''):
    """Panels contain complete, non-overlapping source sections; deep IDs survive."""
    k=lang=='ko';t=lambda en,ko:ko if k else en;parts=Fragments(source)
    used=[id for _,_,ids in panels for id in ids]+list(tail)
    ranges=sorted((parts.ids[id][0],parts.ids[id][1],id) for id in used)
    for previous,current in zip(ranges,ranges[1:]):
        if previous[1]>current[0]:raise ValueError(f'Overlapping reader sections: {previous[2]} / {current[2]}')
    nav='';body=''
    for i,(name,title,ids) in enumerate(panels):
        panel_id=f'reader-{key}-{name}'
        nav+=f'<a href="#{ids[0]}" data-reader-tab="{name}" id="{panel_id}-tab"><span>{title[k]}</span></a>'
        body+=f'<details class="reader-panel" id="{panel_id}" data-reader-panel="{name}"{(" open" if i==0 else "")}><summary class="reader-fallback">{title[k]}</summary><div class="reader-body">'+''.join(parts.get(id) for id in ids)+'</div></details>'
    return f'<div class="topic-reader" data-topic-reader="{key}">{lead}<nav class="reader-tabs" data-reader-tabs aria-label="{t("Choose a guide topic", "읽을 주제 선택")}">{nav}</nav>{body}</div>'+''.join(parts.get(id) for id in tail)


def compact_links(lang, base):
    k=lang=='ko';r=base+('ko/' if k else '')
    links=[('pet-growth',('Pet growth','펫 내실')),('gear-targets',('Target gear','목표 장비')),('dungeon-rewards',('Dungeon rewards','던전 보상')),('kinah-farming',('Kinah','키나 파밍'))]
    return '<nav class="reader-related" aria-label="'+('Related growth guides','성장 상세 공략')[k]+'">'+''.join(f'<a href="{r}guides/{slug}/" data-growth-guide="{slug}">{label[k]} →</a>' for slug,label in links)+'</nav>'


def fold(source, id, title, note=''):
    parts=Fragments(source);a,b=parts.ids[id]
    body=parts.get(id).replace(f' id="{id}"','',1)
    # A fragment on the details itself only exposes its summary without scripts.
    # Start folds open; the enhanced reader collapses them before resolving the hash.
    return source[:a]+f'<details class="reader-fold" id="{id}" open><summary><strong>{e(title)}</strong><span>{e(note)}</span></summary><div class="reader-fold-body">{body}</div></details>'+source[b:]


def organize(sub, source, lang, base):
    k=lang=='ko';t=lambda en,ko:ko if k else en;r=base+('ko/' if k else '')
    if sub=='endgame/':
        lead=compact_links(lang,base)+f'<a class="reader-routine-link routine-gateway" href="{r}routines/">{t("Looking for today’s runs? Daily & weekly rewards", "오늘 돌 콘텐츠를 찾는다면? 일일·주간 숙제")} →</a>'
        return reader(lang,'endgame',source,[
            ('route',('What to do first','먼저 할 일'),['after-story']),
            ('rewards',('Reward map','보상 사용처'),['growth-visual']),
            ('bosses',('Choose a boss','보스 고르기'),['boss-guides']),
            ('stuck',('When stuck','성장이 막힐 때'),['priorities','investment','party-prep'])],lead=lead)
    if sub=='routines/':
        source=fold(source,'routine-group-banked',t('Recharging entries & energy','충전되는 입장권·에너지'),t('Check caps before they fill','상한에 닿기 전에 확인'))
        source=fold(source,'routine-group-optional',t('Raids & Abyss','성역·어비스'),t('Choose when you have a goal','목표가 생기면 선택'))
        result=reader(lang,'routines',source,[
            ('daily',('Today','오늘 할 일'),['routine-group-daily','routine-group-banked']),
            ('weekly',('This week','주간 숙제'),['routine-group-weekly','routine-group-optional']),
            ('dungeons',('Daily Dungeons','일일 던전 3종'),['daily-dungeon-choices']),
            ('rewards',('Spend rewards','보상 사용처'),['reward-uses'])],tail=['routine-scope','routine-sources'])
        return '<div class="routine-guide" data-routine-guide>'+result+compact_links(lang,base)+'</div>'
    if sub=='gear/':
        lead=f'<a class="reader-featured growth-gateway" href="{r}guides/gear-targets/"><strong>{t("Looking for your next item?", "다음 장비를 어디서 얻을까?")}</strong><span>{t("Choose your slot and dungeon", "부위별 목표 던전 선택")} →</span></a>'
        return reader(lang,'gear',source,[
            ('enhance',('Enhance','강화 순서'),['upgrade']),
            ('budget',('Investment','투자 판단'),['upgrade-decisions']),
            ('read',('Gear & stats','장비·스탯 읽기'),['gear-item-reader','stats','arcana']),
            ('materials',('Material glossary','재료 사전'),['materials'])],lead=lead)+f'<noscript><style>[data-item-panel][hidden],[data-stat-panel][hidden]{{display:block!important}}</style></noscript>'
    return source


def growth_reader(slug, source, lang):
    k=lang=='ko'
    plans={
        'pet-growth': [('flow',('Growth paths','성장 흐름'),['pet-growth-loop']),('farm',('Soul locations','영혼 사냥터'),['pet-farming']),('family',('Choose a family','종족 선택'),['pet-families']),('spend',('Spend materials','재료 사용'),['pet-spending'])],
        'gear-targets': [('target',('Target gear','목표 장비'),['gear-ladder']),('enhance',('Enhancement','강화 순서'),['gear-investment','gear-small-wins']),('materials',('Get materials','재료 획득처'),['gear-materials']),('fallback',('Vouchers & crafts','교환·제작'),['gear-fallbacks'])],
        'dungeon-rewards': [('choose',('Choose a dungeon','갈 던전 고르기'),['dungeon-visual']),('plans',('Boss & loot','공략·보상'),['dungeon-plans']),('use',('After the run','클리어 이후'),['dungeon-after'])],
        'kinah-farming': [('plan',('Today’s route','오늘의 파밍'),['kinah-plan','kinah-fixed']),('wallet',('Spending example','키나 사용 계산'),['kinah-types']),('market',('Market sales','거래소 판매'),['kinah-market'])],
    }
    if slug=='dungeon-rewards':
        from fieldnotes import BOSSES
        for b in BOSSES:
            source=fold(source,'dungeon-'+b['slug'],b['dungeon'][k],b['name'][k])
    return reader(lang,slug,source,plans[slug],tail=['growth-sources'])

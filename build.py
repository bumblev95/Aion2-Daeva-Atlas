#!/usr/bin/env python3
"""Dependency-free bilingual static publishing for GitHub Pages."""
import json, re, shutil, html, hashlib, subprocess
from pathlib import Path
from datetime import date
from content import CLASSES, GUIDES, GLOSSARY, SOURCES
from visuals import dashboard, explorer, guide_visual
from encounters import boss_lab, insights, source_registry
from fieldnotes import BOSSES, NOTES, KR_SOURCES
import onboarding
import skillbook
import fieldtips
import measurement
import endgame
import routines
import liveops
from bossmedia import validate_evidence
import patchbook

ROOT=Path(__file__).parent
CONFIG=json.loads((ROOT/'site.json').read_text())
measurement.validate(CONFIG)
OUT=ROOT/'docs'
SITE=CONFIG['url'].rstrip('/')
from urllib.parse import urlparse
BASE=urlparse(SITE).path.rstrip('/')+'/'
REPO=CONFIG['repository']
REVIEWED=CONFIG['reviewed']
ads=CONFIG['adsense']
valid_pub=bool(re.fullmatch(r'ca-pub-\d{16}',ads['publisher_id']))
if ads['enabled'] and not (valid_pub and ads['consent_reviewed'] and re.fullmatch(r'\d+',ads['slot'])):
    raise SystemExit('Ads require a valid publisher ID, ad slot and completed consent/privacy review. See OPERATIONS.md.')
E=lambda s:html.escape(str(s),quote=True)
search_index=[]
pages=[]
page_dates={}
L=0
LANG='en'
def t(en,ko):return (en,ko)[L]
def pair(v):return v[L]
def path(sub='',lang=None):
    lang=lang or LANG
    return ('ko/' if lang=='ko' else '')+sub
def href(sub='',lang=None):return BASE+path(sub,lang)
def link(sub,label,css='',lang=None):return f'<a href="{href(sub,lang)}" class="{css}">{label}</a>'
def icon(name,css='icon'):
    return f'<svg class="{css}" aria-hidden="true" viewBox="0 0 48 48" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><use href="{BASE}assets/icons.svg#{name}"/></svg>'
def button(sub,label,primary=False):return link(sub,f'{label}<span class="arrow" aria-hidden="true">↗</span>','btn'+(' primary' if primary else ''))
def brand():return f'<a class="brand" href="{href()}" aria-label="PLAYER’S CODEX home"><span class="brandmark" aria-hidden="true"><b>P</b><i></i></span><span><strong>PLAYER’S <span>CODEX</span></strong><small>YOUR GAME. EVERY ANGLE.</small></span></a>'
def role(r):return {'damage':t('Damage','공격'),'tank':t('Tank','탱커'),'healer':t('Healer','회복'),'support':t('Support','지원')}[r]
def combat_range(r):return t('Melee','근접') if r=='melee' else t('Ranged','원거리')
def adslot():
    if not ads['enabled']:return ''
    return f'<aside class="ad-slot" aria-label="Advertisement"><span>ADVERTISEMENT</span><ins class="adsbygoogle" style="display:block" data-ad-client="{E(ads["publisher_id"])}" data-ad-slot="{E(ads["slot"])}" data-ad-format="auto" data-full-width-responsive="true"></ins><script>(adsbygoogle=window.adsbygoogle||[]).push({{}});</script></aside>'
def header(sub,active):
    groups=[
        (t('Guides by stage','진행 단계별 공략'),[('',t('Home','홈'),'grid'),('start/',t('Early game','초반 공략'),'check'),('endgame/',t('Endgame','엔드게임 공략'),'boss'),('routines/',t('Daily & weekly','일일·주간 숙제'),'check')]),
        (t('Your character','캐릭터 성장'),[('classes/',t('Choose a class','직업 알아보기'),'swords'),('skills/',t('Skills & builds','스킬·빌드'),'book'),('gear/',t('Gear & stats','장비·스탯'),'spark')]),
        (t('Your adventure','모험과 전투'),[('maps/',t('World maps','월드 지도'),'target'),('dungeons/',t('Boss patterns','보스 패턴'),'boss')]),
        (t('More guides','더 찾아보기'),[('insights/',t('Player tips','유저 팁'),'book'),('guides/',t('All guides','전체 공략'),'grid')]),
    ]
    navhtml=''
    for label,items in groups:
        navhtml+=f'<div class="nav-group"><p class="nav-group-label">{label}</p>'
        for p,n,i in items:
            current=sub==p or bool(p and sub.startswith(p))
            navhtml+=f'<a href="{href(p)}" class="side-link{(" active" if current else "")}"{(" aria-current="+chr(34)+"page"+chr(34) if current else "")}>{icon(i)}<span>{n}</span></a>'
        navhtml+='</div>'
    return f'''<a class="skip" href="#main">{t('Skip to content','본문으로 건너뛰기')}</a>
<header class="masthead"><div class="nav">{brand()}<a class="header-game" href="{href()}">AION <span>2</span></a><a class="header-search" href="{href('search/')}" aria-label="{t('Search all guides','전체 공략 검색')}">{icon('search')}<span>{t('Search a class, skill or boss','직업, 스킬, 보스 이름으로 검색')}</span><kbd>/</kbd></a><div class="navtools">{link(sub,'한국어' if LANG=='en' else 'EN','lang',lang='ko' if LANG=='en' else 'en')}<button class="menu" data-menu aria-controls="main-nav" aria-expanded="false" aria-label="{t('Navigation menu','전체 메뉴')}">{icon('grid')}<span>{t('Menu','메뉴')}</span></button></div></div></header>
<button class="nav-backdrop" data-menu-close hidden tabindex="-1" aria-label="{t('Close menu','메뉴 닫기')}"></button><aside class="sidebar" id="main-nav"><div class="side-game"><strong>AION <em>2</em></strong><span class="small muted">{t('Find your next step','다음 플레이를 위한 가이드')}</span></div><nav aria-label="{t('AION 2 navigation','아이온 2 메뉴')}">{navhtml}</nav><div class="side-bottom"><p class="nav-group-label">{t('My tools','플레이 도구')}</p>{link('tools/compare/',t('Compare classes','직업 비교'))}{link('tools/planner/',t('My checklist','나의 체크리스트'))}{link('glossary/',t('KR ↔ EN glossary','한영 용어집'))}</div></aside>'''
def footer():return f'''<footer class="footer"><div class="wrap"><div class="footer-main"><strong class="footer-brand">PLAYER’S CODEX<span> / AION 2</span></strong><nav class="footer-links" aria-label="{t('Footer','하단 메뉴')}">{link('about/',t('About','소개'))}{link('sources/',t('Sources','출처'))}{link('contact/',t('Contact','문의'))}{link('privacy/',t('Privacy','개인정보'))}{link('terms/',t('Terms','이용 안내'))}<a href="{REPO}">GitHub ↗</a></nav></div><p class="footer-bottom">© 2026 PLAYER’S CODEX · {t('Independent fan project. AION 2 artwork and trademarks © NC. Not affiliated with NC.','독립 팬 프로젝트. AION 2 아트워크·상표 © NC. NC와 제휴 관계가 없습니다.')}</p></div></footer>'''
def write(sub,title,description,content,active='',article=False,index=True):
    boss_styles = f'<link rel="stylesheet" href="{BASE}assets/boss-evidence.css?v=boss-scenes-1">' if sub.startswith('dungeons/') else ''
    if 'data-skill=' in content: content += skillbook.widgets(LANG,BASE,set(re.findall(r'data-skill="([a-z0-9-]+)"',content)))
    route=path(sub)
    canonical=SITE+'/'+route
    en=SITE+'/'+path(sub,'en');ko=SITE+'/'+path(sub,'ko')
    meta={'@context':'https://schema.org','@type':'Article' if article else 'WebPage','headline':title,'name':title,'description':description,'url':canonical,'inLanguage':LANG}
    if article:meta.update({'author':{'@type':'Organization','name':'PLAYER’S CODEX editorial','url':SITE+'/about/'},'publisher':{'@type':'Organization','name':'PLAYER’S CODEX'},'datePublished':REVIEWED,'dateModified':REVIEWED})
    adhead=f'<meta name="google-adsense-account" content="{E(ads["publisher_id"])}">' if valid_pub else ''
    if ads['enabled']:adhead+=f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={E(ads["publisher_id"])}" crossorigin="anonymous"></script>'
    adhead+=measurement.head(CONFIG,BASE)
    guidecss=f'<link rel="stylesheet" href="{BASE}assets/practical-guide.css?v=rpg-goals-1">' if sub in ('','start/','endgame/','gear/','routines/','tools/planner/','guides/') else ''
    if sub == 'routines/':guidecss+=f'<link rel="stylesheet" href="{BASE}assets/routines.css?v=1">'
    output=f'''<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | PLAYER’S CODEX</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#101219"><meta name="color-scheme" content="dark"><meta name="robots" content="{'index,follow' if index else 'noindex,follow'}"><link rel="canonical" href="{canonical}"><link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="ko" href="{ko}"><link rel="alternate" hreflang="x-default" href="{en}"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="PLAYER’S CODEX"><meta name="referrer" content="strict-origin-when-cross-origin"><link rel="icon" type="image/svg+xml" href="{BASE}assets/favicon.svg"><link rel="stylesheet" href="{BASE}assets/style.css?v=codex-7"><link rel="stylesheet" href="{BASE}assets/encounters.css?v=codex-6"><link rel="stylesheet" href="{BASE}assets/learn.css?v=codex-6"><script defer src="{BASE}assets/app.js?v=codex-7"></script><script defer src="{BASE}assets/explorer.js?v=codex-6"></script><script defer src="{BASE}assets/encounters.js?v=codex-6"></script><script defer src="{BASE}assets/learn.js?v=codex-7"></script><link rel="stylesheet" href="{BASE}assets/deep-guide.css?v=codex-6"><script defer src="{BASE}assets/deep-guide.js?v=codex-8"></script><script defer src="{BASE}assets/battle.js?v={'boss-scenes-1' if sub.startswith('dungeons/') else 'codex-6'}"></script><script type="application/ld+json">{json.dumps(meta,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script>{adhead}<link rel="stylesheet" href="{BASE}assets/layout.css?v=2">{guidecss}{boss_styles}</head><body data-base="{BASE}">{header(sub,active)}<main id="main">{content}</main>{footer()}{measurement.controls(CONFIG,LANG,BASE)}</body></html>'''
    dest=OUT/route/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(output)
    if index:pages.append(canonical)
def pagehead(title,desc,tag='',crumb=''):
    return f'<div class="page-head"><div class="breadcrumbs">{link("",t("Home","홈"))}<span>/</span><span>{E(crumb or title)}</span></div><h1>{title}</h1><p class="lead">{desc}</p>{f"<span class=\"tag\">{tag}</span>" if tag else ""}</div>'
def classcard(c):return f'''<a href="{href('classes/'+c['id']+'/')}" class="class-card" style="--class-color:{c['color']}" data-class-card data-role="{c['role']}"><span class="mini-arrow" aria-hidden="true">↗</span>{icon(c['icon'],'class-symbol')}<h3>{c['ko'] if L else c['en']}</h3><p>{role(c['role'])} · {combat_range(c['range'])}</p></a>'''
def guidecard(g):
    symbols={'choose-your-class':'swords','first-session':'grid','read-korean-guides':'book','first-group-dungeon':'boss','upgrade-decisions':'spark','pvp-context':'target'}
    return f'''<a class="guide-card" href="{href('guides/'+g['slug']+'/')}"><span class="guide-card-art">{icon(symbols[g['slug']],'guide-glyph')}</span><span class="tag">{pair(g['category'])}</span><h2>{pair(g['title'])}</h2><span class="small muted">{g['minutes']} {t('min read','분 읽기')} <span aria-hidden="true">↗</span></span></a>'''
def sourcelist(keys):
    return '<div class="sources"><strong>'+t('Sources & scope','출처와 적용 범위')+'</strong><ul>'+''.join(f'<li><a href="{E(SOURCES[k]["url"])}" rel="noopener">{E(SOURCES[k]["title"])}</a><span class="source-note">{E(SOURCES[k]["scope"])} · {E(SOURCES[k]["note"])}</span></li>' for k in keys)+'</ul><p class="small muted">'+t('Source review: October 7, 2026. Advice and practice exercises are original editorial analysis, not live gameplay measurements.','출처 검토: 2026년 10월 7일. 조언과 연습 방법은 편집상 분석이며 실제 플레이 측정 결과가 아닙니다.')+'</p></div>'

def home():
    write('',t('AION 2 classes, guides & tools','아이온 2 직업·공략·플레이 도구'),t('Explore AION 2 classes, visual combat basics, guides, comparisons and a personal checklist on PLAYER’S CODEX.','PLAYER’S CODEX에서 아이온 2 직업, 전투 위치, 공략, 직업 비교와 개인 체크리스트를 확인하세요.'),dashboard(LANG,BASE),'home')



def learning():
    for sub,title,desc,body in [
        ('start/',t('AION 2 early-game guide','아이온 2 초반 공략'),t('Progression routes, skill investment, equipment choices and useful settings.','육성 동선·스킬 투자·장비 선택·편의 설정을 정리한 초반 공략.'),onboarding.beginner(LANG,BASE)),
        ('endgame/',t('Endgame guide.','엔드게임 공략.'),t('After the story: Sealed Dungeons, feathers, Monolith rewards, skill points, Daevanion and equipment farming.','스토리 이후 봉인 던전·깃털·모노리스 보상을 스킬 포인트·데바니온·장비 성장으로 연결하는 순서.'),endgame.guide(LANG,BASE)),
        ('routines/',t('Daily & weekly: rewards that make you stronger.','일일·주간 숙제, 보상부터 사용처까지.'),t('Daily Dungeon choices, Duty Missions, weekly activities and how to spend stones, Arcana, pet materials and energy.','일일 던전 선택·사명·주간 콘텐츠와 강화석·아르카나·펫 재료·오드의 사용처를 정리했습니다.'),routines.guide(LANG,BASE)),
        ('gear/',t('Enhance your gear & understand its stats.','장비 강화와 스탯, 알고 키우세요.'),t('Enhancement materials, where to get them, the enhancement steps, equipment options and base stats.','강화 재료·획득처·실제 강화 순서부터 장비 옵션·기본 능력치까지.'),onboarding.gear(LANG,BASE)),
        ('maps/',t('Find your next destination.','다음 목적지를 찾아보세요.'),t('Elyos and Asmodian starting maps, with zoom, markers and route priorities.','천족·마족 시작 지역의 실제 지도와 이동 우선순위.'),onboarding.maps(LANG,BASE)),
        ('skills/',t('Know the skill behind the name.','스킬 이름 너머의 효과까지.'),t('English and Korean names, effects and practical usage.','영문·한국어 이름부터 효과와 실제 사용 시점까지.'),skillbook.library(LANG,BASE))]:
        heading=pagehead(title,desc) if sub!='start/' else ''
        if sub in ('start/','endgame/','maps/'):
            body += liveops.screenshots(LANG,BASE,{'start/':'combat','endgame/':'boss','maps/':'flight'}[sub])
        write(sub,title,desc,f'<div class="wrap">{heading}{body}</div>',sub.rstrip('/'))
        search_index.append({'lang':LANG,'path':path(sub),'title':title,'description':desc,'category':t('Daily & weekly','일일·주간 숙제') if sub=='routines/' else t('Endgame guide','엔드게임 공략') if sub=='endgame/' else t('Early-game guide','초반 공략') if sub=='start/' else t('Character reference','캐릭터 공략'),'keywords':title+' '+desc})
        if sub == 'routines/':
            page_dates[SITE+'/'+path(sub)]=routines.REVIEWED
            search_index.extend(routines.search_entries(LANG,BASE))
    for tip in fieldtips.TIPS:
        search_index.append({'lang':LANG,'path':path('start/'),'anchor':'tip-'+tip['id'],'title':pair(tip['title']),'description':pair(tip['copy']),'category':t('Useful settings','편의 설정'),'keywords':pair(tip['path'])})
    for sk in skillbook.SKILLS:
        sub='skills/'+sk['id']+'/'
        title=sk['ko' if L else 'en']
        desc=pair(sk['effect'])
        body=f'<div class="wrap">{pagehead(title,desc)}<a class="text-link" href="{href("skills/")}?class={sk["cls"]}">← {t("Skill dictionary","스킬 문서 목록")}</a><article class="skill-page">{skillbook.details(sk,LANG,BASE)}</article></div>'
        write(sub,title,desc,body,'skills',True)
        search_index.append({'lang':LANG,'path':path(sub),'title':title,'description':desc,'category':t('Skill dictionary','스킬 문서'),'keywords':' '.join([sk['en'],sk['ko'],*sk['aliases']])})

def dungeons():
    title=t('See the cue. Practise the move.','움직임으로 배우는 보스 패턴.')
    description=t('Automatic animated lessons. Pause, slow down and follow the movement.','자동으로 움직이는 패턴 설명. 멈추거나 느리게 보며 이동을 따라가세요.')
    write('dungeons/',title,description,f'<div class="wrap">{pagehead(title,description)}{boss_lab(LANG,BASE)}</div>','dungeon')
    for b in BOSSES:
        name=pair(b['name']);sub='dungeons/'+b['slug']+'/'
        title=name+t(' — mechanic field guide',' — 기믹 공략')
        desc=pair(b['hook'])
        write(sub,title,desc,f'<div class="wrap">{pagehead(title,desc,crumb=pair(b["dungeon"]))}{boss_lab(LANG,BASE,b["id"])}</div>','dungeon',True)
        search_index.append({'lang':LANG,'path':path(sub),'title':title,'description':desc,'category':t('Boss mechanics','보스 기믹'),'keywords':' '.join(b['name']+b['dungeon'])+' '+' '.join(' '.join(m['title']+m['cue']+m['action']) for m in b['mechanics'])})

def community():
    title=t('Korean players, practical takeaways.','한국 유저의 실전 팁.')
    desc=t('Filter short, attributed notes by class, activity and topic.','직업·콘텐츠·주제별로 골라 보는 짧은 공략 요약.')
    write('insights/',title,desc,f'<div class="wrap">{pagehead(title,desc)}{insights(LANG,BASE)}</div>','insights')
    for n in NOTES:
        search_index.append({'lang':LANG,'path':path('insights/'),'anchor':'note-'+n['id'],'title':pair(n['title']),'description':pair(n['body']),'category':t('KR insight','한국 유저 팁'),'keywords':' '.join(n['classes'])+' '+n['mode']+' '+pair(n['body'])})

def guides():
    write('guides/',t('AION 2 guides','아이온 2 공략 모음'),t('Practical reading for your first character, group play, upgrades and Korean-to-global context.','첫 캐릭터, 파티 플레이, 성장 판단과 한국·글로벌 맥락을 위한 가이드.'),f'<div class="wrap">{pagehead(t("Find your next guide.","필요한 공략을 골라보세요."),t("One useful question at a time. Choose where your next session needs a little clarity.","한 번에 질문 하나씩. 다음 플레이에 도움이 필요한 주제를 골라보세요."))}{routines.gateway(LANG,BASE)}<div class="guide-grid">{"".join(guidecard(g) for g in GUIDES)}</div></div>','guides')
    for g in GUIDES:
        sub='guides/'+g['slug']+'/'
        toc=''.join(f'<li><a href="#section-{i+1}">{pair(h)}</a></li>' for i,(h,p) in enumerate(g['sections']))
        body=''.join(f'<details class="guide-section" id="section-{i+1}"{chr(32)+"open" if i==0 else ""}><summary><span class="step-number">0{i+1}</span><h2>{pair(h)}</h2><span class="detail-toggle" aria-hidden="true">+</span></summary><p>{pair(p)}</p></details>'+ (adslot() if i==2 else '') for i,(h,p) in enumerate(g['sections']))
        related='tools/compare/' if g['slug']=='choose-your-class' else 'glossary/' if g['slug']=='read-korean-guides' else 'tools/planner/'
        expanded={'first-session':'start/','upgrade-decisions':'gear/','first-group-dungeon':'dungeons/','read-korean-guides':'skills/'}
        if g['slug'] in expanded:
            body='<div class="related">'+button(expanded[g['slug']],t('Open the interactive guide','클릭하며 보는 상세 가이드'),True)+'</div>'+body
        relatedlabel=t('Put the guide into practice →','관련 도구로 실천해보기 →')
        content=f'''<div class="wrap">{pagehead(pair(g['title']),pair(g['description']),pair(g['scope']),t('Guides','공략'))}<div class="meta" style="margin:0 0 35px"><span>PLAYER’S CODEX editorial</span><span>{t('Reviewed','검토')} {REVIEWED}</span><span>{g['minutes']} {t('min read','분 읽기')}</span></div><div class="article-layout"><aside class="toc"><strong>{t('In this guide','이 글의 순서')}</strong><ol>{toc}</ol></aside><article class="article-body">{guide_visual(LANG,BASE,g["slug"])}{body}{sourcelist(g['sources'])}<div class="related">{button(related,relatedlabel,True)}</div></article></div></div>'''
        write(sub,pair(g['title']),pair(g['description']),content,'guides',True)
        search_index.append({'lang':LANG,'path':path(sub),'title':pair(g['title']),'description':pair(g['description']),'category':pair(g['category']),'keywords':' '.join(pair(h)+' '+pair(p) for h,p in g['sections'])})

def classes():
    content=f'<div class="wrap">{pagehead(t("AION 2 classes","아이온 2 직업"),t("Tap a class. Explore its role, combat and preparation.","직업을 눌러 역할·전투·준비 항목을 살펴보세요."))}{explorer(LANG,BASE)}</div>'
    write('classes/',t('AION 2 class explorer','아이온 2 직업 탐색'),t('Explore eight AION 2 class playstyles with visual role guides.','여덟 직업의 플레이스타일과 전투 위치를 한눈에 확인하세요.'),content,'classes')
    for c in CLASSES:
        name=c['ko'] if L else c['en'];sub='classes/'+c['id']+'/'
        title=t(c['en']+' playstyle guide',name+' 플레이스타일 가이드')
        sections=[(t('Why put this class on your shortlist?','이 직업을 후보로 생각한다면'),pair(c['fit'])),(t('The trade-off to consider','함께 고려할 점'),pair(c['trade'])),(t('Your first practice exercise','첫 번째 연습'),pair(c['practice'])),(t('How to compare fairly','공정하게 비교하는 방법'),t('Use similar equipment and the same available encounter when comparing classes. Repeat more than one attempt. Record control comfort, missed mechanics and whether the playstyle stays enjoyable after a mistake. Your favourite activity and available play time matter more than an unlabelled tier score.','장비와 전투 조건을 비슷하게 맞추고 여러 번 비교하세요. 조작감, 놓친 패턴, 실수 이후에도 즐겁게 이어갈 수 있는지 기록해보세요. 조건 없는 티어 점수보다 자주 하는 콘텐츠와 실제 플레이 시간이 중요합니다.')),(t('Build and version context','세팅과 버전의 맥락'),t('This profile describes a playstyle; it does not prescribe a rotation, skill build or stat priority. Before following a detailed setup, match its region, date, activity and equipment assumptions to your character. Do not infer a global skill value from a Korean clip or an early design announcement.','이 글은 플레이스타일을 설명하며 스킬 연계, 스킬 구성, 능력치 우선순위를 지정하지 않습니다. 자세한 세팅을 따르기 전 지역, 날짜, 콘텐츠, 장비 전제가 자신의 캐릭터와 맞는지 확인하세요. 한국 영상이나 초기 개발 발표의 수치를 글로벌 수치로 단정하지 마세요.'))]
        content=f'''<div class="wrap">{pagehead(title,pair(c['line']),crumb=t('Classes','직업'))}{explorer(LANG,BASE,c['id'])}<section class="class-reading"><h2>{t('Go deeper','더 알아보기')}</h2>{''.join(f'<details class="guide-section"><summary><h3>{h}</h3><span class="detail-toggle" aria-hidden="true">+</span></summary><p>{p}</p></details>' for h,p in sections)}{sourcelist(['core','official'])}</section></div>'''
        write(sub,title,pair(c['fit']),content,'classes',True)
        search_index.append({'lang':LANG,'path':path(sub),'title':title,'description':pair(c['identity']),'category':t('Class guide','직업 안내'),'keywords':c['en']+' '+c['ko']+' '+role(c['role'])+' '+pair(c['fit'])})

def compare():
    options=lambda selected:''.join(f'<option value="{c["id"]}"{" selected" if c["id"]==selected else ""}>{c["ko"] if L else c["en"]}</option>' for c in CLASSES)
    content=f'''<div class="wrap">{pagehead(t('Compare classes.','직업 비교.'),t('Compare the role, trade-offs and first practice exercise for your shortlist. No invented scores.','역할, 고려할 점, 첫 연습 방법을 비교하세요. 근거 없는 점수는 사용하지 않습니다.'))}<div class="compare-selects"><label class="field" for="class-a">{t('First class','첫 번째 직업')}<select id="class-a">{options('templar')}</select></label><label class="field" for="class-b">{t('Second class','두 번째 직업')}<select id="class-b">{options('gladiator')}</select></label></div><div class="comparison" data-comparison></div><p class="status" data-compare-status role="status"></p><div style="margin:20px 0 40px"><button class="btn" data-share>{t('Copy comparison link ↗','비교 링크 복사 ↗')}</button><span class="share-status" data-share-status role="status"></span></div><noscript><p>{t('JavaScript is needed for the comparison tool. All class profiles can be read below.','비교 도구에는 자바스크립트가 필요합니다. 아래 직업별 글에서 내용을 볼 수 있습니다.')}</p><div class="class-grid">{''.join(classcard(c) for c in CLASSES)}</div></noscript><div class="callout"><p>{t('These are editorial playstyle profiles. They are not measured DPS, current tier rankings, or a guarantee about endgame viability.','편집한 플레이스타일 프로필입니다. 실측 DPS, 현재 티어 순위, 최종 콘텐츠 성능을 보장하는 자료는 아닙니다.')}</p></div>{sourcelist(['core','official'])}<div style="height:35px"></div><script id="class-data" type="application/json">{json.dumps(CLASSES,ensure_ascii=False).replace('<',chr(92)+'u003c')}</script></div>'''
    write('tools/compare/',t('AION 2 class comparison tool','아이온 2 직업 비교 도구'),t('Compare two AION 2 class playstyles side by side and share your shortlist.','아이온 2의 두 직업 플레이스타일을 나란히 비교하고 링크를 공유하세요.'),content,'classes')

def glossary():
    rows=''.join(f'<tr data-term><td lang="ko"><strong>{E(kr)}</strong></td><td lang="en">{E(en)}</td><td><small>{E(note)}</small></td></tr>' for kr,en,note in GLOSSARY)
    content=f'''<div class="wrap">{pagehead(t('KR ↔ EN glossary.','한영 용어 검색.'),t('Korean class names and common community terms. Match skill and item names to your current client before copying a build.','한국어 직업명과 커뮤니티 용어를 영어와 함께 확인하세요. 스킬·아이템 이름은 현재 클라이언트와 대조해야 합니다.'))}<label class="sr-only" for="glossary-search">{t('Search Korean or English terms','한국어·영어 용어 검색')}</label><div class="searchbox">{icon('search')}<input id="glossary-search" data-glossary-search type="search" placeholder="{t('Try 검성, tank, cooldown…','검성, tank, cooldown…')}" autocomplete="off"></div><p class="small muted" data-glossary-count role="status">32 {t('terms','개 용어')}</p><p class="no-results" data-glossary-empty hidden>{t('No matching terms. Try a shorter word.','일치하는 용어가 없습니다. 더 짧은 단어로 검색해보세요.')}</p><div class="table-wrap"><table><thead><tr><th>{t('Korean','한국어')}</th><th>{t('English','영어')}</th><th>{t('Context','맥락')}</th></tr></thead><tbody>{rows}</tbody></table></div></div>'''
    write('glossary/',t('AION 2 Korean–English glossary','아이온 2 한국어·영어 용어집'),t('Search Korean AION 2 class names, combat terms and common guide vocabulary.','아이온 2 한국어·영어 직업명, 전투 용어, 공략 표현을 검색하세요.'),content,'glossary')
    search_index.append({'lang':LANG,'path':path('glossary/'),'title':t('Korean–English glossary','한국어·영어 용어집'),'description':t('32 class names and useful community terms.','직업명과 커뮤니티 용어 32개.'),'category':t('Tool','도구'),'keywords':' '.join(' '.join(row) for row in GLOSSARY)})

def planner():
    content=f'''<div class="wrap">{pagehead(t('My checklist.','나의 체크리스트.'),t('One goal is a good start. Keep your own checklist, then leave yourself a clear next step.','목표 하나면 충분합니다. 나의 할 일을 기록하고 다음 접속 때 이어가세요.'))}{routines.gateway(LANG,BASE)}<div class="planner-layout" data-planner><section class="planner-panel"><span class="eyebrow">{t('MY SESSION','나의 플레이')}</span><h2>{t('Today’s checklist','오늘의 체크리스트')}</h2><p class="small muted">{t('Personal tasks, not an official daily or weekly activity list. Nothing resets automatically.','개인 할 일이며 공식 일일·주간 활동 목록이 아닙니다. 자동 초기화되지 않습니다.')}</p><p class="small" data-progress-text aria-live="polite"></p><div class="progress-track" aria-hidden="true"><div class="progress-fill" data-progress-fill></div></div><div data-task-list></div><form class="task-form" data-task-form><label class="sr-only" for="new-task">{t('Add a personal task','개인 할 일 추가')}</label><input id="new-task" class="task-input" maxlength="160" required placeholder="{t('One thing to work on…','이번에 할 일 하나…')}"><button class="btn primary" type="submit">{t('Add +','추가 +')}</button></form><div class="planner-actions"><button class="btn" data-reset-checks>{t('Uncheck all','전체 체크 해제')}</button><button class="btn" data-export>{t('Export list ↓','목록 내보내기 ↓')}</button></div><p class="status" data-planner-status role="status"></p></section><aside class="planner-panel"><span class="eyebrow">{t('Set a gentle boundary','시간을 가볍게 정해보세요')}</span><h2>{t('How long do you have?','얼마나 플레이할까요?')}</h2><p class="small muted">{t('An editable mindset, not an estimate of dungeon duration. Choose your own activity for the middle block.','던전 소요 시간의 예측이 아닙니다. 가운데 시간에 할 활동을 직접 정하세요.')}</p><div class="budget-choice">{''.join(f'<button class="filter" data-budget="{n}" aria-pressed="false">{n} {t("min","분")}</button>' for n in [30,60,90])}</div><div data-session-plan aria-live="polite"></div><div class="callout"><p>{t('Finish by writing one sentence: “Next time, I will…” A clear stopping point helps you return without rebuilding the whole plan.','마지막에는 “다음에는…”으로 시작하는 문장을 하나 남겨보세요. 다시 들어왔을 때 계획을 처음부터 세우지 않아도 됩니다.')}</p></div></aside></div><noscript><p>{t('The interactive planner needs JavaScript. You can use the first-session guide without it.','인터랙티브 플래너에는 자바스크립트가 필요합니다. 첫 접속 가이드는 자바스크립트 없이도 읽을 수 있습니다.')}</p></noscript></div>'''
    write('tools/planner/',t('AION 2 personal session planner','아이온 2 개인 플레이 플래너'),t('A browser-saved personal checklist and a 30, 60 or 90 minute session plan.','브라우저에 저장되는 개인 체크리스트와 30·60·90분 플레이 계획.'),content,'planner')
    search_index.append({'lang':LANG,'path':path('tools/planner/'),'title':t('Your session planner','나의 플레이 플래너'),'description':t('Save a personal checklist and export your plan.','개인 체크리스트를 저장하고 계획을 내보내세요.'),'category':t('Tool','도구'),'keywords':'checklist daily plan 할일 체크리스트 숙제'})

def info():
    about=f'''<p>{t('PLAYER’S CODEX is an independent, AI-assisted game guide and tools project maintained by GitHub user bumblev95. AION 2 is its first game hub. Its purpose is to help English-speaking and Korean-speaking readers make sense of class choices and the context around game advice. It is not an official NC publication.','PLAYER’S CODEX는 GitHub 사용자 bumblev95가 관리하는 독립 게임 공략·도구 프로젝트입니다. AI의 도움을 받아 제작했으며 아이온 2가 첫 번째 게임 허브입니다. 영어·한국어 독자가 직업 선택과 공략의 맥락을 이해하도록 돕습니다. NC 공식 간행물이 아닙니다.')}</p><h2>{t('What we publish','제공하는 내용')}</h2><p>{t('Our launch collection combines sourced orientation with original decision frameworks and practical browser tools. Class comparisons describe playstyle trade-offs. They do not claim live damage testing, professional player credentials, or privileged access to the game.','초기 가이드는 출처를 확인한 안내, 독자적인 판단 방법, 브라우저 도구로 구성됩니다. 직업 비교는 플레이스타일의 고려 사항을 설명합니다. 실제 피해량 측정, 전문 플레이어 경력, 게임의 비공개 정보 접근을 주장하지 않습니다.')}</p><h2>{t('Three labels we keep separate','구분하는 세 가지 정보')}</h2><ul><li>{t('Official fact: a narrow claim linked to a publisher source.','공식 사실: 제작사 출처가 뒷받침하는 구체적인 주장.')}</li><li>{t('Editorial advice: an explanation, exercise or decision method developed for this guide.','편집 조언: 이 가이드를 위해 작성한 설명, 연습법, 판단 방법.')}</li><li>{t('Unverified detail: something we cannot currently substantiate. We omit numerical recommendations when their evidence is missing.','미확인 정보: 현재 입증하지 못한 내용. 근거가 부족한 수치 추천은 제외합니다.')}</li></ul><h2>{t('Updates and corrections','수정과 업데이트')}</h2><p>{t('Review dates reflect a content review, not a live connection to the game. We update dates when we review the actual substance. A Korean balance change does not automatically become a global recommendation. Readers can submit a source or correction through the public issue tracker.','검토 날짜는 내용 확인 시점을 뜻하며 게임에 실시간 연결되었다는 의미가 아닙니다. 실제 내용을 검토했을 때 날짜를 바꿉니다. 한국 밸런스 변경을 곧바로 글로벌 추천으로 적용하지 않습니다. 공개 이슈 게시판에서 출처나 수정 요청을 제출할 수 있습니다.')}</p><h2>{t('Funding','운영과 광고')}</h2><p>{t('The site is free to read. Advertising may support its operation after the relevant account, site and consent setup is complete. No payment changes our class descriptions. At this release, advertising and analytics scripts are disabled.','사이트는 무료로 읽을 수 있습니다. 계정·사이트·동의 설정이 완료되면 광고가 운영을 지원할 수 있습니다. 금전 제공이 직업 설명을 바꾸지는 않습니다. 이번 배포에서는 광고와 방문 분석 스크립트가 꺼져 있습니다.')}</p>'''
    privacy=f'''<p>{t('Effective October 7, 2026. This notice describes this release of PLAYER’S CODEX.','시행일: 2026년 10월 7일. 현재 배포된 PLAYER’S CODEX의 데이터 처리를 설명합니다.')}</p><h2>{t('What the website stores','사이트가 저장하는 정보')}</h2><p>{t('The planner saves task text and completion state in your browser’s local storage under daeva-atlas-planner-v1. A saved class preference uses raidnote-aion2-class-v1. Beginner checklist completion uses players-codex-start-v1. Map completion uses players-codex-map-v1. Old lesson progress may remain under players-codex-lessons-v1; this version no longer creates it. Temporary gear checks last only for the current visit. We do not upload these to a server. It persists until you clear it or clear browser storage, and it does not sync between devices. Avoid putting private account information in a task.','플래너는 할 일과 완료 여부를 브라우저의 daeva-atlas-planner-v1 로컬 저장소에 저장합니다. 내 직업 선택은 raidnote-aion2-class-v1에, 초보 체크리스트 완료 여부는 players-codex-start-v1에 저장됩니다. 지도 완료 표시는 players-codex-map-v1에 저장됩니다. 이전 버전의 연습 진도 players-codex-lessons-v1이 남아 있을 수 있지만 현재 버전은 새로 기록하지 않습니다. 장비 점검표는 이번 방문에만 유지됩니다. 이 정보는 서버에 업로드하지 않습니다. 직접 삭제하거나 브라우저 데이터를 지울 때까지 남으며 기기 간 동기화되지 않습니다. 할 일에 비공개 계정 정보를 적지 마세요.')}</p><button class="btn" data-clear-local>{t('Delete my saved data','저장된 데이터 삭제')}</button><p class="status" data-clear-status role="status"></p><h2>{t('Hosting and external links','호스팅과 외부 링크')}</h2><p>{t('GitHub Pages delivers this website and may process request information such as IP addresses and access logs under GitHub’s own policies. When you follow a link to NC, Steam, GitHub or another website, that service handles your visit under its policies. Fonts are local or system resources. Skill icons load from MetaBot or Aion2t.com, terrain tiles from The Hidden Gaming Lair, and Korean video thumbnails from YouTube. Boss animations run on this site. Gameplay videos and KR loops open on the original YouTube or Inven page. These services receive your network request and apply their own policies. YouTube playback may include platform advertising or storage.','GitHub Pages가 사이트를 제공하며 GitHub 자체 정책에 따라 IP 주소와 접속 기록 같은 요청 정보를 처리할 수 있습니다. NC, Steam, GitHub 등 외부 링크로 이동하면 해당 서비스의 정책이 적용됩니다. 글꼴은 기기 기본 자원 또는 자체 파일입니다. 스킬 아이콘은 MetaBot 또는 Aion2t.com, 지도 타일은 The Hidden Gaming Lair, 한국 영상 썸네일은 YouTube에서 불러옵니다. 보스 애니메이션은 사이트 안에서 재생됩니다. 실제 영상과 한국 반복 장면은 YouTube·인벤 원문 링크로 열립니다. 각 서비스는 네트워크 요청을 받고 자체 정책을 적용하며 YouTube 재생에는 플랫폼 광고·저장 기능이 포함될 수 있습니다.')}</p><p><a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub General Privacy Statement ↗</a></p><h2>{t('Advertising and analytics','광고와 방문 분석')}</h2><p>{t('This release includes an AdSense publisher verification tag; the tag and ads.txt do not themselves show ads or track visits. Ad serving remains off pending account review and the required advertising consent setup. Google Analytics collection is not active while the dedicated measurement ID is unconfigured. When activated, analytics loads only after you choose Allow analytics; the footer Analytics preferences control lets you decline or withdraw. The site sends page paths and fixed interaction categories, not planner text or search terms. Analytics consent is saved locally for up to 180 days under players-codex-analytics-consent-v1; analytics cookies use a site-specific pcx prefix. Advertising consent is handled separately, with a Google-certified CMP where required.','AdSense 게시자 확인 태그를 추가했습니다. 이 태그와 ads.txt 자체는 광고를 표시하거나 방문을 추적하지 않습니다. 계정 심사와 광고 동의 설정이 끝나기 전까지 광고 송출은 꺼져 있습니다. 전용 측정 ID가 미설정된 현재는 Google Analytics가 수집하지 않습니다. 연결 후에는 방문자가 분석 허용을 선택해야만 분석 코드를 불러오며, 하단 방문 통계 설정에서 거절하거나 철회할 수 있습니다. 페이지 경로와 정해진 기능 이용 분류를 보내며 플래너 내용과 검색어는 보내지 않습니다. 분석 선택은 players-codex-analytics-consent-v1에 최대 180일 저장되며 분석 쿠키에는 사이트 전용 pcx 접두사를 사용합니다. 광고 동의는 필요한 지역의 Google 인증 CMP를 포함해 별도로 설정합니다.')}</p><h2>{t('Contact','문의')}</h2><p>{t('For site or privacy questions, use the project issue tracker. GitHub issues are public; do not include passwords, account identifiers, payment details or other private information. A GitHub account is required to submit an issue.','사이트·개인정보 관련 질문은 프로젝트 이슈 게시판을 이용하세요. GitHub 이슈는 공개되므로 비밀번호, 계정 식별 정보, 결제 내용 등 비공개 정보를 적지 마세요. 이슈 작성에는 GitHub 계정이 필요합니다.')}</p><p><a href="{REPO}/issues">{t('Open the issue tracker','이슈 게시판 열기')} ↗</a></p>'''
    privacy+=f'<h2>{t("Damage calculator and game images","DPS 계산기와 게임 이미지")}</h2><p>{t("Saved DPS comparisons, including build names and skill inputs, stay in this browser under players-codex-dps-v1. They are not sent to NC or analytics. The delete button above removes them. Gameplay images load from the publisher’s Steam CDN, which receives the image request. The page refreshes our collected news snapshot without sending your build inputs.","저장한 DPS 비교의 빌드 이름·스킬 입력값은 이 브라우저의 players-codex-dps-v1에만 남습니다. NC나 방문 분석에 전송하지 않습니다. 위 기기 데이터 삭제 버튼으로 함께 지울 수 있습니다. 인게임 이미지는 공식 Steam CDN에서 불러오며 해당 서비스는 이미지 요청을 받습니다. 뉴스 화면은 수집본을 갱신하며 빌드 입력값을 보내지 않습니다.")}</p>'
    if CONFIG.get('analytics',{}).get('enabled'):
        privacy=privacy.replace('Google Analytics collection is not active while the dedicated measurement ID is unconfigured. When activated, analytics loads only after you choose Allow analytics;', 'Google Analytics is connected to a dedicated web stream. Analytics loads only after you choose Allow analytics;').replace('전용 측정 ID가 미설정된 현재는 Google Analytics가 수집하지 않습니다. 연결 후에는 방문자가 분석 허용을 선택해야만 분석 코드를 불러오며,', 'Google Analytics 전용 웹 스트림이 연결되어 있습니다. 방문자가 분석 허용을 선택해야만 분석 코드를 불러오며,')
        about=about.replace('At this release, advertising and analytics scripts are disabled.', 'Advertising is disabled; optional analytics requires your consent.').replace('이번 배포에서는 광고와 방문 분석 스크립트가 꺼져 있습니다.', '광고는 꺼져 있으며 선택적 방문 분석에는 방문자의 동의가 필요합니다.')
    privacy+=f'<p><a href="https://policies.google.com/privacy">Google Privacy Policy ↗</a> · <a href="https://policies.google.com/technologies/partner-sites">'+t('How Google uses information from partner sites','Google의 파트너 사이트 정보 처리 안내')+' ↗</a></p>'
    contact=f'''<p>{t('Found an outdated detail, a broken page or a translation that misses the meaning? Send a clear correction through our GitHub issue tracker. This is the site’s current contact channel.','오래된 정보, 깨진 페이지, 의미가 맞지 않는 번역을 발견했다면 GitHub 이슈로 알려주세요. 현재 사이트의 문의 창구입니다.')}</p><p><a class="btn primary" href="{REPO}/issues/new?template=correction.yml">{t('Report a correction ↗','수정 요청하기 ↗')}</a></p><h2>{t('What helps us verify a correction','확인에 도움이 되는 내용')}</h2><ol><li>{t('The guide URL and the sentence that needs changing.','수정할 공략 주소와 문장.')}</li><li>{t('Your game region, the relevant update date and the activity.','게임 지역, 관련 업데이트 날짜, 콘텐츠.')}</li><li>{t('A public official source, or a clear description of a reproducible observation.','공개 공식 출처 또는 반복 확인할 수 있는 관찰 설명.')}</li></ol><p>{t('GitHub requires an account to submit issues, and reports are public. Please do not share credentials, payment details or private screenshots. Game account or billing support belongs with NC, not this fan project.','이슈 작성에는 GitHub 계정이 필요하며 내용은 공개됩니다. 로그인 정보, 결제 내용, 비공개 스크린샷을 올리지 마세요. 게임 계정·결제 지원은 이 팬 프로젝트가 아닌 NC에 문의해야 합니다.')}</p>'''
    terms=f'''<p>{t('PLAYER’S CODEX provides educational game commentary and planning tools. It is an independent fan publication and is not endorsed by NC. AION 2, class names and related trademarks belong to their respective owners.','PLAYER’S CODEX는 게임 해설과 계획 도구를 제공하는 독립 팬 프로젝트이며 NC의 인증을 받지 않았습니다. 아이온 2, 직업명과 관련 상표의 권리는 각 권리자에게 있습니다.')}</p><h2>{t('Using a guide','공략 이용 안내')}</h2><p>{t('Game rules, availability and balance change. Check the current official notice and in-game text before making a decision involving money, limited resources or account changes. Editorial advice does not guarantee a result. The planner is a personal organisational tool, not an automated game client.','게임 규칙, 이용 가능 범위, 밸런스는 바뀔 수 있습니다. 금전, 한정 재화, 계정 변경과 관련한 결정 전에는 최신 공식 공지와 게임 안의 설명을 확인하세요. 편집 조언이 결과를 보장하지는 않습니다. 플래너는 개인 정리 도구이며 게임 자동화 프로그램이 아닙니다.')}</p><h2>{t('Attribution and artwork','출처와 일러스트')}</h2><p>{t('Our articles link to their sources and use original explanations. The AION 2 banner uses publisher promotional artwork, credited to NC. Class symbols, diagrams and teaching animations are original illustrations. Real game skill icons and tooltip facts are sourced from MetaBot and Aion2t.com. Boss animations summarise linked Korean guides; distances and playback timing are illustrative. Gameplay videos open on their original YouTube or Nirr / Inven page. Map terrain and location data are sourced from The Hidden Gaming Lair with attribution. Game artwork and data belong to NC. Linking to a source does not imply a partnership.','글에는 출처 링크와 직접 작성한 설명을 제공합니다. AION 2 배너는 NC의 홍보 아트워크를 출처 표시와 함께 사용합니다. 직업 기호·도해·설명 애니메이션은 자체 제작했습니다. 실제 스킬 아이콘과 툴팁 정보는 MetaBot·Aion2t.com을 참고합니다. 보스 애니메이션은 연결된 한국 공략의 기믹을 요약하며 거리와 재생 시간은 설명용입니다. 실제 영상은 원본 YouTube 또는 Nirr의 인벤 페이지로 연결합니다. 지도 지형과 위치 데이터는 출처를 표시한 The Hidden Gaming Lair 자료이며 게임 아트워크·데이터의 권리는 NC에 있습니다. 출처 링크가 제휴 관계를 의미하지는 않습니다.')}</p><h2>{t('Corrections','수정 요청')}</h2><p>{t('If you believe content is inaccurate or infringes your rights, identify the page and the issue through the contact channel. Do not repost other creators’ full guides into a public report.','정보 오류나 권리 침해가 있다고 판단되면 문의 창구에서 해당 페이지와 문제를 알려주세요. 다른 제작자의 전체 공략을 공개 이슈에 재게시하지 마세요.')}</p>'''
    sourcebody=f'''<p>{t('This is a curated source register, not a live news feed. The current guide collection was reviewed on October 7, 2026. We do not publish a new “updated” date simply because the website was rebuilt.','실시간 뉴스 피드가 아닌 출처 목록입니다. 현재 가이드의 검토일은 2026년 10월 7일입니다. 사이트를 다시 빌드했다는 이유만으로 검토 날짜를 바꾸지 않습니다.')}</p><h2>{t('The source register','출처 목록')}</h2>{sourcelist(list(SOURCES))}<h2>{t('Publication log','발행 기록')}</h2><p><strong>2026-10-07 · {t('First edition','첫 번째 버전')}</strong><br>{t('Published six editorial guides, eight class profiles, a class comparison tool, a bilingual glossary and a browser-local planner. Ads and analytics remain disabled. No live combat benchmarks have been published.','편집 가이드 6개, 직업 프로필 8개, 직업 비교, 한영 용어집, 브라우저 플래너를 공개했습니다. 광고·분석 스크립트는 꺼져 있으며 실제 전투 벤치마크는 공개하지 않았습니다.')}</p>'''
    sourcebody += f'<h2>{t("Visual field-guide update","시각 공략 업데이트")}</h2><p>{t("16 boss mechanics, 21 short community notes and 15 attributed sources. KR source dates are retained; Global mechanics have not been independently checked.","보스 기믹 16개, 커뮤니티 팁 21개, 출처 15개를 추가했습니다. 한국 원문의 작성일을 유지하며 글로벌 기믹은 별도로 검증하지 않았습니다.")}</p>' + source_registry(LANG)
    sourcebody += '<h2>'+t('Global beginner edition','글로벌 초보 가이드 업데이트')+'</h2><p>'+t('Separate early-game and endgame guides, four progression stages including post-story growth, four live maps, item anatomy, six base stats, 280 skill documents, 16 animated boss mechanics and 384 map locations.','초반·엔드게임 공략을 분리하고 스토리 이후를 포함한 성장 단계 4개, 실제 지도 4개, 장비 툴팁, 기본 스탯 6개, 스킬 문서 280개, 보스 패턴 애니메이션 16개와 지도 위치 384곳을 제공합니다.')+'</p>'+onboarding.evidence(LANG,*onboarding.SOURCES.keys())+'<p><a href="https://metabot.gg/en/aion-2/skills">MetaBot skill reference ↗</a></p><p><a href="https://www.youtube.com/watch?v=3OXxi7f1coQ">김호러 Horror · Korean dungeon footage ↗</a> · <a href="https://www.youtube.com/watch?v=Hl0Ky59z8jg">만두집아들 · Nuakum guide ↗</a></p>'
    sourcebody += '<h2>'+t('Reader-submitted practical tips','독자가 보내준 실전 팁')+'</h2>'+fieldtips.source_note(LANG)
    for sub,title,desc,body in [
        ('about/',t('About PLAYER’S CODEX','PLAYER’S CODEX 소개'),t('An independent guide with visible sources and clear editorial boundaries.','출처와 편집 범위를 명확하게 설명하는 독립 가이드.'),about),
        ('privacy/',t('Privacy & local data','개인정보와 기기 저장'),t('What this release stores and how to delete your saved planner.','현재 버전이 저장하는 정보와 플래너 삭제 방법.'),privacy),
        ('contact/',t('Contact & corrections','문의와 수정 요청'),t('Help make the guide more useful with a source-backed correction.','출처가 있는 수정 요청으로 가이드의 품질을 높여주세요.'),contact),
        ('terms/',t('Terms & disclaimer','이용 안내와 면책'),t('How to use this independent fan guide.','독립 팬 가이드의 이용 안내.'),terms),
        ('sources/',t('Sources & publication log','출처와 발행 기록'),t('The evidence behind this edition, and what has actually changed.','이번 버전의 정보 출처와 실제 변경 내용을 확인하세요.'),sourcebody)]:
        write(sub,title,desc,f'<div class="wrap">{pagehead(title,desc)}<div class="prose">{body}</div></div>')

def searchpage():
    content=f'''<div class="wrap">{pagehead(t('Find a guide.','어떤 정보가 궁금한가요?'),t('Search class names in English or Korean, guide topics and planning tools.','영어·한국어 직업명, 공략 주제, 플레이 도구를 검색하세요.'))}<form data-search-form role="search"><label class="sr-only" for="site-search">{t('Search all guides','모든 공략 검색')}</label><div class="searchbox">{icon('search')}<input id="site-search" data-site-search type="search" name="q" placeholder="{t('Class, PvP, Korean guide…','직업, PvP, 한국 공략…')}" autocomplete="off"><button type="submit" class="btn">{t('Search','검색')}</button></div></form><p class="small muted" data-search-status role="status">{t('Loading search…','검색 준비 중…')}</p><div class="search-results" data-search-results></div><noscript><p>{t('Search needs JavaScript. Browse all articles in the guide library.','검색에는 자바스크립트가 필요합니다. 공략 모음에서 모든 글을 확인하세요.')}</p>{link('guides/',t('Browse guides','공략 보기'),'btn')}</noscript></div>'''
    write('search/',t('Search AION 2 guides','아이온 2 공략 검색'),t('Search PLAYER’S CODEX guides and tools.','PLAYER’S CODEX의 공략과 도구를 검색하세요.'),content,index=False)

def layoutpreview():
    revision=hashlib.sha256((ROOT/'assets/practical-guide.css').read_bytes()).hexdigest()[:10]
    content=f'''<div class="wrap">{pagehead(t('Responsive preview','모바일 화면 미리보기'),t('Live pages at narrow screen widths.','좁은 화면에서 보는 실제 페이지입니다.'))}<label class="small">Preview <select data-layout-route><option value="?preview={revision}">Home</option><option value="start/?preview={revision}">Early game</option><option value="endgame/?preview={revision}">Endgame</option><option value="gear/?preview={revision}">Gear &amp; stats</option><option value="maps/?preview={revision}">Maps</option><option value="skills/?preview={revision}">Skills</option><option value="dungeons/?preview={revision}">Boss videos</option></select></label><div style="display:flex;gap:20px;align-items:flex-start;overflow:auto;padding-bottom:20px"><div><p class="small">English · 390px</p><iframe title="English mobile preview" src="{href('',lang='en')}?preview={revision}" width="390" height="1650" style="display:block;border:1px solid #414356;border-radius:8px"></iframe></div><div><p class="small">한국어 · 360px</p><iframe title="Korean mobile preview" src="{href('',lang='ko')}?preview={revision}" width="360" height="1650" style="display:block;border:1px solid #414356;border-radius:8px"></iframe></div></div></div>'''
    write('tools/layout-preview/',t('Responsive preview','모바일 화면 미리보기'),t('PLAYER’S CODEX layout review.','PLAYER’S CODEX 화면 검토.'),content,index=False)

def livepages():
    for sub,title,desc,body in [
        ('updates/',t('AION 2 news & patch changes','아이온 2 뉴스·패치 변경사항'),t('Official Korea and North America updates with reviewed class impact.','한국·북미 공식 업데이트와 직업별 변경 요약.'),liveops.news(LANG,BASE)+liveops.coverage(LANG)),
        ('tools/dps/',t('AION 2 DPS record comparisons','아이온 2 실전 DPS 비교'),t('Reviewed boss DPS records and class indices with regions, sample counts and source links.','한국 보스별 DPS 기록과 글로벌 전투력 지수, 표본 수와 출처를 함께 비교합니다.'),liveops.dps(LANG,BASE)),
        ('screenshots/',t('AION 2 gameplay screenshots','아이온 2 인게임 스크린샷'),t('Official in-game combat, boss and flight frames with source credits.','공식 전투·보스·비행 장면과 원본 출처.'),liveops.screenshots(LANG,BASE)),
    ]:
        write(sub,title,desc,'<div class="wrap">'+body+'</div>')
        search_index.append({'lang':LANG,'path':path(sub),'title':title,'description':desc,'category':t('Live tools','업데이트·계산 도구'),'keywords':title+' '+desc+' DPS eDPS buff nerf patch 버프 너프 조정 최신'})
    for item in patchbook.patches(liveops.load('news.json')):
        sub=patchbook.detail_path(item)
        title=patchbook.title(item,LANG)
        desc=item.get('summary',{}).get(LANG) or t('Official patch changes awaiting review.','공식 패치의 전체 변경사항을 검토하고 있습니다.')
        content=liveops.resources(BASE)+patchbook.render_detail(item,LANG,BASE)
        write(sub,title,desc,'<div class="wrap">'+content+'</div>','updates/')
        page_dates[SITE+'/'+path(sub)]=(item.get('reviewedAt') or item.get('sourceUpdatedAt') or REVIEWED)[:10]
        search_index.append({'lang':LANG,'path':path(sub),'title':title,'description':desc,'category':t('Patch notes','패치 상세'),'keywords':title+' '+desc+' '+' '.join(g['info'][LANG] for g in patchbook.class_groups(item))+' 버프 너프 조정 buff nerf patch'})

def build():
    global L,LANG
    validate_evidence()
    subprocess.run(['node', str(ROOT/'scripts/build_dps_rankings.js'), '--build'], cwd=ROOT, check=True)
    if OUT.exists():shutil.rmtree(OUT)
    OUT.mkdir();shutil.copytree(ROOT/'assets',OUT/'assets')
    for L,LANG in enumerate(['en','ko']):
        home();learning();dungeons();community();guides();classes();compare();glossary();planner();info();livepages();searchpage();layoutpreview()
    (OUT/'data').mkdir()
    shutil.copyfile(ROOT/'data/news.json',OUT/'data/news.json')
    (OUT/'data/dps.json').write_text(json.dumps(liveops.catalog(),ensure_ascii=False,separators=(',',':'))+'\n')
    for name in ('dps-rankings.json','dps-rankings.csv'):
        shutil.copyfile(ROOT/'data'/name,OUT/'data'/name)
    (OUT/'search-index.json').write_text(json.dumps(search_index,ensure_ascii=False,separators=(',',':')))
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+E(url)+'</loc><lastmod>'+page_dates.get(url,REVIEWED)+'</lastmod></url>' for url in pages)+'</urlset>')
    measurement.write_verification(CONFIG,OUT)
    (OUT/'.nojekyll').write_text('')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+SITE+'/sitemap.xml\n')
    if valid_pub:(OUT/'ads.txt').write_text('google.com, '+ads['publisher_id'].removeprefix('ca-')+', DIRECT, f08c47fec0942fa0\n')
    L=0;LANG='en'
    (OUT/'404.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Page not found | PLAYER’S CODEX</title><meta name="robots" content="noindex"><link rel="stylesheet" href="{BASE}assets/style.css?v=codex-7"><link rel="stylesheet" href="{BASE}assets/encounters.css?v=codex-6"></head><body><main class="wrap"><div class="page-head"><div class="eyebrow">PLAYER’S CODEX · 404</div><h1>This path leads elsewhere.</h1><p>The guide you requested could not be found.</p>{button("","Back to the field guide",True)}</div></main></body></html>')
    print(f'Built {len(pages)} indexable pages + search/layout previews and 404; {len(search_index)} search entries.')
if __name__=='__main__':build()

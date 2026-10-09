"""Patch desk, an explicit DPS model and attributed NC gameplay screenshots."""
import html
import json
import re
import hashlib
from pathlib import Path
from content import CLASSES
import dpsrules
import dpsmath
import dpslevels
import dpsranking
import patchbook

ROOT = Path(__file__).parent
E = lambda x: html.escape(str(x), quote=True)

def load(name):
    return json.loads((ROOT/'data'/name).read_text())

def resources(base):
    return f'<link rel="stylesheet" href="{base}assets/liveops.css?v=2"><link rel="stylesheet" href="{base}assets/patchbook.css?v=1"><script defer src="{base}assets/patchbook.js?v=2"></script><script defer src="{base}assets/news.js?v=2"></script>'+patchbook.config()

def catalog(skill_level=1):
    skills = load('skills.json')
    resource_data = load('dps-resources.json')
    source_hash = hashlib.sha256((ROOT/'data/skills.json').read_bytes()).hexdigest()
    mp = resource_data['skills'] if resource_data['skillSourceHash'] == source_hash else {}
    result = []
    for c in CLASSES:
        candidates = []
        audits = []
        for s in skills:
            if s['cls'] != c['id'] or s['kind'] != 'active': continue
            cd = re.fullmatch(r'([\d.]+)s', s['cooldown'])
            model = dpsmath.damage(s)
            if skill_level != 1:
                model = dpslevels.model(s, model, skill_level)
            audits.append(dpsmath.audit(s, model))
            candidate = dict(id=s['id'],en=s['en'],ko=s['ko'],cast=1,hits=1,
                cooldown=float(cd[1]) if cd else 0,url=s['url'],icon=s['icon'],effect=s['en_data']['effect'],
                **dpsrules.rules(s,mp))
            candidate.update(model)
            if skill_level != 1:
                candidate.update(dpslevels.snapshot()['skills'][s['id']]['metadata'][str(skill_level)])
            candidates.append(candidate)
        rows = [x for x in candidates if x['damageStatus'] == 'direct']
        # Every known direct term is available, including conditional zero-CD
        # attacks. Basic combo cadence is still an explicit timing limitation.
        conditional = lambda x: bool(x['requires'] or x['elementCost'])
        ordered = [x for x in rows if x['cooldown'] > 0] + [x for x in rows if x['cooldown'] == 0 and conditional(x)] + [x for x in rows if x['cooldown'] == 0 and not conditional(x)]
        direct_count = len(rows)
        result.append(dict(id=c['id'],en=c['en'],ko=c['ko'],color=c['color'],skills=ordered,
                           candidates=candidates, directCount=direct_count, omitted=12-direct_count,
                           damageAudit=audits,
                           conditionAudit=[dpsrules.audit(s,dpsrules.rules(s,mp)) for s in skills
                                           if s['cls']==c['id'] and s['kind']=='active']))
    rule_hash = hashlib.sha256((ROOT/'data/skills.json').read_bytes() +
        (ROOT/'data/dps-resources.json').read_bytes() + (ROOT/'dpsrules.py').read_bytes() +
        (ROOT/'dpsmath.py').read_bytes()).hexdigest()
    if skill_level != 1:
        rule_hash = hashlib.sha256((rule_hash + json.dumps(dpslevels.snapshot(), sort_keys=True)).encode()).hexdigest()
    return dict(version='conditional-rotation-v3',sourceDate=load('skill-snapshot.json')['reviewedAt'] if skill_level == 1 else dpslevels.snapshot()['reviewedAt'],
                sourceHash=rule_hash,conditionReviewDate='2026-10-08',
                conditionsVerified=source_hash == dpsrules.REVIEWED_SKILL_HASH,
                damageReviewDate=dpsmath.REVIEWED_AT,
                damageVerified=source_hash == dpsmath.REVIEWED_SKILL_HASH,
                states=[dict(id=s,en=en,ko=ko,control=s in dpsrules.CONTROL) for s,en,ko in dpsrules.STATES],classes=result)

def patch_card(item,lang,base):
    return patchbook.patch_card(item,lang,base)

def news(lang,base):
    k=lang=='ko';t=lambda a,b:b if k else a;data=load('news.json');r=base+('ko/' if k else '')
    sources=data['sources']
    items=sorted((x for s in sources for x in s['items']),key=lambda x:x.get('publishedAt') or '',reverse=True)
    cards=''.join(patch_card(x,lang,base) for x in items)
    options=''.join(f'<option value="{x["id"]}">{E(x["ko" if k else "en"])}</option>' for x in CLASSES)+f'<option value="brawler">{t("Brawler · KR","권성 · 한국판")}</option>'
    return resources(base)+f'''<section class="live-desk" data-news-desk data-lang="{lang}" data-feed="{base}data/news.json"><div class="desk-intro"><span class="section-kicker">PATCH DESK / AION 2</span><h1>{t('What changed. Who is affected.','무엇이 바뀌었고,<br>누가 영향을 받는지.')}</h1><p>{t('Official announcements, readable change summaries and class impact. Korea and North America stay separate.','공식 소식, 변경 요약, 직업별 영향을 한곳에서. 한국과 북미 패치를 구분해 보여줍니다.')}</p></div><div class="feed-status"><span class="feed-dot"></span><p data-news-status role="status">{t('Source check','원문 확인')}: {E(data['checkedAt'])} · {t('Hourly collection · page refresh every 5 minutes','매시간 수집 · 열린 화면은 5분마다 재확인')}</p><button type="button" class="btn" data-news-refresh>{t('Refresh','새로 확인')}</button></div><div class="desk-controls"><label>{t('Region','서버 지역')}<select data-news-region><option value="NA">{t('North America · US / Canada','북미 · 미국 / 캐나다')}</option><option value="KR">{t('Korea','한국')}</option><option value="all">{t('All regions','모든 지역')}</option></select></label><label>{t('Show','표시')}<select data-news-kind><option value="all">{t('News & patches','소식·패치 전체')}</option><option value="patch" selected>{t('Patch notes','패치만')}</option><option value="class">{t('Class changes','클래스 변경')}</option></select></label><label>{t('Class','직업')}<select data-news-class><option value="all">{t('All classes','전체 직업')}</option>{options}</select></label></div><p class="desk-note">{t('A bug fix can restore lost damage without changing a coefficient. Unquantified effects are kept as fixes or adjustments. US and Canada use the North America feed; this is not a separately verified Canadian ruleset.','버그 수정은 계수 변경 없이도 실제 딜을 회복시킬 수 있습니다. 수치가 없는 변경은 버그 수정·조정으로 표시합니다. 미국·캐나다는 북미 공지를 함께 사용합니다.')}</p><div class="patch-feed" data-news-items>{cards}</div><p data-news-empty hidden>{t('No matching reviewed class changes. New unreviewed patches remain available in the full feed.','해당 조건의 검토된 클래스 변경이 없습니다. 미검토 패치는 전체 소식에서 볼 수 있습니다.')}</p><section class="source-health"><h2>{t('Source health','원문 수집 상태')}</h2><div data-source-health>{''.join(f'<p>{E(s["id"])} · {E(s["status"])} · {t("Last successful check","마지막 정상 확인")} {E(s.get("lastSuccessAt") or "—")}</p>' for s in sources)}</div><p>{t('If a source fails, its last successful items remain visible with their original dates. A source check is not an editorial review.','수집이 실패하면 기존 항목과 실제 날짜를 유지합니다. 수집 시각과 요약 검토 시각은 서로 다릅니다.')}</p></section><a class="btn" href="{r}tools/dps/">{t('See class DPS rankings','직업별 DPS 순위 보기')} →</a></section>'''

def home_strip(lang,base):
    k=lang=='ko';t=lambda a,b:b if k else a;r=base+('ko/' if k else '')
    reviewed=[x for s in load('news.json')['sources'] if s['region']=='NA' for x in s['items'] if x['kind']=='patch' and x.get('reviewState')=='reviewed']
    latest=sorted(reviewed,key=lambda x:x['publishedAt'],reverse=True)
    lead=latest[0]['summary'][lang] if latest else t('Latest official notices and reviewed changes.','최신 공식 소식과 검토한 변경 요약.')
    return resources(base)+f'''<section class="home-live" aria-label="{t('Updates and damage tools','업데이트와 DPS 도구')}"><a href="{r}updates/"><span class="section-kicker">PATCH DESK · NA / KR</span><h2>{t('Latest changes','최신 변경사항')} <span>→</span></h2><p>{E(lead)}</p></a><a href="{r}tools/dps/"><span class="section-kicker">CLASS DPS</span><h2>{t('Class DPS rankings','직업별 DPS 순위')} <span>→</span></h2><p>{t('Server-computed results under a common profile, with boss scenarios and skill contributions.','공통 조건으로 서버에서 계산한 순위와 보스별 차이·스킬 기여도를 확인합니다.')}</p></a></section>'''

def screenshots(lang,base,spotlight=None):
    k=lang=='ko';t=lambda a,b:b if k else a;r=base+('ko/' if k else '')
    selected=load('screenshots.json')
    if spotlight: selected=[x for x in selected if x['category']==spotlight]
    figures=''
    for x in selected:
        figures+=f'''<figure class="gameplay-shot"><a href="{E(x['url'])}" target="_blank" rel="noopener" aria-label="{E(t('Open full screenshot: ','전체 스크린샷 보기: ')+x['title'][lang])}"><img src="{E(x['thumbnail'])}" alt="{E(x['alt'][lang])}" loading="lazy" width="1920" height="1080"></a><figcaption><span class="section-kicker">NC / {t('OFFICIAL GAMEPLAY SCREENSHOT','공식 인게임 스크린샷')}</span><h3>{E(x['title'][lang])}</h3><p>{E(x['caption'][lang])}</p><a href="{E(x['source'])}" target="_blank" rel="noopener">AION 2 © NC · Steam ↗</a></figcaption></figure>'''
    copy=t('Publisher-provided in-game frames, with the HUD hidden. These illustrate combat and movement; they are not player-submitted evidence for a build or a particular boss mechanic.','공식 공개 인게임 장면이며 HUD는 숨겨져 있습니다. 전투·이동 맥락을 보여주는 자료로, 특정 빌드나 보스 패턴의 실측 증거는 아닙니다.')
    if spotlight:
        return f'<link rel="stylesheet" href="{base}assets/liveops.css?v=2"><section class="gameplay-context"><h2>{t("See the in-game scene","실제 게임 장면")}</h2><div class="gameplay-grid">{figures}</div><a class="text-link" href="{r}screenshots/">{t("All screenshots & credits","전체 스크린샷·출처 보기")} →</a></section>'
    return resources(base)+f'<section class="screenshot-desk"><div class="desk-intro"><span class="section-kicker">IN-GAME / AION 2</span><h1>{t("Real scenes from Atreia.","아트레이아의 실제 장면.")}</h1><p>{copy}</p></div><div class="gameplay-grid">{figures}</div><p class="desk-note">{t("Images are served by the publisher’s Steam CDN. Community settings captures remain linked to their originals until reuse permission is available.","이미지는 공식 Steam 배포 주소에서 표시합니다. 커뮤니티의 설정 캡처는 재사용 허락이 확인되기 전까지 원본 링크를 유지합니다.")}</p></section>'

def coverage(lang):
    t=lambda a,b:b if lang=='ko' else a
    data=load('coverage-audit.json');cards=''
    for item in data['items']:
        links=' · '.join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["title"])} ↗</a>' for s in item['sources'])
        status=t('Evidence needed','자료 보강 필요') if item['status']=='needs-evidence' else t('Tracking in place','추적 중')
        cards+=f'<article class="patch-card"><span class="tag">{E(item["region"])} · {status}</span><h3>{E(item["title"][lang])}</h3><p>{E(item["finding"][lang])}</p><footer>{links}</footer></article>'
    return f'<section class="coverage-desk"><h2>{t("What our guides still need","공략 보강 목록")}</h2><p class="desk-note">{t("Community review","커뮤니티 검토")}: {E(data["reviewedAt"])} · {t("Daily source review checks for new evidence; this date changes only after a completed editorial audit.","매일 새 자료를 확인하며, 이 날짜는 실제 공략 검토를 마친 경우에만 바뀝니다.")}</p><div class="patch-feed">{cards}</div></section>'

def dps(lang,base):
    return dpsranking.render(lang,base)

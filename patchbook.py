"""Readable, source-bound full patch pages and compact patch-list cards."""
import html
import json
import re
from pathlib import Path
from content import CLASSES

E=lambda value:html.escape(str(value),quote=True)
CLASS_INFO={c['id']:c for c in CLASSES}
CLASS_INFO.update({
    'all':dict(id='all',ko='공통',en='All classes',icon='swords',color='#b3bdd2'),
    'brawler':dict(id='brawler',ko='권성',en='Brawler · KR',icon='swords',color='#edb581'),
})
LABELS={'buff':('Buff','버프'),'nerf':('Nerf','너프'),
        'adjustment':('Adjustment','조정'),'fix':('Bug fix','버그 수정'),
        'tooltip':('Tooltip','툴팁 수정'),'system':('Other change','기타 변경')}
MARKS={'buff':'↑','nerf':'↓','adjustment':'↔','fix':'✓','tooltip':'i','system':'•'}

def label(kind,lang):return LABELS.get(kind,LABELS['system'])[lang=='ko']
def badge(kind,lang):
    kind=kind if kind in LABELS else 'system'
    return f'<span class="change-badge {kind}"><span aria-hidden="true">{MARKS[kind]}</span> {label(kind,lang)}</span>'
def classification(changes):
    types={c.get('type') for c in changes}
    if 'adjustment' in types or {'buff','nerf'} <= types:return 'adjustment'
    return next((kind for kind in ('buff','nerf','fix','tooltip') if kind in types),'system')
def class_groups(item):
    groups={}
    for row in item.get('changes',[]):
        cls=row.get('classId')
        if cls in CLASS_INFO:groups.setdefault(cls,[]).append(row)
    return [dict(classId=cls,info=CLASS_INFO[cls],rows=groups[cls],type=classification(groups[cls]))
            for cls in CLASS_INFO if cls in groups]
def detail_path(item):
    if item.get('region') not in ('NA','KR') or not re.fullmatch(r'[a-zA-Z0-9_-]{1,64}',item['id']):
        raise ValueError('Invalid patch identity')
    return 'updates/'+item['region'].lower()+'-'+item['id']+'/'
def patches(feed):
    return sorted((x for s in feed['sources'] for x in s['items'] if x['kind']=='patch'),
                  key=lambda x:x.get('publishedAt') or '',reverse=True)
def title(item,lang):return item.get('displayTitle',{}).get(lang) or item['title']
def detail_ready(item):return item.get('reviewState')=='reviewed' and item.get('detail',{}).get('coverage')=='complete'
def region_name(item,lang):
    return ('북미 · 미국 / 캐나다' if lang=='ko' else 'NA · US / Canada') if item['region']=='NA' else ('한국' if lang=='ko' else 'Korea')
def review_label(item,lang):
    t=lambda en,ko:ko if lang=='ko' else en
    if detail_ready(item):return t('Full change list reviewed','전체 항목 검토 완료')
    if item.get('reviewState')=='revised':return t('Source revised · reviewing','원문 수정 · 재검토 중')
    if item.get('reviewState')=='reviewed':return t('Summary reviewed','요약 검토 완료')
    return t('Review pending','검토 중')
def config():
    values={cid:{key:c[key] for key in ('id','en','ko','icon','color')} for cid,c in CLASS_INFO.items()}
    return '<script type="application/json" id="pc-patch-classes">'+json.dumps(values,ensure_ascii=False).replace('<','\\u003c')+'</script>'
def portrait(cls,base,lang,compact=False):
    if cls not in {c['id'] for c in CLASSES}:
        return f'<svg class="patch-emblem" aria-hidden="true" viewBox="0 0 48 48"><use href="{base}assets/icons.svg#{CLASS_INFO[cls]["icon"]}"/></svg>'
    return f'<img class="{"patch-chip-image" if compact else "patch-portrait"}" src="{base}assets/classes/{cls}.webp" alt="{E(CLASS_INFO[cls][lang]) if not compact else ""}" width="460" height="920" loading="lazy">'
def patch_card(item,lang,base):
    k=lang=='ko';t=lambda en,ko:ko if k else en;r=base+('ko/' if k else '')
    is_patch=item['kind']=='patch'
    url=r+detail_path(item) if is_patch else item['url']
    groups=class_groups(item)
    chips=''.join(f'<a class="patch-impact-chip" href="{url}#class-{g["classId"]}">{portrait(g["classId"],base,lang,True)}<strong>{E(g["info"][lang])}</strong>{badge(g["type"],lang)}</a>' for g in groups)
    summary=item.get('summary',{}).get(lang) or t('The new notice is awaiting an editorial review.','새 공지를 수집했습니다. 변경 내용을 검토하고 있습니다.')
    if is_patch:
        link=f'<a class="patch-title-link" href="{url}">{E(title(item,lang))}</a>'
        action=f'<a class="text-link patch-read-link" href="{url}">{t("Read full change list","전체 패치 보기")} <span aria-hidden="true">→</span></a>'
    else:
        link=f'<a href="{E(url)}" target="_blank" rel="noopener">{E(item["title"])}</a>'
        action=f'<a class="text-link" href="{E(url)}" target="_blank" rel="noopener">{t("Read official notice","공식 공지 보기")} ↗</a>'
    return f'''<article class="patch-card patch-summary" data-region="{item['region']}" data-kind="{item['kind']}" data-class-ids="{' '.join(g['classId'] for g in groups)}" data-review="{E(item.get('reviewState','pending'))}"><header><span class="tag">{region_name(item,lang)}</span><time datetime="{E(item.get('publishedAt') or '')}">{E((item.get('publishedAt') or '')[:10])}</time><span class="review-badge">{review_label(item,lang)}</span></header><h2>{link}</h2><p class="patch-summary-copy">{E(summary)}</p>{f'<div class="patch-impact-chips">{chips}</div>' if chips else ''}<footer>{action}<a class="patch-source-link" href="{E(item['url'])}" target="_blank" rel="noopener">{t('NC source','NC 원문')} ↗</a></footer></article>'''

def table_html(table,lang,index):
    t=lambda en,ko:ko if lang=='ko' else en
    headings=''.join(f'<th scope="col">{E(x)}</th>' for x in table['headers'])
    rows=''.join('<tr>'+f'<th scope="row">{E(row[0])}</th>'+''.join(f'<td>{E(x)}</td>' for x in row[1:])+'</tr>' for row in table['rows'])
    return f'<div class="patch-fact-table" tabindex="0" role="region" aria-label="{t("Detailed values","상세 수치 표")} {index}"><table><caption>{t("Published values · KR item names retained","공지 기준 상세 수치")}</caption><thead><tr>{headings}</tr></thead><tbody>{rows}</tbody></table></div>'

def render_detail(item,lang,base):
    k=lang=='ko';t=lambda en,ko:ko if k else en;r=base+('ko/' if k else '')
    detail=item.get('detail',{}) if detail_ready(item) else {}
    groups=class_groups(item);section_rows=detail.get('sections',[])
    intro=f'''<nav class="patch-breadcrumb" aria-label="{t('Breadcrumb','경로')}"><a href="{r}updates/?region={item['region']}&amp;kind=patch">← {t('All patches','패치 목록')}</a><span>{region_name(item,lang)}</span></nav><header class="patch-detail-head"><span class="section-kicker">PATCH NOTES / {item['region']}</span><h1>{E(title(item,lang))}</h1><p>{E(item.get('summary',{}).get(lang) or t('The source notice is available below.','공식 공지에서 변경사항을 확인할 수 있습니다.'))}</p><div class="patch-detail-meta"><time datetime="{E(item.get('publishedAt') or '')}">{E((item.get('publishedAt') or '')[:10])} UTC</time><span class="review-badge">{review_label(item,lang)}</span><span>{t('Source updated','원문 수정')}: {E((item.get('sourceUpdatedAt') or '')[:16].replace('T',' '))} UTC</span></div><a class="text-link" href="{E(item['url'])}" target="_blank" rel="noopener">NC · {t('Official source','공식 원문')} ↗</a></header>'''
    if not detail:
        state=t('The source has changed or its full list is still under review. Use the official notice for the complete current patch.','원문이 바뀌었거나 전체 항목을 검토하고 있습니다. 현재 전체 내용은 위 공식 원문에서 확인할 수 있습니다.')
        return f'<section class="patch-detail">{intro}<p class="patch-review-notice">{state}</p></section>'
    toc=f'<a href="#class-changes">{t("Class changes","직업 변경")}</a>'+''.join(f'<a href="#patch-section-{i}">{E(s["title"][lang])}</a>' for i,s in enumerate(section_rows))
    jumps=''.join(f'<a class="patch-class-jump" href="#class-{g["classId"]}">{portrait(g["classId"],base,lang,True)}<span>{E(g["info"][lang])}</span>{badge(g["type"],lang)}</a>' for g in groups)
    cards=''
    skills=json.loads((Path(__file__).parent/'data/skills.json').read_text())
    for g in groups:
        cid=g['classId'];content=''
        counts={kind:sum(c['type']==kind for c in g['rows']) for kind in LABELS}
        count_text=' · '.join(f'{label(kind,lang)} {n}' for kind,n in counts.items() if n)
        for row in g['rows']:
            names=row['subject']['ko'].split(' · ')
            skill=next((s for s in skills if s['ko'] in names and s['cls']==cid),None)
            name=E(row['subject'][lang])
            if skill:
                name=f'<a href="{r}skills/{E(skill["id"])}/"><img src="{E(skill["icon"])}" alt="" width="34" height="34" loading="lazy">{name}</a>'
            difference=''
            if row.get('before') and row.get('after'):
                difference=f'<div class="patch-before-after"><span><small>{t("Before","변경 전")}</small>{E(row["before"][lang])}</span><b aria-hidden="true">→</b><span><small>{t("After","변경 후")}</small>{E(row["after"][lang])}</span></div>'
            content+=f'<li class="patch-skill-change">{badge(row["type"],lang)}<div><h3>{name}</h3><p>{E(row["description"][lang])}</p>{difference}</div></li>'
        extra_tables=''.join(table_html(table,lang,i+1) for i,table in enumerate(detail.get('classTables',[]))) if cid=='ranger' else ''
        guide=f'<a class="text-link" href="{r}classes/{cid}/">{t("Class guide","직업 공략")} →</a>' if cid in {c['id'] for c in CLASSES} else ''
        cards+=f'<article class="patch-class-card" id="class-{cid}" style="--class-color:{g["info"]["color"]}"><header>{portrait(cid,base,lang)}<div><span class="section-kicker">{t("CLASS CHANGES","직업 변경")}</span><h2>{E(g["info"][lang])} {badge(g["type"],lang)}</h2><p>{count_text}</p>{guide}</div></header><ul class="patch-skill-list">{content}</ul>{extra_tables}</article>'
    no_class=t('This patch contains no class-specific changes. Read the system and fix sections below.','이 패치에는 직업별 변경이 없습니다. 아래 시스템·오류 수정 항목을 확인하세요.')
    classes=f'<section id="class-changes" class="patch-class-changes"><h2>{t("At a glance · class impact","한눈에 보는 직업 변경")}</h2>{f"<div class=patch-class-jumps>{jumps}</div>" if jumps else f"<p class=patch-no-class>{no_class}</p>"}{cards}</section>'
    sections=''
    for i,s in enumerate(section_rows):
        notes=''.join(f'<li>{E(n[lang])}</li>' for n in s['notes'])
        tables=''.join(table_html(tab,lang,j+1) for j,tab in enumerate(s['tables']))
        sections+=f'<section class="patch-full-section" id="patch-section-{i}"><h2><span class="patch-section-number" aria-hidden="true">{i+1:02}</span>{E(s["title"][lang])}</h2><ul class="patch-fact-list">{notes}</ul>{tables}</section>'
    scope=t('This page reorganizes all reviewed change topics and numeric tables in our own words. Class labels describe the announced changes, not a measured total DPS result. ↑ buff + ↓ nerf within one class = ↔ adjustment.','공식 공지의 전체 변경 주제와 수치 표를 읽기 쉽게 다시 정리했습니다. 직업 표시는 공지된 변경의 분류이며 전체 DPS 실측 결과를 뜻하지 않습니다. 한 직업이 버프와 너프를 함께 받으면 ‘조정’으로 표시합니다.')
    media=t('Class artwork © NC · official AION 2 teaser. Korea-only class terms and tables are not applied to North America.','직업 이미지 © NC · 공식 AION 2 소개 자료. 한국판 전용 직업·수치·일정은 북미판에 적용하지 않습니다.')
    return f'''<section class="patch-detail" data-news-detail data-lang="{lang}" data-item-id="{E(item['id'])}" data-content-hash="{E(item['contentHash'])}" data-feed="{base}data/news.json">{intro}<p class="patch-review-notice" data-detail-revision role="status" hidden></p><div data-detail-content><p class="patch-reading-note">{scope}</p><details class="patch-toc"><summary>{t('Jump to a topic','항목 바로가기')} · {len(section_rows)+1}</summary><nav aria-label="{t('Patch contents','패치 목차')}">{toc}</nav></details>{classes}<section id="full-changes" class="patch-full-changes"><div class="patch-full-heading"><span class="section-kicker">FULL CHANGE LIST</span><h2>{t('Everything else in this patch','콘텐츠부터 오류 수정까지')}</h2></div>{sections}</section><p class="patch-media-credit">{media} <a href="https://aion2.ncsoft.jp/en/teaser" target="_blank" rel="noopener">NC ↗</a></p></div><div class="patch-bottom-nav"><a class="btn" href="{r}updates/?region={item['region']}&amp;kind=patch">← {t('Back to patch list','패치 목록으로')}</a><a class="text-link" href="{r}tools/dps/">{t('Compare the damage impact','DPS 변화 비교하기')} →</a></div></section>'''

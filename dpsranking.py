"""Publish reviewed combat summaries; incomplete formula models cannot rank classes."""
import html
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).parent
E = lambda value: html.escape(str(value), quote=True)

def formatted(value, digits=2):
    rounded = Decimal(str(value)).quantize(Decimal(1).scaleb(-digits), rounding=ROUND_HALF_UP)
    return f'{rounded:,.{digits}f}'

def load():
    data = json.loads((ROOT / 'data/dps-rankings.json').read_text())
    if data['kind'] != 'server-published-observed-dps-comparison' or data['schema'] != 2:
        raise ValueError('Only reviewed combat observations can be published')
    if data['scope']['canDescribeAsEndgameTier'] or data['scope']['usesTooltipSimulation']:
        raise ValueError('Incomplete simulations cannot become a class ranking')
    if not data['methodology']['noUserInputs'] or any(len(d['rows']) != 8 for d in data['comparisons']):
        raise ValueError('Incomplete public comparison')
    return data

def needs_patch_review(news, reviewed_at, region='NA'):
    patches = [p for source in news['sources'] if source.get('region') == region
               for p in source['items'] if p.get('kind') == 'patch']
    return any((p.get('sourceUpdatedAt') or p.get('publishedAt') or '')[:10] > reviewed_at for p in patches)

def render(lang, base):
    k = lang == 'ko'
    t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')
    data = load()
    datasets = {d['id']: d for d in data['comparisons']}
    roles = {'damage': t('Damage', '딜러'), 'healer': t('Healer', '힐러'),
             'tank': t('Tank', '탱커'), 'support': t('Support', '지원')}

    def table(dataset):
        record = dataset['kind'] == 'record'
        report = dataset['kind'] in ('weekly', 'band')
        dps = record or dataset['kind'] == 'band'
        rows = ''
        for row in dataset['rows']:
            if dps:
                score = E(row['publishedDps']) if record else (E(row['publishedDps']) + '/s' if k else formatted(row['value'], 0) + '/s')
            else:
                score = formatted(row['value'], 2 if report else 0) if row['value'] is not None else '—'
            position = row['rank'] if row['rank'] is not None else '—'
            samples = (str(row['sampleCount']) if report else str(row['publishedRecords']) if record else
                       f"{row['characterWeeks']:,} / {row['uploaders'] if row['uploaders'] is not None else '<5'} / {row['bosses']}")
            extra = '' if record or report else f'<td>{row["topEnd"] if row["topEnd"] is not None else "—"}</td>'
            value = '' if row['value'] is None else str(row['value'])
            metric_label = t('Recorded DPS','게시 DPS') if record else t('Median DPS','중앙값 DPS') if dps else t('Adjusted index','보정 지수') if report else t('Median index','중앙값 지수')
            rows += f'''<tr data-rank-class="{E(row['classId'])}" data-value="{E(value)}" data-place="{row['rank'] or ''}"><td class="rank-place">{position}</td><th scope="row"><a href="{r}classes/{E(row['classId'])}/"><span class="rank-class-dot" style="background:{row['color']}"></span>{E(row[lang])}</a><small>{roles[row['role']]}</small></th><td class="rank-value"><strong>{score}</strong><small>{metric_label}</small></td>{extra}<td class="rank-sample">{E(samples)}</td></tr>'''
        headers = [t('Record order', '기록 순서') if record else t('Index order', '지수 순서'), t('Class', '직업'),
                   t('Best published DPS', '공개 최고 DPS') if record else t('Median DPS', '중앙값 DPS') if dps else t('Adjusted index', '보정 지수') if report else t('Median index', '중앙값 지수')]
        if not record and not report: headers.append(t('P95 index', '상위 5% 지수'))
        headers.append(t('Records', '기록 수') if report else t('Published records', '게시 기록 수') if record else t('Char-weeks / uploaders / bosses', '캐릭터·주 / 업로더 / 보스'))
        caption = dataset.get(lang) or t('Class DPS index', '직업별 DPS 지수')
        return f'''<div class="rank-table-scroll" tabindex="0" role="region" aria-label="{E(caption)}"><table class="rank-table" data-comparison-table="{E(dataset['id'])}"><caption class="sr-only">{E(caption)}</caption><thead><tr>{''.join('<th scope="col">'+h+'</th>' for h in headers)}</tr></thead><tbody>{rows}</tbody></table></div>'''

    current = datasets['jameter-current']
    completed = datasets['jameter-complete']
    provisional = t('In progress · snapshot, not a final week', '집계 중 · 확인 시점의 표본') if current['provisional'] else t('Completed week', '완료된 주간')
    weekly = f'''<section class="rank-weekly" id="weekly-comparison"><div class="rank-section-head"><h2>{t('Weekly: boss and Combat-Power adjusted DPS','주간: 보스·전투력 보정 DPS')}</h2><a href="{base}data/dps-rankings.csv" download>CSV ↓</a></div><p class="rank-summary">JaMeter · {E(current['periodStart'])} ~ {E(current['periodEnd'])} · {provisional}.</p><p class="rank-detail-note">{t('The publisher compares DPS per point of Combat Power on the same boss, against that week’s median of 1.00. We sort the published indices on the server. This linear adjustment leaves party, gear and skill differences; it is not identical-build DPS or nDPS with buffs removed.','출처가 같은 보스의 전투력 1당 DPS를 그 주 중앙값 1.00에 비교한 지수입니다. 서버에서 공개값을 정렬합니다. 선형 전투력 보정 뒤에도 파티·장비·숙련도 차이가 남으며, 동일 빌드 DPS나 외부 버프를 뺀 nDPS는 아닙니다.')}</p>{table(current)}<p class="rank-detail-note"><a href="{E(current['source'])}" target="_blank" rel="noopener">JaMeter · {t('Weekly report','주간 원문')} ↗</a> · {t('Region is not specified in this report; no Korea-only population is inferred.','이 보고서에는 서버 지역이 명시되지 않아 한국 전용 모집단으로 추정하지 않습니다.')} {t('Collected','확인')} {E(data['collectedAt'])}.</p><details class="rank-scenario" data-matched-week><summary>{t('Completed week: DPS within one Combat-Power band','완료된 주간: 같은 전투력 구간의 DPS')}<span>{E(completed['periodStart'])} ~ {E(completed['periodEnd'])} · {E(completed['commonBand'])}</span></summary><p>{t('Published medians for the same CP band; each class has at least 20 records. Boss and party mixes still differ. This is a previous week and is not substituted for the current patch.','같은 전투력 구간의 공개 DPS 중앙값이며 직업당 20건 이상 기록입니다. 보스와 파티 구성은 여전히 다릅니다. 이전 주간 결과이므로 현재 패치의 값으로 대체하지 않습니다.')}</p>{table(completed)}<p class="rank-detail-note"><a href="{E(completed['source'])}" target="_blank" rel="noopener">JaMeter · {t('Completed report','완료된 주간 원문')} ↗</a> · {t('Published precision retained. The report does not specify a server region.','출처의 표시 정밀도를 유지합니다. 보고서에는 서버 지역이 명시되지 않았습니다.')}</p></details></section>'''

    records = ''
    for index, ident in enumerate(('turgen', 'griosa', 'basilus')):
        d = datasets[ident]
        records += f'''<details class="rank-scenario" id="rank-{ident}" data-rank-scenario="{ident}"{' open' if index == 0 else ''}><summary>{E(d[lang])}<span>{t('KR · Hard · all time','한국 · 어려움 · 전체 기간')}</span></summary><p>{t('One highest published record per class on this boss. Gear, fight dates, party buffs and duration are not controlled; this orders records, not class potential. Published counts can be small.','이 보스에서 직업별 공개 최고 기록 하나를 비교합니다. 장비·전투 날짜·파티 버프·전투 길이는 통일되지 않았으므로 직업 성능의 최종 순위로 읽으면 안 됩니다. 게시 기록이 적은 직업도 있습니다.')}</p>{table(d)}<p class="rank-detail-note"><a href="{E(d['source'])}" target="_blank" rel="noopener">AionFlex · {t('Same-boss KR records','같은 보스의 한국 기록')} ↗</a> · {t('Original rounded notation is retained. No missing decimals are estimated.','출처의 반올림 표기를 유지하며 미공개 소수점은 추정하지 않습니다.')}</p></details>'''
    korean = f'''<section class="rank-scenarios" id="kr-records"><div class="rank-section-head"><h2>{t('Korea: boss DPS records','한국: 보스별 DPS 기록')}</h2><a href="{base}data/dps-rankings.csv" download>{t('Download comparisons','비교 결과 내려받기')} · CSV ↓</a></div><p class="rank-summary">{t('Citadel of the Fallen Daeva · Hard. Compare damage on the same boss; never combine best runs from different bosses into one overall DPS.','타락한 데바의 성 · 어려움. 같은 보스 안에서 피해 기록을 비교하며, 서로 다른 보스의 최고 기록을 합쳐 종합 DPS를 만들지 않습니다.')}</p>{records}</section>'''

    global_data = datasets['global-balance']
    enough = global_data['status'] == 'observed'
    global_status = t('Compared over Under 300K Combat Power.', '비교 구간: 전투력 30만 미만.') if enough else t('Insufficient matched samples. No index order is assigned.', '같은 전투력 구간의 표본이 부족해 지수 순서를 매기지 않습니다.')
    global_section = f'''<section class="rank-overall" id="global-comparison"><h2>{t('Global: comparable DPS indices','글로벌: 같은 전투력의 DPS 지수')}</h2><p class="rank-summary">{global_status} {t('Last 30 days · source coverage','최근 30일 · 출처 집계 기준')} {E(global_data['sourceAsOf'])}.</p><p class="rank-detail-note">{t('100 is the source uploader field on the same boss and Combat Power. Median and P95 are separate published indices, not damage per second. We order the median indices on the backend. Party gear and buffs are not held constant.','100은 같은 보스·전투력 구간의 출처 업로더 집단 기준입니다. 중앙값과 상위 5%는 각각의 공개 지수이며 초당 피해량이 아닙니다. 서버에서 중앙값 지수를 정렬합니다. 파티 장비와 버프까지 통일한 비교는 아닙니다.')}</p>{table(global_data)}<p class="rank-detail-note">{t('Healers: damage dealt while healing, on parties of at least four. Sorcerer/Spiritmaster: summons without an owner stamp can be missing. These indices describe this uploader sample.','치유성·호법성은 4인 이상 파티에서 회복을 병행한 개인 피해입니다. 마도성·정령성은 소유자 표시가 없는 소환 피해가 누락될 수 있습니다. 이 지수는 출처 업로더 표본을 설명합니다.')} <a href="{E(global_data['source'])}" target="_blank" rel="noopener">AionFlex · {t('Comparison and samples','비교 조건과 표본')} ↗</a></p></section>'''

    kr_data = datasets['kr-balance']
    if kr_data['status'] == 'insufficient':
        reason = t('AionFlex cannot form a shared Combat-Power comparison with sufficient samples in this KR cut. No index order is assigned, and the Global index is never substituted for it.', 'AionFlex의 한국 표본에는 전 직업이 공유하는 충분한 전투력 구간이 없어 지수 순서를 매기지 않습니다. 글로벌 지수를 한국 순위로 대체하지 않습니다.')
    else:
        reason = t('Matched samples are available. These are published median indices, separate from the boss records above.', '비교 가능한 표본의 공개 중앙값 지수입니다. 위 보스 최고 기록과 별도로 읽어주세요.')
    kr_coverage = f'''<details class="rank-method" data-kr-coverage><summary>{t('Korea-wide comparison: sample coverage','한국 전체 비교: 표본 현황')}</summary><p>{reason}</p><p>{t('Last 30 days · source coverage','최근 30일 · 출처 집계 기준')} {E(kr_data['sourceAsOf'])}.</p>{table(kr_data)}<p><a href="{E(kr_data['source'])}" target="_blank" rel="noopener">AionFlex · {t('Korea sample coverage','한국 표본 현황')} ↗</a></p></details>'''

    news = json.loads((ROOT / 'data/news.json').read_text())
    newer = [name for region, name in [('KR', t('Korea', '한국')), ('NA', t('North America', '북미'))]
             if needs_patch_review(news, data['sourceReviewedAt'], region)]
    patch_note = f'<p class="rank-patch-note">{E(" · ".join(newer))}: {t("A newer patch needs source review; historical records below do not become current-patch predictions.","새 패치 이후 출처 재검토가 필요합니다. 아래 과거 기록은 현재 패치의 예상 DPS로 바뀌지 않습니다.")} <a href="{r}updates/">{t("Patch notes","패치 확인")} →</a></p>' if newer else ''
    sections = weekly + korean + kr_coverage + global_section if k else global_section + weekly + korean + kr_coverage
    return f'''<link rel="stylesheet" href="{base}assets/dps-rankings.css?v=observed-2"><section class="rank-desk" data-dps-rankings data-computed-by="backend" data-source-reviewed="{E(data['sourceReviewedAt'])}"><header class="rank-intro"><span class="section-kicker">DPS / COMBAT RECORDS</span><h1>{t('Compare actual DPS records','실전 DPS 비교')}</h1><p>{t('See boss damage records and comparable class indices from published combat data.','공개된 전투 기록으로 보스별 피해와 같은 전투력 구간의 직업별 지수를 확인하세요.')}</p><div class="rank-tags"><span>AionFlex / JaMeter · {t('Public combat summaries','공개 실전 요약')}</span><span>{t('Reviewed','검토')} {E(data['sourceReviewedAt'])}</span><span>{t('Eight launch classes','출시 8개 직업')}</span></div><nav class="rank-links" aria-label="{t('Comparison scope','비교 범위')}"><a href="#weekly-comparison">{t('Weekly comparisons','주간 비교')}</a><a href="#kr-records">{t('Korea boss records','한국 보스 기록')}</a><a href="#global-comparison">{t('Global matched indices','글로벌 전투력 비교')}</a></nav></header><aside class="rank-scope"><strong>{t('Damage records, with their comparison conditions','피해 기록과 비교 조건을 함께 보세요')}</strong><p>{t('Korea boss records and Global matched indices describe different samples. Healing and the damage teammates gain from buffs are not personal DPS. Published summaries are reviewed and ordered by our backend; raw fight damage/times are unavailable here, so DPS is not recomputed from invented skill timings.','한국 보스 최고 기록과 글로벌 전투력 지수는 서로 다른 표본입니다. 회복량과 버프로 늘어난 파티원 피해는 개인 DPS에 합치지 않습니다. 공개 요약을 검토해 서버에서 정렬하며, 원본 전투 피해·시간이 없어 임의의 스킬 시간으로 DPS를 재계산하지 않습니다.')}</p></aside>{patch_note}{sections}<details class="rank-method"><summary>{t('Method and sources','비교 방법과 출처')}</summary><ul><li>{t('Weekly summaries retain the publisher’s period and Combat-Power method. Korea tables sort the highest public class record within one boss. Global indices sort the published median index, with the original sample floor. Equal public values share a place.','주간 표는 출처의 기간과 전투력 보정법을 유지합니다. 한국 표는 같은 보스의 직업별 공개 최고 기록을 정렬합니다. 글로벌 표는 출처의 표본 기준을 적용해 공개 중앙값 지수를 정렬합니다. 공개값이 같으면 공동 순서입니다.')}</li><li>{t('A normalized index needs all eight classes, a shared Combat-Power band and at least 100 character-weeks, 10 uploaders and 3 qualifying bosses per class. Insufficient samples receive no rank or zero-DPS replacement.','정규화 지수는 8개 직업·공통 전투력 구간과 직업당 캐릭터·주 100개, 업로더 10명, 유효 보스 3개 이상의 표본을 요구합니다. 표본이 부족하면 순서나 DPS 0을 대신 넣지 않습니다.')}</li><li>{t('Records include historical patches and different gear. They do not measure a legal shared final build or establish a current-patch class tier. No healer penalty or class-role weight is applied.','기록에는 과거 패치와 서로 다른 장비가 포함됩니다. 동일 최종빌드나 현재 패치의 직업 티어를 입증하지 않습니다. 힐러 감점이나 역할별 보정값은 넣지 않습니다.')}</li><li>{t('The former level-20, one-second-action formula table was withdrawn: unequal passive, pet and charge coverage made its cross-class ordering unreliable. The formula engine remains offline research.','이전의 공통 20레벨·동작 1초 공식 순위는 패시브·정령·차징 피해 반영 범위가 달라 철회했습니다. 공식 엔진은 오프라인 연구로 유지합니다.')}</li></ul><p><a href="https://aionflex.gg/hall-of-champions" target="_blank" rel="noopener">AionFlex · Hall of Champions ↗</a> · <a href="https://jameter.net/metrics" target="_blank" rel="noopener">JaMeter · {t("Metric definitions","측정 방식")} ↗</a> · <a href="{E(data['methodology']['normalizedIndexSource'])}" target="_blank" rel="noopener">{t('Source methodology','출처의 집계 방법')} ↗</a> · <a href="https://aion.ing/aion2/stats.php" target="_blank" rel="noopener">{t('AIONING: compare other records','아이온잉: 다른 기록 확인')} ↗</a></p><p><a href="{base}data/dps-rankings.json">{t('Reviewed results','검토 결과')} · JSON</a> · {t('Collected','자료 확인')} {E(data['collectedAt'])}. {t('Published counts are source summaries, not a count of independently verified raw logs.','게시 수·표본 수는 출처의 요약이며 우리가 원본 로그를 독립 검증한 수가 아닙니다.')}</p></details></section>'''

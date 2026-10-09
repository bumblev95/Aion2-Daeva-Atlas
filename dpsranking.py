"""Render authoritative backend results as bilingual, read-only HTML."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
E = lambda value: html.escape(str(value), quote=True)

def load():
    data = json.loads((ROOT / 'data/dps-rankings.json').read_text())
    if data['kind'] != 'server-computed-dps-ranking' or len(data['overall']) != 8:
        raise ValueError('Backend ranking snapshot is incomplete')
    if data['scope']['canDescribeAsEndgameTier'] or not data['methodology']['noUserInputs']:
        raise ValueError('Ranking scope changed; review the public description')
    return data

def needs_patch_review(news, reviewed_at):
    patches = [p for source in news['sources'] if source.get('region') == 'NA'
               for p in source['items'] if p.get('kind') == 'patch']
    return any((p.get('sourceUpdatedAt') or p.get('publishedAt') or '')[:10] > reviewed_at for p in patches)

def render(lang, base):
    k = lang == 'ko'
    t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')
    data = load()
    classes = {c['classId']: c for c in data['classes']}
    fmt = lambda value: f'{value:,.2f}'
    number = lambda value: f'{value:,g}'

    def table(rows, caption):
        body = ''
        for row in rows:
            c = classes[row['classId']]
            color = row['color'] if re.fullmatch(r'#[0-9a-fA-F]{6}', row['color']) else '#91d9c4'
            missing = len(c['damageCoverage']['unresolved'])
            body += f'''<tr data-rank-class="{E(row['classId'])}" data-dps="{row['dps']:.12g}"><td class="rank-place">{row['rank']}</td><th scope="row"><a href="#class-{E(row['classId'])}"><span class="rank-class-dot" style="background:{color}"></span>{E(row[lang])}</a><small>{t('Known formulas','확인된 공식')} {c['damageCoverage']['modeled']} / 12</small></th><td class="rank-value"><strong>{fmt(row['dps'])}</strong><small>DPS</small></td><td class="rank-relative"><span>{row['leaderPercent']:.1f}%</span><div class="rank-meter" aria-hidden="true"><i style="width:{row['leaderPercent']:.6f}%"></i></div></td><td class="rank-missing">{t('Unresolved','미확인 피해')} <b>{missing}</b></td></tr>'''
        headings = [t('Rank', '순위'), t('Class', '직업'), 'DPS', t('vs. leader', '1위 대비'), t('Coverage', '반영 범위')]
        return f'''<div class="rank-table-scroll" tabindex="0" role="region" aria-label="{E(caption)}"><table class="rank-table"><caption class="sr-only">{E(caption)}</caption><thead><tr>{''.join('<th scope="col">'+h+'</th>' for h in headings)}</tr></thead><tbody>{body}</tbody></table></div>'''

    scenarios = ''
    for scenario in data['scenarios']:
        windows = E(scenario['downtime'].replace(',', ' · ')) or t('None', '없음')
        scenarios += f'''<details class="rank-scenario" id="rank-{E(scenario['id'])}" data-rank-scenario="{E(scenario['id'])}"><summary>{E(scenario[lang])}<span>{number(scenario['duration'])}{t(' s','초')} · {t('No-damage time','공격 불가')} {number(scenario['unavailableSeconds'])}{t(' s','초')}</span></summary><p>{t('All classes face a control-immune NPC boss. No-damage windows','전 직업에 상태이상 면역 NPC 보스를 적용합니다. 공격 불가 구간')}: {windows}. {t('Movement and invulnerability remain in the DPS denominator.','이동·무적 시간도 DPS 분모에 포함합니다.')}</p>{table(scenario['rows'], scenario[lang])}</details>'''

    details = ''
    for overall in data['overall']:
        c = classes[overall['classId']]
        skills = {}
        warnings = set()
        for fight in c['test']:
            warnings.update(fight['warnings'])
            for s in fight['skills']:
                if s['id'] not in skills:
                    skills[s['id']] = dict(id=s['id'], en=s['en'], ko=s['ko'], casts=0, damage=0, ticks=0, blocked=set())
                row = skills[s['id']]
                row['casts'] += s['casts']; row['damage'] += s['damage']; row['ticks'] += s['ticks']
                row['blocked'].update(s['blocked'])
        skill_rows = ''
        for s in sorted(skills.values(), key=lambda s: (-s['damage'], s['id'])):
            share = s['damage'] / c['totalDamage'] * 100 if c['totalDamage'] else 0
            blocked = t('Unavailable under these conditions', '이 조건에서 사용 불가') if s['casts'] == 0 and s['blocked'] else ''
            skill_rows += f'''<tr><th scope="row"><a href="{r}skills/{E(s['id'])}/">{E(s[lang])}</a>{'<small>'+blocked+'</small>' if blocked else ''}</th><td>{s['casts']}</td><td>{s['ticks']}</td><td>{fmt(s['damage'])}</td><td>{share:.1f}%</td></tr>'''
        unresolved = c['damageCoverage']['unresolved']
        missing = ', '.join(f'<a href="{E(s["source"])}" target="_blank" rel="noopener">{E(s[lang])} ↗</a>' for s in unresolved) or t('No unresolved charge, summon or trap entries.', '미확인 차징·소환·덫 항목 없음.')
        order = ' → '.join(E(skills[sid][lang]) for sid in c['policy']['order'])
        assumption_note = t('Unmeasured actions, passive/specification bonuses, resource sustainability and random follow-up triggers are excluded or assumed for every class.', '전 직업에 미측정 동작 시간·패시브/특화 보너스·자원 지속 가능성·확률 발동 연계의 미반영 또는 가정이 남아 있습니다.')
        if 'dot-lifetime-assumption' in warnings:
            assumption_note += ' ' + t('Chain of Torment supplies its prerequisite only after our modeled hit, for the declared 10-second DoT duration.', '고통의 연쇄가 모델에서 적중한 뒤에만 지속 피해의 10초 동안 선행 상태를 제공한다고 가정합니다.')
        details += f'''<details class="rank-class-detail" id="class-{E(c['classId'])}" data-class-detail="{E(c['classId'])}"><summary>{E(c[lang])}<span>{fmt(c['dps'])} DPS</span></summary><div class="rank-components"><p>{t('Direct damage','직접 피해')}<strong>{fmt(c['directDamage'])}</strong></p><p>{t('Periodic damage','지속 피해')}<strong>{fmt(c['periodicDamage'])}</strong></p><p>{t('Total fight time','총 전투 시간')}<strong>{number(c['seconds'])}{t(' s','초')}</strong></p></div><p class="rank-detail-note"><b>{t('Unresolved damage','미확인 피해')}</b>: {missing}</p><p class="rank-detail-note">{assumption_note}</p><div class="rank-table-scroll" tabindex="0" role="region" aria-label="{E(c[lang])} {t('skill contributions','스킬 기여도')}"><table class="rank-breakdown"><thead><tr>{''.join('<th scope="col">'+x+'</th>' for x in [t('Skill','스킬'),t('Casts','사용 횟수'),t('Ticks','틱 수'),t('Total damage','누적 피해'),t('Share','기여도')])}</tr></thead><tbody>{skill_rows}</tbody></table></div><p class="rank-detail-note"><b>{t('Model priority','모델 우선순위')}</b>: {order}</p><p class="rank-detail-note">{t('Maximum wait for a higher priority cooldown','상위 우선순위 쿨타임 대기 한도')}: {number(c['policy']['holdSeconds'])}{t(' s','초')}. <a href="{r}classes/{E(c['classId'])}/">{t('Class guide','직업 공략')} →</a></p></details>'''

    common = data['commonConditions']
    chips = [(t('Skill level', '스킬 레벨'), str(data['scope']['skillLevel'])),
             (t('Attack', '공격력'), number(common['attack'])),
             (t('Critical', '치명'), number(common['crit']) + '% × ' + number(common['critMultiplier'])),
             (t('Hit chance', '적중'), number(common['accuracy']) + '%'),
             (t('Action time', '동작 시간'), number(common['actionSeconds']) + t(' s assumed', '초 가정'))]
    news = json.loads((ROOT / 'data/news.json').read_text())
    newer = needs_patch_review(news, data['sourceReviewedAt'])
    patch_note = f'<p class="rank-patch-note">{t("A newer North America patch needs review. The table retains the declared tooltip baseline.","새 북미 패치의 재검토가 필요합니다. 아래 순위는 표시된 툴팁 기준을 유지합니다.")} <a href="{r}updates/">{t("Check the patch","패치 확인")} →</a></p>' if newer else ''
    seconds = data['overall'][0]['seconds']
    return f'''<link rel="stylesheet" href="{base}assets/dps-rankings.css?v=1"><section class="rank-desk" data-dps-rankings data-computed-by="backend" data-source-reviewed="{E(data['sourceReviewedAt'])}"><header class="rank-intro"><span class="section-kicker">CLASS DPS / SERVER RESULTS</span><h1>{t('Class DPS rankings','직업별 DPS 순위')}</h1><p>{t('We calculate every class under one common profile. See the results, then compare stationary and moving boss fights.','같은 조건으로 우리가 계산한 결과입니다. 종합 순위와 보스 상황별 차이를 바로 확인하세요.')}</p><div class="rank-tags"><span>{t('Computed on the server','서버 계산 결과')}</span><span>{t('Global tooltip baseline','글로벌 툴팁 기준')}</span><span>{t('Source review','수치 검토')} {E(data['sourceReviewedAt'])}</span></div></header><aside class="rank-scope" aria-label="{t('Ranking scope','순위 적용 범위')}"><strong>{t('Common level-20 model','공통 20레벨 모델')}</strong><p>{t('These ranks compare known skill formulas, without specializations or Stigmas. Gear, animation timings, pets and some charged skills are incomplete; this is not a verified live endgame tier or a Korea patch ranking.','특화·스티그마 없이 확인된 스킬 공식을 비교한 순위입니다. 장비·실제 동작 시간·정령·일부 차징 기술은 자료가 미완성이라 현재 최종빌드 티어나 한국 패치 순위로 확정할 수 없습니다.')}</p></aside>{patch_note}<dl class="rank-conditions">{''.join('<div><dt>'+a+'</dt><dd>'+b+'</dd></div>' for a,b in chips)}</dl><section id="rank-overall" class="rank-overall"><div class="rank-section-head"><h2>{t('Overall DPS','종합 DPS')}</h2><a href="{base}data/dps-rankings.csv" download>{t('Download results','결과 내려받기')} · CSV ↓</a></div><p class="rank-summary">{t('Both boss fights combined','두 보스 전투 합산')} · {number(seconds)}{t(' seconds including interruptions','초, 공격 불가 시간 포함')}. {t('Ranked by total damage ÷ total fight time; displayed values are rounded.','누적 피해 ÷ 총 전투 시간으로 정렬하며, 표시값만 반올림합니다.')}</p>{table(data['overall'], t('Overall server-computed DPS ranking','서버 계산 종합 DPS 순위'))}</section><section class="rank-scenarios"><h2>{t('Rankings by boss fight','보스 상황별 순위')}</h2>{scenarios}</section><section class="rank-class-details"><h2>{t('Damage contributions by class','직업별 피해 구성')}</h2><p>{t('Open a class to see damage, casts and excluded skills from the same two boss fights.','직업을 펼치면 같은 두 보스 전투의 피해·사용 횟수·미반영 기술을 볼 수 있습니다.')}</p>{details}</section><details class="rank-method"><summary>{t('Calculation rules and sources','계산 기준과 출처')}</summary><p><code>{t('Expected hit = (level-specific base + attack × coefficient) × hits × critical expectation × hit chance','기대 피해 = (해당 레벨 고정 피해 + 공격력 × 계수) × 타격 수 × 치명 기대 배율 × 적중 확률')}</code><code>DPS = {t('sum damage / sum full fight seconds','누적 피해 합 / 전체 전투 시간 합')}</code></p><ul><li>{t('All eight classes use the same stats, level, timings and boss conditions. Policies are chosen only on training fights across three seeds, then scored on separate boss fights.','8개 직업의 능력치·레벨·동작 시간·보스 조건을 통일합니다. 3개 학습 시드의 사이클은 학습 전투로만 선택하고, 별도 보스 전투에서 순위를 계산합니다.')}</li><li>{t('Known prerequisite states and elemental stacks must be created by modeled actions. Boss control immunity blocks crowd-control prerequisites; no free external windows are supplied.','선행 상태와 원소 중첩은 모델의 스킬 행동으로 만들어야 합니다. 보스의 상태이상 면역을 검사하며 외부 선행 구간을 임의로 제공하지 않습니다.')}</li><li>{t('Periodic damage begins one interval after the hit, refresh replaces old ticks, and periodic critical damage is omitted. Ticks in invulnerability or after fight end do not deal damage. Chain of Torment uses its DoT duration as an explicit prerequisite assumption.','지속 피해는 적중 후 한 주기 뒤에 시작하고 재적용 시 이전 틱을 교체하며 지속 피해 치명은 제외합니다. 무적 구간·전투 종료 후 틱은 피해에 넣지 않습니다. 고통의 연쇄 선행 상태는 지속 피해 시간을 따른다는 가정입니다.')}</li><li>{t('Insignias expire individually and are consumed on explosion. Cooldowns begin at action start; unknown charge time, pet frequency and trigger timing are not invented. MP sustainability, defense, buffs, resets and basic-combo cadence remain unverified.','문양은 개별 만료하고 폭발 시 소모한다고 가정합니다. 쿨타임은 동작 시작부터 계산합니다. 미확인 차징 시간·정령 주기·발동 시점을 임의로 넣지 않습니다. MP 지속 가능성·방어·버프·쿨 초기화·기본 연계 속도는 미검증입니다.')}</li></ul><p><a href="https://metabot.gg/en/aion-2/skills" target="_blank" rel="noopener">MetaBot · {t('client tooltip sources','클라이언트 툴팁 출처')} ↗</a> · <a href="{base}data/dps-rankings.json">{t('Full computed results','전체 계산 결과')} · JSON</a> · <a href="{r}updates/">{t('Official patches','공식 패치')} →</a></p></details></section>'''

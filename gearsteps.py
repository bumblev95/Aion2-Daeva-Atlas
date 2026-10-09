"""Practical enhancement steps and material routes with regional sources."""
from html import escape as e


def guide(lang, base):
    k = lang == 'ko'
    t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')
    steps = [
        (('Select the equipment', '강화할 장비 선택'),
         ('Open Enhancement and select the item you intend to keep using.',
          '강화 메뉴에서 계속 사용할 장비를 선택합니다.')),
        (('Prepare the matching material', '장비에 맞는 재료 준비'),
         ('Regular enhancement uses Kinah and Enhance Stones. Amulets and belts use their matching scrolls.',
          '일반 장비는 키나·강화석, 아뮬렛·허리띠는 해당 부위의 강화 주문서를 준비합니다.')),
        (('Read the next attempt', '이번 강화의 비용·확률 확인'),
         ('Check the required amount, success chance and failure result for this item and level.',
          '선택한 장비·단계의 필요 수량, 성공률, 실패 시 결과를 확인합니다.')),
        (('Enhance and compare the result', '강화 후 변화 확인'),
         ('Complete the attempt. Compare the new level and stats before spending on another step.',
          '강화를 진행한 뒤 강화 단계와 능력치 변화를 확인하고 다음 단계의 투자 범위를 정합니다.')),
    ]
    process = ''.join(f'<li><span class="growth-step-number" aria-hidden="true">0{i}</span><div><h3>{e(title[k])}</h3><p>{e(body[k])}</p></div></li>' for i, (title, body) in enumerate(steps, 1))
    materials = [
        (('Kinah + Enhance Stones', '키나 + 강화석'),
         ('Regular equipment enhancement', '일반 장비 강화'),
         ('Stone rewards: quests, dungeons, chests and achievements. Quest/dungeon completion achievements also list Kinah.',
          '강화석은 퀘스트·던전 보상, 강화석 상자·업적에서 찾습니다. 퀘스트·던전 완료 업적의 키나 보상도 확인합니다.'),
         'https://metabot.gg/en/aion-2/items/enhance-stone', ('Listed stone sources', '강화석 획득처')),
        (('Revelation Amulet scroll · KR', '계시의 아뮬렛 강화 주문서 · 한국 참고'),
         ('The matching amulet', '해당 아뮬렛 강화'),
         ('Lord’s Traces → Monolith resonance rewards in the KR field guide.',
          '한국 필드 공략: 주신의 흔적 수집 → 모노리스 공명 보상'),
         r + 'endgame/#after-story-feathers', ('Feather and turn-in route', '깃털·반납 순서')),
        (('Noble Belt scroll · KR', '고결의 허리띠 강화 주문서 · 한국 참고'),
         ('The matching belt', '해당 허리띠 강화'),
         ('Garrison completion rewards in the KR field guide.',
          '한국 필드 공략: 주둔지 완료 보상'),
         'https://www.inven.co.kr/webzine/news/?news=311570&site=aion2', ('Original field reward guide', '필드 보상 원문')),
    ]
    rows = []
    for name, use, where, url, label in materials:
        external = ' target="_blank" rel="noopener noreferrer"' if url.startswith('https://') else ''
        rows.append(f'<tr><th scope="row">{e(name[k])}</th><td>{e(use[k])}</td><td>{e(where[k])}<br><a href="{e(url)}"{external}>{e(label[k])} →</a></td></tr>')
    return f'''<section class="reference-section enhancement-route post-story" id="upgrade" aria-labelledby="enhancement-heading">
<header class="start-reference-heading"><span class="section-kicker">{t('ENHANCE EQUIPMENT', '장비 강화')}</span><h2 id="enhancement-heading">{t('How do I enhance this item?', '이 장비는 어떻게 강화하지?')}</h2><p>{t('Match the equipment to its material, collect what is missing, then follow the enhancement steps.', '장비에 맞는 재료를 확인하고 부족한 재료를 모은 뒤 강화 순서를 따라갑니다.')}</p></header>
<nav class="rpg-guide-nav" aria-label="{t('Enhancement guide sections', '강화 공략 순서')}"><a href="#enhancement-process">{t('Enhancement steps', '강화 순서')}</a><a href="#enhancement-materials">{t('Materials and sources', '재료·획득처')}</a><a href="#upgrade-decisions">{t('How far to invest', '얼마나 투자할까')}</a></nav>
<ol class="growth-route" id="enhancement-process">{process}</ol>
<section id="enhancement-materials"><h3>{t('Which material, and where do I get it?', '무슨 재료가 필요하고, 어디서 얻을까?')}</h3><div class="reference-table"><table><thead><tr><th>{t('Material', '필요 재료')}</th><th>{t('Used for', '사용처')}</th><th>{t('Where to obtain it', '획득처')}</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<p class="reference-scope">{t('General steps use the Global client reference; amulet and belt routes are from the dated KR guide. Match quantities and conditions to your server’s item and reward screen.', '일반 절차는 글로벌 클라이언트 참고 자료, 아뮬렛·허리띠 동선은 한국 필드 공략 기준입니다. 필요 수량·조건은 현재 서버의 장비·보상 화면에 맞춥니다.')}</p>
<details class="evidence"><summary>{t('Enhancement and material sources · reviewed Oct 8, 2026', '강화 절차·재료 출처 · 2026.10.08 검토')}</summary><a href="https://metabot.gg/en/aion-2/guides/gear-enhancement-guide" target="_blank" rel="noopener noreferrer">{t('Global enhancement reference', '글로벌 강화 참고 자료')} ↗</a><a href="https://metabot.gg/en/aion-2/items/enhance-stone" target="_blank" rel="noopener noreferrer">{t('Client item data · Enhance Stone', '클라이언트 아이템 자료 · 강화석')} ↗</a><a href="https://www.inven.co.kr/webzine/news/?news=311570&amp;site=aion2" target="_blank" rel="noopener noreferrer">{t('Inven Rune · KR field rewards · Nov 22, 2025', '인벤 Rune · 한국 필드 보상 · 2025.11.22')} ↗</a></details>
</section>'''

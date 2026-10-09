"""Connect post-story rewards to the investments they actually fund."""
from html import escape as e

SOURCES = [
    ('Global item text · Wisdom Stone', '글로벌 아이템 설명 · 지혜의 돌',
     'https://metabot.gg/en/aion-2/items/wisdom-stone-bound'),
    ('Global item text · Daevanion Crystal', '글로벌 아이템 설명 · 데바니온 결정',
     'https://metabot.gg/en/aion-2/items/daevanion-crystal-bound'),
    ('Global client reference · Sealed Dungeons', '글로벌 클라이언트 자료 · 봉인 던전',
     'https://metabot.gg/en/aion-2/guides/beginners-guide'),
    ('Inven · Rune · KR field rewards (2025-11-22)', '인벤 Rune · 한국 필드 보상 (2025.11.22)',
     'https://www.inven.co.kr/webzine/news/?news=311570&site=aion2'),
    ('Inven · Rokah · KR feathers and Monolith (2025-11-21)', '인벤 Rokah · 한국 깃털·모노리스 (2025.11.21)',
     'https://www.inven.co.kr/webzine/news/?news=311568&site=aion2'),
    ('Global client reference · Repeatable activities', '글로벌 클라이언트 자료 · 반복 콘텐츠',
     'https://metabot.gg/en/aion-2/guides/endgame-guide'),
]


def teaser(lang, base):
    t = lambda en, ko: ko if lang == 'ko' else en
    r = base + ('ko/' if lang == 'ko' else '')
    return f'''<a class="endgame-gateway post-story-gateway" href="{r}endgame/#after-story"><strong>{t('Story cleared. What makes me stronger now?', '메인 스토리 끝났는데, 이제 뭘 해야 강해질까?')}</strong><span>{t('Sealed Dungeons · feathers · spending rewards · your next run', '봉인 던전·깃털 → 보상 사용 → 스킬·장비 성장')} →</span></a>'''


def guide(lang, base):
    k = lang == 'ko'
    t = lambda en, ko: ko if k else en
    r = base + ('ko/' if k else '')
    steps = [
        ('spend-points', ('Use the points you already earned', '이미 받은 포인트부터 실제 성장으로 바꾸기'),
         ('Use Wisdom Stones and Daevanion Crystals in your inventory. Spend skill points on frequently used skills, equip available specializations, and invest board points in useful nodes.',
          '가방에 남은 지혜의 돌·데바니온 결정을 사용하세요. 스킬 포인트는 자주 쓰는 기술에 투자하고, 열린 특화 슬롯에 효과를 장착합니다. 데바니온 포인트는 필요한 능력치·스킬 노드에 배분합니다.'),
         ('Check the skill level, equipped specialization and board node after investing.', '투자 전후의 스킬 레벨·장착한 특화·데바니온 노드를 확인합니다.'),
         'skills/', ('Class skill priorities', '직업별 스킬 투자 순서')),
        ('field-rewards', ('Clear missed field growth rewards', '지도에서 놓친 봉인 던전·지역 보상 챙기기'),
         ('Inspect the name behind a map question mark. Identify a quest, Sealed Dungeon or another activity. Clear nearby unfinished Sealed Dungeons and claim the listed reward. Use any Wisdom Stones or Daevanion Crystals you receive; these feed separate point systems.',
          '지도에 ?가 보이면 이름을 열어 지역 퀘스트인지, 봉인 던전인지, 다른 콘텐츠인지 구분하세요. 가까운 미완료 봉인 던전부터 실제 보상 목록을 확인해 완료 보상을 받습니다. 지혜의 돌·데바니온 결정을 얻었다면 사용하고 각각의 포인트를 투자합니다.'),
         ('Claiming and using a clear reward completes the growth loop.', '클리어 → 완료 보상 받기 → 아이템 사용 → 포인트 투자까지 이어져야 합니다.'),
         'maps/?type=sealed_dungeon&zone=Verteron', ('Elyos Sealed Dungeons', '천족 봉인 던전 위치')),
        ('feathers', ('Collect feathers, then return to the Monolith', '깃털을 줍고 모노리스에서 보상으로 교환하기'),
         ('The feather-shaped Lord’s Traces connect to Monolith resonance in the linked KR guide. Turn them in, claim rewards, use Wisdom Stones and apply Revelation Amulet scrolls. Work through a manageable area near an activated travel point.',
          '깃털 모양의 주신의 흔적은 한국 공략에서 모노리스 공명으로 연결됩니다. 모노리스에 반납해 보상을 받고, 지혜의 돌은 사용하고 계시의 아뮬렛 강화 주문서는 해당 아뮬렛에 씁니다. 활성화한 이동 거점 근처부터 작은 구역씩 정리하세요.'),
         ('Finish the collection, turn-in, item-use and equipment steps together.', '깃털 수집 → 모노리스 반납 → 보상 사용·아뮬렛 강화가 한 묶음입니다.'),
         SOURCES[4][2], ('Feather locations and original guide', '깃털 위치·원문 공략')),
        ('accessories', ('Finish a named accessory goal', '장신구 성장도 한 부위씩 마무리하기'),
         ('The KR field guide links Garrison rewards to Noble Belt scrolls and Manastones. If present in your client, use them for the matching accessory or useful option. Compare the item before and after, and collect materials for a specific upgrade.',
          '한국 필드 공략은 주둔지 보상을 고결의 허리띠 강화 주문서·마석으로 연결합니다. 현재 서버에서도 같은 보상이 보이면 해당 허리띠와 필요한 장비 옵션에 활용하세요. 재료만 모아두기보다 한 부위의 강화 전후를 확인합니다.'),
         ('Skill and board growth, accessory growth and new gear are separate paths.', '스킬·데바니온 성장, 장신구 강화, 새 장비 획득은 서로 다른 성장 경로입니다.'),
         'gear/#upgrade', ('Equipment upgrade guide', '장비·강화 안내')),
        ('repeatable', ('Choose a reward-bearing run, then move up', '보상 받을 수 있는 던전부터 반복하고 다음 단계로 이동하기'),
         ('Choose an unlocked activity with an upgrade you need. Expedition supplies equipment; Transcendence adds Arcana. Duty or other unlocked activities fund upgrades. Check reward counters and required Od Energy before repeated clears.',
          '지금 열려 있는 콘텐츠 중 필요한 보상이 있는 곳을 고릅니다. 원정은 장비, 초월은 아르카나 성장으로 연결하고, 사명 등 해금된 콘텐츠에서 다음 강화에 필요한 재화를 확보합니다. 반복하기 전에 남은 보상 횟수와 오드 에너지 등 보상 조건을 확인하세요.'),
         ('After an upgrade, revisit entry requirements and how consistently you clear.', '성장 후 다음 난이도 입장 조건과 클리어 안정성을 다시 확인하고 목표를 올립니다.'),
         'endgame/#boss-guides', ('Prepare for the next dungeon', '다음 던전·보스 준비')),
    ]
    cards = []
    for i, (key, title, action, result, url, label) in enumerate(steps, 1):
        external = url.startswith('https://')
        target = url if external or url.startswith('#') else r + url
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
        extra = ''
        if key == 'field-rewards':
            extra = f'<a href="{r}maps/?type=sealed_dungeon&amp;zone=Altgard">{t("Asmodian Sealed Dungeons", "마족 봉인 던전 위치")} →</a>'
        cards.append(f'''<li id="after-story-{key}"><span class="growth-step-number" aria-hidden="true">0{i}</span><div><h3>{e(title[k])}</h3><p>{e(action[k])}</p><p class="growth-result"><strong>{t('What changes', '성장 확인')}</strong> {e(result[k])}</p><div class="reference-links"><a href="{e(target)}"{attrs}>{e(label[k])} →</a>{extra}</div></div></li>''')
    rewards = [
        (('Wisdom Stone', '지혜의 돌'), ('Use → skill point → skill investment', '아이템 사용 → 스킬 포인트 → 스킬 투자')),
        (('Daevanion Crystal', '데바니온 결정'), ('Use → Daevanion point → board node', '아이템 사용 → 데바니온 포인트 → 보드 노드')),
        (('Lord’s Traces · KR', '주신의 흔적 · 한국 참고'), ('Monolith turn-in → resonance reward → use the item', '모노리스 반납 → 공명 보상 → 보상 아이템 사용')),
        (('Accessory scrolls · KR names', '장신구 주문서 · 한국 명칭'), ('Matching Revelation Amulet or Noble Belt → enhance', '계시의 아뮬렛·고결의 허리띠에 맞는 주문서 → 해당 부위 강화')),
        (('Equipment and Arcana', '새 장비·아르카나'), ('Compare equipped item → equip a useful upgrade', '현재 장착품과 비교 → 필요한 옵션의 새 장비 장착')),
    ]
    rows = ''.join(f'<tr><th scope="row">{e(name[k])}</th><td>{e(use[k])}</td></tr>' for name, use in rewards)
    sources = ''.join(f'<li><a href="{e(url)}" target="_blank" rel="noopener noreferrer">{e((en, ko)[k])} ↗</a></li>' for en, ko, url in SOURCES)
    return f'''<section class="reference-section post-story" id="after-story" aria-labelledby="after-story-heading"><header class="start-reference-heading"><span class="section-kicker">{t('AFTER THE STORY', '스토리 이후 성장')}</span><h2 id="after-story-heading">{t('The story ended. Your next five steps.', '메인 스토리 이후, 강해지는 순서 5단계')}</h2><p>{t('Start with unused points and missed field rewards, then repeat a dungeon for an upgrade you can name.', '남은 포인트와 놓친 필드 보상부터 챙긴 뒤, 필요한 장비를 얻을 수 있는 던전을 반복합니다.')}</p></header><p class="reference-scope">{t('Global item references and KR field guides are labeled separately. Match the rewards and unlocks shown by your server.', '글로벌 아이템 자료와 한국 필드 공략을 구분했습니다. 획득 수량·해금 조건은 현재 서버의 보상 화면에 맞춰 확인합니다.')}</p><ol class="growth-route">{''.join(cards)}</ol><section class="growth-rewards" id="use-rewards"><h3>{t('I received a reward. Where does it go?', '보상은 받았는데, 어디에 써야 할까?')}</h3><div class="reference-table"><table><thead><tr><th scope="col">{t('Reward', '얻은 보상')}</th><th scope="col">{t('Turn it into growth', '실제 성장으로 바꾸는 방법')}</th></tr></thead><tbody>{rows}</tbody></table></div></section><div class="growth-rhythm"><article><h3>{t('Finish / claim completion rewards', '먼저 정리할 완료 보상')}</h3><p>{t('Unfinished field objectives, feathers and rewards already in your inventory. A completed objective does not become another first-clear reward just by repeating it.', '미완료 지역 콘텐츠, 깃털 수집, 가방에 남은 성장 보상부터 정리합니다. 완료한 필드 콘텐츠를 다시 돈다고 첫 완료 보상이 계속 생기는 것은 아닙니다.')}</p></article><article><h3>{t('Repeat for an available useful reward', '이후 반복할 보상 파밍')}</h3><p>{t('An unlocked dungeon, Duty or another activity with a needed reward. Check its reward count, complete one upgrade, then review the next target.', '필요한 보상이 있는 해금된 던전·사명 등을 반복합니다. 입장 가능 여부와 보상 횟수를 따로 확인하고 성장 목표 하나를 마친 뒤 다음 목표를 정합니다.')}</p></article></div><p class="growth-bottom-line">{t('Follow the full loop: earn → claim → use → invest/equip → try the next challenge.', '획득 → 보상 수령 → 아이템 사용 → 투자·장착 → 다음 콘텐츠 확인까지 이어가세요.')}</p><details class="evidence" id="growth-sources"><summary>{t('Reward sources and feather locations · reviewed Oct 9, 2026', '보상 출처·깃털 위치 참고 · 2026.10.09 검토')}</summary><ul>{sources}</ul><p>{t('Inven links original Elyos/Asmodian feather maps. Its old feather auto-move tip is withdrawn. Our map covers story NPCs, travel points and Sealed Dungeons; use the original feather maps for those coordinates.', '인벤 깃털 글에서 천족·마족 원본 위치 지도를 볼 수 있습니다. 예전 깃털 자동이동 팁은 철회된 내용입니다. 자체 지도에는 메인 퀘스트·이동 거점·봉인 던전이 있으며, 깃털 좌표는 원본 위치 공략을 참고합니다.')}</p></details></section>'''

"""Reviewed activation rules, separated from optional damage bonuses.

Global base-1 client tooltips via MetaBot, reviewed 2026-10-08. This is
not combat validation or a KR ruleset. Unknown triggers require timed inputs.
"""
import re

STATES = [
    ('slow', 'Slow', '이동 둔화'), ('root', 'Root', '속박'),
    ('knockdown', 'Knockdown', '넘어짐'), ('stun', 'Stun', '기절'),
    ('frost', 'Frost', '빙결'), ('stagger', 'Stagger', '그로기'),
    ('fire-mark', 'Fire Mark', '불의 표식'),
    ('chain-of-torment', 'Chain of Torment', '고통의 연쇄'),
    ('judgment-ready', 'Judgment available', '심판 사용 가능'),
    ('dark-crush-ready', 'Dark Crush available', '암격쇄 사용 가능'),
    ('critical-trigger', 'Critical-hit trigger available', '치명타 연계 사용 가능'),
    ('spirit-trigger', 'Spirit-skill trigger available', '정령 기술 연계 사용 가능'),
    ('dodge', 'After Dodge', '회피 후 사용 가능'), ('flying', 'Flying', '비행 중'),
    ('immune-trigger', 'Confirmed immunity-target proc', '면역 대상 발동 확인'),
]
REVIEWED_SKILL_HASH = '8cff9ef8aa9374122e9df305fdfcea69317eed0327a245bb19d0952459ad1a6e'
CONTROL = {'slow', 'root', 'knockdown', 'stun', 'frost', 'stagger'}

GATES = {
    'overhead-slam': ['knockdown', 'immune-trigger'],
    'aerial-snare': ['knockdown', 'immune-trigger'],
    'annihilate': ['stun', 'knockdown', 'immune-trigger'],
    'shadow-fall': ['stun', 'immune-trigger'],
    'frost-burst': ['frost', 'immune-trigger'],
    'wave-blow': ['stun', 'immune-trigger'],
    'burst-arrow': ['slow', 'root'], 'blaze': ['fire-mark'],
    'condemnation': ['chain-of-torment'],
    'judgment': ['judgment-ready'], 'dark-crush': ['dark-crush-ready'],
    'heart-gore': ['critical-trigger'], 'dimensional-control': ['spirit-trigger'],
    **{x: ['stagger'] for x in ('sword-aura-rampage', 'flash-rampage',
       'storm-rampage', 'arrow-scattershot', 'flame-scattershot',
       'rapid-scattershot', 'lightning-strike-scattershot', 'gust-rampage')},
    **{x: ['dodge', 'flying'] for x in ('rush-strike', 'shield-rush',
                                     'infiltrate', 'tremor-crush')},
}
HELPERS = {'templar': ['shield-smite'], 'chanter': ['impactful-crush'],
           'cleric': ['chain-of-torment']}

def effect(state, duration, on='hit', source=None, **extra):
    return dict(state=state, duration=duration, on=on, chance=100, source=source, **extra)

def rules(skill, resources):
    sid = skill['id']; text = skill['en_data']['effect']
    result = dict(requires=GATES.get(sid, []), effects=[], consumeStates=[],
                  elementCost=4 if sid == 'elemental-fusion' else 0,
                  mpCost=resources.get(sid, {}).get('mpCost'), mpGain=0,
                  source=skill['url'], conditionRegion='Global')
    gain = re.search(r'restores (\d+) MP', text, re.I)
    if gain and 'on landing a Critical Hit' not in text:
        result['mpGain'] = int(gain[1])
    if sid == 'snare-shot' or sid == 'ice-chain':
        result['effects'].append(effect('slow', 5, source=skill['url']))
    if sid == 'winters-shackles':
        result['effects'].append(effect('slow', 3, source=skill['url']))
    if sid == 'mocking-blade':
        result['effects'].append(effect('knockdown', 3, source=skill['url']))
    if sid == 'shadowstrike':
        result['effects'].append(effect('stun', 3, source=skill['url']))
    if sid == 'chain-of-torment':
        # The source gives a 10s DoT. Treating this as the prerequisite lifetime
        # is a visible model assumption; users can instead supply observed windows.
        result['effects'].append(effect('chain-of-torment', 10, source=skill['url'],
                                       assumption='dot-lifetime'))
    if sid in ('shield-smite', 'warding-strike', 'shield-rush'):
        result['effects'].append(effect('judgment-ready', 2, 'use', skill['url']))
    if sid in ('impactful-crush', 'spinning-strike', 'marchutans-wrath', 'ensnaring-mark'):
        result['effects'].append(effect('dark-crush-ready', 3 if skill['kind'] == 'stigma' else 2,
                                       'use', skill['url']))
    if sid in ('judgment', 'dark-crush', 'heart-gore', 'dimensional-control'):
        # One follow-up per opener is conservative, not asserted client behavior.
        result['consumeStates'] = result['requires'].copy()
    if skill['cls'] == 'sorcerer' and re.search(r'Fire damage', text):
        result['effects'].append(effect('fire-mark', 5, source='https://metabot.gg/en/aion-2/skills/fire-mark',
                                       passive='fire-mark'))
    return result

def audit(skill, rule):
    text = skill['en_data']['effect']
    categories = []
    if rule['requires']: categories.append('activation')
    if rule['elementCost']: categories.append('stack-resource')
    if rule['effects']: categories.append('provider')
    # Do not interpret bonuses, chance-based CC, MP-on-crit, or specializations
    # as a prerequisite for the base direct damage.
    if re.search(r'chance|Back attack|Precision|Insignia|Charge Level', text, re.I):
        categories.append('conditional-effect')
    return dict(id=skill['id'], en=skill['en'], ko=skill['ko'], kind=skill['kind'],
                source=skill['url'], categories=categories, requires=rule['requires'],
                elementCost=rule['elementCost'], mpCost=rule['mpCost'],
                unknownTrigger=bool(set(rule['requires']) & {'critical-trigger', 'spirit-trigger',
                    'immune-trigger', 'dodge'}),
                specializationsExcluded=bool(skill['en_data']['specs']))

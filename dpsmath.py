"""Base-1 damage terms, kept separate from unverified timing/bonus mechanics.

Source numbers are client-tooltip terms, not measured damage. A secondary
chance/CC/MP sentence must not erase a known direct term. All 96 actives get
an audit entry, including genuinely non-offensive skills and unresolved pets.
"""
import re
from dpsrules import REVIEWED_SKILL_HASH

REVIEWED_AT = '2026-10-08'
TERM = r'([\d,]+(?:\.\d+)?)\s*\(\+([\d,.]+)% Attack\)'
DIRECT = re.compile(r'\bdeal(?:s|ing)?\s+' + TERM + r'\s*(?:\w+\s+)?damage', re.I)
CHARGES = {'punishment', 'deadshot', 'hellfire', 'bolt'}
UNRESOLVED = {
    'bittercold-wind': ['ground-effect-hit-frequency'],
    'explosion-trap': ['trap-trigger-time'],
    'divine-aura': ['summon-tick-interval'],
    **{f'summon-{s}-spirit': ['pet-basic-damage', 'pet-attack-frequency',
                             'pet-skill-proc-timeline'] for s in ('fire','water','earth','wind')},
}
DOTS = {
    'drill-dart': (43, 45, 1, 6),
    'jointstrike-curse': (148, 150, 1, 5),
    'debilitating-mark': (74, 141.9, 1, 10),
    'chain-of-torment': (173, 189.8, 1, 10),
}

def terms(match):
    return dict(flat=float(match[1].replace(',', '')), coefficient=float(match[2].replace(',', '')))

def damage(skill):
    sid, text = skill['id'], skill['en_data']['effect']
    result = dict(flat=0, coefficient=0, damageStatus='non-offensive', periodic=[],
                  mathUnverified=[], skillLevel=1, source=skill['url'])
    if sid in UNRESOLVED:
        result.update(damageStatus='input-required', damageInputRequired=True,
                      damageConfirmed=False, mathUnverified=UNRESOLVED[sid])
        matches = list(DIRECT.finditer(text))
        if matches: result['referenceTerms'] = [terms(m) for m in matches]
    elif sid in CHARGES:
        matches = list(re.finditer(TERM, text))
        assert len(matches) == 2, sid
        result.update(damageStatus='charge-input-required', charge={
            'minimum': terms(matches[0]), 'maximum': terms(matches[1]),
            'intermediateVerified': False, 'durationVerified': False},
            chargeConfirmed=False, mathUnverified=['charge-duration', 'intermediate-charge-damage'])
        # Endpoint values are selectable references, never a 1s max-charge seed.
    else:
        match = DIRECT.search(text)
        if match:
            result.update(**terms(match), damageStatus='direct')
        elif re.search(r'\bdeal(?:s|ing)?\b', text, re.I):
            raise ValueError('Unaudited damage wording: ' + sid)
    if sid in DOTS:
        flat, coefficient, interval, duration = DOTS[sid]
        # Assert against the frozen tooltip, so a changed term fails review.
        tail = re.search(r'\b(?:deals|dealing)\s+' + TERM +
                         r'\s*(?:Fire damage|Damage over Time|damage)\s*(?:over Time\s*)?every\s+([\d.]+)s', text, re.I)
        assert tail and terms(tail) == dict(flat=flat, coefficient=coefficient), sid
        assert float(tail[3]) == interval and f'for {duration}s' in text, sid
        result['periodic'] = [dict(flat=flat, coefficient=coefficient, interval=interval,
                                   duration=duration, firstTick=interval, source=skill['url'])]
        result['mathUnverified'] += ['first-tick-phase', 'refresh-rule', 'periodic-critical-rule']
    if sid == 'savage-roar':
        result.update(insigniaGain=1, insigniaDuration=10)
    if sid == 'insignia-explosion':
        variants = [dict(stacks=0, flat=result['flat'], coefficient=result['coefficient'])]
        for m in re.finditer(r'(\d) stacks?:\s*' + TERM, text):
            variants.append(dict(stacks=int(m[1]), flat=float(m[2].replace(',','')), coefficient=float(m[3].replace(',',''))))
        assert [v['stacks'] for v in variants] == list(range(6))
        result.update(insigniaDamage=variants)
        result['mathUnverified'] += ['insignia-consumption', 'stack-expiry-refresh']
    if sid == 'jointstrike-curse':
        result['mathUnverified'] += ['coordinated-spirit-hit', 'duration-from-shared-curse-effect']
    if re.search(r'Back attack|Precision|Damage Boost|Critical Damage Boost|Defense by', text, re.I):
        result['mathUnverified'] += ['conditional-bonus-or-stat-conversion']
    return result

def audit(skill, model):
    return dict(id=skill['id'], en=skill['en'], ko=skill['ko'], source=skill['url'],
                status=model['damageStatus'], skillLevel=1,
                directTerms=dict(flat=model['flat'], coefficient=model['coefficient'])
                    if model['damageStatus'] == 'direct' else None,
                periodic=model['periodic'], charge=model.get('charge'),
                unverified=model['mathUnverified'])

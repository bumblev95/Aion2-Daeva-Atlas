"""Freeze factual client terms at reviewed levels; never fetch during publishing.

Run explicitly after reviewing the source diff. --cache accepts downloaded
per-level responses for a reproducible review without another network request.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import dpsmath

def extract_levels(html):
    chunks = []
    for raw in re.findall(r'self\.__next_f\.push\((\[.*?\])\)</script>', html, re.S):
        value = json.loads(raw)
        if len(value) > 1 and isinstance(value[1], str):
            chunks.append(value[1])
    stream = ''.join(chunks)
    for match in re.finditer(r'"levels":\s*(\[)', stream):
        try:
            rows, _ = json.JSONDecoder().raw_decode(stream[match.start(1):])
        except ValueError:
            continue
        if isinstance(rows, list) and rows and all(isinstance(r, dict) and 'level' in r and 'text' in r for r in rows):
            return {str(r['level']): r for r in rows if r['level'] in (1, 20)}
    raise ValueError('Per-level client terms not found')

def normalized(text):
    return ' '.join(text.split())

def damage_free(text, sid):
    text = re.sub(dpsmath.TERM, 'DAMAGE', text)
    if sid == 'warding-strike':
        # Reviewed non-damage change: the maximum immediate heal also scales.
        text = re.sub(r'DAMAGE-[\d,]+ HP', 'HEAL HP', text)
    return normalized(text)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reviewed-at', required=True, type=date.fromisoformat)
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args()
    skills = json.loads((ROOT / 'data/skills.json').read_text())
    result = dict(schema=1, region='Global', reviewedAt=str(args.reviewed_at), levels=[1, 20],
                  skillSourceHash=hashlib.sha256((ROOT / 'data/skills.json').read_bytes()).hexdigest(),
                  provenance='Public Global client per-level tooltips, via MetaBot. No combat timing or legal equipment loadout is inferred.',
                  skills={})
    for skill in skills:
        if skill['kind'] != 'active':
            continue
        sid = skill['id']
        if args.cache:
            source = json.loads((args.cache / (sid + '.json')).read_text())
            if source['id'] != sid or source['url'] != skill['url']:
                raise ValueError('Wrong cached source: ' + sid)
            levels = source['levels']
        else:
            with urllib.request.urlopen(skill['url'], timeout=30) as response:
                levels = extract_levels(response.read().decode())
        if set(levels) != {'1', '20'} or any(v['level'] != int(k) for k, v in levels.items()):
            raise ValueError('Incomplete level snapshot: ' + sid)
        if normalized(levels['1']['text']) != normalized(skill['en_data']['effect']):
            raise ValueError('Base tooltip changed: ' + sid)
        base = dpsmath.damage(skill)
        if base['damageStatus'] == 'direct' and damage_free(levels['1']['text'], sid) != damage_free(levels['20']['text'], sid):
            raise ValueError('Review non-damage mechanics before publishing: ' + sid)
        models = {}
        metadata = {}
        hashes = {}
        for key, value in levels.items():
            clone = copy.deepcopy(skill)
            clone['en_data']['effect'] = value['text']
            models[key] = dpsmath.damage(clone, int(key))
            cd = value['cooldown']
            if cd is not None and not re.fullmatch(r'[\d.]+s', cd):
                raise ValueError('Unknown cooldown: ' + sid)
            metadata[key] = dict(cooldown=float(cd[:-1]) if cd else 0,
                                 mpCost=float(value['mp']) if value['mp'] else None)
            hashes[key] = hashlib.sha256(normalized(value['text']).encode()).hexdigest()
        result['skills'][sid] = dict(source=skill['url'], models=models, metadata=metadata, tooltipHashes=hashes)
    (ROOT / 'data/dps-skill-levels.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Reviewed level 1/20 terms for', len(result['skills']), 'active skills; no level extrapolation.')

if __name__ == '__main__':
    main()

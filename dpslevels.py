"""Apply reviewed per-level client terms without inventing linear scaling."""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).parent

@lru_cache(maxsize=1)
def snapshot():
    data = json.loads((ROOT / 'data/dps-skill-levels.json').read_text())
    actual = hashlib.sha256((ROOT / 'data/skills.json').read_bytes()).hexdigest()
    if data['skillSourceHash'] != actual:
        raise ValueError('Skill-level snapshot needs review against the current skillbook')
    if data['region'] != 'Global' or data['levels'] != [1, 20]:
        raise ValueError('Unsupported skill-level snapshot')
    return data

def model(skill, base_model, level):
    data = snapshot()
    row = data['skills'][skill['id']]
    if row['source'] != skill['url'] or row['models']['1'] != base_model:
        raise ValueError('Base terms changed; review levels for ' + skill['id'])
    if level not in data['levels']:
        raise ValueError('No reviewed tooltip for skill level ' + str(level))
    return row['models'][str(level)].copy()

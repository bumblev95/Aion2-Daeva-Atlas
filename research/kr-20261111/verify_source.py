#!/usr/bin/env python3
"""Explicit optional NC source recheck. Does not change any repository file."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from scripts.collect_updates import fetch, fingerprint  # noqa: E402


def verify(payload, review):
    article = payload['article']
    meta = article['contentMeta']
    assert meta['id'] == '6af370b8577e8c01355e047b', 'Wrong article'
    assert meta['categoryBoard']['boardAlias'] == 'update_ko', 'Wrong region/board'
    body = article['content']['content']
    assert fingerprint(meta['title'], body) == review['sourceHash'], 'NC source changed; re-review before reuse'
    return dict(sourceHash=review['sourceHash'], sourceUpdatedAt=meta['timestamps']['updatedAt'],
                status='source matches reviewed body; live mechanics remain unverified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--file', type=Path, help='Previously downloaded complete NC API JSON')
    source.add_argument('--fetch', action='store_true', help='One read of the public NC API')
    args = parser.parse_args()
    review = json.loads((Path(__file__).parent / 'inputs.json').read_text())
    payload = fetch(review['sourceApi']) if args.fetch else json.loads(args.file.read_text())
    print(json.dumps(verify(payload, review), ensure_ascii=False))

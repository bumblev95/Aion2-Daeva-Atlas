#!/usr/bin/env python3
"""Collect public NC announcements; preserve successful snapshots on failures.

Only headlines, short teasers, timestamps and hashes are published. Full articles
stay on the publisher's site. Human reviews are bound to a content hash.
"""
import argparse
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    dict(id='kr-update', region='KR', kind='patch', base='https://api-community.plaync.com/aion2/', alias='update_ko', page='https://aion2.plaync.com/ko-kr/board/update/view?articleId='),
    dict(id='kr-notice', region='KR', kind='news', base='https://api-community.plaync.com/aion2/', alias='notice_ko', page='https://aion2.plaync.com/ko-kr/board/notice/view?articleId='),
    dict(id='na-update', region='NA', kind='patch', base='https://api-global-community.plaync.com/aion2_global/', alias='update_en', page='https://aion2.plaync.com/en-us/board/update/view?articleId='),
    dict(id='na-notice', region='NA', kind='news', base='https://api-global-community.plaync.com/aion2_global/', alias='notice_en', page='https://aion2.plaync.com/en-us/board/notice/view?articleId='),
]

def stamp():
    return datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def fetch(url):
    request = Request(url, headers={'User-Agent': 'PlayersCodex/1.0 (+https://bumblev95.github.io/Aion2-Daeva-Atlas/about/)'})
    # No auth, cookies, anti-bot bypass or repeated requests after rate limiting.
    with urlopen(request, timeout=25) as response:
        data = response.read(4_000_001)
        if len(data) > 4_000_000:
            raise ValueError('oversized response')
        return json.loads(data)

def text(value):
    if not isinstance(value, str):
        raise ValueError('expected content text')
    value = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', value, flags=re.S|re.I)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', value))).strip()

def fingerprint(title, body):
    return hashlib.sha256((title+'\n'+text(body)).encode()).hexdigest()

def reviewed(item, reviews):
    review = reviews.get(item['id'], {})
    valid = bool(review and item.get('contentHash') and review.get('contentHash') == item['contentHash'])
    item['reviewState'] = 'reviewed' if valid else 'revised' if review else 'pending'
    item['summary'] = review.get('summary', {}) if valid else {}
    item['changes'] = review.get('changes', []) if valid else []
    item['classScopeReviewed'] = bool(valid and review.get('classScopeReviewed'))
    item['reviewedAt'] = review.get('reviewedAt') if valid else None
    return item

def collect_source(source, previous, reviews, now, fetcher=fetch):
    prior = previous.get(source['id'], {})
    try:
        response = fetcher(source['base']+'board/'+source['alias']+'/article?moreSize=6')
        contents = response.get('contentList')
        if not isinstance(contents, list) or not contents:
            raise ValueError('empty or invalid source list')
        old = {x['id']: x for x in prior.get('items', [])}
        items = []
        for meta in contents[:6]:
            if not isinstance(meta.get('id'), str) or not meta.get('title'):
                raise ValueError('invalid article metadata')
            dates = meta.get('timestamps', {})
            item = dict(id=meta['id'], title=meta['title'][:220], region=source['region'], kind=source['kind'],
                        source=source['id'], url=source['page']+meta['id'],
                        publishedAt=dates.get('postedAt'), sourceUpdatedAt=dates.get('updatedAt'),
                        contentHash=None, bodyState='not-required')
            if source['kind'] == 'patch':
                prior_item = old.get(item['id'], {})
                if prior_item.get('sourceUpdatedAt') == item['sourceUpdatedAt'] and prior_item.get('title') == item['title'] and prior_item.get('contentHash') and prior_item.get('bodyState') == 'ready':
                    item['contentHash'] = prior_item['contentHash']; item['bodyState'] = 'ready'
                else:
                    detail = fetcher(source['base']+'board/'+source['alias']+'/article/'+meta['id'])
                    body = detail.get('article', {}).get('content', {})
                    if isinstance(body, dict):
                        body = body.get('body') or body.get('contents') or body.get('html') or body.get('content')
                    if not isinstance(body, str) or not text(body):
                        raise ValueError('invalid patch body')
                    item['contentHash'] = fingerprint(item['title'], body); item['bodyState'] = 'ready'
            items.append(reviewed(item, reviews))
        # Keep earlier records, including previous hash-bound reviews. Never erase them on an outage.
        incoming = {x['id'] for x in items}
        items += [reviewed(dict(x),reviews) for x in prior.get('items',[]) if x['id'] not in incoming]
        return dict(id=source['id'], region=source['region'], kind=source['kind'], status='ready',
                    checkedAt=now, lastSuccessAt=now, error=None, fromCache=False, items=items[:24])
    except (HTTPError, OSError, ValueError, KeyError, TypeError) as exc:
        return dict(id=source['id'], region=source['region'], kind=source['kind'], status='unavailable',
                    checkedAt=now, lastSuccessAt=prior.get('lastSuccessAt'), error=type(exc).__name__,
                    fromCache=bool(prior.get('items')), items=[reviewed(dict(x),reviews) for x in prior.get('items',[])])

def run():
    target = ROOT/'data/news.json'
    previous = json.loads(target.read_text()) if target.exists() else {'sources': []}
    reviews = json.loads((ROOT/'data/patch-reviews.json').read_text())
    old = {x['id']:x for x in previous.get('sources',[])}
    now = stamp()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda source: collect_source(source,old,reviews,now), SOURCES))
    current = dict(schema=1, checkedAt=now, pollMinutes=60, sources=results)
    target.parent.mkdir(exist_ok=True)
    temporary = target.with_suffix('.tmp')
    temporary.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
    temporary.replace(target)
    failures = [x['id'] for x in results if x['status'] != 'ready']
    print(json.dumps({'checkedAt':now,'articles':sum(len(x['items']) for x in results),'unavailable':failures},ensure_ascii=False))
    return bool(failures)

if __name__ == '__main__':
    sys.exit(int(run()))

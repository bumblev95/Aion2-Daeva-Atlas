#!/usr/bin/env python3
"""Review limited public numeric summaries. Never access private fight APIs.

Builds use this frozen review without network access. Recollection is an explicit
editorial operation; changed markup, scopes or missing classes fail closed.
"""
import argparse
import hashlib
import json
import re
from datetime import date, datetime, timezone, timedelta
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CLASSES = {'Gladiator': 'gladiator', 'Templar': 'templar', 'Assassin': 'assassin',
           'Ranger': 'ranger', 'Sorcerer': 'sorcerer', 'Elementalist': 'spiritmaster',
           'Cleric': 'cleric', 'Chanter': 'chanter'}
SOURCES = [
    ('global-balance', 'https://aionflex.gg/meta/classes?region=global&window=30d', 'balance', 'GLOBAL'),
    ('kr-balance', 'https://aionflex.gg/meta/classes?region=kr&window=30d', 'balance', 'KR'),
    ('turgen', 'https://aionflex.gg/rankings/boss/2301721-willful-turgen?region=kr', 'record', 'KR'),
    ('griosa', 'https://aionflex.gg/rankings/boss/2301722-forbidden-hexbeast-griosa?region=kr', 'record', 'KR'),
    ('basilus', 'https://aionflex.gg/rankings/boss/2301723-basilus-the-false?region=kr', 'record', 'KR'),
]
BOSSES = {'turgen': ('2301721', 'Willful Turgen', '의지의 투르겐'),
          'griosa': ('2301722', 'Forbidden Hexbeast Griosa', '금기의 마수 그리오사'),
          'basilus': ('2301723', 'Basilus the False', '위악의 바실루스')}
KO_CLASSES = dict(zip(('검성', '수호성', '살성', '궁성', '마도성', '정령성', '치유성', '호법성'), CLASSES.values()))

class Node:
    def __init__(self, tag='', attrs=(), parent=None):
        self.tag, self.attrs, self.parent = tag, dict(attrs), parent
        self.children = []

    def text(self):
        return ' '.join(' '.join(c.text() if isinstance(c, Node) else c
                                for c in self.children).split())

    def find(self, tag):
        result = []
        for child in self.children:
            if isinstance(child, Node):
                if child.tag == tag: result.append(child)
                result.extend(child.find(tag))
        return result

class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node(); self.current = self.root
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current); self.current.children.append(node)
        if tag not in {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
                       'link', 'meta', 'param', 'source', 'track', 'wbr'}:
            self.current = node

    def handle_startendtag(self, tag, attrs):
        self.current.children.append(Node(tag, attrs, self.current))

    def handle_endtag(self, tag):
        node = self.current
        while node.parent is not None:
            if node.tag == tag:
                self.current = node.parent; return
            node = node.parent

    def handle_data(self, text): self.current.children.append(text)

def number(text):
    if text == '—' or text.startswith('<'): return None
    if not re.fullmatch(r'[\d,]+', text): raise ValueError(f'Unexpected count: {text}')
    return int(text.replace(',', ''))

def rounded_dps(text):
    match = re.fullmatch(r'(\d+(?:\.\d+)?)([KM]?)/s', text)
    if not match: raise ValueError(f'Unrecognized public DPS: {text}')
    amount, suffix = match.groups(); scale = {'': 1, 'K': 1000, 'M': 1000000}[suffix]
    decimals = len(amount.split('.')[1]) if '.' in amount else 0
    return dict(publishedDps=text, value=float(Decimal(amount) * scale),
                resolution=float(Decimal(scale) / (10 ** decimals)))

def korean_dps(text):
    match = re.fullmatch(r'(\d+(?:\.\d+)?)만', text)
    if not match: raise ValueError('Unrecognized report DPS')
    amount = match.group(1)
    decimals = len(amount.split('.')[1]) if '.' in amount else 0
    return dict(publishedDps=text, value=float(Decimal(amount) * 10000),
                resolution=float(Decimal(10000) / 10 ** decimals))

def parse_report(source, start, kind):
    root = Document(source).root
    headings = root.find('h1')
    start_date = date.fromisoformat(start); end_date = start_date + timedelta(days=7)
    short = f'{start_date.month}.{start_date.day}'
    if len(headings) != 1 or headings[0].text() != f'{short} 주간 직업별 DPS 리포트':
        raise ValueError('Weekly report identity changed')
    text = root.text()
    if '같은 보스를 잡은 기록끼리 전투력 1당 DPS' not in text:
        raise ValueError('Weekly index definition changed')
    tables = root.find('table')
    if len(tables) != 5: raise ValueError('Weekly report layout changed')
    def cells(table):
        return [[x.text() for x in tr.children if isinstance(x, Node) and x.tag in {'td', 'th'}]
                for tr in table.find('tbody')[0].find('tr')]
    counts = {KO_CLASSES[x[0]]: number(x[1]) for x in cells(tables[0]) if x[0] in KO_CLASSES}
    rows = []
    if kind == 'weekly':
        headers = tables[1].find('thead')[0].find('th')
        columns = [i for i, node in enumerate(headers) if node.text().split(' ')[0] == short]
        if len(columns) != 1: raise ValueError('Current weekly index column missing')
        for x in cells(tables[1]):
            if x[0] not in KO_CLASSES: continue
            cell = x[columns[0]]
            value = None if cell in {'—', '–'} else float(cell)
            rows.append(dict(classId=KO_CLASSES[x[0]], value=value, resolution=.01,
                             sampleCount=counts[KO_CLASSES[x[0]]]))
        band = None
    else:
        for x in cells(tables[2]):
            if x[0] not in KO_CLASSES: continue
            if len(x) != 3: raise ValueError('Matched CP columns changed')
            rows.append(dict(classId=KO_CLASSES[x[0]], sampleCount=number(x[1]), **korean_dps(x[2])))
        match = re.search(r'같은 전투력끼리 \(([^)]+)\)', text)
        if not match: raise ValueError('Matched CP range missing')
        band = match.group(1)
    return dict(rows=rows, sourceAsOf=None, commonBand=band, sourceWithheld=False,
                periodStart=start, periodEnd=end_date.isoformat(),
                provisional='진행 중인 주입니다' in text,
                region='UNSPECIFIED', regionVerified=False,
                en='JaMeter weekly comparison', ko='JaMeter 주간 비교')

def parse(source, kind, region):
    document = Document(source); mains = document.root.find('main')
    if len(mains) != 1: raise ValueError('Expected one public main section')
    main = mains[0]; text = main.text(); tables = main.find('table')
    if not re.search(r'\bregion\s+' + ('Global' if region == 'GLOBAL' else r'(?:🇰🇷\s*)?KR') + r'\b', text):
        raise ValueError('Source region differs from requested scope')
    if kind == 'balance':
        if 'window Last 30 days' not in text: raise ValueError('Source window changed')
        table = next((x for x in tables if x.find('thead') and
                      x.find('thead')[0].text().startswith('Class Typical Top end')), None)
        if table is None: raise ValueError('Public class-balance table missing')
        rows = []
        for tr in table.find('tbody')[0].find('tr'):
            cells = [c for c in tr.children if isinstance(c, Node) and c.tag in {'td', 'th'}]
            if len(cells) != 11: raise ValueError('Class-balance columns changed')
            links = cells[0].find('a'); name = links[0].text() if links else ''
            if name not in CLASSES: continue
            typical, top = number(cells[1].text()), number(cells[2].text())
            rows.append(dict(classId=CLASSES[name], value=typical, topEnd=top, resolution=1,
                             characterWeeks=number(cells[4].text()), parses=number(cells[5].text()),
                             characters=number(cells[6].text()), uploaders=number(cells[7].text()),
                             bosses=number(cells[8].text())))
        common = re.search(r'Compared over ([^.]+)\.', text)
        stamp = re.search(r'Coverage as of (\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC', text)
        if not stamp: raise ValueError('Source coverage time missing')
        return dict(rows=rows, sourceAsOf=stamp.group(1).replace(' ', 'T') + ':00Z',
                    commonBand=common.group(1) if common else None,
                    sourceWithheld='No Combat-Power band is held by every class' in text)
    if 'window All-Time' not in text: raise ValueError('Record window changed')
    rows = []
    for table in tables:
        header = table.find('thead')
        if not header or header[0].text() != '# Character Server DPS Tier': continue
        panel = table.parent.parent
        anchors = [x for x in panel.find('span') if x.attrs.get('id', '').startswith('class-')]
        if len(anchors) != 1: raise ValueError('Public class record panel changed')
        name = anchors[0].attrs['id'][6:]
        if name not in CLASSES: continue
        count = re.search(r'^' + re.escape(name) + r' (\d+) parses?\b', panel.text())
        if not count: raise ValueError('Published record count missing')
        best = table.find('tbody')[0].find('tr')[0]
        cells = [x for x in best.children if isinstance(x, Node) and x.tag == 'td']
        if len(cells) != 5 or cells[0].text() != '1': raise ValueError('Record table changed')
        rows.append(dict(classId=CLASSES[name], publishedRecords=int(count.group(1)),
                         **rounded_dps(cells[3].text())))
    return dict(rows=rows, sourceAsOf=None, commonBand=None, sourceWithheld=False)

def review(reviewed_at, cache=None):
    date.fromisoformat(reviewed_at)
    datasets = []
    for ident, url, kind, region in SOURCES:
        file = Path(cache) / f'{ident}.html' if cache else None
        if file and file.exists(): raw = file.read_bytes()
        else:
            with urlopen(Request(url, headers={'User-Agent': 'PLAYER-CODEX public source review'}), timeout=30) as response:
                if response.url != url: raise ValueError('Unexpected source redirect')
                raw = response.read(3 * 1024 * 1024)
            if file:
                file.parent.mkdir(parents=True, exist_ok=True); file.write_bytes(raw)
        data = parse(raw.decode('utf-8'), kind, region)
        if len(data['rows']) != 8 or {x['classId'] for x in data['rows']} != set(CLASSES.values()):
            raise ValueError(f'{ident}: incomplete or duplicate class coverage; review before publishing')
        dataset = dict(id=ident, kind=kind, publisher='AionFlex', region=region, regionVerified=True,
                       window='30d' if kind == 'balance' else 'all-time',
                       source=url, sourceHtmlSha256=hashlib.sha256(raw).hexdigest(),
                       metric='normalized-index' if kind == 'balance' else 'published-record-dps',
                       patchId=None, sameEquipment=False, rawFightTotalsAvailable=False, **data)
        if kind == 'record':
            boss, en, ko = BOSSES[ident]
            if en not in Document(raw.decode('utf-8')).root.find('h1')[0].text():
                raise ValueError('Boss identity changed')
            dataset.update(bossId=boss, en=en, ko=ko, instance='DaevaCitadel', difficulty='hard')
        datasets.append(dataset)
    for name, start, kind in [('jameter-current', '2026-10-07', 'weekly'),
                              ('jameter-complete', '2026-09-30', 'band')]:
        url = f'https://jameter.net/report/week/{start}'
        file = Path(cache) / f'{name}.html' if cache else None
        if file and file.exists(): raw = file.read_bytes()
        else:
            with urlopen(Request(url, headers={'User-Agent': 'PLAYER-CODEX public source review'}), timeout=30) as response:
                if response.url != url: raise ValueError('Unexpected report redirect')
                raw = response.read(3 * 1024 * 1024)
            if file:
                file.parent.mkdir(parents=True, exist_ok=True); file.write_bytes(raw)
        data = parse_report(raw.decode('utf-8'), start, kind)
        if len(data['rows']) != 8 or {x['classId'] for x in data['rows']} != set(CLASSES.values()):
            raise ValueError('Weekly report has incomplete launch-class coverage')
        datasets.append(dict(id=name, kind=kind, publisher='JaMeter', window='source-week', source=url,
                             sourceHtmlSha256=hashlib.sha256(raw).hexdigest(),
                             metric='boss-cp-ratio-index' if kind == 'weekly' else 'cp-band-median-dps',
                             patchId=None, sameEquipment=False, rawFightTotalsAvailable=False, **data))
    return dict(schema=1, kind='reviewed-public-combat-summaries', reviewedAt=reviewed_at,
                collectedAt=datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z'),
                publishers=['AionFlex', 'JaMeter'], methodologySource='https://aionflex.gg/meta/methodology',
                launchClassCount=8, datasets=datasets)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviewed-at', required=True)
    parser.add_argument('--cache', type=Path)
    args = parser.parse_args()
    result = review(args.reviewed_at, args.cache)
    (ROOT / 'data/dps-observations.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print('Reviewed public summaries: regional comparisons, KR boss records and weekly CP comparisons. No private APIs or player identities stored.')

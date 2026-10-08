#!/usr/bin/env python3
"""Publication checks: generated links, language pairs, SEO and inert monetization."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import xml.etree.ElementTree as ET
import measurement
ROOT=Path(__file__).parent
OUT=ROOT/'docs';cfg=json.loads((ROOT/'site.json').read_text())
measurement.validate(cfg)
base=urlparse(cfg['url']).path.rstrip('/')+'/'
errors=[];checked=0
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.ids=set();self.jsons=[];self.collect=False;self.raw=''
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.tags.append((tag,a))
  if 'id'in a:
   if a['id'] in self.ids:errors.append('duplicate id '+a['id'])
   self.ids.add(a['id'])
  if tag=='script' and a.get('type') in ['application/ld+json','application/json']:self.collect=True;self.raw=''
 def handle_data(self,data):
  if self.collect:self.raw+=data
 def handle_endtag(self,tag):
  if tag=='script' and self.collect:self.jsons.append(self.raw);self.collect=False
for f in OUT.rglob('*.html'):
 if f.name==cfg.get('search_console',{}).get('verification_file'):
  if f.read_text()!='google-site-verification: '+f.name:errors.append('Invalid Google verification file')
  continue
 checked+=1;s=f.read_text();p=Parser();p.feed(s)
 hs=[a for tag,a in p.tags if tag=='h1']
 if len(hs)!=1:errors.append(f'{f}: expected one h1')
 for raw in p.jsons:
  try:json.loads(raw)
  except Exception as e:errors.append(f'{f}: invalid JSON {e}')
 for tag,a in p.tags:
  u=a.get('href') or a.get('src')
  if not u:continue
  if u.startswith('#'):
   if u[1:] and u[1:] not in p.ids:errors.append(f'{f}: missing anchor {u}')
  if u.startswith(base):
   local=unquote(urlparse(u).path[len(base):]);dest=OUT/local
   if u.split('?')[0].split('#')[0].endswith('/'):dest=dest/'index.html'
   if not dest.exists():errors.append(f'{f}: missing {u}')
  if tag=='a' and not (u.startswith(('https://',base,'#'))):errors.append(f'{f}: invalid link {u}')
 if f.name!='404.html':
  langs={a.get('hreflang') for tag,a in p.tags if tag=='link' and a.get('rel')=='alternate'}
  if langs!={'en','ko','x-default'}:errors.append(f'{f}: language alternates missing')
  if not any(tag=='link'and a.get('rel')=='canonical' for tag,a in p.tags):errors.append(f'{f}: canonical missing')
 if not cfg['adsense']['enabled'] and 'pagead2.googlesyndication.com' in s:errors.append(f'{f}: unexpected ad request')
 if 'ca-pub-0000' in s:errors.append(f'{f}: placeholder publisher')
 if f.name!='404.html':
  if cfg['adsense']['publisher_id'] and not any(tag=='meta' and a.get('name')=='google-adsense-account' and a.get('content')==cfg['adsense']['publisher_id'] for tag,a in p.tags):errors.append(f'{f}: publisher verification missing')
  analytics_enabled=bool(cfg.get('analytics',{}).get('enabled'))
  if ('id="pc-analytics-config"' in s)!=analytics_enabled:errors.append(f'{f}: analytics state mismatch')
  if analytics_enabled and not all(x in s for x in ['data-analytics-accept','data-analytics-decline','data-analytics-settings']):errors.append(f'{f}: analytics preferences missing')
ET.parse(OUT/'sitemap.xml')
idx=json.loads((OUT/'search-index.json').read_text())
for item in idx:
 if not (OUT/item['path']/'index.html').exists():errors.append('Search entry is broken: '+item['path'])
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS: {checked} HTML documents; internal links, anchors, language pairs, JSON, sitemap, verification and measurement state checked.')

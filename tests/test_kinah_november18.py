"""Keep the NA currency amendment scoped, visible and tied to its evidence."""
import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

import guidebrowse
import progression

ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'
ID = '6afd5b00ebccad0e4b5bad8b'
HASH = 'f4f6e5541d26a74131f6b84001379bcd5e366270558dce78b22a2657341f0d8e'


class KinahNovember18Test(unittest.TestCase):
    def test_official_fact_stays_bound_to_na_review(self):
        review = json.loads((ROOT / 'data/patch-reviews.json').read_text())[ID]
        self.assertEqual(review['contentHash'], HASH)
        news = json.loads((ROOT / 'data/news.json').read_text())
        source = next(s for s in news['sources'] if any(i['id'] == ID for i in s['items']))
        self.assertEqual((source['id'], source['region']), ('na-update', 'NA'))
        fact = next(c for c in review['changes']
                    if c['subject']['en'] == 'Field-monster Kina becomes bound')
        self.assertIn('1,000,000', fact['after']['en'])
        self.assertIn('Bound Kina', fact['after']['en'])
        self.assertEqual(progression.SOURCES['kinah-na-nov18'][0], review['sourceUrl'])

    def test_bilingual_notice_survives_reader_and_all_tabs(self):
        for lang, tokens in (
            ('en', ('NA · November 18, 2026', 'all field monsters', '1,000,000',
                    'not a promised payout', 'Per-character or per-account',
                    'reset time', 'share the counter', 'after reaching the cap',
                    'Market sales are included or exempt', 'No KR rule',
                    'enhancement cost label', 'settlement currency')),
            ('ko', ('북미 · 2026년 11월 18일', '모든 필드 몬스터', '1,000,000',
                    '보장 지급액이 아닙니다', '캐릭터·계정 단위',
                    '초기화 시각', '카운터 공유 여부', '한도 도달 후 동작',
                    '거래소 판매가 포함·제외', '한국 서버 규칙',
                    '강화 비용의 화폐 표시', '정산 화폐')),
        ):
            with self.subTest(lang=lang):
                rendered = progression.render('kinah-farming', lang, BASE)
                parts = guidebrowse.Fragments(rendered)
                notice = parts.get('kinah-na-patch')
                for token in tokens:
                    self.assertIn(token, notice)
                self.assertEqual(rendered.count('id="kinah-na-patch"'), 1)
                # The amendment is outside collapsible tabs, so wallet/Market
                # deep links cannot hide the current regional rule.
                a, b = parts.ids['kinah-na-patch']
                for panel in ('plan', 'wallet', 'market'):
                    start, end = parts.ids['reader-kinah-farming-' + panel]
                    self.assertTrue(b <= start or a >= end)
                self.assertIn(ID, notice)
                self.assertIn('growth-source-kinah-na-nov18', rendered)

    def test_old_reward_arithmetic_and_sales_routes_are_preserved(self):
        for lang in ('en', 'ko'):
            rendered = progression.render('kinah-farming', lang, BASE)
            parts = guidebrowse.Fragments(rendered)
            fixed = parts.get('kinah-fixed')
            market = parts.get('kinah-market')
            for token in (('50,000', '250,000', '300,000', '15,000', '550,000')
                          if lang == 'en' else ('5만', '25만', '30만', '1만 5천', '55만')):
                self.assertIn(token, fixed)
            self.assertIn('2026-10-12' if lang == 'en' else '2026.10.12', fixed)
            self.assertIn('not been reverified' if lang == 'en' else '재검증하지 않았습니다', fixed)
            for item in ('Wrathful Mind', 'Wrathful Will', 'Wrathful Ego',
                         'Ruby Powder', 'Yggdrasil Paper'):
                self.assertIn(item, market)
            self.assertIn('No live prices or measured Kinah-per-hour'
                          if lang == 'en' else '시간당 수급량을 측정한 자료는 없습니다', market)
        self.assertEqual(progression.REVIEWED, '2026-10-12')
        self.assertEqual(progression.KINAH_NA_REVIEWED, '2026-11-18')

    def test_built_bilingual_pages_and_dates_match_scoped_amendment(self):
        sitemap = ET.parse(ROOT / 'docs/sitemap.xml')
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        dates = {n.find('s:loc', ns).text: n.find('s:lastmod', ns).text
                 for n in sitemap.findall('s:url', ns)}
        for prefix in ('', 'ko/'):
            for slug in ('pet-growth', 'gear-targets', 'dungeon-rewards', 'kinah-farming'):
                relative = prefix + 'guides/' + slug + '/'
                html = (ROOT / 'docs' / relative / 'index.html').read_text()
                current = slug == 'kinah-farming'
                self.assertEqual('id="kinah-na-patch"' in html, current)
                self.assertEqual(dates['https://bumblev95.github.io/Aion2-Daeva-Atlas/' + relative],
                                 '2026-11-18' if current else '2026-10-12')
                if current:
                    self.assertIn('"dateModified": "2026-11-18"', html)


if __name__ == '__main__':
    unittest.main()

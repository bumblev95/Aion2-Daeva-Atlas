"""Currency guidance must survive topic extraction and keep evidence boundaries."""
import json
from pathlib import Path
import unittest
from xml.etree import ElementTree as ET

import guidebrowse
import progression


ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'


class KinahGuideRegressionTest(unittest.TestCase):
    def test_patch_claims_match_reviewed_na_source(self):
        review = json.loads((ROOT / 'data/patch-reviews.json').read_text())[progression.KINAH_PATCH_ID]
        change = next(c for c in review['changes'] if c['subject']['en'] == 'Field-monster Kina becomes bound')
        self.assertIn('1,000,000', change['after']['en'])
        self.assertIn('Bound', change['after']['en'])
        for lang in ('en', 'ko'):
            html = progression.render('kinah-farming', lang, BASE)
            notice = guidebrowse.Fragments(html).get('kinah-na-update')
            for token in ('1,000,000', '2026', progression.KINAH_PATCH_ID):
                self.assertIn(token, notice)
            self.assertIn('북미 전용' if lang == 'ko' else 'NA only', notice)
            self.assertIn('보장 수입이 아닙니다' if lang == 'ko' else 'not a guaranteed payout', notice)
            self.assertLess(html.index('id="kinah-na-update"'), html.index('data-reader-tabs'))

    def test_uncertainty_and_market_routes_remain_separate(self):
        cases = {
            'en': ('account versus character', 'reset time', 'share this cap',
                   'other loot at the cap', 'debit priority', 'does not establish KR rules',
                   'does not announce that all material-sale routes are removed',
                   'completed sales of tradable surplus', 'not sale stock',
                   'No live prices or measured Kinah-per-hour'),
            'ko': ('계정·캐릭터별', '초기화 시각', '한도 합산 여부', '다른 전리품',
                   '차감 우선순위', '한국 서버 규칙으로 적용하지 않습니다',
                   '재료 판매 경로 전체의 폐지를 공지한 것이 아닙니다',
                   '실제 판매대금', '판매용 재고에 넣지 마세요', '시간당 수급량을 측정한 자료는 없습니다'),
        }
        for lang, qualifiers in cases.items():
            html = progression.render('kinah-farming', lang, BASE)
            for text in qualifiers:
                self.assertIn(text, html)
            market = guidebrowse.Fragments(html).get('kinah-market')
            for material in ('Wrathful Mind', 'Wrathful Will', 'Wrathful Ego', 'Ruby Powder', 'Yggdrasil Paper'):
                self.assertIn(material, market)

    def test_legacy_conditional_rewards_not_replaced_with_new_income(self):
        en = progression.render('kinah-farming', 'en', BASE)
        for text in ('50,000', '250,000', '300,000', '10,000 score', '15,000',
                     '550,000', 'Shared Daily Dungeon pool', '2026-10-12',
                     'not revalidated in game', 'Do not add 1,000,000 field Kinah'):
            self.assertIn(text, en)
        self.assertNotIn('1,550,000', en)

    def test_wallet_is_a_budget_assumption_not_na_spending_verification(self):
        for lang in ('en', 'ko'):
            html = progression.render('kinah-farming', lang, BASE)
            wallet = guidebrowse.Fragments(html).get('kinah-types')
            self.assertIn('가정합니다' if lang == 'ko' else 'calculator assumes bound-first', wallet)
            self.assertIn('인게임 검증 대기' if lang == 'ko' else 'need in-game verification', wallet)

    def test_generated_languages_dates_links_and_scoped_metadata(self):
        sitemap = ET.parse(ROOT / 'docs/sitemap.xml')
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        dates = {n.find('s:loc', ns).text: n.find('s:lastmod', ns).text
                 for n in sitemap.findall('s:url', ns)}
        for lang in ('en', 'ko'):
            prefix = 'ko/' if lang == 'ko' else ''
            page = ROOT / 'docs' / prefix / 'guides/kinah-farming/index.html'
            html = page.read_text()
            self.assertIn('id="kinah-na-update"', html)
            self.assertIn('id="growth-source-kinah-na-patch"', html)
            self.assertIn(progression.KINAH_PATCH, html)
            self.assertIn('"dateModified": "2026-11-18"', html)
            self.assertEqual(dates['https://bumblev95.github.io/Aion2-Daeva-Atlas/'+prefix+'guides/kinah-farming/'], '2026-11-18')
        for slug in ('pet-growth', 'gear-targets', 'dungeon-rewards'):
            self.assertEqual(progression.reviewed_on(slug), '2026-10-12')


if __name__ == '__main__':
    unittest.main()

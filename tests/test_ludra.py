"""Keep the NA beginner route discoverable and separate from unverified combat."""
import json
from pathlib import Path
import unittest
from xml.etree import ElementTree

import advancedguides
import ludra

ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'


class LudraGuideTest(unittest.TestCase):
    def test_review_matches_current_official_snapshot(self):
        evidence = json.loads((ROOT / 'research/ludra-guide-review-2026-11-18.json').read_text())
        review = json.loads((ROOT / 'data/patch-reviews.json').read_text())[evidence['official']['articleId']]
        self.assertEqual(evidence['official']['contentHash'], review['contentHash'])
        self.assertFalse(evidence['naCombatVerified'])
        self.assertEqual(ludra.ENTRY_LEVELS, {'easy': 2800, 'normal': 2800, 'hard': 3000})
        self.assertEqual(ludra.TIME_LIMIT_MINUTES, 120)
        self.assertEqual(ludra.VOUCHERS, {'normal_to_bracelet': 6, 'hard_to_bracelet': 3, 'normal_to_hard': 2})
        self.assertEqual(ludra.WEAPON_CHEST, {'kina': 5000000, 'easy_vouchers': 4, 'normal_vouchers': 2, 'hard_vouchers': 1})
        self.assertEqual(ludra.GEAR_COMBINED_DROP_PERCENT, 15)

    def test_bilingual_scope_cost_and_combat_boundaries(self):
        for lang in ('en', 'ko'):
            html = advancedguides.render('na-ludra', lang, BASE)
            for key in ('entry', 'prepare', 'combat', 'rewards', 'materials'):
                self.assertIn('id="ludra-'+key+'"', html)
            for token in ('2,800', '3,000', '15%', '5,000,000', '100%', 'COMBO', '×6', '×4', '×3', '×2'):
                self.assertIn(token, html)
            self.assertIn('6afd5b00ebccad0e4b5bad8b', html)
            self.assertIn('2026-11-18', html)
            self.assertIn('100%', html)
            self.assertNotIn('data-animation=', html)
            self.assertNotIn('data-raid-lesson=', html)
            self.assertNotIn('<iframe', html)
        en = advancedguides.render('na-ludra', 'en', BASE)
        self.assertIn('unlimited personal revives', en)
        for qualifier in ('not yet verified',
                          '6 vouchers does not mean 6 clears',
                          'not a verified boss-enrage timer', 'no COMBO (Great Success)',
                          'not a Ludra drop recipe', 'Normal/Hard resurrection'):
            self.assertIn(qualifier, en)
        self.assertIn('30% to 100%', en)
        ko = advancedguides.render('na-ludra', 'ko', BASE)
        for qualifier in ('아직 검증되지 않음', '6회 클리어를 뜻하지 않습니다',
                          '결과물 귀속', '개인 부활 무제한'):
            self.assertIn(qualifier, ko)

    def test_generated_journey_search_and_review_date(self):
        search = json.loads((ROOT / 'docs/search-index.json').read_text())
        for lang, prefix in (('en', ''), ('ko', 'ko/')):
            route = prefix+'guides/na-ludra/'
            page = (ROOT / 'docs' / route / 'index.html').read_text()
            self.assertIn(BASE+prefix+'guides/endgame-crafts/', page)
            self.assertIn('2026-11-04', page)
            for gateway in ('dungeons/', 'endgame/', 'guides/gear-targets/',
                            'guides/dungeon-rewards/', 'guides/endgame-crafts/'):
                self.assertIn(BASE+route, (ROOT / 'docs' / prefix / gateway / 'index.html').read_text())
            self.assertTrue(any(item['path'] == route and item['lang'] == lang for item in search))
        ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = ElementTree.parse(ROOT / 'docs/sitemap.xml').getroot()
        dates = {item.find('s:loc', ns).text: item.find('s:lastmod', ns).text for item in urls}
        for prefix in ('', 'ko/'):
            self.assertEqual(dates['https://bumblev95.github.io'+BASE+prefix+'guides/na-ludra/'], ludra.REVIEWED)


if __name__ == '__main__':
    unittest.main()

import json
import unittest
from pathlib import Path

import advancedguides
import ludra
import progression


ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'
ID = '6afd5b00ebccad0e4b5bad8b'
HASH = 'f4f6e5541d26a74131f6b84001379bcd5e366270558dce78b22a2657341f0d8e'


def load(path):
    return json.loads((ROOT / path).read_text())


class November18NorthAmericaRegressionTest(unittest.TestCase):
    def test_review_is_hash_bound_highlights_and_na_only(self):
        review = load('data/patch-reviews.json')[ID]
        self.assertEqual(review['contentHash'], HASH)
        self.assertEqual(review['detail']['coverage'], 'highlights')
        self.assertTrue(review['classScopeReviewed'])
        self.assertFalse(any(change['classId'] != 'all' for change in review['changes']))
        self.assertTrue(any(change['subject']['en'] == 'Ludra attack patterns'
                            and change['type'] == 'fix' for change in review['changes']))
        self.assertTrue(any(change['subject']['en'] == 'Field-monster Kina becomes bound'
                            and change['type'] == 'system' for change in review['changes']))
        self.assertIn('United States and Canada', review['detail']['sections'][0]['notes'][1]['en'])

    def test_news_publishes_review_without_kr_copy(self):
        news = load('data/news.json')
        item = next(item for source in news['sources'] for item in source['items'] if item['id'] == ID)
        self.assertEqual(item['region'], 'NA')
        self.assertEqual(item['contentHash'], HASH)
        self.assertEqual(item['reviewState'], 'reviewed')
        self.assertFalse(any(item['id'] == ID for source in news['sources'] if source['region'] == 'KR'
                             for item in source['items']))

    def test_current_ludra_guide_uses_official_easy_and_morph_values(self):
        self.assertEqual(ludra.ENTRY_LEVELS['easy'], 2800)
        self.assertEqual(ludra.GEAR_COMBINED_DROP_PERCENT, 15)
        self.assertEqual(ludra.WEAPON_CHEST['kina'], 5_000_000)
        for lang in ('en', 'ko'):
            guide = advancedguides.render('na-ludra', lang, BASE)
            growth = progression.ludra_entry(progression.View(lang, BASE))
            self.assertIn(ID, guide)
            self.assertIn(ID, growth)
            self.assertIn('15%', guide)
            self.assertIn('5,000,000', guide)
        self.assertIn('unlimited personal revives', advancedguides.render('na-ludra', 'en', BASE))

    def test_coverage_lists_direct_checks_without_class_or_dps_change(self):
        audit = next(item for item in load('data/coverage-audit.json')['items']
                     if item['id'] == 'na-20261118-ludra-easy-rewards-bound-kina')
        self.assertEqual(audit['status'], 'needs-evidence')
        self.assertIn('/guides/na-ludra/', audit['finding']['en'])
        self.assertIn('No class input', audit['finding']['en'])


if __name__ == '__main__':
    unittest.main()

import json
import unittest
from pathlib import Path

import advancedguides
import ludra
import progression


ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'


class November11UpdateRegressionTest(unittest.TestCase):
    def setUp(self):
        self.reviews = json.loads((ROOT / 'data/patch-reviews.json').read_text())

    def test_na_patch_is_hash_bound_and_region_scoped(self):
        patch = self.reviews['6af42a1affaccc00c265785f']
        self.assertEqual(
            patch['contentHash'],
            '690c4181690c1b17dfd69334143b898a3b65a66f15a851748895684fc7831372',
        )
        self.assertEqual(patch['detail']['coverage'], 'highlights')
        self.assertTrue(patch['classScopeReviewed'])
        self.assertTrue(any(c['type'] == 'fix' and 'Zikel' in c['subject']['en']
                            for c in patch['changes']))
        self.assertFalse(any(c['classId'] != 'all' for c in patch['changes']))

    def test_ludra_current_public_guides_use_two_hour_limit(self):
        self.assertEqual(ludra.TIME_LIMIT_MINUTES, 120)
        for lang in ('en', 'ko'):
            guide = advancedguides.render('na-ludra', lang, BASE)
            growth = progression.ludra_entry(progression.View(lang, BASE))
            self.assertIn('6af42a1affaccc00c265785f', guide)
            self.assertIn('6af42a1affaccc00c265785f', growth)
            self.assertIn('120', guide)
        self.assertIn('30% to 100%', advancedguides.render('na-ludra', 'en', BASE))

    def test_kr_revision_rebinds_review_and_official_inputs(self):
        expected = '4d5f58baf153aef3b5bce5cf476d84fb9c6c553db963fd2f386732853dfd1f89'
        patch = self.reviews['6af370b8577e8c01355e047b']
        self.assertEqual(patch['contentHash'], expected)
        correction = next(c for c in patch['changes'] if c['subject']['en'] == 'November 11 source corrections')
        self.assertIn('Lower only', correction['after']['en'])
        snapshot = json.loads((ROOT / 'data/skill-snapshot.json').read_text())
        kr = next(item for item in snapshot['officialOverrides'] if item['region'] == 'KR')
        self.assertEqual(kr['sourceHash'], expected)
        self.assertEqual(kr['effectiveAt'], '2026-11-11')


if __name__ == '__main__':
    unittest.main()

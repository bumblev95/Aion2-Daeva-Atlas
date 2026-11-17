import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = '6afcab38ebccad0e4b5bad5f'
HASH = 'e085599c9e7b9b3a76c9125f6f743c04df579af032a5b7bc0ee6b32b7f17b8a1'


def load(path):
    return json.loads((ROOT / path).read_text())


class November18UpdateRegressionTest(unittest.TestCase):
    def test_review_is_hash_bound_highlights_and_region_scoped(self):
        review = load('data/patch-reviews.json')[ID]
        self.assertEqual(review['contentHash'], HASH)
        self.assertEqual(review['detail']['coverage'], 'highlights')
        self.assertTrue(review['classScopeReviewed'])
        self.assertEqual(
            {c['classId'] for c in review['changes'] if c['classId'] != 'all'},
            {'gladiator', 'templar', 'assassin', 'brawler', 'chanter', 'ranger', 'cleric'},
        )
        self.assertTrue(any(c['type'] == 'nerf' and c['classId'] == 'assassin'
                            for c in review['changes']))
        self.assertTrue(any(c['type'] == 'fix' and c['subject']['en'].startswith('Boss targeting')
                            for c in review['changes']))
        self.assertTrue(any(c['type'] == 'system' and c['subject']['en'].startswith('KR PvP weapon')
                            for c in review['changes']))
        self.assertIn('KR only', review['detail']['sections'][0]['notes'][1]['en'])

    def test_news_publishes_review_without_source_outage_or_na_copy(self):
        news = load('data/news.json')
        self.assertTrue(all(s['status'] == 'ready' for s in news['sources']))
        item = next(x for s in news['sources'] for x in s['items'] if x['id'] == ID)
        self.assertEqual(item['region'], 'KR')
        self.assertEqual(item['reviewState'], 'reviewed')
        self.assertEqual(item['contentHash'], HASH)
        self.assertEqual(item['reviewedAt'], '2026-11-17T20:13:14Z')
        self.assertFalse(any(x['id'] == ID for s in news['sources'] if s['region'] == 'NA'
                             for x in s['items']))

    def test_explicit_inputs_are_kr_only_and_global_base_is_preserved(self):
        snapshot = load('data/skill-snapshot.json')
        override = next(x for x in snapshot['officialOverrides'] if x.get('sourceHash') == HASH)
        self.assertEqual(override['region'], 'KR')
        self.assertEqual(override['effectiveAt'], '2026-11-18')
        self.assertEqual(override['skills']['ruinous-blow']['cooldownSeconds'], 40)
        self.assertEqual(override['skills']['judgment']['cooldownSeconds'], 7)
        self.assertEqual(override['skills']['insignia-explosion']['cooldownSeconds'], 5)
        self.assertEqual(override['skills']['burst-arrow']['pveDamageChangePercent'], 100)
        self.assertEqual(override['skills']['condemnation']['pveDamageChangePercent'], 15)
        self.assertIn('brawler', override['unmatchedSkillInputs'])
        base = {x['id']: x for x in load('data/skills.json')}
        self.assertEqual(base['ruinous-blow']['cooldown'], '45s')
        self.assertEqual(base['judgment']['cooldown'], '5s')
        self.assertEqual(base['insignia-explosion']['cooldown'], '10s')

    def test_coverage_keeps_global_transfer_guide_separate(self):
        audit = next(x for x in load('data/coverage-audit.json')['items']
                     if x['id'] == 'kr-20261118-classes-bosses-trust-transfer')
        self.assertEqual(audit['status'], 'needs-evidence')
        self.assertIn('/guides/server-transfer/', audit['finding']['en'])
        self.assertIn('not reopened', audit['finding']['en'])
        self.assertIn('글로벌', audit['finding']['ko'])


if __name__ == '__main__':
    unittest.main()

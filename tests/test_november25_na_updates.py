import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID = '6b0695806b68bef8bae9148e'
HASH = '52b79b0084ca326cec94b2daed2ed0fe1871e64d3c347a289831400a81d09efb'


def load(path):
    return json.loads((ROOT / path).read_text())


class November25NAUpdateRegressionTest(unittest.TestCase):
    def test_review_is_hash_bound_highlights_and_class_complete(self):
        review = load('data/patch-reviews.json')[ID]
        self.assertEqual(review['contentHash'], HASH)
        self.assertEqual(review['detail']['coverage'], 'highlights')
        self.assertTrue(review['classScopeReviewed'])
        self.assertEqual(
            {row['classId'] for row in review['changes'] if row['classId'] != 'all'},
            {'templar', 'ranger', 'chanter', 'spiritmaster'},
        )
        self.assertTrue(any(row['type'] == 'nerf' and row['classId'] == 'chanter'
                            for row in review['changes']))
        self.assertTrue(any(row['type'] == 'fix' and 'targeting' in row['subject']['en'].lower()
                            for row in review['changes']))
        self.assertIn('United States and Canada', review['summary']['en'])
        self.assertIn('does not claim a complete', review['detail']['sections'][-1]['notes'][-1]['en'])
        facility = next(row for row in review['changes']
                        if row['subject']['en'] == 'Corroded Decontamination Facility')
        self.assertIn('consumes no Odyle Energy', facility['description']['en'])
        self.assertIn('no cube-opening energy cost', facility['impact']['en'].lower())

    def test_news_publishes_na_review_and_preserves_notice_failure(self):
        news = load('data/news.json')
        source = next(s for s in news['sources'] if s['id'] == 'na-update')
        item = next(x for x in source['items'] if x['id'] == ID)
        self.assertEqual(source['region'], 'NA')
        self.assertEqual(item['reviewState'], 'reviewed')
        self.assertEqual(item['contentHash'], HASH)
        notice = next(s for s in news['sources'] if s['id'] == 'na-notice')
        self.assertIn(notice['status'], {'ready', 'unavailable'})
        if notice['status'] == 'unavailable':
            self.assertTrue(notice['fromCache'])
            self.assertTrue(notice['items'])

    def test_exact_na_inputs_are_separate_and_history_is_preserved(self):
        snapshot = load('data/skill-snapshot.json')
        override = next(row for row in snapshot['officialOverrides'] if row.get('sourceHash') == HASH)
        self.assertEqual(override['region'], 'NA')
        self.assertEqual(override['skills']['marking-shot']['specialization1PerfectChancePercent'], 10)
        self.assertEqual(override['skills']['bow-of-blessing']['cooldownSeconds'], 90)
        self.assertEqual(override['skills']['cold-shock']['specialization4EarthTremorMaxStacks'], 1)
        self.assertFalse(override['skills']['element-unification']['stackable'])
        self.assertTrue(override['skills']['judgment']['exactCoefficientPendingClientVerification'])
        base = {row['id']: row for row in load('data/skills.json')}
        self.assertEqual(base['bow-of-blessing']['cooldown'], '120s')

    def test_na_stigma_guide_does_not_rewrite_kr_snapshot(self):
        source = (ROOT / 'advancedguides.py').read_text()
        self.assertIn("('Wind Breeze Merchants','산들바람 상인')", source)
        self.assertIn("'50', ('Per character','캐릭터별')", source)
        self.assertIn("('Shugo Festival','슈고 페스타'), '300', '35', '10,500'", source)
        self.assertIn("('Nightmare','악몽'), '1,500', '35', '52,500'", source)
        skillbook = (ROOT / 'skillbook.py').read_text()
        self.assertIn('NA supports up to five equipped Stigma skills', skillbook)

    def test_audit_records_exact_targets_and_direct_verification(self):
        audit = next(row for row in load('data/coverage-audit.json')['items']
                     if row['id'] == 'na-20261125-classes-stigma-market-economy')
        self.assertEqual(audit['status'], 'needs-evidence')
        self.assertEqual(audit['sources'][0]['contentHash'], HASH)
        self.assertIn('/guides/stigma-growth/', audit['finding']['en'])
        self.assertIn('/guides/abyss-outland/', audit['finding']['en'])
        self.assertIn('Bargott', audit['finding']['en'])
        self.assertIn('final tier', audit['finding']['en'])


if __name__ == '__main__':
    unittest.main()

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTICLE_ID = '6b047f20d65afc4bb5d63c4e'
CONTENT_HASH = '1c0376ae86f8d23f6f3cc09d6f1df41ebae540c0a21ca14ed0b98ec9dd0580fb'


class November21WorldMarketTest(unittest.TestCase):
    def test_general_notice_stays_an_official_link_card(self):
        news = json.loads((ROOT / 'data/news.json').read_text())
        source = next(x for x in news['sources'] if x['id'] == 'na-notice')
        item = next(x for x in source['items'] if x['id'] == ARTICLE_ID)
        self.assertEqual(item['reviewState'], 'official')
        self.assertIsNone(item['contentHash'])
        self.assertEqual(item['summary'], {})
        self.assertEqual(item['changes'], [])

    def test_review_is_hash_bound_and_keeps_regions_separate(self):
        review = json.loads((ROOT / 'research/na-world-market-review-2026-11-21.json').read_text())
        self.assertEqual(review['article']['contentHash'], CONTENT_HASH)
        self.assertEqual(review['article']['reviewState'], 'official')
        self.assertEqual(review['classification'], 'system')
        self.assertEqual(review['classIds'], [])
        self.assertIn('Applying this NA announcement to Korea', review['notSupported'])
        self.assertIn('Applying the 20% World sales tax to Server Market or Server Exchange', review['notSupported'])

    def test_guide_records_only_announced_world_rules(self):
        source = (ROOT / 'progression.py').read_text()
        for fact in (
            'same faction and region',
            'existing Server Market and Server Exchange stay available',
            'World sales have a 20% tax',
            '10 for the World Market and 10 for the World Exchange (Quna)',
            'The 20% figure is for World sales',
            'No live prices or measured Kinah-per-hour',
        ):
            self.assertIn(fact, source)
        self.assertIn("'kinah-na-world-market'", source)
        self.assertIn('World trading · direct checks pending', source)

    def test_coverage_audit_names_exact_public_targets(self):
        audit = json.loads((ROOT / 'data/coverage-audit.json').read_text())
        item = next(x for x in audit['items'] if x['id'] == 'na-20261125-world-market-exchange')
        self.assertEqual(item['status'], 'needs-evidence')
        self.assertEqual(item['sources'][0]['contentHash'], CONTENT_HASH)
        finding = item['finding']['en']
        self.assertIn('P1 growth/system', finding)
        self.assertIn('No KR application', finding)


if __name__ == '__main__':
    unittest.main()

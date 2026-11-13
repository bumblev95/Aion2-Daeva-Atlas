import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = '6af65300b0586e28ebc4aaa6'
HASH = 'c64838c40eb37629e56b435267a81778b9864ae9acafec8b1dc9652fd97d2402'


def load(name):
    return json.loads((ROOT / name).read_text())


def feed_item(article_id):
    news = load('data/news.json')
    return next(
        item
        for source in news['sources']
        for item in source['items']
        if item['id'] == article_id
    )


class November13UpdateTests(unittest.TestCase):
    def test_patch_review_is_bound_to_current_source(self):
        item = feed_item(ARTICLE)
        review = load('data/patch-reviews.json')[ARTICLE]
        self.assertEqual(item['contentHash'], HASH)
        self.assertEqual(review['contentHash'], HASH)
        self.assertEqual(item['reviewState'], 'reviewed')
        self.assertEqual(item['reviewedAt'], '2026-11-13T08:40:09Z')
        self.assertEqual(review['detail']['coverage'], 'highlights')
        self.assertTrue(review['classScopeReviewed'])
        self.assertEqual(
            {change['classId'] for change in review['changes'] if change['classId'] != 'all'},
            {'gladiator', 'templar', 'assassin', 'brawler', 'ranger', 'sorcerer', 'spiritmaster'},
        )

    def test_kr_numeric_inputs_are_separate_and_dated(self):
        snapshot = load('data/skill-snapshot.json')
        override = next(
            row for row in snapshot['officialOverrides']
            if row.get('sourceHash') == HASH
        )
        self.assertEqual(override['region'], 'KR')
        self.assertEqual(override['effectiveAt'], '2026-11-13')
        self.assertEqual(override['skills']['ruinous-blow']['cooldownSeconds'], 60)
        self.assertEqual(override['skills']['insignia-explosion']['cooldownSeconds'], 3)
        self.assertEqual(override['skills']['element-enhancement']['cooldownSeconds'], 45)
        self.assertEqual(override['skills']['summon-fire-spirit']['cooldownSeconds'], 10)
        self.assertIn('brawler', override['unmatchedSkillInputs'])
        self.assertIn('not applied', override['calculationState'])

    def test_maintenance_notices_remain_official_cards(self):
        upcoming = feed_item('6af6c5d8cd0c2d6575c81301')
        completed = feed_item('6af644f067841a056945a937')
        for item in (upcoming, completed):
            self.assertEqual(item['kind'], 'news')
            self.assertEqual(item['reviewState'], 'official')
            self.assertIsNone(item['contentHash'])
            self.assertEqual(item['summary'], {})
        self.assertIn('(완료)', completed['title'])

    def test_audit_keeps_fact_analysis_and_direct_checks(self):
        audit = load('data/coverage-audit.json')
        row = next(item for item in audit['items'] if item['id'] == 'kr-20261113-class-rotation-and-dungeon-fixes')
        self.assertEqual(row['status'], 'needs-evidence')
        self.assertIn('/guides/dungeon-rewards/', row['finding']['en'])
        self.assertIn('직접', row['finding']['ko'])
        self.assertIn('no arbitrary DPS percentage', row['finding']['en'])


if __name__ == '__main__':
    unittest.main()

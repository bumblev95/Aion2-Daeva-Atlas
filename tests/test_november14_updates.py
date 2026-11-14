import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTICLE = '6af77a507d773f10fbeb07f9'
HASH = 'ff91677012c8b856d45261aaea7217b092ce2b66f993122061c1251ebb061ccf'


def load(path):
    return json.loads((ROOT / path).read_text())


def feed_item(article_id):
    return next(
        item
        for source in load('data/news.json')['sources']
        for item in source['items']
        if item['id'] == article_id
    )


class November14UpdateTests(unittest.TestCase):
    def test_new_patch_is_reviewed_and_hash_bound(self):
        item = feed_item(ARTICLE)
        review = load('data/patch-reviews.json')[ARTICLE]
        self.assertEqual(item['contentHash'], HASH)
        self.assertEqual(review['contentHash'], HASH)
        self.assertEqual(item['reviewState'], 'reviewed')
        self.assertEqual(item['reviewedAt'], '2026-11-14T08:38:50Z')
        self.assertEqual(review['detail']['coverage'], 'highlights')
        self.assertTrue(review['classScopeReviewed'])
        self.assertEqual(
            {change['classId'] for change in review['changes'] if change['classId'] != 'all'},
            {'gladiator', 'templar', 'assassin', 'brawler', 'chanter',
             'ranger', 'sorcerer', 'cleric', 'spiritmaster'},
        )

    def test_kr_inputs_are_separate_dated_and_do_not_rewrite_global_base(self):
        snapshot = load('data/skill-snapshot.json')
        override = next(row for row in snapshot['officialOverrides'] if row.get('sourceHash') == HASH)
        self.assertEqual(override['region'], 'KR')
        self.assertEqual(override['effectiveAt'], '2026-11-14')
        self.assertEqual(override['skills']['wave-armor']['cooldownSeconds'], 30)
        self.assertEqual(override['skills']['insignia-explosion']['cooldownSeconds'], 7)
        self.assertEqual(override['skills']['element-enhancement']['cooldownSeconds'], 60)
        self.assertEqual(override['skills']['condemnation']['pveDamageChangePercent'], 15)
        self.assertIn('brawler-rage', override['unmatchedSkillInputs'])
        self.assertIn('not applied', override['calculationState'])

        base = {skill['id']: skill for skill in load('data/skills.json')}
        self.assertEqual(base['wave-armor']['cooldown'], '60s')
        self.assertEqual(base['element-enhancement']['cooldown'], '60s')

    def test_pvp_and_bug_fix_claims_remain_scoped(self):
        review = load('data/patch-reviews.json')[ARTICLE]
        pvp = next(change for change in review['changes'] if change['subject']['en'] == 'Shackle conditions and resource flow')
        arena = next(c for c in review['changes'] if c['subject']['en'] == 'Arena and Abyss healing reduction')
        bug = next(c for c in review['changes'] if c['type'] == 'fix' and c['classId'] == 'assassin')
        self.assertIn('KR PvP rule', arena['impact']['en'])
        self.assertIn('No arbitrary DPS percentage', bug['impact']['en'])
        self.assertIn('MP', pvp['description']['en'])

    def test_audit_names_exact_paths_and_direct_checks(self):
        row = next(item for item in load('data/coverage-audit.json')['items']
                   if item['id'] == 'kr-20261114-class-pvp-sanctuary')
        self.assertEqual(row['status'], 'needs-evidence')
        self.assertIn('/guides/kr-bitan/', row['finding']['en'])
        self.assertIn('확인해야', row['finding']['ko'])
        self.assertIn('no NA PvE application', row['finding']['en'])


if __name__ == '__main__':
    unittest.main()

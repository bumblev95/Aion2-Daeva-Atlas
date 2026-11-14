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
        self.news = json.loads((ROOT / 'data/news.json').read_text())

    def test_na_patch_is_hash_bound_and_region_scoped(self):
        patch = self.reviews['6af42a1affaccc00c265785f']
        self.assertEqual(
            patch['contentHash'],
            '269fabc0325bf5904bd3c315225984162abce57d0111e2487a6aca9309626d42',
        )
        self.assertEqual(patch['detail']['coverage'], 'highlights')
        self.assertTrue(patch['classScopeReviewed'])
        self.assertTrue(any(c['type'] == 'fix' and 'Zikel' in c['subject']['en']
                            for c in patch['changes']))
        self.assertFalse(any(c['classId'] != 'all' for c in patch['changes']))
        scope_note = patch['detail']['sections'][0]['notes'][0]['en']
        self.assertIn('revised at 09:52:19 UTC', scope_note)
        self.assertIn('269fabc0', scope_note)

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
        expected = 'a8d3b7503679b6c0f9b921c0ab6b2d1d1e2d95fc2468c07c3a933ce49f011d7a'
        patch = self.reviews['6af370b8577e8c01355e047b']
        self.assertEqual(patch['contentHash'], expected)
        correction = next(c for c in patch['changes'] if c['subject']['en'] == 'November 11 source corrections')
        self.assertIn('Liberated White Night Ring', correction['before']['en'])
        self.assertIn('deletes Liberated White Night Ring', correction['description']['en'])
        snapshot = json.loads((ROOT / 'data/skill-snapshot.json').read_text())
        kr = next(item for item in snapshot['officialOverrides'] if item['region'] == 'KR')
        self.assertEqual(kr['sourceHash'], expected)
        self.assertEqual(kr['effectiveAt'], '2026-11-11')

    def test_kr_emergency_maintenance_inputs_are_separate_and_source_bound(self):
        snapshot = json.loads((ROOT / 'data/skill-snapshot.json').read_text())
        hotfix = next(
            item for item in snapshot['officialOverrides']
            if item.get('source', '').endswith('6af3ea98553a6c1fba041803')
        )
        self.assertEqual(
            hotfix['sourceHash'],
            'f47a6238d4d9fc089a947c2731106be9171992f7dbf6ac80b53000f06947b441',
        )
        self.assertEqual(hotfix['region'], 'KR')
        self.assertEqual(hotfix['skills']['rending-blow']['mpCost'], 50)
        self.assertEqual(hotfix['skills']['ruinous-blow']['frenzyDurationSeconds'], 9)
        self.assertEqual(
            hotfix['skills']['keen-strike']['specializations']['4']['afterCooldownReductionSkill'],
            'aerial-snare',
        )
        self.assertIn('weapon-block', hotfix['unmatchedSkillInputs'])

        evidence = json.loads(
            (ROOT / 'research/kr-emergency-maintenance-review-2026-11-12.json').read_text()
        )
        self.assertEqual(evidence['sources'][0]['contentHash'], hotfix['sourceHash'])
        known_issues = next(
            item for item in evidence['sources']
            if item['id'] == '6af3d328066b033317c02bd3'
        )
        self.assertEqual(
            known_issues['contentHash'],
            '47f5777952e644c71617854b65c6b9333b2c98d345a0517f01bb4975d9947915',
        )
        self.assertTrue(any(
            c['subject']['en'] == 'Atiel Earth Collapse stagger in parties'
            and c['type'] == 'fix'
            for c in evidence['changes']
        ))
        self.assertTrue(any(c['type'] == 'fix' and c['classId'] == 'chanter'
                            for c in evidence['changes']))
        self.assertTrue(all(c['region'] == 'KR' for c in evidence['changes']))

    def test_substantive_general_notices_remain_official_link_cards(self):
        notices = {
            item['id']: item
            for source in self.news['sources']
            for item in source['items']
            if item['id'] in {
                '6af3ea98553a6c1fba041803',
                '6af3d328066b033317c02bd3',
                '6af443dacd0c2d6575c812d6',
                '6af32952bcc8631989223db1',
                '6af644f067841a056945a937',
            }
        }
        self.assertEqual(len(notices), 5)
        for item in notices.values():
            self.assertEqual(item['kind'], 'news')
            self.assertEqual(item['reviewState'], 'official')
            self.assertEqual(item['summary'], {})
            self.assertIsNone(item['contentHash'])
        self.assertEqual(
            notices['6af32952bcc8631989223db1']['sourceUpdatedAt'],
            '2026-11-12T01:14:23.930Z',
        )
        self.assertEqual(
            notices['6af3d328066b033317c02bd3']['sourceUpdatedAt'],
            '2026-11-14T00:42:08.322Z',
        )


if __name__ == '__main__':
    unittest.main()

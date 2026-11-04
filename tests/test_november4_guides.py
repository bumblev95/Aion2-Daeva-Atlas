import json
import unittest
from pathlib import Path

import advancedguides
import outland
import progression
import routines


ROOT = Path(__file__).resolve().parents[1]


class November4GuideRegressionTest(unittest.TestCase):
    def test_outland_uses_revised_slots_and_marks_unmeasured_rules(self):
        for lang in ('en', 'ko'):
            page = outland.render(lang, '/Aion2-Daeva-Atlas/')
            self.assertIn('11:10–13:40', page)
            self.assertIn('20:10–23:40', page)
            self.assertNotIn('<li>11:00–13:30</li>', page)
            self.assertIn('6aea36386cfe4756db5b9115', page)
        ko = outland.render('ko', '/Aion2-Daeva-Atlas/')
        for fact in ('30초 늦게', '바람길 위치', '은신이 풀립니다', '무적 시간은 줄지만'):
            self.assertIn(fact, ko)
        self.assertIn('미검증', ko)

    def test_patch_hash_and_deltras_warning_stay_source_bound(self):
        reviews = json.loads((ROOT / 'data/patch-reviews.json').read_text())
        patch = reviews['6aea36386cfe4756db5b9115']
        self.assertEqual(
            patch['contentHash'],
            'cebda46d11d4269ba4580d86b21ddbe4df8c2aef30733f559a5ad6b4a3dbed2e',
        )
        self.assertEqual(patch['detail']['coverage'], 'highlights')
        self.assertTrue(any(change['type'] == 'fix' and '델트라스' in change['subject']['ko']
                            for change in patch['changes']))
        ko = advancedguides.render('kr-bitan', 'ko', '/Aion2-Daeva-Atlas/')
        self.assertIn('충격 해제를 확정 탈출 수단으로 계획하지 말고', ko)
        self.assertIn('6aea36386cfe4756db5b9115', ko)

    def test_na_patch_hash_and_current_ludra_terms_stay_source_bound(self):
        reviews = json.loads((ROOT / 'data/patch-reviews.json').read_text())
        patch = reviews['6aead0e86cfe4756db5b913f']
        self.assertEqual(
            patch['contentHash'],
            '13ac8cfab9ce63fd6fbb7823bebeb6d6ec434b4594ea98e94abdfdf2b096e536',
        )
        self.assertEqual(patch['detail']['coverage'], 'highlights')
        en = advancedguides.render('endgame-crafts', 'en', '/Aion2-Daeva-Atlas/')
        self.assertIn('4 Odyle Energy per account per day', en)
        self.assertNotIn('2 Odyle Energy per character per day', en)
        self.assertIn('6 Normal vouchers or 3 Hard vouchers', en)

    def test_na_routine_schedule_and_deltras_hotfix_are_regional(self):
        activities = {item['id']: item for item in routines.ACTIVITIES}
        self.assertIn('Thursday / Saturday · siege 21:00, bosses 21:30',
                      activities['na-artifact']['cadence'][0])
        self.assertIn('Argo 10:30 / 22:30', activities['na-field-boss']['cadence'][0])
        self.assertIn('3 hours / week', activities['na-outer']['cadence'][0])
        self.assertNotIn('Before launch', progression.ludra_entry(
            progression.View('en', '/Aion2-Daeva-Atlas/')))

        reviews = json.loads((ROOT / 'data/patch-reviews.json').read_text())
        hotfix = reviews['6aea9be081a1f241964f2d12']
        self.assertEqual(hotfix['kind'], 'patch')
        self.assertEqual(hotfix['source'], 'kr-notice')
        self.assertFalse(any('before' in change or 'after' in change
                             for change in hotfix['changes'] if change['type'] == 'fix'))


if __name__ == '__main__':
    unittest.main()

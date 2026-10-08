"""Source/generator boundaries: no unverified value becomes a free skill."""
import copy
import unittest
from unittest.mock import patch
import liveops
import dpsrules

class CatalogTests(unittest.TestCase):
    def test_coverage_and_known_gates(self):
        db = liveops.catalog()
        self.assertEqual(sum(c['directCount'] for c in db['classes']), 26)
        self.assertEqual(sum(len(c['conditionAudit']) for c in db['classes']), 96)
        all_skills = {s['id']:s for c in db['classes'] for s in c['candidates']}
        self.assertEqual(all_skills['burst-arrow']['requires'], ['slow', 'root'])
        self.assertEqual(all_skills['condemnation']['requires'], ['chain-of-torment'])
        self.assertEqual(all_skills['blaze']['requires'], ['fire-mark'])
        self.assertEqual(all_skills['elemental-fusion']['elementCost'], 4)
        self.assertEqual(all_skills['heart-gore']['requires'], ['critical-trigger'])
        self.assertEqual(all_skills['drill-dart']['requires'], [])

    def test_helpers_have_no_invented_damage(self):
        helpers = [s for c in liveops.catalog()['classes'] for s in c['skills'] if s.get('setupOnly')]
        self.assertEqual({s['id'] for s in helpers}, {'shield-smite','impactful-crush','chain-of-torment'})
        self.assertTrue(all(s['flat'] == s['coefficient'] == 0 for s in helpers))

    def test_dash_costs_and_changed_snapshot_fail_closed(self):
        db = liveops.catalog()
        skills = {s['id']:s for c in db['classes'] for s in c['candidates']}
        self.assertIsNone(skills['burst-arrow']['mpCost'])
        self.assertEqual(skills['shield-smite']['mpCost'], 100)
        original = liveops.load
        def stale(name):
            data = copy.deepcopy(original(name))
            if name == 'dps-resources.json':data['skillSourceHash'] = 'stale'
            return data
        with patch.object(liveops, 'load', side_effect=stale):
            changed = liveops.catalog()
            self.assertTrue(all(s['mpCost'] is None for c in changed['classes'] for s in c['candidates']))

    def test_bilingual_condition_help_and_mp_controls(self):
        for lang in ('en', 'ko'):
            page = liveops.dps(lang, '/Aion2-Daeva-Atlas/')
            for control in ('data-state-windows','data-condition-audit','data-dps-add-source',
                            'data-param="resourceMode"','data-param="elementEvents"'):
                self.assertIn(control,page)
        self.assertIn('빠진 조건을 항상 활성 상태로 가정하지 않습니다',liveops.dps('ko','/'))
        self.assertIn('Missing conditions are never assumed',liveops.dps('en','/'))

    def test_changed_skill_snapshot_requires_condition_review(self):
        self.assertTrue(liveops.catalog()['conditionsVerified'])
        with patch.object(dpsrules, 'REVIEWED_SKILL_HASH', 'outdated'):
            self.assertFalse(liveops.catalog()['conditionsVerified'])

if __name__ == '__main__':unittest.main()

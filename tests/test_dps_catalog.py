"""Source/generator boundaries: no unverified value becomes a free skill."""
import copy
import unittest
from unittest.mock import patch
import liveops
import dpsrules
import dpsmath

class CatalogTests(unittest.TestCase):
    def test_coverage_and_known_gates(self):
        db = liveops.catalog()
        self.assertEqual(sum(c['directCount'] for c in db['classes']), 72)
        self.assertEqual(sum(len(c['conditionAudit']) for c in db['classes']), 96)
        all_skills = {s['id']:s for c in db['classes'] for s in c['candidates']}
        self.assertEqual(all_skills['burst-arrow']['requires'], ['slow', 'root'])
        self.assertEqual(all_skills['condemnation']['requires'], ['chain-of-torment'])
        self.assertEqual(all_skills['blaze']['requires'], ['fire-mark'])
        self.assertEqual(all_skills['elemental-fusion']['elementCost'], 4)
        self.assertEqual(all_skills['heart-gore']['requires'], ['critical-trigger'])
        self.assertEqual(all_skills['drill-dart']['requires'], [])
        self.assertEqual(all_skills['heart-gore']['mpGain'],100)
        self.assertEqual(all_skills['drill-dart']['mpGain'],0)

    def test_secondary_effects_do_not_erase_direct_damage(self):
        skills = {s['id']:s for c in liveops.catalog()['classes'] for s in c['skills']}
        for sid, flat, coefficient in [('shield-smite',173,175.8),('impactful-crush',224,218.4),
                                       ('chain-of-torment',138,151.8),('heart-gore',111,122),
                                       ('tremor-crush',260,102),('ruinous-blow',2387,689),
                                       ('savage-roar',68,83.5),('drill-dart',112,115.5)]:
            self.assertEqual((skills[sid]['flat'],skills[sid]['coefficient']), (flat,coefficient))
        self.assertEqual(len(skills['chain-of-torment']['periodic']),1)

    def test_complete_damage_audit_and_unresolved_models(self):
        db=liveops.catalog()
        audits=[s for c in db['classes'] for s in c['damageAudit']]
        self.assertEqual(len(audits),96)
        self.assertEqual(sum(x['status']=='direct' for x in audits),72)
        self.assertEqual(sum(x['status']=='non-offensive' for x in audits),13)
        self.assertEqual(sum(x['status']=='input-required' for x in audits),7)
        self.assertEqual(sum(x['status']=='charge-input-required' for x in audits),4)
        skills={s['id']:s for c in db['classes'] for s in c['candidates']}
        for sid in dpsmath.UNRESOLVED:
            self.assertTrue(skills[sid]['damageInputRequired'])
            self.assertFalse(skills[sid]['damageConfirmed'])
            self.assertEqual(skills[sid]['flat'],0)
        self.assertEqual(skills['punishment']['charge']['maximum']['coefficient'],1291.5)
        for sid in dpsmath.CHARGES:
            self.assertFalse(skills[sid]['chargeConfirmed'])
            self.assertFalse(skills[sid]['charge']['durationVerified'])
        self.assertEqual([x['stacks']for x in skills['insignia-explosion']['insigniaDamage']],list(range(6)))
        self.assertEqual(skills['insignia-explosion']['insigniaDamage'][5]['flat'],1061)
        self.assertEqual(sum(len(s['periodic'])for s in skills.values()),4)

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
                            'data-param="resourceMode"','data-param="elementEvents"',
                            'data-param="periodicMode"','data-param="insigniaMode"'):
                self.assertIn(control,page)
        self.assertIn('빠진 조건을 항상 활성 상태로 가정하지 않습니다',liveops.dps('ko','/'))
        self.assertIn('Missing conditions are never assumed',liveops.dps('en','/'))

    def test_changed_skill_snapshot_requires_condition_review(self):
        self.assertTrue(liveops.catalog()['conditionsVerified'])
        with patch.object(dpsrules, 'REVIEWED_SKILL_HASH', 'outdated'):
            self.assertFalse(liveops.catalog()['conditionsVerified'])
        with patch.object(dpsmath, 'REVIEWED_SKILL_HASH', 'outdated'):
            self.assertFalse(liveops.catalog()['damageVerified'])

if __name__ == '__main__':unittest.main()

"""Source/generator boundaries: no unverified value becomes a free skill."""
import copy
import unittest
from unittest.mock import patch
import liveops
import dpsrules
import dpsmath
import dpslevels
import dpsranking
import tempfile
import json
from pathlib import Path
from scripts.check_news_diff import allowed_path

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

    def test_bilingual_backend_results_without_visitor_calculation(self):
        for lang in ('en', 'ko'):
            page = liveops.dps(lang, '/Aion2-Daeva-Atlas/')
            self.assertIn('data-computed-by="backend"',page)
            self.assertEqual(page.count('data-rank-class='),24)
            for tag in ('<form','<input','<select','dps-engine.js','assets/dps.js'):
                self.assertNotIn(tag,page)
            self.assertIn('dps-rankings.csv',page)
        self.assertIn('한국 패치 순위로 확정할 수 없습니다',liveops.dps('ko','/'))
        self.assertIn('sum full fight seconds',liveops.dps('en','/'))

    def test_exact_level_terms_and_periodic_scaling(self):
        skills={s['id']:s for c in liveops.catalog(skill_level=20)['classes'] for s in c['candidates']}
        self.assertEqual((skills['keen-strike']['flat'],skills['keen-strike']['coefficient']),(602,43))
        self.assertEqual((skills['drill-dart']['flat'],skills['drill-dart']['coefficient']),(1491,115.5))
        self.assertEqual((skills['drill-dart']['periodic'][0]['flat'],skills['drill-dart']['periodic'][0]['coefficient']),(581,45))
        self.assertEqual(skills['insignia-explosion']['insigniaDamage'][5]['flat'],4889)
        self.assertEqual(skills['defiance']['cooldown'],41)
        self.assertTrue(all(s['skillLevel']==20 for s in skills.values()))
        self.assertTrue(all(a['skillLevel']==20 for c in liveops.catalog(skill_level=20)['classes'] for a in c['damageAudit']))
        with self.assertRaisesRegex(ValueError,'No reviewed tooltip'):
            liveops.catalog(skill_level=19)
        source=next(s for s in liveops.load('skills.json') if s['id']=='drill-dart')
        bad=dpsmath.damage(source);bad['flat']+=1
        with self.assertRaisesRegex(ValueError,'Base terms changed'):
            dpslevels.model(source,bad,20)

    def test_damage_audit_does_not_mutate_shared_rules(self):
        original=copy.deepcopy(dpsmath.UNRESOLVED)
        skills=[s for s in liveops.load('skills.json') if s['id'] in dpsmath.UNRESOLVED]
        baseline=[dpsmath.damage(s) for s in skills]
        for _ in range(3):
            self.assertEqual([dpsmath.damage(s) for s in skills],baseline)
        self.assertEqual(dpsmath.UNRESOLVED,original)

    def test_stale_level_snapshot_cannot_publish(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);(root/'data').mkdir()
            (root/'data/skills.json').write_text('[]')
            (root/'data/dps-skill-levels.json').write_text(json.dumps({'skillSourceHash':'outdated'}))
            dpslevels.snapshot.cache_clear()
            try:
                with patch.object(dpslevels,'ROOT',root):
                    with self.assertRaisesRegex(ValueError,'needs review'):
                        dpslevels.snapshot()
            finally:
                dpslevels.snapshot.cache_clear()

    def test_patch_freshness_keeps_regions_and_news_separate(self):
        def feed(region,kind,posted,updated=None):
            return dict(region=region,items=[dict(kind=kind,publishedAt=posted,sourceUpdatedAt=updated)])
        self.assertFalse(dpsranking.needs_patch_review({'sources':[
            feed('KR','patch','2026-10-10'),feed('NA','news','2026-10-10'),feed('NA','patch','2026-10-07')
        ]},'2026-10-09'))
        self.assertTrue(dpsranking.needs_patch_review({'sources':[
            feed('NA','patch','2026-10-07','2026-10-10')
        ]},'2026-10-09'))
        self.assertTrue(allowed_path('docs/ko/tools/dps/index.html'))
        self.assertFalse(allowed_path('data/dps-ranking-model.json'))
        self.assertFalse(allowed_path('data/dps-rankings.json'))

    def test_changed_skill_snapshot_requires_condition_review(self):
        self.assertTrue(liveops.catalog()['conditionsVerified'])
        with patch.object(dpsrules, 'REVIEWED_SKILL_HASH', 'outdated'):
            self.assertFalse(liveops.catalog()['conditionsVerified'])
        with patch.object(dpsmath, 'REVIEWED_SKILL_HASH', 'outdated'):
            self.assertFalse(liveops.catalog()['damageVerified'])

if __name__ == '__main__':unittest.main()

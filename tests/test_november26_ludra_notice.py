import json
import unittest
from pathlib import Path

import advancedguides
import ludra


ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'
NOTICE_ID = '6b079e1563dd78f52230e0fe'


def load(path):
    return json.loads((ROOT / path).read_text())


class November26LudraNoticeRegressionTest(unittest.TestCase):
    def test_general_notice_remains_an_official_link_card(self):
        news = load('data/news.json')
        source = next(row for row in news['sources'] if row['id'] == 'na-notice')
        item = next(row for row in source['items'] if row['id'] == NOTICE_ID)
        self.assertEqual(item['region'], 'NA')
        self.assertEqual(item['kind'], 'news')
        self.assertEqual(item['reviewState'], 'official')
        self.assertIsNone(item['contentHash'])
        self.assertEqual(item['summary'], {})
        self.assertEqual(item['changes'], [])
        self.assertIsNone(item['reviewedAt'])

    def test_na_guides_publish_the_extended_term_bilingually(self):
        for slug in ('na-ludra', 'endgame-crafts'):
            en = advancedguides.render(slug, 'en', BASE)
            ko = advancedguides.render(slug, 'ko', BASE)
            self.assertIn(NOTICE_ID, en)
            self.assertIn(NOTICE_ID, ko)
            self.assertIn('December 15', en)
            self.assertIn('12월 15일', ko)
            self.assertIn('RMT', en)
            self.assertIn('RMT', ko)
            self.assertNotIn('November 24 before maintenance', en)
            self.assertNotIn('11월 24일 점검 전', ko)
        self.assertEqual(ludra.REVIEWED, '2026-11-26')

    def test_audit_separates_official_facts_and_direct_verification(self):
        audit = next(row for row in load('data/coverage-audit.json')['items']
                     if row['id'] == 'na-20261126-ludra-event-extension')
        self.assertEqual(audit['status'], 'needs-evidence')
        self.assertIn('/guides/na-ludra/', audit['finding']['en'])
        self.assertIn('/guides/endgame-crafts/', audit['finding']['en'])
        self.assertIn('Direct verification pending', audit['finding']['en'])
        self.assertIn('직접 검증 대기', audit['finding']['ko'])
        self.assertEqual(audit['sources'][0]['url'].split('articleId=')[-1], NOTICE_ID)


if __name__ == '__main__':
    unittest.main()

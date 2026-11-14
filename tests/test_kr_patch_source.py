import copy
import importlib.util
import unittest
from pathlib import Path

from scripts.collect_updates import fingerprint

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('kr_verify_source', ROOT/'research/kr-20261111/verify_source.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class KrSourceBindingTests(unittest.TestCase):
    def setUp(self):
        # Tiny synthetic publisher-shaped payload, not a copy of NC prose.
        self.payload = {'article': {'contentMeta': {
            'id': '6af370b8577e8c01355e047b', 'title': 'Synthetic source',
            'categoryBoard': {'boardAlias': 'update_ko'},
            'timestamps': {'updatedAt': '2026-11-10T20:09:12.369Z'}},
            'content': {'content': '<p>Synthetic value 7</p>'}}}
        self.review = {'sourceHash': fingerprint('Synthetic source', '<p>Synthetic value 7</p>')}

    def test_unchanged_body(self):
        self.assertEqual(module.verify(self.payload, self.review)['sourceHash'], self.review['sourceHash'])

    def test_changed_value_or_title(self):
        for key in ('body', 'title'):
            payload = copy.deepcopy(self.payload)
            if key == 'body':
                payload['article']['content']['content'] = '<p>Synthetic value 8</p>'
            else:
                payload['article']['contentMeta']['title'] = 'Other source'
            with self.assertRaises(AssertionError):
                module.verify(payload, self.review)

    def test_wrong_identity_or_region(self):
        for key in ('id', 'region'):
            payload = copy.deepcopy(self.payload)
            if key == 'id':
                payload['article']['contentMeta']['id'] = 'other-article'
            else:
                payload['article']['contentMeta']['categoryBoard']['boardAlias'] = 'update_en'
            with self.assertRaises(AssertionError):
                module.verify(payload, self.review)

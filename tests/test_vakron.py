"""Supplement evidence must never upgrade unseen gameplay to verified."""
import copy
from pathlib import Path
import unittest
from unittest.mock import patch
import vakron
from fieldnotes import BOSSES

class VakronTests(unittest.TestCase):
    def test_order_and_bilingual_notes(self):
        vakron.validate()
        self.assertEqual(len(BOSSES),6)
        self.assertEqual(sum(len(b['mechanics']) for b in BOSSES),16)
        for lang in ('en','ko'):
            html=vakron.render(lang,'/Aion2-Daeva-Atlas/')
            self.assertEqual(html.count('data-animation="'),9)
            self.assertEqual(html.count('data-video-verified="false"'),9)
            for lesson in vakron.LESSONS:
                self.assertIn(lesson['note'][lang=='ko'],html)
                self.assertIn('t='+str(lesson['seconds'])+'s',html)
            self.assertNotIn('<iframe',html)
            self.assertNotIn('<video',html)
            self.assertIn('CC BY-SA 4.0',html)

    def test_claims_and_missing_translation_fail_build(self):
        for key in ('video_verified','timing_verified','global_verified'):
            lessons=copy.deepcopy(vakron.LESSONS);lessons[0]['evidence'][key]=True
            with patch.object(vakron,'LESSONS',lessons),self.assertRaises(ValueError):vakron.validate()
        lessons=copy.deepcopy(vakron.LESSONS);lessons[0]['note']=('note','')
        with patch.object(vakron,'LESSONS',lessons),self.assertRaises(ValueError):vakron.validate()

    def test_renderer_loads_before_player_even_with_reduced_motion(self):
        root=Path(__file__).resolve().parents[1]
        for lang in ('','ko/'):
            html=(root/'docs'/lang/'dungeons/vakron-island/index.html').read_text()
            self.assertLess(html.index('assets/vakron.js'),html.index('assets/battle.js'))
            for asset in ('vakron.js','vakron.css'):
                self.assertEqual((root/'assets'/asset).read_bytes(),(root/'docs/assets'/asset).read_bytes())

if __name__=='__main__':unittest.main()

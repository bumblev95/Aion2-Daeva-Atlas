"""Publication regressions for irreversible transfer preparation guidance."""
import json
import unittest
from pathlib import Path
from html.parser import HTMLParser
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import servertransfer as transfer


class Text(HTMLParser):
    def __init__(self, source):
        super().__init__();self.parts=[];self.feed(source)
    def handle_data(self,data):self.parts.append(data)


class TransferGuide(unittest.TestCase):
    def test_bilingual_critical_rules(self):
        for lang in ('en','ko'):
            source=(ROOT/'docs'/('ko' if lang=='ko' else '')/transfer.ROOT/'index.html').read_text()
            text=' '.join(Text(source).parts)
            for token in ('1,000 Quna','2,000 Quna','0 Quna','Genus Insight','CEST/CET','03:30 PDT','20:00–23:00 PDT'):
                self.assertIn(token,text)
            for id in ('checklist','schedule','cost','storage','pets','rewards','transfer-sources'):
                self.assertIn('id="'+id+'"',source)
            self.assertEqual(source.count('type="checkbox"'),7)
            self.assertIn('서버 이전 중단' if lang=='ko' else 'server transfers on hold',text)
            self.assertIn('취소·되돌리기' if lang=='ko' else 'canceled or reversed',text)
            self.assertIn('이전되지 않습니다' if lang=='ko' else 'do not move',text)
            self.assertIn('출발 서버의 Genus Insight는 초기화' if lang=='ko' else 'Origin Genus Insight resets',text)

    def test_discovery_language_and_deep_links(self):
        index=json.loads((ROOT/'docs/search-index.json').read_text())
        for lang in ('en','ko'):
            prefix='ko/' if lang=='ko' else ''
            rows=[x for x in index if x['path']==prefix+transfer.ROOT]
            self.assertEqual({x['anchor'] for x in rows},{'checklist','schedule','cost','storage','pets','rewards'})
            for route in ('','guides/','endgame/','routines/','dungeons/','gear/','guides/pet-growth/','guides/dungeon-rewards/'):
                source=(ROOT/'docs'/prefix/route/'index.html').read_text()
                self.assertIn(prefix+transfer.ROOT,source)
            page=(ROOT/'docs'/prefix/transfer.ROOT/'index.html').read_text()
            self.assertIn('hreflang="ko"',page)
            self.assertIn('hreflang="en"',page)
            self.assertIn(prefix+transfer.ROOT,(ROOT/'docs/sitemap.xml').read_text())

    def test_region_hours_and_evidence(self):
        self.assertEqual(len(transfer.REGIONS),5)
        self.assertEqual(transfer.REGIONS[2][2],'03:00–07:00 / 09:00–13:00')
        self.assertEqual(transfer.REGIONS[4][2],'20:00–+1 00:00 / 02:00–06:00')
        evidence=json.loads((ROOT/'research/server-transfer-review.json').read_text())
        self.assertEqual(evidence['availability'],'paused-by-publisher')
        self.assertEqual(len(evidence['discrepancies']),5)
        self.assertEqual({s['id'] for s in evidence['sources']},{'hold','qa','products','maintenance'})


if __name__=='__main__':unittest.main()

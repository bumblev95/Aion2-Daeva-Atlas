import copy
import json
import unittest
from pathlib import Path
import patchbook
from scripts.collect_updates import reviewed
from scripts.check_news_diff import allowed_path

ROOT=Path(__file__).resolve().parents[1]

class PatchbookTests(unittest.TestCase):
    def setUp(self):
        self.feed=json.loads((ROOT/'data/news.json').read_text())
        self.reviews=json.loads((ROOT/'data/patch-reviews.json').read_text())

    def reviewed_item(self, article_id):
        item=copy.deepcopy(next(x for x in patchbook.patches(self.feed) if x['id']==article_id))
        item['contentHash']=self.reviews[article_id]['contentHash']
        return reviewed(item,self.reviews)

    def test_mixed_changes_are_class_local_not_patch_wide(self):
        item={'changes':[{'classId':'templar','type':'buff'},{'classId':'assassin','type':'nerf'}]}
        groups={g['classId']:g for g in patchbook.class_groups(item)}
        self.assertEqual(groups['templar']['type'],'buff')
        self.assertEqual(groups['assassin']['type'],'nerf')
        item['changes'].append({'classId':'templar','type':'nerf'})
        self.assertEqual(patchbook.class_groups(item)[0]['type'],'adjustment')

    def test_fixes_and_tooltip_edits_are_not_advertised_as_buffs(self):
        self.assertEqual(patchbook.classification([{'type':'fix'}]),'fix')
        self.assertEqual(patchbook.classification([{'type':'tooltip'}]),'tooltip')

    def test_actual_templar_mixed_patch_preserves_both_directions(self):
        item=self.reviewed_item('6a9727b8fa34c1011d627551')
        group=next(g for g in patchbook.class_groups(item) if g['classId']=='templar')
        self.assertEqual(group['type'],'adjustment')
        nerfs={x['subject']['ko']:x for x in group['rows'] if x['type']=='nerf'}
        self.assertIn('연속 난타',nerfs);self.assertIn('응징의 일격',nerfs)
        self.assertEqual(nerfs['연속 난타']['after']['ko'],'기존 피해의 90%')

    def test_full_reviews_cover_all_source_topics_and_tables(self):
        complete={key:value for key,value in self.reviews.items() if value.get('detail',{}).get('coverage')=='complete'}
        self.assertGreaterEqual(len(complete),7)
        for article_id in complete:
            item=self.reviewed_item(article_id)
            with self.subTest(id=article_id):
                self.assertTrue(patchbook.detail_ready(item))
                self.assertEqual(item['contentHash'],self.reviews[item['id']]['contentHash'])
                d=item['detail'];covered={s['sourceSection'].replace('\u200b','') for s in d['sections']}|{'클래스 변경사항'}
                self.assertFalse(set(d['sourceSections'])-covered)
                for section in d['sections']:
                    self.assertTrue(section['notes'])
                    for table in section['tables']:
                        self.assertTrue(table['rows'])
                        self.assertTrue(all(len(row)==len(table['headers']) for row in table['rows']))
                        self.assertNotIn('변경 내용',table['headers'])

    def test_future_unreviewed_patch_keeps_a_working_pending_detail_page(self):
        item=self.reviewed_item('6a9727b8fa34c1011d627551')
        item.update(id='future-patch',contentHash='new-content')
        item=reviewed(item,self.reviews)
        self.assertEqual(item['reviewState'],'pending')
        self.assertFalse(patchbook.detail_ready(item))
        self.assertIn('updates/kr-future-patch/',patchbook.patch_card(item,'ko','/'))
        self.assertIn('공식 원문',patchbook.render_detail(item,'ko','/'))

    def test_source_revision_removes_full_detail_and_class_claims(self):
        item=self.reviewed_item('6a9727b8fa34c1011d627551');item['contentHash']='changed'
        revised=reviewed(item,self.reviews)
        self.assertEqual(revised['detail'],{});self.assertEqual(revised['changes'],[])
        output=patchbook.render_detail(revised,'ko','/Aion2-Daeva-Atlas/')
        self.assertNotIn('class-templar',output);self.assertNotIn('patch-full-section',output)
        self.assertIn('재검토',output)

    def test_compact_card_links_to_local_full_page_without_full_body(self):
        item=self.reviewed_item('6a9727b8fa34c1011d627551')
        card=patchbook.patch_card(item,'ko','/Aion2-Daeva-Atlas/')
        self.assertIn('/ko/'+patchbook.detail_path(item),card)
        self.assertNotIn('patch-fact-table',card);self.assertNotIn('patch-skill-change',card)

    def test_automated_publication_allows_new_detail_pages_but_not_code(self):
        self.assertTrue(allowed_path('docs/ko/updates/kr-new-patch/index.html'))
        self.assertTrue(allowed_path('docs/search-index.json'))
        for path in ['docs/assets/news.js','data/patch-reviews.json','docs/ko/updates/../../skills/index.html','docs/updates/patch.js']:
            self.assertFalse(allowed_path(path),path)

if __name__=='__main__':unittest.main()

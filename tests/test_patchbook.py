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

    def test_oct21_kr_highlights_keep_conditions_and_regional_scope(self):
        item=self.reviewed_item('6ad7c138577e8c01355e006c')
        self.assertEqual(item['region'],'KR')
        self.assertEqual(item['detail']['coverage'],'highlights')
        self.assertTrue(item['classScopeReviewed'])
        self.assertEqual({r['classId'] for r in item['changes']},
            {'all','gladiator','templar','assassin','brawler','chanter','ranger','cleric','spiritmaster','sorcerer'})
        sorcerer=[r for r in item['changes'] if r['classId']=='sorcerer' and r['type']=='fix']
        self.assertEqual(len(sorcerer),4)
        self.assertTrue(all('before' not in r and 'after' not in r for r in sorcerer))
        self.assertTrue(any('누락' in r['description']['ko'] for r in sorcerer))
        self.assertTrue(any('의도하지 않은' in r['description']['ko'] for r in sorcerer))
        corrode=next(r for r in item['changes'] if r['classId']=='spiritmaster')
        self.assertNotIn('before',corrode)
        self.assertIn('75%',corrode['after']['ko'])
        self.assertNotEqual(item['reviewedAt'],item['publishedAt'])
        output=patchbook.render_detail(item,'ko','/Aion2-Daeva-Atlas/')
        self.assertIn('시행 예정',output)
        self.assertIn('인게임 테스트는 수행하지 못했습니다',output)
        self.assertIn('data/maps.json',output)
        item['contentHash']='new-revision'
        revised=reviewed(item,self.reviews)
        self.assertEqual(revised['changes'],[])
        self.assertEqual(revised['detail'],{})

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

    def test_october_14_regions_keep_different_combat_changes(self):
        kr=self.reviewed_item('6ace86b86cfe4756db5b8d81')
        na=self.reviewed_item('6acf20d007b77e214688a7ac')
        kr_groups={g['classId']:g for g in patchbook.class_groups(kr)}
        na_groups={g['classId']:g for g in patchbook.class_groups(na)}
        self.assertEqual(kr_groups['all']['type'],'nerf')
        self.assertEqual(kr_groups['templar']['type'],'adjustment')
        self.assertEqual(na_groups['sorcerer']['type'],'fix')
        self.assertEqual(na_groups['spiritmaster']['type'],'fix')
        self.assertNotIn('brawler',na_groups)
        self.assertFalse(any(x['type']=='nerf' for x in na['changes']))
        for item in (kr,na):
            self.assertTrue(patchbook.detail_ready(item))
            self.assertEqual(patchbook.review_label(item,'en'),'Summary reviewed')
            page=patchbook.render_detail(item,'ko','/')
            self.assertIn('실전 영향',page)
            self.assertIn('이벤트 보상·상품 전체 표는 공식 공지',page)
            self.assertNotIn('전체 항목 검토 완료',page)
            self.assertIn('패치 요약 보기',patchbook.patch_card(item,'ko','/'))

    def test_notice_and_missing_summary_have_honest_states(self):
        notice={'id':'notice','title':'Server notice','kind':'news','region':'NA','url':'https://aion2.plaync.com/','reviewState':'pending'}
        card=patchbook.patch_card(notice,'en','/')
        self.assertIn('Official notice',card)
        self.assertNotIn('Review pending',card)
        self.assertNotIn('editorial review',card)
        notice['kind']='patch'
        self.assertEqual(patchbook.review_label(notice,'ko'),'요약 미등록')

    def test_same_day_hotfix_supersedes_without_rewriting_regular_patch(self):
        regular=self.reviewed_item('6ace86b86cfe4756db5b8d81')
        hotfix=self.reviewed_item('6acf3680263e537d356d1155')
        self.assertIn('0.3초',json.dumps(regular['changes'],ensure_ascii=False))
        self.assertEqual(hotfix['source'],'kr-notice')
        self.assertEqual(hotfix['changes'][0]['before']['en'],'Cooldown reduction: 0.3s')
        self.assertEqual(hotfix['changes'][0]['after']['en'],'Cooldown reduction: 0.1s')
        for lang in ('en','ko'):
            for output in (patchbook.patch_card(regular,lang,'/'),patchbook.render_detail(regular,lang,'/')):
                self.assertIn('patch-followup',output)
                self.assertIn('updates/kr-6acf3680263e537d356d1155/',output)
            self.assertIn('articleId=6acf3680263e537d356d1155',patchbook.render_detail(hotfix,lang,'/'))
        regular['contentHash']='changed'
        self.assertEqual(reviewed(regular,self.reviews)['followups'],[])

if __name__=='__main__':unittest.main()

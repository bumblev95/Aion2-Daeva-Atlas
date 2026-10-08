import unittest
from urllib.error import HTTPError
from scripts.collect_updates import SOURCES, collect_source, reviewed, fingerprint, text

class CollectorTests(unittest.TestCase):
    def setUp(self):
        self.source=SOURCES[0];self.now='2026-10-08T09:00:00Z'
        self.meta={'id':'abc','title':'Update','timestamps':{'postedAt':'2026-10-07T00:00:00Z','updatedAt':'2026-10-07T00:00:00Z'}}
        self.body='<p>Damage changed by 10%.</p>'
        self.hash=fingerprint('Update',self.body)
        self.reviews={'abc':{'contentHash':self.hash,'reviewedAt':self.now,'summary':{'en':'Change summary'},'changes':[{'type':'buff','classId':'sorcerer'}],'classScopeReviewed':True}}
    def response(self,url):
        return {'article':{'content':{'content':self.body}}} if url.endswith('/abc') else {'contentList':[self.meta]}
    def test_success_is_headline_hash_and_review_not_full_article(self):
        result=collect_source(self.source,{},self.reviews,self.now,self.response)
        self.assertEqual(result['status'],'ready');item=result['items'][0]
        self.assertEqual(item['reviewState'],'reviewed');self.assertEqual(item['contentHash'],self.hash)
        self.assertNotIn('body',item);self.assertNotIn('teaser',item)
        self.assertIn('plaync.com',item['url'])
    def test_revision_removes_old_claims(self):
        self.body='<p>Damage changed by 20%.</p>'
        item=collect_source(self.source,{},self.reviews,self.now,self.response)['items'][0]
        self.assertEqual(item['reviewState'],'revised');self.assertEqual(item['changes'],[])
        self.assertEqual(item['summary'],{});self.assertFalse(item['classScopeReviewed'])
    def test_unchanged_patch_does_not_fetch_body_again(self):
        prior=collect_source(self.source,{},self.reviews,self.now,self.response)
        def fetcher(url):
            self.assertNotEqual(url.rsplit('/',1)[-1],'abc')
            return {'contentList':[self.meta]}
        result=collect_source(self.source,{self.source['id']:prior},self.reviews,self.now,fetcher)
        self.assertEqual(result['items'][0]['reviewState'],'reviewed')
    def test_title_change_invalidates_the_cached_hash(self):
        prior=collect_source(self.source,{},self.reviews,self.now,self.response)
        self.meta['title']='Update (revised)'
        item=collect_source(self.source,{self.source['id']:prior},self.reviews,self.now,self.response)['items'][0]
        self.assertEqual(item['reviewState'],'revised')
    def test_outage_keeps_data_and_actual_success_time(self):
        prior=collect_source(self.source,{},self.reviews,self.now,self.response)
        def fetcher(url):raise HTTPError(url,429,'rate limit',{},None)
        result=collect_source(self.source,{self.source['id']:prior},self.reviews,'2026-10-08T10:00:00Z',fetcher)
        self.assertEqual(result['status'],'unavailable');self.assertTrue(result['fromCache'])
        self.assertEqual(result['items'],prior['items']);self.assertEqual(result['lastSuccessAt'],self.now)
    def test_unreviewed_and_empty_source_never_invent_a_summary(self):
        item=collect_source(self.source,{}, {},self.now,self.response)['items'][0]
        self.assertEqual(item['reviewState'],'pending');self.assertEqual(item['changes'],[])
        result=collect_source(self.source,{}, {},self.now,lambda _: {'contentList':[]})
        self.assertEqual(result['status'],'unavailable');self.assertEqual(result['items'],[])
        notice=reviewed({'id':'news','contentHash':None},{})
        self.assertEqual(notice['reviewState'],'pending')
    def test_hash_ignores_markup_and_excludes_scripts(self):
        self.assertEqual(text('<script>unsafe()</script><p>A &amp; B</p>'),'A & B')
        self.assertEqual(fingerprint('T','<p>A</p>'),fingerprint('T','A'))

if __name__=='__main__':unittest.main()

"""Editorial and generated-page regressions; no third-party media requests."""
import copy
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse, unquote

from bossmedia import SCENES, VIDEOS, CHAPTER_VIDEO, BOSS_REVIEW_DATE, media, validate_evidence
from battlelab import animation
from encounters import boss_lab, mechanic_panel, note_card
from fieldnotes import BOSSES, NOTES, KR_SOURCES, REVIEW_DATE

ROOT = Path(__file__).resolve().parents[1]
BASE = '/Aion2-Daeva-Atlas/'
PATTERNS = [(b, m) for b in BOSSES for m in b['mechanics']]

class Page(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, text):
        self.text.append(text)

    def find(self, key):
        return [(tag, attrs) for tag, attrs in self.tags if key in attrs]

class BossEvidenceTests(unittest.TestCase):
    def test_all_six_bosses_and_sixteen_patterns_have_specific_references(self):
        self.assertEqual(len(BOSSES), 6)
        self.assertEqual(len(PATTERNS), 16)
        self.assertEqual(set(SCENES), {b['id']+'-'+m['id'] for b,m in PATTERNS})
        validate_evidence()

    def test_missing_or_orphan_reference_stops_publication(self):
        refs = copy.deepcopy(SCENES)
        refs.pop('vakron-prison')
        with patch.dict(SCENES, refs, clear=True), self.assertRaises(ValueError):
            validate_evidence()
        with patch.dict(SCENES, {'invented':SCENES['berk-cover']}), self.assertRaises(ValueError):
            validate_evidence()

    def test_wrong_source_or_rehosted_media_stops_publication(self):
        for change in [{'source':'fire-temple'}, {'url':'https://example.org/copied.webp'}]:
            with self.subTest(change=change):
                ref = {**SCENES['vakron-bind'], **change}
                with patch.dict(SCENES, {'vakron-bind':ref}), self.assertRaises(ValueError):
                    validate_evidence()

    def test_unearned_verification_claims_stop_publication(self):
        for key in ['global_verified','timing_verified','video_verified']:
            with self.subTest(key=key):
                ref = {**SCENES['auldor-stack'], key:True}
                with patch.dict(SCENES, {'auldor-stack':ref}), self.assertRaises(ValueError):
                    validate_evidence()

    def test_both_languages_connect_the_selected_pattern_to_its_scene(self):
        for b,m in PATTERNS:
            uid = b['id']+'-'+m['id']
            for lang in ['en','ko']:
                with self.subTest(pattern=uid, lang=lang):
                    page = Page(mechanic_panel(b,m,lang,True,BASE))
                    refs = page.find('data-scene-reference')
                    self.assertEqual(len(refs), 1)
                    self.assertEqual(refs[0][1]['data-scene-reference'], uid)
                    links = [a['href'] for tag,a in page.tags if tag=='a']
                    self.assertIn(SCENES[uid]['url'], links)
                    article = next(u for u in links if '#:~:text=' in u)
                    self.assertEqual(article.split('#')[0], KR_SOURCES[m['source']]['url'])
                    self.assertEqual(unquote(article.split('#:~:text=')[1]),SCENES[uid]['section'])
                    text = ' '.join(' '.join(page.text).replace('↗','').split())
                    for key in ['cue','action','mistake','safe','success']:
                        self.assertIn(' '.join(m[key][lang=='ko'].split()),text)

    def test_no_third_party_media_is_embedded_or_fetched_by_reference_cards(self):
        for b,m in PATTERNS:
            page = Page(media(b,m,'en'))
            self.assertFalse(any(tag in {'img','iframe','video','source','script'} for tag,a in page.tags))
            for tag,a in page.tags:
                if tag=='a' and a.get('target')=='_blank':
                    self.assertEqual(set(a['rel'].split()),{'noopener','noreferrer'})

    def test_new_video_bosses_are_not_mislabelled_korean_or_verified(self):
        for bid in ['auldor','vakron','kromede']:
            self.assertEqual(VIDEOS[bid][0],CHAPTER_VIDEO)
            b = next(b for b in BOSSES if b['id']==bid)
            for lang in ['en','ko']:
                page = Page(media(b,b['mechanics'][0],lang))
                text = ' '.join(page.text)
                self.assertIn('TW footage' if lang=='en' else '대만 촬영', text)
                self.assertIn('Russian' if lang=='en' else '러시아어', text)
                self.assertIn('not verified' if lang=='en' else '검증하지 못', text)
                link = next(a['href'] for tag,a in page.tags if a.get('class')=='source-video-link')
                self.assertEqual(parse_qs(urlparse(link).query)['t'],[str(SCENES[b['id']+'-'+b['mechanics'][0]['id']]['chapter'])+'s'])

    def test_dive_chapter_does_not_claim_heading_demonstration(self):
        b = next(b for b in BOSSES if b['id']=='bakarma')
        m = next(m for m in b['mechanics'] if m['id']=='dive')
        self.assertIn('not a verified heading demonstration',media(b,m,'en'))
        self.assertIn('No fixed safe spot',m['safe'][0])

    def test_bow_chapter_does_not_claim_verified_kr_repeat(self):
        b = next(b for b in BOSSES if b['id']=='kromede')
        m = next(m for m in b['mechanics'] if m['id']=='bow')
        self.assertIn('not a verified example of the KR low-HP repeat',media(b,m,'en'))

    def test_mechanic_specific_followups_survive_rendering(self):
        checks = {
            'vakron-rings':('straight attacks','후속타'),
            'vakron-prison':('that rock’s opening','붉은 바위'),
            'kromede-bow':('two bursts','두 번'),
            'kromede-clones':('both hits','두 공격'),
            'nuakum-orb':('four opportunities','네 번'),
        }
        for b,m in PATTERNS:
            uid = b['id']+'-'+m['id']
            if uid not in checks:
                continue
            for lang, phrase in zip(['en','ko'],checks[uid]):
                with self.subTest(pattern=uid,lang=lang):
                    self.assertIn(phrase,animation(b,m,lang))

    def test_accessible_controls_and_text_steps_for_every_lesson(self):
        for b,m in PATTERNS:
            for lang in ['en','ko']:
                with self.subTest(pattern=b['id']+'-'+m['id'],lang=lang):
                    page = Page(animation(b,m,lang))
                    box = page.find('data-animation')[0][1]
                    captions = json.loads(box['data-captions'])
                    self.assertEqual(len(captions),3)
                    self.assertTrue(all(captions))
                    for control in ['data-animation-toggle','data-animation-replay','data-animation-seek']:
                        self.assertTrue(page.find(control)[0][1]['aria-label'])
                    svg = next(a for tag,a in page.tags if tag=='svg')
                    self.assertEqual(svg['role'],'img')
                    ids = {a['id'] for tag,a in page.tags if 'id' in a}
                    self.assertIn(svg['aria-describedby'],ids)
                    self.assertEqual([a['value'] for tag,a in page.tags if tag=='option'],['0.5','1','2'])
                    self.assertTrue(any(a.get('class')=='battle-transcript' for tag,a in page.tags))
                    self.assertIn('not a measured replay' if lang=='en' else '실측 재현이 아닙니다', ' '.join(page.text))

    def test_review_date_is_scoped_to_bosses_and_keeps_source_dates(self):
        b,m = PATTERNS[0]
        markup = mechanic_panel(b,m,'en',True,BASE)
        self.assertIn(BOSS_REVIEW_DATE,markup)
        self.assertIn(KR_SOURCES[m['source']]['date'],markup)
        self.assertIn(REVIEW_DATE,note_card(NOTES[0],'en',BASE))
        self.assertNotIn(BOSS_REVIEW_DATE,note_card(NOTES[0],'en',BASE))

    def test_no_javascript_still_exposes_all_patterns_and_hides_playback_controls(self):
        markup = boss_lab('en',BASE)
        self.assertIn('.battle-controls,.mechanic-tabs{display:none}',markup)
        self.assertEqual(len(Page(markup).find('data-scene-reference')),16)

    def test_generated_bilingual_boss_pages_have_matching_sources_and_assets(self):
        for lang in ['en','ko']:
            root = ROOT/'docs'/('ko' if lang=='ko' else '')
            for b in BOSSES:
                page = Page((root/'dungeons'/b['slug']/'index.html').read_text())
                refs = page.find('data-scene-reference')
                self.assertEqual({a['data-scene-reference'] for tag,a in refs},{b['id']+'-'+m['id'] for m in b['mechanics']})
                asset_urls = [a.get('src',a.get('href','')) for tag,a in page.tags]
                self.assertIn(BASE+'assets/boss-evidence.css?v=boss-scenes-1',asset_urls)
                self.assertIn(BASE+'assets/battle.js?v=boss-scenes-1',asset_urls)
        self.assertEqual((ROOT/'assets/battle.js').read_bytes(),(ROOT/'docs/assets/battle.js').read_bytes())
        self.assertEqual((ROOT/'assets/boss-evidence.css').read_bytes(),(ROOT/'docs/assets/boss-evidence.css').read_bytes())

if __name__=='__main__':
    unittest.main()

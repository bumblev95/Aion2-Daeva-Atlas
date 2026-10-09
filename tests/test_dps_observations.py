"""Source extraction and publication boundaries for measured public summaries."""
import unittest
from unittest.mock import patch
from scripts.review_dps_observations import parse, parse_report, rounded_dps, korean_dps, number
import dpsranking

class ObservationTests(unittest.TestCase):
    def test_source_precision(self):
        self.assertEqual(rounded_dps('1.6M/s'),dict(publishedDps='1.6M/s',value=1600000,resolution=100000))
        self.assertEqual(rounded_dps('311K/s')['resolution'],1000)
        self.assertEqual(rounded_dps('1.25K/s')['value'],1250)
        for invalid in ('311','Infinity/s','-2K/s','2B/s','2M/s<script>'):
            with self.assertRaises(ValueError): rounded_dps(invalid)
        self.assertIsNone(number('<5'))
        self.assertIsNone(number('—'))
        self.assertEqual(korean_dps('91.1만')['value'],911000)
        self.assertEqual(korean_dps('91.1만')['resolution'],1000)

    def test_weekly_current_column_not_chart_or_previous_week(self):
        def table(head, row):
            return '<table><thead><tr>'+''.join('<th>'+x+'</th>' for x in head)+'</tr></thead><tbody><tr>'+''.join('<td>'+x+'</td>' for x in row)+'</tr></tbody></table>'
        source = '<h1>10.7 주간 직업별 DPS 리포트</h1><p>같은 보스를 잡은 기록끼리 전투력 1당 DPS 진행 중인 주입니다</p>'
        source += table(['직업', '기록 수'], ['치유성', '405'])
        source += table(['직업', '9.30', '10.7 집계 중', ''], ['치유성', '0.67', '0.71', ''])
        source += table(['직업', '기록 수', 'DPS'], ['치유성', '30', '91.1만'])
        source += table(['보스'], ['보스']) + table(['주'], ['10.7'])
        result = parse_report(source, '2026-10-07', 'weekly')
        self.assertEqual(result['rows'][0]['value'], .71)
        self.assertTrue(result['provisional'])
        self.assertEqual(result['region'], 'UNSPECIFIED')
        self.assertFalse(result['regionVerified'])
        with self.assertRaisesRegex(ValueError,'identity'):
            parse_report(source,'2026-09-30','weekly')
        with self.assertRaisesRegex(ValueError,'column'):
            parse_report(source.replace('10.7 집계 중','10.14 집계 중'),'2026-10-07','weekly')

    def test_scope_and_layout_fail_closed(self):
        html = '''<main>region Global window Last 30 days Coverage as of 2026-10-07 14:25 UTC
        Compared over Under 300K.<table><thead><tr><th>Class</th><th>Typical</th><th>Top end</th></tr></thead>
        <tbody><tr><th><a>Cleric</a></th><td>77</td><td>74</td><td>11.4%</td><td>1,013</td>
        <td>19,941</td><td>800</td><td>774</td><td>44</td><td>1:45</td><td>17%</td></tr></tbody></table></main>'''
        row = parse(html,'balance','GLOBAL')['rows'][0]
        self.assertEqual((row['classId'],row['value'],row['parses']),('cleric',77,19941))
        with self.assertRaisesRegex(ValueError,'region'):parse(html,'balance','KR')
        with self.assertRaisesRegex(ValueError,'window'):parse(html.replace('Last 30 days','All time'),'balance','GLOBAL')
        with self.assertRaisesRegex(ValueError,'columns'):parse(html.replace('<td>44</td>',''),'balance','GLOBAL')

    def test_old_formula_results_cannot_render(self):
        with patch.object(dpsranking.json,'loads',return_value={'kind':'server-computed-dps-ranking','schema':1}):
            with self.assertRaisesRegex(ValueError,'Only reviewed combat'):dpsranking.load()

    def test_korean_page_prioritizes_korean_records(self):
        ko = dpsranking.render('ko','/')
        en = dpsranking.render('en','/')
        self.assertLess(ko.index('<section class="rank-scenarios"'),ko.index('<section class="rank-overall"'))
        self.assertLess(ko.index('<section class="rank-weekly"'),ko.index('<section class="rank-scenarios"'))
        self.assertLess(en.index('<section class="rank-overall"'),en.index('<section class="rank-scenarios"'))
        self.assertIn('임의의 스킬 시간으로 DPS를 재계산하지 않습니다',ko)
        self.assertIn('회복량과 버프로 늘어난 파티원 피해는 개인 DPS에 합치지 않습니다',ko)
        self.assertNotIn('data-dps=',ko)
        self.assertNotIn('7,284.85',ko)
        self.assertIn('311K/s',ko)

if __name__ == '__main__':unittest.main()

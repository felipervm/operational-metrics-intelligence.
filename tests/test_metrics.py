import sys,unittest,json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from build import dataset,calculate
class MetricsTests(unittest.TestCase):
    def setUp(self):self.rows=dataset();self.data=calculate(self.rows)
    def test_reproducible(self):self.assertEqual(dataset(),dataset())
    def test_unique_ids(self):self.assertEqual(len({r['ticket_id'] for r in self.rows}),len(self.rows))
    def test_coverage(self):self.assertEqual(len(self.rows),180)
    def test_partition(self):self.assertEqual(self.data['counts']['resolved']+self.data['counts']['open'],180)
    def test_severity_partition(self):self.assertEqual(sum(x['total'] for x in self.data['severity']),180)
    def test_team_partition(self):self.assertEqual(sum(x['total'] for x in self.data['teams']),180)
    def test_closed_status(self):self.assertTrue(all(bool(x['resolved_at'])==(x['status']=='resolved') for x in self.rows))
    def test_metric_contracts(self):
        it=self.data['comparison']['IT dashboard'];sec=self.data['comparison']['Security dashboard'];self.assertAlmostEqual(it['value'],round(100*it['numerator']/it['denominator'],1));self.assertAlmostEqual(sec['value'],round(100*sec['numerator']/sec['denominator'],1))
    def test_all_teams(self):self.assertEqual({x['team'] for x in self.rows},{'IT','Security','Compliance'})
    def test_rates_in_range(self):self.assertTrue(all(0<=x['sla_met_pct']<=100 for x in self.data['severity']))
    def test_critical_investigation(self):self.assertLess(self.data['severity'][0]['sla_met_pct'],50)
    def test_no_real_data(self):self.assertIn('synthetic',self.data['scope'].lower())
    def test_page_payload_matches(self):
        html=(ROOT/'index.html').read_text(encoding='utf-8');import re
        m=re.search(r'<script id="payload" type="application/json">(.*?)</script>',html,re.S)
        self.assertIsNotNone(m);self.assertEqual(json.loads(m.group(1)),self.data)
if __name__=='__main__':unittest.main()

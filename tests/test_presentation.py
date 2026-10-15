"""Timestamp traceability and published-artifact checks."""
import csv,json,re,sys,unittest
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from build import dataset,calculate
from build_site import render,json_script

class TraceabilityTests(unittest.TestCase):
    def test_duration_matches_timestamps(self):
        for row in dataset():
            created=datetime.fromisoformat(row['created_at'])
            self.assertIsNotNone(created.tzinfo)
            if row['status']=='resolved':
                closed=datetime.fromisoformat(row['resolved_at'])
                self.assertEqual((closed-created).total_seconds()/3600,row['elapsed_hours'])
                self.assertGreater(closed,created)

    def test_cohorts_reconcile_from_timestamp_evidence(self):
        rows=dataset();report=calculate(rows)
        for cohort in report['severity']:
            chosen=[r for r in rows if r['severity']==cohort['severity']]
            within=late=opened=0
            for row in chosen:
                if not row['resolved_at']:opened+=1;continue
                hours=(datetime.fromisoformat(row['resolved_at'])-datetime.fromisoformat(row['created_at'])).total_seconds()/3600
                if hours<=row['sla_hours']:within+=1
                else:late+=1
            self.assertEqual(within+late+opened,cohort['total'])
            self.assertEqual(late,cohort['late_resolved'])
            self.assertEqual(opened,cohort['open'])
            self.assertEqual(round(100*within/len(chosen),1),cohort['sla_met_pct'])
        critical=report['severity'][0]
        self.assertEqual((critical['resolved']-critical['late_resolved'],critical['late_resolved'],critical['open']),(21,22,8))

class PresentationTests(unittest.TestCase):
    def test_generated_page_rebuilds_exactly(self):
        self.assertEqual((ROOT/'index.html').read_bytes(),render(calculate(dataset())).encode('utf-8'))

    def test_json_cannot_close_its_script(self):
        value={'label':'</script><script>alert(1)</script>'}
        encoded=json_script(value)
        self.assertNotIn('<',encoded)
        self.assertEqual(json.loads(encoded),value)

    def test_local_links_and_unique_ids(self):
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        ids=re.findall(r'\bid="([^"]+)"',html)
        self.assertEqual(len(ids),len(set(ids)))
        for href in re.findall(r'href="([^"]+)"',html):
            if href.startswith('#'):self.assertIn(href[1:],ids)
            elif '/blob/main/' in href:self.assertTrue((ROOT/href.split('/blob/main/')[1]).is_file(),href)

    def test_assets_are_embedded_and_no_tokens_remain(self):
        html=(ROOT/'index.html').read_text(encoding='utf-8')
        self.assertEqual(html.count('data:image/jpeg;base64,'),2)
        self.assertEqual(html.count('data:font/woff2;base64,'),4)
        self.assertNotRegex(html,r'/\*__[A-Z_]+__\*/')
        self.assertNotRegex(html,r'<(?:script|img)[^>]+src="https?://')

if __name__=='__main__':unittest.main()

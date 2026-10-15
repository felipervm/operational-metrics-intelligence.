"""Deterministic fictional Risk / IT / Compliance metric-governance case."""
from __future__ import annotations
import csv, json, random, statistics
from collections import defaultdict, Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data';DATA.mkdir(exist_ok=True)
BASE=datetime(2026,7,1,9,tzinfo=timezone.utc)

def write_csv(name,rows):
    with (DATA/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def dataset():
    rng=random.Random(20261015)
    cases=[]
    for i in range(1,181):
        team=['IT','Security','Compliance'][i%3]
        month=(i*7)%3
        opened=BASE+timedelta(days=month*30+(i*11)%28)
        severity=['critical','high','medium','low'][(i*5+i//7)%4]
        target={'critical':72,'high':120,'medium':168,'low':336}[severity]
        # Synthetic mechanism: critical cases have operational delays and occasional stale handoffs.
        delay=rng.randint(5,120)+(9 if severity=='critical' else 0)+(55 if i%13==0 else 0)
        if team=='Security':delay+=rng.randint(0,44)
        resolved=(i%8!=0 and i%17!=0)
        closed=opened+timedelta(hours=delay) if resolved else None
        cases.append({'ticket_id':f'ISS-{i:04}', 'team':team,'severity':severity,
                      'created_at':opened.isoformat(),'resolved_at':closed.isoformat() if closed else '',
                      'sla_hours':target,'elapsed_hours':delay if resolved else '',
                      'status':'resolved' if resolved else 'open','source':'ticketing_simulation'})
    return cases

def calculate(cases):
    resolved=[x for x in cases if x['status']=='resolved']
    critical=[x for x in cases if x['severity']=='critical']
    # Distinct metrics: their populations and completion criteria intentionally differ.
    summaries={
        'IT dashboard':{'numerator':len(resolved),'denominator':len(cases), 'definition':'All resolved tickets / all tickets opened', 'value':round(100*len(resolved)/len(cases),1)},
        'Security dashboard':{'numerator':sum(x['status']=='resolved' and float(x['elapsed_hours'] or 1e6)<=int(x['sla_hours']) for x in critical), 'denominator':len(critical), 'definition':'Critical tickets resolved within the sample target / all created critical tickets', 'value':round(100*sum(x['status']=='resolved' and float(x['elapsed_hours'] or 1e6)<=int(x['sla_hours']) for x in critical)/len(critical),1)}
    }
    priority=[]
    for sev in ['critical','high','medium','low']:
        cohort=[x for x in cases if x['severity']==sev]
        done=[x for x in cohort if x['status']=='resolved']
        ontime=[x for x in done if float(x['elapsed_hours']) <= int(x['sla_hours'])]
        backlog=len(cohort)-len(done)
        missed=len(done)-len(ontime)
        priority.append({'severity':sev,'total':len(cohort),'resolved':len(done),'open':backlog,'late_resolved':missed,
                         'sla_met_pct':round(100*len(ontime)/len(cohort),1),
                         'p75_resolution_hours':round(sorted(float(x['elapsed_hours']) for x in done)[int(.75*(len(done)-1))],1) if done else 0})
    owner_results=[]
    for team in ['IT','Security','Compliance']:
        group=[x for x in cases if x['team']==team];done=[x for x in group if x['status']=='resolved']
        owner_results.append({'team':team,'total':len(group),'open':len(group)-len(done),'resolved_pct':round(100*len(done)/len(group),1)})
    findings=[]
    high=next(x for x in priority if x['severity']=='critical')
    if high['sla_met_pct']<50:
        findings.append({'priority':'P1','title':'Review critical-cohort completion against the sample target',
                         'observation':f"{high['sla_met_pct']}% of all created critical items were resolved within the illustrative target. Open items count as incomplete, not proven overdue.",
                         'decision':'Investigate critical-item routing and target-clock assumptions before assessing operational health.',
                         'proposed_owner':'Security Operations + IT Service Management',
                         'evidence':'Severity-specific created cohort; fictional records','validation':'Confirm target clock rules, pause states and severity taxonomy with both teams.'})
    discrepancy=round(summaries['IT dashboard']['value']-summaries['Security dashboard']['value'],1)
    if discrepancy>10:
        findings.append({'priority':'P1','title':'Keep unlike KPI definitions explicit',
                         'observation':f"Overall closure is {summaries['IT dashboard']['value']}%; critical intake completed within the sample target is {summaries['Security dashboard']['value']}%. These answer different questions, with different populations and completion criteria.",
                         'decision':'Approve separate names and definitions rather than averaging the two scores.',
                         'proposed_owner':'Enterprise BI + IT + Security','evidence':'Metric contract and dashboard reconciliation',
                         'validation':'Check business purpose and sign off metric glossary with functional owners.'})
    findings.append({'priority':'P2','title':'Define a consistent operational review cadence',
                     'observation':'Reporting ownership and exceptions should be visible alongside each metric.',
                     'decision':'Use a monthly leadership review with named owners and exception commentary.',
                     'proposed_owner':'Business Intelligence + functional leads','evidence':'Proposed operating model, not an observed company process',
                     'validation':'Pilot definitions on approved data; measure reviewer workload before scaling.'})
    return {'scope':'Entirely synthetic; hypothetical cross-functional operations, not Fortra data',
            'counts':{'records':len(cases),'resolved':len(resolved),'open':len(cases)-len(resolved)},
            'comparison':summaries,'metric_gap_pp':discrepancy,'severity':priority,'teams':owner_results,'findings':findings}

def main():
    rows=dataset();out=calculate(rows)
    write_csv('fictional_tickets.csv',rows)
    (DATA/'analysis.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'counts':out['counts'],'comparison':out['comparison'],'severity':out['severity']},indent=2))
if __name__=='__main__':main()

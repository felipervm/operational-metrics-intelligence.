# Using this work sample in a Business Intelligence & Metrics application

This independent case maps to the Fortra Business Analyst — Business Intelligence & Metrics job description supplied for the application. It demonstrates metric definitions, exception analysis and executive communication using 180 fictional tickets. It does not describe Fortra's internal operations, service agreements, risk exposure or reporting systems.

## Evidence to lead with

| Role responsibility | Repository evidence | Discussion to prepare |
| --- | --- | --- |
| Govern KPI definitions across functions | [Metric dictionary](metric_dictionary.md) | Define numerator, denominator, grain, accountable owner, reporting period, exclusions and the decision each metric supports. Explain why two different rates should not be averaged. |
| Translate operational data into useful leadership reporting | [Interactive case](../index.html), [executive brief](decision_brief.md) | Move from an aggregate metric to a severity-specific exception, then to a proposed owner and a concrete validation question. |
| Identify bottlenecks and improvement opportunities | [Severity results](../data/analysis.json), [calculation code](../src/build.py) | Identify a cohort requiring investigation. Do not claim that a rate proves a bottleneck, root cause, staffing problem or actual service failure. |
| Communicate risk and operational performance clearly | [Executive brief](decision_brief.md) | Distinguish throughput from time-target completion and status from risk reduction. Avoid presenting either rate as overall organizational health. |
| Establish consistent collection and reporting methods | [Source fixture](../data/fictional_tickets.csv), [deterministic build](../src/build.py), [tests](../tests/test_metrics.py) | Explain reproducibility, checks, source limitations and the definitions that functional owners would need to approve. |
| Bridge business and technical stakeholders | [Proposed owner and validation fields](../data/analysis.json), [metric dictionary](metric_dictionary.md) | Frame the Security, IT Service Management and BI conversations needed before operationalizing a scorecard. Owner assignments are proposals, not real stakeholder agreements. |
| Executive reviews, KPI/OKR programs and enterprise reporting | Proposed operating approach in the [brief](decision_brief.md) | The sample supports a discussion about a review cadence; it does not demonstrate a live monthly reporting program, an OKR implementation or a governed enterprise platform. |

## The central interpretation

**149 of 180 tickets are resolved (82.8%). Separately, 21 of 51 critical tickets are resolved within the exercise's invented target (41.2%).** These are different populations and criteria, not contradictory calculations or a discrepancy to reconcile.

The critical cohort contains 21 items completed within target, 22 completed beyond target and 8 open items. The conservative sample rate includes every critical ticket in its denominator and counts open items as not met. It does not establish contractual SLA compliance: an open ticket may still have time remaining. Similarly, 31 total open tickets are a status count, not an overdue-backlog measure.

The leadership decision is to inspect critical exceptions, confirm the metric contract with functional owners, and assign an accountable follow-up. The data does not establish the cause of a delay, the right investment, actual business risk or the benefit of a proposed intervention.

## Three-sentence application snippet

I created an independent operational metrics case using 180 fictional IT, Security and Compliance tickets to explore what leaders should review beyond an overall closure rate. The work includes reproducible Python calculations, an interactive scorecard, a proposed metric dictionary and an executive brief that connects exceptions to owners and validation questions. I would welcome the opportunity to walk through the definitions and discuss how I would adapt the reporting approach with business and technical stakeholders at Fortra.

Use the case URL alongside an accurate resume in the official application. This snippet describes the project; it makes no claim about previous employment, years of experience, qualifications or access to enterprise systems. No application or outreach has been sent as part of this work.

## Interview walkthrough

1. **State the business question.** What should leadership inspect before treating a high closure rate as evidence of operational health?
2. **Define both rates.** Show 149/180 overall closure and 21/51 critical-cohort completion within target. Explain why the denominator and time criteria change the question.
3. **Inspect the exception.** Break the critical cohort into within-target, resolved-late and open records. Explain why open does not mean overdue and why a cohort outcome does not prove a root cause.
4. **Propose a conversation.** Ask Security Operations and IT Service Management to validate severity mapping, clock rules, pauses and ownership. Ask BI to document the approved metric contract alongside the view.
5. **Make the follow-up observable.** Propose an exception review with a named owner, validation task and review date. Measure whether it changes a decision or uncovers a useful issue before claiming operational improvement.
6. **Describe the production gap.** Explain how a real source mapping, stakeholder review, permissions, refresh process and agreed reporting period would change this sample.

## Questions for the team

- Which leadership decision does each KPI or OKR support, and what action is expected when it moves?
- Who approves the definition, source, target, severity mapping and exceptions? How are definition changes versioned?
- Should the population be tickets created, tickets due, or tickets resolved during the reporting period? How are open items that are not yet due represented?
- How do pause states, reopened tickets, reassignment, business hours and time zones affect the clock?
- Which identifiers and source-of-truth rules connect Jira, service management, risk, compliance and BI data without duplicate counting?
- What should be reviewed monthly versus quarterly, and which leading indicators need validation before they influence decisions?
- How will stakeholders judge actionability, false alarms and reporting effort during a permissioned pilot?

## Scope and tooling limits

- Implemented: deterministic Python standard-library calculations, a synthetic CSV, JSON results, tests, documentation and a static interactive web report.
- Not implemented: Power BI, DAX, SQL transformations, Jira or Confluence integration, live security/compliance sources, an enterprise semantic model, or an automated executive reporting service.
- The sample targets and escalation priorities are illustrative assumptions. They are not Fortra policies, contractual SLAs, external benchmarks or validated risk scores.
- The sample omits real SLA starts/stops, business hours, pause/resume, reopening, reassignment and live backlog aging. The fictional UTC timestamps now preserve the hour-level duration used in calculations. Real clock rules and source-system timestamps still require validation.
- The fixture is deliberately small. It does not establish scalability, governance-program adoption, stakeholder experience, measured time savings or improved operational outcomes.

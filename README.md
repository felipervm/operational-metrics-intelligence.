# What Should Leadership Look At First?

**An independent operational metrics governance case by Felipe Mattos.** Inspired by the responsibilities of Fortra's Business Analyst – Business Intelligence & Metrics vacancy, not commissioned by or affiliated with Fortra.

## Business question

When cross-functional dashboard values look healthy, what needs review before leaders make a decision? This fictional case contrasts an **overall ticket closure rate** with a **critical-item SLA attainment rate**. They're intentionally different metrics, and should never be averaged or presented under a shared unqualified 'performance' label.

The real deliverable is **a decision-ready exception brief with a proposed owner and a metric contract**—not the dashboard itself.

## What the synthetic case finds

The seeded dataset has 180 fictional tickets across IT, Security and Compliance. The current outputs are generated from the source records: **82.8% closed overall**, **41.2% critical intake completed within the illustrative target (all created critical items are counted)**, and **31 tickets still open**. The difference does *not* represent an error or discrepancy in any actual Fortra dashboard. It demonstrates why leadership needs definitions and severity context.

The sample's synthetic escalation thresholds, created timestamp ranges, priority distribution and service targets are **assumptions for this exercise**, not company policies or external benchmarks.

## Run locally

Requires only Python 3.9+ and standard library:

```bash
python src/build.py
python src/build_site.py
python -m unittest discover -s tests -v
```

Open `index.html` locally for an interactive narrative with severity switching and action-oriented findings. No external packages, tracking, or network requests.

## Deliverables

- **Leadership decision case:** [`index.html`](index.html), interactive, static and easy to host on GitHub Pages.
- **Transparent source data:** [`data/fictional_tickets.csv`](data/fictional_tickets.csv).
- **Metrics and findings:** [`data/analysis.json`](data/analysis.json).
- **Reusable KPI contract:** [`docs/metric_dictionary.md`](docs/metric_dictionary.md).
- **Executive brief:** [`docs/decision_brief.md`](docs/decision_brief.md).
- **Reproduction and QA:** [`src/build.py`](src/build.py), [`src/build_site.py`](src/build_site.py), [`tests/test_metrics.py`](tests/test_metrics.py).

## Constraints

No access to Fortra's ticketing, Jira, security, compliance or executive reporting systems; no real incident details; no measured savings. SLA windows are simplified calendar-hour fixtures and do not model pause/resume, business hours, reopen behavior, reassignment or live open-ticket aging. This is a small, deliberately illustrative **control-design exercise**, not a validated enterprise operational performance model.

A real pilot would begin with authorized stakeholders agreeing to definitions, source ownership, data classifications, exceptions and the business actions each KPI should trigger. Any outcome claims would require a measured pilot.

## Public context

- [Fortra cybersecurity platform](https://www.fortra.com/platform): company positioning around consolidated operations, integrated tools and actionable risk visibility.
- [Fortra KPI guide](https://www.fortra.com/resources/guides/key-performance-indicators-and-reporting-tools-success): public context on reporting and metric use.
- [LinkedIn vacancy](https://www.linkedin.com/jobs/view/4478861661/): Business Analyst – Business Intelligence & Metrics responsibilities.

## Why this framing? Published rationale

I focused on the decision rather than a dashboard feature because the [Fortra KPI guide](https://www.fortra.com/resources/guides/key-performance-indicators-and-reporting-tools-success) emphasizes business information needs and shared KPIs; [Fortra's guidance on security performance reporting](https://www.fortra.com/blog/3-ways-peer-insight-peer-comparison-illustrates-cybersecurity-performance) highlights the difficulty of explaining technical risk to leadership; and the [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20) frames cybersecurity outcomes in terms of assessing, prioritizing, and communicating risk. Those sources motivate the general approach, **not** an allegation about actual Fortra reporting.

See [Research rationale](docs/research_rationale.md) for the claim-to-source mapping and boundaries.
# Metric contract — proposed definitions

All numbers in this project are fictional. These definitions represent an example of **governance documentation**, not Fortra standards.

| Metric | Numerator | Denominator | Grain | Owner to confirm | Interpretation and caveat |
| --- | --- | --- | --- | --- | --- |
| Overall closure rate | Tickets marked resolved | Tickets created in synthetic sample | Ticket | IT Service Management | Work throughput measure; does not represent SLA adherence or risk mitigated. |
| Critical cohort on-time completion | Critical tickets resolved within sample severity target | All critical tickets in sample, including open | Critical ticket | Security + IT Service Management | Conservative closed-cohort view; open items counted as not met, even when they may still have time remaining. **Not production-ready.** |
| Open backlog | Tickets with open status | N/A, count | Ticket | Functional ticket owners | Without current snapshot date and open-item aging, does not measure overdue backlog. |
| p75 time to resolve | 75th percentile of close duration | Resolved tickets in selected severity | Resolved ticket | IT + Security | Simplified hours. Does not include unresolved records; should be paired with backlog aging. |

**Before implementation:** Agree on reporting period, status taxonomy, severity mapping, pause states, reopened tickets, ticket ownership, whether the denominator is opened-versus-due or resolved-within-period, and data sensitivity. The synthetic case deliberately omits these complexities.

## Why two headline values should not be reconciled into one

The 82.8% completion figure and 41.2% critical-item SLA figure are not competing measurements of the same KPI. They have different populations and criteria. The 'metric conflict' is **a presentation and semantics risk**: executives might erroneously treat both as generic effectiveness signals. An appropriate remedy is clearer names, contracts and decision context, not forcing a single number.
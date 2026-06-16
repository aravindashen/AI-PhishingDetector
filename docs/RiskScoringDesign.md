# Risk Scoring Design

## Category Scores

| Category | Score |
|-----------|-----------|
| Urgency | 10 |
| Credential | 25 |
| Financial | 20 |
| Social Engineering | 15 |

---

## Risk Levels

| Score | Risk Level |
|-----------|-----------|
| 0-20 | Low |
| 21-50 | Medium |
| 51-100 | High |
| >100 | Critical |

---

## Purpose

The Risk Scoring Engine calculates phishing severity based on detected indicators and provides a user-friendly risk assessment.

## Keyword Counting Rule

For Version 1, each keyword contributes to the score only once regardless of how many times it appears in the email.

Reason:
- Reduces false positives
- Simplifies implementation
- Improves result consistency
<div align="center">

# 🛡️ Phishing Guardian AI

**Email threat analysis platform — detects phishing indicators, scores risk, and generates actionable security recommendations in real time.**

Built by Aravind

**🚀 [Live Demo](https://phishing-guardian-ai.streamlit.app/)**

</div>

---

## Screenshots

<table>
<tr>
<td width="50%"><img src="docs/screenshots/dashboard-empty.png" alt="Dashboard"></td>
<td width="50%"><img src="docs/screenshots/email-input.png" alt="Email Analysis Input"></td>
</tr>
<tr>
<td width="50%"><img src="docs/screenshots/analysis-results.png" alt="Threat Analysis Results"></td>
<td width="50%"><img src="docs/screenshots/recommendations.png" alt="Security Recommendations"></td>
</tr>
</table>

## Overview

Phishing Guardian AI is a rule-engine-driven threat analysis tool that inspects raw email content and flags social engineering, credential theft, and fraud indicators across **8 distinct threat categories**. It calculates a weighted threat score, classifies risk severity, and produces a downloadable incident report — all through an interactive dashboard.

The project was built to explore how detection logic used in real SOC (Security Operations Center) tooling — keyword/pattern matching, weighted risk scoring, and tiered response recommendations — can be implemented end-to-end as a working application.

## Features

- **Threat Indicator Detection** — scans email text against a categorized rule set covering credential theft, social engineering, financial fraud, domain impersonation, attachment lures, invoice fraud, crypto scams, and gift card scams
- **Weighted Risk Scoring** — each detected indicator contributes to a cumulative threat score based on category severity
- **Risk Classification** — automatically tiers results into `Low`, `Medium`, `High`, or `Critical`
- **Actionable Recommendations** — generates a tailored response checklist based on the assessed risk level
- **Downloadable Reports** — exports a plain-text incident summary for record-keeping
- **Interactive Dashboard** — built with Streamlit, styled as a dark, real-time analyst console

## Tech Stack

| Layer | Technology |
|---|---|
| Interface | Streamlit |
| Language | Python |
| Data handling | Pandas |
| Detection logic | Custom rule engine (keyword/pattern matching) |

## Project Structure

```
AI-PhishingDetector/
├── src/
│   ├── app.py                    # Streamlit dashboard (UI + orchestration)
│   ├── main.py                   # Entry point
│   ├── preprocessing.py          # Text cleaning/normalization
│   ├── rule_engine.py            # Indicator detection logic
│   ├── threat_categories.py      # Threat category keyword definitions
│   ├── risk_scores.py            # Per-category risk weights
│   ├── risk_calc.py              # Score aggregation + risk level classification
│   ├── recommendation_engine.py  # Risk-tiered response recommendations
│   └── report_generator.py       # Incident report generation
├── docs/                         # Architecture & design documentation
│   ├── Architecture.md
│   ├── DetectionEngine.md
│   ├── RiskScoringDesign.md
│   ├── RuleEngineDesign.md
│   ├── SRS.md
│   └── ThreatCategoriesv2.md
└── requirements.txt
```

## How It Works

1. **Input** — paste raw email content (headers, body, links) into the dashboard
2. **Preprocessing** — text is cleaned and normalized for consistent matching
3. **Detection** — the rule engine scans for indicators across all threat categories
4. **Scoring** — each match is weighted and summed into a cumulative threat score
5. **Classification** — the score maps to a risk tier (`Low` → `Critical`)
6. **Response** — the dashboard surfaces detected indicators, an executive summary, and tiered recommendations
7. **Export** — a full analysis report can be downloaded for documentation

## Getting Started

**Prerequisites:** Python 3.9+

```bash
# Clone the repository
git clone https://github.com/aravindashen/AI-PhishingDetector.git
cd AI-PhishingDetector

# Install dependencies
pip install -r requirements.txt


## Roadmap

- [ ] Expand detection to support HTML email parsing and header analysis
- [ ] Add machine learning-based classification alongside rule-based detection
- [ ] URL reputation checks via external threat intelligence APIs
- [ ] Batch analysis for multiple emails
- [ ] Persistent logging/history of past analyses

## Documentation

Detailed design notes are available in [`/docs`](./docs), covering system architecture, detection engine design, risk scoring methodology, and threat category definitions.

## Author

**Aravind** — Cybersecurity student specializing in network & cloud security.
GitHub: [@aravindashen](https://github.com/aravindashen)

---

<div align="center">
<sub>Built as a hands-on exploration of SOC-style threat detection and risk scoring systems.</sub>
</div>

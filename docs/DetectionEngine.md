# Detection Engine V2 Design

## Objective

The objective of Detection Engine V2 is to improve the scalability, maintainability, and extensibility of the phishing detection system.

Version 1 used separate keyword lists and separate loops for each category.

Version 2 will use a centralized dictionary-based architecture.

---

## Why Upgrade?

Problems in Version 1:

* Multiple keyword lists
* Multiple detection loops
* Difficult to maintain
* Difficult to add new categories
* Increased code duplication

Version 2 solves these issues using a dictionary-based design.

---

## Dictionary-Based Architecture

Example Structure:

THREAT_CATEGORIES

* credential_theft
* social_engineering
* financial_fraud
* domain_impersonation
* attachment_lure
* invoice_fraud
* crypto_scam
* gift_card_scam

Each category contains its own indicators and keywords.

---

## Advantages

### Scalability

New threat categories can be added without changing the detection logic.

### Maintainability

All categories are managed from a single location.

### Reduced Code Duplication

A single detection loop can process all categories.

### Extensibility

Future phishing techniques can be incorporated easily.

---

## Detection Flow

Email Input
↓
Preprocessing Module
↓
Load Threat Categories
↓
Loop Through Categories
↓
Loop Through Keywords
↓
Keyword Match Found
↓
Store Indicator and Category
↓
Continue Scan
↓
Risk Calculation
↓
Executive Summary Generation
↓
SOC Dashboard Output

---

## Future Enhancements

* Machine Learning Detection
* URL Analysis
* Sender Reputation Analysis
* Attachment Analysis
* Domain Reputation Checking
* AI-Based Threat Summaries

---

## Engineering Principles Used

* Separation of Concerns (SoC)
* Single Responsibility Principle (SRP)
* Open/Closed Principle (OCP)
* Modular Design
* Scalable Architecture

---

## Conclusion

Detection Engine V2 provides a scalable and maintainable architecture for phishing detection. The design enables rapid addition of new threat categories while keeping the detection logic simple and reusable.

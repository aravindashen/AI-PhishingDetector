from preprocessing import clean_text
from rule_engine import detect_indicators
from risk_calc import calculate_score, get_risk_level
from report_generator import generate_report
email_text = input("Enter Email Content:\n")
cleaned_text = clean_text(email_text)
findings = detect_indicators(cleaned_text)
score = calculate_score(findings)

risk_level = get_risk_level(score)
report = generate_report(
    score,
    risk_level,
    findings
)
print(report)
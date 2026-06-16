def generate_report(score, risk_level, findings):

    report = "\n"
    report += "=" * 40 + "\n"
    report += "PHISHING ANALYSIS REPORT\n"
    report += "=" * 40 + "\n\n"

    report += f"Risk Score : {score}\n"
    report += f"Risk Level : {risk_level}\n\n"

    report += "Detected Indicators:\n"

    for keyword, category in findings:
        report += f"- {keyword} ({category})\n"

    report += "\n"

    if risk_level == "Low":
        report += "Recommendation: Email appears safe.\n"

    elif risk_level == "Medium":
        report += "Recommendation: Verify sender before taking action.\n"

    elif risk_level == "High":
        report += "Recommendation: Do not click links or share credentials.\n"

    else:
        report += "Recommendation: Treat this email as highly suspicious.\n"

    report += "=" * 40

    return report

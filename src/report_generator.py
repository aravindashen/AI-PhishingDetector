from recommendation_engine import get_recommendations


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

    recommendations = get_recommendations(risk_level)

    report += "Recommendations:\n"

    for recommendation in recommendations:
        report += f"- {recommendation}\n"

    report += "=" * 40

    return report
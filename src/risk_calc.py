from risk_scores import RISK_SCORES

def calculate_score(findings):

    score = 0

    for keyword, category in findings:

        score += RISK_SCORES.get(category, 0)

    return score


def get_risk_level(score):

    if score == 0:
        return "Low"

    elif score <= 30:
        return "Medium"

    elif score <= 70:
        return "High"

    else:
        return "Critical"
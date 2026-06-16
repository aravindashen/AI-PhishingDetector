CATEGORY_SCORES = {
    "urgency": 10,
    "credential": 25,
    "financial": 20,
    "social_engineering": 15
}
def calculate_score(detected_indicators):
    total_score = 0

    for keyword, category in detected_indicators:
        total_score += CATEGORY_SCORES[category]

    return total_score
def get_risk_level(score):
    if score <= 20:
        return "Low"

    elif score <= 50:
        return "Medium"

    elif score <= 100:
        return "High"

    else:
        return "Critical"
    

    
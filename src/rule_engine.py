from threat_categories import THREAT_CATEGORIES

def detect_indicators(text):

    detected = []

    for category, keywords in THREAT_CATEGORIES.items():

        for keyword in keywords:

            if keyword in text:
                detected.append(
                    (keyword, category)
                )

    return detected
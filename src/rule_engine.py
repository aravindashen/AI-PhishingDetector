# ==========================
# Indicator Database
# ==========================

URGENCY_INDICATORS = [
    "urgent",
    "immediately",
    "warning",
    "suspended"
]

CREDENTIAL_INDICATORS = [
    "password",
    "login",
    "verify",
    "otp"
]

FINANCIAL_INDICATORS = [
    "bank",
    "payment",
    "refund",
    "invoice"
]

SOCIAL_ENGINEERING_INDICATORS = [
    "click here",
    "verify now",
    "open attachment"
]


# ==========================
# Detection Engine
# ==========================

def detect_indicators(text):
    detected = []

    # Urgency Indicators
    for keyword in URGENCY_INDICATORS:
        if keyword in text:
            detected.append((keyword, "urgency"))

    # Credential Indicators
    for keyword in CREDENTIAL_INDICATORS:
        if keyword in text:
            detected.append((keyword, "credential"))

    # Financial Indicators
    for keyword in FINANCIAL_INDICATORS:
        if keyword in text:
            detected.append((keyword, "financial"))

    # Social Engineering Indicators
    for keyword in SOCIAL_ENGINEERING_INDICATORS:
        if keyword in text:
            detected.append((keyword, "social_engineering"))

    return detected


# ==========================
# Testing
# ==========================

sample = """
Verify your password immediately.
Click here to login now.
"""

result = detect_indicators(sample.lower())

print("Detected Indicators:")
print(result)
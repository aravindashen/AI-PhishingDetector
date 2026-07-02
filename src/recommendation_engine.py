def get_recommendations(risk_level):

    if risk_level == "Low":
        return [
            "No immediate action required.",
            "Continue normal communication.",
            "Stay cautious with future emails."
        ]

    elif risk_level == "Medium":
        return [
            "Verify the sender before responding.",
            "Avoid clicking unknown links.",
            "Confirm requests using another communication channel."
        ]

    elif risk_level == "High":
        return [
            "Do not click any links.",
            "Do not share passwords or personal information.",
            "Verify the sender independently.",
            "Report the email to your security team."
        ]

    elif risk_level == "Critical":
        return [
            "Treat the email as malicious.",
            "Delete the email immediately.",
            "Block the sender.",
            "Notify the security team.",
            "Scan your device if you interacted with the email."
        ]

    else:
        return [
            "Unable to determine recommendations."
        ]
    

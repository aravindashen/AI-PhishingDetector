import streamlit as st
import pandas as pd

from preprocessing import clean_text
from rule_engine import detect_indicators
from risk_calc import calculate_score, get_risk_level
from recommendation_engine import get_recommendations

st.set_page_config(
    page_title="Phishing Guardian AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Phishing Guardian AI")
st.caption("Enterprise Email Threat Analysis Platform")

st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    email_text = st.text_area(
        "📧 Email Content",
        height=250,
        placeholder="Paste suspicious email content here..."
    )

with col2:
    st.markdown("### Quick Actions")
    analyze = st.button(
        "🔍 Analyze Threat",
        use_container_width=True
    )

if analyze:

    if email_text.strip() == "":
        st.warning("Please enter an email before analysis.")
        st.stop()

    cleaned_text = clean_text(email_text)

    findings = detect_indicators(cleaned_text)

    score = calculate_score(findings)

    risk_level = get_risk_level(score)

    recommendations = get_recommendations(risk_level)

    st.divider()

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Threat Score", score)

    with metric2:

        st.markdown("### Risk Level")

        colors = {
            "Low": "#2ecc71",
            "Medium": "#f1c40f",
            "High": "#e67e22",
            "Critical": "#e74c3c"
        }

        st.markdown(
            f"""
            <div style="
                background-color:{colors[risk_level]};
                color:white;
                padding:14px;
                border-radius:10px;
                text-align:center;
                font-size:22px;
                font-weight:bold;">
                {risk_level}
            </div>
            """,
            unsafe_allow_html=True
        )

    with metric3:
        st.metric("Indicators Found", len(findings))

    st.progress(min(score / 200, 1.0))

    st.divider()

    st.subheader("🚨 Detected Threat Indicators")

    if findings:

        df = pd.DataFrame(
            findings,
            columns=["Keyword", "Threat Category"]
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("✅ No phishing indicators detected.")

    st.divider()

    st.subheader("📋 Executive Summary")

    if risk_level == "Low":

        st.success(
            "This email appears legitimate. No suspicious phishing indicators were detected."
        )

    elif risk_level == "Medium":

        st.warning(
            "Some suspicious indicators were detected. Verify the sender before clicking links or sharing information."
        )

    elif risk_level == "High":

        st.error(
            "Multiple phishing indicators were detected. This email may attempt credential theft or social engineering."
        )

    else:

        st.error(
            "Critical phishing attempt detected. This email is highly malicious and should not be trusted."
        )

    st.divider()

    st.subheader("🛠 Security Recommendations")

    for recommendation in recommendations:
        st.write(f"✅ {recommendation}")

    st.divider()

    report = f"""
PHISHING ANALYSIS REPORT
========================

Threat Score : {score}
Risk Level   : {risk_level}

Detected Indicators
-------------------
"""

    if findings:
        for keyword, category in findings:
            report += f"- {keyword} ({category})\n"
    else:
        report += "No indicators detected.\n"

    report += "\nRecommendations\n----------------\n"

    for recommendation in recommendations:
        report += f"- {recommendation}\n"

    st.download_button(
        label="📄 Download Analysis Report",
        data=report,
        file_name="phishing_analysis_report.txt",
        mime="text/plain",
        use_container_width=True
    )
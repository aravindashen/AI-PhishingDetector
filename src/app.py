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

# ------------------------------------------------------------------
# GLOBAL STYLE — clean, professional, product-grade SaaS look
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

:root {
    --bg: #f6f8fb;
    --card: #ffffff;
    --border: #e5e9f0;
    --ink: #101828;
    --muted: #667085;
    --accent: #4338ca;
    --accent-soft: #eef2ff;
    --low: #059669;
    --medium: #d97706;
    --high: #ea580c;
    --critical: #dc2626;
}

.stApp {
    background: var(--bg);
}

#MainMenu, footer, header {visibility: hidden;}

/* ---- Top banner ---- */
.app-header {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 55%, #4338ca 100%);
    border-radius: 16px;
    padding: 32px 36px;
    margin-bottom: 28px;
    box-shadow: 0 8px 24px rgba(67, 56, 202, 0.18);
}
.app-header h1 {
    color: #ffffff;
    font-size: 28px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
}
.app-header p {
    color: #c7d2fe;
    font-size: 14.5px;
    margin: 6px 0 0 0;
    font-weight: 500;
}
.app-header .badge-row {
    margin-top: 16px;
    display: flex;
    gap: 8px;
}
.pill {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    color: #e0e7ff;
    font-size: 12px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.18);
}

/* ---- Cards ---- */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 22px 24px;
    box-shadow: 0 1px 2px rgba(16,24,40,0.04);
}

/* ---- Section labels ---- */
.section-label {
    font-size: 12.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    margin-bottom: 10px;
}

/* ---- Streamlit input override ---- */
.stTextArea textarea {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13.5px !important;
    background: #fbfbfd !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-soft) !important;
}

/* ---- Button override ---- */
.stButton > button {
    background: var(--accent) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 12px 0 !important;
    font-size: 14.5px !important;
    box-shadow: 0 4px 12px rgba(67,56,202,0.25) !important;
    transition: transform 0.1s ease;
}
.stButton > button:hover {
    background: #3730a3 !important;
    transform: translateY(-1px);
}

/* ---- Metric tiles ---- */
.metric-tile {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    text-align: left;
}
.metric-tile .label {
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--muted);
}
.metric-tile .value {
    font-size: 30px;
    font-weight: 800;
    color: var(--ink);
    margin-top: 4px;
    font-family: 'JetBrains Mono', monospace;
}

/* ---- Risk badge ---- */
.risk-badge {
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.02em;
}

/* ---- Executive summary box ---- */
.summary-box {
    border-radius: 12px;
    padding: 18px 20px;
    font-size: 14.5px;
    font-weight: 500;
    line-height: 1.55;
    border-left: 4px solid;
}

/* ---- Recommendation rows ---- */
.rec-row {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
    color: var(--ink);
}
.rec-row:last-child { border-bottom: none; }
.rec-check {
    color: var(--low);
    font-weight: 800;
    flex-shrink: 0;
}

.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
}

.stDownloadButton > button {
    background: var(--ink) !important;
    color: #fff !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

RISK_COLORS = {
    "Low": "#059669",
    "Medium": "#d97706",
    "High": "#ea580c",
    "Critical": "#dc2626",
}

RISK_BG = {
    "Low": "#ecfdf5",
    "Medium": "#fffbeb",
    "High": "#fff7ed",
    "Critical": "#fef2f2",
}

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.markdown("""
<div class="app-header">
    <h1>🛡️ Phishing Guardian AI</h1>
    <p>Enterprise Email Threat Analysis Platform</p>
    <div class="badge-row">
        <span class="pill">Real-time Detection</span>
        <span class="pill">NLP Rule Engine</span>
        <span class="pill">Risk Scoring</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="section-label">📧 Email Content</div>', unsafe_allow_html=True)
    email_text = st.text_area(
        "Email Content",
        height=230,
        placeholder="Paste suspicious email content here...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)
    analyze = st.button(
        "🔍  Analyze Threat",
        use_container_width=True
    )
    st.markdown(
        '<div style="margin-top:14px; font-size:12.5px; color:#667085; line-height:1.5;">'
        'Paste the full raw email — headers, body, and links — for the most accurate '
        'risk assessment.</div>',
        unsafe_allow_html=True
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

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Threat Score</div>
            <div class="value">{score}</div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown(f"""
        <div class="risk-badge" style="background:{RISK_COLORS[risk_level]};">
            {risk_level} Risk
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Indicators Found</div>
            <div class="value">{len(findings)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.progress(min(score / 200, 1.0))
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">🚨 Detected Threat Indicators</div>', unsafe_allow_html=True)

    if findings:
        df = pd.DataFrame(findings, columns=["Keyword", "Threat Category"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No phishing indicators detected.")

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">📋 Executive Summary</div>', unsafe_allow_html=True)

    summary_text = {
        "Low": "This email appears legitimate. No suspicious phishing indicators were detected.",
        "Medium": "Some suspicious indicators were detected. Verify the sender before clicking links or sharing information.",
        "High": "Multiple phishing indicators were detected. This email may attempt credential theft or social engineering.",
        "Critical": "Critical phishing attempt detected. This email is highly malicious and should not be trusted.",
    }[risk_level]

    st.markdown(f"""
    <div class="summary-box" style="background:{RISK_BG[risk_level]}; border-left-color:{RISK_COLORS[risk_level]}; color:#1f2937;">
        {summary_text}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">🛠 Security Recommendations</div>', unsafe_allow_html=True)

    rec_html = '<div class="card">'
    for recommendation in recommendations:
        rec_html += f'<div class="rec-row"><span class="rec-check">✓</span><span>{recommendation}</span></div>'
    rec_html += '</div>'
    st.markdown(rec_html, unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

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

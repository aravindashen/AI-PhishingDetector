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
# GLOBAL STYLE
# ------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

:root {
    --bg: #0b0e1a;
    --panel: #131829;
    --panel-2: #171d33;
    --border: #262f4d;
    --ink: #eef1fb;
    --muted: #8891b3;
    --violet: #7c5cff;
    --cyan: #22d3ee;
    --low: #22c55e;
    --medium: #eab308;
    --high: #fb923c;
    --critical: #f43f5e;
}

.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(124,92,255,0.18) 0%, transparent 45%),
        radial-gradient(circle at 85% 20%, rgba(34,211,238,0.12) 0%, transparent 40%),
        var(--bg);
    background-attachment: fixed;
}

#MainMenu, footer, header {visibility: hidden;}

/* faint grid texture behind everything */
.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(124,92,255,0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124,92,255,0.045) 1px, transparent 1px);
    background-size: 42px 42px;
    pointer-events: none;
    z-index: 0;
}

/* ---- Hero ---- */
.hero {
    position: relative;
    background: linear-gradient(135deg, #1a1436 0%, #241a4d 45%, #1c2a4d 100%);
    border: 1px solid #302a5c;
    border-radius: 20px;
    padding: 40px 42px;
    margin-bottom: 30px;
    overflow: hidden;
    box-shadow: 0 0 0 1px rgba(124,92,255,0.08), 0 20px 60px rgba(76,29,149,0.25);
}
.hero::after {
    content: "";
    position: absolute;
    top: -60%;
    left: -10%;
    width: 55%;
    height: 260%;
    background: linear-gradient(100deg, transparent 40%, rgba(124,92,255,0.10) 50%, transparent 60%);
    animation: sweep 5s ease-in-out infinite;
}
@keyframes sweep {
    0%   { transform: translateX(-40%) rotate(8deg); }
    50%  { transform: translateX(140%) rotate(8deg); }
    100% { transform: translateX(-40%) rotate(8deg); }
}
.hero-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: relative;
    z-index: 1;
}
.hero h1 {
    color: #ffffff;
    font-size: 32px;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 12px;
}
.hero p {
    color: #a5b0e0;
    font-size: 15px;
    margin: 8px 0 0 0;
    font-weight: 500;
}
.live-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(34,211,238,0.08);
    border: 1px solid rgba(34,211,238,0.35);
    color: var(--cyan);
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    padding: 7px 14px;
    border-radius: 999px;
    letter-spacing: 0.03em;
}
.live-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan);
    animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.75); }
}
.badge-row {
    margin-top: 20px;
    display: flex;
    gap: 10px;
    position: relative;
    z-index: 1;
    flex-wrap: wrap;
}
.pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.05);
    color: #cdd4f0;
    font-size: 12.5px;
    font-weight: 600;
    padding: 7px 14px;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.10);
}

/* ---- Panels ---- */
.panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    z-index: 1;
}
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--cyan);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::before {
    content: "";
    width: 3px;
    height: 14px;
    background: var(--cyan);
    border-radius: 2px;
    display: inline-block;
}

/* ---- Inputs ---- */
.stTextArea textarea {
    border-radius: 12px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13.5px !important;
    background: #0e1326 !important;
    color: var(--ink) !important;
}
.stTextArea textarea:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px rgba(124,92,255,0.18) !important;
}
.stTextArea textarea::placeholder { color: #4c557a !important; }

/* ---- Button ---- */
.stButton > button {
    background: linear-gradient(135deg, var(--violet), #5b3fd6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    padding: 14px 0 !important;
    font-size: 15px !important;
    box-shadow: 0 8px 20px rgba(124,92,255,0.35) !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    box-shadow: 0 10px 26px rgba(124,92,255,0.5) !important;
    transform: translateY(-2px);
}

/* ---- Gauge ---- */
.gauge-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 10px 0 4px 0;
}
.gauge {
    width: 132px;
    height: 132px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
}
.gauge-inner {
    width: 104px;
    height: 104px;
    border-radius: 50%;
    background: var(--panel);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.gauge-inner .num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--ink);
}
.gauge-inner .lbl {
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}

/* ---- Metric tiles ---- */
.metric-tile {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 22px;
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.metric-tile .label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--muted);
    margin-bottom: 8px;
}
.metric-tile .value {
    font-size: 34px;
    font-weight: 800;
    color: var(--ink);
    font-family: 'JetBrains Mono', monospace;
}

/* ---- Risk badge tile ---- */
.risk-tile {
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1.5px solid;
}
.risk-tile .rlabel {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    opacity: 0.85;
    margin-bottom: 8px;
}
.risk-tile .rvalue {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 0.01em;
}

/* ---- Summary box ---- */
.summary-box {
    border-radius: 14px;
    padding: 18px 22px;
    font-size: 14.5px;
    font-weight: 500;
    line-height: 1.6;
    border-left: 4px solid;
    background: var(--panel-2);
    color: #d6dbf5;
}

/* ---- Recommendation rows ---- */
.rec-row {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
    color: var(--ink);
}
.rec-row:last-child { border-bottom: none; }
.rec-check {
    color: var(--cyan);
    font-weight: 800;
    flex-shrink: 0;
    font-family: 'JetBrains Mono', monospace;
}

.stDataFrame { border-radius: 14px !important; overflow: hidden; border: 1px solid var(--border) !important; }

.stDownloadButton > button {
    background: transparent !important;
    color: var(--cyan) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    border: 1.5px solid var(--cyan) !important;
}
.stDownloadButton > button:hover {
    background: rgba(34,211,238,0.08) !important;
}

h1, h2, h3, p, span, div { color: var(--ink); }
</style>
""", unsafe_allow_html=True)

RISK_COLORS = {
    "Low": "#22c55e",
    "Medium": "#eab308",
    "High": "#fb923c",
    "Critical": "#f43f5e",
}

RISK_TILE_BG = {
    "Low": "rgba(34,197,94,0.08)",
    "Medium": "rgba(234,179,8,0.08)",
    "High": "rgba(251,146,60,0.08)",
    "Critical": "rgba(244,63,94,0.08)",
}

# ------------------------------------------------------------------
# HERO
# ------------------------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-top">
        <div>
            <h1>🛡️ Phishing Guardian AI</h1>
            <p>Enterprise Email Threat Analysis Platform</p>
        </div>
        <div class="live-pill"><span class="live-dot"></span>ENGINE ONLINE</div>
    </div>
    <div class="badge-row">
        <span class="pill">⚡ Real-time Detection</span>
        <span class="pill">🧠 NLP Rule Engine</span>
        <span class="pill">📊 Risk Scoring</span>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.markdown('<div class="section-label">Email Content</div>', unsafe_allow_html=True)
    email_text = st.text_area(
        "Email Content",
        height=230,
        placeholder="Paste suspicious email content here — headers, body, and links...",
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="section-label">Quick Actions</div>', unsafe_allow_html=True)
    analyze = st.button("🔍  Analyze Threat", use_container_width=True)
    st.markdown(
        '<div style="margin-top:14px; font-size:12.5px; color:#8891b3; line-height:1.5;">'
        'Paste the full raw email for the most accurate risk assessment.</div>',
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
    color = RISK_COLORS[risk_level]

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    metric1, metric2, metric3 = st.columns([1, 1, 1])

    gauge_pct = min(score / 200, 1.0) * 360

    with metric1:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Threat Score</div>
            <div class="gauge-wrap">
                <div class="gauge" style="background: conic-gradient({color} {gauge_pct}deg, #232a49 {gauge_pct}deg);">
                    <div class="gauge-inner">
                        <div class="num">{score}</div>
                        <div class="lbl">/ 200</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with metric2:
        st.markdown(f"""
        <div class="risk-tile" style="border-color:{color}; background:{RISK_TILE_BG[risk_level]};">
            <div class="rlabel" style="color:{color};">Risk Level</div>
            <div class="rvalue" style="color:{color};">⚠ {risk_level}</div>
        </div>
        """, unsafe_allow_html=True)

    with metric3:
        st.markdown(f"""
        <div class="metric-tile">
            <div class="label">Indicators Found</div>
            <div class="value">{len(findings)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Detected Threat Indicators</div>', unsafe_allow_html=True)

    if findings:
        df = pd.DataFrame(findings, columns=["Keyword", "Threat Category"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No phishing indicators detected.")

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Executive Summary</div>', unsafe_allow_html=True)

    summary_text = {
        "Low": "This email appears legitimate. No suspicious phishing indicators were detected.",
        "Medium": "Some suspicious indicators were detected. Verify the sender before clicking links or sharing information.",
        "High": "Multiple phishing indicators were detected. This email may attempt credential theft or social engineering.",
        "Critical": "Critical phishing attempt detected. This email is highly malicious and should not be trusted.",
    }[risk_level]

    st.markdown(f"""
    <div class="summary-box" style="border-left-color:{color};">
        {summary_text}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Security Recommendations</div>', unsafe_allow_html=True)

    rec_html = '<div class="panel">'
    for recommendation in recommendations:
        rec_html += f'<div class="rec-row"><span class="rec-check">▸</span><span>{recommendation}</span></div>'
    rec_html += '</div>'
    st.markdown(rec_html, unsafe_allow_html=True)

    st.markdown("<div style='height:30px'></div>", unsafe_allow_html=True)

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

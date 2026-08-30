"""
PathPilot AI — Streamlit application entrypoint.
"Don't just recommend what to learn. Decide what to learn next."
"""

import json
import streamlit as st

from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant

from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap


st.set_page_config(
    page_title="PathPilot AI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
# DESIGN TOKENS + GLOBAL STYLES
# ======================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #F7F8FC;
    --surface: #FFFFFF;
    --surface-raised: #FFFFFF;
    --surface-sunken: #EEF0F7;
    --border: #E4E7F1;
    --border-strong: #D3D7E6;

    --accent: #5B5CE2;
    --accent-hover: #4C4DD1;
    --accent-soft: rgba(91,92,226,0.08);
    --accent-soft-strong: rgba(91,92,226,0.14);
    --accent-dim: rgba(91,92,226,0.30);
    --accent-ink: #FFFFFF;

    --text-primary: #1B1D2B;
    --text-secondary: #545873;
    --text-muted: #767A97;
    --text-faint: #9DA1BC;

    --success: #16A34A;
    --success-soft: rgba(22,163,74,0.09);
    --success-border: rgba(22,163,74,0.24);
    --warning: #C4791A;
    --warning-soft: rgba(196,121,26,0.10);
    --warning-border: rgba(196,121,26,0.26);
    --danger: #DC3545;
    --danger-soft: rgba(220,53,69,0.08);
    --danger-border: rgba(220,53,69,0.24);

    --font-display: 'Plus Jakarta Sans', sans-serif;
    --font-body: 'Inter', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;

    --space-xs: 0.4rem;
    --space-sm: 0.75rem;
    --space-md: 1.25rem;
    --space-lg: 2rem;
    --space-xl: 3rem;

    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 18px;

    --shadow-sm: 0 1px 2px rgba(24,27,53,0.04), 0 1px 1px rgba(24,27,53,0.03);
    --shadow-md: 0 6px 20px rgba(24,27,53,0.07), 0 2px 6px rgba(24,27,53,0.04);
    --shadow-lg: 0 16px 40px rgba(24,27,53,0.10), 0 4px 10px rgba(24,27,53,0.05);
}

html, body, .stApp, [class*="css"] { font-family: var(--font-body) !important; }
.stApp { background-color: var(--bg); color: var(--text-primary); }
h1, h2, h3, h4, .pp-display { font-family: var(--font-display) !important; letter-spacing: -0.017em; color: var(--text-primary); }
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: var(--border); }
.block-container { padding-top: 2rem; padding-bottom: 3.5rem; max-width: 1160px; }
::selection { background: var(--accent-soft-strong); }

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border-strong); border-radius: 8px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-faint); }

/* ======================================================================
   APP SHELL — HEADER
====================================================================== */
.pp-page-header {
    display: flex; justify-content: space-between; align-items: flex-end;
    padding-bottom: var(--space-lg); margin-bottom: var(--space-lg);
    border-bottom: 1px solid var(--border);
    flex-wrap: wrap; gap: var(--space-md);
}
.pp-page-header h1 { font-size: 1.65rem; font-weight: 700; margin: 0 0 5px 0; }
.pp-page-header p { color: var(--text-muted); font-size: 0.93rem; margin: 0; max-width: 460px; line-height: 1.5; }

.pp-status-chip {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 0.85rem 1.2rem; text-align: right; min-width: 150px;
    box-shadow: var(--shadow-sm);
}
.pp-status-label { font-size: 0.63rem; letter-spacing: 0.09em; color: var(--text-faint); text-transform: uppercase; font-weight: 600; }
.pp-status-value { font-family: var(--font-display); font-size: 1.18rem; font-weight: 700; margin-top: 4px; }
.pp-status-sub { color: var(--text-faint); font-size: 0.74rem; font-family: var(--font-mono); margin-top: 1px; }

/* ======================================================================
   SIDEBAR
====================================================================== */
section[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--border); }
section[data-testid="stSidebar"] .block-container { padding-top: 1.8rem; padding-left: 1.3rem; padding-right: 1.3rem; }

.pp-brand { display: flex; align-items: center; gap: 10px; margin-bottom: 0.15rem; }
.pp-brand-mark {
    width: 30px; height: 30px; border-radius: 9px;
    background: linear-gradient(135deg, var(--accent), #7B6BF0);
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: #fff; font-weight: 700;
    box-shadow: 0 3px 8px rgba(91,92,226,0.30);
}
.pp-brand-name { font-family: var(--font-display); font-weight: 800; font-size: 1.05rem; color: var(--text-primary); }
.pp-brand-sub {
    font-size: 0.71rem; color: var(--text-faint); font-weight: 500;
    margin: 0.2rem 0 1.7rem 40px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px; }
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: var(--radius-sm); padding: 8px 12px !important;
    margin-bottom: 1px; transition: background 0.15s ease, transform 0.1s ease; width: 100%;
    border-left: 2px solid transparent;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: var(--surface-sunken); }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: var(--accent-soft); border-left: 2px solid var(--accent);
}
section[data-testid="stSidebar"] div[role="radiogroup"] input { accent-color: var(--accent); }
section[data-testid="stSidebar"] div[role="radiogroup"] label p { font-size: 0.87rem; color: var(--text-secondary); font-weight: 500; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color: var(--accent); font-weight: 600; }

.pp-user-card {
    border-top: 1px solid var(--border); margin-top: var(--space-md);
    padding-top: var(--space-md); display: flex; align-items: center; gap: 10px;
}
.pp-user-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    background: var(--surface-sunken); border: 1px solid var(--border-strong);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display); font-weight: 700; font-size: 0.85rem; color: var(--accent);
    flex-shrink: 0;
}
.pp-user-name { font-weight: 600; font-size: 0.89rem; color: var(--text-primary); line-height: 1.3; }
.pp-user-role { color: var(--text-faint); font-size: 0.73rem; margin-top: 1px; }

/* ======================================================================
   TYPOGRAPHY UTILITIES
====================================================================== */
.pp-eyebrow {
    font-size: 0.69rem; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--accent); font-weight: 700; margin-bottom: 0.4rem;
}
.pp-section-title { font-size: 1.3rem; font-weight: 700; margin: 0 0 var(--space-md) 0; color: var(--text-primary); }

/* ======================================================================
   BUTTONS
====================================================================== */
.stButton > button {
    background: var(--surface); color: var(--text-secondary);
    border: 1px solid var(--border-strong); border-radius: 9px;
    font-weight: 600; padding: 0.5rem 1rem;
    transition: border-color 0.15s ease, background 0.15s ease, transform 0.08s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    border-color: var(--accent); background: var(--accent-soft); color: var(--accent);
    box-shadow: var(--shadow-sm);
}
.stButton > button:active { transform: translateY(1px); }

div[data-testid="stFormSubmitButton"] > button, .pp-primary-btn button {
    background: var(--accent) !important;
    border: 1px solid var(--accent) !important; color: #fff !important; font-weight: 700 !important;
    box-shadow: 0 4px 14px rgba(91,92,226,0.28) !important;
}
div[data-testid="stFormSubmitButton"] > button:hover, .pp-primary-btn button:hover {
    background: var(--accent-hover) !important; border-color: var(--accent-hover) !important;
    box-shadow: 0 6px 18px rgba(91,92,226,0.36) !important;
    transform: translateY(-1px);
}

/* Text inputs / selects */
.stTextInput input, .stTextArea textarea, .stNumberInput input, div[data-baseweb="select"] > div {
    background: var(--surface) !important; border-color: var(--border-strong) !important;
    border-radius: 9px !important; color: var(--text-primary) !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important; box-shadow: 0 0 0 3px var(--accent-soft) !important;
}
label, .stMarkdown p { color: var(--text-secondary); }
.stSelectSlider [role="slider"] { background: var(--accent) !important; }

/* ======================================================================
   CARDS
====================================================================== */
.pp-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 1.35rem 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
}
.pp-card:hover { border-color: var(--border-strong); box-shadow: var(--shadow-md); transform: translateY(-1px); }

/* ======================================================================
   LANDING PAGE
====================================================================== */
.pp-landing-topbar { display: flex; align-items: center; gap: 10px; padding: 0.4rem 0 2.2rem 0; }
.pp-landing-topbar .pp-brand-mark { width: 28px; height: 28px; font-size: 13px; }
.pp-landing-topbar .pp-brand-name { font-size: 1rem; }

.pp-landing-hero { text-align: center; padding: 1.4rem 1rem 0 1rem; }
.pp-landing-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: var(--accent-soft); border: 1px solid var(--accent-dim); border-radius: 999px;
    padding: 0.42rem 1.05rem; font-size: 0.73rem; color: var(--accent); font-weight: 600;
    margin-bottom: var(--space-lg); font-family: var(--font-mono); letter-spacing: 0.04em;
}
.pp-landing-badge-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); }
.pp-landing-hero h1 {
    font-size: 3rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.1;
    color: var(--text-primary);
}
.pp-landing-hero p.pp-tagline { color: var(--text-secondary); font-size: 1.12rem; max-width: 560px; margin: 0 auto; line-height: 1.6; }

/* Intelligence flow strip */
.pp-flow-strip {
    display: flex; align-items: center; justify-content: center; gap: 0;
    margin: var(--space-xl) auto 0.5rem auto; max-width: 920px; flex-wrap: wrap;
}
.pp-flow-node {
    display: flex; flex-direction: column; align-items: center; gap: 8px;
    padding: 0 0.4rem; position: relative;
}
.pp-flow-node.active .pp-flow-dot { background: var(--accent); border-color: var(--accent); box-shadow: 0 0 0 5px var(--accent-soft); }
.pp-flow-node.active .pp-flow-label { color: var(--accent); font-weight: 700; }
.pp-flow-dot {
    width: 13px; height: 13px; border-radius: 50%;
    background: var(--surface); border: 2px solid var(--border-strong);
    transition: all 0.2s ease;
}
.pp-flow-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; white-space: nowrap; letter-spacing: 0.01em; }
.pp-flow-connector { width: 44px; height: 2px; background: var(--border-strong); margin: 0 2px; align-self: flex-start; margin-top: 6px; }

.pp-feature-row { display: flex; gap: 0; border-top: 1px solid var(--border); margin-top: var(--space-xl); }
.pp-feature-col {
    flex: 1; padding: 1.7rem 1.6rem; border-right: 1px solid var(--border);
    transition: background 0.18s ease;
}
.pp-feature-col:last-child { border-right: none; }
.pp-feature-col:hover { background: var(--surface-sunken); }
.pp-feature-num { font-family: var(--font-mono); color: var(--accent); font-size: 0.8rem; margin-bottom: 0.55rem; font-weight: 600; }
.pp-feature-title { font-family: var(--font-display); font-weight: 700; font-size: 1.05rem; margin-bottom: 0.45rem; color: var(--text-primary); }
.pp-feature-desc { color: var(--text-muted); font-size: 0.88rem; line-height: 1.55; }

/* ======================================================================
   ONBOARDING
====================================================================== */
.pp-onboarding-header { text-align: center; margin-bottom: var(--space-lg); }
.pp-onb-progress { display: flex; justify-content: center; gap: 6px; margin-bottom: 1.1rem; }
.pp-onb-progress-seg { width: 40px; height: 4px; border-radius: 4px; background: var(--accent); }
.pp-step-header { display: flex; align-items: center; gap: 11px; margin: 1.9rem 0 0.9rem 0; }
.pp-step-num {
    width: 24px; height: 24px; border-radius: 50%; background: var(--accent-soft);
    border: 1px solid var(--accent-dim); display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.72rem; color: var(--accent); flex-shrink: 0; font-weight: 700;
}
.pp-step-title { font-weight: 700; font-size: 1rem; color: var(--text-primary); }
.pp-step-hint { color: var(--text-faint); font-size: 0.82rem; margin: -0.5rem 0 0.7rem 35px; }

/* ======================================================================
   DASHBOARD METRIC CARDS
====================================================================== */
.pp-metric-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 1.15rem 1.3rem;
    box-shadow: var(--shadow-sm);
    transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
}
.pp-metric-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-md); border-color: var(--border-strong); }
.pp-metric-card.hero {
    background: linear-gradient(155deg, var(--accent-soft) 0%, var(--surface) 55%);
    border-color: var(--accent-dim);
}
.pp-metric-label { font-size: 0.73rem; color: var(--text-faint); font-weight: 600; }
.pp-metric-value { font-family: var(--font-display); font-size: 1.85rem; font-weight: 700; margin: 0.18rem 0; color: var(--text-primary); }
.pp-metric-desc { font-size: 0.76rem; font-weight: 600; }
.trend-good { color: var(--success); }
.trend-warn { color: var(--warning); }
.trend-bad { color: var(--danger); }
.trend-neutral { color: var(--text-faint); }

/* ======================================================================
   NEXT BEST ACTION
====================================================================== */
.pp-nba-card {
    background: linear-gradient(160deg, var(--accent-soft) 0%, var(--surface) 45%);
    border: 1px solid var(--accent-dim);
    border-radius: var(--radius-lg); padding: 2.1rem 2.3rem; margin-bottom: var(--space-md);
    box-shadow: var(--shadow-md);
}
.pp-nba-eyebrow { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.12em; color: var(--accent); text-transform: uppercase; margin-bottom: 0.6rem; font-weight: 700; }
.pp-nba-skill { font-family: var(--font-display); font-size: 2rem; font-weight: 800; margin: 0 0 1.2rem 0; color: var(--text-primary); }
.pp-nba-stats { display: flex; gap: 2.4rem; flex-wrap: wrap; }
.pp-nba-stat-label { font-size: 0.71rem; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.pp-nba-stat-value { font-family: var(--font-display); font-size: 1.3rem; font-weight: 700; margin-top: 3px; color: var(--text-primary); }
.pp-nba-why { margin-top: 1.4rem; padding-top: 1.2rem; border-top: 1px solid var(--accent-dim); }
.pp-insight-row { display: flex; align-items: flex-start; gap: 9px; padding: 0.4rem 0; }
.pp-insight-check { color: var(--success); font-size: 0.92rem; margin-top: 1px; }
.pp-insight-text { color: var(--text-secondary); font-size: 0.88rem; line-height: 1.55; }

.pp-score-row { margin-bottom: 0.85rem; }
.pp-score-top { display: flex; justify-content: space-between; font-size: 0.83rem; margin-bottom: 5px; }
.pp-score-name { color: var(--text-muted); font-weight: 500; }
.pp-score-num { font-family: var(--font-mono); font-weight: 700; color: var(--text-primary); }
.pp-score-track { background: var(--surface-sunken); border-radius: 6px; height: 7px; overflow: hidden; }
.pp-score-fill { height: 100%; border-radius: 6px; background: var(--accent); transition: width 0.4s ease; }

.pp-badge {
    display: inline-block; padding: 0.28rem 0.8rem; border-radius: 999px;
    font-size: 0.73rem; font-weight: 700; font-family: var(--font-mono);
}
.badge-healthy { background: var(--success-soft); color: var(--success); border: 1px solid var(--success-border); }
.badge-atrisk { background: var(--warning-soft); color: var(--warning); border: 1px solid var(--warning-border); }
.badge-critical { background: var(--danger-soft); color: var(--danger); border: 1px solid var(--danger-border); }

.pp-chip {
    display: inline-block; background: var(--surface-sunken);
    border: 1px solid var(--border-strong); border-radius: 999px;
    padding: 0.4rem 0.9rem; font-size: 0.8rem; color: var(--text-secondary); font-weight: 500;
    margin: 0 6px 6px 0; transition: border-color 0.15s ease, background 0.15s ease;
}
.pp-chip:hover { border-color: var(--accent); background: var(--accent-soft); color: var(--accent); }

/* ======================================================================
   PATH HEALTH
====================================================================== */
.pp-risk-card {
    background: var(--surface); border: 1px solid var(--border);
    border-left: 3px solid var(--text-faint);
    border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.7rem;
    box-shadow: var(--shadow-sm);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.pp-risk-card:hover { transform: translateX(2px); box-shadow: var(--shadow-md); }
.pp-risk-high { border-left-color: var(--danger); }
.pp-risk-medium { border-left-color: var(--warning); }
.pp-risk-low { border-left-color: var(--accent); }
.pp-risk-severity { font-size: 0.66rem; letter-spacing: 0.09em; text-transform: uppercase; font-weight: 700; }
.pp-risk-high .pp-risk-severity { color: var(--danger); }
.pp-risk-medium .pp-risk-severity { color: var(--warning); }
.pp-risk-low .pp-risk-severity { color: var(--accent); }
.pp-risk-title { font-weight: 700; font-size: 0.97rem; margin: 3px 0 5px 0; color: var(--text-primary); }
.pp-risk-msg { color: var(--text-muted); font-size: 0.87rem; margin-bottom: 6px; line-height: 1.5; }
.pp-risk-action { color: var(--text-faint); font-size: 0.81rem; }
.pp-risk-action b { color: var(--text-muted); }

/* ======================================================================
   AI ASSISTANT
====================================================================== */
.pp-assistant-answer {
    background: linear-gradient(160deg, var(--accent-soft) 0%, var(--surface) 55%);
    border: 1px solid var(--accent-dim);
    border-radius: var(--radius-md); padding: 1.25rem 1.45rem; margin-top: var(--space-sm);
    box-shadow: var(--shadow-sm);
}

/* ======================================================================
   RESPONSIVE
====================================================================== */
@media (max-width: 768px) {
    .pp-landing-hero h1 { font-size: 2.1rem; }
    .pp-nba-skill { font-size: 1.5rem; }
    .pp-nba-stats { gap: 1.3rem; }
    .pp-page-header { flex-direction: column; align-items: flex-start; }
    .pp-status-chip { text-align: left; }
    .pp-feature-row { flex-direction: column; }
    .pp-feature-col { border-right: none; border-bottom: 1px solid var(--border); }
    .pp-feature-col:last-child { border-bottom: none; }
    .pp-flow-strip { flex-direction: column; gap: 14px; }
    .pp-flow-connector { width: 2px; height: 22px; margin: 0; }
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# Session state init
# ----------------------------------------------------------------------
def init_session_state():
    defaults = {
        "stage": "welcome",
        "profile": None,
        "engine_output": None,
        "adaptation_state": AdaptationState(),
        "roadmap_progress": {},
        "nav_section": "Overview",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


init_session_state()


@st.cache_resource
def get_engine():
    try:
        return IntelligenceEngine()
    except Exception as e:
        st.error(f"Failed to load intelligence engine: {e}")
        return None


@st.cache_resource
def get_assistant():
    return AIAssistant()


engine = get_engine()
assistant = get_assistant()
adaptive_engine = AdaptiveEngine(engine) if engine else None


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def safe_call(fn, *args, **kwargs):
    if fn is None:
        return None
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        st.warning(f"A calculation step had an issue: {e}")
        return None


def get_career_options():
    try:
        with open("data/career_paths.json", "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return list(data.keys())
        if isinstance(data, list):
            return [d.get("career_goal") or d.get("name") for d in data if isinstance(d, dict)]
    except Exception:
        pass
    return ["Machine Learning Engineer", "Data Scientist", "Full Stack Web Developer", "Cybersecurity Analyst"]


def run_engine_pipeline(profile):
    output = {
        "skill_gap": safe_call(engine.analyze_skill_gap, profile),
        "readiness": safe_call(engine.calculate_readiness_score, profile),
        "next_best_action": safe_call(engine.calculate_next_best_action, profile),
        "risks": safe_call(engine.detect_risks, profile) or [],
        "path_health": safe_call(engine.calculate_path_health, profile),
        "roadmap": safe_call(engine.generate_roadmap, profile) or [],
    }
    st.session_state.engine_output = output
    return output


def status_badge_class(status):
    return {
        "Healthy": "badge-healthy",
        "At Risk": "badge-atrisk",
        "Critical": "badge-critical",
    }.get(status, "badge-atrisk")


def get_initials(name):
    parts = [p for p in str(name).strip().split(" ") if p]
    if not parts:
        return "PP"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# ----------------------------------------------------------------------
# WELCOME
# ----------------------------------------------------------------------
def render_welcome():
    st.markdown(
        '<div class="pp-landing-topbar">'
        '<div class="pp-brand-mark">◆</div>'
        '<div class="pp-brand-name">PathPilot AI</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="pp-landing-hero">'
        '<div class="pp-landing-badge"><span class="pp-landing-badge-dot"></span>PERSONALIZED LEARNING INTELLIGENCE</div>'
        '<h1>Stop guessing.<br>Start moving with direction.</h1>'
        '<p class="pp-tagline">PathPilot analyzes your current skills, career goal and learning constraints '
        'to determine what you should learn next — and explains exactly why.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pp-flow-strip">
            <div class="pp-flow-node active"><div class="pp-flow-dot"></div><div class="pp-flow-label">You Are Here</div></div>
            <div class="pp-flow-connector"></div>
            <div class="pp-flow-node"><div class="pp-flow-dot"></div><div class="pp-flow-label">Analyze</div></div>
            <div class="pp-flow-connector"></div>
            <div class="pp-flow-node"><div class="pp-flow-dot"></div><div class="pp-flow-label">Identify Gaps</div></div>
            <div class="pp-flow-connector"></div>
            <div class="pp-flow-node"><div class="pp-flow-dot"></div><div class="pp-flow-label">Decide Next Step</div></div>
            <div class="pp-flow-connector"></div>
            <div class="pp-flow-node"><div class="pp-flow-dot"></div><div class="pp-flow-label">Build Your Path</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    spacer_l, center, spacer_r = st.columns([1, 1, 1])
    with center:
        st.markdown('<div class="pp-primary-btn">', unsafe_allow_html=True)
        clicked = st.button("Build My Learning Path →", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if clicked:
        st.session_state.stage = "profiling"
        st.rerun()

    st.markdown(
        """
        <div class="pp-feature-row">
            <div class="pp-feature-col">
                <div class="pp-feature-num">01</div>
                <div class="pp-feature-title">Personalized Intelligence</div>
                <div class="pp-feature-desc">Move beyond generic course lists to one scored, explainable recommendation built from your actual skills and goals.</div>
            </div>
            <div class="pp-feature-col">
                <div class="pp-feature-num">02</div>
                <div class="pp-feature-title">Next Best Action</div>
                <div class="pp-feature-desc">A single decision, not a wall of options — with the reasoning behind it laid out clearly.</div>
            </div>
            <div class="pp-feature-col">
                <div class="pp-feature-num">03</div>
                <div class="pp-feature-title">Adaptive Learning Path</div>
                <div class="pp-feature-desc">Your feedback reshapes the path in real time, catching blockers before they slow you down.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# PROFILING
# ----------------------------------------------------------------------
def render_profiling():
    st.markdown(
        '<div class="pp-onboarding-header">'
        '<div class="pp-onb-progress"><div class="pp-onb-progress-seg"></div>'
        '<div class="pp-onb-progress-seg"></div><div class="pp-onb-progress-seg"></div></div>'
        '<div class="pp-eyebrow" style="justify-content:center; display:flex;">ONBOARDING</div>'
        '<h2 style="margin:0.2rem 0;">Let\'s build your path</h2>'
        '<p style="color:var(--text-muted); margin:0;">Three quick steps. Every answer sharpens your recommendations.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    career_options = get_career_options()

    with st.form("profiling_form"):
        st.markdown(
            '<div class="pp-step-header"><div class="pp-step-num">1</div>'
            '<div class="pp-step-title">Your destination</div></div>'
            '<div class="pp-step-hint">Where are you trying to get to?</div>',
            unsafe_allow_html=True,
        )
        name = st.text_input("Name", placeholder="e.g. Akshaya Reddy")
        career_goal = st.selectbox("Career Goal", options=career_options)
        natural_language_goal = st.text_area(
            "In your own words, what do you want to achieve?",
            placeholder="e.g. I want to become an ML engineer within 6 months and land an internship.",
        )

        st.markdown(
            '<div class="pp-step-header"><div class="pp-step-num">2</div>'
            '<div class="pp-step-title">Your current position</div></div>'
            '<div class="pp-step-hint">What do you already bring to the table?</div>',
            unsafe_allow_html=True,
        )
        experience_level_label = st.select_slider(
            "Experience Level",
            options=["Beginner", "Intermediate", "Advanced"],
            value="Beginner",
        )
        experience_map = {"Beginner": 1, "Intermediate": 3, "Advanced": 5}
        current_skills_raw = st.text_input(
            "Current Skills (comma-separated)", placeholder="e.g. Python Basics, SQL, Git"
        )
        interests_raw = st.text_input(
            "Interests (comma-separated)", placeholder="e.g. AI, Data, Web Development"
        )

        st.markdown(
            '<div class="pp-step-header"><div class="pp-step-num">3</div>'
            '<div class="pp-step-title">Your learning reality</div></div>'
            '<div class="pp-step-hint">What can you realistically commit to?</div>',
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            weekly_hours = st.number_input("Weekly Learning Hours", min_value=1, max_value=80, value=10)
        with col2:
            timeline_weeks = st.number_input("Target Timeline (weeks)", min_value=1, max_value=104, value=24)
        preferred_learning_style = st.selectbox(
            "Preferred Learning Style",
            options=["visual", "reading", "hands-on", "video", "mixed"],
        )

        st.write("")
        submitted = st.form_submit_button("Generate My Intelligence Path →")

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
            return

        current_skills = [s.strip() for s in current_skills_raw.split(",") if s.strip()]
        interests = [s.strip() for s in interests_raw.split(",") if s.strip()]

        try:
            profile = LearnerProfile(
                name=name.strip(),
                career_goal=career_goal,
                natural_language_goal=natural_language_goal.strip(),
                experience_level=experience_map[experience_level_label],
                current_skills=current_skills,
                interests=interests,
                completed_courses=[],
                weekly_hours=int(weekly_hours),
                timeline_weeks=int(timeline_weeks),
                preferred_learning_style=preferred_learning_style,
            )
        except Exception as e:
            st.error(f"Could not build your profile: {e}")
            return

        st.session_state.profile = profile

        if engine is None:
            st.error("Intelligence engine is unavailable. Please check the data files.")
            return

        with st.spinner("Analyzing your profile..."):
            run_engine_pipeline(profile)

        st.session_state.stage = "app"
        st.rerun()

    if st.button("← Back"):
        st.session_state.stage = "welcome"
        st.rerun()


# ----------------------------------------------------------------------
# NEXT BEST ACTION SECTION
# ----------------------------------------------------------------------
def render_next_best_action():
    st.markdown('<div class="pp-eyebrow">DECISION ENGINE</div><h2 class="pp-section-title">Next Best Action</h2>', unsafe_allow_html=True)

    engine_output = st.session_state.engine_output or {}
    nba = engine_output.get("next_best_action")

    if not nba:
        st.markdown(
            '<div class="pp-card">You\'re caught up — no further recommendation right now for your current goal.</div>',
            unsafe_allow_html=True,
        )
        return

    reasons = nba.get("reasons", [])
    reasons_html = "".join(
        f'<div class="pp-insight-row"><span class="pp-insight-check">✓</span>'
        f'<span class="pp-insight-text">{r}</span></div>'
        for r in reasons
    ) or '<div class="pp-insight-text">No additional reasoning provided.</div>'

    st.markdown(
        f"""
        <div class="pp-nba-card">
            <div class="pp-nba-eyebrow">PathPilot's Decision</div>
            <div class="pp-nba-skill">Learn: {nba.get('skill', 'N/A')}</div>
            <div class="pp-nba-stats">
                <div><div class="pp-nba-stat-label">Confidence Score</div><div class="pp-nba-stat-value">{nba.get('score', 'N/A')}</div></div>
                <div><div class="pp-nba-stat-label">Estimated Effort</div><div class="pp-nba-stat-value">{nba.get('est_hours', 'N/A')} hrs</div></div>
                <div><div class="pp-nba-stat-label">Difficulty</div><div class="pp-nba-stat-value">{nba.get('difficulty', 'N/A')}</div></div>
            </div>
            <div class="pp-nba-why">
                <div class="pp-eyebrow">WHY THIS NOW?</div>
                {reasons_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    breakdown = nba.get("score_breakdown", {})
    if breakdown:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown('<div class="pp-eyebrow">SCORE BREAKDOWN</div>', unsafe_allow_html=True)
        rows_html = ""
        for factor, value in breakdown.items():
            try:
                pct = max(0, min(100, float(value)))
            except (TypeError, ValueError):
                pct = 0
            rows_html += f"""
            <div class="pp-score-row">
                <div class="pp-score-top">
                    <span class="pp-score-name">{str(factor).replace('_', ' ').title()}</span>
                    <span class="pp-score-num">{value}</span>
                </div>
                <div class="pp-score-track"><div class="pp-score-fill" style="width:{pct}%;"></div></div>
            </div>
            """
        st.markdown(rows_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    render_adaptive_feedback(nba)

    if assistant:
        with st.expander("AI Explanation", expanded=False):
            with st.spinner("Generating explanation..."):
                explanation = safe_call(assistant.explain_next_best_action, st.session_state.profile, nba)
            st.write(explanation or "Explanation unavailable right now.")


def render_adaptive_feedback(nba):
    st.markdown('<p style="color:var(--text-muted); font-size:0.87rem; margin:1.4rem 0 0.6rem 0; font-weight:500;">How does this feel for you?</p>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    skill_name = nba.get("skill")

    feedback_clicked = None
    with col1:
        if st.button("Too Easy", use_container_width=True):
            feedback_clicked = "too_easy"
    with col2:
        if st.button("Appropriate", use_container_width=True):
            feedback_clicked = "appropriate"
    with col3:
        if st.button("Too Difficult", use_container_width=True):
            feedback_clicked = "too_difficult"

    if feedback_clicked and adaptive_engine and skill_name:
        with st.spinner("Adapting your path..."):
            result = safe_call(
                adaptive_engine.apply_feedback,
                st.session_state.profile,
                skill_name,
                feedback_clicked,
                st.session_state.adaptation_state,
            )

        if result:
            st.success("Your learning path has been adapted based on your feedback.")
            st.info(result.get("adaptation_message", ""))

            if result.get("root_blockers"):
                st.warning(f"Root blockers identified: {', '.join(result['root_blockers'])}")

            engine_output = st.session_state.engine_output or {}
            if result.get("updated_recommendation") is not None:
                engine_output["next_best_action"] = result["updated_recommendation"]
            if result.get("updated_path_health") is not None:
                engine_output["path_health"] = result["updated_path_health"]
            if result.get("updated_risks") is not None:
                engine_output["risks"] = result["updated_risks"]
            st.session_state.engine_output = engine_output
            st.rerun()


# ----------------------------------------------------------------------
# AI ASSISTANT SECTION
# ----------------------------------------------------------------------
def render_ai_assistant():
    st.markdown(
        '<div class="pp-eyebrow">PATH INTELLIGENCE ASSISTANT</div>'
        '<h2 class="pp-section-title" style="margin-bottom:0.2rem;">Ask about your learning path</h2>'
        '<p style="color:var(--text-muted); margin-top:0; margin-bottom:1.3rem;">'
        'Understand your recommendations, roadmap, blockers and progress.</p>',
        unsafe_allow_html=True,
    )

    engine_output = st.session_state.engine_output or {}
    profile = st.session_state.profile

    if not assistant:
        st.error("AI assistant unavailable.")
        return

    nba = engine_output.get("next_best_action")
    if nba:
        with st.spinner("Preparing explanation..."):
            auto_explanation = safe_call(assistant.explain_next_best_action, profile, nba)
        st.markdown(
            '<div class="pp-card"><div class="pp-eyebrow">WHY YOUR NEXT STEP IS RECOMMENDED</div>'
            f'<p style="color:var(--text-secondary); font-size:0.92rem; margin-top:6px; margin-bottom:0; line-height:1.55;">{auto_explanation or "Explanation unavailable right now."}</p></div>',
            unsafe_allow_html=True,
        )
        st.write("")

    question = st.text_input(
        "Ask about your learning path...",
        placeholder="e.g. What should I learn next? What is blocking my progress?",
        label_visibility="collapsed",
    )

    st.markdown('<p style="color:var(--text-faint); font-size:0.79rem; margin-bottom:0.5rem; font-weight:500;">SUGGESTED QUESTIONS</p>', unsafe_allow_html=True)
    examples = [
        "What should I learn next?",
        "What is blocking my progress?",
        "How can I improve my path?",
        "Which skill has the highest impact?",
    ]
    example_cols = st.columns(4)
    for col, ex in zip(example_cols, examples):
        with col:
            if st.button(ex, use_container_width=True, key=f"chip_{ex}"):
                question = ex

    if question:
        with st.spinner("Thinking..."):
            answer = safe_call(assistant.answer_path_question, profile, engine_output, question)
        st.markdown(
            '<div class="pp-assistant-answer">'
            '<div class="pp-eyebrow">INSIGHT</div>'
            f'<p style="color:var(--text-primary); font-size:0.93rem; margin-top:6px; margin-bottom:0; line-height:1.6;">{answer or "I couldn\'t generate an answer right now."}</p></div>',
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------
# MAIN APP SHELL
# ----------------------------------------------------------------------
def render_app():
    profile = st.session_state.profile
    engine_output = st.session_state.engine_output

    if profile is None or engine_output is None:
        st.warning("No learner profile found. Please build your path first.")
        if st.button("← Go to Profiling"):
            st.session_state.stage = "profiling"
            st.rerun()
        return

    with st.sidebar:
        st.markdown(
            '<div class="pp-brand"><div class="pp-brand-mark">◆</div>'
            '<div class="pp-brand-name">PathPilot</div></div>'
            '<div class="pp-brand-sub">Intelligent learning paths</div>',
            unsafe_allow_html=True,
        )

        nav_options = ["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"]
        current_index = nav_options.index(st.session_state.nav_section) if st.session_state.nav_section in nav_options else 0
        section = st.radio("Navigate", nav_options, index=current_index, label_visibility="collapsed")
        st.session_state.nav_section = section

        learner_name = getattr(profile, 'name', 'Learner')
        st.markdown(
            f"""
            <div class="pp-user-card">
                <div class="pp-user-avatar">{get_initials(learner_name)}</div>
                <div>
                    <div class="pp-user-name">{learner_name}</div>
                    <div class="pp-user-role">{getattr(profile, 'career_goal', 'N/A')}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("Restart Journey", use_container_width=True):
            for key in ["stage", "profile", "engine_output", "adaptation_state", "roadmap_progress"]:
                st.session_state.pop(key, None)
            init_session_state()
            st.rerun()

    health = (engine_output.get("path_health") or {})
    status = health.get("status", "Unknown")
    score = health.get("health_score", "—")

    st.markdown(
        f"""
        <div class="pp-page-header">
            <div>
                <h1>Good to see you, {getattr(profile, 'name', 'there')}</h1>
                <p>Your learning path, at a glance — continuously analyzed based on your skills, goals and progress.</p>
            </div>
            <div class="pp-status-chip">
                <div class="pp-status-label">Path Status</div>
                <div class="pp-status-value">{status}</div>
                <div class="pp-status-sub">{score} / 100</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if section == "Overview":
        render_dashboard(profile, engine_output, safe_call, engine)
    elif section == "Next Action":
        render_next_best_action()
    elif section == "Learning Roadmap":
        render_roadmap(profile, engine_output, safe_call)
    elif section == "Path Health":
        render_path_health(engine_output)
    elif section == "AI Assistant":
        render_ai_assistant()


def render_path_health(engine_output):
    st.markdown('<div class="pp-eyebrow">DIAGNOSTICS</div><h2 class="pp-section-title">Path Health</h2>', unsafe_allow_html=True)
    health = engine_output.get("path_health") or {}
    risks = engine_output.get("risks") or []

    if not health:
        st.markdown('<div class="pp-card">Path health data unavailable.</div>', unsafe_allow_html=True)
        return

    status = health.get("status", "Unknown")
    score = health.get("health_score", 0)
    try:
        score_num = float(score)
    except (TypeError, ValueError):
        score_num = 0

    gauge_col, factor_col = st.columns([1, 1.4])

    with gauge_col:
        try:
            import plotly.graph_objects as go
            gauge_color = {"Healthy": "#16A34A", "At Risk": "#C4791A", "Critical": "#DC3545"}.get(status, "#5B5CE2")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_num,
                number={"font": {"size": 36, "color": "#1B1D2B", "family": "Plus Jakarta Sans"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#9DA1BC", "tickfont": {"color": "#9DA1BC"}},
                    "bar": {"color": gauge_color},
                    "bgcolor": "#FFFFFF",
                    "borderwidth": 1,
                    "bordercolor": "#E4E7F1",
                    "steps": [
                        {"range": [0, 40], "color": "rgba(220,53,69,0.07)"},
                        {"range": [40, 70], "color": "rgba(196,121,26,0.07)"},
                        {"range": [70, 100], "color": "rgba(22,163,74,0.07)"},
                    ],
                },
                domain={"x": [0, 1], "y": [0, 1]},
            ))
            fig.update_layout(
                height=220, margin=dict(l=20, r=20, t=20, b=10),
                paper_bgcolor="rgba(0,0,0,0)", font_color="#1B1D2B",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.metric("Health Score", score)

        badge_class = status_badge_class(status)
        st.markdown(f'<div style="text-align:center;"><span class="pp-badge {badge_class}">{status}</span></div>', unsafe_allow_html=True)

    with factor_col:
        st.markdown('<div class="pp-eyebrow">CONTRIBUTING FACTORS</div>', unsafe_allow_html=True)
        factors = health.get("contributing_factors", [])
        if factors:
            for f in factors:
                text = str(f)
                icon = "⚠" if any(w in text.lower() for w in ["risk", "tight", "gap", "missing", "low"]) else "✓"
                color = "var(--warning)" if icon == "⚠" else "var(--success)"
                st.markdown(
                    f'<div class="pp-insight-row"><span style="color:{color};">{icon}</span>'
                    f'<span class="pp-insight-text">{text}</span></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown('<p style="color:var(--text-faint);">No contributing factors reported.</p>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="pp-eyebrow">DETECTED RISKS</div>', unsafe_allow_html=True)
    if not risks:
        st.markdown('<div class="pp-card">No active risks detected.</div>', unsafe_allow_html=True)
    else:
        for risk in risks:
            if isinstance(risk, dict):
                severity = str(risk.get("severity", "low")).lower()
                sev_class = {"high": "pp-risk-high", "medium": "pp-risk-medium"}.get(severity, "pp-risk-low")
                message = risk.get("message", "")
                title = risk.get("title") or risk.get("type") or "Risk"
                action = risk.get("suggested_action") or risk.get("action")
                st.markdown(
                    f"""
                    <div class="pp-risk-card {sev_class}">
                        <div class="pp-risk-severity">{severity.upper()} PRIORITY</div>
                        <div class="pp-risk-title">{title}</div>
                        <div class="pp-risk-msg">{message}</div>
                        {f'<div class="pp-risk-action"><b>Recommended Action:</b> {action}</div>' if action else ''}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(f'<div class="pp-risk-card">{risk}</div>', unsafe_allow_html=True)

    if assistant:
        with st.expander("AI Explanation", expanded=False):
            with st.spinner("Generating explanation..."):
                explanation = safe_call(assistant.explain_path_health, st.session_state.profile, health, risks)
            st.write(explanation or "Explanation unavailable right now.")


# ----------------------------------------------------------------------
# ROUTER
# ----------------------------------------------------------------------
stage = st.session_state.stage

if stage == "welcome":
    render_welcome()
elif stage == "profiling":
    render_profiling()
else:
    render_app()

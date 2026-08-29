"""
PathPilot AI — Streamlit application entrypoint.
UI-focused production redesign.
Backend logic and existing engine contracts are preserved.
"""

import json
import streamlit as st

from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant
from ui.roadmap import render_roadmap

from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap


# ======================================================================
# PAGE CONFIG
# ======================================================================

st.set_page_config(
    page_title="PathPilot AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================================================================
# DESIGN SYSTEM
# ======================================================================

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">

    <link href="https://fonts.googleapis.com/css2?
    family=DM+Mono:wght@400;500&
    family=Manrope:wght@400;500;600;700;800&
    family=Inter:wght@400;500;600&
    display=swap"
    rel="stylesheet">

    <style>

    /* ================================================================
       1. DESIGN TOKENS
    ================================================================= */

    :root {
        --bg: #090B10;
        --bg-secondary: #0D1017;

        --surface: #11141C;
        --surface-raised: #151923;
        --surface-hover: #1A1F2B;

        --border: rgba(255,255,255,0.07);
        --border-strong: rgba(255,255,255,0.12);

        --primary: #7C6CFF;
        --primary-soft: rgba(124,108,255,0.12);

        --violet: #9B8CFF;
        --cyan: #5EEAD4;

        --success: #4ADE80;
        --warning: #FBBF24;
        --danger: #FB7185;

        --text-primary: #F5F7FA;
        --text-secondary: #B6BDCA;
        --text-muted: #7F8898;
        --text-faint: #555E6E;

        --font-display: 'Manrope', sans-serif;
        --font-body: 'Inter', sans-serif;
        --font-mono: 'DM Mono', monospace;

        --radius-sm: 10px;
        --radius-md: 16px;
        --radius-lg: 22px;
        --radius-xl: 28px;

        --shadow-soft:
            0 10px 40px rgba(0,0,0,0.22);

        --shadow-card:
            0 12px 35px rgba(0,0,0,0.18);
    }


    /* ================================================================
       2. GLOBAL STYLES
    ================================================================= */

    html,
    body,
    .stApp {
        font-family: var(--font-body);
        color: var(--text-primary);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 15% -10%,
                rgba(124,108,255,0.13),
                transparent 35%
            ),
            radial-gradient(
                circle at 95% 5%,
                rgba(94,234,212,0.05),
                transparent 28%
            ),
            var(--bg);
    }

    h1,
    h2,
    h3,
    h4 {
        font-family: var(--font-display) !important;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1220px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    p {
        line-height: 1.65;
    }


    /* ================================================================
       3. APP SHELL
    ================================================================= */

    .pp-page-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 2rem;

        padding-bottom: 2rem;
        margin-bottom: 2rem;

        border-bottom: 1px solid var(--border);
    }

    .pp-page-header h1 {
        margin: 0 0 0.45rem 0;

        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
    }

    .pp-page-header p {
        margin: 0;

        max-width: 620px;

        color: var(--text-muted);
        font-size: 0.92rem;
    }

    .pp-status-card {
        min-width: 180px;

        padding: 1rem 1.1rem;

        background: rgba(21,25,35,0.75);

        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        box-shadow: var(--shadow-card);
    }

    .pp-status-label {
        display: flex;
        align-items: center;
        gap: 7px;

        font-size: 0.66rem;
        font-family: var(--font-mono);

        letter-spacing: 0.1em;
        text-transform: uppercase;

        color: var(--text-faint);
    }

    .pp-status-dot {
        width: 7px;
        height: 7px;

        border-radius: 50%;

        background: var(--success);
    }

    .pp-status-value {
        margin-top: 0.55rem;

        font-family: var(--font-display);
        font-size: 1.05rem;
        font-weight: 700;
    }

    .pp-status-score {
        margin-top: 0.15rem;

        font-family: var(--font-mono);
        font-size: 0.76rem;

        color: var(--text-muted);
    }


    /* ================================================================
       4. SIDEBAR
    ================================================================= */

    section[data-testid="stSidebar"] {
        background: #0C0F15;

        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.8rem;
    }

    .pp-brand {
        display: flex;
        align-items: center;
        gap: 11px;

        margin-bottom: 0.2rem;
    }

    .pp-brand-mark {
        width: 34px;
        height: 34px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                var(--primary),
                var(--violet)
            );

        color: white;

        font-size: 16px;
        font-weight: 700;

        box-shadow:
            0 8px 22px rgba(124,108,255,0.28);
    }

    .pp-brand-name {
        font-family: var(--font-display);

        font-size: 1.05rem;
        font-weight: 800;

        letter-spacing: -0.03em;
    }

    .pp-brand-sub {
        margin: 0.25rem 0 1.8rem 45px;

        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.61rem;

        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 5px;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label {
        padding: 9px 11px !important;

        border-radius: 9px;

        transition:
            background 0.18s ease,
            color 0.18s ease;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:hover {
        background: rgba(255,255,255,0.035);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:has(input:checked) {
        background: var(--primary-soft);

        border: 1px solid rgba(124,108,255,0.16);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label p {
        font-size: 0.86rem;
        font-weight: 500;

        color: var(--text-muted);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:has(input:checked) p {
        color: var(--text-primary);
    }

    .pp-user-card {
        margin-top: 1.8rem;
        padding-top: 1.2rem;

        border-top: 1px solid var(--border);
    }

    .pp-user-name {
        font-family: var(--font-display);
        font-weight: 700;
        font-size: 0.88rem;
    }

    .pp-user-role {
        margin-top: 3px;

        font-size: 0.73rem;

        color: var(--text-faint);
    }


    /* ================================================================
       5. TYPOGRAPHY
    ================================================================= */

    .pp-eyebrow {
        margin-bottom: 0.45rem;

        font-family: var(--font-mono);
        font-size: 0.68rem;
        font-weight: 500;

        letter-spacing: 0.12em;
        text-transform: uppercase;

        color: var(--cyan);
    }

    .pp-section-title {
        margin: 0;

        font-size: 1.45rem;
        font-weight: 800;

        letter-spacing: -0.035em;
    }

    .pp-section-description {
        margin-top: 0.45rem;

        color: var(--text-muted);
        font-size: 0.9rem;
    }


    /* ================================================================
       6. BUTTONS
    ================================================================= */

    .stButton > button {
        min-height: 42px;

        border-radius: 10px;

        background: var(--surface-raised);

        border: 1px solid var(--border-strong);

        color: var(--text-primary);

        font-family: var(--font-body);
        font-weight: 600;

        transition:
            transform 0.16s ease,
            background 0.16s ease,
            border-color 0.16s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);

        background: var(--surface-hover);

        border-color:
            rgba(124,108,255,0.4);
    }

    div[data-testid="stFormSubmitButton"] > button,
    .pp-primary-action button {
        background:
            linear-gradient(
                135deg,
                #7668F8,
                #8B7CFF
            ) !important;

        border: none !important;

        box-shadow:
            0 10px 28px rgba(124,108,255,0.28);
    }


    /* ================================================================
       7. CARDS
    ================================================================= */

    .pp-card {
        padding: 1.35rem;

        background:
            rgba(20,24,34,0.78);

        border:
            1px solid var(--border);

        border-radius:
            var(--radius-md);

        box-shadow:
            var(--shadow-card);
    }

    .pp-card:hover {
        border-color:
            rgba(255,255,255,0.1);
    }


    /* ================================================================
       8. LANDING PAGE
    ================================================================= */

    .pp-landing {
        max-width: 900px;

        margin: auto;

        padding:
            4.5rem 1rem
            2.5rem;
    }

    .pp-landing-hero {
        text-align: center;
    }

    .pp-landing-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;

        margin-bottom: 1.3rem;
        padding: 0.45rem 0.9rem;

        background:
            rgba(124,108,255,0.08);

        border:
            1px solid rgba(124,108,255,0.2);

        border-radius: 999px;

        color: #B8B1FF;

        font-family: var(--font-mono);
        font-size: 0.7rem;

        letter-spacing: 0.06em;
    }

    .pp-landing h1 {
        margin: 0;

        font-size: clamp(3rem, 6vw, 5rem);
        font-weight: 800;

        letter-spacing: -0.06em;
        line-height: 1;
    }

    .pp-landing h1 span {
        color: var(--violet);
    }

    .pp-landing-subtitle {
        max-width: 620px;

        margin:
            1.2rem auto
            0;

        color: var(--text-secondary);

        font-size: 1.05rem;
        line-height: 1.75;
    }

    .pp-feature {
        min-height: 170px;

        padding: 1.4rem;

        background:
            rgba(17,20,28,0.8);

        border:
            1px solid var(--border);

        border-radius:
            var(--radius-md);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    .pp-feature:hover {
        transform: translateY(-4px);

        border-color:
            rgba(124,108,255,0.28);
    }

    .pp-feature-number {
        margin-bottom: 1rem;

        color: var(--primary);

        font-family: var(--font-mono);
        font-size: 0.72rem;
    }

    .pp-feature-title {
        font-family: var(--font-display);

        font-size: 1rem;
        font-weight: 700;
    }

    .pp-feature-text {
        margin-top: 0.5rem;

        color: var(--text-muted);

        font-size: 0.85rem;
        line-height: 1.65;
    }


    /* ================================================================
       9. ONBOARDING
    ================================================================= */

    .pp-onboarding-header {
        max-width: 620px;

        margin:
            1rem auto
            2.5rem;

        text-align: center;
    }

    .pp-onboarding-header h2 {
        margin: 0;

        font-size: 2rem;

        letter-spacing: -0.04em;
    }

    .pp-step-header {
        display: flex;
        align-items: center;
        gap: 10px;

        margin:
            1.8rem 0
            0.9rem;
    }

    .pp-step-number {
        width: 28px;
        height: 28px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background:
            var(--primary-soft);

        border:
            1px solid rgba(124,108,255,0.25);

        color: var(--violet);

        font-family: var(--font-mono);
        font-size: 0.72rem;
    }

    .pp-step-title {
        font-family: var(--font-display);

        font-size: 1rem;
        font-weight: 700;
    }


    /* ================================================================
       10. DASHBOARD
    ================================================================= */

    .pp-metric-card {
        min-height: 142px;

        padding: 1.2rem;

        background:
            rgba(20,24,34,0.8);

        border:
            1px solid var(--border);

        border-radius:
            var(--radius-md);

        transition:
            transform 0.18s ease,
            border-color 0.18s ease;
    }

    .pp-metric-card:hover {
        transform: translateY(-3px);

        border-color:
            rgba(255,255,255,0.12);
    }

    .pp-metric-label {
        color: var(--text-faint);

        font-size: 0.72rem;
        font-weight: 600;

        text-transform: uppercase;
        letter-spacing: 0.07em;
    }

    .pp-metric-value {
        margin: 0.65rem 0 0.35rem;

        font-family: var(--font-display);

        font-size: 2rem;
        font-weight: 800;

        letter-spacing: -0.04em;
    }

    .pp-metric-description {
        font-size: 0.78rem;

        color: var(--text-muted);
    }

    .trend-good { color: var(--success); }
    .trend-warning { color: var(--warning); }
    .trend-danger { color: var(--danger); }


    /* ================================================================
       11. NEXT BEST ACTION
    ================================================================= */

    .pp-nba-card {
        position: relative;

        padding: 2rem;

        overflow: hidden;

        background:
            linear-gradient(
                135deg,
                rgba(124,108,255,0.13),
                rgba(21,25,35,0.95) 45%
            );

        border:
            1px solid rgba(124,108,255,0.22);

        border-radius:
            var(--radius-lg);
    }

    .pp-nba-label {
        margin-bottom: 0.65rem;

        color: var(--cyan);

        font-family: var(--font-mono);
        font-size: 0.68rem;

        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .pp-nba-skill {
        margin-bottom: 1.6rem;

        font-family: var(--font-display);

        font-size: clamp(1.7rem, 3vw, 2.3rem);
        font-weight: 800;

        letter-spacing: -0.045em;
    }

    .pp-nba-stats {
        display: flex;
        flex-wrap: wrap;

        gap: 2.5rem;
    }

    .pp-nba-stat-label {
        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.65rem;

        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .pp-nba-stat-value {
        margin-top: 0.35rem;

        font-family: var(--font-display);

        font-size: 1.1rem;
        font-weight: 700;
    }

    .pp-nba-reasons {
        margin-top: 1.7rem;
        padding-top: 1.4rem;

        border-top:
            1px solid var(--border);
    }

    .pp-reason {
        display: flex;
        gap: 10px;

        margin-top: 0.75rem;

        color: var(--text-secondary);

        font-size: 0.88rem;
    }

    .pp-reason-icon {
        color: var(--cyan);
    }


    /* ================================================================
       12. ROADMAP
    ================================================================= */

    .pp-roadmap-step {
        padding: 1.2rem 1.3rem;

        background:
            rgba(20,24,34,0.72);

        border:
            1px solid var(--border);

        border-radius:
            var(--radius-md);

        margin-bottom: 0.8rem;
    }

    .pp-roadmap-step-active {
        border-color:
            rgba(124,108,255,0.35);
    }

    .pp-roadmap-step-completed {
        border-color:
            rgba(74,222,128,0.22);
    }

    .pp-roadmap-step-future {
        opacity: 0.72;
    }

    .pp-roadmap-step-number {
        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.68rem;

        letter-spacing: 0.1em;
    }

    .pp-roadmap-skill {
        margin-top: 0.35rem;

        font-family: var(--font-display);

        font-size: 1.08rem;
        font-weight: 700;
    }

    .pp-roadmap-meta {
        margin-top: 0.35rem;

        color: var(--text-muted);

        font-size: 0.78rem;
    }

    .pp-resource-chip {
        display: inline-block;

        margin:
            0.4rem 0.35rem
            0 0;

        padding:
            0.38rem 0.7rem;

        background:
            var(--surface-hover);

        border:
            1px solid var(--border);

        border-radius: 999px;

        color: var(--text-secondary);

        font-size: 0.75rem;
    }


    /* ================================================================
       13. PATH HEALTH
    ================================================================= */

    .pp-health-summary {
        padding: 1.4rem;

        background:
            rgba(20,24,34,0.75);

        border:
            1px solid var(--border);

        border-radius:
            var(--radius-md);
    }

    .pp-risk-card {
        position: relative;

        padding: 1.15rem 1.25rem;

        margin-bottom: 0.75rem;

        background:
            rgba(20,24,34,0.72);

        border:
            1px solid var(--border);

        border-radius:
            var(--radius-md);
    }

    .pp-risk-card-high {
        border-left:
            3px solid rgba(251,113,133,0.75);
    }

    .pp-risk-card-medium {
        border-left:
            3px solid rgba(251,191,36,0.75);
    }

    .pp-risk-card-low {
        border-left:
            3px solid rgba(94,234,212,0.65);
    }

    .pp-risk-top {
        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 1rem;
    }

    .pp-risk-severity {
        padding:
            0.25rem 0.55rem;

        border-radius: 999px;

        font-family: var(--font-mono);
        font-size: 0.62rem;

        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .pp-risk-severity-high {
        background:
            rgba(251,113,133,0.08);

        color: #FDA4AF;
    }

    .pp-risk-severity-medium {
        background:
            rgba(251,191,36,0.08);

        color: #FCD34D;
    }

    .pp-risk-severity-low {
        background:
            rgba(94,234,212,0.07);

        color: var(--cyan);
    }

    .pp-risk-title {
        margin-top: 0.7rem;

        font-family: var(--font-display);

        font-size: 0.95rem;
        font-weight: 700;
    }

    .pp-risk-message {
        margin-top: 0.35rem;

        color: var(--text-muted);

        font-size: 0.84rem;
    }

    .pp-risk-action {
        margin-top: 0.8rem;
        padding-top: 0.75rem;

        border-top:
            1px solid var(--border);

        color: var(--text-secondary);

        font-size: 0.8rem;
    }

    .pp-risk-action-label {
        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.65rem;

        text-transform: uppercase;
    }


    /* ================================================================
       14. AI ASSISTANT
    ================================================================= */

    .pp-assistant-header {
        padding: 1.7rem;

        margin-bottom: 1rem;

        background:
            linear-gradient(
                135deg,
                rgba(124,108,255,0.12),
                rgba(20,24,34,0.75)
            );

        border:
            1px solid rgba(124,108,255,0.18);

        border-radius:
            var(--radius-lg);
    }

    .pp-assistant-title-row {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .pp-assistant-icon {
        width: 42px;
        height: 42px;

        display: flex;
        align-items: center;
        justify-content: center;

        background:
            var(--primary-soft);

        border:
            1px solid rgba(124,108,255,0.22);

        border-radius: 13px;

        color: var(--violet);

        font-size: 1.1rem;
    }

    .pp-assistant-title {
        font-family: var(--font-display);

        font-size: 1.15rem;
        font-weight: 800;
    }

    .pp-assistant-subtitle {
        margin-top: 3px;

        color: var(--text-muted);

        font-size: 0.82rem;
    }

    .pp-question-label {
        margin:
            1.5rem 0
            0.65rem;

        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.65rem;

        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .pp-suggestion {
        width: 100%;

        min-height: 44px;

        background:
            rgba(20,24,34,0.7) !important;

        border:
            1px solid var(--border) !important;

        border-radius: 999px !important;

        color:
            var(--text-secondary) !important;

        font-size: 0.8rem !important;
    }

    .pp-answer-container {
        margin-top: 1.4rem;

        padding: 1.5rem;

        background:
            linear-gradient(
                180deg,
                rgba(25,29,42,0.92),
                rgba(17,20,28,0.92)
            );

        border:
            1px solid rgba(124,108,255,0.2);

        border-radius:
            var(--radius-lg);

        box-shadow:
            0 16px 45px rgba(0,0,0,0.18);
    }

    .pp-answer-header {
        display: flex;
        align-items: center;
        gap: 8px;

        margin-bottom: 0.9rem;

        color: var(--cyan);

        font-family: var(--font-mono);
        font-size: 0.67rem;

        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .pp-answer-content {
        color: var(--text-secondary);

        font-size: 0.92rem;
        line-height: 1.8;
    }


    /* ================================================================
       15. RESPONSIVE ADJUSTMENTS
    ================================================================= */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 1.3rem;
        }

        .pp-page-header {
            flex-direction: column;
        }

        .pp-status-card {
            width: 100%;
        }

        .pp-landing {
            padding-top: 2.5rem;
        }

        .pp-landing h1 {
            font-size: 3rem;
        }

        .pp-nba-card {
            padding: 1.4rem;
        }

        .pp-nba-stats {
            gap: 1.5rem;
        }

        .pp-assistant-header {
            padding: 1.25rem;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ======================================================================
# SESSION STATE
# ======================================================================

def init_session_state():
    defaults = {
        "stage": "welcome",
        "profile": None,
        "engine_output": None,
        "adaptation_state": AdaptationState(),
        "roadmap_progress": {},
        "nav_section": "Overview",
        "assistant_question": "",
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ======================================================================
# BACKEND INITIALIZATION
# ======================================================================

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


# ======================================================================
# HELPERS
# ======================================================================

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
        with open("data/career_paths.json", "r") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return list(data.keys())

        if isinstance(data, list):
            return [
                item.get("career_goal") or item.get("name")
                for item in data
                if isinstance(item, dict)
            ]

    except Exception:
        pass

    return [
        "Machine Learning Engineer",
        "Data Scientist",
        "Full Stack Web Developer",
        "Cybersecurity Analyst",
    ]


def run_engine_pipeline(profile):
    output = {
        "skill_gap": safe_call(
            engine.analyze_skill_gap,
            profile,
        ),

        "readiness": safe_call(
            engine.calculate_readiness_score,
            profile,
        ),

        "next_best_action": safe_call(
            engine.calculate_next_best_action,
            profile,
        ),

        "risks": safe_call(
            engine.detect_risks,
            profile,
        ) or [],

        "path_health": safe_call(
            engine.calculate_path_health,
            profile,
        ),

        "roadmap": safe_call(
            engine.generate_roadmap,
            profile,
        ) or [],
    }

    st.session_state.engine_output = output

    return output


# ======================================================================
# WELCOME
# ======================================================================

def render_welcome():

    st.markdown(
        """
        <div class="pp-landing">

            <div class="pp-landing-hero">

                <div class="pp-landing-badge">
                    ◈ INTELLIGENT LEARNING SYSTEM
                </div>

                <h1>
                    Your next move,
                    <span>decided intelligently.</span>
                </h1>

                <p class="pp-landing-subtitle">
                    PathPilot analyzes where you are, where you want to go,
                    and what is blocking you — then identifies the most
                    valuable thing to learn next.
                </p>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    features = [
        (
            "01",
            "Decide what matters",
            "Move beyond generic course recommendations with a single prioritized next action."
        ),
        (
            "02",
            "Detect the blockers",
            "Understand prerequisite gaps before wasting time on skills you are not ready for."
        ),
        (
            "03",
            "Monitor your path",
            "Track learning health, risks, progress and alignment with your career goal."
        ),
    ]

    for column, feature in zip([col1, col2, col3], features):

        with column:

            st.markdown(
                f"""
                <div class="pp-feature">

                    <div class="pp-feature-number">
                        {feature[0]}
                    </div>

                    <div class="pp-feature-title">
                        {feature[1]}
                    </div>

                    <div class="pp-feature-text">
                        {feature[2]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    st.write("")

    _, center, _ = st.columns([1, 1.4, 1])

    with center:

        st.markdown(
            '<div class="pp-primary-action">',
            unsafe_allow_html=True,
        )

        clicked = st.button(
            "Build My Learning Path →",
            use_container_width=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    if clicked:
        st.session_state.stage = "profiling"
        st.rerun()


# ======================================================================
# PROFILING
# ======================================================================

def render_profiling():

    st.markdown(
        """
        <div class="pp-onboarding-header">

            <div class="pp-eyebrow">
                Personalization
            </div>

            <h2>
                Build your learning profile
            </h2>

            <p class="pp-section-description">
                Your answers help PathPilot understand your current position
                before generating your learning path.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    career_options = get_career_options()

    with st.form("profiling_form"):

        st.markdown(
            """
            <div class="pp-step-header">
                <div class="pp-step-number">01</div>
                <div class="pp-step-title">Your direction</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        name = st.text_input(
            "Name",
            placeholder="Your name",
        )

        career_goal = st.selectbox(
            "Career Goal",
            career_options,
        )

        natural_language_goal = st.text_area(
            "What are you trying to achieve?",
            placeholder=(
                "Example: I want to become job-ready for machine learning "
                "and secure an internship."
            ),
        )

        st.markdown(
            """
            <div class="pp-step-header">
                <div class="pp-step-number">02</div>
                <div class="pp-step-title">Your current position</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        experience_level_label = st.select_slider(
            "Experience Level",
            options=[
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
            value="Beginner",
        )

        experience_map = {
            "Beginner": 1,
            "Intermediate": 3,
            "Advanced": 5,
        }

        current_skills_raw = st.text_input(
            "Current Skills",
            placeholder="Python, SQL, Git",
        )

        interests_raw = st.text_input(
            "Interests",
            placeholder="AI, Data, Web Development",
        )

        st.markdown(
            """
            <div class="pp-step-header">
                <div class="pp-step-number">03</div>
                <div class="pp-step-title">Your constraints</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            weekly_hours = st.number_input(
                "Weekly Learning Hours",
                min_value=1,
                max_value=80,
                value=10,
            )

        with col2:
            timeline_weeks = st.number_input(
                "Target Timeline (weeks)",
                min_value=1,
                max_value=104,
                value=24,
            )

        preferred_learning_style = st.selectbox(
            "Preferred Learning Style",
            [
                "visual",
                "reading",
                "hands-on",
                "video",
                "mixed",
            ],
        )

        st.write("")

        submitted = st.form_submit_button(
            "Generate My Learning Path →"
        )

    if submitted:

        if not name.strip():
            st.error("Please enter your name.")
            return

        current_skills = [
            skill.strip()
            for skill in current_skills_raw.split(",")
            if skill.strip()
        ]

        interests = [
            interest.strip()
            for interest in interests_raw.split(",")
            if interest.strip()
        ]

        try:

            profile = LearnerProfile(
                name=name.strip(),
                career_goal=career_goal,
                natural_language_goal=natural_language_goal.strip(),
                experience_level=experience_map[
                    experience_level_label
                ],
                current_skills=current_skills,
                interests=interests,
                completed_courses=[],
                weekly_hours=int(weekly_hours),
                timeline_weeks=int(timeline_weeks),
                preferred_learning_style=preferred_learning_style,
            )

        except Exception as e:

            st.error(
                f"Could not build your profile: {e}"
            )

            return

        st.session_state.profile = profile

        if engine is None:
            st.error(
                "Intelligence engine is unavailable."
            )
            return

        with st.spinner("Building your learning intelligence..."):
            run_engine_pipeline(profile)

        st.session_state.stage = "app"
        st.rerun()

    if st.button("← Back"):
        st.session_state.stage = "welcome"
        st.rerun()


# ======================================================================
# NEXT BEST ACTION
# ======================================================================

def render_next_best_action():

    st.markdown(
        """
        <div class="pp-eyebrow">
            Decision Intelligence
        </div>

        <h2 class="pp-section-title">
            Your next best action
        </h2>

        <p class="pp-section-description">
            The highest-value next step based on your current learning state.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    engine_output = (
        st.session_state.engine_output
        or {}
    )

    nba = engine_output.get(
        "next_best_action"
    )

    if not nba:

        st.markdown(
            """
            <div class="pp-card">
                No additional recommendation is available right now.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    reasons = nba.get("reasons", [])

    reasons_html = ""

    for reason in reasons:

        reasons_html += f"""
        <div class="pp-reason">
            <span class="pp-reason-icon">✦</span>
            <span>{reason}</span>
        </div>
        """

    st.markdown(
        f"""
        <div class="pp-nba-card">

            <div class="pp-nba-label">
                PathPilot Recommendation
            </div>

            <div class="pp-nba-skill">
                {nba.get("skill", "N/A")}
            </div>

            <div class="pp-nba-stats">

                <div>
                    <div class="pp-nba-stat-label">
                        Confidence
                    </div>

                    <div class="pp-nba-stat-value">
                        {nba.get("score", "N/A")}
                    </div>
                </div>

                <div>
                    <div class="pp-nba-stat-label">
                        Estimated Time
                    </div>

                    <div class="pp-nba-stat-value">
                        {nba.get("est_hours", "N/A")} hrs
                    </div>
                </div>

                <div>
                    <div class="pp-nba-stat-label">
                        Difficulty
                    </div>

                    <div class="pp-nba-stat-value">
                        {nba.get("difficulty", "N/A")}
                    </div>
                </div>

            </div>

            <div class="pp-nba-reasons">

                <div class="pp-eyebrow">
                    Why this matters
                </div>

                {reasons_html}

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    render_adaptive_feedback(nba)


def render_adaptive_feedback(nba):

    st.markdown(
        """
        <div class="pp-question-label">
            How does this recommendation feel?
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    feedback_clicked = None

    with col1:
        if st.button(
            "Too Easy",
            use_container_width=True,
        ):
            feedback_clicked = "too_easy"

    with col2:
        if st.button(
            "Appropriate",
            use_container_width=True,
        ):
            feedback_clicked = "appropriate"

    with col3:
        if st.button(
            "Too Difficult",
            use_container_width=True,
        ):
            feedback_clicked = "too_difficult"

    skill_name = nba.get("skill")

    if (
        feedback_clicked
        and adaptive_engine
        and skill_name
    ):

        result = safe_call(
            adaptive_engine.apply_feedback,
            st.session_state.profile,
            skill_name,
            feedback_clicked,
            st.session_state.adaptation_state,
        )

        if result:

            engine_output = (
                st.session_state.engine_output
                or {}
            )

            if result.get("updated_recommendation") is not None:
                engine_output["next_best_action"] = (
                    result["updated_recommendation"]
                )

            if result.get("updated_path_health") is not None:
                engine_output["path_health"] = (
                    result["updated_path_health"]
                )

            if result.get("updated_risks") is not None:
                engine_output["risks"] = (
                    result["updated_risks"]
                )

            st.session_state.engine_output = engine_output

            st.rerun()


# ======================================================================
# AI ASSISTANT
# ======================================================================

def render_ai_assistant():

    profile = st.session_state.profile
    engine_output = (
        st.session_state.engine_output
        or {}
    )

    st.markdown(
        """
        <div class="pp-assistant-header">

            <div class="pp-assistant-title-row">

                <div class="pp-assistant-icon">
                    ◈
                </div>

                <div>

                    <div class="pp-assistant-title">
                        PathPilot Intelligence
                    </div>

                    <div class="pp-assistant-subtitle">
                        Ask questions about your roadmap, blockers,
                        recommendations and progress.
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pp-question-label">
            Suggested questions
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = [
        (
            "Why this skill?",
            "Why should I learn this next?"
        ),
        (
            "What's blocking me?",
            "What is blocking my progress?"
        ),
        (
            "Am I on track?",
            "Am I on track for my learning goal?"
        ),
        (
            "What should I focus on?",
            "What should I focus on next?"
        ),
    ]

    columns = st.columns(4)

    for column, (label, question) in zip(
        columns,
        suggestions,
    ):

        with column:

            if st.button(
                label,
                key=f"assistant_{label}",
                use_container_width=True,
            ):

                st.session_state.assistant_question = question

    st.write("")

    typed_question = st.text_input(
        "Ask PathPilot",
        value=st.session_state.assistant_question,
        placeholder=(
            "Ask anything about your learning path..."
        ),
    )

    if typed_question:

        st.session_state.assistant_question = typed_question

        with st.spinner("PathPilot is analyzing your learning context..."):

            answer = safe_call(
                assistant.answer_path_question,
                profile,
                engine_output,
                typed_question,
            )

        st.markdown(
            f"""
            <div class="pp-answer-container">

                <div class="pp-answer-header">
                    ◈ PathPilot Analysis
                </div>

                <div class="pp-answer-content">
                    {answer or "I couldn't generate an answer right now."}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ======================================================================
# PATH HEALTH
# ======================================================================

def render_path_health(engine_output):

    health = (
        engine_output.get("path_health")
        or {}
    )

    risks = (
        engine_output.get("risks")
        or []
    )

    st.markdown(
        """
        <div class="pp-eyebrow">
            Learning Diagnostics
        </div>

        <h2 class="pp-section-title">
            Path Health
        </h2>

        <p class="pp-section-description">
            Understand what is helping — and what could slow down —
            your learning journey.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if not health:

        st.markdown(
            """
            <div class="pp-card">
                Path health data is unavailable.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    status = health.get("status", "Unknown")
    score = health.get("health_score", "—")

    col1, col2 = st.columns([1, 1.5])

    with col1:

        st.markdown(
            f"""
            <div class="pp-health-summary">

                <div class="pp-eyebrow">
                    Current Path Status
                </div>

                <div style="
                    font-family: var(--font-display);
                    font-size: 2.2rem;
                    font-weight: 800;
                    margin-top: 0.5rem;
                ">
                    {score}
                </div>

                <div style="
                    color: var(--text-muted);
                    margin-top: 0.2rem;
                    font-size: 0.85rem;
                ">
                    {status}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="pp-eyebrow">
                What's affecting your path
            </div>
            """,
            unsafe_allow_html=True,
        )

        factors = health.get(
            "contributing_factors",
            [],
        )

        if factors:

            for factor in factors:

                st.markdown(
                    f"""
                    <div class="pp-reason">
                        <span class="pp-reason-icon">✦</span>
                        <span>{factor}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.markdown(
                '<p class="pp-section-description">No major factors reported.</p>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.write("")

    st.markdown(
        """
        <div class="pp-eyebrow">
            Active Risks
        </div>

        <h2 class="pp-section-title">
            What needs attention
        </h2>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    if not risks:

        st.markdown(
            """
            <div class="pp-card">
                No active risks detected. Your learning path currently
                has no major blockers.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    for risk in risks:

        if isinstance(risk, dict):

            severity = str(
                risk.get("severity", "low")
            ).lower()

            title = (
                risk.get("title")
                or risk.get("type")
                or "Learning Risk"
            )

            message = risk.get(
                "message",
                "",
            )

            action = (
                risk.get("suggested_action")
                or risk.get("action")
            )

            severity_class = {
                "high": "high",
                "medium": "medium",
            }.get(
                severity,
                "low",
            )

            st.markdown(
                f"""
                <div class="
                    pp-risk-card
                    pp-risk-card-{severity_class}
                ">

                    <div class="pp-risk-top">

                        <span class="
                            pp-risk-severity
                            pp-risk-severity-{severity_class}
                        ">
                            {severity} priority
                        </span>

                    </div>

                    <div class="pp-risk-title">
                        {title}
                    </div>

                    <div class="pp-risk-message">
                        {message}
                    </div>

                    {
                        f'''
                        <div class="pp-risk-action">

                            <div class="pp-risk-action-label">
                                Recommended Action
                            </div>

                            <div style="margin-top: 0.3rem;">
                                {action}
                            </div>

                        </div>
                        '''
                        if action else ""
                    }

                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
                <div class="pp-risk-card pp-risk-card-low">
                    <div class="pp-risk-message">
                        {risk}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ======================================================================
# MAIN APP
# ======================================================================

def render_app():

    profile = st.session_state.profile
    engine_output = st.session_state.engine_output

    if profile is None or engine_output is None:

        st.warning(
            "No learner profile found."
        )

        if st.button("Build My Path"):
            st.session_state.stage = "profiling"
            st.rerun()

        return

    nav_options = [
        "Overview",
        "Next Action",
        "Learning Roadmap",
        "Path Health",
        "AI Assistant",
    ]

    with st.sidebar:

        st.markdown(
            """
            <div class="pp-brand">

                <div class="pp-brand-mark">
                    ◈
                </div>

                <div class="pp-brand-name">
                    PathPilot
                </div>

            </div>

            <div class="pp-brand-sub">
                Learning Intelligence
            </div>
            """,
            unsafe_allow_html=True,
        )

        current_index = (
            nav_options.index(
                st.session_state.nav_section
            )
            if st.session_state.nav_section in nav_options
            else 0
        )

        section = st.radio(
            "Navigate",
            nav_options,
            index=current_index,
            label_visibility="collapsed",
        )

        st.session_state.nav_section = section

        st.markdown(
            f"""
            <div class="pp-user-card">

                <div class="pp-user-name">
                    {getattr(profile, "name", "Learner")}
                </div>

                <div class="pp-user-role">
                    {getattr(profile, "career_goal", "Learning Path")}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "Restart Journey",
            use_container_width=True,
        ):

            for key in [
                "stage",
                "profile",
                "engine_output",
                "adaptation_state",
                "roadmap_progress",
                "assistant_question",
            ]:

                st.session_state.pop(
                    key,
                    None,
                )

            init_session_state()
            st.rerun()

    health = (
        engine_output.get("path_health")
        or {}
    )

    status = health.get("status", "Unknown")
    score = health.get("health_score", "—")

    status_dot_color = {
        "Healthy": "#4ADE80",
        "At Risk": "#FBBF24",
        "Critical": "#FB7185",
    }.get(
        status,
        "#7C6CFF",
    )

    st.markdown(
        f"""
        <div class="pp-page-header">

            <div>

                <div class="pp-eyebrow">
                    Personal Learning Workspace
                </div>

                <h1>
                    Good to see you,
                    {getattr(profile, "name", "there")} 👋
                </h1>

                <p>
                    Your learning path is continuously evaluated against
                    your skills, career goal, timeline and progress.
                </p>

            </div>

            <div class="pp-status-card">

                <div class="pp-status-label">

                    <span
                        class="pp-status-dot"
                        style="background:{status_dot_color};"
                    ></span>

                    Path Status

                </div>

                <div class="pp-status-value">
                    {status}
                </div>

                <div class="pp-status-score">
                    {score} / 100
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if section == "Overview":

        render_dashboard(
            profile,
            engine_output,
            safe_call,
            engine,
        )

    elif section == "Next Action":

        render_next_best_action()

    elif section == "Learning Roadmap":

        render_roadmap(
            profile,
            engine_output,
            safe_call,
        )

    elif section == "Path Health":

        render_path_health(
            engine_output
        )

    elif section == "AI Assistant":

        render_ai_assistant()


# ======================================================================
# ROUTER
# ======================================================================

stage = st.session_state.stage

if stage == "welcome":

    render_welcome()

elif stage == "profiling":

    render_profiling()

else:

    render_app()

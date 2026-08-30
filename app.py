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
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================================
# 1. DESIGN TOKENS  /  2. GLOBAL STYLES
# ======================================================================
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #0A0B0F;
    --surface: #121319;
    --surface-raised: #16171F;
    --surface-elevated: #1C1E29;
    --border: rgba(255,255,255,0.07);
    --border-strong: rgba(255,255,255,0.14);

    --accent: #7C7FF2;
    --accent-soft: rgba(124,127,242,0.10);
    --accent-dim: rgba(124,127,242,0.35);

    --text-primary: #F2F1ED;
    --text-secondary: #A8A8B3;
    --text-muted: #7C7C88;
    --text-faint: #56565F;

    --success: #4ADE80;
    --success-soft: rgba(74,222,128,0.10);
    --warning: #F5B942;
    --warning-soft: rgba(245,185,66,0.10);
    --danger: #F0685C;
    --danger-soft: rgba(240,104,92,0.10);

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
    --radius-lg: 16px;

    --shadow-sm: 0 2px 8px rgba(0,0,0,0.25);
    --shadow-md: 0 8px 24px rgba(0,0,0,0.3);
}

html, body, .stApp, [class*="css"] { font-family: var(--font-body) !important; }
.stApp { background-color: var(--bg); color: var(--text-primary); }
h1, h2, h3, h4, .pp-display { font-family: var(--font-display) !important; letter-spacing: -0.015em; }
#MainMenu, footer, header { visibility: hidden; }
hr { border-color: var(--border); }
.block-container { padding-top: 2.2rem; padding-bottom: 3.5rem; max-width: 1120px; }

/* ======================================================================
   3. APP SHELL
====================================================================== */
.pp-page-header {
    display: flex; justify-content: space-between; align-items: flex-end;
    padding-bottom: var(--space-lg); margin-bottom: var(--space-lg);
    border-bottom: 1px solid var(--border);
    flex-wrap: wrap; gap: var(--space-md);
}
.pp-page-header h1 { font-size: 1.55rem; font-weight: 700; margin: 0 0 4px 0; }
.pp-page-header p { color: var(--text-muted); font-size: 0.92rem; margin: 0; max-width: 440px; }

.pp-status-chip {
    background: var(--surface-raised); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 0.8rem 1.15rem; text-align: right; min-width: 140px;
}
.pp-status-label { font-size: 0.63rem; letter-spacing: 0.1em; color: var(--text-faint); text-transform: uppercase; }
.pp-status-value { font-family: var(--font-mono); font-size: 1.25rem; font-weight: 600; margin-top: 3px; }
.pp-status-sub { color: var(--text-faint); font-size: 0.73rem; font-family: var(--font-mono); }

/* ======================================================================
   4. SIDEBAR
====================================================================== */
section[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--border); }
section[data-testid="stSidebar"] .block-container { padding-top: 1.7rem; }

.pp-brand { display: flex; align-items: center; gap: 9px; margin-bottom: 0.1rem; }
.pp-brand-mark {
    width: 26px; height: 26px; border-radius: 7px;
    background: var(--accent);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; color: #0A0B0F; font-weight: 700;
}
.pp-brand-name { font-family: var(--font-display); font-weight: 700; font-size: 0.98rem; }
.pp-brand-sub {
    font-size: 0.68rem; color: var(--text-faint);
    margin: 0.15rem 0 1.6rem 35px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 1px; }
section[data-testid="stSidebar"] div[role="radiogroup"] label {
    border-radius: var(--radius-sm); padding: 7px 11px !important;
    margin-bottom: 1px; transition: background 0.15s ease; width: 100%;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(124,127,242,0.06); }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: var(--accent-soft); border-left: 2px solid var(--accent);
}
section[data-testid="stSidebar"] div[role="radiogroup"] input { accent-color: var(--accent); }
section[data-testid="stSidebar"] div[role="radiogroup"] label p { font-size: 0.85rem; color: var(--text-muted); font-weight: 500; }
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color: var(--text-primary); }

.pp-user-card { border-top: 1px solid var(--border); margin-top: var(--space-md); padding-top: var(--space-sm); }
.pp-user-name { font-weight: 600; font-size: 0.9rem; }
.pp-user-role { color: var(--text-faint); font-size: 0.74rem; margin-top: 1px; }

/* ======================================================================
   5. TYPOGRAPHY
====================================================================== */
.pp-eyebrow {
    font-size: 0.68rem; letter-spacing: 0.13em; text-transform: uppercase;
    color: var(--accent); font-weight: 600; margin-bottom: 0.4rem;
}
.pp-section-title { font-size: 1.25rem; font-weight: 700; margin: 0 0 var(--space-md) 0; }

/* ======================================================================
   6. BUTTONS
====================================================================== */
.stButton > button {
    background: var(--surface-elevated); color: var(--text-primary);
    border: 1px solid var(--border-strong); border-radius: 8px;
    font-weight: 500; padding: 0.5rem 1rem; transition: all 0.15s ease;
}
.stButton > button:hover { border-color: var(--accent); background: var(--accent-soft); }

div[data-testid="stFormSubmitButton"] > button, .pp-primary-btn button {
    background: var(--accent) !important;
    border: none !important; color: #0A0B0F !important; font-weight: 600 !important;
    box-shadow: var(--shadow-sm);
}
div[data-testid="stFormSubmitButton"] > button:hover, .pp-primary-btn button:hover { opacity: 0.9; }

/* ======================================================================
   7. CARDS
====================================================================== */
.pp-card {
    background: var(--surface-raised); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 1.3rem 1.45rem;
    transition: border-color 0.15s ease;
}
.pp-card:hover { border-color: var(--border-strong); }

/* ======================================================================
   8. LANDING PAGE
====================================================================== */
.pp-landing-hero { text-align: center; padding: 3.2rem 1rem 1.6rem 1rem; }
.pp-landing-badge {
    display: inline-flex; align-items: center; gap: 7px;
    border: 1px solid var(--border-strong); border-radius: 999px;
    padding: 0.38rem 0.95rem; font-size: 0.72rem; color: var(--accent);
    margin-bottom: var(--space-md); font-family: var(--font-mono); letter-spacing: 0.06em;
}
.pp-landing-hero h1 {
    font-size: 2.5rem; font-weight: 800; margin-bottom: 0.75rem; line-height: 1.12;
    color: var(--text-primary);
}
.pp-landing-hero p.pp-tagline { color: var(--text-secondary); font-size: 1.05rem; max-width: 520px; margin: 0 auto; line-height: 1.55; }

.pp-feature-row { display: flex; gap: 0; border-top: 1px solid var(--border); margin-top: var(--space-xl); }
.pp-feature-col {
    flex: 1; padding: 1.5rem 1.5rem; border-right: 1px solid var(--border);
    transition: background 0.15s ease;
}
.pp-feature-col:last-child { border-right: none; }
.pp-feature-col:hover { background: rgba(255,255,255,0.015); }
.pp-feature-num { font-family: var(--font-mono); color: var(--text-faint); font-size: 0.78rem; margin-bottom: 0.5rem; }
.pp-feature-title { font-family: var(--font-display); font-weight: 700; font-size: 1.02rem; margin-bottom: 0.4rem; }
.pp-feature-desc { color: var(--text-muted); font-size: 0.87rem; line-height: 1.5; }

/* ======================================================================
   9. ONBOARDING
====================================================================== */
.pp-onboarding-header { text-align: center; margin-bottom: var(--space-lg); }
.pp-step-header { display: flex; align-items: center; gap: 10px; margin: 1.6rem 0 0.8rem 0; }
.pp-step-num {
    width: 22px; height: 22px; border-radius: 50%; background: var(--surface-elevated);
    border: 1px solid var(--border-strong); display: flex; align-items: center; justify-content: center;
    font-family: var(--font-mono); font-size: 0.7rem; color: var(--accent); flex-shrink: 0;
}
.pp-step-title { font-weight: 600; font-size: 0.95rem; }

/* ======================================================================
   10. DASHBOARD
====================================================================== */
.pp-metric-card {
    background: var(--surface-raised); border: 1px solid var(--border);
    border-radius: var(--radius-md); padding: 1.1rem 1.25rem;
}
.pp-metric-label { font-size: 0.72rem; color: var(--text-faint); font-weight: 500; }
.pp-metric-value { font-family: var(--font-mono); font-size: 1.7rem; font-weight: 600; margin: 0.15rem 0; }
.pp-metric-desc { font-size: 0.75rem; font-weight: 500; }
.trend-good { color: var(--success); }
.trend-warn { color: var(--warning); }
.trend-bad { color: var(--danger); }
.trend-neutral { color: var(--text-faint); }

/* ======================================================================
   11. NEXT BEST ACTION
====================================================================== */
.pp-nba-card {
    background: var(--surface-raised);
    border: 1px solid var(--accent-dim);
    border-radius: var(--radius-lg); padding: 1.9rem 2.1rem; margin-bottom: var(--space-md);
}
.pp-nba-eyebrow { font-family: var(--font-mono); font-size: 0.7rem; letter-spacing: 0.13em; color: var(--accent); text-transform: uppercase; margin-bottom: 0.5rem; }
.pp-nba-skill { font-family: var(--font-display); font-size: 1.85rem; font-weight: 700; margin: 0 0 1.1rem 0; }
.pp-nba-stats { display: flex; gap: 2.2rem; flex-wrap: wrap; }
.pp-nba-stat-label { font-size: 0.7rem; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.06em; }
.pp-nba-stat-value { font-family: var(--font-mono); font-size: 1.18rem; font-weight: 600; margin-top: 2px; }
.pp-nba-why { margin-top: 1.35rem; padding-top: 1.15rem; border-top: 1px solid var(--border); }
.pp-insight-row { display: flex; align-items: flex-start; gap: 9px; padding: 0.38rem 0; }
.pp-insight-check { color: var(--success); font-size: 0.9rem; margin-top: 1px; }
.pp-insight-text { color: var(--text-secondary); font-size: 0.87rem; line-height: 1.5; }

.pp-score-row { margin-bottom: 0.8rem; }
.pp-score-top { display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 5px; }
.pp-score-name { color: var(--text-muted); }
.pp-score-num { font-family: var(--font-mono); font-weight: 600; }
.pp-score-track { background: var(--surface-elevated); border-radius: 6px; height: 6px; overflow: hidden; }
.pp-score-fill { height: 100%; border-radius: 6px; background: var(--accent); }

.pp-badge {
    display: inline-block; padding: 0.26rem 0.75rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; font-family: var(--font-mono);
}
.badge-healthy { background: var(--success-soft); color: var(--success); border: 1px solid rgba(74,222,128,0.25); }
.badge-atrisk { background: var(--warning-soft); color: var(--warning); border: 1px solid rgba(245,185,66,0.25); }
.badge-critical { background: var(--danger-soft); color: var(--danger); border: 1px solid rgba(240,104,92,0.25); }

.pp-chip {
    display: inline-block; background: var(--surface-elevated);
    border: 1px solid var(--border-strong); border-radius: 999px;
    padding: 0.38rem 0.85rem; font-size: 0.79rem; color: var(--text-muted);
    margin: 0 6px 6px 0;
}

/* ======================================================================
   12. ROADMAP (structural rules live in ui/roadmap.py)
====================================================================== */

/* ======================================================================
   13. PATH HEALTH
====================================================================== */
.pp-risk-card {
    background: var(--surface-raised); border: 1px solid var(--border);
    border-left: 3px solid var(--text-faint);
    border-radius: 10px; padding: 0.95rem 1.15rem; margin-bottom: 0.65rem;
}
.pp-risk-high { border-left-color: var(--danger); }
.pp-risk-medium { border-left-color: var(--warning); }
.pp-risk-low { border-left-color: var(--accent); }
.pp-risk-severity { font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 700; }
.pp-risk-high .pp-risk-severity { color: var(--danger); }
.pp-risk-medium .pp-risk-severity { color: var(--warning); }
.pp-risk-low .pp-risk-severity { color: var(--accent); }
.pp-risk-title { font-weight: 600; font-size: 0.95rem; margin: 3px 0 5px 0; }
.pp-risk-msg { color: var(--text-muted); font-size: 0.86rem; margin-bottom: 6px; line-height: 1.5; }
.pp-risk-action { color: var(--text-faint); font-size: 0.8rem; }
.pp-risk-action b { color: var(--text-muted); }

/* ======================================================================
   14. AI ASSISTANT
====================================================================== */
.pp-assistant-answer {
    background: var(--surface-raised); border: 1px solid var(--border-strong);
    border-radius: var(--radius-md); padding: 1.15rem 1.35rem; margin-top: var(--space-sm);
}

/* ======================================================================
   15. RESPONSIVE ADJUSTMENTS
====================================================================== */
@media (max-width: 768px) {
    .pp-landing-hero h1 { font-size: 1.95rem; }
    .pp-nba-skill { font-size: 1.45rem; }
    .pp-nba-stats { gap: 1.2rem; }
    .pp-page-header { flex-direction: column; align-items: flex-start; }
    .pp-status-chip { text-align: left; }
    .pp-feature-row { flex-direction: column; }
    .pp-feature-col { border-right: none; border-bottom: 1px solid var(--border); }
    .pp-feature-col:last-child { border-bottom: none; }
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


# ----------------------------------------------------------------------
# WELCOME
# ----------------------------------------------------------------------
def render_welcome():
    st.markdown(
        '<div class="pp-landing-hero">'
        '<div class="pp-landing-badge">PERSONALIZED LEARNING INTELLIGENCE</div>'
        '<h1>Stop guessing your next move.<br>Decide intelligently.</h1>'
        '<p class="pp-tagline">PathPilot analyzes where you are, where you want to go, and what is '
        'blocking your progress — then tells you exactly what to focus on next.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pp-feature-row">
            <div class="pp-feature-col">
                <div class="pp-feature-num">01</div>
                <div class="pp-feature-title">Decide what matters</div>
                <div class="pp-feature-desc">Move beyond generic course lists to one scored, explainable recommendation.</div>
            </div>
            <div class="pp-feature-col">
                <div class="pp-feature-num">02</div>
                <div class="pp-feature-title">Detect the blockers</div>
                <div class="pp-feature-desc">Identify prerequisite gaps and risks before they slow you down.</div>
            </div>
            <div class="pp-feature-col">
                <div class="pp-feature-num">03</div>
                <div class="pp-feature-title">Monitor your path</div>
                <div class="pp-feature-desc">Track learning health and progress with real signals, not guesswork.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")
    spacer_l, center, spacer_r = st.columns([1, 1, 1])
    with center:
        st.markdown('<div class="pp-primary-btn">', unsafe_allow_html=True)
        clicked = st.button("Build My Learning Path →", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    if clicked:
        st.session_state.stage = "profiling"
        st.rerun()


# ----------------------------------------------------------------------
# PROFILING
# ----------------------------------------------------------------------
def render_profiling():
    st.markdown(
        '<div class="pp-onboarding-header">'
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
            '<div class="pp-step-title">Who are you?</div></div>',
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
            '<div class="pp-step-title">Where are you now?</div></div>',
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
            '<div class="pp-step-title">Your learning constraints</div></div>',
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
        submitted = st.form_submit_button("Generate My Learning Path →")

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
            <div class="pp-nba-eyebrow">PathPilot Recommends</div>
            <div class="pp-nba-skill">{nba.get('skill', 'N/A')}</div>
            <div class="pp-nba-stats">
                <div><div class="pp-nba-stat-label">Confidence Score</div><div class="pp-nba-stat-value">{nba.get('score', 'N/A')}</div></div>
                <div><div class="pp-nba-stat-label">Estimated Time</div><div class="pp-nba-stat-value">{nba.get('est_hours', 'N/A')} hrs</div></div>
                <div><div class="pp-nba-stat-label">Difficulty</div><div class="pp-nba-stat-value">{nba.get('difficulty', 'N/A')}</div></div>
            </div>
            <div class="pp-nba-why">
                <div class="pp-eyebrow">WHY THIS?</div>
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
    st.markdown('<p style="color:var(--text-muted); font-size:0.86rem; margin:1.3rem 0 0.5rem 0;">How does this feel for you?</p>', unsafe_allow_html=True)
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
        '<div class="pp-eyebrow">PATHPILOT INSIGHTS</div>'
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
            f'<p style="color:var(--text-secondary); font-size:0.91rem; margin-top:6px; margin-bottom:0; line-height:1.55;">{auto_explanation or "Explanation unavailable right now."}</p></div>',
            unsafe_allow_html=True,
        )
        st.write("")

    question = st.text_input(
        "Ask about your learning path...",
        placeholder="e.g. What should I learn next? What is blocking my progress?",
        label_visibility="collapsed",
    )

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
            f'<p style="color:var(--text-primary); font-size:0.92rem; margin-top:6px; margin-bottom:0; line-height:1.6;">{answer or "I couldn\'t generate an answer right now."}</p></div>',
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
            '<div class="pp-brand"><div class="pp-brand-mark">✦</div>'
            '<div class="pp-brand-name">PathPilot</div></div>'
            '<div class="pp-brand-sub">Intelligent learning paths</div>',
            unsafe_allow_html=True,
        )

        nav_options = ["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"]
        current_index = nav_options.index(st.session_state.nav_section) if st.session_state.nav_section in nav_options else 0
        section = st.radio("Navigate", nav_options, index=current_index, label_visibility="collapsed")
        st.session_state.nav_section = section

        st.markdown(
            f"""
            <div class="pp-user-card">
                <div class="pp-user-name">{getattr(profile, 'name', 'Learner')}</div>
                <div class="pp-user-role">{getattr(profile, 'career_goal', 'N/A')}</div>
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
            gauge_color = {"Healthy": "#4ADE80", "At Risk": "#F5B942", "Critical": "#F0685C"}.get(status, "#7C7FF2")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_num,
                number={"font": {"size": 36, "color": "#F2F1ED", "family": "JetBrains Mono"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#56565F", "tickfont": {"color": "#56565F"}},
                    "bar": {"color": gauge_color},
                    "bgcolor": "#121319",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40], "color": "rgba(240,104,92,0.08)"},
                        {"range": [40, 70], "color": "rgba(245,185,66,0.08)"},
                        {"range": [70, 100], "color": "rgba(74,222,128,0.08)"},
                    ],
                },
                domain={"x": [0, 1], "y": [0, 1]},
            ))
            fig.update_layout(
                height=220, margin=dict(l=20, r=20, t=20, b=10),
                paper_bgcolor="rgba(0,0,0,0)", font_color="#F2F1ED",
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

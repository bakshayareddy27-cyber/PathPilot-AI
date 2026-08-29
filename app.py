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
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Design system — tokens + global styling
# ----------------------------------------------------------------------
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
    :root {
        --bg: #0B1020;
        --surface: #111827;
        --surface-elevated: #172033;
        --border: rgba(255,255,255,0.08);
        --border-strong: rgba(255,255,255,0.14);
        --indigo: #6366F1;
        --violet: #8B5CF6;
        --cyan: #22D3EE;
        --text-primary: #F8FAFC;
        --text-muted: #94A3B8;
        --text-faint: #64748B;
        --success: #34D399;
        --warning: #FBBF24;
        --danger: #F87171;
        --font-display: 'Sora', sans-serif;
        --font-body: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    html, body, .stApp, [class*="css"] {
        font-family: var(--font-body) !important;
    }
    .stApp { background: var(--bg); color: var(--text-primary); }
    h1, h2, h3, h4, .pp-display { font-family: var(--font-display) !important; letter-spacing: -0.01em; }
    p, span, label, div { color: inherit; }

    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px; }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

    .pp-brand {
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 0.2rem;
    }
    .pp-brand-mark {
        width: 30px; height: 30px; border-radius: 8px;
        background: linear-gradient(135deg, var(--indigo), var(--violet));
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; color: white; font-weight: 700;
    }
    .pp-brand-name { font-family: var(--font-display); font-weight: 700; font-size: 1.02rem; color: var(--text-primary); }
    .pp-brand-sub {
        font-size: 0.66rem; letter-spacing: 0.14em; color: var(--text-faint);
        text-transform: uppercase; margin: 0.1rem 0 1.4rem 40px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 2px; }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        background: transparent;
        border-radius: 8px;
        padding: 8px 12px !important;
        margin-bottom: 2px;
        transition: background 0.15s ease;
        width: 100%;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(99,102,241,0.08);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: rgba(99,102,241,0.14);
        border-left: 2px solid var(--indigo);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] input { accent-color: var(--indigo); }
    section[data-testid="stSidebar"] div[role="radiogroup"] label p {
        font-size: 0.88rem; color: var(--text-muted); font-weight: 500;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
        color: var(--text-primary);
    }

    .pp-user-card {
        border-top: 1px solid var(--border);
        margin-top: 1.4rem; padding-top: 1.1rem;
    }
    .pp-user-name { font-weight: 600; color: var(--text-primary); font-size: 0.92rem; }
    .pp-user-role { color: var(--text-faint); font-size: 0.76rem; margin-top: 1px; }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: var(--surface-elevated);
        color: var(--text-primary);
        border: 1px solid var(--border-strong);
        border-radius: 9px;
        font-weight: 500;
        transition: all 0.15s ease;
        padding: 0.5rem 1rem;
    }
    .stButton > button:hover {
        border-color: var(--indigo);
        background: rgba(99,102,241,0.10);
        color: var(--text-primary);
    }
    div[data-testid="stFormSubmitButton"] > button,
    .pp-primary-btn button {
        background: linear-gradient(135deg, var(--indigo), var(--violet)) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 18px rgba(99,102,241,0.35);
    }
    div[data-testid="stFormSubmitButton"] > button:hover { opacity: 0.92; }

    /* ---------- Cards ---------- */
    .pp-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.3rem 1.5rem;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }
    .pp-card:hover { border-color: var(--border-strong); transform: translateY(-1px); }

    .pp-eyebrow {
        font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--cyan); font-weight: 600; margin-bottom: 0.35rem;
    }

    /* ---------- Hero ---------- */
    .pp-hero {
        display: flex; justify-content: space-between; align-items: center;
        padding: 1.6rem 0 1.8rem 0; border-bottom: 1px solid var(--border);
        margin-bottom: 1.8rem; flex-wrap: wrap; gap: 1rem;
    }
    .pp-hero h1 { font-size: 1.7rem; color: var(--text-primary); margin: 0 0 0.3rem 0; font-weight: 700; }
    .pp-hero p { color: var(--text-muted); font-size: 0.94rem; margin: 0; max-width: 480px; }
    .pp-status-chip {
        background: var(--surface-elevated); border: 1px solid var(--border);
        border-radius: 12px; padding: 0.9rem 1.3rem; text-align: right; min-width: 160px;
    }
    .pp-status-label { font-size: 0.68rem; letter-spacing: 0.1em; color: var(--text-faint); text-transform: uppercase; }
    .pp-status-value { font-family: var(--font-mono); font-size: 1.5rem; font-weight: 600; margin-top: 2px; }

    /* ---------- Landing hero ---------- */
    .pp-landing-hero {
        text-align: center; padding: 3.2rem 1rem 2.4rem 1rem;
    }
    .pp-landing-badge {
        display: inline-flex; align-items: center; gap: 8px;
        border: 1px solid var(--border-strong); border-radius: 999px;
        padding: 0.4rem 1rem; font-size: 0.78rem; color: var(--cyan);
        margin-bottom: 1.4rem; font-family: var(--font-mono);
    }
    .pp-landing-hero h1 {
        font-size: 2.6rem; font-weight: 800; margin-bottom: 0.7rem;
        background: linear-gradient(135deg, #F8FAFC 30%, #A5B4FC 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .pp-landing-hero p.pp-tagline { color: var(--text-muted); font-size: 1.05rem; max-width: 560px; margin: 0 auto; }

    /* ---------- Metric cards ---------- */
    .pp-metric-card {
        background: var(--surface); border: 1px solid var(--border);
        border-radius: 12px; padding: 1.1rem 1.3rem;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }
    .pp-metric-card:hover { border-color: var(--border-strong); transform: translateY(-2px); }
    .pp-metric-label { font-size: 0.74rem; color: var(--text-faint); font-weight: 500; }
    .pp-metric-value { font-family: var(--font-mono); font-size: 1.9rem; font-weight: 600; margin: 0.15rem 0; color: var(--text-primary); }
    .pp-metric-trend { font-size: 0.76rem; font-weight: 500; }
    .trend-good { color: var(--success); }
    .trend-warn { color: var(--warning); }
    .trend-bad { color: var(--danger); }
    .trend-neutral { color: var(--text-faint); }

    /* ---------- NBA hero card ---------- */
    .pp-nba-wrap { position: relative; margin-bottom: 1.2rem; }
    .pp-nba-glow {
        position: absolute; inset: -2px; border-radius: 18px;
        background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(34,211,238,0.18));
        filter: blur(18px); z-index: 0; opacity: 0.55;
    }
    .pp-nba-card {
        position: relative; z-index: 1;
        background: linear-gradient(160deg, #141a2e 0%, #171b30 100%);
        border: 1px solid rgba(139,92,246,0.35);
        border-radius: 16px; padding: 2rem 2.2rem;
    }
    .pp-nba-eyebrow { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.14em; color: var(--cyan); text-transform: uppercase; margin-bottom: 0.5rem; }
    .pp-nba-skill { font-family: var(--font-display); font-size: 2rem; font-weight: 700; color: var(--text-primary); margin: 0 0 1.1rem 0; }
    .pp-nba-stats { display: flex; gap: 2.4rem; flex-wrap: wrap; }
    .pp-nba-stat-label { font-size: 0.72rem; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.06em; }
    .pp-nba-stat-value { font-family: var(--font-mono); font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin-top: 2px; }

    .pp-insight-row { display: flex; align-items: flex-start; gap: 10px; padding: 0.45rem 0; }
    .pp-insight-check { color: var(--success); font-size: 0.95rem; margin-top: 1px; }
    .pp-insight-text { color: var(--text-muted); font-size: 0.9rem; }

    /* ---------- Score bars ---------- */
    .pp-score-row { margin-bottom: 0.85rem; }
    .pp-score-top { display: flex; justify-content: space-between; font-size: 0.85rem; margin-bottom: 5px; }
    .pp-score-name { color: var(--text-muted); }
    .pp-score-num { font-family: var(--font-mono); color: var(--text-primary); font-weight: 600; }
    .pp-score-track { background: var(--surface-elevated); border-radius: 6px; height: 7px; overflow: hidden; }
    .pp-score-fill { height: 100%; border-radius: 6px; background: linear-gradient(90deg, var(--indigo), var(--cyan)); }

    /* ---------- Badges / pills ---------- */
    .pp-badge {
        display: inline-block; padding: 0.28rem 0.8rem; border-radius: 999px;
        font-size: 0.75rem; font-weight: 600; font-family: var(--font-mono);
    }
    .badge-healthy { background: rgba(52,211,153,0.12); color: var(--success); border: 1px solid rgba(52,211,153,0.3); }
    .badge-atrisk { background: rgba(251,191,36,0.12); color: var(--warning); border: 1px solid rgba(251,191,36,0.3); }
    .badge-critical { background: rgba(248,113,113,0.12); color: var(--danger); border: 1px solid rgba(248,113,113,0.3); }

    /* ---------- Risk cards ---------- */
    .pp-risk-card {
        background: var(--surface); border: 1px solid var(--border);
        border-left: 3px solid var(--text-faint);
        border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.7rem;
    }
    .pp-risk-high { border-left-color: var(--danger); }
    .pp-risk-medium { border-left-color: var(--warning); }
    .pp-risk-low { border-left-color: var(--cyan); }
    .pp-risk-severity { font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 700; }
    .pp-risk-high .pp-risk-severity { color: var(--danger); }
    .pp-risk-medium .pp-risk-severity { color: var(--warning); }
    .pp-risk-low .pp-risk-severity { color: var(--cyan); }
    .pp-risk-title { font-weight: 600; font-size: 0.98rem; margin: 3px 0 5px 0; color: var(--text-primary); }
    .pp-risk-msg { color: var(--text-muted); font-size: 0.88rem; margin-bottom: 6px; }
    .pp-risk-action { color: var(--text-faint); font-size: 0.82rem; }
    .pp-risk-action b { color: var(--text-muted); }

    /* ---------- Chips ---------- */
    .pp-chip {
        display: inline-block; background: var(--surface-elevated);
        border: 1px solid var(--border-strong); border-radius: 999px;
        padding: 0.4rem 0.9rem; font-size: 0.82rem; color: var(--text-muted);
        margin: 0 6px 6px 0;
    }

    /* ---------- Timeline (roadmap) ---------- */
    .pp-timeline-item { display: flex; gap: 1.1rem; }
    .pp-timeline-rail { display: flex; flex-direction: column; align-items: center; width: 28px; }
    .pp-timeline-dot {
        width: 26px; height: 26px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
        border: 2px solid var(--text-faint); color: var(--text-faint); background: var(--bg);
        flex-shrink: 0;
    }
    .dot-inprogress { border-color: var(--indigo); color: var(--indigo); background: rgba(99,102,241,0.12); }
    .dot-completed { border-color: var(--success); color: var(--success); background: rgba(52,211,153,0.12); }
    .pp-timeline-line { width: 2px; flex: 1; background: var(--border-strong); margin: 4px 0; min-height: 24px; }
    .pp-timeline-body { flex: 1; padding-bottom: 1.6rem; }
    .pp-step-skill { font-family: var(--font-display); font-size: 1.08rem; font-weight: 600; color: var(--text-primary); margin-bottom: 2px; }
    .pp-step-meta { font-size: 0.8rem; color: var(--text-faint); margin-bottom: 0.7rem; }

    /* ---------- Step markers (profiling) ---------- */
    .pp-step-header {
        display: flex; align-items: center; gap: 10px; margin: 1.4rem 0 0.7rem 0;
    }
    .pp-step-num {
        width: 24px; height: 24px; border-radius: 50%; background: var(--surface-elevated);
        border: 1px solid var(--border-strong); display: flex; align-items: center; justify-content: center;
        font-family: var(--font-mono); font-size: 0.75rem; color: var(--cyan);
    }
    .pp-step-title { font-weight: 600; color: var(--text-primary); font-size: 0.98rem; }

    hr { border-color: var(--border); }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------
# Session state init
# ----------------------------------------------------------------------
def init_session_state():
    defaults = {
        "stage": "welcome",          # welcome -> profiling -> app
        "profile": None,
        "engine_output": None,
        "adaptation_state": AdaptationState(),
        "roadmap_progress": {},       # skill_name -> status
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
    """Runs all deterministic engine calculations once and centralizes output."""
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
        """
        <div class="pp-landing-hero">
            <div class="pp-landing-badge">◈ AI LEARNING INTELLIGENCE</div>
            <h1>PathPilot AI</h1>
            <p class="pp-tagline">Don't just recommend what to learn. Decide what to learn next.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="text-align:center; color:var(--text-muted); max-width:640px; margin:0 auto 2rem auto; font-size:0.95rem;">
        PathPilot continuously analyzes your skills, career goal, prerequisites, available time,
        experience level and interests — then decides, with transparent reasoning, exactly what
        to learn next.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            '<div class="pp-card"><div class="pp-eyebrow">01 · Decide</div>'
            '<b>Next Best Action</b><p style="color:var(--text-muted); font-size:0.88rem; margin-top:6px;">'
            'A single scored recommendation, not just a list.</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="pp-card"><div class="pp-eyebrow">02 · Validate</div>'
            '<b>Prerequisite Intelligence</b><p style="color:var(--text-muted); font-size:0.88rem; margin-top:6px;">'
            'Recursive root-blocker detection prevents unrealistic jumps.</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="pp-card"><div class="pp-eyebrow">03 · Monitor</div>'
            '<b>Path Health</b><p style="color:var(--text-muted); font-size:0.88rem; margin-top:6px;">'
            'Healthy, At Risk or Critical — based on real signals.</p></div>',
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
        '<div class="pp-eyebrow" style="text-align:center;">ONBOARDING</div>'
        '<h2 style="text-align:center; margin-top:0;">Let\'s build your path</h2>'
        '<p style="text-align:center; color:var(--text-muted); margin-bottom:1.6rem;">'
        'Three quick steps. Every answer sharpens your recommendations.</p>',
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
    st.markdown('<div class="pp-eyebrow">DECISION ENGINE</div><h2 style="margin-top:0;">Next Best Action</h2>', unsafe_allow_html=True)

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
        <div class="pp-nba-wrap">
            <div class="pp-nba-glow"></div>
            <div class="pp-nba-card">
                <div class="pp-nba-eyebrow">PathPilot Recommends</div>
                <div class="pp-nba-skill">{nba.get('skill', 'N/A')}</div>
                <div class="pp-nba-stats">
                    <div><div class="pp-nba-stat-label">Confidence Score</div><div class="pp-nba-stat-value">{nba.get('score', 'N/A')}</div></div>
                    <div><div class="pp-nba-stat-label">Estimated Time</div><div class="pp-nba-stat-value">{nba.get('est_hours', 'N/A')} hrs</div></div>
                    <div><div class="pp-nba-stat-label">Difficulty</div><div class="pp-nba-stat-value">{nba.get('difficulty', 'N/A')}</div></div>
                </div>
                <div style="margin-top:1.4rem; padding-top:1.2rem; border-top:1px solid var(--border);">
                    <div class="pp-eyebrow" style="margin-bottom:0.6rem;">WHY THIS?</div>
                    {reasons_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    breakdown = nba.get("score_breakdown", {})
    if breakdown:
        st.markdown('<div class="pp-card" style="margin-top:0.4rem;">', unsafe_allow_html=True)
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
    st.markdown('<p style="color:var(--text-muted); font-size:0.88rem; margin:1.2rem 0 0.5rem 0;">How does this feel for you?</p>', unsafe_allow_html=True)
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
        '<div class="pp-eyebrow">ASK PATHPILOT</div>'
        '<h2 style="margin-top:0;">AI Assistant</h2>'
        '<p style="color:var(--text-muted); margin-top:-0.6rem;">'
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
        st.markdown('<div class="pp-card"><div class="pp-eyebrow">WHY YOUR NEXT STEP IS RECOMMENDED</div>' +
                    f'<p style="color:var(--text-muted); font-size:0.92rem; margin-top:6px;">{auto_explanation or "Explanation unavailable right now."}</p></div>',
                    unsafe_allow_html=True)
        st.write("")

    question = st.text_input(
        "Ask about your learning path...",
        placeholder="e.g. Why should I learn this next? What's blocking my progress? Am I on track?",
        label_visibility="collapsed",
    )

    examples = ["Why this skill?", "What's blocking me?", "Am I on track?", "What should I focus on?"]
    example_cols = st.columns(4)
    for col, ex in zip(example_cols, examples):
        with col:
            if st.button(ex, use_container_width=True, key=f"chip_{ex}"):
                question = ex.replace("this skill?", "should I learn this next?").replace("blocking me?", "is blocking my progress?")

    if question:
        with st.spinner("Thinking..."):
            answer = safe_call(assistant.answer_path_question, profile, engine_output, question)
        st.markdown(
            '<div class="pp-card" style="border-color: rgba(139,92,246,0.3); margin-top:0.8rem;">'
            '<div class="pp-eyebrow">ANSWER</div>'
            f'<p style="color:var(--text-primary); font-size:0.94rem; margin-top:6px;">{answer or "I couldn\'t generate an answer right now."}</p></div>',
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
            '<div class="pp-brand"><div class="pp-brand-mark">◈</div>'
            '<div class="pp-brand-name">PathPilot</div></div>'
            '<div class="pp-brand-sub">AI Learning Intelligence</div>',
            unsafe_allow_html=True,
        )

        section = st.radio(
            "Navigate",
            ["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"],
            index=["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"].index(
                st.session_state.nav_section
            ) if st.session_state.nav_section in
            ["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"] else 0,
            label_visibility="collapsed",
        )
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
        <div class="pp-hero">
            <div>
                <h1>Good to see you, {getattr(profile, 'name', 'there')} 👋</h1>
                <p>Your learning path is being continuously analyzed based on your skills, goals, timeline and progress.</p>
            </div>
            <div class="pp-status-chip">
                <div class="pp-status-label">● Path Status</div>
                <div class="pp-status-value">{status}</div>
                <div style="color:var(--text-faint); font-size:0.78rem; font-family: var(--font-mono);">{score} / 100</div>
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
    st.markdown('<div class="pp-eyebrow">DIAGNOSTICS</div><h2 style="margin-top:0;">Path Health</h2>', unsafe_allow_html=True)
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
            gauge_color = {"Healthy": "#34D399", "At Risk": "#FBBF24", "Critical": "#F87171"}.get(status, "#6366F1")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_num,
                number={"suffix": "", "font": {"size": 40, "color": "#F8FAFC", "family": "JetBrains Mono"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#64748B", "tickfont": {"color": "#64748B"}},
                    "bar": {"color": gauge_color},
                    "bgcolor": "#111827",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40], "color": "rgba(248,113,113,0.12)"},
                        {"range": [40, 70], "color": "rgba(251,191,36,0.12)"},
                        {"range": [70, 100], "color": "rgba(52,211,153,0.12)"},
                    ],
                },
                domain={"x": [0, 1], "y": [0, 1]},
            ))
            fig.update_layout(
                height=240, margin=dict(l=20, r=20, t=20, b=10),
                paper_bgcolor="rgba(0,0,0,0)", font_color="#F8FAFC",
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.metric("Health Score", score)

        badge_class = status_badge_class(status)
        st.markdown(f'<div style="text-align:center;"><span class="pp-badge {badge_class}">{status}</span></div>', unsafe_allow_html=True)

    with factor_col:
        st.markdown('<div class="pp-eyebrow">WHAT\'S AFFECTING YOUR PATH?</div>', unsafe_allow_html=True)
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

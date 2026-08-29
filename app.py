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

# ======================================================================
# DESIGN SYSTEM
# ======================================================================
st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>

    /* ---------------------------------------------------------------
       1. DESIGN TOKENS
    --------------------------------------------------------------- */
    :root {
        --bg: #0A0E1A;
        --bg-atmosphere: radial-gradient(circle at 20% 0%, rgba(99,102,241,0.10) 0%, transparent 45%),
                          radial-gradient(circle at 85% 15%, rgba(34,211,238,0.06) 0%, transparent 40%);
        --surface: #10141F;
        --surface-raised: #151A28;
        --surface-elevated: #1A2033;
        --border: rgba(255,255,255,0.07);
        --border-strong: rgba(255,255,255,0.13);

        --indigo: #6366F1;
        --indigo-soft: rgba(99,102,241,0.12);
        --violet: #8B5CF6;
        --cyan: #22D3EE;

        --text-primary: #F4F6FB;
        --text-secondary: #B4BCCC;
        --text-muted: #8992A6;
        --text-faint: #5B6478;

        --success: #34D399;
        --warning: #F5B942;
        --danger: #F0685C;

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
    }

    /* ---------------------------------------------------------------
       2. GLOBAL STYLES
    --------------------------------------------------------------- */
    html, body, .stApp, [class*="css"] {
        font-family: var(--font-body) !important;
    }
    .stApp {
        background-color: var(--bg);
        background-image: var(--bg-atmosphere);
        background-attachment: fixed;
        color: var(--text-primary);
    }
    h1, h2, h3, h4, .pp-display { font-family: var(--font-display) !important; letter-spacing: -0.015em; }
    #MainMenu, footer, header { visibility: hidden; }
    hr { border-color: var(--border); }

    /* ---------------------------------------------------------------
       3. APP SHELL
    --------------------------------------------------------------- */
    .block-container { padding-top: 2.2rem; padding-bottom: 3.5rem; max-width: 1160px; }

    .pp-page-header {
        display: flex; justify-content: space-between; align-items: center;
        padding-bottom: var(--space-lg); margin-bottom: var(--space-lg);
        border-bottom: 1px solid var(--border);
        flex-wrap: wrap; gap: var(--space-md);
    }
    .pp-page-header h1 { font-size: 1.65rem; font-weight: 700; margin: 0 0 4px 0; }
    .pp-page-header p { color: var(--text-muted); font-size: 0.93rem; margin: 0; max-width: 460px; }

    .pp-status-chip {
        background: var(--surface-raised); border: 1px solid var(--border);
        border-radius: var(--radius-md); padding: 0.85rem 1.2rem; text-align: right; min-width: 150px;
    }
    .pp-status-label { font-size: 0.65rem; letter-spacing: 0.1em; color: var(--text-faint); text-transform: uppercase; }
    .pp-status-value { font-family: var(--font-mono); font-size: 1.35rem; font-weight: 600; margin-top: 3px; }
    .pp-status-sub { color: var(--text-faint); font-size: 0.75rem; font-family: var(--font-mono); }

    /* ---------------------------------------------------------------
       4. SIDEBAR
    --------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background: var(--surface); border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.6rem; }

    .pp-brand { display: flex; align-items: center; gap: 10px; margin-bottom: 0.15rem; }
    .pp-brand-mark {
        width: 30px; height: 30px; border-radius: 8px;
        background: linear-gradient(135deg, var(--indigo), var(--violet));
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; color: white; font-weight: 700;
    }
    .pp-brand-name { font-family: var(--font-display); font-weight: 700; font-size: 1.02rem; }
    .pp-brand-sub {
        font-size: 0.64rem; letter-spacing: 0.15em; color: var(--text-faint);
        text-transform: uppercase; margin: 0.1rem 0 1.5rem 40px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] { gap: 1px; }
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        border-radius: var(--radius-sm); padding: 8px 12px !important;
        margin-bottom: 1px; transition: background 0.15s ease; width: 100%;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover { background: rgba(99,102,241,0.07); }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        background: var(--indigo-soft); border-left: 2px solid var(--indigo);
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] input { accent-color: var(--indigo); }
    section[data-testid="stSidebar"] div[role="radiogroup"] label p { font-size: 0.87rem; color: var(--text-muted); font-weight: 500; }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p { color: var(--text-primary); }

    .pp-user-card { border-top: 1px solid var(--border); margin-top: var(--space-md); padding-top: var(--space-sm); }
    .pp-user-name { font-weight: 600; font-size: 0.92rem; }
    .pp-user-role { color: var(--text-faint); font-size: 0.76rem; margin-top: 1px; }

    /* ---------------------------------------------------------------
       5. TYPOGRAPHY HELPERS
    --------------------------------------------------------------- */
    .pp-eyebrow {
        font-size: 0.7rem; letter-spacing: 0.13em; text-transform: uppercase;
        color: var(--cyan); font-weight: 600; margin-bottom: 0.4rem;
    }
    .pp-section-title { font-size: 1.3rem; font-weight: 700; margin: 0 0 var(--space-md) 0; }

    /* ---------------------------------------------------------------
       6. BUTTONS
    --------------------------------------------------------------- */
    .stButton > button {
        background: var(--surface-elevated); color: var(--text-primary);
        border: 1px solid var(--border-strong); border-radius: 9px;
        font-weight: 500; padding: 0.5rem 1rem; transition: all 0.15s ease;
    }
    .stButton > button:hover { border-color: var(--indigo); background: rgba(99,102,241,0.10); }

    div[data-testid="stFormSubmitButton"] > button, .pp-primary-btn button {
        background: linear-gradient(135deg, var(--indigo), var(--violet)) !important;
        border: none !important; color: white !important; font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(99,102,241,0.28);
    }
    div[data-testid="stFormSubmitButton"] > button:hover, .pp-primary-btn button:hover { opacity: 0.93; }

    /* ---------------------------------------------------------------
       7. CARDS
    --------------------------------------------------------------- */
    .pp-card {
        background: var(--surface-raised); border: 1px solid var(--border);
        border-radius: var(--radius-md); padding: 1.35rem 1.5rem;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }
    .pp-card:hover { border-color: var(--border-strong); }

    /* ---------------------------------------------------------------
       8. LANDING PAGE
    --------------------------------------------------------------- */
    .pp-landing-hero { text-align: center; padding: 3.4rem 1rem 2.2rem 1rem; }
    .pp-landing-badge {
        display: inline-flex; align-items: center; gap: 7px;
        border: 1px solid var(--border-strong); border-radius: 999px;
        padding: 0.4rem 1rem; font-size: 0.76rem; color: var(--cyan);
        margin-bottom: var(--space-md); font-family: var(--font-mono);
        background: rgba(34,211,238,0.05);
    }
    .pp-landing-hero h1 {
        font-size: 2.75rem; font-weight: 800; margin-bottom: 0.7rem; line-height: 1.1;
        background: linear-gradient(135deg, #F4F6FB 30%, #B4BCFF 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .pp-landing-hero p.pp-tagline { color: var(--text-secondary); font-size: 1.08rem; max-width: 560px; margin: 0 auto; }
    .pp-feature-card {
        background: var(--surface-raised); border: 1px solid var(--border);
        border-radius: var(--radius-md); padding: 1.4rem 1.5rem; height: 100%;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }
    .pp-feature-card:hover { border-color: rgba(99,102,241,0.4); transform: translateY(-2px); }
    .pp-feature-card b { font-size: 1rem; }
    .pp-feature-card p { color: var(--text-muted); font-size: 0.87rem; margin-top: 6px; }

    /* ---------------------------------------------------------------
       9. ONBOARDING / PROFILING
    --------------------------------------------------------------- */
    .pp-step-header { display: flex; align-items: center; gap: 10px; margin: 1.6rem 0 0.8rem 0; }
    .pp-step-num {
        width: 24px; height: 24px; border-radius: 50%; background: var(--surface-elevated);
        border: 1px solid var(--border-strong); display: flex; align-items: center; justify-content: center;
        font-family: var(--font-mono); font-size: 0.74rem; color: var(--cyan); flex-shrink: 0;
    }
    .pp-step-title { font-weight: 600; font-size: 0.98rem; }
    .pp-onboarding-header { text-align: center; margin-bottom: var(--space-lg); }

    /* ---------------------------------------------------------------
       10. DASHBOARD / METRICS
    --------------------------------------------------------------- */
    .pp-metric-card {
        background: var(--surface-raised); border: 1px solid var(--border);
        border-radius: var(--radius-md); padding: 1.15rem 1.3rem;
        transition: border-color 0.15s ease, transform 0.15s ease;
    }
    .pp-metric-card:hover { border-color: var(--border-strong); transform: translateY(-2px); }
    .pp-metric-label { font-size: 0.73rem; color: var(--text-faint); font-weight: 500; }
    .pp-metric-value { font-family: var(--font-mono); font-size: 1.85rem; font-weight: 600; margin: 0.15rem 0; }
    .pp-metric-desc { font-size: 0.76rem; font-weight: 500; }
    .trend-good { color: var(--success); }
    .trend-warn { color: var(--warning); }
    .trend-bad { color: var(--danger); }
    .trend-neutral { color: var(--text-faint); }

    /* ---------------------------------------------------------------
       11. NEXT BEST ACTION
    --------------------------------------------------------------- */
    .pp-nba-card {
        background: linear-gradient(160deg, #12172A 0%, #151B30 100%);
        border: 1px solid rgba(139,92,246,0.28);
        border-radius: var(--radius-lg); padding: 2rem 2.2rem; margin-bottom: var(--space-md);
    }
    .pp-nba-eyebrow { font-family: var(--font-mono); font-size: 0.72rem; letter-spacing: 0.14em; color: var(--cyan); text-transform: uppercase; margin-bottom: 0.5rem; }
    .pp-nba-skill { font-family: var(--font-display); font-size: 1.95rem; font-weight: 700; margin: 0 0 1.15rem 0; }
    .pp-nba-stats { display: flex; gap: 2.4rem; flex-wrap: wrap; }
    .pp-nba-stat-label { font-size: 0.71rem; color: var(--text-faint); text-transform: uppercase; letter-spacing: 0.06em; }
    .pp-nba-stat-value { font-family: var(--font-mono); font-size: 1.22rem; font-weight: 600; margin-top: 2px; }
    .pp-nba-why { margin-top: 1.4rem; padding-top: 1.2rem; border-top: 1px solid var(--border); }
    .pp-insight-row { display: flex; align-items: flex-start; gap: 10px; padding: 0.4rem 0; }
    .pp-insight-check { color: var(--success); font-size: 0.92rem; margin-top: 1px; }
    .pp-insight-text { color: var(--text-secondary); font-size: 0.89rem; }

    .pp-score-row { margin-bottom: 0.85rem; }
    .pp-score-top { display: flex; justify-content: space-between; font-size: 0.84rem; margin-bottom: 5px; }
    .pp-score-name { color: var(--text-muted); }
    .pp-score-num { font-family: var(--font-mono); font-weight: 600; }
    .pp-score-track { background: var(--surface-elevated); border-radius: 6px; height: 6px; overflow: hidden; }
    .pp-score-fill { height: 100%; border-radius: 6px; background: linear-gradient(90deg, var(--indigo), var(--cyan)); }

    .pp-badge {
        display: inline-block; padding: 0.28rem 0.8rem; border-radius: 999px;
        font-size: 0.74rem; font-weight: 600; font-family: var(--font-mono);
    }
    .badge-healthy { background: rgba(52,211,153,0.10); color: var(--success); border: 1px solid rgba(52,211,153,0.25); }
    .badge-atrisk { background: rgba(245,185,66,0.10); color: var(--warning); border: 1px solid rgba(245,185,66,0.25); }
    .badge-critical { background: rgba(240,104,92,0.10); color: var(--danger); border: 1px solid rgba(240,104,92,0.25); }

    .pp-chip {
        display: inline-block; background: var(--surface-elevated);
        border: 1px solid var(--border-strong); border-radius: 999px;
        padding: 0.4rem 0.9rem; font-size: 0.81rem; color: var(--text-muted);
        margin: 0 6px 6px 0; transition: border-color 0.15s ease;
    }
    .pp-chip:hover { border-color: var(--indigo); color: var(--text-primary); }

    /* ---------------------------------------------------------------
       12. ROADMAP  (see ui/roadmap.py for structural markup)
    --------------------------------------------------------------- */
    .pp-timeline-rail { display: flex; flex-direction: column; align-items: center; width: 28px; }
    .pp-timeline-dot {
        width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
        font-family: var(--font-mono); font-size: 0.72rem; font-weight: 700;
        border: 2px solid var(--text-faint); color: var(--text-faint); background: var(--bg); flex-shrink: 0;
    }
    .dot-inprogress { border-color: var(--indigo); color: var(--indigo); background: var(--indigo-soft); }
    .dot-completed { border-color: var(--success); color: var(--success); background: rgba(52,211,153,0.10); }
    .pp-timeline-line { width: 2px; flex: 1; background: var(--border-strong); margin: 4px 0; min-height: 22px; }
    .pp-step-skill { font-family: var(--font-display); font-size: 1.05rem; font-weight: 600; margin-bottom: 2px; }
    .pp-step-meta { font-size: 0.79rem; color: var(--text-faint); margin-bottom: 0.7rem; }

    /* ---------------------------------------------------------------
       13. PATH HEALTH
    --------------------------------------------------------------- */
    .pp-risk-card {
        background: var(--surface-raised); border: 1px solid var(--border);
        border-left: 3px solid var(--text-faint);
        border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.7rem;
    }
    .pp-risk-high { border-left-color: var(--danger); }
    .pp-risk-medium { border-left-color: var(--warning); }
    .pp-risk-low { border-left-color: var(--cyan); }
    .pp-risk-severity { font-size: 0.67rem; letter-spacing: 0.1em; text-transform: uppercase; font-weight: 700; }
    .pp-risk-high .pp-risk-severity { color: var(--danger); }
    .pp-risk-medium .pp-risk-severity { color: var(--warning); }
    .pp-risk-low .pp-risk-severity { color: var(--cyan); }
    .pp-risk-title { font-weight: 600; font-size: 0.97rem; margin: 3px 0 5px 0; }
    .pp-risk-msg { color: var(--text-muted); font-size: 0.87rem; margin-bottom: 6px; }
    .pp-risk-action { color: var(--text-faint); font-size: 0.81rem; }
    .pp-risk-action b { color: var(--text-muted); }

    /* ---------------------------------------------------------------
       14. AI ASSISTANT
    --------------------------------------------------------------- */
    .pp-assistant-answer {
        background: var(--surface-raised); border: 1px solid rgba(139,92,246,0.25);
        border-radius: var(--radius-md); padding: 1.2rem 1.4rem; margin-top: var(--space-sm);
    }

    /* ---------------------------------------------------------------
       15. RESPONSIVE ADJUSTMENTS
    --------------------------------------------------------------- */
    @media (max-width: 768px) {
        .pp-landing-hero h1 { font-size: 2.1rem; }
        .pp-nba-skill { font-size: 1.55rem; }
        .pp-nba-stats { gap: 1.3rem; }
        .pp-page-header { flex-direction: column; align-items: flex-start; }
        .pp-status-chip { text-align: left; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
        <p style="text-align:center; color:var(--text-muted); max-width:620px; margin:0 auto 2.2rem auto; font-size:0.95rem; line-height:1.6;">
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
            '<div class="pp-feature-card"><div class="pp-eyebrow">01 · DECIDE</div>'
            '<b>Next Best Action</b><p>A single scored recommendation, not just a list.</p></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="pp-feature-card"><div class="pp-eyebrow">02 · VALIDATE</div>'
            '<b>Prerequisite Intelligence</b><p>Recursive root-blocker detection prevents unrealistic jumps.</p></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="pp-feature-card"><div class="pp-eyebrow">03 · MONITOR</div>'
            '<b>Path Health</b><p>Healthy, At Risk or Critical — based on real signals.</p></div>',
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
    st.markdown('<p style="color:var(--text-muted); font-size:0.87rem; margin:1.3rem 0 0.5rem 0;">How does this feel for you?</p>', unsafe_allow_html=True)
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
        '<h2 class="pp-section-title" style="margin-bottom:0.2rem;">AI Assistant</h2>'
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
            f'<p style="color:var(--text-secondary); font-size:0.92rem; margin-top:6px; margin-bottom:0;">{auto_explanation or "Explanation unavailable right now."}</p></div>',
            unsafe_allow_html=True,
        )
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
            '<div class="pp-assistant-answer">'
            '<div class="pp-eyebrow">ANSWER</div>'
            f'<p style="color:var(--text-primary); font-size:0.93rem; margin-top:6px; margin-bottom:0;">{answer or "I couldn\'t generate an answer right now."}</p></div>',
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
                <h1>Good to see you, {getattr(profile, 'name', 'there')} 👋</h1>
                <p>Your learning path is being continuously analyzed based on your skills, goals, timeline and progress.</p>
            </div>
            <div class="pp-status-chip">
                <div class="pp-status-label">● Path Status</div>
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
            gauge_color = {"Healthy": "#34D399", "At Risk": "#F5B942", "Critical": "#F0685C"}.get(status, "#6366F1")
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_num,
                number={"font": {"size": 38, "color": "#F4F6FB", "family": "JetBrains Mono"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#5B6478", "tickfont": {"color": "#5B6478"}},
                    "bar": {"color": gauge_color},
                    "bgcolor": "#10141F",
                    "borderwidth": 0,
                    "steps": [
                        {"range": [0, 40], "color": "rgba(240,104,92,0.10)"},
                        {"range": [40, 70], "color": "rgba(245,185,66,0.10)"},
                        {"range": [70, 100], "color": "rgba(52,211,153,0.10)"},
                    ],
                },
                domain={"x": [0, 1], "y": [0, 1]},
            ))
            fig.update_layout(
                height=230, margin=dict(l=20, r=20, t=20, b=10),
                paper_bgcolor="rgba(0,0,0,0)", font_color="#F4F6FB",
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

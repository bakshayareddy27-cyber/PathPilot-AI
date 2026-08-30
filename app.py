import json
import html
from textwrap import dedent

import streamlit as st

from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant
from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PathPilot AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL DESIGN SYSTEM
# ============================================================

st.markdown(
    dedent("""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --bg: #F6F7FB;
        --surface: #FFFFFF;
        --surface-soft: #FAFBFF;
        --text: #172033;
        --muted: #6B7280;
        --line: #E7EAF1;

        --primary: #5B5CE2;
        --primary-dark: #4849C8;
        --primary-soft: #F0F0FF;

        --green: #16A36A;
        --green-soft: #EAF9F1;

        --orange: #E38B24;
        --orange-soft: #FFF5E8;

        --red: #E25555;
        --red-soft: #FFF0F0;
    }

    html,
    body,
    [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(115, 110, 255, 0.08), transparent 25%),
            radial-gradient(circle at 5% 25%, rgba(100, 160, 255, 0.05), transparent 22%),
            #F6F7FB;
        color: var(--text);
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--text) !important;
        letter-spacing: -0.035em;
    }

    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(180deg, #151827 0%, #10131F 100%);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] * {
        color: #F6F7FB;
    }

    section[data-testid="stSidebar"] .stRadio label {
        border-radius: 12px;
        padding: 10px 12px;
        margin-bottom: 4px;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.08);
        transform: translateX(3px);
    }

    section[data-testid="stSidebar"] .stButton button {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        color: white !important;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.12) !important;
    }

    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button,
    .stFormSubmitButton > button {

        min-height: 46px !important;

        border-radius: 13px !important;

        border: 1px solid #E2E6EF !important;

        font-family: 'DM Sans', sans-serif !important;

        font-weight: 700 !important;

        transition:
            transform 0.18s ease,
            box-shadow 0.18s ease,
            border-color 0.18s ease !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {

        transform: translateY(-2px);

        box-shadow: 0 12px 28px rgba(30,40,80,0.12);

        border-color: #C6C7FF !important;
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button {

        background:
            linear-gradient(135deg, #5556D8, #7472E9) !important;

        border: none !important;

        color: white !important;

        box-shadow: 0 10px 24px rgba(91,92,226,0.22);
    }

    /* ========================================================
       INPUTS
    ======================================================== */

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {

        background: #FFFFFF !important;

        color: #172033 !important;

        border: 1px solid #DDE2EB !important;

        border-radius: 13px !important;

        transition:
            border-color 0.2s ease,
            box-shadow 0.2s ease !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stNumberInput input:focus {

        border-color: #7778EA !important;

        box-shadow:
            0 0 0 4px rgba(91,92,226,0.10) !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {

        background: #FFFFFF !important;

        border-radius: 13px !important;

        border-color: #DDE2EB !important;
    }

    /* ========================================================
       CARDS
    ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background: rgba(255,255,255,0.94);

        border: 1px solid #E6EAF1 !important;

        border-radius: 20px !important;

        box-shadow:
            0 8px 28px rgba(25,35,65,0.045);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            border-color 0.2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {

        border-color: #D5D9F0 !important;

        box-shadow:
            0 14px 34px rgba(30,40,75,0.075);
    }

    /* ========================================================
       METRICS
    ======================================================== */

    div[data-testid="stMetric"] {

        background: #FFFFFF;

        border: 1px solid #E7EAF1;

        border-radius: 18px;

        padding: 18px;

        box-shadow: 0 6px 20px rgba(25,35,65,0.04);
    }

    /* ========================================================
       EXPANDERS
    ======================================================== */

    details {

        background: #FFFFFF !important;

        border: 1px solid #E5E8EF !important;

        border-radius: 15px !important;

        margin-bottom: 10px;
    }

    /* ========================================================
       PROGRESS
    ======================================================== */

    div[data-testid="stProgress"] > div > div {

        background: linear-gradient(
            90deg,
            #5B5CE2,
            #8987FF
        ) !important;
    }

    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 760px) {

        .block-container {
            padding: 1.2rem 1rem 3rem 1rem;
        }

    }

    </style>
    """),
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def esc(value):
    return html.escape(str(value if value is not None else "—"))


def render_html(content):
    st.markdown(
        dedent(content).strip(),
        unsafe_allow_html=True,
    )


def hero(eyebrow, title, subtitle):

    render_html(f"""
    <div style="margin-bottom:30px;">

        <div style="
            display:inline-flex;
            align-items:center;
            padding:6px 11px;
            border-radius:999px;
            background:#F0F0FF;
            color:#5B5CE2;
            font-size:10px;
            font-weight:800;
            letter-spacing:.11em;
            text-transform:uppercase;
            margin-bottom:12px;
        ">
            ✦ {esc(eyebrow)}
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(32px,4vw,48px);
            font-weight:800;
            letter-spacing:-.05em;
            line-height:1.08;
            color:#172033;
        ">
            {title}
        </div>

        <div style="
            max-width:720px;
            margin-top:11px;
            font-size:15px;
            line-height:1.75;
            color:#6B7280;
        ">
            {esc(subtitle)}
        </div>

    </div>
    """)


# ============================================================
# SESSION STATE
# ============================================================

def init_state():

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


init_state()


# ============================================================
# ENGINE INITIALIZATION
# ============================================================

@st.cache_resource
def get_engine():
    return IntelligenceEngine()


@st.cache_resource
def get_assistant():
    return AIAssistant()


def safe_call(fn, *args):

    try:
        if fn:
            return fn(*args)

    except Exception:
        return None

    return None


# ============================================================
# CAREER OPTIONS
# ============================================================

def career_options():

    try:

        with open(
            "data/career_paths.json",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return list(data.keys())

        if isinstance(data, list):

            results = []

            for item in data:

                if isinstance(item, dict):

                    name = (
                        item.get("career_goal")
                        or item.get("name")
                        or item.get("title")
                    )

                    if name:
                        results.append(name)

            if results:
                return results

    except Exception:
        pass

    return [

        "Machine Learning Engineer",
        "Data Scientist",
        "AI Engineer",
        "Full Stack Web Developer",
        "Cybersecurity Analyst",

    ]


# ============================================================
# INTELLIGENCE PIPELINE
# ============================================================

def run_pipeline(profile, engine):

    output = {

        "skill_gap":
            safe_call(
                getattr(engine, "analyze_skill_gap", None),
                profile
            ),

        "readiness":
            safe_call(
                getattr(engine, "calculate_readiness_score", None),
                profile
            ),

        "next_best_action":
            safe_call(
                getattr(engine, "calculate_next_best_action", None),
                profile
            ),

        "risks":
            safe_call(
                getattr(engine, "detect_risks", None),
                profile
            ) or [],

        "path_health":
            safe_call(
                getattr(engine, "calculate_path_health", None),
                profile
            ) or {},

        "roadmap":
            safe_call(
                getattr(engine, "generate_roadmap", None),
                profile
            ) or [],

    }

    st.session_state.engine_output = output


# ============================================================
# BRAND
# ============================================================

def brand():

    render_html("""
    <div style="
        display:flex;
        align-items:center;
        gap:11px;
        margin-bottom:6px;
    ">

        <div style="
            width:40px;
            height:40px;
            display:flex;
            align-items:center;
            justify-content:center;
            border-radius:13px;
            background:linear-gradient(135deg,#7778F0,#4F50CC);
            color:white;
            font-size:20px;
            font-weight:800;
            box-shadow:0 10px 24px rgba(90,91,220,.35);
        ">
            ✦
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:21px;
            font-weight:800;
            letter-spacing:-.04em;
            color:#FFFFFF;
        ">
            PathPilot
        </div>

    </div>

    <div style="
        margin-left:51px;
        margin-bottom:30px;
        color:#9DA7BA;
        font-size:11px;
    ">
        Learning intelligence workspace
    </div>
    """)


# ============================================================
# WELCOME PAGE — KEEPING YOUR ORIGINAL CONCEPT
# ============================================================

def welcome():

    render_html("""
    <div style="
        text-align:center;
        padding:55px 10px 35px;
    ">

        <div style="
            display:inline-flex;
            align-items:center;
            padding:7px 14px;
            border-radius:999px;
            background:#F0F0FF;
            border:1px solid #DDDDF8;
            color:#5B5CE2;
            font-size:10px;
            font-weight:800;
            letter-spacing:.12em;
            text-transform:uppercase;
        ">
            ✦ Personalized Learning Intelligence
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(48px,6.5vw,76px);
            font-weight:800;
            letter-spacing:-.065em;
            line-height:1.03;
            color:#172033;
            margin-top:24px;
        ">
            Stop guessing.
            <br>
            <span style="color:#5B5CE2;">
                Start learning with direction.
            </span>
        </div>

        <div style="
            max-width:720px;
            margin:20px auto 0;
            color:#687184;
            font-size:16px;
            line-height:1.75;
        ">
            PathPilot turns your goals, skills, constraints and learning
            patterns into an explainable learning path you can actually follow.
        </div>

    </div>
    """)

    _, center, _ = st.columns([1, 1.25, 1])

    with center:

        start = st.button(
            "Build My Learning Path  →",
            type="primary",
            use_container_width=True,
        )

    st.write("")
    st.write("")

    columns = st.columns(4)

    steps = [

        (
            "01 · PATHPILOT",
            "Understand you",
            "Goals, skills and interests become the starting point.",
        ),

        (
            "02 · PATHPILOT",
            "Find the gaps",
            "Readiness, prerequisites and blockers are analyzed.",
        ),

        (
            "03 · PATHPILOT",
            "Choose the move",
            "One explainable next action instead of random lists.",
        ),

        (
            "04 · PATHPILOT",
            "Adapt with you",
            "Feedback and progress keep the path responsive.",
        ),

    ]

    for column, step in zip(columns, steps):

        number, title, description = step

        with column:

            st.markdown(
                f"<div style='font-size:10px;font-weight:700;"
                f"letter-spacing:.08em;color:#8B93A4;margin-bottom:12px;'>"
                f"{number}</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<div style='font-family:Manrope,sans-serif;"
                f"font-size:24px;font-weight:800;letter-spacing:-.04em;"
                f"color:#172033;margin-bottom:10px;'>"
                f"{title}</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                f"<div style='font-size:14px;line-height:1.7;"
                f"color:#687184;'>{description}</div>",
                unsafe_allow_html=True,
            )

    if start:

        st.session_state.stage = "profiling"

        st.rerun()


# ============================================================
# PROFILING PAGE — COMPLETELY REDESIGNED
# ============================================================

def profiling(engine):

    hero(
        "Build your learner profile",
        "Let's understand where you're starting from.",
        "Tell PathPilot about your goal, current skills and available time. "
        "We'll use that information to build a learning path around you.",
    )

    with st.form("profile_form"):

        # ----------------------------------------------------
        # STEP 1
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown("### 01 · Your destination")

            st.caption(
                "Start with where you want your learning journey to take you."
            )

            st.write("")

            left, right = st.columns(2)

            with left:

                name = st.text_input(
                    "Your name",
                    placeholder="e.g. Akshaya Reddy",
                )

            with right:

                goal = st.selectbox(
                    "Career goal",
                    career_options(),
                )

            natural_goal = st.text_area(
                "Describe your goal in your own words",
                placeholder=(
                    "Example: I want to become a Machine Learning Engineer, "
                    "build strong projects and prepare for internships."
                ),
                height=120,
            )

        st.write("")

        # ----------------------------------------------------
        # STEP 2
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown("### 02 · Your current position")

            st.caption(
                "Help PathPilot understand what you already know."
            )

            st.write("")

            level = st.select_slider(
                "Experience level",
                options=[
                    "Beginner",
                    "Intermediate",
                    "Advanced",
                ],
                value="Beginner",
            )

            left, right = st.columns(2)

            with left:

                skills = st.text_input(
                    "Current skills",
                    placeholder="e.g. Python, SQL, Git",
                )

            with right:

                interests = st.text_input(
                    "Areas you're interested in",
                    placeholder="e.g. AI, Data Science, Computer Vision",
                )

        st.write("")

        # ----------------------------------------------------
        # STEP 3
        # ----------------------------------------------------

        with st.container(border=True):

            st.markdown("### 03 · Your learning reality")

            st.caption(
                "A realistic learning path should fit your actual schedule."
            )

            st.write("")

            col1, col2, col3 = st.columns(3)

            with col1:

                hours = st.number_input(
                    "Hours per week",
                    min_value=1,
                    max_value=80,
                    value=10,
                )

            with col2:

                weeks = st.number_input(
                    "Target timeline (weeks)",
                    min_value=1,
                    max_value=104,
                    value=24,
                )

            with col3:

                style = st.selectbox(
                    "Preferred learning style",
                    [
                        "Mixed",
                        "Hands-on",
                        "Visual",
                        "Video",
                        "Reading",
                    ],
                )

        st.write("")

        submit = st.form_submit_button(
            "Generate My Personalized Learning Path  →",
            type="primary",
            use_container_width=True,
        )

    if not submit:
        return

    if not name.strip():

        st.error("Please enter your name before generating your path.")

        return

    try:

        profile = LearnerProfile(

            name=name.strip(),

            career_goal=goal,

            natural_language_goal=natural_goal.strip(),

            experience_level={
                "Beginner": 1,
                "Intermediate": 3,
                "Advanced": 5,
            }[level],

            current_skills=[
                item.strip()
                for item in skills.split(",")
                if item.strip()
            ],

            interests=[
                item.strip()
                for item in interests.split(",")
                if item.strip()
            ],

            completed_courses=[],

            weekly_hours=int(hours),

            timeline_weeks=int(weeks),

            preferred_learning_style=style.lower(),

        )

        st.session_state.profile = profile

        with st.spinner(
            "PathPilot is analyzing your skills, goals and learning opportunities..."
        ):

            run_pipeline(profile, engine)

        st.session_state.stage = "app"

        st.rerun()

    except Exception as exc:

        st.error(
            f"Something went wrong while generating your learning path: {exc}"
        )


# ============================================================
# NEXT BEST ACTION
# ============================================================

def next_action(engine, adaptive_engine, assistant):

    output = st.session_state.engine_output or {}

    nba = output.get("next_best_action")

    hero(
        "Decision engine",
        "Your next best action.",
        "Instead of overwhelming you with options, PathPilot identifies "
        "the most valuable next move.",
    )

    if not isinstance(nba, dict):

        st.info("Your next recommendation is not available yet.")

        return

    skill = nba.get("skill", "Your next learning step")

    score = nba.get("score", "—")

    hours = nba.get("est_hours", "—")

    difficulty = nba.get("difficulty", "—")

    render_html(f"""
    <div style="
        background:linear-gradient(135deg,#5556D8,#7776EC);
        border-radius:24px;
        padding:34px;
        color:white;
        box-shadow:0 20px 50px rgba(85,86,216,.22);
        margin-bottom:24px;
    ">

        <div style="
            font-size:10px;
            font-weight:800;
            letter-spacing:.12em;
            opacity:.75;
        ">
            PATHPILOT RECOMMENDS
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(30px,4vw,46px);
            font-weight:800;
            letter-spacing:-.04em;
            margin-top:8px;
        ">
            {esc(skill)}
        </div>

        <div style="
            display:flex;
            flex-wrap:wrap;
            gap:12px;
            margin-top:24px;
        ">

            <div style="
                padding:12px 16px;
                border-radius:14px;
                background:rgba(255,255,255,.13);
                border:1px solid rgba(255,255,255,.16);
            ">
                <div style="font-size:9px;opacity:.7;">CONFIDENCE</div>
                <div style="font-weight:800;margin-top:4px;">
                    {esc(score)}
                </div>
            </div>

            <div style="
                padding:12px 16px;
                border-radius:14px;
                background:rgba(255,255,255,.13);
                border:1px solid rgba(255,255,255,.16);
            ">
                <div style="font-size:9px;opacity:.7;">ESTIMATED EFFORT</div>
                <div style="font-weight:800;margin-top:4px;">
                    {esc(hours)} hrs
                </div>
            </div>

            <div style="
                padding:12px 16px;
                border-radius:14px;
                background:rgba(255,255,255,.13);
                border:1px solid rgba(255,255,255,.16);
            ">
                <div style="font-size:9px;opacity:.7;">DIFFICULTY</div>
                <div style="font-weight:800;margin-top:4px;">
                    {esc(difficulty)}
                </div>
            </div>

        </div>

    </div>
    """)

    reasons = nba.get("reasons", [])

    if not isinstance(reasons, list):
        reasons = [reasons]

    left, right = st.columns([1.25, 0.75])

    with left:

        with st.container(border=True):

            st.markdown("### Why this, why now?")

            if reasons:

                for reason in reasons:

                    st.markdown(f"✓ {esc(reason)}")

            else:

                st.write(
                    "This recommendation was selected based on your "
                    "profile, skill gaps and learning path."
                )

    with right:

        with st.container(border=True):

            st.markdown("### Decision signals")

            breakdown = nba.get("score_breakdown", {})

            if isinstance(breakdown, dict):

                for key, value in breakdown.items():

                    st.caption(
                        str(key).replace("_", " ").title()
                    )

                    try:
                        progress = float(value) / 100
                    except Exception:
                        progress = 0

                    progress = max(0, min(progress, 1))

                    st.progress(progress)

            else:

                st.caption(
                    "Detailed decision signals are unavailable."
                )

    st.write("")

    with st.container(border=True):

        st.markdown("### Does this recommendation feel right?")

        st.caption(
            "Your feedback helps the adaptive engine improve future recommendations."
        )

        col1, col2, col3 = st.columns(3)

        choice = None

        with col1:

            if st.button(
                "Too easy",
                use_container_width=True,
            ):
                choice = "too_easy"

        with col2:

            if st.button(
                "Feels right",
                type="primary",
                use_container_width=True,
            ):
                choice = "appropriate"

        with col3:

            if st.button(
                "Too difficult",
                use_container_width=True,
            ):
                choice = "too_difficult"

    if choice and adaptive_engine:

        result = safe_call(
            getattr(adaptive_engine, "apply_feedback", None),
            st.session_state.profile,
            nba.get("skill"),
            choice,
            st.session_state.adaptation_state,
        )

        if isinstance(result, dict):

            if result.get("updated_recommendation"):

                output["next_best_action"] = (
                    result["updated_recommendation"]
                )

            if result.get("updated_path_health"):

                output["path_health"] = (
                    result["updated_path_health"]
                )

            if result.get("updated_risks"):

                output["risks"] = (
                    result["updated_risks"]
                )

            st.session_state.engine_output = output

            st.success(
                result.get(
                    "adaptation_message",
                    "Your learning path has been updated."
                )
            )

            st.rerun()

    if assistant:

        with st.expander("Why did PathPilot choose this?"):

            answer = safe_call(
                getattr(
                    assistant,
                    "explain_next_best_action",
                    None
                ),
                st.session_state.profile,
                nba,
            )

            st.write(
                answer
                or "An explanation is currently unavailable."
            )


# ============================================================
# PATH HEALTH
# ============================================================

def health_page():

    output = st.session_state.engine_output or {}

    health = output.get("path_health") or {}

    risks = output.get("risks") or []

    hero(
        "Learning diagnostics",
        "How healthy is your learning path?",
        "PathPilot evaluates whether your current roadmap is realistic, "
        "sustainable and aligned with your goals.",
    )

    score = (
        health.get("health_score", "—")
        if isinstance(health, dict)
        else "—"
    )

    status = (
        health.get("status", "Unknown")
        if isinstance(health, dict)
        else "Unknown"
    )

    left, right = st.columns([0.7, 1.3])

    with left:

        with st.container(border=True):

            st.caption("OVERALL PATH HEALTH")

            st.markdown(
                f"<div style='font-family:Manrope,sans-serif;"
                f"font-size:58px;font-weight:800;color:#5B5CE2;'>"
                f"{esc(score)}</div>",
                unsafe_allow_html=True,
            )

            st.markdown(f"### {esc(status)}")

    with right:

        with st.container(border=True):

            st.markdown("### What is influencing your path?")

            factors = (
                health.get("contributing_factors", [])
                if isinstance(health, dict)
                else []
            )

            if factors:

                for factor in factors:
                    st.markdown(f"✓ {esc(factor)}")

            else:

                st.write(
                    "Your profile, skill gaps, available time and learning "
                    "progress are used to evaluate path health."
                )

    st.write("")

    st.markdown("### Active risks")

    if not risks:

        st.success(
            "No major risks are currently affecting your learning path."
        )

        return

    for risk in risks:

        with st.container(border=True):

            if isinstance(risk, dict):

                severity = str(
                    risk.get("severity", "Low")
                ).upper()

                title = (
                    risk.get("title")
                    or risk.get("type")
                    or "Learning risk"
                )

                message = risk.get("message", "")

                action = (
                    risk.get("suggested_action")
                    or risk.get("action")
                )

                st.caption(f"{severity} PRIORITY")

                st.markdown(f"### {esc(title)}")

                if message:
                    st.write(message)

                if action:
                    st.info(
                        f"Recommended action: {action}"
                    )

            else:

                st.write(str(risk))


# ============================================================
# AI ASSISTANT
# ============================================================

def assistant_page(assistant):

    output = st.session_state.engine_output or {}

    profile = st.session_state.profile

    hero(
        "Conversational learning intelligence",
        "Ask anything about your path.",
        "Get contextual explanations about your roadmap, skills, "
        "recommendations and next steps.",
    )

    suggestions = [

        "What should I learn next?",

        "What skills am I missing?",

        "How can I improve my learning path?",

        "What is blocking my progress?",

    ]

    columns = st.columns(4)

    for index, suggestion in enumerate(suggestions):

        with columns[index]:

            if st.button(
                suggestion,
                key=f"suggestion_{index}",
                use_container_width=True,
            ):

                st.session_state.assistant_question = suggestion

    st.write("")

    question = st.text_input(
        "Ask PathPilot",
        value=st.session_state.assistant_question,
        placeholder=(
            "Example: What should I focus on this week?"
        ),
    )

    st.session_state.assistant_question = question

    if question:

        with st.spinner("PathPilot is thinking..."):

            answer = safe_call(
                getattr(
                    assistant,
                    "answer_path_question",
                    None
                ) if assistant else None,
                profile,
                output,
                question,
            )

        with st.container(border=True):

            st.caption("✦ PATHPILOT INSIGHT")

            st.markdown(
                answer
                or "I couldn't generate an answer right now."
            )


# ============================================================
# APPLICATION SHELL
# ============================================================

def app_shell(engine, adaptive_engine, assistant):

    profile = st.session_state.profile

    output = st.session_state.engine_output

    if not profile or output is None:

        st.session_state.stage = "profiling"

        st.rerun()

    with st.sidebar:

        brand()

        options = [

            "Overview",

            "Next Action",

            "Learning Roadmap",

            "Path Health",

            "AI Assistant",

        ]

        current = st.session_state.nav_section

        if current not in options:
            current = "Overview"

        section = st.radio(
            "Navigation",
            options,
            index=options.index(current),
            label_visibility="collapsed",
        )

        st.session_state.nav_section = section

        st.divider()

        st.markdown(
            f"### {esc(getattr(profile, 'name', 'Learner'))}",
            unsafe_allow_html=True,
        )

        st.caption(
            str(
                getattr(
                    profile,
                    "career_goal",
                    "Personalized Learning Path"
                )
            )
        )

        st.write("")

        if st.button(
            "↻ Restart journey",
            use_container_width=True,
        ):

            keys = [

                "stage",

                "profile",

                "engine_output",

                "adaptation_state",

                "roadmap_progress",

                "nav_section",

                "assistant_question",

            ]

            for key in keys:
                st.session_state.pop(key, None)

            init_state()

            st.rerun()

    # --------------------------------------------------------
    # ROUTING
    # --------------------------------------------------------

    if section == "Overview":

        render_dashboard(profile, output)

    elif section == "Next Action":

        next_action(
            engine,
            adaptive_engine,
            assistant
        )

    elif section == "Learning Roadmap":

        render_roadmap(profile, output)

    elif section == "Path Health":

        health_page()

    else:

        assistant_page(assistant)


# ============================================================
# APPLICATION START
# ============================================================

try:

    engine = get_engine()

    assistant = get_assistant()

    adaptive_engine = AdaptiveEngine(engine)

except Exception as exc:

    st.error(
        f"PathPilot could not initialize its intelligence layer: {exc}"
    )

    st.stop()


if st.session_state.stage == "welcome":

    welcome()

elif st.session_state.stage == "profiling":

    profiling(engine)

else:

    app_shell(
        engine,
        adaptive_engine,
        assistant
    )

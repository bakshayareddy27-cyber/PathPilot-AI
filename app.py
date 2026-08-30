import json
import html
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


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --bg: #F6F7FB;
        --surface: #FFFFFF;
        --surface-2: #F1F3F8;
        --ink: #172033;
        --muted: #697386;
        --line: #E5E9F1;
        --primary: #5B5CE2;
        --primary-dark: #4546C8;
        --primary-soft: #EEEDFF;
        --green: #158A5B;
        --green-soft: #EAF8F1;
        --amber: #B7791F;
        --amber-soft: #FFF6E6;
        --red: #C84B5A;
        --red-soft: #FFF0F2;
    }

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 0%, rgba(91,92,226,.08), transparent 25%),
            radial-gradient(circle at 0% 45%, rgba(21,138,91,.045), transparent 24%),
            var(--bg);
        color: var(--ink);
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 1320px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: "Manrope", sans-serif !important;
        letter-spacing: -.035em !important;
        color: var(--ink) !important;
    }

    /* --- Sidebar Custom Styling --- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #182033 100%);
        border-right: 1px solid rgba(255, 255, 255, .07);
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #F7F8FC !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #AAB4C6 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, .10);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 10px 12px;
        border-radius: 12px;
        margin: 3px 0;
        transition: background .18s ease, transform .18s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, .08);
        transform: translateX(3px);
    }

    /* --- Input Fields Fix (Contrast & Visibility) --- */
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] div {
        color: #172033 !important;
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stSlider"] label,
    div[data-testid="stNumberInput"] label {
        color: #172033 !important;
        font-weight: 600 !important;
    }

    /* Slider Specific Fixes */
    div[data-testid="stSlider"] div[data-testid="stMarkdownContainer"] p {
        color: #172033 !important;
    }

    /* Cards & Containers */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid var(--line) !important;
        border-radius: 20px !important;
        background: rgba(255, 255, 255, .92) !important;
        box-shadow: 0 10px 30px rgba(26, 35, 60, .045);
        transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 18px 42px rgba(26, 35, 60, .08);
        border-color: #D9DDF0 !important;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, .88);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 15px 17px;
        transition: transform .18s ease, box-shadow .18s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 30px rgba(26, 35, 60, .07);
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 44px !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: 1px solid #DDE2EC !important;
        transition: all .18s ease !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(26, 35, 60, .12);
    }

    .stButton > button[kind="primary"],
    .stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary), #7778F0) !important;
        color: white !important;
        border: none !important;
    }

    details {
        border-radius: 14px !important;
        border: 1px solid var(--line) !important;
        background: white !important;
    }

    .pp-kicker {
        color: var(--primary);
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .12em;
        text-transform: uppercase;
        margin-bottom: .45rem;
    }

    .pp-title {
        font-family: "Manrope", sans-serif;
        font-size: clamp(2rem, 4vw, 3.45rem);
        font-weight: 800;
        line-height: 1.06;
        letter-spacing: -.055em;
        color: var(--ink);
        margin: 0;
    }

    .pp-subtitle {
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.7;
        max-width: 760px;
        margin-top: .75rem;
    }

    .pp-brand {
        font-family: "Manrope", sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        letter-spacing: -.04em;
    }

    .pp-brand-dot {
        width: 38px; height: 38px; border-radius: 12px;
        display: inline-flex; align-items: center; justify-content: center;
        background: linear-gradient(135deg, #7A7CF4, #5152D7);
        color: white; font-weight: 800; margin-right: 10px;
        box-shadow: 0 10px 22px rgba(91, 92, 226, .28);
    }

    .pp-hero {
        padding: 2.2rem 0 1.3rem;
        text-align: center;
    }

    .pp-pill {
        display: inline-block;
        padding: .42rem .8rem;
        border-radius: 999px;
        background: var(--primary-soft);
        color: var(--primary);
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        border: 1px solid #DDD9FF;
    }

    @media(max-width: 760px) {
        .block-container { padding: 1.2rem 1rem 2rem; }
        .pp-title { font-size: 2.2rem; }
    }
    </style>
    """, unsafe_allow_html=True)


inject_css()


def esc(value):
    return html.escape(str(value if value is not None else "—"))


def hero(eyebrow, title, subtitle):
    st.markdown(
        f"""
        <div>
            <div class="pp-kicker">{esc(eyebrow)}</div>
            <div class="pp-title">{esc(title)}</div>
            <div class="pp-subtitle">{esc(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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


@st.cache_resource
def get_engine():
    return IntelligenceEngine()


@st.cache_resource
def get_assistant():
    return AIAssistant()


def safe_call(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs) if callable(fn) else None
    except Exception:
        return None


def career_options():
    try:
        with open("data/career_paths.json", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return list(data.keys())
        if isinstance(data, list):
            values = []
            for item in data:
                if isinstance(item, dict):
                    value = item.get("career_goal") or item.get("name")
                    if value:
                        values.append(str(value))
            if values:
                return values
    except Exception:
        pass

    return [
        "Machine Learning Engineer",
        "Data Scientist",
        "Full Stack Web Developer",
        "Cybersecurity Analyst",
    ]


def run_pipeline(profile, engine):
    st.session_state.engine_output = {
        "skill_gap": safe_call(getattr(engine, "analyze_skill_gap", None), profile),
        "readiness": safe_call(getattr(engine, "calculate_readiness_score", None), profile),
        "next_best_action": safe_call(getattr(engine, "calculate_next_best_action", None), profile),
        "risks": safe_call(getattr(engine, "detect_risks", None), profile) or [],
        "path_health": safe_call(getattr(engine, "calculate_path_health", None), profile) or {},
        "roadmap": safe_call(getattr(engine, "generate_roadmap", None), profile) or [],
    }


def welcome():
    st.markdown(
        """
        <div class="pp-hero">
            <span class="pp-pill">✦ Personalized learning intelligence</span>
            <div class="pp-title" style="margin-top:1.2rem;">
                Stop guessing.<br>
                <span style="color:#5B5CE2;">Start learning with direction.</span>
            </div>
            <div class="pp-subtitle" style="margin:1rem auto 0;">
                PathPilot turns your goals, skills, constraints and learning patterns into
                an explainable path you can actually follow.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, center, _ = st.columns([1, 1.25, 1])
    with center:
        if st.button("Build My Learning Path  →", type="primary", use_container_width=True):
            st.session_state.stage = "profiling"
            st.rerun()

    st.write("")
    steps = [
        ("01", "Understand you", "Goals, skills and interests become the starting point."),
        ("02", "Find the gaps", "Readiness, prerequisites and blockers are analyzed."),
        ("03", "Choose the move", "One explainable next action instead of random lists."),
        ("04", "Adapt with you", "Feedback and progress keep the path responsive."),
    ]
    for col, step in zip(st.columns(4), steps):
        with col:
            with st.container(border=True):
                st.caption(f"{step[0]} · PATHPILOT")
                st.subheader(step[1])
                st.write(step[2])


def profiling(engine):
    hero(
        "Getting started",
        "Let’s map your starting point.",
        "Answer a few questions so PathPilot can build a learning path around your actual situation.",
    )

    with st.form("profile_form"):
        with st.container(border=True):
            st.subheader("01 · Your destination")
            st.caption("Where do you want this learning journey to take you?")
            name = st.text_input("Your name", placeholder="e.g. Akshaya Reddy")
            goal = st.selectbox("Career goal", career_options())
            natural = st.text_area(
                "Describe your goal in your own words",
                placeholder="I want to become an ML engineer and prepare for internships.",
            )

        st.write("")
        with st.container(border=True):
            st.subheader("02 · Your current position")
            level = st.select_slider(
                "Experience level",
                ["Beginner", "Intermediate", "Advanced"],
                value="Beginner",
            )
            skills = st.text_input("Current skills", placeholder="Python, SQL, Git")
            interests = st.text_input("Interests", placeholder="AI, Data, Web Development")

        st.write("")
        with st.container(border=True):
            st.subheader("03 · Your learning reality")
            left, right = st.columns(2)
            with left:
                hours = st.number_input("Hours available each week", 1, 80, 10)
            with right:
                weeks = st.number_input("Target timeline (weeks)", 1, 104, 24)
            style = st.selectbox(
                "Preferred learning style",
                ["visual", "reading", "hands-on", "video", "mixed"],
            )
            submit = st.form_submit_button(
                "Generate My Intelligence Path  →",
                type="primary",
                use_container_width=True,
            )

    if submit:
        if not name.strip():
            st.error("Please enter your name before continuing.")
            return

        profile = LearnerProfile(
            name=name.strip(),
            career_goal=goal,
            natural_language_goal=natural.strip(),
            experience_level={"Beginner": 1, "Intermediate": 3, "Advanced": 5}[level],
            current_skills=[s.strip() for s in skills.split(",") if s.strip()],
            interests=[s.strip() for s in interests.split(",") if s.strip()],
            completed_courses=[],
            weekly_hours=int(hours),
            timeline_weeks=int(weeks),
            preferred_learning_style=style,
        )

        st.session_state.profile = profile
        with st.spinner("PathPilot is analysing your learning profile..."):
            run_pipeline(profile, engine)
        st.session_state.stage = "app"
        st.rerun()


def next_action(adaptive_engine, assistant):
    output = st.session_state.engine_output or {}
    nba = output.get("next_best_action") or {}

    hero(
        "Decision engine",
        "Your next best action.",
        "A focused recommendation selected from your profile, readiness and learning path.",
    )

    if not isinstance(nba, dict) or not nba:
        st.info("No recommendation is available yet. Try regenerating your learning path.")
        return

    skill = nba.get("skill") or nba.get("title") or nba.get("name") or "Your next step"
    reasons = nba.get("reasons") or nba.get("reason") or []
    if isinstance(reasons, str):
        reasons = [reasons]

    with st.container(border=True):
        st.subheader(str(skill))
        st.caption("PATHPILOT'S RECOMMENDATION")
        c1, c2, c3 = st.columns(3)
        c1.metric("Confidence", nba.get("score", "—"))
        c2.metric("Estimated effort", f"{nba.get('est_hours', '—')} hrs")
        c3.metric("Difficulty", nba.get("difficulty", "—"))

        st.divider()
        st.markdown("**Why this, why now?**")
        if reasons:
            for reason in reasons:
                st.write(f"✓  {reason}")
        else:
            st.write("This step was selected from your current profile and learning path.")

    st.write("")
    with st.container(border=True):
        st.subheader("Does this recommendation feel right?")
        st.caption("Your feedback helps the adaptive engine adjust future recommendations.")
        a, b, c = st.columns(3)
        choice = None
        with a:
            if st.button("Too easy", use_container_width=True):
                choice = "too_easy"
        with b:
            if st.button("Appropriate", type="primary", use_container_width=True):
                choice = "appropriate"
        with c:
            if st.button("Too difficult", use_container_width=True):
                choice = "too_difficult"

        if choice:
            result = safe_call(
                getattr(adaptive_engine, "apply_feedback", None),
                st.session_state.profile,
                skill,
                choice,
                st.session_state.adaptation_state,
            )
            if isinstance(result, dict):
                if result.get("updated_recommendation") is not None:
                    output["next_best_action"] = result["updated_recommendation"]
                if result.get("updated_path_health") is not None:
                    output["path_health"] = result["updated_path_health"]
                if result.get("updated_risks") is not None:
                    output["risks"] = result["updated_risks"]
                st.session_state.engine_output = output
                st.success(result.get("adaptation_message", "Your path was updated."))
                st.rerun()
            else:
                st.info("Feedback recorded for the next recommendation cycle.")

    if assistant:
        with st.expander("Why did PathPilot choose this?"):
            answer = safe_call(
                getattr(assistant, "explain_next_best_action", None),
                st.session_state.profile,
                nba,
            )
            st.write(answer or "Explanation is unavailable right now.")


def health_page():
    output = st.session_state.engine_output or {}
    health = output.get("path_health") or {}
    risks = output.get("risks") or []

    hero(
        "Diagnostics",
        "Path health.",
        "A quick diagnostic view of how sustainable and achievable your current path is.",
    )

    score = health.get("health_score", "—") if isinstance(health, dict) else "—"
    status = health.get("status", "Unknown") if isinstance(health, dict) else "Unknown"

    c1, c2 = st.columns([1, 2])
    with c1:
        with st.container(border=True):
            st.metric("Path health", f"{score}/100")
            st.write(f"**{status}**")
    with c2:
        with st.container(border=True):
            st.subheader("What is influencing your path?")
            factors = health.get("contributing_factors", []) if isinstance(health, dict) else []
            if factors:
                for factor in factors:
                    st.write(f"✓  {factor}")
            else:
                st.caption("No detailed factors are available yet.")

    st.write("")
    st.subheader("Detected risks")
    if not risks:
        st.success("No active risks detected.")
        return

    for risk in risks:
        with st.container(border=True):
            if isinstance(risk, dict):
                title = risk.get("title") or risk.get("type") or "Learning risk"
                st.markdown(f"**{title}**")
                if risk.get("message"):
                    st.write(risk["message"])
                if risk.get("suggested_action") or risk.get("action"):
                    st.caption(
                        f"Recommended action: {risk.get('suggested_action') or risk.get('action')}"
                    )
            else:
                st.write(str(risk))


def assistant_page(assistant):
    profile = st.session_state.profile
    output = st.session_state.engine_output or {}

    hero(
        "Path intelligence",
        "Ask about your learning path.",
        "Get explanations grounded in your recommendation, roadmap and progress.",
    )

    prompts = [
        "What should I learn next?",
        "What is blocking my progress?",
        "How can I improve my path?",
        "Which skill has the highest impact?",
    ]

    for col, prompt in zip(st.columns(4), prompts):
        with col:
            if st.button(prompt, use_container_width=True, key=f"quick_{prompt}"):
                st.session_state.assistant_question = prompt

    question = st.text_input(
        "Ask PathPilot",
        value=st.session_state.assistant_question,
        placeholder="Ask something about your path...",
    )
    st.session_state.assistant_question = question

    if question:
        answer = safe_call(
            getattr(assistant, "answer_path_question", None) if assistant else None,
            profile,
            output,
            question,
        )
        with st.container(border=True):
            st.caption("PATHPILOT INSIGHT")
            st.write(answer or "I could not generate an answer right now.")


def app_shell(adaptive_engine, assistant):
    profile = st.session_state.profile
    output = st.session_state.engine_output

    if profile is None or output is None:
        st.session_state.stage = "profiling"
        st.rerun()

    with st.sidebar:
        st.markdown(
            '<div><span class="pp-brand-dot">✦</span><span class="pp-brand">PathPilot</span></div>',
            unsafe_allow_html=True,
        )
        st.caption("Learning intelligence workspace")
        st.write("")

        options = ["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"]
        current = st.session_state.nav_section
        if current not in options:
            current = options[0]
        section = st.radio(
            "Navigate",
            options,
            index=options.index(current),
            label_visibility="collapsed",
        )
        st.session_state.nav_section = section

        st.divider()
        st.markdown(f"**{getattr(profile, 'name', 'Learner')}**")
        st.caption(str(getattr(profile, "career_goal", "Learning path")))

        if st.button("Restart journey", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key in {
                    "stage", "profile", "engine_output", "adaptation_state",
                    "roadmap_progress", "nav_section", "assistant_question"
                }:
                    del st.session_state[key]
            init_state()
            st.rerun()

    if section == "Overview":
        render_dashboard(profile, output)
    elif section == "Next Action":
        next_action(adaptive_engine, assistant)
    elif section == "Learning Roadmap":
        render_roadmap(profile, output)
    elif section == "Path Health":
        health_page()
    else:
        assistant_page(assistant)


try:
    engine = get_engine()
    assistant = get_assistant()
    adaptive_engine = AdaptiveEngine(engine)
except Exception as exc:
    st.error(f"PathPilot could not initialise its intelligence layer: {exc}")
    st.stop()

if st.session_state.stage == "welcome":
    welcome()
elif st.session_state.stage == "profiling":
    profiling(engine)
else:
    app_shell(adaptive_engine, assistant)

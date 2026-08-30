import json
import html

import streamlit as st

from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant

from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PathPilot AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# GLOBAL UI / CSS
# =========================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --bg: #F7F8FC;
    --surface: #FFFFFF;
    --text: #1E293B;
    --muted: #718096;
    --border: #E5E7EF;
    --primary: #5B5CE2;
    --primary-dark: #494ACB;
    --primary-soft: #F0F0FF;
    --success: #20A36A;
}


/* ---------------------------------------------------------
   GLOBAL
--------------------------------------------------------- */

html,
body,
[class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 50% -20%,
            rgba(91, 92, 226, 0.08),
            transparent 35%
        ),
        #F7F8FC;
    color: #1E293B;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ---------------------------------------------------------
   MAIN LAYOUT
--------------------------------------------------------- */

.block-container {
    max-width: 1240px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}


/* ---------------------------------------------------------
   HEADINGS
--------------------------------------------------------- */

h1, h2, h3 {
    font-family: 'Manrope', sans-serif !important;
    color: #1E293B !important;
    letter-spacing: -0.035em;
}


/* ---------------------------------------------------------
   SIDEBAR
--------------------------------------------------------- */

section[data-testid="stSidebar"] {
    background: #171925;
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #E9EBF5 !important;
}


/* Sidebar radio */

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 4px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 12px;
    border-radius: 10px;
    transition: all 0.2s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.08);
    transform: translateX(3px);
}


/* ---------------------------------------------------------
   INPUTS
--------------------------------------------------------- */

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stNumberInput"] input {

    background: #FFFFFF !important;

    color: #1E293B !important;

    border: 1px solid #DDE1EA !important;

    border-radius: 12px !important;

    box-shadow: none !important;

    transition:
        border 0.2s ease,
        box-shadow 0.2s ease,
        transform 0.2s ease;
}


/* Placeholder */

div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {

    color: #A7AFBE !important;

    opacity: 1 !important;
}


/* Focus */

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus,
div[data-testid="stNumberInput"] input:focus {

    border-color: #5B5CE2 !important;

    box-shadow:
        0 0 0 4px rgba(91,92,226,0.10) !important;
}


/* Textarea */

div[data-testid="stTextArea"] textarea {
    min-height: 120px !important;
}


/* ---------------------------------------------------------
   SELECT BOX
--------------------------------------------------------- */

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {

    background: #FFFFFF !important;

    color: #1E293B !important;

    border-color: #DDE1EA !important;

    border-radius: 12px !important;

}


/* ---------------------------------------------------------
   BUTTONS
--------------------------------------------------------- */

.stButton > button,
.stFormSubmitButton > button {

    min-height: 46px;

    border-radius: 12px;

    font-family: 'DM Sans', sans-serif !important;

    font-weight: 700 !important;

    border: 1px solid #E1E4EC;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease;
}


.stButton > button:hover,
.stFormSubmitButton > button:hover {

    transform: translateY(-2px);

    box-shadow:
        0 12px 30px rgba(31,41,55,0.12);

    border-color: #B9BAF5;
}


/* Primary button */

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {

    background:
        linear-gradient(
            135deg,
            #5455D7,
            #6C6DE8
        ) !important;

    color: white !important;

    border: none !important;

    box-shadow:
        0 10px 24px rgba(91,92,226,0.20);
}


.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {

    box-shadow:
        0 16px 34px rgba(91,92,226,0.28);
}


/* ---------------------------------------------------------
   CARDS
--------------------------------------------------------- */

div[data-testid="stVerticalBlockBorderWrapper"] {

    background: rgba(255,255,255,0.92);

    border: 1px solid #E5E7EF;

    border-radius: 20px;

    box-shadow:
        0 8px 28px rgba(31,41,55,0.04);

    transition:
        transform 0.22s ease,
        box-shadow 0.22s ease,
        border-color 0.22s ease;
}


div[data-testid="stVerticalBlockBorderWrapper"]:hover {

    border-color: #D6D8EE;

    box-shadow:
        0 16px 36px rgba(31,41,55,0.07);
}


/* ---------------------------------------------------------
   METRICS
--------------------------------------------------------- */

div[data-testid="stMetric"] {

    background: #FFFFFF;

    border: 1px solid #E5E7EF;

    border-radius: 16px;

    padding: 16px;

}


/* ---------------------------------------------------------
   EXPANDERS
--------------------------------------------------------- */

details {

    background: #FFFFFF !important;

    border: 1px solid #E5E7EF !important;

    border-radius: 14px !important;

}


/* ---------------------------------------------------------
   PROGRESS
--------------------------------------------------------- */

div[data-testid="stProgress"] > div > div {
    background-color: #5B5CE2 !important;
}


/* ---------------------------------------------------------
   MOBILE
--------------------------------------------------------- */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 1.5rem;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HELPERS
# =========================================================

def esc(value):
    """Safely escape dynamic text used inside HTML."""
    if value is None:
        return "—"
    return html.escape(str(value))


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
        if fn:
            return fn(*args, **kwargs)
    except Exception:
        return None

    return None


# =========================================================
# CAREER OPTIONS
# =========================================================

def career_options():

    try:

        with open("data/career_paths.json", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return list(data.keys())

        if isinstance(data, list):

            options = []

            for item in data:

                if isinstance(item, dict):

                    value = (
                        item.get("career_goal")
                        or item.get("name")
                    )

                    if value:
                        options.append(value)

            if options:
                return options

    except Exception:
        pass


    return [

        "Machine Learning Engineer",

        "Data Scientist",

        "AI Engineer",

        "Full Stack Web Developer",

        "Cybersecurity Analyst",

    ]


# =========================================================
# PIPELINE
# =========================================================

def run_pipeline(profile, engine):

    output = {

        "skill_gap": safe_call(
            getattr(engine, "analyze_skill_gap", None),
            profile,
        ),

        "readiness": safe_call(
            getattr(engine, "calculate_readiness_score", None),
            profile,
        ),

        "next_best_action": safe_call(
            getattr(engine, "calculate_next_best_action", None),
            profile,
        ),

        "risks": safe_call(
            getattr(engine, "detect_risks", None),
            profile,
        ) or [],

        "path_health": safe_call(
            getattr(engine, "calculate_path_health", None),
            profile,
        ) or {},

        "roadmap": safe_call(
            getattr(engine, "generate_roadmap", None),
            profile,
        ) or [],

    }

    st.session_state.engine_output = output


# =========================================================
# WELCOME PAGE
# =========================================================

def welcome():

    # IMPORTANT:
    # This is ONE complete HTML block rendered with
    # unsafe_allow_html=True.
    # It will NOT appear as raw <div> code.

    hero = """
<div style="
    text-align:center;
    padding:42px 10px 34px;
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
"""

    st.markdown(hero, unsafe_allow_html=True)

    _, middle, _ = st.columns([1, 1.35, 1])

    with middle:

        start = st.button(
            "Build My Learning Path →",
            type="primary",
            use_container_width=True,
        )


    st.markdown("<div style='height:36px'></div>", unsafe_allow_html=True)


    # FOUR FEATURE COLUMNS

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
                f"""
<div style="
    padding:18px 6px;
    min-height:145px;
">

    <div style="
        font-size:10px;
        letter-spacing:.08em;
        font-weight:700;
        color:#8A92A3;
        margin-bottom:20px;
    ">
        {number}
    </div>

    <div style="
        font-family:Manrope,sans-serif;
        font-size:25px;
        font-weight:700;
        letter-spacing:-.04em;
        color:#1E293B;
        margin-bottom:14px;
    ">
        {title}
    </div>

    <div style="
        font-size:14px;
        line-height:1.65;
        color:#687184;
        max-width:240px;
    ">
        {description}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


    if start:

        st.session_state.stage = "profiling"

        st.rerun()


# =========================================================
# PROFILING PAGE
# =========================================================

def profiling(engine):

    st.markdown(
        """
<div style="
    max-width:780px;
    margin:0 auto 30px;
">

    <div style="
        color:#5B5CE2;
        font-size:11px;
        font-weight:800;
        letter-spacing:.11em;
        text-transform:uppercase;
        margin-bottom:10px;
    ">
        Getting Started
    </div>

    <div style="
        font-family:Manrope,sans-serif;
        font-size:42px;
        font-weight:800;
        letter-spacing:-.05em;
        color:#1E293B;
        line-height:1.1;
    ">
        Let's map your starting point.
    </div>

    <div style="
        margin-top:12px;
        color:#718096;
        font-size:16px;
        line-height:1.7;
    ">
        Tell PathPilot where you are today and where you want to go.
        We'll build a learning path around your actual goals.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


    with st.form("profile_form"):


        # -------------------------------------------------
        # SECTION 1
        # -------------------------------------------------

        with st.container(border=True):

            st.markdown("### 01 · Your destination")

            st.caption(
                "Where do you want this learning journey to take you?"
            )


            name = st.text_input(

                "Your name",

                placeholder="e.g. Akshaya Reddy",

            )


            goal = st.selectbox(

                "Career goal",

                career_options(),

            )


            natural = st.text_area(

                "Describe your goal in your own words",

                placeholder=(
                    "Example: I want to become a Machine Learning "
                    "Engineer, build strong projects and prepare for "
                    "internship opportunities."
                ),

            )


        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


        # -------------------------------------------------
        # SECTION 2
        # -------------------------------------------------

        with st.container(border=True):

            st.markdown("### 02 · Your current position")

            st.caption(
                "Tell PathPilot what you already know and what interests you."
            )


            level = st.select_slider(

                "Experience level",

                options=[
                    "Beginner",
                    "Intermediate",
                    "Advanced",
                ],

                value="Beginner",

            )


            skills = st.text_input(

                "Current skills",

                placeholder="e.g. Python, SQL, Git, NumPy",

            )


            interests = st.text_input(

                "Interests",

                placeholder=(
                    "e.g. Artificial Intelligence, Data Science, "
                    "Computer Vision"
                ),

            )


        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


        # -------------------------------------------------
        # SECTION 3
        # -------------------------------------------------

        with st.container(border=True):

            st.markdown("### 03 · Your learning reality")

            st.caption(
                "A useful learning path should fit your real schedule."
            )


            left, right = st.columns(2)


            with left:

                hours = st.number_input(

                    "Hours available each week",

                    min_value=1,

                    max_value=80,

                    value=10,

                )


            with right:

                weeks = st.number_input(

                    "Target timeline (weeks)",

                    min_value=1,

                    max_value=104,

                    value=24,

                )


            style = st.selectbox(

                "Preferred learning style",

                [
                    "Visual",
                    "Hands-on",
                    "Reading",
                    "Video",
                    "Mixed",
                ],

            )


            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


            submit = st.form_submit_button(

                "Generate My Personalized Learning Path →",

                type="primary",

                use_container_width=True,

            )


    # =====================================================
    # FORM SUBMISSION
    # =====================================================

    if not submit:
        return


    if not name.strip():

        st.error("Please enter your name before continuing.")

        return


    try:

        profile = LearnerProfile(

            name=name.strip(),

            career_goal=goal,

            natural_language_goal=natural.strip(),

            experience_level={

                "Beginner": 1,

                "Intermediate": 3,

                "Advanced": 5,

            }[level],

            current_skills=[
                skill.strip()
                for skill in skills.split(",")
                if skill.strip()
            ],

            interests=[
                interest.strip()
                for interest in interests.split(",")
                if interest.strip()
            ],

            completed_courses=[],

            weekly_hours=int(hours),

            timeline_weeks=int(weeks),

            preferred_learning_style=style.lower(),

        )


        st.session_state.profile = profile


        with st.spinner(
            "PathPilot is analyzing your profile and building your path..."
        ):

            run_pipeline(profile, engine)


        st.session_state.stage = "app"

        st.rerun()


    except Exception as exc:

        st.error(
            f"Could not generate your learning path: {exc}"
        )


# =========================================================
# NEXT BEST ACTION
# =========================================================

def next_action(engine, adaptive_engine, assistant):

    output = st.session_state.engine_output or {}

    nba = output.get("next_best_action")


    st.markdown(
        """
<div style="margin-bottom:28px;">

    <div style="
        color:#5B5CE2;
        font-size:11px;
        font-weight:800;
        letter-spacing:.1em;
        text-transform:uppercase;
    ">
        Decision Engine
    </div>

    <div style="
        font-family:Manrope,sans-serif;
        font-size:42px;
        font-weight:800;
        letter-spacing:-.05em;
        margin-top:8px;
    ">
        Your next best action.
    </div>

    <div style="
        color:#718096;
        margin-top:10px;
        font-size:16px;
    ">
        One focused recommendation based on your learning profile.
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


    if not isinstance(nba, dict):

        st.info("No recommendation is available yet.")

        return


    skill = esc(nba.get("skill", "Your next step"))

    score = esc(nba.get("score", "—"))

    hours = esc(nba.get("est_hours", "—"))

    difficulty = esc(nba.get("difficulty", "—"))


    st.markdown(
        f"""
<div style="
    background:linear-gradient(135deg,#5455D7,#7778E8);
    border-radius:24px;
    padding:34px;
    color:white;
    box-shadow:0 20px 45px rgba(84,85,215,.20);
">

    <div style="
        font-size:10px;
        font-weight:800;
        letter-spacing:.12em;
        opacity:.75;
    ">
        PATHPILOT'S DECISION
    </div>

    <div style="
        font-family:Manrope,sans-serif;
        font-size:42px;
        font-weight:800;
        letter-spacing:-.045em;
        margin-top:10px;
    ">
        {skill}
    </div>

    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:12px;
        margin-top:24px;
    ">

        <div style="
            background:rgba(255,255,255,.12);
            border:1px solid rgba(255,255,255,.15);
            border-radius:14px;
            padding:12px 16px;
        ">
            <div style="font-size:10px;opacity:.7;">CONFIDENCE</div>
            <div style="font-weight:700;margin-top:4px;">{score}</div>
        </div>

        <div style="
            background:rgba(255,255,255,.12);
            border:1px solid rgba(255,255,255,.15);
            border-radius:14px;
            padding:12px 16px;
        ">
            <div style="font-size:10px;opacity:.7;">ESTIMATED EFFORT</div>
            <div style="font-weight:700;margin-top:4px;">{hours} hrs</div>
        </div>

        <div style="
            background:rgba(255,255,255,.12);
            border:1px solid rgba(255,255,255,.15);
            border-radius:14px;
            padding:12px 16px;
        ">
            <div style="font-size:10px;opacity:.7;">DIFFICULTY</div>
            <div style="font-weight:700;margin-top:4px;">{difficulty}</div>
        </div>

    </div>

</div>
""",
        unsafe_allow_html=True,
    )


    reasons = nba.get("reasons") or []


    if not isinstance(reasons, list):
        reasons = [reasons]


    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


    with st.container(border=True):

        st.markdown("### Why this recommendation?")

        st.caption(
            "These are the learning signals that influenced the decision."
        )


        if reasons:

            for reason in reasons:

                st.markdown(
                    f"✓ &nbsp; {esc(reason)}",
                    unsafe_allow_html=True,
                )

        else:

            st.write(
                "This step was selected based on your learning profile."
            )


# =========================================================
# PATH HEALTH
# =========================================================

def health_page():

    output = st.session_state.engine_output or {}

    health = output.get("path_health") or {}

    risks = output.get("risks") or []


    st.markdown("## Path health")

    st.caption(
        "Understand how sustainable and realistic your learning path is."
    )


    score = health.get("health_score", "—")

    status = health.get("status", "Unknown")


    left, right = st.columns([1, 2])


    with left:

        with st.container(border=True):

            st.caption("OVERALL PATH HEALTH")

            st.markdown(
                f"## {esc(score)} / 100"
            )

            st.markdown(
                f"**{esc(status)}**"
            )


    with right:

        with st.container(border=True):

            st.markdown("### What influences your path?")

            factors = health.get(
                "contributing_factors",
                [],
            )


            if factors:

                for factor in factors:

                    st.markdown(
                        f"✓ {esc(factor)}"
                    )

            else:

                st.caption(
                    "No additional path factors available."
                )


    st.markdown("### Detected risks")


    if not risks:

        st.success("No major learning risks detected.")

        return


    for risk in risks:

        with st.container(border=True):

            if isinstance(risk, dict):

                severity = risk.get(
                    "severity",
                    "Low",
                )

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


                st.caption(
                    f"{str(severity).upper()} PRIORITY"
                )

                st.markdown(
                    f"### {esc(title)}"
                )


                if message:
                    st.write(message)


                if action:
                    st.info(
                        f"Recommended action: {action}"
                    )

            else:

                st.write(str(risk))


# =========================================================
# AI ASSISTANT
# =========================================================

def assistant_page(assistant):

    profile = st.session_state.profile

    output = st.session_state.engine_output or {}


    st.markdown("## Ask PathPilot")

    st.caption(
        "Ask questions about your learning roadmap, skills and next steps."
    )


    prompts = [

        "What should I learn next?",

        "What is blocking my progress?",

        "How can I improve my path?",

        "Which skill has the highest impact?",

    ]


    columns = st.columns(4)


    for index, prompt in enumerate(prompts):

        with columns[index]:

            if st.button(
                prompt,
                key=f"prompt_{index}",
                use_container_width=True,
            ):

                st.session_state.assistant_question = prompt


    question = st.text_input(

        "Ask PathPilot",

        value=st.session_state.assistant_question,

        placeholder=(
            "Example: What should I focus on this week?"
        ),

    )


    st.session_state.assistant_question = question


    if question:

        answer = safe_call(

            getattr(
                assistant,
                "answer_path_question",
                None,
            ),

            profile,

            output,

            question,

        )


        with st.container(border=True):

            st.caption("PATHPILOT INSIGHT")

            st.write(
                answer
                or "I could not generate an answer right now."
            )


# =========================================================
# SIDEBAR
# =========================================================

def sidebar(profile):

    with st.sidebar:


        st.markdown(
            """
<div style="
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:4px;
">

    <div style="
        width:38px;
        height:38px;
        border-radius:12px;
        display:flex;
        align-items:center;
        justify-content:center;
        background:linear-gradient(135deg,#7778E8,#4F50C9);
        color:white;
        font-size:18px;
        font-weight:800;
    ">
        ✦
    </div>

    <div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:20px;
            font-weight:800;
            color:white;
        ">
            PathPilot
        </div>

        <div style="
            font-size:10px;
            color:#9BA3B8;
            margin-top:2px;
        ">
            Learning intelligence
        </div>

    </div>

</div>
""",
            unsafe_allow_html=True,
        )


        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)


        options = [

            "Overview",

            "Next Action",

            "Learning Roadmap",

            "Path Health",

            "AI Assistant",

        ]


        current = st.session_state.nav_section


        if current not in options:
            current = options[0]


        section = st.radio(

            "Navigation",

            options,

            index=options.index(current),

            label_visibility="collapsed",

        )


        st.session_state.nav_section = section


        st.divider()


        st.markdown(
            f"**{esc(getattr(profile, 'name', 'Learner'))}**"
        )

        st.caption(
            str(
                getattr(
                    profile,
                    "career_goal",
                    "Learning path",
                )
            )
        )


        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


        if st.button(

            "Restart journey",

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


    return st.session_state.nav_section


# =========================================================
# MAIN APPLICATION
# =========================================================

def app_shell(engine, adaptive_engine, assistant):

    profile = st.session_state.profile

    output = st.session_state.engine_output


    if not profile or output is None:

        st.session_state.stage = "profiling"

        st.rerun()


    section = sidebar(profile)


    health = output.get("path_health") or {}


    status = health.get(
        "status",
        "Analyzing",
    )


    score = health.get(
        "health_score",
        "—",
    )


    # -----------------------------------------------------
    # APP HEADER
    # -----------------------------------------------------

    left, right = st.columns([4, 1])


    with left:

        st.markdown(
            f"""
<div style="margin-bottom:20px;">

    <div style="
        font-size:10px;
        font-weight:800;
        letter-spacing:.11em;
        text-transform:uppercase;
        color:#5B5CE2;
    ">
        Your Learning Workspace
    </div>

    <div style="
        font-family:Manrope,sans-serif;
        font-size:38px;
        font-weight:800;
        letter-spacing:-.05em;
        color:#1E293B;
        margin-top:7px;
    ">
        Good to see you, {esc(getattr(profile, 'name', 'there'))}.
    </div>

    <div style="
        color:#718096;
        margin-top:8px;
        font-size:15px;
    ">
        Your personalized learning intelligence, roadmap and next actions.
    </div>

</div>
""",
            unsafe_allow_html=True,
        )


    with right:

        st.markdown(
            f"""
<div style="
    background:white;
    border:1px solid #E5E7EF;
    border-radius:18px;
    padding:16px;
    margin-top:15px;
">

    <div style="
        font-size:10px;
        font-weight:800;
        letter-spacing:.08em;
        color:#9AA2B1;
    ">
        PATH STATUS
    </div>

    <div style="
        font-family:Manrope,sans-serif;
        font-size:19px;
        font-weight:800;
        color:#1E293B;
        margin-top:5px;
    ">
        {esc(status)}
    </div>

    <div style="
        color:#718096;
        font-size:12px;
        margin-top:3px;
    ">
        {esc(score)} / 100 health score
    </div>

</div>
""",
            unsafe_allow_html=True,
        )


    # -----------------------------------------------------
    # NAVIGATION
    # -----------------------------------------------------

    if section == "Overview":

        render_dashboard(profile, output)


    elif section == "Next Action":

        next_action(
            engine,
            adaptive_engine,
            assistant,
        )


    elif section == "Learning Roadmap":

        render_roadmap(
            profile,
            output,
        )


    elif section == "Path Health":

        health_page()


    elif section == "AI Assistant":

        assistant_page(assistant)


# =========================================================
# INITIALIZE INTELLIGENCE LAYER
# =========================================================

try:

    engine = get_engine()

    assistant = get_assistant()

    adaptive_engine = AdaptiveEngine(engine)


except Exception as exc:

    st.error(
        f"PathPilot could not initialize its intelligence layer: {exc}"
    )

    st.stop()


# =========================================================
# ROUTING
# =========================================================

if st.session_state.stage == "welcome":

    welcome()


elif st.session_state.stage == "profiling":

    profiling(engine)


else:

    app_shell(
        engine,
        adaptive_engine,
        assistant,
    )

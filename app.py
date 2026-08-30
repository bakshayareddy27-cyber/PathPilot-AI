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


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root{
    --ink:#172033;
    --muted:#6E778B;
    --soft-muted:#8E97A8;
    --line:#E6EAF0;
    --paper:#FFFFFF;
    --canvas:#F6F7FB;
    --violet:#635BFF;
    --violet-dark:#5149D8;
    --violet-soft:#F0EFFF;
    --mint:#16A36A;
    --amber:#D38A18;
    --danger:#E25B5B;
}

html, body, [class*="css"] {
    font-family:'DM Sans', sans-serif;
}

.stApp {
    background:var(--canvas);
    color:var(--ink);
}

#MainMenu,
footer,
header {
    visibility:hidden;
}

.block-container{
    max-width:1220px;
    padding-top:2rem;
    padding-bottom:3rem;
}

h1,h2,h3 {
    font-family:'Manrope',sans-serif;
    letter-spacing:-0.03em;
    color:var(--ink);
}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid rgba(255,255,255,.08);
}

section[data-testid="stSidebar"] *{
    color:#F7F8FC !important;
}

section[data-testid="stSidebar"] .stButton button{
    background:rgba(255,255,255,.06) !important;
    border-color:rgba(255,255,255,.12) !important;
    color:#FFFFFF !important;
}


/* =========================================================
   BUTTONS
========================================================= */

.stButton > button,
.stFormSubmitButton > button{
    min-height:46px !important;
    border-radius:13px !important;
    font-weight:700 !important;
    border:1px solid #E0E5EE !important;
    transition:
        transform .18s ease,
        box-shadow .18s ease,
        border-color .18s ease !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 12px 28px rgba(41,51,80,.12);
    border-color:#BFC2FF !important;
}


/* Primary buttons */

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"]{
    background:linear-gradient(
        135deg,
        #5149D8,
        #7069E8
    ) !important;

    color:#FFFFFF !important;
    border:none !important;

    box-shadow:
        0 10px 24px rgba(81,73,216,.22) !important;
}


/* =========================================================
   CARDS
========================================================= */

div[data-testid="stVerticalBlockBorderWrapper"]{
    background:var(--paper);
    border:1px solid var(--line);
    border-radius:20px;
    box-shadow:0 8px 28px rgba(30,40,70,.045);
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover{
    border-color:#D9DDF0;
}


/* =========================================================
   METRICS
========================================================= */

div[data-testid="stMetric"]{
    background:#FFFFFF;
    border:1px solid var(--line);
    border-radius:16px;
    padding:16px;
}


/* =========================================================
   EXPANDERS
========================================================= */

details{
    border:1px solid var(--line) !important;
    border-radius:14px !important;
    background:#FFFFFF !important;
}


/* =========================================================
   SIDEBAR NAVIGATION
========================================================= */

section[data-testid="stSidebar"] div[role="radiogroup"] label{
    padding:10px 12px;
    border-radius:10px;
    transition:.18s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover{
    background:rgba(255,255,255,.08);
    transform:translateX(2px);
}


/* =========================================================
   PROFILE / ONBOARDING FORM
========================================================= */

[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSlider"] label {
    color:#273247 !important;
    font-size:14px !important;
    font-weight:650 !important;
    margin-bottom:6px !important;
}


/* TEXT INPUTS */

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background:#FFFFFF !important;
    color:#172033 !important;

    border:1px solid #DDE3EC !important;
    border-radius:13px !important;

    min-height:48px !important;

    box-shadow:none !important;

    transition:
        border-color .18s ease,
        box-shadow .18s ease,
        transform .18s ease !important;
}


/* TEXTAREA */

[data-testid="stTextArea"] textarea {
    min-height:120px !important;
    padding-top:13px !important;
}


/* PLACEHOLDERS — CLEARLY VISIBLE */

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stNumberInput"] input::placeholder {
    color:#98A1B2 !important;
    opacity:1 !important;
}


/* INPUT FOCUS */

[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus,
[data-testid="stNumberInput"] input:focus {
    border-color:#635BFF !important;

    box-shadow:
        0 0 0 4px rgba(99,91,255,.10) !important;

    outline:none !important;
}


/* SELECTBOX */

[data-testid="stSelectbox"] > div > div {
    background:#FFFFFF !important;
    color:#172033 !important;

    border-color:#DDE3EC !important;
    border-radius:13px !important;

    min-height:48px !important;
}


/* SELECTED TEXT */

[data-testid="stSelectbox"] div[data-baseweb="select"] *{
    color:#172033 !important;
}


/* SLIDER */

[data-testid="stSlider"] {
    padding-top:4px;
    padding-bottom:8px;
}


/* Number input */

[data-testid="stNumberInput"] {
    margin-bottom:6px;
}


/* FORM SUBMIT BUTTON */

[data-testid="stForm"] .stFormSubmitButton button {
    min-height:52px !important;
    font-size:15px !important;
    letter-spacing:-.01em !important;
}


/* =========================================================
   MOBILE
========================================================= */

@media(max-width:760px){

    .block-container{
        padding:1.2rem 1rem;
    }

}
</style>
""", unsafe_allow_html=True)


def esc(value):
    return html.escape(str(value if value is not None else "—"))


def hero_html(eyebrow, title, subtitle):
    return f"""
    <div style="margin-bottom:26px;">
        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:.11em;
            text-transform:uppercase;
            color:#635BFF;
            margin-bottom:8px;
        ">
            {esc(eyebrow)}
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(30px,4vw,46px);
            font-weight:800;
            letter-spacing:-.045em;
            line-height:1.08;
            color:#172033;
        ">
            {title}
        </div>

        <div style="
            font-size:15px;
            line-height:1.7;
            color:#6E778B;
            margin-top:10px;
            max-width:760px;
        ">
            {esc(subtitle)}
        </div>
    </div>
    """


def brand():
    st.markdown("""
    <div style="
        display:flex;
        align-items:center;
        gap:11px;
        margin-bottom:4px;
    ">
        <div style="
            width:38px;
            height:38px;
            border-radius:12px;
            background:linear-gradient(135deg,#817CFF,#5149D8);
            display:grid;
            place-items:center;
            font-family:Manrope;
            font-weight:800;
            font-size:19px;
            color:white;
        ">
            ✦
        </div>

        <div style="
            font-family:Manrope;
            font-size:20px;
            font-weight:800;
            letter-spacing:-.03em;
            color:white;
        ">
            PathPilot
        </div>
    </div>

    <div style="
        font-size:12px;
        color:#AAB3C7;
        margin-left:49px;
        margin-bottom:26px;
    ">
        Learning intelligence workspace
    </div>
    """, unsafe_allow_html=True)


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
        return fn(*args, **kwargs) if fn else None

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

                    value = (
                        item.get("career_goal")
                        or item.get("name")
                    )

                    if value:
                        values.append(value)

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


# =========================================================
# WELCOME PAGE
# DO NOT CHANGE
# =========================================================

def welcome():

    st.markdown("""
    <div style="text-align:center;padding:54px 10px 26px;">

        <div style="
            display:inline-block;
            padding:7px 13px;
            border-radius:999px;
            background:#F0EFFF;
            border:1px solid #DCD9FF;
            color:#635BFF;
            font-size:11px;
            font-weight:800;
            letter-spacing:.08em;
            text-transform:uppercase;
        ">
            ✦ Personalized Learning Intelligence
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(46px,7vw,78px);
            font-weight:800;
            letter-spacing:-.06em;
            line-height:1.01;
            color:#172033;
            margin-top:22px;
        ">
            Stop guessing.<br>
            <span style="color:#635BFF;">
                Start learning with direction.
            </span>
        </div>

        <p style="
            max-width:720px;
            margin:20px auto 0;
            font-size:18px;
            line-height:1.7;
            color:#6E778B;
        ">
            PathPilot turns your goals, skills, constraints and learning patterns into an explainable path you can actually follow.
        </p>

    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 1.4, 1])

    with center:

        start = st.button(
            "Build My Learning Path →",
            type="primary",
            use_container_width=True
        )

    st.write("")

    cols = st.columns(4)

    steps = [

        (
            "01",
            "Understand you",
            "Goals, skills and interests become the starting point."
        ),

        (
            "02",
            "Find the gaps",
            "Readiness, prerequisites and blockers are analyzed."
        ),

        (
            "03",
            "Choose the move",
            "One explainable next action instead of random lists."
        ),

        (
            "04",
            "Adapt with you",
            "Feedback and progress keep the path responsive."
        ),

    ]

    for col, (num, title, copy) in zip(cols, steps):

        with col:

            st.caption(f"{num} · PATHPILOT")

            st.markdown(f"## {title}")

            st.write(copy)

    if start:

        st.session_state.stage = "profiling"

        st.rerun()


# =========================================================
# PROFILE / ONBOARDING PAGE
# FIXED UI
# =========================================================

def profiling(engine):

    # Premium centered onboarding header

    st.markdown("""
    <div style="
        max-width:820px;
        margin:30px auto 28px;
        text-align:center;
    ">

        <div style="
            display:inline-flex;
            align-items:center;
            gap:7px;
            padding:7px 14px;
            border-radius:999px;
            background:#F0EFFF;
            border:1px solid #DDD9FF;
            color:#635BFF;
            font-size:11px;
            font-weight:800;
            letter-spacing:.09em;
            text-transform:uppercase;
        ">
            ✦ Your personalized journey starts here
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(34px,4vw,52px);
            font-weight:800;
            letter-spacing:-.045em;
            line-height:1.08;
            color:#172033;
            margin-top:18px;
        ">
            Let’s understand where you are
            <span style="color:#635BFF;"> and where you’re going.</span>
        </div>

        <div style="
            font-size:16px;
            line-height:1.7;
            color:#6E778B;
            margin:14px auto 0;
            max-width:680px;
        ">
            A few details are all PathPilot needs to analyze your starting point and build a learning path around you.
        </div>

    </div>
    """, unsafe_allow_html=True)


    # Progress indicator

    st.markdown("""
    <div style="
        max-width:920px;
        margin:0 auto 26px;
        display:flex;
        align-items:center;
        justify-content:center;
        gap:10px;
    ">

        <div style="
            height:8px;
            width:33%;
            border-radius:999px;
            background:#635BFF;
        "></div>

        <div style="
            height:8px;
            width:33%;
            border-radius:999px;
            background:#E5E7EE;
        "></div>

        <div style="
            height:8px;
            width:33%;
            border-radius:999px;
            background:#E5E7EE;
        "></div>

    </div>
    """, unsafe_allow_html=True)


    # CENTER THE ENTIRE FORM

    left_space, form_area, right_space = st.columns([1, 2.25, 1])

    with form_area:

        with st.form("profile_form"):

            # -------------------------------------------------
            # SECTION 01
            # -------------------------------------------------

            with st.container(border=True):

                st.markdown("""
                <div style="
                    display:flex;
                    align-items:flex-start;
                    gap:14px;
                    margin-bottom:20px;
                ">

                    <div style="
                        width:42px;
                        height:42px;
                        min-width:42px;
                        border-radius:13px;
                        background:#F0EFFF;
                        color:#635BFF;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-family:Manrope;
                        font-weight:800;
                        font-size:15px;
                    ">
                        01
                    </div>

                    <div>
                        <div style="
                            font-family:Manrope;
                            font-size:22px;
                            font-weight:800;
                            letter-spacing:-.025em;
                            color:#172033;
                        ">
                            Your destination
                        </div>

                        <div style="
                            font-size:14px;
                            color:#7A8496;
                            margin-top:3px;
                        ">
                            Tell us what you're working towards.
                        </div>
                    </div>

                </div>
                """, unsafe_allow_html=True)


                name = st.text_input(
                    "What should we call you?",
                    placeholder="e.g. Akshaya Reddy"
                )


                goal = st.selectbox(
                    "What's your career goal?",
                    career_options()
                )


                natural = st.text_area(
                    "Describe your goal in your own words",
                    placeholder=(
                        "Example: I want to become a Machine Learning Engineer, "
                        "build strong practical skills, create projects and prepare "
                        "for internship opportunities."
                    )
                )


            st.write("")


            # -------------------------------------------------
            # SECTION 02
            # -------------------------------------------------

            with st.container(border=True):

                st.markdown("""
                <div style="
                    display:flex;
                    align-items:flex-start;
                    gap:14px;
                    margin-bottom:20px;
                ">

                    <div style="
                        width:42px;
                        height:42px;
                        min-width:42px;
                        border-radius:13px;
                        background:#EEF7FF;
                        color:#3673B8;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-family:Manrope;
                        font-weight:800;
                        font-size:15px;
                    ">
                        02
                    </div>

                    <div>
                        <div style="
                            font-family:Manrope;
                            font-size:22px;
                            font-weight:800;
                            letter-spacing:-.025em;
                            color:#172033;
                        ">
                            Your current position
                        </div>

                        <div style="
                            font-size:14px;
                            color:#7A8496;
                            margin-top:3px;
                        ">
                            Help PathPilot understand your current starting point.
                        </div>
                    </div>

                </div>
                """, unsafe_allow_html=True)


                level = st.select_slider(
                    "How would you describe your current experience?",
                    options=[
                        "Beginner",
                        "Intermediate",
                        "Advanced"
                    ],
                    value="Beginner"
                )


                st.write("")


                skills = st.text_input(
                    "What skills do you already have?",
                    placeholder="e.g. Python, SQL, Git, HTML"
                )


                interests = st.text_input(
                    "What topics genuinely interest you?",
                    placeholder="e.g. Artificial Intelligence, Data Science, Web Development"
                )


            st.write("")


            # -------------------------------------------------
            # SECTION 03
            # -------------------------------------------------

            with st.container(border=True):

                st.markdown("""
                <div style="
                    display:flex;
                    align-items:flex-start;
                    gap:14px;
                    margin-bottom:20px;
                ">

                    <div style="
                        width:42px;
                        height:42px;
                        min-width:42px;
                        border-radius:13px;
                        background:#F1FAF5;
                        color:#16835A;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-family:Manrope;
                        font-weight:800;
                        font-size:15px;
                    ">
                        03
                    </div>

                    <div>
                        <div style="
                            font-family:Manrope;
                            font-size:22px;
                            font-weight:800;
                            letter-spacing:-.025em;
                            color:#172033;
                        ">
                            Your learning reality
                        </div>

                        <div style="
                            font-size:14px;
                            color:#7A8496;
                            margin-top:3px;
                        ">
                            A realistic learning path should fit your actual schedule.
                        </div>
                    </div>

                </div>
                """, unsafe_allow_html=True)


                left, right = st.columns(2)


                with left:

                    hours = st.number_input(
                        "Hours available each week",
                        min_value=1,
                        max_value=80,
                        value=10
                    )


                with right:

                    weeks = st.number_input(
                        "Your target timeline (weeks)",
                        min_value=1,
                        max_value=104,
                        value=24
                    )


                style = st.selectbox(
                    "How do you prefer to learn?",
                    [
                        "visual",
                        "reading",
                        "hands-on",
                        "video",
                        "mixed"
                    ]
                )


            st.write("")


            # -------------------------------------------------
            # FINAL ACTION
            # -------------------------------------------------

            st.markdown("""
            <div style="
                text-align:center;
                margin:8px 0 14px;
            ">
                <div style="
                    font-family:Manrope;
                    font-size:18px;
                    font-weight:750;
                    color:#172033;
                ">
                    Ready to build your personalized path?
                </div>

                <div style="
                    font-size:13px;
                    color:#7A8496;
                    margin-top:4px;
                ">
                    PathPilot will analyze your profile, skill gaps and learning priorities.
                </div>
            </div>
            """, unsafe_allow_html=True)


            submit = st.form_submit_button(
                "Generate My Intelligence Path →",
                type="primary",
                use_container_width=True
            )


    # -------------------------------------------------
    # FORM SUBMISSION
    # -------------------------------------------------

    if not submit:
        return


    if not name.strip():

        st.error(
            "Please enter your name so PathPilot can personalize your learning journey."
        )

        return


    try:

        profile = LearnerProfile(

            name=name.strip(),

            career_goal=goal,

            natural_language_goal=natural.strip(),

            experience_level={
                "Beginner": 1,
                "Intermediate": 3,
                "Advanced": 5
            }[level],

            current_skills=[
                s.strip()
                for s in skills.split(",")
                if s.strip()
            ],

            interests=[
                s.strip()
                for s in interests.split(",")
                if s.strip()
            ],

            completed_courses=[],

            weekly_hours=int(hours),

            timeline_weeks=int(weeks),

            preferred_learning_style=style,
        )


        st.session_state.profile = profile


        with st.spinner(
            "PathPilot is analyzing your learning profile..."
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
        hero_html(
            "Decision engine",
            "Your next best action",
            "One focused decision based on your current learning intelligence.",
        ),
        unsafe_allow_html=True
    )


    if not isinstance(nba, dict):

        st.info("No recommendation is available yet.")

        return


    skill = nba.get("skill", "Your next step")

    score = nba.get("score", "—")

    hours = nba.get("est_hours", "—")

    difficulty = nba.get("difficulty", "—")


    st.markdown(f"""
    <div style="
        background:linear-gradient(135deg,#625BFF,#827BFF);
        border-radius:24px;
        padding:30px;
        color:white;
        box-shadow:0 18px 48px rgba(98,91,255,.20);
    ">

        <div style="
            font-size:11px;
            font-weight:800;
            letter-spacing:.1em;
            text-transform:uppercase;
            opacity:.8;
        ">
            PathPilot's decision
        </div>

        <div style="
            font-family:Manrope;
            font-size:clamp(28px,4vw,44px);
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
            margin-top:22px;
        ">

            <div style="
                background:rgba(255,255,255,.14);
                border:1px solid rgba(255,255,255,.18);
                border-radius:14px;
                padding:10px 14px;
                min-width:130px;
            ">
                <small style="opacity:.75;">CONFIDENCE</small>

                <div style="
                    font-family:Space Mono;
                    font-weight:700;
                    margin-top:4px;
                ">
                    {esc(score)}
                </div>
            </div>


            <div style="
                background:rgba(255,255,255,.14);
                border:1px solid rgba(255,255,255,.18);
                border-radius:14px;
                padding:10px 14px;
                min-width:130px;
            ">
                <small style="opacity:.75;">EST. EFFORT</small>

                <div style="
                    font-family:Space Mono;
                    font-weight:700;
                    margin-top:4px;
                ">
                    {esc(hours)} hrs
                </div>
            </div>


            <div style="
                background:rgba(255,255,255,.14);
                border:1px solid rgba(255,255,255,.18);
                border-radius:14px;
                padding:10px 14px;
                min-width:130px;
            ">
                <small style="opacity:.75;">DIFFICULTY</small>

                <div style="
                    font-family:Space Mono;
                    font-weight:700;
                    margin-top:4px;
                ">
                    {esc(difficulty)}
                </div>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)


    st.write("")


    left, right = st.columns([1.35, .65])


    reasons = nba.get("reasons") or []

    if not isinstance(reasons, list):
        reasons = [reasons]


    with left:

        with st.container(border=True):

            st.markdown("### Why this, why now?")

            st.caption(
                "The signals that influenced the recommendation."
            )

            if reasons:

                for reason in reasons:

                    st.markdown(
                        f"✓ &nbsp; {esc(reason)}",
                        unsafe_allow_html=True
                    )

            else:

                st.write(
                    "This step was selected from the learner profile and current learning path."
                )


    with right:

        with st.container(border=True):

            st.markdown("### Decision score")

            breakdown = nba.get("score_breakdown") or {}

            if isinstance(breakdown, dict) and breakdown:

                for key, value in breakdown.items():

                    try:

                        progress = max(
                            0.0,
                            min(1.0, float(value) / 100)
                        )

                    except Exception:

                        progress = 0.0


                    st.caption(
                        str(key)
                        .replace("_", " ")
                        .title()
                    )

                    st.progress(progress)

            else:

                st.caption(
                    "Detailed score signals are unavailable for this recommendation."
                )


    st.write("")


    with st.container(border=True):

        st.markdown(
            "### Does this recommendation feel right?"
        )

        st.caption(
            "Feedback is used by the adaptive engine to adjust future recommendations."
        )


        c1, c2, c3 = st.columns(3)

        choice = None


        with c1:

            if st.button(
                "Too easy",
                use_container_width=True
            ):
                choice = "too_easy"


        with c2:

            if st.button(
                "Appropriate",
                type="primary",
                use_container_width=True
            ):
                choice = "appropriate"


        with c3:

            if st.button(
                "Too difficult",
                use_container_width=True
            ):
                choice = "too_difficult"


    if choice and adaptive_engine:

        result = safe_call(

            getattr(
                adaptive_engine,
                "apply_feedback",
                None
            ),

            st.session_state.profile,

            nba.get("skill"),

            choice,

            st.session_state.adaptation_state,
        )


        if isinstance(result, dict):

            if result.get(
                "updated_recommendation"
            ) is not None:

                output["next_best_action"] = (
                    result["updated_recommendation"]
                )


            if result.get(
                "updated_path_health"
            ) is not None:

                output["path_health"] = (
                    result["updated_path_health"]
                )


            if result.get(
                "updated_risks"
            ) is not None:

                output["risks"] = (
                    result["updated_risks"]
                )


            st.session_state.engine_output = output


            st.success(
                result.get(
                    "adaptation_message",
                    "Your path was updated."
                )
            )


            st.rerun()


    if assistant:

        with st.expander("See AI explanation"):

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
                answer or "Explanation unavailable."
            )


# =========================================================
# PATH HEALTH
# =========================================================

def health_page():

    output = st.session_state.engine_output or {}

    health = output.get("path_health") or {}

    risks = output.get("risks") or []


    st.markdown(
        hero_html(
            "Diagnostics",
            "Path health",
            "A diagnostic view of how sustainable the current learning path is.",
        ),
        unsafe_allow_html=True
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


    left, right = st.columns([.75, 1.25])


    with left:

        with st.container(border=True):

            st.caption("OVERALL HEALTH")

            st.markdown(
                f"""
                <div style="
                    font-family:Space Mono;
                    font-size:54px;
                    font-weight:700;
                    color:#635BFF;
                ">
                    {esc(score)}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"### {esc(status)}",
                unsafe_allow_html=True
            )


    with right:

        with st.container(border=True):

            st.markdown(
                "### What is influencing your path?"
            )


            factors = (
                health.get("contributing_factors", [])
                if isinstance(health, dict)
                else []
            )


            if factors:

                for factor in factors:

                    st.markdown(
                        f"✓ &nbsp; {esc(factor)}",
                        unsafe_allow_html=True
                    )

            else:

                st.caption(
                    "No detailed contributing factors are available yet."
                )


    st.write("")

    st.markdown("### Detected risks")


    if not risks:

        st.success("No active risks detected.")

        return


    for risk in risks:

        with st.container(border=True):

            if isinstance(risk, dict):

                severity = str(
                    risk.get("severity", "low")
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


                st.caption(
                    f"{severity} PRIORITY"
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

    output = st.session_state.engine_output or {}

    profile = st.session_state.profile


    st.markdown(
        hero_html(
            "Path intelligence",
            "Ask about your learning path.",
            "Get explanations grounded in the recommendation, roadmap and progress.",
        ),
        unsafe_allow_html=True
    )


    prompts = [

        "What should I learn next?",

        "What is blocking my progress?",

        "How can I improve my path?",

        "Which skill has the highest impact?",

    ]


    cols = st.columns(4)


    for i, prompt in enumerate(prompts):

        with cols[i]:

            if st.button(
                prompt,
                key=f"prompt_{i}",
                use_container_width=True
            ):

                st.session_state.assistant_question = prompt


    question = st.text_input(

        "Ask PathPilot",

        value=st.session_state.assistant_question,

        placeholder="Ask something about your path...",
    )


    st.session_state.assistant_question = question


    if question:

        answer = safe_call(

            getattr(
                assistant,
                "answer_path_question",
                None
            )
            if assistant
            else None,

            profile,

            output,

            question,
        )


        with st.container(border=True):

            st.caption("PATHPILOT INSIGHT")

            st.markdown(
                answer
                or "I could not generate an answer right now."
            )


# =========================================================
# APPLICATION SHELL
# =========================================================

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

            current = options[0]


        section = st.radio(

            "Navigate",

            options,

            index=options.index(current),

            label_visibility="collapsed",
        )


        st.session_state.nav_section = section


        st.divider()


        st.markdown(
            f"**{esc(getattr(profile, 'name', 'Learner'))}**",
            unsafe_allow_html=True
        )


        st.caption(
            str(
                getattr(
                    profile,
                    "career_goal",
                    "Learning path"
                )
            )
        )


        if st.button(
            "Restart journey",
            use_container_width=True
        ):

            for key in [

                "stage",

                "profile",

                "engine_output",

                "adaptation_state",

                "roadmap_progress",

                "nav_section",

                "assistant_question",

            ]:

                st.session_state.pop(key, None)


            init_state()

            st.rerun()


    health = output.get("path_health") or {}


    status = (

        health.get("status", "Unknown")

        if isinstance(health, dict)

        else "Unknown"

    )


    score = (

        health.get("health_score", "—")

        if isinstance(health, dict)

        else "—"

    )


    top_left, top_right = st.columns([4, 1])


    with top_left:

        st.markdown(

            hero_html(

                "Your learning workspace",

                f"Good to see you, {esc(getattr(profile, 'name', 'there'))}.",

                "Everything important about your learning path — analyzed in one place.",

            ),

            unsafe_allow_html=True

        )


    with top_right:

        st.markdown(f"""

        <div style="
            background:white;
            border:1px solid #E6EAF0;
            border-radius:18px;
            padding:16px;
            margin-top:22px;
        ">

            <div style="
                font-size:10px;
                font-weight:800;
                letter-spacing:.09em;
                color:#98A0B3;
            ">
                PATH STATUS
            </div>

            <div style="
                font-family:Manrope;
                font-size:20px;
                font-weight:800;
                margin-top:6px;
                color:#172033;
            ">
                {esc(status)}
            </div>

            <div style="
                font-size:12px;
                color:#6E778B;
                margin-top:4px;
            ">
                {esc(score)} / 100 health score
            </div>

        </div>

        """, unsafe_allow_html=True)


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


# =========================================================
# INITIALIZATION
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
        assistant
    )

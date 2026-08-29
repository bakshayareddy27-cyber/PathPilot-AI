import streamlit as st

from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant

from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="PathPilot AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================================
# DESIGN SYSTEM + GLOBAL CSS
# ==========================================================

def inject_css():
    st.markdown(
        """
        <style>

        /* ==========================================================
           1. DESIGN TOKENS
        ========================================================== */

        :root {
            --pp-bg: #09090b;
            --pp-surface: #111114;
            --pp-surface-2: #18181c;
            --pp-surface-3: #202026;

            --pp-border: #2a2a31;
            --pp-border-soft: #202027;

            --pp-text: #f4f4f5;
            --pp-muted: #a1a1aa;
            --pp-subtle: #71717a;

            --pp-accent: #8b5cf6;
            --pp-accent-soft: rgba(139, 92, 246, 0.15);

            --pp-success: #34d399;
            --pp-success-soft: rgba(52, 211, 153, 0.12);

            --pp-warning: #fbbf24;
            --pp-warning-soft: rgba(251, 191, 36, 0.12);

            --pp-danger: #fb7185;
            --pp-danger-soft: rgba(251, 113, 133, 0.12);

            --pp-radius-sm: 10px;
            --pp-radius-md: 16px;
            --pp-radius-lg: 24px;

            --pp-shadow:
                0 20px 60px rgba(0, 0, 0, 0.35);
        }


        /* ==========================================================
           2. GLOBAL STYLES
        ========================================================== */

        .stApp {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(139, 92, 246, 0.08),
                    transparent 30%
                ),
                var(--pp-bg);
            color: var(--pp-text);
        }

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        header {
            background: transparent !important;
        }

        .block-container {
            max-width: 1450px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            color: var(--pp-text);
            letter-spacing: -0.03em;
        }

        p {
            color: var(--pp-muted);
        }


        /* ==========================================================
           3. APP SHELL
        ========================================================== */

        .pp-shell {
            max-width: 1280px;
            margin: 0 auto;
        }


        /* ==========================================================
           4. SIDEBAR
        ========================================================== */

        [data-testid="stSidebar"] {
            background: #0d0d10;
            border-right: 1px solid var(--pp-border);
        }

        [data-testid="stSidebar"] * {
            color: var(--pp-text);
        }


        /* ==========================================================
           5. TYPOGRAPHY
        ========================================================== */

        .pp-eyebrow {
            color: var(--pp-accent);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .pp-title {
            font-size: clamp(2.4rem, 5vw, 4.5rem);
            font-weight: 800;
            line-height: 1.05;
            margin: 1rem 0;
            letter-spacing: -0.055em;
        }

        .pp-subtitle {
            max-width: 680px;
            font-size: 1.08rem;
            line-height: 1.7;
            color: var(--pp-muted);
        }

        .pp-section-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .pp-section-subtitle {
            color: var(--pp-muted);
            margin-bottom: 1.5rem;
        }


        /* ==========================================================
           6. BUTTONS
        ========================================================== */

        .stButton > button {
            border-radius: 12px;
            border: 1px solid var(--pp-border);
            background: var(--pp-surface-2);
            color: var(--pp-text);
            font-weight: 600;
            transition: all 0.2s ease;
            min-height: 42px;
        }

        .stButton > button:hover {
            border-color: var(--pp-accent);
            background: var(--pp-accent-soft);
            transform: translateY(-1px);
        }

        .stFormSubmitButton > button {
            width: 100%;
            background: var(--pp-accent);
            color: white;
            border: none;
            border-radius: 12px;
            min-height: 48px;
            font-weight: 700;
        }


        /* ==========================================================
           7. CARDS
        ========================================================== */

        .pp-card {
            background: rgba(24, 24, 28, 0.78);
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius-md);
            padding: 1.35rem;
            box-shadow: var(--pp-shadow);
        }

        .pp-card-label {
            color: var(--pp-subtle);
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .pp-card-value {
            font-size: 1.8rem;
            font-weight: 750;
            margin-top: 0.35rem;
            color: var(--pp-text);
        }


        /* ==========================================================
           8. LANDING PAGE
        ========================================================== */

        .pp-hero {
            padding: 5rem 0 3rem 0;
        }

        .pp-hero-highlight {
            color: var(--pp-accent);
        }

        .pp-feature {
            height: 100%;
            background: var(--pp-surface);
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius-md);
            padding: 1.5rem;
        }

        .pp-feature-number {
            color: var(--pp-accent);
            font-weight: 800;
            font-size: 0.85rem;
        }

        .pp-feature-title {
            font-size: 1.1rem;
            font-weight: 700;
            margin: 0.8rem 0 0.5rem;
        }

        .pp-feature-text {
            color: var(--pp-muted);
            line-height: 1.6;
            font-size: 0.92rem;
        }


        /* ==========================================================
           9. ONBOARDING
        ========================================================== */

        .pp-onboarding {
            max-width: 900px;
            margin: 2rem auto;
            background: var(--pp-surface);
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius-lg);
            padding: 2rem;
        }


        /* ==========================================================
           10. DASHBOARD
        ========================================================== */

        .pp-dashboard-hero {
            margin-bottom: 2rem;
        }


        /* ==========================================================
           11. NEXT BEST ACTION
        ========================================================== */

        .pp-nba {
            background:
                linear-gradient(
                    135deg,
                    rgba(139, 92, 246, 0.16),
                    rgba(24, 24, 28, 0.95)
                );
            border: 1px solid rgba(139, 92, 246, 0.35);
            border-radius: var(--pp-radius-lg);
            padding: 1.8rem;
            margin-bottom: 1.5rem;
        }

        .pp-nba-label {
            color: #c4b5fd;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .pp-nba-title {
            font-size: 2rem;
            font-weight: 750;
            margin: 0.5rem 0;
        }


        /* ==========================================================
           12. ROADMAP
        ========================================================== */

        .pp-roadmap-step {
            position: relative;
            padding: 1.25rem;
            margin-bottom: 1rem;
            background: var(--pp-surface);
            border: 1px solid var(--pp-border);
            border-radius: var(--pp-radius-md);
        }

        .pp-roadmap-step.active {
            border-color: rgba(139, 92, 246, 0.6);
            background: rgba(139, 92, 246, 0.08);
        }

        .pp-roadmap-step.completed {
            border-color: rgba(52, 211, 153, 0.4);
        }


        /* ==========================================================
           13. PATH HEALTH
        ========================================================== */

        .pp-health {
            border-radius: var(--pp-radius-md);
            padding: 1.4rem;
            border: 1px solid var(--pp-border);
            background: var(--pp-surface);
        }

        .pp-health-score {
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.05em;
        }


        /* ==========================================================
           14. AI ASSISTANT
        ========================================================== */

        .pp-ai {
            background:
                linear-gradient(
                    145deg,
                    rgba(139, 92, 246, 0.10),
                    rgba(24, 24, 28, 0.95)
                );
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: var(--pp-radius-lg);
            padding: 1.5rem;
        }

        .pp-ai-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .pp-ai-icon {
            width: 40px;
            height: 40px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--pp-accent-soft);
            font-size: 1.2rem;
        }

        .pp-answer {
            margin-top: 1rem;
            padding: 1.2rem;
            border-radius: 14px;
            background: rgba(9, 9, 11, 0.65);
            border: 1px solid var(--pp-border);
            line-height: 1.7;
        }


        /* ==========================================================
           15. RESPONSIVE ADJUSTMENTS
        ========================================================== */

        @media (max-width: 768px) {

            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .pp-hero {
                padding-top: 2rem;
            }

            .pp-title {
                font-size: 2.5rem;
            }

        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# SESSION STATE
# ==========================================================

def initialize_state():

    defaults = {
        "page": "Home",
        "profile": None,
        "engine": None,
        "engine_output": None,
        "adaptive_engine": None,
        "adaptation_state": None,
        "ai_assistant": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ==========================================================
# ENGINE
# ==========================================================

def calculate_engine_output(profile, engine):

    next_best_action = engine.calculate_next_best_action(profile)
    path_health = engine.calculate_path_health(profile)
    risks = engine.detect_risks(profile)

    return {
        "next_best_action": next_best_action,
        "path_health": path_health,
        "risks": risks or [],
    }


# ==========================================================
# SIDEBAR
# ==========================================================

def render_sidebar():

    with st.sidebar:

        st.markdown(
            """
            <div style="padding: 0.5rem 0 1.5rem 0;">
                <div style="font-size: 1.35rem; font-weight: 800;">
                    ✦ PathPilot
                </div>
                <div style="color: #71717a; font-size: 0.82rem;">
                    Intelligent learning paths
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        pages = ["Home", "Dashboard", "Roadmap"]

        for page in pages:

            if st.button(
                page,
                use_container_width=True,
                key=f"nav_{page}",
            ):
                st.session_state.page = page

        st.markdown("---")

        if st.session_state.profile:

            profile = st.session_state.profile

            st.markdown(
                f"""
                <div class="pp-card">
                    <div class="pp-card-label">Current goal</div>
                    <div style="margin-top:0.5rem;font-weight:650;">
                        {profile.career_goal}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "Reset profile",
                use_container_width=True,
            ):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]

                st.rerun()


# ==========================================================
# LANDING PAGE
# ==========================================================

def render_home():

    st.markdown(
        """
        <div class="pp-hero">

            <div class="pp-eyebrow">
                PERSONALIZED LEARNING INTELLIGENCE
            </div>

            <div class="pp-title">
                Stop guessing your next move.<br>
                <span class="pp-hero-highlight">
                    Decide intelligently.
                </span>
            </div>

            <div class="pp-subtitle">
                PathPilot analyzes where you are, where you want to go,
                and what is blocking your progress — then identifies
                the most valuable thing to learn next.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    features = [
        (
            "01",
            "Decide what matters",
            "Move beyond generic course recommendations and focus on the next skill that creates meaningful progress.",
        ),
        (
            "02",
            "Detect the blockers",
            "Understand prerequisite gaps and risks before wasting time moving in the wrong direction.",
        ),
        (
            "03",
            "Monitor your path",
            "Track learning health, identify pressure points, and continuously understand where your roadmap stands.",
        ),
    ]

    for column, feature in zip(
        [col1, col2, col3],
        features,
    ):

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

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.button(
        "Build my learning path →",
        type="primary",
    ):
        st.session_state.page = "Onboarding"
        st.rerun()


# ==========================================================
# ONBOARDING
# ==========================================================

def render_onboarding():

    st.markdown(
        """
        <div class="pp-onboarding">

            <div class="pp-eyebrow">
                SET UP YOUR PATH
            </div>

            <h1 style="margin-bottom:0.4rem;">
                Tell PathPilot where you're going.
            </h1>

            <p style="margin-bottom:1.5rem;">
                Your information is used to build a personalized
                learning recommendation.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("profile_form"):

        name = st.text_input(
            "Your name",
            placeholder="e.g. Akshaya",
        )

        career_goal = st.text_input(
            "Career goal",
            placeholder="e.g. Machine Learning Engineer",
        )

        natural_goal = st.text_area(
            "Describe your goal",
            placeholder="What do you want to achieve?",
        )

        experience = st.selectbox(
            "Current experience level",
            [
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
        )

        skills_text = st.text_area(
            "Current skills",
            placeholder="Python, SQL, Machine Learning...",
        )

        interests_text = st.text_input(
            "Areas you're interested in",
            placeholder="AI, Data Science, Backend...",
        )

        col1, col2 = st.columns(2)

        with col1:
            weekly_hours = st.number_input(
                "Hours available per week",
                min_value=1,
                max_value=80,
                value=10,
            )

        with col2:
            timeline_weeks = st.number_input(
                "Timeline (weeks)",
                min_value=1,
                max_value=260,
                value=24,
            )

        learning_style = st.selectbox(
            "Preferred learning style",
            [
                "Visual",
                "Practical",
                "Reading",
                "Mixed",
            ],
        )

        submitted = st.form_submit_button(
            "Generate my path",
        )

    if submitted:

        if not name.strip() or not career_goal.strip():

            st.error(
                "Please enter your name and career goal."
            )
            return

        skills = [
            skill.strip()
            for skill in skills_text.split(",")
            if skill.strip()
        ]

        interests = [
            interest.strip()
            for interest in interests_text.split(",")
            if interest.strip()
        ]

        profile = LearnerProfile(
            name=name.strip(),
            career_goal=career_goal.strip(),
            natural_language_goal=natural_goal.strip(),
            experience_level=experience,
            current_skills=skills,
            interests=interests,
            completed_courses=[],
            weekly_hours=weekly_hours,
            timeline_weeks=timeline_weeks,
            preferred_learning_style=learning_style,
        )

        try:

            engine = IntelligenceEngine()

            engine_output = calculate_engine_output(
                profile,
                engine,
            )

            st.session_state.profile = profile
            st.session_state.engine = engine
            st.session_state.engine_output = engine_output

            st.session_state.adaptive_engine = AdaptiveEngine(
                engine
            )

            st.session_state.adaptation_state = AdaptationState()

            st.session_state.ai_assistant = AIAssistant()

            st.session_state.page = "Dashboard"

            st.rerun()

        except Exception as error:

            st.error(
                f"PathPilot couldn't generate the path: {error}"
            )


# ==========================================================
# APP
# ==========================================================

def main():

    initialize_state()
    inject_css()
    render_sidebar()

    page = st.session_state.page

    if page == "Home":
        render_home()

    elif page == "Onboarding":
        render_onboarding()

    elif page == "Dashboard":

        if not st.session_state.profile:
            st.session_state.page = "Onboarding"
            st.rerun()

        render_dashboard(
            profile=st.session_state.profile,
            engine_output=st.session_state.engine_output,
            ai_assistant=st.session_state.ai_assistant,
            adaptive_engine=st.session_state.adaptive_engine,
            adaptation_state=st.session_state.adaptation_state,
        )

    elif page == "Roadmap":

        if not st.session_state.profile:
            st.session_state.page = "Onboarding"
            st.rerun()

        render_roadmap(
            profile=st.session_state.profile,
            engine_output=st.session_state.engine_output,
        )


if __name__ == "__main__":
    main()

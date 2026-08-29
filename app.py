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
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# Global style
# ----------------------------------------------------------------------
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; }
    .ppai-hero {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        padding: 2.2rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.2rem;
    }
    .ppai-hero h1 { color: white; font-size: 2.1rem; margin-bottom: 0.2rem; }
    .ppai-hero p { color: rgba(255,255,255,0.9); font-size: 1.05rem; }
    .ppai-card {
        background: #1a1c24;
        border: 1px solid #2a2d39;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1rem;
    }
    .ppai-nba-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        border: 1px solid #6366f1;
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1rem;
    }
    .ppai-badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
    }
    .badge-healthy { background:#065f46; color:#a7f3d0; }
    .badge-atrisk { background:#78350f; color:#fde68a; }
    .badge-critical { background:#7f1d1d; color:#fecaca; }
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
        "nav_section": "🏠 Overview",
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


# ----------------------------------------------------------------------
# WELCOME
# ----------------------------------------------------------------------
def render_welcome():
    st.markdown(
        """
        <div class="ppai-hero">
            <h1>🧭 PathPilot AI</h1>
            <p><em>"Don't just recommend what to learn. Decide what to learn next."</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        PathPilot AI analyzes your **skills**, **career goals**, **prerequisites**,
        **available time**, **experience level**, and **interests** to generate a
        personalized, prerequisite-aware learning roadmap — and tells you exactly
        what to learn next, with transparent, explainable reasoning.
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="ppai-card">🎯 <b>Next Best Action</b><br>A single, scored recommendation — not just a list.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="ppai-card">🧩 <b>Prerequisite Intelligence</b><br>Recursive root-blocker detection prevents unrealistic jumps.</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="ppai-card">❤️ <b>Path Health Monitor</b><br>Healthy / At Risk / Critical, based on real signals.</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🚀 Build My Learning Path", type="primary", use_container_width=False):
        st.session_state.stage = "profiling"
        st.rerun()


# ----------------------------------------------------------------------
# PROFILING
# ----------------------------------------------------------------------
def render_profiling():
    st.markdown("## 👤 Tell PathPilot About Yourself")
    st.caption("This takes about a minute. Your answers drive every recommendation.")

    career_options = get_career_options()

    with st.form("profiling_form"):
        name = st.text_input("Name", placeholder="e.g. Asha Rao")

        career_goal = st.selectbox("Career Goal", options=career_options)

        natural_language_goal = st.text_area(
            "In your own words, what do you want to achieve?",
            placeholder="e.g. I want to become an ML engineer within 6 months and land an internship.",
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

        col1, col2 = st.columns(2)
        with col1:
            weekly_hours = st.number_input("Weekly Learning Hours", min_value=1, max_value=80, value=10)
        with col2:
            timeline_weeks = st.number_input("Target Timeline (weeks)", min_value=1, max_value=104, value=24)

        preferred_learning_style = st.selectbox(
            "Preferred Learning Style",
            options=["visual", "reading", "hands-on", "video", "mixed"],
        )

        submitted = st.form_submit_button("✨ Generate My Path", type="primary")

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
    st.markdown("## 🎯 Your Next Best Action")

    engine_output = st.session_state.engine_output or {}
    nba = engine_output.get("next_best_action")

    if not nba:
        st.info("No further recommendation right now — you may be caught up with your current goal!")
        return

    st.markdown(
        f"""
        <div class="ppai-nba-card">
            <h2 style="color:white; margin-bottom:0.3rem;">📘 {nba.get('skill', 'N/A')}</h2>
            <p style="color:#c7d2fe;">Confidence Score: <b>{nba.get('score', 'N/A')}</b> ·
            Estimated: <b>{nba.get('est_hours', 'N/A')} hrs</b> ·
            Difficulty: <b>{nba.get('difficulty', 'N/A')}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reasons = nba.get("reasons", [])
    if reasons:
        st.markdown("**Why this recommendation:**")
        for r in reasons:
            st.markdown(f"- {r}")

    breakdown = nba.get("score_breakdown", {})
    if breakdown:
        st.markdown("**Score Breakdown:**")
        cols = st.columns(min(len(breakdown), 4) or 1)
        for i, (factor, value) in enumerate(breakdown.items()):
            with cols[i % len(cols)]:
                st.metric(factor.replace("_", " ").title(), value)

    render_adaptive_feedback(nba)

    if assistant:
        with st.expander("🤖 AI Explanation", expanded=False):
            with st.spinner("Generating explanation..."):
                explanation = safe_call(assistant.explain_next_best_action, st.session_state.profile, nba)
            st.write(explanation or "Explanation unavailable right now.")


def render_adaptive_feedback(nba):
    st.markdown("#### How does this feel for you?")
    col1, col2, col3 = st.columns(3)
    skill_name = nba.get("skill")

    feedback_clicked = None
    with col1:
        if st.button("👍 Too Easy", use_container_width=True):
            feedback_clicked = "too_easy"
    with col2:
        if st.button("👌 Appropriate", use_container_width=True):
            feedback_clicked = "appropriate"
    with col3:
        if st.button("😵 Too Difficult", use_container_width=True):
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
            st.success(f"⚡ Your learning path has been adapted based on your feedback.")
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
    st.markdown("## 🤖 AI Assistant")
    st.caption("Ask about your recommendations, roadmap, prerequisites, or risks.")

    engine_output = st.session_state.engine_output or {}
    profile = st.session_state.profile

    if not assistant:
        st.error("AI assistant unavailable.")
        return

    nba = engine_output.get("next_best_action")
    if nba:
        with st.spinner("Preparing explanation..."):
            auto_explanation = safe_call(assistant.explain_next_best_action, profile, nba)
        st.markdown("**Why your next step is recommended:**")
        st.write(auto_explanation or "Explanation unavailable right now.")
        st.divider()

    question = st.text_input(
        "Ask about your learning path...",
        placeholder="e.g. Why should I learn this next? What's blocking my progress? Am I on track?",
    )

    example_cols = st.columns(4)
    examples = [
        "Why should I learn this next?",
        "What is blocking my progress?",
        "Am I on track?",
        "What should I focus on first?",
    ]
    for col, ex in zip(example_cols, examples):
        with col:
            if st.button(ex, use_container_width=True):
                question = ex

    if question:
        with st.spinner("Thinking..."):
            answer = safe_call(assistant.answer_path_question, profile, engine_output, question)
        st.markdown("**Answer:**")
        st.write(answer or "I couldn't generate an answer right now.")


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
        st.markdown(f"### 👋 Hi, {getattr(profile, 'name', 'there')}")
        st.caption(f"Goal: {getattr(profile, 'career_goal', 'N/A')}")
        st.divider()
        section = st.radio(
            "Navigate",
            ["🏠 Overview", "🎯 Next Best Action", "🗺️ Learning Roadmap", "📊 Path Health", "🤖 AI Assistant"],
            index=0,
        )
        st.session_state.nav_section = section
        st.divider()
        if st.button("🔄 Restart"):
            for key in ["stage", "profile", "engine_output", "adaptation_state", "roadmap_progress"]:
                st.session_state.pop(key, None)
            init_session_state()
            st.rerun()

    st.markdown(
        """
        <div class="ppai-hero" style="padding:1.2rem 1.6rem;">
            <h1 style="font-size:1.6rem;">🧭 PathPilot AI</h1>
            <p style="font-size:0.95rem;">Don't just recommend what to learn. Decide what to learn next.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section = st.session_state.nav_section

    if section == "🏠 Overview":
        render_dashboard(profile, engine_output, safe_call, engine)
    elif section == "🎯 Next Best Action":
        render_next_best_action()
    elif section == "🗺️ Learning Roadmap":
        render_roadmap(profile, engine_output, safe_call)
    elif section == "📊 Path Health":
        render_path_health(engine_output)
    elif section == "🤖 AI Assistant":
        render_ai_assistant()


def render_path_health(engine_output):
    st.markdown("## 📊 Path Health")
    health = engine_output.get("path_health") or {}
    risks = engine_output.get("risks") or []

    if not health:
        st.info("Path health data unavailable.")
        return

    status = health.get("status", "Unknown")
    badge_class = {
        "Healthy": "badge-healthy",
        "At Risk": "badge-atrisk",
        "Critical": "badge-critical",
    }.get(status, "badge-atrisk")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Health Score", health.get("health_score", "N/A"))
    with col2:
        st.markdown(f'<span class="ppai-badge {badge_class}">{status}</span>', unsafe_allow_html=True)

    factors = health.get("contributing_factors", [])
    if factors:
        st.markdown("**Contributing Factors:**")
        for f in factors:
            st.markdown(f"- {f}")

    st.markdown("### ⚠️ Detected Risks")
    if not risks:
        st.success("No active risks detected.")
    else:
        for risk in risks:
            if isinstance(risk, dict):
                severity = risk.get("severity", "info")
                message = risk.get("message", "")
                action = risk.get("suggested_action") or risk.get("action")
                icon = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(str(severity).lower(), "ℹ️")
                with st.container():
                    st.markdown(f"{icon} **{severity.title() if isinstance(severity,str) else severity}** — {message}")
                    if action:
                        st.caption(f"Suggested action: {action}")
            else:
                st.markdown(f"- {risk}")

    if assistant:
        with st.expander("🤖 AI Explanation", expanded=False):
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
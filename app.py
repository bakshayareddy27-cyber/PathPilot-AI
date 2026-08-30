import streamlit as st
import pandas as pd
import json
import os

# Import core engine classes
from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant

# Import UI components
from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap

# Set page configuration
st.set_page_config(
    page_title="PathPilot AI | Learning Intelligence Platform",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Custom CSS for Premium SaaS Aesthetic
def apply_custom_theme():
    st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

        /* CSS Variables & Design Tokens */
        :root {
            --bg-main: #F8FAFC;
            --surface-card: #FFFFFF;
            --surface-elevated: #FFFFFF;
            --primary-brand: #4F46E5;
            --primary-hover: #4338CA;
            --primary-light: #EEF2FF;
            --text-primary: #0F172A;
            --text-secondary: #475569;
            --text-muted: #94A3B8;
            --border-color: #E2E8F0;
            --border-focus: #C7D2FE;
            --success: #10B981;
            --success-bg: #ECFDF5;
            --warning: #F59E0B;
            --warning-bg: #FFFBEB;
            --danger: #EF4444;
            --danger-bg: #FEF2F2;
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
            --shadow-subtle: 0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03);
            --shadow-card: 0 4px 6px -1px rgba(15, 23, 42, 0.04), 0 2px 4px -1px rgba(15, 23, 42, 0.02);
            --shadow-hover: 0 10px 15px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -2px rgba(15, 23, 42, 0.03);
        }

        /* Base Application Layout */
        .stApp {
            background-color: var(--bg-main) !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            color: var(--text-primary) !important;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: var(--text-primary) !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF !important;
            border-right: 1px solid var(--border-color) !important;
        }

        section[data-testid="stSidebar"] .block-container {
            padding-top: 2rem !important;
            padding-bottom: 2rem !important;
        }

        /* Navigation Radio Buttons transformed into Tab-like Navigation */
        div[data-testid="stRadio"] > label {
            display: none !important;
        }

        div[data-testid="stRadio"] > div {
            gap: 6px !important;
        }

        div[data-testid="stRadio"] > div > label {
            background-color: transparent !important;
            border-radius: var(--radius-sm) !important;
            padding: 10px 14px !important;
            border: 1px solid transparent !important;
            color: var(--text-secondary) !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
        }

        div[data-testid="stRadio"] > div > label:hover {
            background-color: var(--primary-light) !important;
            color: var(--primary-brand) !important;
        }

        div[data-testid="stRadio"] > div > label[data-checked="true"] {
            background-color: var(--primary-light) !important;
            color: var(--primary-brand) !important;
            font-weight: 600 !important;
            border-color: #C7D2FE !important;
        }

        /* Cards & Container Surfaces */
        .pp-card {
            background: var(--surface-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: var(--shadow-card);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }

        .pp-card:hover {
            box-shadow: var(--shadow-hover);
            border-color: #CBD5E1;
        }

        .pp-card-interactive {
            background: var(--surface-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: var(--shadow-subtle);
            transition: all 0.2s ease;
        }

        .pp-card-interactive:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
            border-color: var(--primary-brand);
        }

        /* Hero Banner */
        .pp-hero {
            background: linear-gradient(135deg, #FFFFFF 0%, #EEF2FF 100%);
            border: 1px solid #C7D2FE;
            border-radius: var(--radius-lg);
            padding: 40px 32px;
            margin-bottom: 32px;
            box-shadow: var(--shadow-card);
        }

        /* Badges & Chips */
        .pp-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        .pp-badge-indigo {
            background-color: #EEF2FF;
            color: #4F46E5;
            border: 1px solid #C7D2FE;
        }

        .pp-badge-emerald {
            background-color: #ECFDF5;
            color: #059669;
            border: 1px solid #A7F3D0;
        }

        .pp-badge-amber {
            background-color: #FFFBEB;
            color: #D97706;
            border: 1px solid #FDE68A;
        }

        .pp-badge-rose {
            background-color: #FEF2F2;
            color: #DC2626;
            border: 1px solid #FECACA;
        }

        /* Streamlit Native Button Overrides */
        .stButton > button {
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            transition: all 0.2s ease !important;
            border: 1px solid var(--border-color) !important;
        }

        .stButton > button[kind="primary"] {
            background-color: var(--primary-brand) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2) !important;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: var(--primary-hover) !important;
            box-shadow: 0 4px 8px rgba(79, 70, 229, 0.3) !important;
            transform: translateY(-1px);
        }

        .stButton > button[kind="secondary"]:hover {
            border-color: var(--primary-brand) !important;
            color: var(--primary-brand) !important;
            background-color: var(--primary-light) !important;
        }

        /* Streamlit Form Input Enhancements */
        .stTextInput input, .stSelectbox select, .stTextArea textarea, .stMultiselect {
            border-radius: var(--radius-sm) !important;
            border: 1px solid var(--border-color) !important;
        }

        .stTextInput input:focus, .stSelectbox select:focus, .stTextArea textarea:focus {
            border-color: var(--primary-brand) !important;
            box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
        }

        /* Custom Metric Cards */
        .pp-metric-val {
            font-family: 'JetBrains Mono', monospace;
            font-size: 2.2rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.1;
        }

        .pp-metric-lbl {
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        /* Hide Streamlit Branding Overhead */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

# Safe Backend Execution Wrapper
def safe_call(func, default, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.warning(f"Engine operational alert: {str(e)}")
        return default

# Load JSON helper safely
def safe_load_json(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

# Core State Initialization
def init_session_state():
    if 'profile' not in st.session_state:
        st.session_state.profile = LearnerProfile()
    if 'intelligence_engine' not in st.session_state:
        st.session_state.intelligence_engine = IntelligenceEngine()
    if 'adaptive_engine' not in st.session_state:
        st.session_state.adaptive_engine = AdaptiveEngine()
    if 'ai_assistant' not in st.session_state:
        st.session_state.ai_assistant = AIAssistant()
    if 'onboarded' not in st.session_state:
        st.session_state.onboarded = False
    if 'engine_output' not in st.session_state:
        st.session_state.engine_output = None
    if 'nav_selection' not in st.session_state:
        st.session_state.nav_selection = "Overview"

# Main App Controller
def main():
    apply_custom_theme()
    init_session_state()

    # If learner has not onboarded, show Welcome / Onboarding experience
    if not st.session_state.onboarded:
        render_onboarding_experience()
    else:
        render_main_application_shell()

# Landing / Onboarding Screen
def render_onboarding_experience():
    # Brand Header
    st.markdown("""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 0 24px 0;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: #4F46E5; color: white; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem;">P</div>
                <span style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 800; color: #0F172A; letter-spacing: -0.02em;">PathPilot <span style="color: #4F46E5;">AI</span></span>
            </div>
            <span class="pp-badge pp-badge-indigo">Learning Intelligence System</span>
        </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
        <div class="pp-hero">
            <span class="pp-badge pp-badge-indigo" style="margin-bottom: 12px;">Strategic Learning Recommender</span>
            <h1 style="font-size: 2.75rem; margin: 12px 0 16px 0; line-height: 1.15; color: #0F172A;">
                Stop guessing.<br/><span style="color: #4F46E5;">Start moving with direction.</span>
            </h1>
            <p style="font-size: 1.1rem; color: #475569; max-width: 680px; line-height: 1.6; margin-bottom: 0;">
                PathPilot evaluates your current skills, career objectives, and personal constraints to decide what you should learn next—and explains exactly why.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Visual Workflow Narrative
    st.markdown("""
        <div style="margin-bottom: 32px;">
            <h4 style="font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.08em; color: #94A3B8; margin-bottom: 16px;">The PathPilot Decision Pipeline</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
                <div class="pp-card-interactive" style="margin-bottom: 0;">
                    <div style="color: #4F46E5; font-weight: 700; font-size: 0.8rem;">01. PROFILE</div>
                    <div style="font-weight: 600; font-size: 0.95rem; margin-top: 4px; color: #0F172A;">Context Capture</div>
                </div>
                <div class="pp-card-interactive" style="margin-bottom: 0;">
                    <div style="color: #4F46E5; font-weight: 700; font-size: 0.8rem;">02. ANALYZE</div>
                    <div style="font-weight: 600; font-size: 0.95rem; margin-top: 4px; color: #0F172A;">Skill Gap Graph</div>
                </div>
                <div class="pp-card-interactive" style="margin-bottom: 0;">
                    <div style="color: #4F46E5; font-weight: 700; font-size: 0.8rem;">03. DECIDE</div>
                    <div style="font-weight: 600; font-size: 0.95rem; margin-top: 4px; color: #0F172A;">Next Best Action</div>
                </div>
                <div class="pp-card-interactive" style="margin-bottom: 0;">
                    <div style="color: #4F46E5; font-weight: 700; font-size: 0.8rem;">04. ROADMAP</div>
                    <div style="font-weight: 600; font-size: 0.95rem; margin-top: 4px; color: #0F172A;">Adaptive Path</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Onboarding Form Container
    st.markdown("""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 32px; box-shadow: var(--shadow-card);">
            <h2 style="font-size: 1.5rem; margin-bottom: 8px;">Configure Your Profile</h2>
            <p style="color: #475569; font-size: 0.95rem; margin-bottom: 28px;">Provide your current background and target aspirations to build your personalized intelligence model.</p>
    """, unsafe_allow_html=True)

    # Load career path options from data
    career_paths_data = safe_load_json("data/career_paths.json")
    career_options = list(career_paths_data.keys()) if career_paths_data else [
        "AI/ML Engineer", "Data Scientist", "Backend Engineer", "Frontend Engineer", "Fullstack Developer"
    ]

    with st.form("onboarding_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 1. Learner Identity & Goals")
            name = st.text_input("Full Name", value="Akshaya Reddy", help="Your profile identifier")
            career_goal = st.selectbox("Target Career Role", options=career_options)
            natural_goal = st.text_area(
                "Describe your goal in your own words",
                value="I want to master AI engineering, build multi-agent systems, and deploy production models.",
                height=100
            )

        with col2:
            st.markdown("##### 2. Background & Skill Matrix")
            experience_level = st.selectbox("Current Experience Level", options=["Beginner", "Intermediate", "Advanced"], index=1)
            
            default_skills = ["Python", "SQL", "Git"]
            available_skills = ["Python", "Java", "C++", "JavaScript", "SQL", "Git", "HTML/CSS", "Data Structures", "Docker", "Machine Learning"]
            current_skills = st.multiselect("Skills You Currently Possess", options=available_skills, default=default_skills)

            interests = st.multiselect(
                "Key Areas of Interest",
                options=["Artificial Intelligence", "Web Development", "Data Engineering", "Cloud Systems", "DevOps", "Agentic Workflows"],
                default=["Artificial Intelligence", "Agentic Workflows"]
            )

        st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0;'>", unsafe_allow_html=True)
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("##### 3. Time Commitment & Pace")
            weekly_hours = st.slider("Available Weekly Learning Hours", min_value=2, max_value=40, value=10, step=1)
            timeline = st.selectbox("Target Goal Timeline", options=["1 Month", "3 Months", "6 Months", "12 Months"], index=1)

        with col4:
            st.markdown("##### 4. Preferences")
            learning_style = st.selectbox(
                "Preferred Learning Format",
                options=["Project-based", "Video Courses", "Interactive Labs", "Reading & Documentation"],
                index=0
            )

        st.markdown("<br/>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("Generate My Intelligence Path", type="primary", use_container_width=True)

        if submit_btn:
            # Update session state profile
            p = st.session_state.profile
            p.name = name
            p.target_role = career_goal
            p.natural_goal = natural_goal
            p.experience_level = experience_level
            p.current_skills = current_skills
            p.interests = interests
            p.weekly_hours = weekly_hours
            p.timeline = timeline
            p.learning_style = learning_style

            # Run Intelligence Engine safely
            engine = st.session_state.intelligence_engine
            output = safe_call(engine.run_pipeline, {}, p)
            st.session_state.engine_output = output
            st.session_state.onboarded = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Main Application Shell after Onboarding
def render_main_application_shell():
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 24px;">
                <div style="background: #4F46E5; color: white; width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem;">P</div>
                <div>
                    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; font-weight: 800; color: #0F172A; line-height: 1;">PathPilot <span style="color: #4F46E5;">AI</span></div>
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 500; margin-top: 2px;">Learning Intelligence</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Navigation Options
        st.markdown("<div style='font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;'>Workspace</div>", unsafe_allow_html=True)
        nav_options = ["Overview", "Next Action", "Learning Roadmap", "Path Health", "AI Assistant"]
        selected_nav = st.radio("Navigation", nav_options, index=nav_options.index(st.session_state.nav_selection))
        st.session_state.nav_selection = selected_nav

        st.markdown("<hr style='border: none; border-top: 1px solid #E2E8F0; margin: 24px 0;'>", unsafe_allow_html=True)

        # Learner Profile Summary Card in Sidebar
        profile = st.session_state.profile
        st.markdown(f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
                <div style="font-size: 0.75rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em;">Active Profile</div>
                <div style="font-weight: 700; color: #0F172A; font-size: 0.95rem; margin-top: 4px;">{profile.name}</div>
                <div style="font-size: 0.82rem; color: #4F46E5; font-weight: 600; margin-top: 2px;">{profile.target_role}</div>
                <div style="font-size: 0.78rem; color: #64748B; margin-top: 8px;">Pace: {profile.weekly_hours} hrs/week ({profile.timeline})</div>
            </div>
        """, unsafe_allow_html=True)

        # Reset / Re-onboard
        if st.button("Restart Journey / Edit Profile", use_container_width=True, type="secondary"):
            st.session_state.onboarded = False
            st.rerun()

    # Top Bar Header Area
    p = st.session_state.profile
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #E2E8F0; padding-bottom: 16px; margin-bottom: 24px;">
            <div>
                <span style="font-size: 0.85rem; color: #64748B; font-weight: 500;">Learning Path / {st.session_state.nav_selection}</span>
                <h2 style="font-size: 1.6rem; margin: 2px 0 0 0;">Welcome back, {p.name.split()[0]}</h2>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="pp-badge pp-badge-emerald">● Path Health: Active</span>
                <span class="pp-badge pp-badge-indigo">{p.target_role}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Dispatch to specific View Modules
    engine_output = st.session_state.engine_output or {}
    engine = st.session_state.intelligence_engine

    if st.session_state.nav_selection == "Overview":
        render_dashboard(p, engine_output, safe_call, engine)
    elif st.session_state.nav_selection == "Next Action":
        render_next_action_page(p, engine_output)
    elif st.session_state.nav_selection == "Learning Roadmap":
        render_roadmap(p, engine_output, safe_call)
    elif st.session_state.nav_selection == "Path Health":
        render_path_health_page(p, engine_output)
    elif st.session_state.nav_selection == "AI Assistant":
        render_ai_assistant_page(p, engine_output)

# Interactive Page: Next Action (Core Feature View)
def render_next_action_page(profile, engine_output):
    st.markdown("### Next Best Action Recommendation")
    st.markdown("PathPilot's decision engine calculates the highest-leverage skill to focus on right now.")

    next_action = engine_output.get("next_best_action", {})
    skill_name = next_action.get("skill", "Core Fundamentals")
    reasoning = next_action.get("reasoning", "Recommended based on your target role requirements and skill gap priorities.")
    confidence = next_action.get("confidence", "High")
    est_hours = next_action.get("estimated_hours", "8-12 hours")
    difficulty = next_action.get("difficulty", "Intermediate")

    # Main Recommendation Hero Box
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FFFFFF 0%, #EEF2FF 100%); border: 1.5px solid #818CF8; border-radius: 16px; padding: 32px; box-shadow: var(--shadow-card); margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                <span class="pp-badge pp-badge-indigo">Highest Priority Recommendation</span>
                <span class="pp-badge pp-badge-emerald">Confidence Score: {confidence}</span>
            </div>
            <div style="font-size: 0.9rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Recommended Skill Focus</div>
            <h1 style="font-size: 2.2rem; color: #0F172A; margin: 4px 0 16px 0;">{skill_name}</h1>
            <p style="font-size: 1.05rem; color: #334155; line-height: 1.6; max-width: 800px;">
                {reasoning}
            </p>
            <div style="display: flex; gap: 24px; margin-top: 24px; padding-top: 20px; border-top: 1px solid #C7D2FE;">
                <div>
                    <div style="font-size: 0.78rem; color: #64748B; font-weight: 600;">ESTIMATED TIME</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A;">{est_hours}</div>
                </div>
                <div>
                    <div style="font-size: 0.78rem; color: #64748B; font-weight: 600;">DIFFICULTY</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A;">{difficulty}</div>
                </div>
                <div>
                    <div style="font-size: 0.78rem; color: #64748B; font-weight: 600;">IMPACT</div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: #059669;">Unlocks Next Milestones</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Adaptive Feedback Loop
    st.markdown("#### Adaptive Feedback")
    st.markdown("How does this recommendation feel for your current pace?")

    f_col1, f_col2, f_col3 = st.columns(3)
    adaptive_engine = st.session_state.adaptive_engine

    with f_col1:
        if st.button("Too Easy — Accelerate", use_container_width=True):
            safe_call(adaptive_engine.record_feedback, None, "too_easy", skill_name)
            st.success("Adjusted model: Increasing pacing and advancing prerequisites.")
    with f_col2:
        if st.button("Appropriate Pace — Keep Going", use_container_width=True, type="primary"):
            safe_call(adaptive_engine.record_feedback, None, "appropriate", skill_name)
            st.info("Pace confirmed. Maintaining optimal trajectory.")
    with f_col3:
        if st.button("Too Difficult — Need Foundations", use_container_width=True):
            safe_call(adaptive_engine.record_feedback, None, "too_difficult", skill_name)
            st.warning("Adjusted model: Inserting foundational micro-lessons.")

# Interactive Page: Path Health
def render_path_health_page(profile, engine_output):
    st.markdown("### Path Health & Diagnostic Analytics")
    st.markdown("Real-time telemetry on learning velocity, risk factors, and timeline stability.")

    health_data = engine_output.get("path_health", {})
    health_score = health_data.get("score", 85)
    status_text = health_data.get("status", "Healthy")
    risks = engine_output.get("risks", [])

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(f"""
            <div class="pp-card" style="text-align: center; padding: 36px 20px;">
                <div class="pp-metric-lbl">Overall Health Index</div>
                <div class="pp-metric-val" style="color: #4F46E5; font-size: 3.5rem; margin: 12px 0;">{health_score}<span style="font-size: 1.5rem; color: #94A3B8;">/100</span></div>
                <span class="pp-badge pp-badge-emerald" style="font-size: 0.85rem;">Status: {status_text}</span>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("<div class="pp-card">", unsafe_allow_html=True)
        st.markdown("##### Detected Risks & Vulnerabilities")
        if risks:
            for r in risks:
                st.markdown(f"""
                    <div style="background: #FEF2F2; border-left: 4px solid #EF4444; padding: 12px 16px; border-radius: 4px; margin-bottom: 10px;">
                        <div style="font-weight: 700; color: #991B1B; font-size: 0.9rem;">{r.get('title', 'Risk Factor Detected')}</div>
                        <div style="font-size: 0.85rem; color: #7F1D1D; margin-top: 2px;">{r.get('description', 'Potential timeline bottleneck based on weekly hour allocation.')}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="background: #ECFDF5; border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 4px;">
                    <div style="font-weight: 700; color: #065F46; font-size: 0.9rem;">No Critical Risks Identified</div>
                    <div style="font-size: 0.85rem; color: #047857; margin-top: 2px;">Your weekly hour commitment aligns well with your target timeline.</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Interactive Page: AI Assistant Workspace
def render_ai_assistant_page(profile, engine_output):
    st.markdown("### Path Intelligence Assistant")
    st.markdown("Ask natural language questions about your roadmap, skill choices, or career trajectory.")

    ai_assistant = st.session_state.ai_assistant

    # Context Bar
    st.markdown(f"""
        <div style="background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 12px; padding: 12px 20px; margin-bottom: 20px; font-size: 0.88rem; color: #3730A3;">
            💡 <strong>Context Active:</strong> Grounded in profile for <strong>{profile.name}</strong> targeting <strong>{profile.target_role}</strong>.
        </div>
    """, unsafe_allow_html=True)

    # Suggested Prompts
    st.markdown("##### Suggested Inquiries")
    p_col1, p_col2, p_col3 = st.columns(3)
    prompt_input = None

    with p_col1:
        if st.button("Why is this my Next Action?", use_container_width=True):
            prompt_input = "Why is this skill recommended as my next best action?"
    with p_col2:
        if st.button("How do I prepare for projects?", use_container_width=True):
            prompt_input = "What foundational concepts should I review before starting the next project?"
    with p_col3:
        if st.button("Optimize for tighter timeline", use_container_width=True):
            prompt_input = "How can I restructure my schedule to achieve this goal faster?"

    user_query = st.text_input("Ask PathPilot Assistant...", value=prompt_input if prompt_input else "", placeholder="e.g., Explain why Docker is required before Kubernetes...")

    if user_query:
        with st.spinner("Analyzing skill graph and profile context..."):
            response = safe_call(
                ai_assistant.answer_query,
                "PathPilot Assistant is analyzing your path details. Ensure your query aligns with your target role.",
                user_query,
                profile,
                engine_output
            )
            st.markdown(f"""
                <div class="pp-card" style="border-left: 4px solid #4F46E5; margin-top: 16px;">
                    <div style="font-weight: 700; color: #4F46E5; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;">Intelligence Explanation</div>
                    <div style="font-size: 0.98rem; color: #1E293B; line-height: 1.6;">{response}</div>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

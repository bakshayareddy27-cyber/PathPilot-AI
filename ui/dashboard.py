import html
import streamlit as st


# ==========================================================
# HELPERS
# ==========================================================

def safe_text(value, fallback="—"):
    if value is None:
        return fallback

    text = str(value).strip()

    if not text:
        return fallback

    return html.escape(text)


def get_risk_text(risk):

    if isinstance(risk, dict):

        return (
            risk.get("description")
            or risk.get("message")
            or risk.get("risk")
            or risk.get("type")
            or "Potential path risk"
        )

    return str(risk)


def get_risk_priority(risk):

    if isinstance(risk, dict):

        value = (
            risk.get("priority")
            or risk.get("severity")
            or risk.get("level")
            or ""
        )

        return str(value).lower()

    return ""


def risk_class(priority):

    if any(word in priority for word in ["critical", "high"]):
        return "high"

    if any(word in priority for word in ["medium", "moderate"]):
        return "medium"

    return "low"


# ==========================================================
# DASHBOARD
# ==========================================================

def render_dashboard(
    profile,
    engine_output,
    ai_assistant,
    adaptive_engine,
    adaptation_state,
):

    engine_output = engine_output or {}

    nba = engine_output.get("next_best_action") or {}
    health = engine_output.get("path_health") or {}
    risks = engine_output.get("risks") or []

    # ======================================================
    # HEADER
    # ======================================================

    st.markdown(
        f"""
        <div class="pp-dashboard-hero">

            <div class="pp-eyebrow">
                YOUR PERSONAL LEARNING INTELLIGENCE
            </div>

            <div class="pp-section-title">
                Welcome back, {safe_text(profile.name)}
            </div>

            <div class="pp-section-subtitle">
                Here's what deserves your attention right now.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ======================================================
    # KPI CARDS
    # ======================================================

    health_score = health.get("health_score", "—")
    health_status = health.get("status", "Unknown")

    weekly_hours = getattr(
        profile,
        "weekly_hours",
        "—",
    )

    current_skills = getattr(
        profile,
        "current_skills",
        [],
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="pp-card">
                <div class="pp-card-label">
                    Path Health
                </div>

                <div class="pp-card-value">
                    {safe_text(health_score)}
                </div>

                <div style="color:#a1a1aa;font-size:0.85rem;">
                    {safe_text(health_status)}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="pp-card">
                <div class="pp-card-label">
                    Current Skills
                </div>

                <div class="pp-card-value">
                    {len(current_skills)}
                </div>

                <div style="color:#a1a1aa;font-size:0.85rem;">
                    Skills recognized
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="pp-card">
                <div class="pp-card-label">
                    Weekly Capacity
                </div>

                <div class="pp-card-value">
                    {safe_text(weekly_hours)}h
                </div>

                <div style="color:#a1a1aa;font-size:0.85rem;">
                    Available learning time
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:

        st.markdown(
            f"""
            <div class="pp-card">
                <div class="pp-card-label">
                    Active Risks
                </div>

                <div class="pp-card-value">
                    {len(risks)}
                </div>

                <div style="color:#a1a1aa;font-size:0.85rem;">
                    Things to monitor
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown("<br>", unsafe_allow_html=True)


    # ======================================================
    # NEXT BEST ACTION
    # ======================================================

    if nba:

        skill = nba.get("skill", "Your next learning step")
        reasons = nba.get("reasons") or []
        est_hours = nba.get("est_hours")
        difficulty = nba.get("difficulty")

        reason_html = ""

        if reasons:

            items = []

            for reason in reasons[:3]:

                items.append(
                    f"""
                    <li style="margin-bottom:0.45rem;">
                        {safe_text(reason)}
                    </li>
                    """
                )

            reason_html = (
                "<ul style='color:#a1a1aa;"
                "padding-left:1.2rem;"
                "margin-top:0.8rem;'>"
                + "".join(items)
                + "</ul>"
            )

        st.markdown(
            f"""
            <div class="pp-nba">

                <div class="pp-nba-label">
                    NEXT BEST ACTION
                </div>

                <div class="pp-nba-title">
                    {safe_text(skill)}
                </div>

                <div style="
                    color:#a1a1aa;
                    line-height:1.7;
                    max-width:850px;
                ">
                    This is the highest-value next step based on
                    your current skills, career direction, and
                    learning readiness.
                </div>

                <div style="
                    display:flex;
                    gap:0.7rem;
                    flex-wrap:wrap;
                    margin-top:1rem;
                ">
                    <span style="
                        padding:0.4rem 0.75rem;
                        border-radius:999px;
                        background:rgba(139,92,246,0.15);
                        color:#c4b5fd;
                        font-size:0.8rem;
                    ">
                        {safe_text(difficulty, "Personalized difficulty")}
                    </span>

                    <span style="
                        padding:0.4rem 0.75rem;
                        border-radius:999px;
                        background:rgba(255,255,255,0.06);
                        color:#d4d4d8;
                        font-size:0.8rem;
                    ">
                        {safe_text(est_hours, "Flexible")} hours
                    </span>
                </div>

                {reason_html}

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "No immediate recommendation is available yet."
        )


    # ======================================================
    # FEEDBACK
    # ======================================================

    if nba and adaptive_engine:

        st.markdown(
            """
            <div class="pp-section-title">
                How does this step feel?
            </div>

            <div class="pp-section-subtitle">
                Your feedback helps PathPilot adapt your learning path.
            </div>
            """,
            unsafe_allow_html=True,
        )

        skill_name = nba.get("skill")

        feedback_col1, feedback_col2, feedback_col3 = st.columns(3)

        feedback_map = [
            (
                feedback_col1,
                "Too easy",
                "too_easy",
                "Move me forward faster",
            ),
            (
                feedback_col2,
                "Feels right",
                "appropriate",
                "Keep this in progress",
            ),
            (
                feedback_col3,
                "Too difficult",
                "too_difficult",
                "Find the foundation first",
            ),
        ]

        for column, label, feedback_value, caption in feedback_map:

            with column:

                if st.button(
                    f"{label}",
                    key=f"feedback_{feedback_value}",
                    use_container_width=True,
                ):

                    try:

                        result = adaptive_engine.apply_feedback(
                            profile,
                            skill_name,
                            feedback_value,
                            adaptation_state,
                        )

                        st.session_state.engine_output = {
                            "next_best_action": (
                                result.get(
                                    "updated_recommendation"
                                )
                            ),
                            "path_health": (
                                result.get(
                                    "updated_path_health"
                                )
                            ),
                            "risks": (
                                result.get(
                                    "updated_risks"
                                )
                                or []
                            ),
                        }

                        st.success(
                            result.get(
                                "adaptation_message",
                                "Your path has been updated.",
                            )
                        )

                        st.rerun()

                    except Exception as error:

                        st.error(
                            f"Couldn't adapt the path: {error}"
                        )

                st.caption(caption)


    st.markdown("<br>", unsafe_allow_html=True)


    # ======================================================
    # PATH HEALTH + RISKS
    # ======================================================

    left, right = st.columns([1, 1.35])

    with left:

        factors = (
            health.get(
                "contributing_factors",
                [],
            )
            or []
        )

        factors_html = ""

        if factors:

            factor_items = "".join(
                f"""
                <div style="
                    padding:0.65rem 0;
                    border-bottom:1px solid #2a2a31;
                    color:#a1a1aa;
                ">
                    {safe_text(factor)}
                </div>
                """
                for factor in factors[:5]
            )

            factors_html = factor_items

        else:

            factors_html = """
            <div style="color:#71717a;">
                No major contributing factors available.
            </div>
            """

        st.markdown(
            f"""
            <div class="pp-health">

                <div class="pp-card-label">
                    PATH HEALTH
                </div>

                <div class="pp-health-score">
                    {safe_text(health_score)}
                </div>

                <div style="
                    color:#c4b5fd;
                    font-weight:650;
                    margin-bottom:1rem;
                ">
                    {safe_text(health_status)}
                </div>

                {factors_html}

            </div>
            """,
            unsafe_allow_html=True,
        )


    with right:

        st.markdown(
            """
            <div class="pp-section-title">
                Risks to watch
            </div>

            <div class="pp-section-subtitle">
                Structured signals that may affect your progress.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if risks:

            for index, risk in enumerate(risks):

                risk_text = get_risk_text(risk)
                priority = get_risk_priority(risk)
                category = risk_class(priority)

                if category == "high":

                    badge_style = """
                    background:rgba(251,113,133,0.12);
                    color:#fda4af;
                    border:1px solid rgba(251,113,133,0.22);
                    """

                    label = "HIGH PRIORITY"

                elif category == "medium":

                    badge_style = """
                    background:rgba(251,191,36,0.10);
                    color:#fcd34d;
                    border:1px solid rgba(251,191,36,0.2);
                    """

                    label = "WATCH"

                else:

                    badge_style = """
                    background:rgba(255,255,255,0.05);
                    color:#a1a1aa;
                    border:1px solid #2a2a31;
                    """

                    label = "MONITOR"

                st.markdown(
                    f"""
                    <div class="pp-card"
                        style="margin-bottom:0.8rem;">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            align-items:center;
                            gap:1rem;
                        ">

                            <div style="
                                color:#f4f4f5;
                                font-weight:600;
                            ">
                                {safe_text(risk_text)}
                            </div>

                            <span style="
                                {badge_style}
                                padding:0.28rem 0.55rem;
                                border-radius:999px;
                                font-size:0.68rem;
                                font-weight:800;
                                white-space:nowrap;
                            ">
                                {label}
                            </span>

                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.markdown(
                """
                <div class="pp-card">
                    <div style="
                        color:#34d399;
                        font-weight:700;
                    ">
                        ✓ No major risks detected
                    </div>

                    <div style="
                        color:#a1a1aa;
                        margin-top:0.5rem;
                    ">
                        Your current path does not have any
                        significant warning signals.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


    st.markdown("<br><br>", unsafe_allow_html=True)


    # ======================================================
    # AI ASSISTANT
    # ======================================================

    st.markdown(
        """
        <div class="pp-ai">

            <div class="pp-ai-header">

                <div class="pp-ai-icon">
                    ✦
                </div>

                <div>
                    <div style="
                        font-weight:750;
                        font-size:1.05rem;
                    ">
                        PathPilot Intelligence
                    </div>

                    <div style="
                        color:#a1a1aa;
                        font-size:0.82rem;
                    ">
                        Ask about your learning path
                    </div>
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    question = st.text_input(
        "Ask PathPilot",
        placeholder=(
            "Why is this my next best action?"
        ),
        label_visibility="collapsed",
        key="ai_question",
    )

    chip_col1, chip_col2, chip_col3 = st.columns(3)

    suggestions = [
        (
            chip_col1,
            "Why this skill?",
            "Why is this my next best skill?",
        ),
        (
            chip_col2,
            "Check my path health",
            "What does my path health mean?",
        ),
        (
            chip_col3,
            "What is blocking me?",
            "Are there any prerequisites or blockers?",
        ),
    ]

    selected_question = question

    for column, label, prompt in suggestions:

        with column:

            if st.button(
                label,
                key=f"chip_{label}",
                use_container_width=True,
            ):
                selected_question = prompt

    if selected_question:

        if st.button(
            "Ask PathPilot →",
            type="primary",
        ):

            try:

                answer = ai_assistant.answer_path_question(
                    profile,
                    engine_output,
                    selected_question,
                )

                st.session_state.ai_answer = answer

            except Exception as error:

                st.error(
                    f"Assistant unavailable: {error}"
                )

    if st.session_state.get("ai_answer"):

        answer = safe_text(
            st.session_state.ai_answer
        ).replace("\n", "<br>")

        st.markdown(
            f"""
            <div class="pp-answer">
                {answer}
            </div>
            """,
            unsafe_allow_html=True,
        )

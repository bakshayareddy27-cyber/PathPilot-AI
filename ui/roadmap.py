import html
import streamlit as st


# ==========================================================
# HELPERS
# ==========================================================

def safe_text(value, fallback="—"):

    if value is None:
        return fallback

    value = str(value).strip()

    if not value:
        return fallback

    return html.escape(value)


def difficulty_label(value):

    if value is None:
        return "Personalized"

    value = str(value)

    mapping = {
        "1": "Beginner",
        "2": "Foundation",
        "3": "Intermediate",
        "4": "Advanced",
        "5": "Expert",
    }

    return mapping.get(
        value,
        value.capitalize(),
    )


# ==========================================================
# ROADMAP
# ==========================================================

def render_roadmap(profile, engine_output):

    engine_output = engine_output or {}

    nba = engine_output.get(
        "next_best_action"
    ) or {}

    health = engine_output.get(
        "path_health"
    ) or {}

    current_skills = getattr(
        profile,
        "current_skills",
        [],
    ) or []

    # ======================================================
    # HEADER
    # ======================================================

    st.markdown(
        f"""
        <div style="margin-bottom:2rem;">

            <div class="pp-eyebrow">
                PERSONALIZED ROADMAP
            </div>

            <div class="pp-section-title">
                Your path toward {safe_text(profile.career_goal)}
            </div>

            <div class="pp-section-subtitle">
                A structured view of what you've built,
                where you are now, and what comes next.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ======================================================
    # ROADMAP OVERVIEW
    # ======================================================

    timeline = getattr(
        profile,
        "timeline_weeks",
        None,
    )

    weekly_hours = getattr(
        profile,
        "weekly_hours",
        None,
    )

    health_score = health.get(
        "health_score",
        "—",
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="pp-card">
                <div class="pp-card-label">
                    Timeline
                </div>

                <div class="pp-card-value">
                    {safe_text(timeline)}
                </div>

                <div style="color:#a1a1aa;">
                    weeks available
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
                    Weekly Capacity
                </div>

                <div class="pp-card-value">
                    {safe_text(weekly_hours)}h
                </div>

                <div style="color:#a1a1aa;">
                    learning time
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
                    Path Health
                </div>

                <div class="pp-card-value">
                    {safe_text(health_score)}
                </div>

                <div style="color:#a1a1aa;">
                    current readiness
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown("<br><br>", unsafe_allow_html=True)


    # ======================================================
    # ROADMAP TIMELINE
    # ======================================================

    st.markdown(
        """
        <div class="pp-section-title">
            Learning journey
        </div>

        <div class="pp-section-subtitle">
            Your roadmap is organized around your current
            capability and highest-value next step.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # ======================================================
    # STEP 1 — CURRENT FOUNDATION
    # ======================================================

    if current_skills:

        skills_html = "".join(
            f"""
            <span style="
                display:inline-block;
                margin:0.25rem;
                padding:0.4rem 0.7rem;
                border-radius:999px;
                background:rgba(52,211,153,0.10);
                border:1px solid rgba(52,211,153,0.2);
                color:#86efac;
                font-size:0.82rem;
            ">
                ✓ {safe_text(skill)}
            </span>
            """
            for skill in current_skills
        )

        current_text = skills_html

    else:

        current_text = """
        <div style="color:#71717a;">
            No skills have been added yet.
            PathPilot will build recommendations from your profile.
        </div>
        """

    st.markdown(
        f"""
        <div class="pp-roadmap-step completed">

            <div style="
                color:#34d399;
                font-size:0.75rem;
                font-weight:800;
                letter-spacing:0.1em;
            ">
                STEP 01 · CURRENT FOUNDATION
            </div>

            <div style="
                font-size:1.25rem;
                font-weight:700;
                margin:0.5rem 0 0.9rem;
            ">
                What you already know
            </div>

            <div>
                {current_text}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ======================================================
    # STEP 2 — NEXT BEST ACTION
    # ======================================================

    if nba:

        skill = nba.get(
            "skill",
            "Next learning step",
        )

        reasons = nba.get(
            "reasons",
            [],
        ) or []

        est_hours = nba.get("est_hours")
        difficulty = difficulty_label(
            nba.get("difficulty")
        )

        reasons_html = ""

        if reasons:

            reasons_html = "".join(
                f"""
                <div style="
                    margin-top:0.5rem;
                    color:#a1a1aa;
                ">
                    • {safe_text(reason)}
                </div>
                """
                for reason in reasons[:4]
            )

        else:

            reasons_html = """
            <div style="
                margin-top:0.5rem;
                color:#a1a1aa;
            ">
                Selected based on your personalized
                career direction and current readiness.
            </div>
            """

        st.markdown(
            f"""
            <div class="pp-roadmap-step active">

                <div style="
                    color:#c4b5fd;
                    font-size:0.75rem;
                    font-weight:800;
                    letter-spacing:0.1em;
                ">
                    STEP 02 · CURRENT FOCUS
                </div>

                <div style="
                    font-size:1.4rem;
                    font-weight:750;
                    margin:0.5rem 0;
                ">
                    {safe_text(skill)}
                </div>

                <div style="
                    display:flex;
                    gap:0.6rem;
                    flex-wrap:wrap;
                    margin:0.7rem 0;
                ">

                    <span style="
                        padding:0.35rem 0.65rem;
                        border-radius:999px;
                        background:rgba(139,92,246,0.14);
                        color:#c4b5fd;
                        font-size:0.78rem;
                    ">
                        {safe_text(difficulty)}
                    </span>

                    <span style="
                        padding:0.35rem 0.65rem;
                        border-radius:999px;
                        background:rgba(255,255,255,0.06);
                        color:#d4d4d8;
                        font-size:0.78rem;
                    ">
                        {safe_text(est_hours, "Flexible")} hours
                    </span>

                </div>

                <div style="margin-top:1rem;">
                    {reasons_html}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="pp-roadmap-step active">

                <div style="
                    color:#c4b5fd;
                    font-size:0.75rem;
                    font-weight:800;
                ">
                    CURRENT FOCUS
                </div>

                <div style="
                    font-size:1.2rem;
                    font-weight:700;
                    margin-top:0.5rem;
                ">
                    Your next step is being evaluated
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ======================================================
    # STEP 3 — FUTURE PROGRESSION
    # ======================================================

    st.markdown(
        f"""
        <div class="pp-roadmap-step">

            <div style="
                color:#71717a;
                font-size:0.75rem;
                font-weight:800;
                letter-spacing:0.1em;
            ">
                STEP 03 · FUTURE PROGRESSION
            </div>

            <div style="
                font-size:1.25rem;
                font-weight:700;
                margin:0.5rem 0;
            ">
                Build toward {safe_text(profile.career_goal)}
            </div>

            <div style="
                color:#a1a1aa;
                line-height:1.7;
            ">
                Future recommendations will be recalculated as you
                progress. PathPilot adapts your next best action
                instead of locking you into a rigid static course list.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ======================================================
    # PATH HEALTH
    # ======================================================

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="pp-section-title">
            Roadmap health
        </div>

        <div class="pp-section-subtitle">
            Signals influencing how sustainable your current path is.
        </div>
        """,
        unsafe_allow_html=True,
    )

    factors = health.get(
        "contributing_factors",
        [],
    ) or []

    status = health.get(
        "status",
        "Unknown",
    )

    score = health.get(
        "health_score",
        "—",
    )

    left, right = st.columns([0.75, 1.25])

    with left:

        st.markdown(
            f"""
            <div class="pp-health">

                <div class="pp-card-label">
                    CURRENT STATUS
                </div>

                <div class="pp-health-score">
                    {safe_text(score)}
                </div>

                <div style="
                    color:#c4b5fd;
                    font-weight:700;
                ">
                    {safe_text(status)}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:

        if factors:

            for factor in factors:

                st.markdown(
                    f"""
                    <div class="pp-card"
                        style="margin-bottom:0.7rem;">

                        <div style="
                            color:#d4d4d8;
                            font-size:0.92rem;
                        ">
                            {safe_text(factor)}
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
                        color:#a1a1aa;
                    ">
                        No additional path health factors are
                        currently available.

                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


    # ======================================================
    # ACTION
    # ======================================================

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(
        "← Back to Dashboard",
    ):
        st.session_state.page = "Dashboard"
        st.rerun()

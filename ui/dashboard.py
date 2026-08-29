"""
PathPilot AI — Overview Dashboard

Presentation layer only.
Uses the existing IntelligenceEngine output without changing
backend contracts or calculations.
"""

import html
import streamlit as st

try:
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True

except Exception:

    PLOTLY_AVAILABLE = False


# ==============================================================
# MAIN DASHBOARD
# ==============================================================

def render_dashboard(
    profile,
    engine_output,
    safe_call,
    engine,
):

    st.markdown(
        """
        <div class="pp-eyebrow">
            YOUR LEARNING INTELLIGENCE
        </div>

        <h2 class="pp-section-title">
            Overview
        </h2>

        <p class="pp-section-description">
            A clear snapshot of your current learning position.
        </p>
        """,
        unsafe_allow_html=True,
    )

    readiness = engine_output.get(
        "readiness"
    )

    health = (
        engine_output.get("path_health")
        or {}
    )

    skill_gap = engine_output.get(
        "skill_gap"
    )

    risks = (
        engine_output.get("risks")
        or []
    )

    readiness_score = _extract_score(
        readiness
    )

    health_score = health.get(
        "health_score",
        "—",
    )

    health_status = health.get(
        "status",
        "Unknown",
    )

    missing_skills = (
        _extract_missing_skills(
            skill_gap
        )
    )

    _render_metric_cards(
        readiness_score,
        health_score,
        health_status,
        len(missing_skills),
        len(risks),
    )

    st.write("")

    left, right = st.columns(2)

    # ==========================================================
    # SKILLS COVERAGE
    # ==========================================================

    with left:

        st.markdown(
            """
            <div class="pp-card">

                <div class="pp-eyebrow">
                    SKILLS COVERAGE
                </div>
            """,
            unsafe_allow_html=True,
        )

        current_skills = list(
            getattr(
                profile,
                "current_skills",
                [],
            )
            or []
        )

        _render_skills_chart(
            current_skills,
            missing_skills,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    # ==========================================================
    # PRIORITIZED SKILL GAPS
    # ==========================================================

    with right:

        st.markdown(
            """
            <div class="pp-card">

                <div class="pp-eyebrow">
                    PRIORITIZED SKILL GAPS
                </div>
            """,
            unsafe_allow_html=True,
        )

        _render_skill_gap_list(
            missing_skills
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    # ==========================================================
    # QUICK SNAPSHOT
    # ==========================================================

    st.write("")

    st.markdown(
        """
        <div class="pp-card">

            <div class="pp-eyebrow">
                QUICK SNAPSHOT
            </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        career_goal = html.escape(
            str(
                getattr(
                    profile,
                    "career_goal",
                    "N/A",
                )
            )
        )

        weekly_hours = html.escape(
            str(
                getattr(
                    profile,
                    "weekly_hours",
                    "N/A",
                )
            )
        )

        st.markdown(
            f"""
            <div class="pp-dashboard-list-item">

                <div>
                    <div class="pp-metric-label">
                        Career Goal
                    </div>

                    <div class="pp-dashboard-skill">
                        {career_goal}
                    </div>
                </div>

            </div>

            <div class="pp-dashboard-list-item">

                <div>
                    <div class="pp-metric-label">
                        Weekly Learning
                    </div>

                    <div class="pp-dashboard-skill">
                        {weekly_hours} hours / week
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        timeline = html.escape(
            str(
                getattr(
                    profile,
                    "timeline_weeks",
                    "N/A",
                )
            )
        )

        skills = getattr(
            profile,
            "current_skills",
            [],
        ) or []

        skills_text = (
            ", ".join(
                str(skill)
                for skill in skills
            )
            if skills
            else "None yet"
        )

        skills_text = html.escape(
            skills_text
        )

        st.markdown(
            f"""
            <div class="pp-dashboard-list-item">

                <div>
                    <div class="pp-metric-label">
                        Target Timeline
                    </div>

                    <div class="pp-dashboard-skill">
                        {timeline} weeks
                    </div>
                </div>

            </div>

            <div class="pp-dashboard-list-item">

                <div>
                    <div class="pp-metric-label">
                        Current Skills
                    </div>

                    <div class="pp-dashboard-skill">
                        {skills_text}
                    </div>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ==============================================================
# METRIC CARDS
# ==============================================================

def _render_metric_cards(
    readiness_score,
    health_score,
    health_status,
    missing_count,
    risk_count,
):

    readiness_good = (
        isinstance(
            readiness_score,
            (int, float),
        )
        and readiness_score >= 60
    )

    health_class = {
        "Healthy": "trend-good",
        "At Risk": "trend-warn",
        "Critical": "trend-bad",
    }.get(
        health_status,
        "trend-neutral",
    )

    cards = [

        (
            "Readiness",
            (
                f"{readiness_score}%"
                if readiness_score is not None
                else "—"
            ),
            (
                "Strong foundation"
                if readiness_good
                else "Still building"
            ),
            (
                "trend-good"
                if readiness_good
                else "trend-neutral"
            ),
        ),

        (
            "Path Health",
            str(health_score),
            health_status,
            health_class,
        ),

        (
            "Missing Skills",
            str(missing_count),
            "Skills remaining",
            "trend-neutral",
        ),

        (
            "Active Risks",
            str(risk_count),
            (
                "Needs attention"
                if risk_count > 0
                else "All clear"
            ),
            (
                "trend-bad"
                if risk_count > 0
                else "trend-good"
            ),
        ),
    ]

    columns = st.columns(4)

    for column, card in zip(
        columns,
        cards,
    ):

        label, value, description, trend_class = card

        with column:

            st.markdown(
                f"""
                <div class="pp-metric-card">

                    <div class="pp-metric-label">
                        {html.escape(str(label))}
                    </div>

                    <div class="pp-metric-value">
                        {html.escape(str(value))}
                    </div>

                    <div class="pp-metric-desc {trend_class}">
                        {html.escape(str(description))}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================
# READINESS EXTRACTION
# ==============================================================

def _extract_score(readiness):

    if readiness is None:
        return None

    if isinstance(
        readiness,
        dict,
    ):

        return (
            readiness.get("score")
            or readiness.get("readiness_score")
        )

    if isinstance(
        readiness,
        (int, float),
    ):

        return readiness

    return None


# ==============================================================
# SKILL GAP EXTRACTION
# ==============================================================

def _extract_missing_skills(skill_gap):

    if not skill_gap:
        return []

    if isinstance(
        skill_gap,
        dict,
    ):

        for key in [
            "missing_skills",
            "missing",
            "gaps",
        ]:

            if (
                key in skill_gap
                and isinstance(
                    skill_gap[key],
                    list,
                )
            ):

                return skill_gap[key]

        return []

    if isinstance(
        skill_gap,
        list,
    ):

        return skill_gap

    return []


# ==============================================================
# SKILLS CHART
# ==============================================================

def _render_skills_chart(
    current_skills,
    missing_skills,
):

    possessed_count = len(
        current_skills
    )

    missing_count = len(
        missing_skills
    )

    if (
        possessed_count == 0
        and missing_count == 0
    ):

        st.markdown(
            """
            <p style="
                color:var(--text-faint);
                font-size:0.85rem;
            ">
                No skill data available yet.
            </p>
            """,
            unsafe_allow_html=True,
        )

        return

    if PLOTLY_AVAILABLE:

        figure = go.Figure()

        figure.add_trace(
            go.Bar(
                x=[
                    "Current Skills",
                    "Skills to Build",
                ],

                y=[
                    possessed_count,
                    missing_count,
                ],

                marker_color=[
                    "#6d72ff",
                    "#2a3448",
                ],

                marker_line_width=0,

                width=0.5,
            )
        )

        figure.update_layout(
            height=260,

            margin=dict(
                l=10,
                r=10,
                t=15,
                b=10,
            ),

            paper_bgcolor=
                "rgba(0,0,0,0)",

            plot_bgcolor=
                "rgba(0,0,0,0)",

            font_color="#7f8a9e",

            font_family="Inter",

            showlegend=False,

            yaxis=dict(
                gridcolor=
                    "rgba(255,255,255,0.05)",

                zeroline=False,

                title="Skill Count",
            ),

            xaxis=dict(
                showgrid=False,
            ),
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
        )

    else:

        st.bar_chart(
            {
                "Current Skills":
                    possessed_count,

                "Skills to Build":
                    missing_count,
            }
        )


# ==============================================================
# SKILL GAP LIST
# ==============================================================

def _render_skill_gap_list(
    missing_skills,
):

    if not missing_skills:

        st.markdown(
            """
            <div style="
                color:var(--success);
                font-size:0.87rem;
                padding:0.8rem 0;
            ">
                ✓ No missing skills detected.
                You're well aligned with your goal.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    for item in missing_skills[:8]:

        if isinstance(
            item,
            dict,
        ):

            name = (
                item.get("skill")
                or item.get("name")
                or "Unknown Skill"
            )

            priority = item.get(
                "priority",
                "",
            )

        else:

            name = str(item)

            priority = ""

        priority_html = ""

        if priority != "":

            priority_html = f"""
            <span class="pp-dashboard-priority">
                Priority {html.escape(str(priority))}
            </span>
            """

        st.markdown(
            f"""
            <div class="pp-dashboard-list-item">

                <div class="pp-dashboard-skill">
                    {html.escape(str(name))}
                </div>

                {priority_html}

            </div>
            """,
            unsafe_allow_html=True,
        )

    if len(missing_skills) > 8:

        remaining = (
            len(missing_skills) - 8
        )

        st.markdown(
            f"""
            <p style="
                color:var(--text-faint);
                font-size:0.78rem;
                margin-top:0.8rem;
            ">
                + {remaining} more skill gaps
            </p>
            """,
            unsafe_allow_html=True,
        )

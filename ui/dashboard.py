"""
PathPilot AI — Overview Dashboard
UI rendering only.
Existing backend output contract is preserved.
"""

import streamlit as st

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


# ======================================================================
# MAIN DASHBOARD
# ======================================================================

def render_dashboard(
    profile,
    engine_output,
    safe_call,
    engine,
):

    st.markdown(
        """
        <div class="pp-eyebrow">
            Learning Intelligence
        </div>

        <h2 class="pp-section-title">
            Your learning overview
        </h2>

        <p class="pp-section-description">
            A clear snapshot of your readiness, skill coverage
            and learning risks.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    readiness = engine_output.get("readiness")

    health = (
        engine_output.get("path_health")
        or {}
    )

    skill_gap = engine_output.get("skill_gap")

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

    missing_skills = _extract_missing_skills(
        skill_gap
    )

    _render_metrics(
        readiness_score,
        health_score,
        health_status,
        len(missing_skills),
        len(risks),
    )

    st.write("")
    st.write("")

    left, right = st.columns([1.05, 0.95])

    with left:

        st.markdown(
            """
            <div class="pp-card">
                <div class="pp-eyebrow">
                    Skills Coverage
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

    with right:

        st.markdown(
            """
            <div class="pp-card">
                <div class="pp-eyebrow">
                    Priority Gaps
                </div>

                <div style="
                    font-family:var(--font-display);
                    font-size:1.05rem;
                    font-weight:700;
                    margin-bottom:1rem;
                ">
                    Skills worth focusing on
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

    st.write("")
    st.write("")

    _render_snapshot(profile)


# ======================================================================
# METRICS
# ======================================================================

def _render_metrics(
    readiness_score,
    health_score,
    health_status,
    missing_count,
    risk_count,
):

    readiness_display = (
        f"{readiness_score}%"
        if readiness_score is not None
        else "—"
    )

    readiness_description = (
        "Strong foundation"
        if isinstance(readiness_score, (int, float))
        and readiness_score >= 70
        else "Still building"
    )

    health_class = {
        "Healthy": "trend-good",
        "At Risk": "trend-warning",
        "Critical": "trend-danger",
    }.get(
        health_status,
        "",
    )

    cards = [

        (
            "Readiness",
            readiness_display,
            readiness_description,
            "trend-good"
            if readiness_score
            and readiness_score >= 70
            else "",
        ),

        (
            "Path Health",
            health_score,
            health_status,
            health_class,
        ),

        (
            "Skill Gaps",
            missing_count,
            "Skills remaining",
            "",
        ),

        (
            "Active Risks",
            risk_count,
            (
                "Needs attention"
                if risk_count
                else "No active risks"
            ),
            (
                "trend-danger"
                if risk_count
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
                        {label}
                    </div>

                    <div class="pp-metric-value">
                        {value}
                    </div>

                    <div class="
                        pp-metric-description
                        {trend_class}
                    ">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ======================================================================
# DATA EXTRACTION
# ======================================================================

def _extract_score(readiness):

    if readiness is None:
        return None

    if isinstance(readiness, dict):

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


def _extract_missing_skills(skill_gap):

    if not skill_gap:
        return []

    if isinstance(skill_gap, dict):

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

    if isinstance(skill_gap, list):
        return skill_gap

    return []


# ======================================================================
# SKILLS CHART
# ======================================================================

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
            <p class="pp-section-description">
                No skill data is available yet.
            </p>
            """,
            unsafe_allow_html=True,
        )

        return

    if PLOTLY_AVAILABLE:

        fig = go.Figure()

        fig.add_trace(
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
                    "#7C6CFF",
                    "#303747",
                ],

                marker_line_width=0,

                width=0.55,
            )
        )

        fig.update_layout(
            height=280,

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

            font_color="#7F8898",

            font_family="Inter",

            showlegend=False,

            yaxis=dict(
                title="",
                gridcolor=
                    "rgba(255,255,255,0.05)",
                zeroline=False,
            ),

            xaxis=dict(
                showgrid=False,
            ),
        )

        st.plotly_chart(
            fig,
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


# ======================================================================
# SKILL GAP LIST
# ======================================================================

def _render_skill_gap_list(
    missing_skills
):

    if not missing_skills:

        st.markdown(
            """
            <div style="
                color:var(--success);
                font-size:0.88rem;
                padding:0.5rem 0;
            ">
                ✓ Your current skills are well aligned with your goal.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    for index, item in enumerate(
        missing_skills[:8],
        start=1,
    ):

        if isinstance(item, dict):

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

        priority_text = (
            f"Priority {priority}"
            if priority != ""
            else "Recommended"
        )

        st.markdown(
            f"""
            <div class="pp-reason">

                <span style="
                    min-width:22px;
                    color:var(--primary);
                    font-family:var(--font-mono);
                    font-size:0.72rem;
                ">
                    {index:02d}
                </span>

                <span>

                    <b style="
                        color:var(--text-primary);
                    ">
                        {name}
                    </b>

                    <span style="
                        color:var(--text-faint);
                        font-size:0.75rem;
                    ">
                        · {priority_text}
                    </span>

                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )

    if len(missing_skills) > 8:

        st.markdown(
            f"""
            <p style="
                color:var(--text-faint);
                font-size:0.78rem;
                margin-top:0.8rem;
            ">
                + {len(missing_skills) - 8}
                additional skills identified
            </p>
            """,
            unsafe_allow_html=True,
        )


# ======================================================================
# SNAPSHOT
# ======================================================================

def _render_snapshot(profile):

    st.markdown(
        """
        <div class="pp-card">

            <div class="pp-eyebrow">
                Learning Profile
            </div>

            <div style="
                font-family:var(--font-display);
                font-size:1.1rem;
                font-weight:700;
                margin-bottom:1rem;
            ">
                Your current setup
            </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    current_skills = (
        ", ".join(
            getattr(
                profile,
                "current_skills",
                [],
            )
            or []
        )
        or "None yet"
    )

    with col1:

        st.markdown(
            f"""
            <div class="pp-metric-label">
                Career Goal
            </div>

            <div style="
                margin-top:0.45rem;
                color:var(--text-secondary);
                font-size:0.88rem;
            ">
                {getattr(profile, "career_goal", "N/A")}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            f"""
            <div class="pp-metric-label">
                Weekly Commitment
            </div>

            <div style="
                margin-top:0.45rem;
                color:var(--text-secondary);
                font-size:0.88rem;
            ">
                {getattr(profile, "weekly_hours", "N/A")}
                hours / week
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            f"""
            <div class="pp-metric-label">
                Timeline
            </div>

            <div style="
                margin-top:0.45rem;
                color:var(--text-secondary);
                font-size:0.88rem;
            ">
                {getattr(profile, "timeline_weeks", "N/A")}
                weeks
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style="
            margin-top:1.5rem;
            padding-top:1rem;
            border-top:1px solid var(--border);
        ">

            <div class="pp-metric-label">
                Current Skills
            </div>

            <div style="
                margin-top:0.5rem;
                color:var(--text-muted);
                font-size:0.84rem;
                line-height:1.7;
            ">
                {current_skills}
            </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

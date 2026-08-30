import html
from textwrap import dedent

import streamlit as st


def esc(value):
    return html.escape(
        str(value if value is not None else "—")
    )


def render_html(content):
    st.markdown(
        dedent(content).strip(),
        unsafe_allow_html=True,
    )


def get_value(data, *keys, default=None):

    if not isinstance(data, dict):
        return default

    for key in keys:

        if key in data and data[key] is not None:
            return data[key]

    return default


def normalize_score(value, default=0):

    if isinstance(value, dict):

        value = (
            value.get("score")
            or value.get("readiness_score")
            or value.get("value")
            or default
        )

    try:
        value = float(value)

        if value <= 1:
            value *= 100

        return max(0, min(int(value), 100))

    except Exception:
        return default


def render_dashboard(profile, output):

    # ========================================================
    # EXTRACT DATA
    # ========================================================

    readiness_data = output.get("readiness", {})

    readiness = normalize_score(
        readiness_data,
        default=0
    )

    skill_gap = output.get("skill_gap") or {}

    roadmap = output.get("roadmap") or []

    health = output.get("path_health") or {}

    next_action = output.get("next_best_action") or {}

    health_score = normalize_score(
        get_value(
            health,
            "health_score",
            "score",
            default=0
        ),
        default=0
    )

    health_status = get_value(
        health,
        "status",
        default="Analyzing"
    )

    # ========================================================
    # HERO
    # ========================================================

    render_html(f"""
    <div style="margin-bottom:28px;">

        <div style="
            display:inline-flex;
            padding:6px 11px;
            border-radius:999px;
            background:#F0F0FF;
            color:#5B5CE2;
            font-size:10px;
            font-weight:800;
            letter-spacing:.1em;
        ">
            ✦ YOUR LEARNING WORKSPACE
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(32px,4vw,48px);
            font-weight:800;
            letter-spacing:-.05em;
            color:#172033;
            margin-top:12px;
        ">
            Good to see you, {esc(getattr(profile, "name", "Learner"))}.
        </div>

        <div style="
            color:#6B7280;
            font-size:15px;
            margin-top:9px;
        ">
            Here's what PathPilot currently understands about your learning journey.
        </div>

    </div>
    """)

    # ========================================================
    # TOP METRICS
    # ========================================================

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:

        st.metric(
            "Career readiness",
            f"{readiness}%",
            "Personalized analysis",
        )

    with metric2:

        st.metric(
            "Path health",
            f"{health_score}%",
            str(health_status),
        )

    with metric3:

        st.metric(
            "Roadmap milestones",
            len(roadmap),
            "Structured learning plan",
        )

    skills = getattr(profile, "current_skills", []) or []

    with metric4:

        st.metric(
            "Current skills",
            len(skills),
            "Skills in your profile",
        )

    st.write("")

    # ========================================================
    # NEXT BEST ACTION
    # ========================================================

    skill = get_value(
        next_action,
        "skill",
        "title",
        "action",
        default="Generate your next learning action"
    )

    difficulty = get_value(
        next_action,
        "difficulty",
        default="Personalized"
    )

    effort = get_value(
        next_action,
        "est_hours",
        "hours",
        default="—"
    )

    left, right = st.columns([1.45, 0.55])

    with left:

        render_html(f"""
        <div style="
            background:linear-gradient(135deg,#5556D8,#7776EB);
            border-radius:24px;
            padding:30px;
            color:white;
            min-height:210px;
            box-shadow:0 18px 45px rgba(85,86,216,.20);
        ">

            <div style="
                font-size:10px;
                font-weight:800;
                letter-spacing:.12em;
                opacity:.75;
            ">
                NEXT BEST ACTION
            </div>

            <div style="
                font-family:Manrope,sans-serif;
                font-size:clamp(27px,3vw,38px);
                font-weight:800;
                letter-spacing:-.04em;
                margin-top:10px;
                max-width:700px;
            ">
                {esc(skill)}
            </div>

            <div style="
                display:flex;
                gap:20px;
                margin-top:22px;
                flex-wrap:wrap;
            ">

                <div>
                    <div style="font-size:9px;opacity:.65;">
                        DIFFICULTY
                    </div>
                    <div style="font-weight:700;margin-top:4px;">
                        {esc(difficulty)}
                    </div>
                </div>

                <div>
                    <div style="font-size:9px;opacity:.65;">
                        ESTIMATED EFFORT
                    </div>
                    <div style="font-weight:700;margin-top:4px;">
                        {esc(effort)} hrs
                    </div>
                </div>

            </div>

        </div>
        """)

    with right:

        with st.container(border=True):

            st.caption("YOUR DESTINATION")

            st.markdown(
                f"### {esc(getattr(profile, 'career_goal', 'Learning Goal'))}"
            )

            st.write("")

            st.caption("WEEKLY COMMITMENT")

            st.markdown(
                f"### {esc(getattr(profile, 'weekly_hours', '—'))} hrs"
            )

            st.caption("available for learning")

    st.write("")

    # ========================================================
    # SKILLS + INSIGHTS
    # ========================================================

    left, right = st.columns([1.1, 0.9])

    with left:

        with st.container(border=True):

            st.markdown("### Your skill profile")

            st.caption(
                "Skills currently recognized in your learner profile."
            )

            st.write("")

            skills = getattr(
                profile,
                "current_skills",
                []
            ) or []

            if skills:

                tags = ""

                for skill_name in skills:

                    tags += (
                        f"<span style='display:inline-block;"
                        f"padding:8px 12px;"
                        f"margin:4px;"
                        f"background:#F1F2FF;"
                        f"border:1px solid #E0E1FF;"
                        f"border-radius:999px;"
                        f"color:#5556D8;"
                        f"font-size:13px;"
                        f"font-weight:700;'>"
                        f"{esc(skill_name)}</span>"
                    )

                st.markdown(
                    tags,
                    unsafe_allow_html=True,
                )

            else:

                st.info(
                    "Add your skills during profiling to make "
                    "recommendations more personalized."
                )

    with right:

        with st.container(border=True):

            st.markdown("### Learning preferences")

            st.caption("How your path is being personalized.")

            st.write("")

            col1, col2 = st.columns(2)

            with col1:

                st.caption("STYLE")

                st.markdown(
                    f"**{str(getattr(profile, 'preferred_learning_style', 'Mixed')).title()}**"
                )

            with col2:

                st.caption("TIMELINE")

                st.markdown(
                    f"**{getattr(profile, 'timeline_weeks', '—')} weeks**"
                )

            interests = getattr(
                profile,
                "interests",
                []
            ) or []

            if interests:

                st.write("")

                st.caption("INTEREST AREAS")

                st.write(", ".join(
                    [str(item) for item in interests]
                ))

    st.write("")

    # ========================================================
    # INTELLIGENCE INSIGHTS
    # ========================================================

    st.markdown("### PathPilot intelligence")

    insight1, insight2 = st.columns(2)

    with insight1:

        with st.container(border=True):

            st.markdown("#### Skill gap analysis")

            if isinstance(skill_gap, dict):

                missing = (
                    skill_gap.get("missing_skills")
                    or skill_gap.get("skill_gaps")
                    or skill_gap.get("gaps")
                    or []
                )

                if missing:

                    if not isinstance(missing, list):
                        missing = [missing]

                    for item in missing[:5]:

                        if isinstance(item, dict):

                            label = (
                                item.get("skill")
                                or item.get("name")
                                or str(item)
                            )

                        else:
                            label = str(item)

                        st.markdown(f"• {esc(label)}")

                else:

                    st.write(
                        "PathPilot has analyzed your profile and will "
                        "identify the highest-priority skills as your "
                        "roadmap develops."
                    )

            else:

                st.write(
                    "Skill gap intelligence is based on your career "
                    "goal and current profile."
                )

    with insight2:

        with st.container(border=True):

            st.markdown("#### What happens next?")

            st.write(
                "Your learning path is designed as a sequence—not just "
                "a list of courses."
            )

            st.markdown(
                """
                **PathPilot will help you:**

                - Build prerequisite knowledge
                - Close important skill gaps
                - Complete practical milestones
                - Adapt recommendations using feedback
                """
            )

    st.write("")

    # ========================================================
    # QUICK CTA
    # ========================================================

    with st.container(border=True):

        st.markdown("### Ready to continue?")

        st.caption(
            "Explore your personalized roadmap to see the recommended learning sequence."
        )

        if st.button(
            "View My Learning Roadmap  →",
            type="primary",
        ):

            st.session_state.nav_section = "Learning Roadmap"

            st.rerun()

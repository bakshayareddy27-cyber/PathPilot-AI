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


def normalize_roadmap(roadmap):

    if not roadmap:
        return []

    if isinstance(roadmap, dict):

        for key in [
            "roadmap",
            "phases",
            "milestones",
            "learning_path",
            "steps",
        ]:

            if key in roadmap and isinstance(
                roadmap[key],
                list
            ):

                return roadmap[key]

        return [roadmap]

    if isinstance(roadmap, list):
        return roadmap

    return []


def get_title(item, index):

    if isinstance(item, dict):

        return (
            item.get("title")
            or item.get("skill")
            or item.get("name")
            or item.get("milestone")
            or f"Learning milestone {index + 1}"
        )

    return str(item)


def get_description(item):

    if isinstance(item, dict):

        return (
            item.get("description")
            or item.get("reason")
            or item.get("summary")
            or item.get("details")
            or ""
        )

    return ""


def get_resources(item):

    if isinstance(item, dict):

        return (
            item.get("resources")
            or item.get("courses")
            or item.get("learning_resources")
            or []
        )

    return []


def render_roadmap(profile, output):

    roadmap_data = output.get("roadmap") or []

    roadmap = normalize_roadmap(roadmap_data)

    # ========================================================
    # HERO
    # ========================================================

    render_html(f"""
    <div style="margin-bottom:30px;">

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
            ✦ PERSONALIZED ROADMAP
        </div>

        <div style="
            font-family:Manrope,sans-serif;
            font-size:clamp(32px,4vw,48px);
            font-weight:800;
            letter-spacing:-.05em;
            color:#172033;
            margin-top:12px;
        ">
            Your path to {esc(getattr(profile, "career_goal", "your goal"))}.
        </div>

        <div style="
            max-width:760px;
            color:#6B7280;
            font-size:15px;
            line-height:1.7;
            margin-top:10px;
        ">
            A structured sequence designed around your current skills,
            learning goals and available time.
        </div>

    </div>
    """)

    # ========================================================
    # ROADMAP OVERVIEW
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Learning milestones",
            len(roadmap),
        )

    with col2:

        st.metric(
            "Weekly commitment",
            f"{getattr(profile, 'weekly_hours', '—')} hrs",
        )

    with col3:

        st.metric(
            "Target timeline",
            f"{getattr(profile, 'timeline_weeks', '—')} weeks",
        )

    st.write("")

    # ========================================================
    # EMPTY STATE
    # ========================================================

    if not roadmap:

        with st.container(border=True):

            st.markdown("### Your roadmap is being prepared")

            st.write(
                "PathPilot has your learner profile and is ready to "
                "structure your personalized learning sequence."
            )

            st.info(
                "No roadmap milestones were returned by the intelligence "
                "engine yet."
            )

        return

    # ========================================================
    # PROGRESS
    # ========================================================

    progress_state = st.session_state.get(
        "roadmap_progress",
        {}
    )

    completed = sum(
        1
        for index in range(len(roadmap))
        if progress_state.get(str(index), False)
    )

    progress_percent = (
        completed / len(roadmap)
        if roadmap
        else 0
    )

    with st.container(border=True):

        left, right = st.columns([0.75, 0.25])

        with left:

            st.markdown("### Your roadmap progress")

            st.caption(
                f"{completed} of {len(roadmap)} milestones completed"
            )

            st.progress(progress_percent)

        with right:

            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    font-family:Manrope,sans-serif;
                    font-size:32px;
                    font-weight:800;
                    color:#5B5CE2;
                    padding-top:10px;
                ">
                    {int(progress_percent * 100)}%
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")

    # ========================================================
    # ROADMAP TIMELINE
    # ========================================================

    st.markdown("### Your learning sequence")

    for index, item in enumerate(roadmap):

        title = get_title(item, index)

        description = get_description(item)

        resources = get_resources(item)

        key = str(index)

        is_complete = progress_state.get(
            key,
            False
        )

        # ----------------------------------------------------
        # MILESTONE HEADER
        # ----------------------------------------------------

        status_text = (
            "COMPLETED"
            if is_complete
            else "UP NEXT"
        )

        status_color = (
            "#16A36A"
            if is_complete
            else "#5B5CE2"
        )

        with st.container(border=True):

            top_left, top_right = st.columns([0.12, 0.88])

            with top_left:

                st.markdown(
                    f"""
                    <div style="
                        width:46px;
                        height:46px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        border-radius:14px;
                        background:#F0F0FF;
                        color:#5B5CE2;
                        font-family:Manrope,sans-serif;
                        font-size:17px;
                        font-weight:800;
                    ">
                        {index + 1}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with top_right:

                st.caption(
                    f"STEP {index + 1} · {status_text}"
                )

                st.markdown(f"### {esc(title)}")

            if description:

                st.write(description)

            # ------------------------------------------------
            # ITEM DETAILS
            # ------------------------------------------------

            if isinstance(item, dict):

                prerequisites = (
                    item.get("prerequisites")
                    or item.get("required_skills")
                    or []
                )

                estimated_time = (
                    item.get("estimated_hours")
                    or item.get("est_hours")
                    or item.get("duration")
                )

                difficulty = item.get("difficulty")

                details = []

                if difficulty:
                    details.append(
                        f"**Difficulty:** {esc(difficulty)}"
                    )

                if estimated_time:
                    details.append(
                        f"**Estimated effort:** {esc(estimated_time)}"
                    )

                if details:

                    st.caption(" · ".join(details))

                if prerequisites:

                    if not isinstance(prerequisites, list):
                        prerequisites = [prerequisites]

                    st.write("")

                    st.caption("PREREQUISITES")

                    for prerequisite in prerequisites:

                        st.markdown(
                            f"• {esc(prerequisite)}"
                        )

            # ------------------------------------------------
            # RESOURCES
            # ------------------------------------------------

            if resources:

                if not isinstance(resources, list):
                    resources = [resources]

                with st.expander(
                    "Recommended learning resources"
                ):

                    for resource in resources:

                        if isinstance(resource, dict):

                            name = (
                                resource.get("title")
                                or resource.get("name")
                                or "Learning resource"
                            )

                            url = (
                                resource.get("url")
                                or resource.get("link")
                            )

                            if url:

                                st.markdown(
                                    f"• [{esc(name)}]({url})"
                                )

                            else:

                                st.markdown(
                                    f"• {esc(name)}"
                                )

                        else:

                            st.markdown(
                                f"• {esc(resource)}"
                            )

            st.write("")

            # ------------------------------------------------
            # PROGRESS ACTION
            # ------------------------------------------------

            if not is_complete:

                if st.button(
                    f"Mark '{title}' as complete ✓",
                    key=f"complete_{index}",
                ):

                    progress_state[key] = True

                    st.session_state.roadmap_progress = (
                        progress_state
                    )

                    st.rerun()

            else:

                if st.button(
                    f"Completed ✓ — Undo",
                    key=f"undo_{index}",
                ):

                    progress_state[key] = False

                    st.session_state.roadmap_progress = (
                        progress_state
                    )

                    st.rerun()

        if index < len(roadmap) - 1:

            st.markdown(
                """
                <div style="
                    width:2px;
                    height:24px;
                    background:#E2E5F0;
                    margin-left:24px;
                ">
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ========================================================
    # COMPLETION STATE
    # ========================================================

    if completed == len(roadmap):

        st.write("")

        render_html("""
        <div style="
            background:linear-gradient(135deg,#ECFAF3,#F7FFFA);
            border:1px solid #CDEEDC;
            border-radius:22px;
            padding:30px;
            text-align:center;
        ">

            <div style="
                font-size:34px;
                margin-bottom:8px;
            ">
                ✦
            </div>

            <div style="
                font-family:Manrope,sans-serif;
                font-size:27px;
                font-weight:800;
                color:#16794F;
            ">
                Learning path completed!
            </div>

            <div style="
                color:#4E8068;
                margin-top:8px;
            ">
                You've completed every milestone currently in your personalized roadmap.
            </div>

        </div>
        """)

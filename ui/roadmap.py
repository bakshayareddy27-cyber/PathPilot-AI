import streamlit as st


def _pick(data, *keys, default=None):
    if not isinstance(data, dict):
        return default
    for key in keys:
        value = data.get(key)
        if value is not None and value != "":
            return value
    return default


def _items(roadmap):
    if isinstance(roadmap, list):
        return roadmap
    if isinstance(roadmap, dict):
        for key in ("phases", "roadmap", "steps", "milestones", "learning_path"):
            if isinstance(roadmap.get(key), list):
                return roadmap[key]
    return []


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _title(item, index):
    if isinstance(item, dict):
        return str(
            _pick(item, "title", "skill", "name", "phase", "milestone", default=f"Milestone {index + 1}")
        )
    return str(item)


def render_roadmap(profile, output):
    output = output or {}
    roadmap = _items(output.get("roadmap"))

    st.markdown(
        """
        <div class="pp-kicker">Personalised path generator</div>
        <div class="pp-title">Your learning roadmap.</div>
        <div class="pp-subtitle">
            A structured sequence of milestones designed around prerequisites, skill gaps,
            learning capacity and your career objective.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not roadmap:
        st.info(
            "Your roadmap is being prepared. Generate the learning path again if no milestones appear."
        )
        return

    progress_state = st.session_state.setdefault("roadmap_progress", {})

    completed_count = sum(
        1
        for index in range(len(roadmap))
        if progress_state.get(f"roadmap_{index}") is True
    )
    progress = completed_count / len(roadmap)

    st.write("")
    with st.container(border=True):
        a, b, c = st.columns([1.3, 1, 1])
        with a:
            st.caption("JOURNEY PROGRESS")
            st.subheader(f"{completed_count} of {len(roadmap)} milestones completed")
            st.progress(progress)
        with b:
            st.metric("Completion", f"{round(progress * 100)}%")
        with c:
            st.metric("Goal", str(getattr(profile, "career_goal", "Personalised path")))

    st.write("")
    st.caption("MILESTONE JOURNEY")

    for index, item in enumerate(roadmap):
        key = f"roadmap_{index}"
        done = progress_state.get(key, False)
        title = _title(item, index)

        if done:
            label = f"✓  {index + 1:02d} · {title}"
        elif index == completed_count:
            label = f"✦  {index + 1:02d} · {title}"
        else:
            label = f"○  {index + 1:02d} · {title}"

        with st.container(border=True):
            top_left, top_right = st.columns([4, 1])
            with top_left:
                st.subheader(label)

                if isinstance(item, dict):
                    description = _pick(
                        item,
                        "description",
                        "summary",
                        "objective",
                        "details",
                        default=None,
                    )
                    if description:
                        st.write(str(description))

                    prerequisites = _as_list(
                        _pick(item, "prerequisites", "prerequisite", default=[])
                    )
                    resources = _as_list(
                        _pick(item, "resources", "learning_resources", default=[])
                    )
                    project = _pick(item, "project", "project_idea", "assessment", default=None)

                    meta = []
                    difficulty = _pick(item, "difficulty", "level", default=None)
                    duration = _pick(
                        item, "duration", "estimated_time", "estimated_hours", "hours", default=None
                    )
                    if difficulty:
                        meta.append(f"Difficulty: {difficulty}")
                    if duration:
                        meta.append(f"Estimated effort: {duration}")
                    if meta:
                        st.caption(" · ".join(map(str, meta)))

                    if prerequisites:
                        with st.expander("Prerequisites"):
                            for prereq in prerequisites:
                                st.write(f"• {prereq}")

                    if resources:
                        with st.expander("Recommended learning resources"):
                            for resource in resources:
                                if isinstance(resource, dict):
                                    name = _pick(resource, "title", "name", "resource", default="Resource")
                                    link = _pick(resource, "url", "link", default=None)
                                    if link:
                                        st.markdown(f"- [{name}]({link})")
                                    else:
                                        st.write(f"• {name}")
                                else:
                                    st.write(f"• {resource}")

                    if project:
                        st.markdown("**Practice / milestone project**")
                        st.write(str(project))

            with top_right:
                button_label = "Completed ✓" if done else "Mark complete"
                if st.button(
                    button_label,
                    key=f"complete_button_{index}",
                    use_container_width=True,
                    type="primary" if not done else "secondary",
                ):
                    progress_state[key] = not done
                    st.session_state.roadmap_progress = progress_state
                    st.rerun()

    st.write("")
    with st.container(border=True):
        st.caption("ADAPTIVE LEARNING")
        st.subheader("Your roadmap is not static.")
        st.write(
            "As you complete milestones and provide feedback, PathPilot can use your progress "
            "signals to adjust future recommendations and keep the path aligned with your needs."
        )

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
            value = roadmap.get(key)
            if isinstance(value, list):
                return value
    return []


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def _title(item, index):
    if isinstance(item, dict):
        return str(_pick(
            item,
            "title", "skill", "name", "phase", "milestone",
            default=f"Milestone {index + 1}",
        ))
    return str(item)


def _resource_text(resource):
    if isinstance(resource, dict):
        return str(_pick(resource, "title", "name", "resource", default="Resource"))
    return str(resource)


def _completed_indices(total, progress_state):
    return {
        i for i in range(total)
        if progress_state.get(f"roadmap_{i}") is True
        or progress_state.get(f"roadmap_{i}") == "completed"
    }


def render_roadmap(profile, output):
    output = output or {}
    roadmap = _items(output.get("roadmap"))

    st.markdown(
        """
        <div class="pp-kicker">Personalised path generator</div>
        <div class="pp-title">Your learning roadmap.</div>
        <div class="pp-subtitle">
            A prerequisite-aware sequence of milestones designed around your skill gaps,
            learning capacity and career objective.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not roadmap:
        st.info("Your roadmap is not available yet. Generate the learning path again to create your milestones.")
        return

    progress_state = st.session_state.setdefault("roadmap_progress", {})
    completed_indices = _completed_indices(len(roadmap), progress_state)
    completed_count = len(completed_indices)
    progress = completed_count / len(roadmap)
    next_index = next((i for i in range(len(roadmap)) if i not in completed_indices), None)

    st.write("")
    with st.container(border=True):
        a, b, c = st.columns([1.45, .8, 1.15], gap="large")
        with a:
            st.caption("JOURNEY PROGRESS")
            st.subheader(f"{completed_count} of {len(roadmap)} milestones completed")
            st.progress(progress)
            if next_index is not None:
                st.caption(f"Next up: Milestone {next_index + 1}")
            else:
                st.success("Roadmap complete 🎉")
        with b:
            st.metric("Completion", f"{round(progress * 100)}%")
        with c:
            st.metric("Milestones", len(roadmap))

    st.write("")
    st.caption("MILESTONE JOURNEY")

    for index, item in enumerate(roadmap):
        key = f"roadmap_{index}"
        done = index in completed_indices
        is_next = index == next_index
        title = _title(item, index)

        if done:
            marker = "✓"
            state_text = "COMPLETED"
        elif is_next:
            marker = "✦"
            state_text = "UP NEXT"
        else:
            marker = "○"
            state_text = "UPCOMING"

        with st.container(border=True):
            top_left, top_right = st.columns([4.2, 1], gap="large")
            with top_left:
                st.caption(f"{marker}  MILESTONE {index + 1:02d} · {state_text}")
                st.subheader(title)

                if isinstance(item, dict):
                    description = _pick(item, "description", "summary", "objective", "details")
                    if description:
                        st.write(str(description))

                    difficulty = _pick(item, "difficulty", "level")
                    duration = _pick(item, "duration", "estimated_time", "estimated_hours", "hours")
                    meta = []
                    if difficulty:
                        meta.append(f"Difficulty · {difficulty}")
                    if duration:
                        meta.append(f"Estimated effort · {duration}")
                    if meta:
                        st.caption("  •  ".join(map(str, meta)))

                    prerequisites = _as_list(_pick(item, "prerequisites", "prerequisite", default=[]))
                    resources = _as_list(_pick(item, "resources", "learning_resources", default=[]))
                    project = _pick(item, "project", "project_idea", "assessment")

                    if prerequisites:
                        with st.expander("Prerequisites"):
                            for prereq in prerequisites:
                                if isinstance(prereq, dict):
                                    st.write(f"• {_pick(prereq, 'title', 'skill', 'name', default=str(prereq))}")
                                else:
                                    st.write(f"• {prereq}")

                    if resources:
                        with st.expander("Recommended learning resources"):
                            for resource in resources:
                                if isinstance(resource, dict):
                                    name = _resource_text(resource)
                                    link = _pick(resource, "url", "link")
                                    if link:
                                        st.markdown(f"• [{name}]({link})")
                                    else:
                                        st.write(f"• {name}")
                                else:
                                    st.write(f"• {resource}")

                    if project:
                        st.markdown("**Practice / milestone project**")
                        st.write(str(project))

            with top_right:
                st.write("")
                if done:
                    button_label = "Completed ✓"
                    button_type = "secondary"
                else:
                    button_label = "Mark complete"
                    button_type = "primary" if is_next else "secondary"

                if st.button(
                    button_label,
                    key=f"complete_button_{index}",
                    use_container_width=True,
                    type=button_type,
                ):
                    progress_state[key] = not done
                    st.session_state.roadmap_progress = progress_state
                    st.rerun()

    st.write("")
    with st.container(border=True):
        st.caption("ADAPTIVE LEARNING")
        st.subheader("Your roadmap can evolve with you.")
        st.write(
            "As you complete milestones and provide feedback, PathPilot can use those progress "
            "signals to keep future recommendations aligned with your pace and goals."
        )

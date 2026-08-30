import streamlit as st


def _value(data, *keys, default="—"):
    if not isinstance(data, dict):
        return default
    for key in keys:
        value = data.get(key)
        if value is not None and value != "":
            return value
    return default


def _normalise_score(value):
    if isinstance(value, dict):
        value = _value(value, "score", "readiness_score", "value", default="—")
    if isinstance(value, (int, float)):
        return round(value, 1)
    return value


def _listify(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return list(value)
    return [value]


def _roadmap_items(roadmap):
    if isinstance(roadmap, list):
        return roadmap
    if isinstance(roadmap, dict):
        for key in ("phases", "roadmap", "steps", "milestones", "learning_path"):
            value = roadmap.get(key)
            if isinstance(value, list):
                return value
    return []


def _item_title(item, default="Next milestone"):
    if isinstance(item, dict):
        return str(_value(item, "title", "skill", "name", "phase", "milestone", default=default))
    return str(item) if item is not None else default


def _completed_indices(total, progress_state):
    return {
        i for i in range(total)
        if progress_state.get(f"roadmap_{i}") is True
        or progress_state.get(f"roadmap_{i}") == "completed"
    }


def render_dashboard(profile, output):
    output = output or {}

    name = getattr(profile, "name", "Learner")
    goal = getattr(profile, "career_goal", "your goal")
    weekly_hours = getattr(profile, "weekly_hours", "—")

    readiness = _normalise_score(output.get("readiness"))
    health = output.get("path_health") or {}
    health_score = _value(health, "health_score", "score", default="—")
    health_status = _value(health, "status", default="Building")

    roadmap = _roadmap_items(output.get("roadmap"))
    next_action = output.get("next_best_action") or {}
    skill = _value(next_action, "skill", "title", "name", default="Your next learning step")
    difficulty = _value(next_action, "difficulty", "level", default="Personalized")
    effort = _value(next_action, "est_hours", "estimated_hours", "hours", default="—")

    st.markdown(
        f"""
        <div class="pp-kicker">Your learning workspace</div>
        <div class="pp-title">Good to see you, {name}.</div>
        <div class="pp-subtitle">
            Here is your personalised intelligence snapshot for your journey toward <b>{goal}</b>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Career goal", str(goal))
    with m2:
        st.metric("Readiness", f"{readiness}/100" if readiness != "—" else "—")
    with m3:
        st.metric("Path health", f"{health_score}/100" if health_score != "—" else "—")
    with m4:
        st.metric("Weekly commitment", f"{weekly_hours} hrs")

    st.write("")
    left, right = st.columns([1.55, 0.85], gap="large")

    with left:
        with st.container(border=True):
            st.caption("✦ PATHPILOT'S NEXT BEST MOVE")
            st.subheader(str(skill))
            st.write(
                "This recommendation is selected from your learner profile, current readiness "
                "and the structure of your personalised learning path."
            )

            a, b, c = st.columns(3)
            with a:
                st.caption("DIFFICULTY")
                st.write(f"**{difficulty}**")
            with b:
                st.caption("ESTIMATED EFFORT")
                st.write(f"**{effort} hrs**" if effort != "—" else "**Personalised**")
            with c:
                st.caption("PATH STATUS")
                st.write(f"**{health_status}**")

            reasons = _listify(_value(next_action, "reasons", "reason", "why", default=[]))
            if reasons:
                st.divider()
                st.markdown("**Why this now?**")
                for reason in reasons[:3]:
                    if isinstance(reason, dict):
                        reason = _value(reason, "text", "reason", "message", default=str(reason))
                    st.write(f"✓  {reason}")

    with right:
        with st.container(border=True):
            st.caption("JOURNEY SNAPSHOT")
            st.subheader("Your path at a glance")

            total = len(roadmap)
            progress_state = st.session_state.get("roadmap_progress", {})
            completed_indices = _completed_indices(total, progress_state)
            completed = len(completed_indices)
            progress = min(completed / total, 1.0) if total else 0.0

            st.metric("Milestones", total)
            st.progress(progress)
            st.caption(f"{completed} completed · {max(total - completed, 0)} remaining")

            if total:
                st.divider()
                st.caption("UP NEXT")
                next_index = next((i for i in range(total) if i not in completed_indices), None)
                if next_index is None:
                    st.success("All milestones completed 🎉")
                else:
                    st.write(f"**{_item_title(roadmap[next_index])}**")
                    st.caption(f"Milestone {next_index + 1} of {total}")

    st.write("")
    lower_left, lower_right = st.columns(2, gap="large")

    with lower_left:
        with st.container(border=True):
            st.caption("SKILL GAP INTELLIGENCE")
            st.subheader("Where to focus")
            gaps = output.get("skill_gap")
            if isinstance(gaps, dict):
                missing = gaps.get("missing_skills") or gaps.get("skill_gaps") or gaps.get("gaps") or []
                strengths = gaps.get("strengths") or gaps.get("current_skills") or []
                if missing:
                    st.markdown("**Priority gaps**")
                    for item in _listify(missing)[:5]:
                        st.write(f"• {_item_title(item, 'Skill') if isinstance(item, dict) else item}")
                elif strengths:
                    st.markdown("**Current strengths**")
                    for item in _listify(strengths)[:5]:
                        st.write(f"• {item}")
                else:
                    st.caption("Skill-gap details will appear after analysis.")
            elif isinstance(gaps, list) and gaps:
                for item in gaps[:5]:
                    st.write(f"• {item}")
            else:
                st.caption("Skill-gap details will appear after analysis.")

    with lower_right:
        with st.container(border=True):
            st.caption("INTELLIGENCE SIGNALS")
            st.subheader("What PathPilot is watching")
            risks = _listify(output.get("risks"))
            if risks:
                for risk in risks[:4]:
                    if isinstance(risk, dict):
                        title = _value(risk, "title", "type", "name", default="Learning signal")
                        message = _value(risk, "message", "description", default="")
                        st.write(f"**{title}**")
                        if message:
                            st.caption(str(message))
                    else:
                        st.write(f"**{risk}**")
            else:
                st.success("No major learning risks detected right now.")

    st.write("")
    with st.container(border=True):
        st.caption("WHAT MAKES THIS PATH PERSONAL")
        c1, c2, c3 = st.columns(3, gap="large")
        with c1:
            st.write("**Profile-aware**")
            st.caption("Goal, experience level, interests and current skills shape the path.")
        with c2:
            st.write("**Explainable**")
            st.caption("Recommendations include reasoning instead of appearing as random suggestions.")
        with c3:
            st.write("**Adaptive**")
            st.caption("Feedback and progress can influence future learning recommendations.")

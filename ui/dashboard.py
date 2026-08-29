"""
PathPilot AI — Overview dashboard rendering.
Displays readiness, path health, skill gaps, and active risks using
real deterministic engine output only.
"""

import streamlit as st

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


def render_dashboard(profile, engine_output, safe_call, engine):
    st.markdown("## 🏠 Overview")

    readiness = engine_output.get("readiness")
    health = engine_output.get("path_health") or {}
    skill_gap = engine_output.get("skill_gap")
    risks = engine_output.get("risks") or []

    readiness_score = _extract_score(readiness)
    health_score = health.get("health_score", "N/A")
    health_status = health.get("status", "Unknown")

    missing_skills = _extract_missing_skills(skill_gap)
    active_risks_count = len(risks)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Readiness Score", readiness_score if readiness_score is not None else "N/A")
    with col2:
        st.metric("❤️ Path Health", f"{health_score}", delta=health_status if health_status != "Unknown" else None)
    with col3:
        st.metric("📚 Missing Skills", len(missing_skills))
    with col4:
        st.metric("⚠️ Active Risks", active_risks_count)

    st.divider()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("### Skills: Possessed vs Missing")
        current_skills = list(getattr(profile, "current_skills", []) or [])
        _render_skills_chart(current_skills, missing_skills)

    with col_right:
        st.markdown("### Prioritized Skill Gaps")
        _render_skill_gap_list(missing_skills)

    st.divider()
    st.markdown("### Quick Snapshot")
    snap_col1, snap_col2 = st.columns(2)
    with snap_col1:
        st.markdown(f"**Career Goal:** {getattr(profile, 'career_goal', 'N/A')}")
        st.markdown(f"**Weekly Hours:** {getattr(profile, 'weekly_hours', 'N/A')}")
    with snap_col2:
        st.markdown(f"**Timeline:** {getattr(profile, 'timeline_weeks', 'N/A')} weeks")
        st.markdown(f"**Current Skills:** {', '.join(getattr(profile, 'current_skills', []) or []) or 'None yet'}")


def _extract_score(readiness):
    if readiness is None:
        return None
    if isinstance(readiness, dict):
        return readiness.get("score") or readiness.get("readiness_score")
    if isinstance(readiness, (int, float)):
        return readiness
    return None


def _extract_missing_skills(skill_gap):
    if not skill_gap:
        return []
    if isinstance(skill_gap, dict):
        for key in ("missing_skills", "missing", "gaps"):
            if key in skill_gap and isinstance(skill_gap[key], list):
                return skill_gap[key]
        return []
    if isinstance(skill_gap, list):
        return skill_gap
    return []


def _render_skills_chart(current_skills, missing_skills):
    possessed_count = len(current_skills)
    missing_count = len(missing_skills)

    if possessed_count == 0 and missing_count == 0:
        st.info("No skill data available yet.")
        return

    if PLOTLY_AVAILABLE:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=["Possessed", "Missing"],
                    y=[possessed_count, missing_count],
                    marker_color=["#22c55e", "#ef4444"],
                )
            ]
        )
        fig.update_layout(
            height=280,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#e5e7eb",
            yaxis_title="Skill Count",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart({"Possessed": possessed_count, "Missing": missing_count})


def _render_skill_gap_list(missing_skills):
    if not missing_skills:
        st.success("No missing skills detected — you're well aligned with your goal.")
        return

    for item in missing_skills[:8]:
        if isinstance(item, dict):
            name = item.get("skill") or item.get("name") or "Unknown skill"
            priority = item.get("priority", "")
            st.markdown(f"- **{name}**" + (f" · priority: {priority}" if priority else ""))
        else:
            st.markdown(f"- **{item}**")

    if len(missing_skills) > 8:
        st.caption(f"+ {len(missing_skills) - 8} more skill gaps")
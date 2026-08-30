"""
PathPilot AI — Overview dashboard rendering.
Reads only from engine_output (produced in app.py). No backend calls here.
"""

import streamlit as st

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


def render_dashboard(profile, engine_output, safe_call, engine):
    st.markdown('<div class="pp-eyebrow">LEARNING INTELLIGENCE SNAPSHOT</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="pp-section-title">Overview</h2>', unsafe_allow_html=True)

    readiness = engine_output.get("readiness")
    health = engine_output.get("path_health") or {}
    skill_gap = engine_output.get("skill_gap")
    risks = engine_output.get("risks") or []

    readiness_score = _extract_score(readiness)
    health_score = health.get("health_score", "—")
    health_status = health.get("status", "Unknown")
    missing_skills = _extract_missing_skills(skill_gap)

    _render_hero_and_supporting_metrics(readiness_score, health_score, health_status, len(missing_skills), len(risks))

    st.write("")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown('<div class="pp-eyebrow">SKILLS LANDSCAPE</div>', unsafe_allow_html=True)
        current_skills = list(getattr(profile, "current_skills", []) or [])
        _render_skills_chart(current_skills, missing_skills)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown('<div class="pp-eyebrow">PRIORITY GAPS</div>', unsafe_allow_html=True)
        _render_skill_gap_list(missing_skills)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.markdown('<div class="pp-eyebrow">YOUR CURRENT POSITION</div>', unsafe_allow_html=True)
    snap_col1, snap_col2, snap_col3, snap_col4 = st.columns(4)
    with snap_col1:
        _render_position_field("Career Goal", getattr(profile, "career_goal", "N/A"))
    with snap_col2:
        _render_position_field("Weekly Hours", f'{getattr(profile, "weekly_hours", "N/A")} hrs/wk')
    with snap_col3:
        _render_position_field("Timeline", f'{getattr(profile, "timeline_weeks", "N/A")} weeks')
    with snap_col4:
        skills_text = ", ".join(getattr(profile, "current_skills", []) or []) or "None yet"
        _render_position_field("Current Skills", skills_text)
    st.markdown('</div>', unsafe_allow_html=True)


def _render_position_field(label, value):
    st.markdown(
        f'<div style="margin-bottom:0.2rem;">'
        f'<div style="font-size:0.7rem; color:var(--text-faint); text-transform:uppercase; '
        f'letter-spacing:0.06em; font-weight:600; margin-bottom:4px;">{label}</div>'
        f'<div style="font-size:0.9rem; color:var(--text-primary); font-weight:600; line-height:1.45;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_hero_and_supporting_metrics(readiness_score, health_score, health_status, missing_count, risk_count):
    """
    Visual hierarchy: readiness is the hero metric (larger, tinted card, spans more width);
    path health, missing skills and active risks are supporting metrics in a row beside it.
    This intentionally avoids four identical cards.
    """
    is_good_readiness = isinstance(readiness_score, (int, float)) and readiness_score >= 60
    readiness_display = f"{readiness_score}%" if readiness_score is not None else "—"
    readiness_trend_class = "trend-good" if is_good_readiness else "trend-neutral"
    readiness_desc = "On track" if is_good_readiness else "Building up"

    health_trend_class = {"Healthy": "trend-good", "At Risk": "trend-warn", "Critical": "trend-bad"}.get(health_status, "trend-neutral")
    risk_trend_class = "trend-bad" if risk_count > 0 else "trend-good"
    risk_desc = "Needs attention" if risk_count > 0 else "All clear"

    hero_col, supporting_col = st.columns([1.15, 2])

    with hero_col:
        st.markdown(
            f"""
            <div class="pp-metric-card hero" style="height:100%;">
                <div class="pp-metric-label">READINESS SCORE</div>
                <div class="pp-metric-value" style="font-size:2.6rem;">{readiness_display}</div>
                <div class="pp-metric-desc {readiness_trend_class}">{readiness_desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with supporting_col:
        s1, s2, s3 = st.columns(3)
        with s1:
            st.markdown(
                f"""
                <div class="pp-metric-card">
                    <div class="pp-metric-label">Path Health</div>
                    <div class="pp-metric-value">{health_score}</div>
                    <div class="pp-metric-desc {health_trend_class}">{health_status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s2:
            st.markdown(
                f"""
                <div class="pp-metric-card">
                    <div class="pp-metric-label">Missing Skills</div>
                    <div class="pp-metric-value">{missing_count}</div>
                    <div class="pp-metric-desc trend-neutral">Skills remaining</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with s3:
            st.markdown(
                f"""
                <div class="pp-metric-card">
                    <div class="pp-metric-label">Active Risks</div>
                    <div class="pp-metric-value">{risk_count}</div>
                    <div class="pp-metric-desc {risk_trend_class}">{risk_desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


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
        st.markdown('<p style="color:var(--text-faint);">No skill data available yet.</p>', unsafe_allow_html=True)
        return

    if PLOTLY_AVAILABLE:
        fig = go.Figure(
            data=[
                go.Bar(
                    x=["Current Skills", "Skills Needed"],
                    y=[possessed_count, missing_count],
                    marker_color=["#5B5CE2", "#EEF0F7"],
                    marker_line=dict(color=["#5B5CE2", "#D3D7E6"], width=1),
                    width=0.5,
                    text=[possessed_count, missing_count],
                    textposition="outside",
                    textfont=dict(color="#545873", family="JetBrains Mono", size=13),
                )
            ]
        )
        fig.update_layout(
            height=240,
            margin=dict(l=10, r=10, t=25, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#767A97",
            font_family="Inter",
            yaxis=dict(gridcolor="#EEF0F7", title="Skill Count", zeroline=False),
            xaxis=dict(showgrid=False),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart({"Current Skills": possessed_count, "Skills Needed": missing_count})


def _render_skill_gap_list(missing_skills):
    if not missing_skills:
        st.markdown('<p style="color:var(--success);">No missing skills detected — you\'re well aligned with your goal.</p>', unsafe_allow_html=True)
        return

    for item in missing_skills[:8]:
        if isinstance(item, dict):
            name = item.get("skill") or item.get("name") or "Unknown skill"
            priority = item.get("priority", "")
            priority_badge = ""
            if priority != "":
                try:
                    p = int(priority)
                    tier = "high" if p == 1 else ("medium" if p == 2 else "low")
                except (TypeError, ValueError):
                    tier = "low"
                colors = {
                    "high": ("var(--danger)", "var(--danger-soft)", "var(--danger-border)"),
                    "medium": ("var(--warning)", "var(--warning-soft)", "var(--warning-border)"),
                    "low": ("var(--accent)", "var(--accent-soft)", "var(--accent-dim)"),
                }
                fg, bg, bd = colors[tier]
                priority_badge = (
                    f'<span style="font-family:var(--font-mono); font-size:0.68rem; font-weight:700; '
                    f'color:{fg}; background:{bg}; border:1px solid {bd}; border-radius:999px; '
                    f'padding:0.15rem 0.55rem; margin-left:8px;">P{priority}</span>'
                )
            st.markdown(
                f'<div class="pp-insight-row"><span class="pp-insight-check" style="color:var(--accent);">•</span>'
                f'<span class="pp-insight-text"><b style="color:var(--text-primary);">{name}</b>{priority_badge}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="pp-insight-row"><span class="pp-insight-check" style="color:var(--accent);">•</span>'
                f'<span class="pp-insight-text">{item}</span></div>',
                unsafe_allow_html=True,
            )

    if len(missing_skills) > 8:
        st.markdown(f'<p style="color:var(--text-faint); font-size:0.81rem; margin-top:6px;">+ {len(missing_skills) - 8} more skill gaps</p>', unsafe_allow_html=True)

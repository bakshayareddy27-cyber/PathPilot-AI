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
    st.markdown('<div class="pp-eyebrow">YOUR LEARNING INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="pp-section-title">Overview</h2>', unsafe_allow_html=True)

    readiness = engine_output.get("readiness")
    health = engine_output.get("path_health") or {}
    skill_gap = engine_output.get("skill_gap")
    risks = engine_output.get("risks") or []

    readiness_score = _extract_score(readiness)
    health_score = health.get("health_score", "—")
    health_status = health.get("status", "Unknown")
    missing_skills = _extract_missing_skills(skill_gap)

    _render_metric_cards(readiness_score, health_score, health_status, len(missing_skills), len(risks))

    st.write("")
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown('<div class="pp-eyebrow">SKILLS COVERAGE</div>', unsafe_allow_html=True)
        current_skills = list(getattr(profile, "current_skills", []) or [])
        _render_skills_chart(current_skills, missing_skills)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="pp-card">', unsafe_allow_html=True)
        st.markdown('<div class="pp-eyebrow">PRIORITIZED SKILL GAPS</div>', unsafe_allow_html=True)
        _render_skill_gap_list(missing_skills)
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="pp-card">', unsafe_allow_html=True)
    st.markdown('<div class="pp-eyebrow">QUICK SNAPSHOT</div>', unsafe_allow_html=True)
    snap_col1, snap_col2 = st.columns(2)
    with snap_col1:
        st.markdown(
            f'<p style="color:var(--text-muted); font-size:0.9rem;">'
            f'<b style="color:var(--text-primary);">Career Goal</b><br>{getattr(profile, "career_goal", "N/A")}</p>'
            f'<p style="color:var(--text-muted); font-size:0.9rem;">'
            f'<b style="color:var(--text-primary);">Weekly Hours</b><br>{getattr(profile, "weekly_hours", "N/A")} hrs/week</p>',
            unsafe_allow_html=True,
        )
    with snap_col2:
        skills_text = ", ".join(getattr(profile, "current_skills", []) or []) or "None yet"
        st.markdown(
            f'<p style="color:var(--text-muted); font-size:0.9rem;">'
            f'<b style="color:var(--text-primary);">Timeline</b><br>{getattr(profile, "timeline_weeks", "N/A")} weeks</p>'
            f'<p style="color:var(--text-muted); font-size:0.9rem;">'
            f'<b style="color:var(--text-primary);">Current Skills</b><br>{skills_text}</p>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)


def _render_metric_cards(readiness_score, health_score, health_status, missing_count, risk_count):
    is_good_readiness = isinstance(readiness_score, (int, float)) and readiness_score >= 60
    cards = [
        ("Readiness", f"{readiness_score}%" if readiness_score is not None else "—",
         "↑ Improving" if is_good_readiness else "Building up",
         "trend-good" if is_good_readiness else "trend-neutral"),
        ("Path Health", f"{health_score}", health_status,
         {"Healthy": "trend-good", "At Risk": "trend-warn", "Critical": "trend-bad"}.get(health_status, "trend-neutral")),
        ("Missing Skills", str(missing_count), "Skills remaining", "trend-neutral"),
        ("Active Risks", str(risk_count), "Needs attention" if risk_count > 0 else "All clear",
         "trend-bad" if risk_count > 0 else "trend-good"),
    ]

    cols = st.columns(4)
    for col, (label, value, desc, trend_class) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="pp-metric-card">
                    <div class="pp-metric-label">{label}</div>
                    <div class="pp-metric-value">{value}</div>
                    <div class="pp-metric-desc {trend_class}">{desc}</div>
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
                    x=["Possessed", "Missing"],
                    y=[possessed_count, missing_count],
                    marker_color=["#6366F1", "#2A3145"],
                    marker_line_width=0,
                    width=0.5,
                )
            ]
        )
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#8992A6",
            font_family="Inter",
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Skill Count"),
            xaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.bar_chart({"Possessed": possessed_count, "Missing": missing_count})


def _render_skill_gap_list(missing_skills):
    if not missing_skills:
        st.markdown('<p style="color:var(--success);">No missing skills detected — you\'re well aligned with your goal.</p>', unsafe_allow_html=True)
        return

    for item in missing_skills[:8]:
        if isinstance(item, dict):
            name = item.get("skill") or item.get("name") or "Unknown skill"
            priority = item.get("priority", "")
            st.markdown(
                f'<div class="pp-insight-row"><span class="pp-insight-check" style="color:var(--cyan);">•</span>'
                f'<span class="pp-insight-text"><b style="color:var(--text-primary);">{name}</b>'
                f'{f" · priority {priority}" if priority != "" else ""}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="pp-insight-row"><span class="pp-insight-check" style="color:var(--cyan);">•</span>'
                f'<span class="pp-insight-text">{item}</span></div>',
                unsafe_allow_html=True,
            )

    if len(missing_skills) > 8:
        st.markdown(f'<p style="color:var(--text-faint); font-size:0.82rem; margin-top:6px;">+ {len(missing_skills) - 8} more skill gaps</p>', unsafe_allow_html=True)

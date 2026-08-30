import streamlit as st

def render_dashboard(profile, engine_output, safe_call, engine):
    """
    Renders the primary Overview Dashboard for PathPilot AI.
    Presents readiness scores, skill gap analysis, risk detection, and current position summary.
    """
    # Readiness & Path Health Metrics
    readiness = engine_output.get("readiness_score", 65)
    path_health = engine_output.get("path_health", {}).get("score", 85)
    skill_gaps = engine_output.get("skill_gaps", [])
    risks = engine_output.get("risks", [])
    next_action = engine_output.get("next_best_action", {}).get("skill", "Core Skill Setup")

    # Hero Intelligence Summary Banner
    st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 28px; margin-bottom: 24px; box-shadow: var(--shadow-card);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <span class="pp-badge pp-badge-indigo">Target Role Snapshot</span>
                    <h2 style="font-size: 1.8rem; margin: 8px 0 4px 0; color: #0F172A;">{profile.target_role}</h2>
                    <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 0;">Goal: "{profile.natural_goal}"</p>
                </div>
                <div style="text-align: right;">
                    <span class="pp-badge pp-badge-emerald">Role Readiness</span>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 2.5rem; font-weight: 800; color: #4F46E5; line-height: 1; margin-top: 4px;">{readiness}%</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Metrics Grid
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.markdown(f"""
            <div class="pp-card" style="margin-bottom: 0;">
                <div class="pp-metric-lbl">Role Readiness</div>
                <div class="pp-metric-val" style="color: #4F46E5;">{readiness}%</div>
                <div style="font-size: 0.78rem; color: #10B981; font-weight: 600; margin-top: 6px;">↑ Based on skill graph</div>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
            <div class="pp-card" style="margin-bottom: 0;">
                <div class="pp-metric-lbl">Skill Gaps</div>
                <div class="pp-metric-val" style="color: #0F172A;">{len(skill_gaps)}</div>
                <div style="font-size: 0.78rem; color: #64748B; font-weight: 500; margin-top: 6px;">Skills to acquire</div>
            </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
            <div class="pp-card" style="margin-bottom: 0;">
                <div class="pp-metric-lbl">Active Risks</div>
                <div class="pp-metric-val" style="color: {'#EF4444' if risks else '#10B981'};">{len(risks)}</div>
                <div style="font-size: 0.78rem; color: #64748B; font-weight: 500; margin-top: 6px;">Timeline blockers</div>
            </div>
        """, unsafe_allow_html=True)

    with m4:
        st.markdown(f"""
            <div class="pp-card" style="margin-bottom: 0;">
                <div class="pp-metric-lbl">Path Health</div>
                <div class="pp-metric-val" style="color: #10B981;">{path_health}</div>
                <div style="font-size: 0.78rem; color: #10B981; font-weight: 600; margin-top: 6px;">Optimal trajectory</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Main Dashboard Body: Skills Landscape & Priority Gaps
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown("""
            <div class="pp-card">
                <h4 style="font-size: 1.1rem; margin-bottom: 16px; color: #0F172A;">Priority Skill Gaps</h4>
        """, unsafe_allow_html=True)

        if skill_gaps:
            for idx, gap in enumerate(skill_gaps[:5]):
                gap_name = gap.get("skill", gap) if isinstance(gap, dict) else str(gap)
                priority = gap.get("priority", "High") if isinstance(gap, dict) else "High"
                category = gap.get("category", "Core Competency") if isinstance(gap, dict) else "Core Competency"

                badge_class = "pp-badge-rose" if priority == "High" else "pp-badge-amber"

                st.markdown(f"""
                    <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px 16px; border: 1px solid #F1F5F9; border-radius: 8px; margin-bottom: 8px; background: #FAF5FF;">
                        <div>
                            <div style="font-weight: 600; color: #0F172A; font-size: 0.95rem;">{gap_name}</div>
                            <div style="font-size: 0.78rem; color: #64748B;">Category: {category}</div>
                        </div>
                        <span class="pp-badge {badge_class}">{priority} Priority</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="padding: 16px; background: #ECFDF5; border-radius: 8px; color: #065F46; font-size: 0.9rem;">
                    🎉 No immediate skill gaps detected for your selected configuration!
                </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Current Skill Matrix
        st.markdown("""
            <div class="pp-card">
                <h4 style="font-size: 1.1rem; margin-bottom: 12px; color: #0F172A;">Validated Existing Skills</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 8px;">
        """, unsafe_allow_html=True)

        if profile.current_skills:
            for sk in profile.current_skills:
                st.markdown(f'<span class="pp-badge pp-badge-indigo" style="font-size: 0.82rem; padding: 6px 12px;">✓ {sk}</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span style="color: #94A3B8; font-size: 0.88rem;">No existing skills declared.</span>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with col_right:
        # Next Best Action Focus Box
        st.markdown(f"""
            <div class="pp-card" style="border-left: 4px solid #4F46E5; background: linear-gradient(180deg, #FFFFFF 0%, #EEF2FF 100%);">
                <span class="pp-badge pp-badge-indigo" style="margin-bottom: 8px;">Immediate Focus</span>
                <h4 style="font-size: 1.1rem; margin: 4px 0 8px 0; color: #0F172A;">Recommended Action</h4>
                <div style="font-size: 1.25rem; font-weight: 700; color: #4F46E5; margin-bottom: 8px;">{next_action}</div>
                <p style="font-size: 0.85rem; color: #475569; line-height: 1.5; margin-bottom: 16px;">
                    This skill is calculated as your single highest-leverage prerequisite.
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Learner Profile Information Card
        st.markdown(f"""
            <div class="pp-card">
                <h4 style="font-size: 1.1rem; margin-bottom: 12px; color: #0F172A;">Learner Profile Matrix</h4>
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #F1F5F9; font-size: 0.88rem;">
                    <span style="color: #64748B;">Experience</span>
                    <span style="font-weight: 600; color: #0F172A;">{profile.experience_level}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #F1F5F9; font-size: 0.88rem;">
                    <span style="color: #64748B;">Weekly Pace</span>
                    <span style="font-weight: 600; color: #0F172A;">{profile.weekly_hours} Hours</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #F1F5F9; font-size: 0.88rem;">
                    <span style="color: #64748B;">Target Horizon</span>
                    <span style="font-weight: 600; color: #0F172A;">{profile.timeline}</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 8px 0; font-size: 0.88rem;">
                    <span style="color: #64748B;">Learning Style</span>
                    <span style="font-weight: 600; color: #0F172A;">{profile.learning_style}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

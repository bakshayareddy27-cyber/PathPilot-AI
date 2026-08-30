import streamlit as st

def render_roadmap(profile, engine_output, safe_call):
    """
    Renders the Personalized Learning Roadmap View for PathPilot AI.
    Displays sequential learning milestones, progress tracking, prerequisites, and resource cards.
    """
    st.markdown("### Personalized Learning Journey")
    st.markdown("A structured, step-by-step roadmap optimized specifically for your target role and pace.")

    roadmap_data = engine_output.get("roadmap", [])

    # Default fallback roadmap stages if empty or loading
    if not roadmap_data:
        roadmap_data = [
            {
                "stage": "Stage 1: Core Fundamentals",
                "skill": "Python & Data Foundations",
                "status": "In Progress",
                "duration": "2 Weeks",
                "description": "Establish core mastery over data structures, language fundamentals, and environment setup.",
                "resources": [
                    {"title": "Python Core Documentation", "type": "Documentation", "link": "https://docs.python.org/3/"},
                    {"title": "Data Structures & Algorithms in Python", "type": "Course", "link": "#"}
                ],
                "prerequisites": ["None"]
            },
            {
                "stage": "Stage 2: Applied Architecture",
                "skill": "REST APIs & System Design",
                "status": "Upcoming",
                "duration": "3 Weeks",
                "description": "Learn to design modular API endpoints, handle data flows, and connect microservices.",
                "resources": [
                    {"title": "FastAPI Web Development Masterclass", "type": "Video", "link": "#"}
                ],
                "prerequisites": ["Python & Data Foundations"]
            },
            {
                "stage": "Stage 3: Advanced Specialization",
                "skill": "LLM Orchestration & Multi-Agent Workflows",
                "status": "Upcoming",
                "duration": "4 Weeks",
                "description": "Deploy stateful agent graph architectures, implement RAG systems, and optimize latency.",
                "resources": [
                    {"title": "LangGraph & LangChain Official Guide", "type": "Interactive", "link": "#"}
                ],
                "prerequisites": ["REST APIs & System Design"]
            }
        ]

    # Progress Summary Banner
    total_stages = len(roadmap_data)
    completed_stages = sum(1 for s in roadmap_data if s.get("status") == "Completed")
    progress_pct = int((completed_stages / total_stages) * 100) if total_stages > 0 else 0

    st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px 24px; margin-bottom: 28px; box-shadow: var(--shadow-subtle);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-weight: 700; color: #0F172A; font-size: 1rem;">Overall Roadmap Progress</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-weight: 700; color: #4F46E5;">{progress_pct}% Completed ({completed_stages}/{total_stages} Stages)</div>
            </div>
            <div style="width: 100%; background-color: #E2E8F0; border-radius: 9999px; height: 10px; overflow: hidden;">
                <div style="width: {progress_pct}%; background-color: #4F46E5; height: 100%; border-radius: 9999px; transition: width 0.4s ease;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Timeline Journey Render
    for idx, stage in enumerate(roadmap_data):
        stage_name = stage.get("stage", f"Stage {idx+1}")
        skill = stage.get("skill", "Core Competency")
        status = stage.get("status", "Upcoming")
        duration = stage.get("duration", "2 Weeks")
        description = stage.get("description", "Focus on mastering key principles and completing practical milestones.")
        resources = stage.get("resources", [])
        prereqs = stage.get("prerequisites", [])

        # Visual styling based on status
        if status == "Completed":
            badge_markup = '<span class="pp-badge pp-badge-emerald">✓ Completed</span>'
            border_style = "border-left: 4px solid #10B981;"
            bg_style = "background: #FFFFFF;"
        elif status == "In Progress":
            badge_markup = '<span class="pp-badge pp-badge-indigo">⚡ Current Focus</span>'
            border_style = "border-left: 4px solid #4F46E5;"
            bg_style = "background: linear-gradient(180deg, #FFFFFF 0%, #EEF2FF 100%);"
        else:
            badge_markup = '<span class="pp-badge pp-badge-amber">Upcoming</span>'
            border_style = "border-left: 4px solid #94A3B8;"
            bg_style = "background: #FFFFFF;"

        st.markdown(f"""
            <div class="pp-card-interactive" style="{border_style} {bg_style} margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                    <div>
                        <span style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">{stage_name}</span>
                        <h3 style="font-size: 1.35rem; margin: 2px 0 6px 0; color: #0F172A;">{skill}</h3>
                    </div>
                    <div>{badge_markup}</div>
                </div>
                <p style="font-size: 0.95rem; color: #475569; line-height: 1.5; margin-bottom: 16px;">
                    {description}
                </p>
                <div style="display: flex; gap: 16px; font-size: 0.82rem; color: #64748B; margin-bottom: 16px; flex-wrap: wrap;">
                    <div>⏱️ <strong>Estimated Duration:</strong> {duration}</div>
                    <div>🔗 <strong>Prerequisites:</strong> {', '.join(prereqs) if prereqs else 'None'}</div>
                </div>
        """, unsafe_allow_html=True)

        # Render Resources if available
        if resources:
            st.markdown("<div style='font-size: 0.85rem; font-weight: 700; color: #0F172A; margin-bottom: 8px;'>Recommended Curated Resources:</div>", unsafe_allow_html=True)
            res_cols = st.columns(min(len(resources), 3))
            for r_idx, res in enumerate(resources[:3]):
                with res_cols[r_idx]:
                    r_title = res.get("title", "Learning Resource") if isinstance(res, dict) else str(res)
                    r_type = res.get("type", "Course") if isinstance(res, dict) else "Resource"
                    r_link = res.get("link", "#") if isinstance(res, dict) else "#"
                    st.markdown(f"""
                        <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 12px;">
                            <span style="font-size: 0.72rem; font-weight: 700; color: #4F46E5; text-transform: uppercase;">{r_type}</span>
                            <div style="font-weight: 600; font-size: 0.85rem; color: #0F172A; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;"><a href="{r_link}" target="_blank" style="color: #0F172A; text-decoration: none;">{r_title}</a></div>
                        </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # Interactive Stage Status Toggle
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if status != "Completed":
                if st.button(f"Mark Completed", key=f"btn_comp_{idx}", type="secondary"):
                    stage["status"] = "Completed"
                    st.rerun()
            else:
                if st.button(f"Reopen Stage", key=f"btn_reopen_{idx}", type="secondary"):
                    stage["status"] = "In Progress"
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

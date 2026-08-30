"""
PathPilot AI — Learning roadmap rendering.
Reads only from engine_output["roadmap"] and writes to
st.session_state.roadmap_progress. No backend calls here.
"""

import streamlit as st


STATUS_OPTIONS = ["Not Started", "In Progress", "Completed"]

STATUS_META = {
    "Not Started": {"icon": "○", "label": "Not Started", "node_class": "", "accent": "var(--text-faint)"},
    "In Progress": {"icon": "◐", "label": "In Progress", "node_class": "pp-node-inprogress", "accent": "var(--accent)"},
    "Completed":   {"icon": "✓", "label": "Completed",   "node_class": "pp-node-completed", "accent": "var(--success)"},
}


def render_roadmap(profile, engine_output, safe_call):
    _inject_roadmap_styles()

    roadmap = engine_output.get("roadmap") or []

    total = len(roadmap)
    progress = st.session_state.get("roadmap_progress", {})
    completed = sum(1 for s in roadmap if isinstance(s, dict) and progress.get(s.get("skill"), "Not Started") == "Completed")
    current_skill = None
    for s in roadmap:
        if isinstance(s, dict) and progress.get(s.get("skill"), "Not Started") != "Completed":
            current_skill = s.get("skill")
            break

    st.markdown('<div class="pp-eyebrow">YOUR JOURNEY</div>', unsafe_allow_html=True)
    st.markdown('<h2 class="pp-section-title" style="margin-bottom:0.3rem;">Learning Roadmap</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:var(--text-muted); font-size:0.9rem; margin-top:0; margin-bottom:1.3rem;">'
        'A structured path from your current skills to your goal.</p>',
        unsafe_allow_html=True,
    )

    if not roadmap:
        st.markdown(
            '<div class="pp-card">No roadmap has been generated yet. Try adjusting your profile or career goal.</div>',
            unsafe_allow_html=True,
        )
        return

    if "roadmap_progress" not in st.session_state:
        st.session_state.roadmap_progress = {}

    _render_summary_strip(total, completed, current_skill)
    st.write("")

    for idx, step in enumerate(roadmap, start=1):
        _render_stage(idx, step, is_last=(idx == total))


# ----------------------------------------------------------------------
# Summary strip
# ----------------------------------------------------------------------
def _render_summary_strip(total, completed, current_skill):
    pct = int(round((completed / total) * 100)) if total else 0
    current_label = current_skill if current_skill else "Path complete"

    st.markdown(
        f"""
        <div class="pp-roadmap-summary">
            <div class="pp-roadmap-summary-item">
                <div class="pp-roadmap-summary-value">{total}</div>
                <div class="pp-roadmap-summary-label">Total Stages</div>
            </div>
            <div class="pp-roadmap-summary-divider"></div>
            <div class="pp-roadmap-summary-item">
                <div class="pp-roadmap-summary-value" style="color:var(--success);">{completed}</div>
                <div class="pp-roadmap-summary-label">Completed</div>
            </div>
            <div class="pp-roadmap-summary-divider"></div>
            <div class="pp-roadmap-summary-item">
                <div class="pp-roadmap-summary-value" style="color:var(--accent);">{pct}%</div>
                <div class="pp-roadmap-summary-label">Progress</div>
            </div>
            <div class="pp-roadmap-summary-divider"></div>
            <div class="pp-roadmap-summary-item" style="flex:1.6;">
                <div class="pp-roadmap-summary-value" style="font-size:1.05rem; font-family:var(--font-display);">{current_label}</div>
                <div class="pp-roadmap-summary-label">Current Stage</div>
            </div>
        </div>
        <div class="pp-roadmap-track"><div class="pp-roadmap-track-fill" style="width:{pct}%;"></div></div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# Stage
# ----------------------------------------------------------------------
def _render_stage(idx, step, is_last):
    if not isinstance(step, dict):
        st.markdown(f'<div class="pp-card">Stage {idx}: {step}</div>', unsafe_allow_html=True)
        return

    skill = step.get("skill", "Unknown Skill")
    priority = step.get("priority", "N/A")
    difficulty = step.get("difficulty", "N/A")
    prerequisites = step.get("prerequisites", []) or []
    resources = step.get("resources", []) or step.get("recommended_resources", []) or []

    progress = st.session_state.roadmap_progress
    current_status = progress.get(skill, "Not Started")
    meta = STATUS_META.get(current_status, STATUS_META["Not Started"])

    is_current = current_status == "In Progress"
    is_completed = current_status == "Completed"

    if is_current:
        stage_class = "pp-stage pp-stage-current"
    elif is_completed:
        stage_class = "pp-stage pp-stage-done"
    else:
        stage_class = "pp-stage pp-stage-upcoming"

    rail_col, body_col = st.columns([0.06, 0.94])

    with rail_col:
        line_html = "" if is_last else '<div class="pp-rail-line"></div>'
        st.markdown(
            f"""
            <div class="pp-rail">
                <div class="pp-rail-node {meta['node_class']}">{meta['icon']}</div>
                {line_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    with body_col:
        st.markdown(f'<div class="{stage_class}">', unsafe_allow_html=True)

        here_tag = '<span class="pp-here-tag">YOU ARE HERE</span>' if is_current else ""
        st.markdown(
            f"""
            <div class="pp-stage-top">
                <span class="pp-stage-index">STAGE {idx:02d}</span>
                <span class="pp-badge-soft" style="border-color:{meta['accent']}; color:{meta['accent']};">{meta['label']}</span>
                {here_tag}
            </div>
            <div class="pp-stage-title">{skill}</div>
            <div class="pp-stage-tags">
                <span class="pp-tag">{difficulty}</span>
                <span class="pp-tag">Priority {priority}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if prerequisites:
            prereq_chips = "".join(f'<span class="pp-chip pp-chip-prereq">{p}</span>' for p in prerequisites)
            st.markdown(
                f'<div class="pp-stage-block"><div class="pp-stage-block-label">Prerequisites</div>'
                f'<div>{prereq_chips}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="pp-stage-block"><div class="pp-stage-block-label">Prerequisites</div>'
                '<div class="pp-insight-text" style="font-size:0.83rem;">None — ready to start</div></div>',
                unsafe_allow_html=True,
            )

        if resources:
            chips = ""
            for r in resources[:4]:
                if isinstance(r, dict):
                    title = r.get("title") or r.get("name") or "Resource"
                    url = r.get("url") or r.get("link")
                    chips += (
                        f'<a href="{url}" target="_blank" style="text-decoration:none;">'
                        f'<span class="pp-chip">{title} ↗</span></a>'
                        if url else f'<span class="pp-chip">{title}</span>'
                    )
                else:
                    chips += f'<span class="pp-chip">{r}</span>'
            st.markdown(
                f'<div class="pp-stage-block"><div class="pp-stage-block-label">Resources</div><div>{chips}</div></div>',
                unsafe_allow_html=True,
            )

        with st.expander("Update status", expanded=False):
            new_status = st.radio(
                "Status",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(current_status),
                key=f"status_{skill}_{idx}",
                horizontal=True,
                label_visibility="collapsed",
            )
            if new_status != current_status:
                st.session_state.roadmap_progress[skill] = new_status
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)  # close pp-stage
        st.markdown('<div style="height:0.3rem;"></div>', unsafe_allow_html=True)


# ----------------------------------------------------------------------
# Scoped styles
# ----------------------------------------------------------------------
def _inject_roadmap_styles():
    st.markdown(
        """
        <style>
        .pp-roadmap-summary {
            display: flex; align-items: center; gap: 0;
            background: var(--surface); border: 1px solid var(--border);
            border-radius: var(--radius-md) var(--radius-md) 0 0;
            padding: 1.15rem 1.45rem;
            box-shadow: var(--shadow-sm);
        }
        .pp-roadmap-summary-item { flex: 1; }
        .pp-roadmap-summary-value { font-family: var(--font-display); font-size: 1.4rem; font-weight: 700; color: var(--text-primary); }
        .pp-roadmap-summary-label { color: var(--text-faint); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.07em; margin-top: 3px; font-weight: 600; }
        .pp-roadmap-summary-divider { width: 1px; height: 32px; background: var(--border); margin: 0 1.2rem; }
        .pp-roadmap-track { height: 4px; background: var(--surface-sunken); border-radius: 0 0 var(--radius-md) var(--radius-md); overflow: hidden; margin-bottom: 1.5rem; border: 1px solid var(--border); border-top: none; }
        .pp-roadmap-track-fill { height: 100%; background: var(--accent); transition: width 0.4s ease; }

        .pp-rail { display: flex; flex-direction: column; align-items: center; }
        .pp-rail-node {
            width: 30px; height: 30px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-family: var(--font-mono); font-size: 0.78rem; font-weight: 700;
            border: 2px solid var(--border-strong); color: var(--text-faint);
            background: var(--surface); flex-shrink: 0;
            box-shadow: var(--shadow-sm);
        }
        .pp-node-inprogress {
            border-color: var(--accent); color: var(--accent);
            background: var(--accent-soft);
            box-shadow: 0 0 0 4px var(--accent-soft);
        }
        .pp-node-completed {
            border-color: var(--success); color: var(--success);
            background: var(--success-soft);
        }
        .pp-rail-line {
            width: 2px; flex: 1; min-height: 32px; margin: 6px 0;
            background: var(--border-strong);
        }

        .pp-stage {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 1.2rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
            transition: border-color 0.18s ease, box-shadow 0.18s ease, transform 0.18s ease;
        }
        .pp-stage:hover { box-shadow: var(--shadow-md); transform: translateY(-1px); }
        .pp-stage-current {
            border-color: var(--accent-dim);
            background: linear-gradient(160deg, var(--accent-soft) 0%, var(--surface) 60%);
            box-shadow: var(--shadow-md);
        }
        .pp-stage-done { opacity: 0.88; }
        .pp-stage-upcoming { opacity: 0.78; }

        .pp-stage-top { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap; }
        .pp-stage-index { font-family: var(--font-mono); color: var(--text-faint); font-size: 0.72rem; letter-spacing: 0.06em; font-weight: 600; }
        .pp-badge-soft {
            font-family: var(--font-mono); font-size: 0.66rem; font-weight: 700;
            padding: 0.19rem 0.62rem; border-radius: 999px; border: 1px solid;
            background: var(--surface);
        }
        .pp-here-tag {
            font-family: var(--font-mono); font-size: 0.64rem; font-weight: 700;
            color: #fff; background: var(--accent);
            padding: 0.19rem 0.6rem; border-radius: 999px; letter-spacing: 0.04em;
        }
        .pp-stage-title { font-family: var(--font-display); font-size: 1.15rem; font-weight: 700; margin-bottom: 6px; color: var(--text-primary); }
        .pp-stage-tags { margin-bottom: 0.9rem; }
        .pp-tag {
            display: inline-block; font-size: 0.74rem; color: var(--text-muted); font-weight: 500;
            background: var(--surface-sunken); border: 1px solid var(--border);
            border-radius: 6px; padding: 0.18rem 0.55rem; margin-right: 6px;
        }
        .pp-stage-block { margin-bottom: 0.7rem; }
        .pp-stage-block-label {
            font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.07em;
            color: var(--text-faint); margin-bottom: 0.4rem; font-weight: 700;
        }
        .pp-chip-prereq { border-color: var(--accent-dim); color: var(--text-secondary); }
        </style>
        """,
        unsafe_allow_html=True,
    )

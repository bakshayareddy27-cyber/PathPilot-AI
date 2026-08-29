"""
PathPilot AI — Streamlit Application

Frontend/UI layer only.
Core backend logic and data flow are preserved.
"""

import json
import html
import streamlit as st

from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine
from core.adaptive_engine import AdaptiveEngine, AdaptationState
from core.ai_assistant import AIAssistant

from ui.dashboard import render_dashboard
from ui.roadmap import render_roadmap


# ==============================================================
# PAGE CONFIG
# ==============================================================

st.set_page_config(
    page_title="PathPilot AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================
# DESIGN SYSTEM
# ==============================================================

st.markdown(
    """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

    <link
        href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap"
        rel="stylesheet"
    >

    <style>

    /* =========================================================
       1. DESIGN TOKENS
    ========================================================= */

    :root {
        --bg: #090d17;
        --bg-deep: #070a12;

        --surface: #101622;
        --surface-raised: #151c2b;
        --surface-hover: #192235;
        --surface-soft: #111827;

        --border: rgba(255, 255, 255, 0.07);
        --border-strong: rgba(255, 255, 255, 0.13);

        --primary: #6d72ff;
        --primary-soft: rgba(109, 114, 255, 0.12);

        --violet: #9b6dff;
        --cyan: #42d9f5;

        --success: #39d98a;
        --success-soft: rgba(57, 217, 138, 0.10);

        --warning: #f6bd45;
        --warning-soft: rgba(246, 189, 69, 0.10);

        --danger: #f07178;
        --danger-soft: rgba(240, 113, 120, 0.10);

        --text-primary: #f5f7fb;
        --text-secondary: #b7c0d0;
        --text-muted: #7f8a9e;
        --text-faint: #596378;

        --font-display: "Plus Jakarta Sans", sans-serif;
        --font-body: "Inter", sans-serif;
        --font-mono: "DM Mono", monospace;

        --radius-sm: 8px;
        --radius-md: 14px;
        --radius-lg: 20px;
        --radius-xl: 26px;

        --shadow-card: 0 10px 40px rgba(0, 0, 0, 0.18);
    }


    /* =========================================================
       2. GLOBAL STYLES
    ========================================================= */

    html,
    body,
    .stApp {
        font-family: var(--font-body);
        color: var(--text-primary);
    }

    .stApp {
        background:
            radial-gradient(
                circle at 12% 0%,
                rgba(109, 114, 255, 0.11),
                transparent 32%
            ),
            radial-gradient(
                circle at 88% 10%,
                rgba(66, 217, 245, 0.05),
                transparent 28%
            ),
            var(--bg);
        background-attachment: fixed;
    }

    h1,
    h2,
    h3,
    h4 {
        font-family: var(--font-display) !important;
        letter-spacing: -0.025em;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    hr {
        border-color: var(--border);
    }

    ::selection {
        background: rgba(109, 114, 255, 0.35);
    }


    /* =========================================================
       3. APP SHELL
    ========================================================= */

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    .pp-page-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding-bottom: 1.8rem;
        margin-bottom: 2rem;

        border-bottom: 1px solid var(--border);

        gap: 1.5rem;
        flex-wrap: wrap;
    }

    .pp-page-title {
        margin: 0;
        font-size: 1.75rem;
        font-weight: 700;
    }

    .pp-page-subtitle {
        margin-top: 0.45rem;
        color: var(--text-muted);
        font-size: 0.92rem;
        max-width: 620px;
        line-height: 1.6;
    }

    .pp-status-chip {
        min-width: 170px;

        background: rgba(21, 28, 43, 0.8);
        border: 1px solid var(--border);

        border-radius: var(--radius-md);

        padding: 1rem 1.2rem;
    }

    .pp-status-label {
        color: var(--text-faint);

        font-size: 0.68rem;
        font-weight: 600;

        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .pp-status-value {
        margin-top: 0.3rem;

        font-family: var(--font-display);
        font-size: 1.15rem;
        font-weight: 700;
    }

    .pp-status-score {
        margin-top: 0.25rem;

        font-family: var(--font-mono);
        color: var(--text-muted);

        font-size: 0.76rem;
    }


    /* =========================================================
       4. SIDEBAR
    ========================================================= */

    section[data-testid="stSidebar"] {
        background: #0c111c;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.6rem;
    }

    .pp-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .pp-brand-mark {
        width: 36px;
        height: 36px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 11px;

        background:
            linear-gradient(
                135deg,
                var(--primary),
                var(--violet)
            );

        color: white;

        font-size: 1rem;
        font-weight: 700;

        box-shadow:
            0 8px 25px
            rgba(109, 114, 255, 0.28);
    }

    .pp-brand-name {
        font-family: var(--font-display);
        font-size: 1.05rem;
        font-weight: 700;
    }

    .pp-brand-sub {
        margin:
            0.3rem
            0
            1.8rem
            3rem;

        color: var(--text-faint);

        font-size: 0.62rem;
        font-weight: 600;

        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 0.2rem;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label {
        padding: 0.7rem 0.85rem !important;

        border-radius: 9px;

        transition:
            background 0.2s ease,
            color 0.2s ease;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:hover {
        background: rgba(255, 255, 255, 0.035);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:has(input:checked) {
        background: var(--primary-soft);
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label p {
        color: var(--text-muted);
        font-size: 0.88rem;
        font-weight: 500;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:has(input:checked) p {
        color: var(--text-primary);
    }

    .pp-user-card {
        margin-top: 1.5rem;
        padding-top: 1.2rem;

        border-top: 1px solid var(--border);
    }

    .pp-user-name {
        font-size: 0.9rem;
        font-weight: 600;
    }

    .pp-user-role {
        margin-top: 0.2rem;

        color: var(--text-faint);
        font-size: 0.75rem;
    }


    /* =========================================================
       5. TYPOGRAPHY
    ========================================================= */

    .pp-eyebrow {
        margin-bottom: 0.45rem;

        color: var(--cyan);

        font-size: 0.68rem;
        font-weight: 700;

        letter-spacing: 0.13em;
        text-transform: uppercase;
    }

    .pp-section-title {
        margin:
            0
            0
            0.4rem
            0;

        font-size: 1.55rem;
        font-weight: 700;
    }

    .pp-section-description {
        margin: 0 0 1.7rem 0;

        color: var(--text-muted);

        font-size: 0.9rem;
        line-height: 1.6;
    }


    /* =========================================================
       6. BUTTONS
    ========================================================= */

    .stButton > button {
        min-height: 42px;

        background: var(--surface-raised);
        color: var(--text-primary);

        border: 1px solid var(--border-strong);
        border-radius: 10px;

        font-family: var(--font-body);
        font-weight: 600;

        transition:
            transform 0.18s ease,
            border-color 0.18s ease,
            background 0.18s ease;
    }

    .stButton > button:hover {
        background: var(--surface-hover);
        border-color: rgba(109, 114, 255, 0.55);

        transform: translateY(-1px);
    }

    div[data-testid="stFormSubmitButton"] > button,
    .pp-primary-btn button {
        background:
            linear-gradient(
                135deg,
                var(--primary),
                var(--violet)
            ) !important;

        color: white !important;

        border: none !important;

        box-shadow:
            0 10px 30px
            rgba(109, 114, 255, 0.28);
    }

    div[data-testid="stFormSubmitButton"] > button:hover,
    .pp-primary-btn button:hover {
        opacity: 0.94;
    }


    /* =========================================================
       7. CARDS
    ========================================================= */

    .pp-card {
        background: rgba(21, 28, 43, 0.82);

        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        padding: 1.35rem;

        box-shadow: var(--shadow-card);
    }

    .pp-card:hover {
        border-color: var(--border-strong);
    }


    /* =========================================================
       8. LANDING PAGE
    ========================================================= */

    .pp-landing-hero {
        padding: 4rem 1rem 2.5rem;
        text-align: center;
    }

    .pp-landing-badge {
        display: inline-flex;

        padding: 0.45rem 0.9rem;

        margin-bottom: 1.2rem;

        border:
            1px solid
            rgba(66, 217, 245, 0.2);

        border-radius: 999px;

        background:
            rgba(66, 217, 245, 0.05);

        color: var(--cyan);

        font-family: var(--font-mono);
        font-size: 0.7rem;

        letter-spacing: 0.08em;
    }

    .pp-landing-hero h1 {
        margin: 0;

        font-size: 3.4rem;
        font-weight: 800;

        line-height: 1.05;

        background:
            linear-gradient(
                135deg,
                #ffffff,
                #aeb4ff
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .pp-tagline {
        margin-top: 1rem;

        color: var(--text-secondary);

        font-size: 1.1rem;
    }

    .pp-landing-description {
        max-width: 650px;

        margin:
            0
            auto
            2.5rem;

        text-align: center;

        color: var(--text-muted);

        line-height: 1.7;
    }

    .pp-feature-card {
        height: 100%;

        padding: 1.5rem;

        background:
            rgba(21, 28, 43, 0.75);

        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    .pp-feature-card:hover {
        transform: translateY(-4px);

        border-color:
            rgba(109, 114, 255, 0.4);
    }

    .pp-feature-card-title {
        font-family: var(--font-display);
        font-size: 1rem;
        font-weight: 700;
    }

    .pp-feature-card p {
        margin-top: 0.55rem;

        color: var(--text-muted);

        font-size: 0.86rem;
        line-height: 1.6;
    }


    /* =========================================================
       9. ONBOARDING
    ========================================================= */

    .pp-onboarding-header {
        margin-bottom: 2rem;
        text-align: center;
    }

    .pp-onboarding-header h2 {
        margin: 0.3rem 0;

        font-size: 1.8rem;
    }

    .pp-step-header {
        display: flex;
        align-items: center;

        gap: 0.75rem;

        margin:
            1.7rem
            0
            0.9rem;
    }

    .pp-step-num {
        width: 27px;
        height: 27px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 50%;

        background: var(--primary-soft);

        border:
            1px solid
            rgba(109, 114, 255, 0.25);

        color: var(--primary);

        font-family: var(--font-mono);
        font-size: 0.72rem;
    }

    .pp-step-title {
        font-size: 0.96rem;
        font-weight: 700;
    }


    /* =========================================================
       10. DASHBOARD
    ========================================================= */

    .pp-metric-card {
        height: 100%;

        padding: 1.2rem;

        background:
            rgba(21, 28, 43, 0.82);

        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        transition:
            transform 0.2s ease,
            border-color 0.2s ease;
    }

    .pp-metric-card:hover {
        transform: translateY(-3px);
        border-color: var(--border-strong);
    }

    .pp-metric-label {
        color: var(--text-faint);

        font-size: 0.7rem;
        font-weight: 600;

        letter-spacing: 0.06em;
        text-transform: uppercase;
    }

    .pp-metric-value {
        margin: 0.4rem 0;

        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 700;
    }

    .pp-metric-desc {
        color: var(--text-muted);
        font-size: 0.76rem;
    }

    .trend-good {
        color: var(--success);
    }

    .trend-warn {
        color: var(--warning);
    }

    .trend-bad {
        color: var(--danger);
    }

    .trend-neutral {
        color: var(--text-muted);
    }

    .pp-dashboard-list-item {
        display: flex;
        justify-content: space-between;
        align-items: center;

        padding: 0.8rem 0;

        border-bottom: 1px solid var(--border);
    }

    .pp-dashboard-list-item:last-child {
        border-bottom: none;
    }

    .pp-dashboard-skill {
        color: var(--text-secondary);
        font-size: 0.88rem;
    }

    .pp-dashboard-priority {
        padding: 0.25rem 0.55rem;

        border-radius: 999px;

        background: var(--primary-soft);

        color: #aeb4ff;

        font-family: var(--font-mono);
        font-size: 0.67rem;
    }


    /* =========================================================
       11. NEXT BEST ACTION
    ========================================================= */

    .pp-nba-card {
        padding: 2rem;

        background:
            linear-gradient(
                145deg,
                rgba(25, 32, 55, 0.95),
                rgba(17, 22, 37, 0.95)
            );

        border:
            1px solid
            rgba(109, 114, 255, 0.28);

        border-radius: var(--radius-lg);

        box-shadow:
            0 20px 60px
            rgba(0, 0, 0, 0.2);
    }

    .pp-nba-eyebrow {
        margin-bottom: 0.5rem;

        color: var(--cyan);

        font-family: var(--font-mono);
        font-size: 0.7rem;

        letter-spacing: 0.12em;
        text-transform: uppercase;
    }

    .pp-nba-skill {
        margin-bottom: 1.5rem;

        font-family: var(--font-display);
        font-size: 2rem;
        font-weight: 700;
    }

    .pp-nba-stats {
        display: flex;

        gap: 2.5rem;
        flex-wrap: wrap;
    }

    .pp-nba-stat-label {
        color: var(--text-faint);

        font-size: 0.68rem;

        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .pp-nba-stat-value {
        margin-top: 0.3rem;

        font-family: var(--font-display);
        font-size: 1.1rem;
        font-weight: 700;
    }

    .pp-nba-why {
        margin-top: 1.6rem;
        padding-top: 1.3rem;

        border-top: 1px solid var(--border);
    }

    .pp-insight-row {
        display: flex;

        align-items: flex-start;

        gap: 0.7rem;

        padding: 0.4rem 0;
    }

    .pp-insight-check {
        color: var(--success);
        font-weight: 700;
    }

    .pp-insight-text {
        color: var(--text-secondary);

        font-size: 0.88rem;
        line-height: 1.55;
    }

    .pp-score-row {
        margin-bottom: 1rem;
    }

    .pp-score-top {
        display: flex;
        justify-content: space-between;

        margin-bottom: 0.4rem;
    }

    .pp-score-name {
        color: var(--text-muted);
        font-size: 0.82rem;
    }

    .pp-score-num {
        font-family: var(--font-mono);
        font-size: 0.76rem;
    }

    .pp-score-track {
        height: 6px;

        overflow: hidden;

        background: var(--surface-soft);

        border-radius: 99px;
    }

    .pp-score-fill {
        height: 100%;

        background:
            linear-gradient(
                90deg,
                var(--primary),
                var(--cyan)
            );

        border-radius: 99px;
    }


    /* =========================================================
       12. ROADMAP
    ========================================================= */

    .pp-roadmap-overview {
        padding: 1.5rem;

        background:
            linear-gradient(
                145deg,
                rgba(25, 32, 55, 0.9),
                rgba(17, 22, 37, 0.9)
            );

        border:
            1px solid
            rgba(109, 114, 255, 0.2);

        border-radius: var(--radius-lg);
    }

    .pp-roadmap-overview-top {
        display: flex;
        justify-content: space-between;
        align-items: center;

        gap: 1rem;
    }

    .pp-roadmap-overview-label {
        color: var(--text-faint);

        font-size: 0.68rem;
        font-weight: 700;

        letter-spacing: 0.1em;
    }

    .pp-roadmap-overview-value {
        margin-top: 0.45rem;

        font-family: var(--font-display);
        font-size: 1.3rem;
        font-weight: 700;
    }

    .pp-roadmap-overview-value span {
        margin-left: 0.3rem;

        color: var(--text-muted);

        font-family: var(--font-body);
        font-size: 0.82rem;
        font-weight: 400;
    }

    .pp-roadmap-percent {
        color: var(--cyan);

        font-family: var(--font-mono);
        font-size: 1.2rem;
    }

    .pp-roadmap-progress-track {
        height: 7px;

        overflow: hidden;

        margin-top: 1.2rem;

        background: var(--surface-soft);

        border-radius: 99px;
    }

    .pp-roadmap-progress-fill {
        height: 100%;

        background:
            linear-gradient(
                90deg,
                var(--primary),
                var(--cyan)
            );

        border-radius: 99px;

        transition: width 0.4s ease;
    }

    .pp-roadmap-timeline {
        display: flex;
        flex-direction: column;
        align-items: center;

        height: 100%;
    }

    .pp-roadmap-dot {
        width: 30px;
        height: 30px;

        display: flex;
        align-items: center;
        justify-content: center;

        flex-shrink: 0;

        border-radius: 50%;

        background: var(--surface-raised);

        border:
            2px solid
            var(--text-faint);

        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.75rem;
    }

    .roadmap-in-progress {
        background: var(--primary-soft);

        border-color: var(--primary);

        color: var(--primary);
    }

    .roadmap-completed {
        background: var(--success-soft);

        border-color: var(--success);

        color: var(--success);
    }

    .roadmap-not-started {
        border-color: var(--text-faint);
        color: var(--text-faint);
    }

    .pp-roadmap-timeline-line {
        width: 2px;

        min-height: 90px;
        flex-grow: 1;

        margin: 5px 0;

        background:
            linear-gradient(
                var(--border-strong),
                rgba(255,255,255,0.03)
            );
    }

    .pp-roadmap-step-card {
        padding: 1.25rem;

        background:
            rgba(21, 28, 43, 0.78);

        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        transition:
            border-color 0.2s ease,
            transform 0.2s ease;
    }

    .pp-roadmap-step-card:hover {
        border-color: var(--border-strong);
        transform: translateY(-2px);
    }

    .pp-roadmap-step-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;

        gap: 1rem;
    }

    .pp-roadmap-step-number {
        margin-bottom: 0.35rem;

        color: var(--text-faint);

        font-family: var(--font-mono);
        font-size: 0.68rem;

        letter-spacing: 0.08em;
    }

    .pp-step-skill {
        font-family: var(--font-display);
        font-size: 1.08rem;
        font-weight: 700;
    }

    .pp-roadmap-status-badge {
        padding: 0.35rem 0.65rem;

        border-radius: 999px;

        font-family: var(--font-mono);
        font-size: 0.65rem;

        white-space: nowrap;
    }

    .pp-roadmap-status-badge.roadmap-in-progress {
        background: var(--primary-soft);
        color: #aeb4ff;
    }

    .pp-roadmap-status-badge.roadmap-completed {
        background: var(--success-soft);
        color: var(--success);
    }

    .pp-roadmap-status-badge.roadmap-not-started {
        background: rgba(255,255,255,0.04);
        color: var(--text-muted);
    }

    .pp-roadmap-meta {
        display: flex;

        gap: 0.55rem;

        margin-top: 0.8rem;

        color: var(--text-faint);

        font-size: 0.78rem;
    }

    .pp-roadmap-meta b {
        color: var(--text-secondary);
        font-weight: 500;
    }

    .pp-roadmap-detail {
        padding:
            0.9rem
            0.2rem;
    }

    .pp-roadmap-detail-label {
        margin-bottom: 0.35rem;

        color: var(--text-faint);

        font-size: 0.64rem;
        font-weight: 700;

        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .pp-roadmap-detail-text {
        color: var(--text-muted);

        font-size: 0.83rem;
        line-height: 1.5;
    }

    .pp-roadmap-resources {
        margin-bottom: 0.9rem;
    }

    .pp-resource-list {
        display: flex;
        flex-wrap: wrap;

        gap: 0.5rem;
    }

    .pp-resource-chip {
        display: inline-flex;

        padding: 0.42rem 0.7rem;

        background:
            rgba(109, 114, 255, 0.07);

        border:
            1px solid
            rgba(109, 114, 255, 0.16);

        border-radius: 999px;

        color: var(--text-secondary);

        font-size: 0.73rem;

        text-decoration: none;

        transition:
            background 0.2s ease,
            border-color 0.2s ease;
    }

    .pp-resource-chip:hover {
        background: var(--primary-soft);

        border-color:
            rgba(109, 114, 255, 0.4);

        color: white;
    }

    .pp-summary-card {
        padding: 1.2rem;

        background: var(--surface-raised);

        border: 1px solid var(--border);
        border-radius: var(--radius-md);

        text-align: center;
    }

    .pp-summary-value {
        font-family: var(--font-display);
        font-size: 1.6rem;
        font-weight: 700;
    }

    .pp-summary-label {
        margin-top: 0.3rem;

        color: var(--text-faint);

        font-size: 0.64rem;
        font-weight: 700;

        letter-spacing: 0.08em;
    }


    /* =========================================================
       13. PATH HEALTH
    ========================================================= */

    .pp-health-score-card {
        padding: 1.5rem;

        background: var(--surface-raised);

        border: 1px solid var(--border);
        border-radius: var(--radius-lg);

        text-align: center;
    }

    .pp-badge {
        display: inline-block;

        padding: 0.35rem 0.75rem;

        border-radius: 999px;

        font-family: var(--font-mono);
        font-size: 0.68rem;
        font-weight: 500;
    }

    .badge-healthy {
        background: var(--success-soft);
        color: var(--success);

        border:
            1px solid
            rgba(57, 217, 138, 0.22);
    }

    .badge-atrisk {
        background: var(--warning-soft);
        color: var(--warning);

        border:
            1px solid
            rgba(246, 189, 69, 0.22);
    }

    .badge-critical {
        background: var(--danger-soft);
        color: var(--danger);

        border:
            1px solid
            rgba(240, 113, 120, 0.22);
    }

    .pp-risk-card {
        position: relative;

        margin-bottom: 0.8rem;
        padding: 1.1rem 1.2rem;

        background: rgba(21, 28, 43, 0.8);

        border: 1px solid var(--border);
        border-left: 3px solid var(--text-muted);

        border-radius: 12px;
    }

    .pp-risk-high {
        border-left-color: var(--danger);
    }

    .pp-risk-medium {
        border-left-color: var(--warning);
    }

    .pp-risk-low {
        border-left-color: var(--cyan);
    }

    .pp-risk-severity {
        margin-bottom: 0.35rem;

        font-size: 0.64rem;
        font-weight: 700;

        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .pp-risk-high .pp-risk-severity {
        color: var(--danger);
    }

    .pp-risk-medium .pp-risk-severity {
        color: var(--warning);
    }

    .pp-risk-low .pp-risk-severity {
        color: var(--cyan);
    }

    .pp-risk-title {
        font-family: var(--font-display);
        font-size: 0.96rem;
        font-weight: 700;
    }

    .pp-risk-msg {
        margin-top: 0.4rem;

        color: var(--text-muted);

        font-size: 0.84rem;
        line-height: 1.55;
    }

    .pp-risk-action {
        margin-top: 0.7rem;

        color: var(--text-secondary);

        font-size: 0.78rem;
    }


    /* =========================================================
       14. AI ASSISTANT
    ========================================================= */

    .pp-assistant-intro {
        padding: 1.6rem;

        margin-bottom: 1.2rem;

        background:
            linear-gradient(
                145deg,
                rgba(25, 32, 55, 0.9),
                rgba(17, 22, 37, 0.9)
            );

        border:
            1px solid
            rgba(155, 109, 255, 0.22);

        border-radius: var(--radius-lg);
    }

    .pp-assistant-title {
        margin-bottom: 0.4rem;

        font-family: var(--font-display);
        font-size: 1.3rem;
        font-weight: 700;
    }

    .pp-assistant-subtitle {
        color: var(--text-muted);

        font-size: 0.88rem;
        line-height: 1.6;
    }

    .pp-assistant-answer {
        margin-top: 1rem;
        padding: 1.4rem;

        background:
            rgba(21, 28, 43, 0.9);

        border:
            1px solid
            rgba(109, 114, 255, 0.2);

        border-radius: var(--radius-lg);

        line-height: 1.7;
    }

    .pp-answer-label {
        margin-bottom: 0.6rem;

        color: var(--cyan);

        font-family: var(--font-mono);
        font-size: 0.68rem;

        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .pp-answer-text {
        color: var(--text-secondary);

        font-size: 0.9rem;
        line-height: 1.7;
    }


    /* =========================================================
       15. RESPONSIVE ADJUSTMENTS
    ========================================================= */

    @media (max-width: 768px) {

        .block-container {
            padding-top: 1.5rem;
        }

        .pp-landing-hero {
            padding-top: 2.5rem;
        }

        .pp-landing-hero h1 {
            font-size: 2.5rem;
        }

        .pp-page-header {
            align-items: flex-start;
            flex-direction: column;
        }

        .pp-status-chip {
            width: 100%;
        }

        .pp-nba-skill {
            font-size: 1.55rem;
        }

        .pp-nba-stats {
            gap: 1.3rem;
        }

        .pp-roadmap-overview-top {
            align-items: flex-start;
            flex-direction: column;
        }

        .pp-roadmap-meta {
            flex-wrap: wrap;
        }

        .pp-roadmap-timeline-line {
            min-height: 70px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================
# SESSION STATE
# ==============================================================

def init_session_state():

    defaults = {
        "stage": "welcome",
        "profile": None,
        "engine_output": None,
        "adaptation_state": AdaptationState(),
        "roadmap_progress": {},
        "nav_section": "Overview",
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# ==============================================================
# BACKEND INITIALIZATION
# ==============================================================

@st.cache_resource
def get_engine():

    try:
        return IntelligenceEngine()

    except Exception as error:
        st.error(
            f"Failed to load intelligence engine: {error}"
        )
        return None


@st.cache_resource
def get_assistant():

    return AIAssistant()


engine = get_engine()
assistant = get_assistant()

adaptive_engine = (
    AdaptiveEngine(engine)
    if engine
    else None
)


# ==============================================================
# SAFE CALL
# ==============================================================

def safe_call(function, *args, **kwargs):

    if function is None:
        return None

    try:
        return function(*args, **kwargs)

    except Exception as error:

        st.warning(
            f"A calculation step had an issue: {error}"
        )

        return None


# ==============================================================
# CAREER OPTIONS
# ==============================================================

def get_career_options():

    try:

        with open(
            "data/career_paths.json",
            "r"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return list(data.keys())

        if isinstance(data, list):

            return [
                item.get("career_goal")
                or item.get("name")

                for item in data

                if isinstance(item, dict)
            ]

    except Exception:
        pass

    return [
        "Machine Learning Engineer",
        "Data Scientist",
        "Full Stack Web Developer",
        "Cybersecurity Analyst",
    ]


# ==============================================================
# ENGINE PIPELINE
# ==============================================================

def run_engine_pipeline(profile):

    output = {
        "skill_gap":
            safe_call(
                engine.analyze_skill_gap,
                profile,
            ),

        "readiness":
            safe_call(
                engine.calculate_readiness_score,
                profile,
            ),

        "next_best_action":
            safe_call(
                engine.calculate_next_best_action,
                profile,
            ),

        "risks":
            safe_call(
                engine.detect_risks,
                profile,
            )
            or [],

        "path_health":
            safe_call(
                engine.calculate_path_health,
                profile,
            ),

        "roadmap":
            safe_call(
                engine.generate_roadmap,
                profile,
            )
            or [],
    }

    st.session_state.engine_output = output

    return output


# ==============================================================
# STATUS HELPERS
# ==============================================================

def status_badge_class(status):

    return {
        "Healthy": "badge-healthy",
        "At Risk": "badge-atrisk",
        "Critical": "badge-critical",
    }.get(
        status,
        "badge-atrisk",
    )


def clean(value):

    return html.escape(
        str(value)
    )


# ==============================================================
# WELCOME PAGE
# ==============================================================

def render_welcome():

    st.markdown(
        """
        <div class="pp-landing-hero">

            <div class="pp-landing-badge">
                ◈ AI LEARNING INTELLIGENCE
            </div>

            <h1>PathPilot AI</h1>

            <p class="pp-tagline">
                Don't just recommend what to learn.
                Decide what to learn next.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pp-landing-description">

            PathPilot analyzes your skills, career goals,
            prerequisites, available time and experience level
            to determine the most valuable next step in your
            learning journey.

        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="pp-feature-card">

                <div class="pp-eyebrow">
                    01 · DECIDE
                </div>

                <div class="pp-feature-card-title">
                    Next Best Action
                </div>

                <p>
                    One prioritized learning decision instead
                    of an overwhelming list of recommendations.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="pp-feature-card">

                <div class="pp-eyebrow">
                    02 · VALIDATE
                </div>

                <div class="pp-feature-card-title">
                    Prerequisite Intelligence
                </div>

                <p>
                    Detect learning blockers before recommending
                    unrealistic jumps in your roadmap.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
            """
            <div class="pp-feature-card">

                <div class="pp-eyebrow">
                    03 · MONITOR
                </div>

                <div class="pp-feature-card-title">
                    Path Health
                </div>

                <p>
                    Monitor whether your learning journey is
                    healthy, at risk or needs attention.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    _, center, _ = st.columns([1, 1, 1])

    with center:

        st.markdown(
            '<div class="pp-primary-btn">',
            unsafe_allow_html=True,
        )

        clicked = st.button(
            "Build My Learning Path →",
            use_container_width=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    if clicked:

        st.session_state.stage = "profiling"

        st.rerun()


# ==============================================================
# PROFILING
# ==============================================================

def render_profiling():

    st.markdown(
        """
        <div class="pp-onboarding-header">

            <div class="pp-eyebrow">
                ONBOARDING
            </div>

            <h2>
                Let's build your path
            </h2>

            <p style="color:var(--text-muted);">
                Three quick steps.
                Every answer improves your recommendations.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

    career_options = get_career_options()

    with st.form("profiling_form"):

        st.markdown(
            """
            <div class="pp-step-header">

                <div class="pp-step-num">
                    1
                </div>

                <div class="pp-step-title">
                    Who are you?
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        name = st.text_input(
            "Name",
            placeholder="e.g. Akshaya Reddy",
        )

        career_goal = st.selectbox(
            "Career Goal",
            options=career_options,
        )

        natural_language_goal = st.text_area(
            "In your own words, what do you want to achieve?",
            placeholder=(
                "e.g. I want to become an ML engineer "
                "within 6 months and land an internship."
            ),
        )

        st.markdown(
            """
            <div class="pp-step-header">

                <div class="pp-step-num">
                    2
                </div>

                <div class="pp-step-title">
                    Where are you now?
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        experience_level_label = st.select_slider(
            "Experience Level",
            options=[
                "Beginner",
                "Intermediate",
                "Advanced",
            ],
            value="Beginner",
        )

        experience_map = {
            "Beginner": 1,
            "Intermediate": 3,
            "Advanced": 5,
        }

        current_skills_raw = st.text_input(
            "Current Skills (comma-separated)",
            placeholder="e.g. Python Basics, SQL, Git",
        )

        interests_raw = st.text_input(
            "Interests (comma-separated)",
            placeholder="e.g. AI, Data, Web Development",
        )

        st.markdown(
            """
            <div class="pp-step-header">

                <div class="pp-step-num">
                    3
                </div>

                <div class="pp-step-title">
                    Your learning constraints
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:

            weekly_hours = st.number_input(
                "Weekly Learning Hours",
                min_value=1,
                max_value=80,
                value=10,
            )

        with col2:

            timeline_weeks = st.number_input(
                "Target Timeline (weeks)",
                min_value=1,
                max_value=104,
                value=24,
            )

        preferred_learning_style = st.selectbox(
            "Preferred Learning Style",
            options=[
                "visual",
                "reading",
                "hands-on",
                "video",
                "mixed",
            ],
        )

        st.write("")

        submitted = st.form_submit_button(
            "Generate My Learning Path →"
        )

    if submitted:

        if not name.strip():

            st.error(
                "Please enter your name."
            )

            return

        current_skills = [
            skill.strip()

            for skill in current_skills_raw.split(",")

            if skill.strip()
        ]

        interests = [
            interest.strip()

            for interest in interests_raw.split(",")

            if interest.strip()
        ]

        try:

            profile = LearnerProfile(
                name=name.strip(),
                career_goal=career_goal,
                natural_language_goal=natural_language_goal.strip(),
                experience_level=experience_map[
                    experience_level_label
                ],
                current_skills=current_skills,
                interests=interests,
                completed_courses=[],
                weekly_hours=int(weekly_hours),
                timeline_weeks=int(timeline_weeks),
                preferred_learning_style=preferred_learning_style,
            )

        except Exception as error:

            st.error(
                f"Could not build your profile: {error}"
            )

            return

        st.session_state.profile = profile

        if engine is None:

            st.error(
                "Intelligence engine is unavailable. "
                "Please check your backend data files."
            )

            return

        with st.spinner(
            "Analyzing your learning profile..."
        ):

            run_engine_pipeline(profile)

        st.session_state.stage = "app"

        st.rerun()

    if st.button("← Back"):

        st.session_state.stage = "welcome"

        st.rerun()


# ==============================================================
# NEXT BEST ACTION
# ==============================================================

def render_next_best_action():

    st.markdown(
        """
        <div class="pp-eyebrow">
            DECISION ENGINE
        </div>

        <h2 class="pp-section-title">
            Next Best Action
        </h2>

        <p class="pp-section-description">
            The highest-value learning step for your current path.
        </p>
        """,
        unsafe_allow_html=True,
    )

    engine_output = (
        st.session_state.engine_output
        or {}
    )

    nba = engine_output.get(
        "next_best_action"
    )

    if not nba:

        st.markdown(
            """
            <div class="pp-card">
                You're caught up — there is no additional
                recommendation right now for your current goal.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    reasons = nba.get(
        "reasons",
        [],
    )

    reasons_html = ""

    for reason in reasons:

        reasons_html += f"""
        <div class="pp-insight-row">

            <span class="pp-insight-check">
                ✓
            </span>

            <span class="pp-insight-text">
                {clean(reason)}
            </span>

        </div>
        """

    if not reasons_html:

        reasons_html = """
        <div class="pp-insight-text">
            No additional reasoning was provided.
        </div>
        """

    st.markdown(
        f"""
        <div class="pp-nba-card">

            <div class="pp-nba-eyebrow">
                PathPilot Recommends
            </div>

            <div class="pp-nba-skill">
                {clean(nba.get("skill", "N/A"))}
            </div>

            <div class="pp-nba-stats">

                <div>
                    <div class="pp-nba-stat-label">
                        Confidence Score
                    </div>

                    <div class="pp-nba-stat-value">
                        {clean(nba.get("score", "N/A"))}
                    </div>
                </div>

                <div>
                    <div class="pp-nba-stat-label">
                        Estimated Time
                    </div>

                    <div class="pp-nba-stat-value">
                        {clean(nba.get("est_hours", "N/A"))} hrs
                    </div>
                </div>

                <div>
                    <div class="pp-nba-stat-label">
                        Difficulty
                    </div>

                    <div class="pp-nba-stat-value">
                        {clean(nba.get("difficulty", "N/A"))}
                    </div>
                </div>

            </div>

            <div class="pp-nba-why">

                <div class="pp-eyebrow">
                    Why this?
                </div>

                {reasons_html}

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    breakdown = nba.get(
        "score_breakdown",
        {},
    )

    if breakdown:

        st.write("")

        st.markdown(
            '<div class="pp-card">',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="pp-eyebrow">SCORE BREAKDOWN</div>',
            unsafe_allow_html=True,
        )

        rows_html = ""

        for factor, value in breakdown.items():

            try:
                percentage = max(
                    0,
                    min(
                        100,
                        float(value),
                    ),
                )

            except (
                TypeError,
                ValueError,
            ):
                percentage = 0

            factor_name = (
                str(factor)
                .replace("_", " ")
                .title()
            )

            rows_html += f"""
            <div class="pp-score-row">

                <div class="pp-score-top">

                    <span class="pp-score-name">
                        {clean(factor_name)}
                    </span>

                    <span class="pp-score-num">
                        {clean(value)}
                    </span>

                </div>

                <div class="pp-score-track">

                    <div
                        class="pp-score-fill"
                        style="width:{percentage}%;">
                    </div>

                </div>

            </div>
            """

        st.markdown(
            rows_html,
            unsafe_allow_html=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    render_adaptive_feedback(nba)


# ==============================================================
# ADAPTIVE FEEDBACK
# ==============================================================

def render_adaptive_feedback(nba):

    st.markdown(
        """
        <p style="
            color:var(--text-muted);
            font-size:0.86rem;
            margin-top:1.5rem;
        ">
            How does this recommendation feel for you?
        </p>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    skill_name = nba.get("skill")

    feedback_clicked = None

    with col1:

        if st.button(
            "Too Easy",
            use_container_width=True,
        ):

            feedback_clicked = "too_easy"

    with col2:

        if st.button(
            "Appropriate",
            use_container_width=True,
        ):

            feedback_clicked = "appropriate"

    with col3:

        if st.button(
            "Too Difficult",
            use_container_width=True,
        ):

            feedback_clicked = "too_difficult"

    if (
        feedback_clicked
        and adaptive_engine
        and skill_name
    ):

        with st.spinner(
            "Adapting your learning path..."
        ):

            result = safe_call(
                adaptive_engine.apply_feedback,
                st.session_state.profile,
                skill_name,
                feedback_clicked,
                st.session_state.adaptation_state,
            )

        if result:

            st.success(
                "Your learning path has been adapted."
            )

            message = result.get(
                "adaptation_message",
                "",
            )

            if message:
                st.info(message)

            if result.get("root_blockers"):

                blockers = ", ".join(
                    result["root_blockers"]
                )

                st.warning(
                    f"Root blockers identified: {blockers}"
                )

            engine_output = (
                st.session_state.engine_output
                or {}
            )

            if result.get(
                "updated_recommendation"
            ) is not None:

                engine_output[
                    "next_best_action"
                ] = result[
                    "updated_recommendation"
                ]

            if result.get(
                "updated_path_health"
            ) is not None:

                engine_output[
                    "path_health"
                ] = result[
                    "updated_path_health"
                ]

            if result.get(
                "updated_risks"
            ) is not None:

                engine_output[
                    "risks"
                ] = result[
                    "updated_risks"
                ]

            st.session_state.engine_output = (
                engine_output
            )

            st.rerun()


# ==============================================================
# AI ASSISTANT
# ==============================================================

def render_ai_assistant():

    st.markdown(
        """
        <div class="pp-eyebrow">
            ASK PATHPILOT
        </div>

        <h2 class="pp-section-title">
            Learning Intelligence
        </h2>

        <div class="pp-assistant-intro">

            <div class="pp-assistant-title">
                Your path, explained clearly.
            </div>

            <div class="pp-assistant-subtitle">
                Ask PathPilot why a skill is recommended,
                what is blocking your progress, or whether
                your learning path is on track.
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    profile = st.session_state.profile

    engine_output = (
        st.session_state.engine_output
        or {}
    )

    if not assistant:

        st.error(
            "AI assistant unavailable."
        )

        return

    question = st.text_input(
        "Ask PathPilot",
        placeholder=(
            "Ask something about your learning journey..."
        ),
        label_visibility="collapsed",
        key="assistant_question_input",
    )

    st.markdown(
        """
        <div class="pp-eyebrow"
             style="margin-top:1.2rem;">
            SUGGESTED QUESTIONS
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggestions = [
        "Why this skill?",
        "What's blocking me?",
        "Am I on track?",
        "What should I focus on?",
    ]

    columns = st.columns(4)

    selected_question = None

    for column, suggestion in zip(
        columns,
        suggestions,
    ):

        with column:

            if st.button(
                suggestion,
                use_container_width=True,
                key=f"assistant_{suggestion}",
            ):

                mapping = {
                    "Why this skill?":
                        "Why should I learn this skill next?",

                    "What's blocking me?":
                        "What is blocking my progress?",

                    "Am I on track?":
                        "Am I on track with my learning goal?",

                    "What should I focus on?":
                        "What should I focus on next?",
                }

                selected_question = mapping[
                    suggestion
                ]

    active_question = (
        selected_question
        or question
    )

    if active_question:

        with st.spinner(
            "PathPilot is analyzing your question..."
        ):

            answer = safe_call(
                assistant.answer_path_question,
                profile,
                engine_output,
                active_question,
            )

        st.markdown(
            f"""
            <div class="pp-assistant-answer">

                <div class="pp-answer-label">
                    PathPilot Insight
                </div>

                <div class="pp-answer-text">
                    {clean(
                        answer
                        or "I couldn't generate an answer right now."
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ==============================================================
# PATH HEALTH
# ==============================================================

def render_path_health(engine_output):

    st.markdown(
        """
        <div class="pp-eyebrow">
            DIAGNOSTICS
        </div>

        <h2 class="pp-section-title">
            Path Health
        </h2>

        <p class="pp-section-description">
            Understand what is helping or slowing down
            your learning journey.
        </p>
        """,
        unsafe_allow_html=True,
    )

    health = (
        engine_output.get("path_health")
        or {}
    )

    risks = (
        engine_output.get("risks")
        or []
    )

    if not health:

        st.markdown(
            """
            <div class="pp-card">
                Path health data is currently unavailable.
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    status = health.get(
        "status",
        "Unknown",
    )

    score = health.get(
        "health_score",
        0,
    )

    try:
        score_number = float(score)

    except (
        TypeError,
        ValueError,
    ):
        score_number = 0

    left, right = st.columns(
        [1, 1.4]
    )

    with left:

        st.markdown(
            f"""
            <div class="pp-health-score-card">

                <div class="pp-eyebrow">
                    PATH HEALTH SCORE
                </div>

                <div class="pp-metric-value"
                     style="font-size:3rem;">
                    {clean(score)}
                </div>

                <span class="pp-badge
                    {status_badge_class(status)}">
                    {clean(status)}
                </span>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.progress(
            min(
                max(
                    score_number / 100,
                    0,
                ),
                1,
            )
        )

    with right:

        st.markdown(
            """
            <div class="pp-card">

                <div class="pp-eyebrow">
                    WHAT'S AFFECTING YOUR PATH?
                </div>
            """,
            unsafe_allow_html=True,
        )

        factors = health.get(
            "contributing_factors",
            [],
        )

        if factors:

            for factor in factors:

                text = clean(factor)

                st.markdown(
                    f"""
                    <div class="pp-insight-row">

                        <span class="pp-insight-check">
                            ✓
                        </span>

                        <span class="pp-insight-text">
                            {text}
                        </span>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:

            st.markdown(
                """
                <p style="color:var(--text-muted);">
                    No contributing factors reported.
                </p>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    st.write("")

    st.markdown(
        """
        <div class="pp-eyebrow">
            DETECTED RISKS
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not risks:

        st.markdown(
            """
            <div class="pp-card">
                <div style="color:var(--success);">
                    ✓ No active risks detected.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return

    for risk in risks:

        if isinstance(risk, dict):

            severity = str(
                risk.get(
                    "severity",
                    "low",
                )
            ).lower()

            severity_class = {
                "high": "pp-risk-high",
                "medium": "pp-risk-medium",
            }.get(
                severity,
                "pp-risk-low",
            )

            title = (
                risk.get("title")
                or risk.get("type")
                or "Learning Risk"
            )

            message = risk.get(
                "message",
                "",
            )

            action = (
                risk.get("suggested_action")
                or risk.get("action")
            )

            action_html = ""

            if action:

                action_html = f"""
                <div class="pp-risk-action">

                    <b>Recommended action:</b>
                    {clean(action)}

                </div>
                """

            st.markdown(
                f"""
                <div class="pp-risk-card {severity_class}">

                    <div class="pp-risk-severity">
                        {clean(severity)} priority
                    </div>

                    <div class="pp-risk-title">
                        {clean(title)}
                    </div>

                    <div class="pp-risk-msg">
                        {clean(message)}
                    </div>

                    {action_html}

                </div>
                """,
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
                <div class="pp-risk-card">
                    {clean(risk)}
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================
# MAIN APPLICATION
# ==============================================================

def render_app():

    profile = st.session_state.profile

    engine_output = (
        st.session_state.engine_output
    )

    if (
        profile is None
        or engine_output is None
    ):

        st.warning(
            "No learner profile found. "
            "Please build your path first."
        )

        if st.button(
            "← Go to Profiling"
        ):

            st.session_state.stage = "profiling"

            st.rerun()

        return

    with st.sidebar:

        st.markdown(
            """
            <div class="pp-brand">

                <div class="pp-brand-mark">
                    ◈
                </div>

                <div class="pp-brand-name">
                    PathPilot
                </div>

            </div>

            <div class="pp-brand-sub">
                AI Learning Intelligence
            </div>
            """,
            unsafe_allow_html=True,
        )

        nav_options = [
            "Overview",
            "Next Action",
            "Learning Roadmap",
            "Path Health",
            "AI Assistant",
        ]

        current_index = (
            nav_options.index(
                st.session_state.nav_section
            )

            if st.session_state.nav_section
            in nav_options

            else 0
        )

        section = st.radio(
            "Navigate",
            nav_options,
            index=current_index,
            label_visibility="collapsed",
        )

        st.session_state.nav_section = section

        st.markdown(
            f"""
            <div class="pp-user-card">

                <div class="pp-user-name">
                    {clean(
                        getattr(
                            profile,
                            "name",
                            "Learner",
                        )
                    )}
                </div>

                <div class="pp-user-role">
                    {clean(
                        getattr(
                            profile,
                            "career_goal",
                            "N/A",
                        )
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if st.button(
            "Restart Journey",
            use_container_width=True,
        ):

            for key in [
                "stage",
                "profile",
                "engine_output",
                "adaptation_state",
                "roadmap_progress",
            ]:

                st.session_state.pop(
                    key,
                    None,
                )

            init_session_state()

            st.rerun()

    health = (
        engine_output.get("path_health")
        or {}
    )

    status = health.get(
        "status",
        "Unknown",
    )

    score = health.get(
        "health_score",
        "—",
    )

    st.markdown(
        f"""
        <div class="pp-page-header">

            <div>

                <h1 class="pp-page-title">
                    Good to see you,
                    {clean(
                        getattr(
                            profile,
                            "name",
                            "there",
                        )
                    )} 👋
                </h1>

                <div class="pp-page-subtitle">

                    Your learning path is continuously analyzed
                    based on your skills, goals, timeline and
                    progress.

                </div>

            </div>

            <div class="pp-status-chip">

                <div class="pp-status-label">
                    Path Status
                </div>

                <div class="pp-status-value">
                    {clean(status)}
                </div>

                <div class="pp-status-score">
                    {clean(score)} / 100
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    if section == "Overview":

        render_dashboard(
            profile,
            engine_output,
            safe_call,
            engine,
        )

    elif section == "Next Action":

        render_next_best_action()

    elif section == "Learning Roadmap":

        render_roadmap(
            profile,
            engine_output,
            safe_call,
        )

    elif section == "Path Health":

        render_path_health(
            engine_output
        )

    elif section == "AI Assistant":

        render_ai_assistant()


# ==============================================================
# ROUTER
# ==============================================================

stage = st.session_state.stage

if stage == "welcome":

    render_welcome()

elif stage == "profiling":

    render_profiling()

else:

    render_app()

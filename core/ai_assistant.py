"""
AIAssistant: bounded explanation layer over deterministic IntelligenceEngine
output. Never makes recommendations. Uses Groq if GROQ_API_KEY is set;
otherwise falls back to deterministic templated explanations.
"""

import os
from typing import Any, Dict, List, Optional


GROQ_MODEL = "llama-3.3-70b-versatile"

ON_TOPIC_KEYWORDS = (
    "skill", "path", "roadmap", "recommend", "next", "prerequisite",
    "blocker", "risk", "readiness", "health", "course", "milestone",
    "goal", "progress", "learn", "difficulty", "hour", "time",
)


class AIAssistant:
    def __init__(self, api_key: Optional[str] = None, model: str = GROQ_MODEL):
        self.model = model
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.client = None
        self.enabled = False

        if self.api_key:
            try:
                from groq import Groq  # type: ignore
                self.client = Groq(api_key=self.api_key)
                self.enabled = True
            except Exception:
                self.client = None
                self.enabled = False

    # ------------------------------------------------------------------
    # 1. Explain Next Best Action
    # ------------------------------------------------------------------
    def explain_next_best_action(self, profile, nba: Optional[Dict[str, Any]]) -> str:
        if not nba:
            return (
                "There's no immediate next-step recommendation right now — "
                "you may be caught up on your current path."
            )

        ctx = {
            "name": getattr(profile, "name", "there"),
            "career_goal": getattr(profile, "career_goal", "your goal"),
            "experience_level": getattr(profile, "experience_level", None),
            "weekly_hours": getattr(profile, "weekly_hours", None),
            "skill": nba.get("skill"),
            "score": nba.get("score"),
            "score_breakdown": nba.get("score_breakdown", {}),
            "reasons": nba.get("reasons", []),
            "est_hours": nba.get("est_hours"),
            "difficulty": nba.get("difficulty"),
        }

        if self.enabled:
            try:
                return self._groq_chat(
                    system_prompt=(
                        "You are PathPilot AI's explanation layer. You NEVER invent "
                        "skills, scores, or reasons — you only explain the deterministic "
                        "data given below in 3-5 warm, concise sentences. Cover: why this "
                        "skill, how it relates to the career goal, and why it fits their "
                        "current level/time."
                    ),
                    user_prompt=(
                        f"Learner: {ctx['name']}, goal: {ctx['career_goal']}, "
                        f"experience_level: {ctx['experience_level']}, "
                        f"weekly_hours: {ctx['weekly_hours']}\n"
                        f"Recommended skill: {ctx['skill']}\n"
                        f"Score: {ctx['score']}, breakdown: {ctx['score_breakdown']}\n"
                        f"Reasons: {ctx['reasons']}\n"
                        f"Estimated hours: {ctx['est_hours']}, difficulty: {ctx['difficulty']}"
                    ),
                )
            except Exception:
                pass

        return self._fallback_nba(ctx)

    # ------------------------------------------------------------------
    # 2. Explain Path Health
    # ------------------------------------------------------------------
    def explain_path_health(
        self, profile, health: Optional[Dict[str, Any]], risks: Optional[List[Dict[str, Any]]]
    ) -> str:
        health = health or {}
        risks = risks or []
        ctx = {
            "name": getattr(profile, "name", "there"),
            "career_goal": getattr(profile, "career_goal", "your goal"),
            "health_score": health.get("health_score"),
            "status": health.get("status", "Unknown"),
            "contributing_factors": health.get("contributing_factors", []),
            "risks": risks,
        }

        if self.enabled:
            try:
                return self._groq_chat(
                    system_prompt=(
                        "You are PathPilot AI's explanation layer. You NEVER invent "
                        "risks or scores — only explain the deterministic path health "
                        "data below in 3-5 concise sentences, and suggest what the "
                        "learner should do next based strictly on the given factors/risks."
                    ),
                    user_prompt=(
                        f"Learner: {ctx['name']}, goal: {ctx['career_goal']}\n"
                        f"Health score: {ctx['health_score']}, status: {ctx['status']}\n"
                        f"Contributing factors: {ctx['contributing_factors']}\n"
                        f"Risks: {ctx['risks']}"
                    ),
                )
            except Exception:
                pass

        return self._fallback_health(ctx)

    # ------------------------------------------------------------------
    # 3. Bounded Q&A
    # ------------------------------------------------------------------
    def answer_path_question(
        self, profile, engine_output: Optional[Dict[str, Any]], question: str
    ) -> str:
        engine_output = engine_output or {}
        question = (question or "").strip()

        if not question:
            return "Ask me about your recommended skills, path health, prerequisites, or roadmap."

        if not self._is_on_topic(question):
            return (
                "PathPilot focuses on questions about your personalized learning "
                "roadmap and recommendations — try asking about your next skill, "
                "path health, or prerequisites."
            )

        ctx = {
            "name": getattr(profile, "name", "there"),
            "career_goal": getattr(profile, "career_goal", "your goal"),
            "experience_level": getattr(profile, "experience_level", None),
            "current_skills": list(getattr(profile, "current_skills", []) or []),
            "engine_output": engine_output,
        }

        if self.enabled:
            try:
                return self._groq_chat(
                    system_prompt=(
                        "You are PathPilot AI's Q&A assistant. Answer ONLY using the "
                        "engine_output JSON given as ground truth — never invent skills, "
                        "prerequisites, courses, scores, or risks not present in it. "
                        "If the question can't be answered from engine_output, say so "
                        "honestly and suggest what data would help. Keep answers to "
                        "2-4 sentences. If off-topic, redirect to the learner's roadmap."
                    ),
                    user_prompt=(
                        f"Learner: {ctx['name']}, goal: {ctx['career_goal']}, "
                        f"experience_level: {ctx['experience_level']}, "
                        f"current_skills: {ctx['current_skills']}\n"
                        f"engine_output (ground truth): {ctx['engine_output']}\n\n"
                        f"Question: {question}"
                    ),
                )
            except Exception:
                pass

        return self._fallback_question(ctx, question)

    # ==================================================================
    # Groq call
    # ==================================================================
    def _groq_chat(self, system_prompt: str, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=300,
        )
        text = response.choices[0].message.content
        if not text or not text.strip():
            raise ValueError("Empty Groq response")
        return text.strip()

    # ==================================================================
    # Deterministic fallbacks
    # ==================================================================
    def _fallback_nba(self, ctx: Dict[str, Any]) -> str:
        reasons = ctx.get("reasons") or []
        reason_text = "; ".join(str(r) for r in reasons) if reasons else \
            "it best matches your current skills and readiness"
        hours = ctx.get("est_hours")
        hours_text = f" It's estimated at about {hours} hours." if hours else ""
        score = ctx.get("score")
        score_text = f" (score: {score})" if score is not None else ""

        return (
            f"{ctx['name']}, your next recommended skill is **{ctx['skill']}**{score_text}. "
            f"This supports your goal of becoming a {ctx['career_goal']} because "
            f"{reason_text}.{hours_text}"
        )

    def _fallback_health(self, ctx: Dict[str, Any]) -> str:
        status = ctx.get("status", "Unknown")
        score = ctx.get("health_score")
        factors = ctx.get("contributing_factors") or []
        risks = ctx.get("risks") or []

        factor_text = "; ".join(str(f) for f in factors) if factors else "no major factors flagged"

        # Aligned with detect_risks()/app.py field names: severity, message, suggested_action
        risk_lines = []
        for r in risks[:3]:
            if isinstance(r, dict):
                severity = r.get("severity")
                message = r.get("message")
                if message:
                    risk_lines.append(f"[{severity}] {message}" if severity else str(message))
                else:
                    risk_lines.append(str(r))
            else:
                risk_lines.append(str(r))
        risk_text = "; ".join(risk_lines) if risk_lines else "no significant risks detected"

        advice = {
            "Healthy": "Keep going at your current pace.",
            "At Risk": "Consider adjusting your weekly hours or timeline.",
            "Critical": "Revisit your goal, timeline, or foundational skills soon.",
        }.get(status, "Review your roadmap and adjust as needed.")

        return (
            f"{ctx['name']}, your path health is **{status}** (score: {score}). "
            f"Factors: {factor_text}. Risks: {risk_text}. {advice}"
        )

    def _fallback_question(self, ctx: Dict[str, Any], question: str) -> str:
        eo = ctx.get("engine_output") or {}
        q = question.lower()

        if any(k in q for k in ("next", "recommend", "should i learn")):
            nba = eo.get("next_best_action") or eo.get("nba")
            if nba:
                return self._fallback_nba({
                    "name": ctx["name"], "career_goal": ctx["career_goal"],
                    "skill": nba.get("skill"), "reasons": nba.get("reasons", []),
                    "est_hours": nba.get("est_hours"), "score": nba.get("score"),
                })
            return "I don't have a next-step recommendation available right now."

        if any(k in q for k in ("health", "risk", "status", "on track")):
            health = eo.get("path_health") or eo.get("health")
            risks = eo.get("risks") or []
            if health:
                return self._fallback_health({
                    "name": ctx["name"], "career_goal": ctx["career_goal"],
                    "health_score": health.get("health_score"),
                    "status": health.get("status"),
                    "contributing_factors": health.get("contributing_factors", []),
                    "risks": risks,
                })
            return "I don't have path health data available right now."

        if any(k in q for k in ("prerequisite", "blocker", "before i learn")):
            prereq = eo.get("prerequisites") or eo.get("prereq_check")
            if isinstance(prereq, dict):
                blockers = prereq.get("root_blockers", [])
                if blockers:
                    return f"The foundational gaps to close first are: {', '.join(blockers)}."
                return "Your prerequisites look satisfied for that skill."
            return "I don't have prerequisite data available for that yet."

        return (
            "I can answer questions about your recommended skills, path health, "
            "prerequisites, and roadmap — try rephrasing around one of those."
        )

    @staticmethod
    def _is_on_topic(question: str) -> bool:
        q = question.lower()
        return any(k in q for k in ON_TOPIC_KEYWORDS)
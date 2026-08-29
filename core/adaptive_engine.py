"""
AdaptiveEngine: deterministic adaptation of a learner's path based on feedback.
Reruns the existing IntelligenceEngine after controlled state changes.
No LLM usage here.
"""

from typing import Any, Dict, List, Optional


class AdaptationState:
    """
    Plain, Streamlit-session-state-friendly object tracking adaptation
    decisions across a session. Does not touch the original LearnerProfile
    unless explicitly instructed.
    """

    def __init__(self):
        self.in_progress_skills: List[str] = []
        self.mastered_override_skills: List[str] = []  # "too easy" -> treat as known
        self.deprioritized_skills: List[str] = []       # "too difficult" -> skip for now
        self.feedback_history: List[Dict[str, Any]] = []

    def record(self, skill_name: str, feedback: str, adapted_action: str) -> None:
        self.feedback_history.append(
            {"skill": skill_name, "feedback": feedback, "adapted_action": adapted_action}
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "in_progress_skills": list(self.in_progress_skills),
            "mastered_override_skills": list(self.mastered_override_skills),
            "deprioritized_skills": list(self.deprioritized_skills),
            "feedback_history": list(self.feedback_history),
        }


class AdaptiveEngine:
    """
    Wraps an existing IntelligenceEngine instance. Adapts learner state
    (via AdaptationState + a scoped copy of current_skills) based on feedback,
    then reruns the real deterministic engine methods to get updated output.
    """

    VALID_FEEDBACK = {"too_easy", "appropriate", "too_difficult"}

    def __init__(self, engine):
        self.engine = engine  # existing IntelligenceEngine instance

    def apply_feedback(
        self,
        profile,
        skill_name: str,
        feedback: str,
        state: Optional[AdaptationState] = None,
    ) -> Dict[str, Any]:
        if state is None:
            state = AdaptationState()

        feedback_key = (feedback or "").strip().lower().replace(" ", "_")
        if feedback_key not in self.VALID_FEEDBACK:
            return {
                "feedback": feedback,
                "adaptation_message": f"Invalid feedback '{feedback}'. Must be one of: "
                                       f"{sorted(self.VALID_FEEDBACK)}.",
                "updated_recommendation": None,
                "updated_path_health": None,
                "updated_risks": [],
                "root_blockers": [],
                "state": state.to_dict(),
            }

        if not skill_name:
            return {
                "feedback": feedback_key,
                "adaptation_message": "No skill specified for feedback.",
                "updated_recommendation": None,
                "updated_path_health": None,
                "updated_risks": [],
                "root_blockers": [],
                "state": state.to_dict(),
            }

        if feedback_key == "too_easy":
            result = self._handle_too_easy(profile, skill_name, state)
        elif feedback_key == "too_difficult":
            result = self._handle_too_difficult(profile, skill_name, state)
        else:
            result = self._handle_appropriate(profile, skill_name, state)

        state.record(skill_name, feedback_key, result["adapted_action"])
        result["state"] = state.to_dict()
        return result

    # ------------------------------------------------------------------
    # TOO EASY
    # ------------------------------------------------------------------
    def _handle_too_easy(self, profile, skill_name: str, state: AdaptationState) -> Dict[str, Any]:
        if skill_name not in state.mastered_override_skills:
            state.mastered_override_skills.append(skill_name)
        if skill_name in state.deprioritized_skills:
            state.deprioritized_skills.remove(skill_name)
        if skill_name in state.in_progress_skills:
            state.in_progress_skills.remove(skill_name)

        effective_profile = self._effective_profile(profile, state)

        nba = self._safe_call(self.engine.calculate_next_best_action, effective_profile)
        health = self._safe_call(self.engine.calculate_path_health, effective_profile)
        risks = self._safe_call(self.engine.detect_risks, effective_profile) or []

        if nba is None:
            message = (
                f"'{skill_name}' was too easy — nice progress! You're currently "
                f"caught up with no further immediate recommendation available."
            )
        else:
            message = (
                f"'{skill_name}' was too easy, so we're treating it as mastered and "
                f"moving you toward '{nba.get('skill', 'the next skill')}' instead."
            )

        return {
            "feedback": "too_easy",
            "adapted_action": "advanced_step_up",
            "adaptation_message": message,
            "updated_recommendation": nba,
            "updated_path_health": health,
            "updated_risks": risks,
            "root_blockers": [],
        }

    # ------------------------------------------------------------------
    # TOO DIFFICULT
    # ------------------------------------------------------------------
    def _handle_too_difficult(self, profile, skill_name: str, state: AdaptationState) -> Dict[str, Any]:
        if skill_name not in state.deprioritized_skills:
            state.deprioritized_skills.append(skill_name)
        if skill_name in state.in_progress_skills:
            state.in_progress_skills.remove(skill_name)
        if skill_name in state.mastered_override_skills:
            state.mastered_override_skills.remove(skill_name)

        current_skills = list(getattr(profile, "current_skills", []) or [])
        prereq_info = self._safe_call(
            self.engine.check_prerequisites, skill_name, current_skills
        )

        root_blockers: List[str] = []
        if isinstance(prereq_info, dict):
            root_blockers = prereq_info.get("root_blockers", []) or []

        effective_profile = self._effective_profile(profile, state)
        nba = self._safe_call(self.engine.calculate_next_best_action, effective_profile)

        if root_blockers and isinstance(nba, dict) and nba.get("skill") == skill_name:
            blocker_skill = root_blockers[0]
            blocker_prereq = self._safe_call(
                self.engine.check_prerequisites, blocker_skill, current_skills
            )
            nba = {
                "skill": blocker_skill,
                "score": nba.get("score"),
                "score_breakdown": nba.get("score_breakdown", {}),
                "reasons": [f"Root prerequisite blocking progress toward '{skill_name}'"],
                "est_hours": nba.get("est_hours"),
                "difficulty": "foundational",
                "prereq_check": blocker_prereq,
            }

        health = self._safe_call(self.engine.calculate_path_health, effective_profile)
        risks = self._safe_call(self.engine.detect_risks, effective_profile) or []

        if root_blockers:
            message = (
                f"'{skill_name}' was too difficult. Root gap(s) found: "
                f"{', '.join(root_blockers)}. Redirecting your next step there."
            )
        elif prereq_info and isinstance(prereq_info, dict) and not prereq_info.get("satisfied", True):
            missing = prereq_info.get("missing_direct", [])
            message = (
                f"'{skill_name}' was too difficult. Missing prerequisites: "
                f"{', '.join(missing) if missing else 'unspecified'}."
            )
        else:
            message = (
                f"'{skill_name}' was marked too difficult. Recalculating your "
                f"recommendation with this skill deprioritized."
            )

        return {
            "feedback": "too_difficult",
            "adapted_action": "prioritize_root_blockers" if root_blockers else "recompute_recommendation",
            "adaptation_message": message,
            "updated_recommendation": nba,
            "updated_path_health": health,
            "updated_risks": risks,
            "root_blockers": root_blockers,
        }

    # ------------------------------------------------------------------
    # APPROPRIATE
    # ------------------------------------------------------------------
    def _handle_appropriate(self, profile, skill_name: str, state: AdaptationState) -> Dict[str, Any]:
        if skill_name not in state.in_progress_skills:
            state.in_progress_skills.append(skill_name)
        if skill_name in state.deprioritized_skills:
            state.deprioritized_skills.remove(skill_name)

        effective_profile = self._effective_profile(profile, state)
        nba = self._safe_call(self.engine.calculate_next_best_action, effective_profile)

        if isinstance(nba, dict) and nba.get("skill") == skill_name:
            temp_skills = list(getattr(effective_profile, "current_skills", []) or [])
            original = effective_profile.current_skills
            try:
                effective_profile.current_skills = temp_skills + [skill_name]
                nba = self._safe_call(self.engine.calculate_next_best_action, effective_profile)
            finally:
                effective_profile.current_skills = original

        health = self._safe_call(self.engine.calculate_path_health, effective_profile)
        risks = self._safe_call(self.engine.detect_risks, effective_profile) or []

        message = f"Got it — '{skill_name}' is at the right level. Marked as in progress."

        return {
            "feedback": "appropriate",
            "adapted_action": "mark_in_progress",
            "adaptation_message": message,
            "updated_recommendation": nba,
            "updated_path_health": health,
            "updated_risks": risks,
            "root_blockers": [],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _effective_profile(profile, state: AdaptationState):
        base_skills = list(getattr(profile, "current_skills", []) or [])
        for s in state.mastered_override_skills:
            if s not in base_skills:
                base_skills.append(s)
        profile.current_skills = base_skills
        return profile

    @staticmethod
    def _safe_call(fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception:
            return None
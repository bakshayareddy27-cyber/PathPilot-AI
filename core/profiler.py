"""
LearnerProfile: normalized representation of a learner.
No Streamlit or external dependencies.
"""

from dataclasses import dataclass, field
from typing import List


EXPERIENCE_LEVEL_MAP = {
    "beginner": 1,
    "intermediate": 3,
    "advanced": 5,
}


def _normalize_str(value: str) -> str:
    """Trim whitespace and collapse internal spacing for consistent matching."""
    if not value:
        return ""
    return " ".join(str(value).strip().split())


def _normalize_list(values) -> List[str]:
    """
    Normalize a list of skill/interest/course strings:
    - strips whitespace
    - removes empties
    - de-duplicates while preserving order
    """
    if not values:
        return []
    if isinstance(values, str):
        # allow comma-separated string input as a convenience
        values = values.split(",")

    seen = set()
    result = []
    for v in values:
        norm = _normalize_str(v)
        if norm and norm.lower() not in seen:
            seen.add(norm.lower())
            result.append(norm)
    return result


@dataclass
class LearnerProfile:
    name: str = ""
    career_goal: str = ""
    natural_language_goal: str = ""
    experience_level: int = 1  # 1=Beginner, 3=Intermediate, 5=Advanced
    current_skills: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    completed_courses: List[str] = field(default_factory=list)
    weekly_hours: float = 5.0
    timeline_weeks: int = 12
    preferred_learning_style: str = "Mixed"

    def __post_init__(self):
        self.name = _normalize_str(self.name)
        self.career_goal = _normalize_str(self.career_goal)
        self.natural_language_goal = _normalize_str(self.natural_language_goal)
        self.current_skills = _normalize_list(self.current_skills)
        self.interests = _normalize_list(self.interests)
        self.completed_courses = _normalize_list(self.completed_courses)
        self.preferred_learning_style = _normalize_str(self.preferred_learning_style) or "Mixed"

        # experience_level may arrive as a string label ("Beginner") or a raw int/float
        if isinstance(self.experience_level, str):
            key = self.experience_level.strip().lower()
            self.experience_level = EXPERIENCE_LEVEL_MAP.get(key, 1)
        else:
            try:
                self.experience_level = int(self.experience_level)
            except (TypeError, ValueError):
                self.experience_level = 1
            if self.experience_level not in (1, 3, 5):
                # clamp any stray value to the nearest defined level
                self.experience_level = min((1, 3, 5), key=lambda x: abs(x - self.experience_level))

        try:
            self.weekly_hours = max(0.0, float(self.weekly_hours))
        except (TypeError, ValueError):
            self.weekly_hours = 5.0

        try:
            self.timeline_weeks = max(1, int(self.timeline_weeks))
        except (TypeError, ValueError):
            self.timeline_weeks = 12

    @classmethod
    def experience_label(cls, level: int) -> str:
        for label, val in EXPERIENCE_LEVEL_MAP.items():
            if val == level:
                return label.capitalize()
        return "Beginner"

    def has_skill(self, skill_name: str) -> bool:
        """Case-insensitive membership check against current_skills."""
        target = _normalize_str(skill_name).lower()
        return any(s.lower() == target for s in self.current_skills)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "career_goal": self.career_goal,
            "natural_language_goal": self.natural_language_goal,
            "experience_level": self.experience_level,
            "current_skills": self.current_skills,
            "interests": self.interests,
            "completed_courses": self.completed_courses,
            "weekly_hours": self.weekly_hours,
            "timeline_weeks": self.timeline_weeks,
            "preferred_learning_style": self.preferred_learning_style,
        }
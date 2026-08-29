"""
IntelligenceEngine: deterministic core brain of PathPilot AI.
No Groq, no Streamlit, no fake AI logic — pure Python decision logic.
"""

import json
import csv
import os
from typing import List, Dict, Any, Optional, Set


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# NBA scoring weights — named constants so they're visible/tunable, not magic numbers.
W_CAREER_PRIORITY = 3.0
W_CAREER_RELEVANCE = 2.0
W_PREREQ_UNLOCK = 2.5
W_INTEREST = 1.0
W_DIFFICULTY_FIT = 1.5
W_HOURS_FIT = 1.0

# Risk thresholds
TIMELINE_OVERRUN_FACTOR = 1.3
DIFFICULTY_MISMATCH_THRESHOLD = 2
CRITICAL_PRIORITY_THRESHOLD = 4


class IntelligenceEngine:
    def __init__(self, data_dir: str = DATA_DIR):
        self.data_dir = data_dir
        self.career_paths: Dict[str, Any] = {}
        self.skill_graph: Dict[str, Any] = {}
        self.resources: List[Dict[str, Any]] = []
        self._load_data()

    # ------------------------------------------------------------------
    # Data loading
    # ------------------------------------------------------------------
    def _load_data(self):
        self.career_paths = self._load_json("career_paths.json")
        self.skill_graph = self._load_json("skill_graph.json")
        self.resources = self._load_csv("learning_resources.csv")

    def _load_json(self, filename: str) -> dict:
        path = os.path.join(self.data_dir, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[IntelligenceEngine] Warning: could not load {filename}: {e}")
            return {}

    def _load_csv(self, filename: str) -> List[dict]:
        path = os.path.join(self.data_dir, filename)
        rows = []
        try:
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        row["est_hours"] = float(row.get("est_hours", 0) or 0)
                        row["difficulty"] = int(row.get("difficulty", 1) or 1)
                    except (TypeError, ValueError):
                        row["est_hours"] = 0.0
                        row["difficulty"] = 1
                    rows.append(row)
        except FileNotFoundError as e:
            print(f"[IntelligenceEngine] Warning: could not load {filename}: {e}")
        return rows

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def get_career_skills(self, career_goal: str) -> List[dict]:
        """Required skills for a career, or [] if career not found."""
        career = self.career_paths.get(career_goal, {})
        return career.get("required_skills", [])

    def get_skill_info(self, skill_name: str) -> dict:
        """Skill graph entry, or a safe default if the skill is unknown."""
        return self.skill_graph.get(
            skill_name,
            {"depends_on": [], "difficulty": 1, "domain": "general", "tags": []},
        )

    def get_resources_for_skill(self, skill_name: str) -> List[dict]:
        return [r for r in self.resources if r.get("skill") == skill_name]

    # ------------------------------------------------------------------
    # 1. Skill Gap Analysis
    # ------------------------------------------------------------------
    def analyze_skill_gap(self, profile) -> dict:
        career_skills = self.get_career_skills(profile.career_goal)
        possessed = []
        missing = []

        for skill in career_skills:
            name = skill.get("name")
            if not name:
                continue
            if profile.has_skill(name):
                possessed.append(skill)
            else:
                missing.append(skill)

        # prioritized missing = highest career priority first
        prioritized_missing = sorted(missing, key=lambda s: s.get("priority", 0), reverse=True)

        return {
            "possessed_skills": possessed,
            "missing_skills": missing,
            "prioritized_missing_skills": prioritized_missing,
        }

    # ------------------------------------------------------------------
    # 2. Readiness Score
    # ------------------------------------------------------------------
    def calculate_readiness_score(self, profile) -> float:
        career_skills = self.get_career_skills(profile.career_goal)
        if not career_skills:
            return 0.0

        total_priority = sum(s.get("priority", 0) for s in career_skills)
        if total_priority == 0:
            return 0.0

        possessed_priority = sum(
            s.get("priority", 0) for s in career_skills if profile.has_skill(s.get("name", ""))
        )

        return round((possessed_priority / total_priority) * 100, 1)

    # ------------------------------------------------------------------
    # 3. Recursive Prerequisite Validation
    # ------------------------------------------------------------------
    def check_prerequisites(
        self, skill_name: str, current_skills: List[str], _visited: Optional[Set[str]] = None
    ) -> dict:
        """
        Recursively validates whether all prerequisites for skill_name are met.
        Returns:
            satisfied: bool
            missing_direct: prereqs of skill_name itself that are unmet
            root_blockers: deepest unmet skills with no unmet prereqs of their own
                           (the actual skills the learner should start with)
        """
        if _visited is None:
            _visited = set()

        current_lower = {s.lower() for s in current_skills}

        def is_possessed(name: str) -> bool:
            return name.lower() in current_lower

        root_blockers: Set[str] = set()

        def find_roots(name: str, visited: Set[str]):
            """Depth-first search for unmet skills with no unmet dependencies of their own."""
            if name in visited:
                return  # cycle/revisit guard
            visited.add(name)

            if is_possessed(name):
                return

            info = self.get_skill_info(name)
            deps = info.get("depends_on", [])
            unmet_deps = [d for d in deps if not is_possessed(d)]

            if not unmet_deps:
                # This skill itself is unmet and has no unmet prerequisites —
                # it IS a root blocker.
                root_blockers.add(name)
            else:
                for dep in unmet_deps:
                    find_roots(dep, visited)

        direct_info = self.get_skill_info(skill_name)
        direct_deps = direct_info.get("depends_on", [])
        missing_direct = [d for d in direct_deps if not is_possessed(d)]

        if is_possessed(skill_name):
            satisfied = True
        else:
            satisfied = len(missing_direct) == 0

        if not satisfied or missing_direct:
            find_roots(skill_name, set(_visited))

        return {
            "skill": skill_name,
            "satisfied": satisfied,
            "missing_direct": missing_direct,
            "root_blockers": sorted(root_blockers),
        }

    def prereqs_satisfied(self, skill_name: str, current_skills: List[str]) -> bool:
        """Simple boolean convenience wrapper."""
        return self.check_prerequisites(skill_name, current_skills)["satisfied"]

    # ------------------------------------------------------------------
    # 4. Next Best Action Engine
    # ------------------------------------------------------------------
    def _difficulty_compatibility(self, skill_difficulty: int, experience_level: int) -> float:
        """
        1.0 = perfect fit, decreasing as the gap grows.
        experience_level: 1 (beginner) / 3 (intermediate) / 5 (advanced)
        skill_difficulty: 1-5
        """
        gap = abs(skill_difficulty - experience_level)
        if gap <= 1:
            return 1.0
        elif gap == 2:
            return 0.6
        elif gap == 3:
            return 0.3
        else:
            return 0.1

    def _hours_fit(self, est_hours: float, weekly_hours: float) -> float:
        """
        Rough feasibility: can this skill be completed in a reasonable number
        of weeks given the learner's weekly hours? Returns 0.0-1.0.
        """
        if weekly_hours <= 0:
            return 0.0
        weeks_needed = est_hours / weekly_hours
        if weeks_needed <= 4:
            return 1.0
        elif weeks_needed <= 8:
            return 0.7
        elif weeks_needed <= 12:
            return 0.4
        else:
            return 0.2

    def _estimated_hours_for_skill(self, skill_name: str) -> float:
        resources = self.get_resources_for_skill(skill_name)
        courses = [r for r in resources if r.get("type") == "course"]
        pool = courses if courses else resources
        if not pool:
            return 10.0  # sane default if no resource data exists
        return sum(r.get("est_hours", 0) for r in pool) / len(pool)

    def _unlocking_value(self, skill_name: str) -> int:
        """How many other skills in the graph directly depend on this one."""
        count = 0
        for other, info in self.skill_graph.items():
            if skill_name in info.get("depends_on", []):
                count += 1
        return count

    def calculate_next_best_action(self, profile) -> Optional[dict]:
        gap = self.analyze_skill_gap(profile)
        missing = gap["missing_skills"]
        if not missing:
            return None

        max_unlock = max((self._unlocking_value(s.get("name", "")) for s in missing), default=1)
        max_unlock = max(max_unlock, 1)  # avoid div-by-zero

        candidates = []
        for skill in missing:
            name = skill.get("name")
            if not name:
                continue

            prereq_check = self.check_prerequisites(name, profile.current_skills)
            if not prereq_check["satisfied"]:
                # Cannot be logically learned yet — excluded from NBA candidates,
                # but its root blockers still surface via missing_skills/roadmap.
                continue

            info = self.get_skill_info(name)
            career_priority = skill.get("priority", 0)  # 1-5, already career-specific
            skill_tags = set(info.get("tags", [])) | set(skill.get("tags", []))
            interest_match = 1.0 if (skill_tags & set(t.lower() for t in profile.interests)) else 0.0
            # normalize interests to lowercase for comparison
            interests_lower = {i.lower() for i in profile.interests}
            interest_match = 1.0 if any(tag.lower() in interests_lower for tag in skill_tags) else 0.0

            unlock_raw = self._unlocking_value(name)
            unlock_score = unlock_raw / max_unlock

            difficulty = info.get("difficulty", skill.get("difficulty", 1))
            diff_fit = self._difficulty_compatibility(difficulty, profile.experience_level)

            est_hours = self._estimated_hours_for_skill(name)
            hours_fit = self._hours_fit(est_hours, profile.weekly_hours)

            # Career relevance: this skill IS drawn from the selected career's
            # required list, so relevance is baseline 1.0 — this guarantees
            # interest alone can never outrank a skill's fit to the goal,
            # since interest is a smaller separate weighted term, not a
            # multiplier on relevance.
            career_relevance = 1.0

            score = (
                W_CAREER_PRIORITY * (career_priority / 5.0)
                + W_CAREER_RELEVANCE * career_relevance
                + W_PREREQ_UNLOCK * unlock_score
                + W_INTEREST * interest_match
                + W_DIFFICULTY_FIT * diff_fit
                + W_HOURS_FIT * hours_fit
            )

            breakdown = {
                "career_priority": round(W_CAREER_PRIORITY * (career_priority / 5.0), 2),
                "career_relevance": round(W_CAREER_RELEVANCE * career_relevance, 2),
                "prerequisite_unlocking_value": round(W_PREREQ_UNLOCK * unlock_score, 2),
                "interest_alignment": round(W_INTEREST * interest_match, 2),
                "difficulty_compatibility": round(W_DIFFICULTY_FIT * diff_fit, 2),
                "time_feasibility": round(W_HOURS_FIT * hours_fit, 2),
            }

            reasons = []
            if career_priority >= 4:
                reasons.append("High priority for your selected career goal.")
            if unlock_raw > 0:
                reasons.append(f"Unlocks {unlock_raw} further skill(s) once learned.")
            if interest_match:
                reasons.append("Aligns with your stated interests.")
            if diff_fit >= 0.6:
                reasons.append("Matches your current experience level well.")
            if hours_fit >= 0.7:
                reasons.append("Fits comfortably within your weekly available hours.")
            if not reasons:
                reasons.append("Next logical step toward your career goal.")

            candidates.append({
                "skill": name,
                "score": round(score, 2),
                "score_breakdown": breakdown,
                "reasons": reasons,
                "est_hours": round(est_hours, 1),
                "difficulty": difficulty,
            })

        if not candidates:
            return None

        candidates.sort(key=lambda c: c["score"], reverse=True)
        return candidates[0]

    # ------------------------------------------------------------------
    # 5. Learning Risk Detection
    # ------------------------------------------------------------------
    def detect_risks(self, profile) -> List[dict]:
        risks = []
        gap = self.analyze_skill_gap(profile)
        missing = gap["missing_skills"]

        # Risk 1: unmet critical prerequisites
        critical_blockers = set()
        for skill in missing:
            if skill.get("priority", 0) >= CRITICAL_PRIORITY_THRESHOLD:
                check = self.check_prerequisites(skill.get("name", ""), profile.current_skills)
                if not check["satisfied"]:
                    critical_blockers.update(check["root_blockers"])

        if critical_blockers:
            risks.append({
                "type": "unmet_critical_prerequisite",
                "severity": "high",
                "message": (
                    f"Critical prerequisite(s) missing: {', '.join(sorted(critical_blockers))}."
                ),
                "suggested_action": (
                    f"Start with {', '.join(sorted(critical_blockers))} before advancing to "
                    "higher-priority career skills that depend on them."
                ),
            })

        # Risk 2: unrealistic timeline
        total_hours_needed = sum(self._estimated_hours_for_skill(s.get("name", "")) for s in missing)
        if profile.weekly_hours > 0:
            weeks_needed = total_hours_needed / profile.weekly_hours
            if weeks_needed > profile.timeline_weeks * TIMELINE_OVERRUN_FACTOR:
                risks.append({
                    "type": "timeline_unrealistic",
                    "severity": "medium",
                    "message": (
                        f"Estimated {round(weeks_needed)} weeks needed at your current pace, "
                        f"but your target timeline is {profile.timeline_weeks} weeks."
                    ),
                    "suggested_action": "Extend your timeline or increase weekly learning hours.",
                })
        else:
            risks.append({
                "type": "timeline_unrealistic",
                "severity": "high",
                "message": "Weekly learning hours are set to 0, so no progress can be planned.",
                "suggested_action": "Set a realistic weekly hours commitment to generate a roadmap.",
            })

        # Risk 3: difficulty mismatch
        mismatched = []
        for skill in missing:
            name = skill.get("name", "")
            info = self.get_skill_info(name)
            difficulty = info.get("difficulty", 1)
            if (difficulty - profile.experience_level) > DIFFICULTY_MISMATCH_THRESHOLD:
                mismatched.append(name)

        if mismatched:
            risks.append({
                "type": "difficulty_mismatch",
                "severity": "medium",
                "message": (
                    f"These skills are significantly above your current experience level: "
                    f"{', '.join(mismatched)}."
                ),
                "suggested_action": "Build up foundational skills before attempting these directly.",
            })

        return risks

    # ------------------------------------------------------------------
    # 6. Path Health Monitor
    # ------------------------------------------------------------------
    def calculate_path_health(self, profile) -> dict:
        readiness = self.calculate_readiness_score(profile)
        risks = self.detect_risks(profile)

        # Start from readiness (0-100), deduct for each active risk by severity.
        severity_penalty = {"high": 25, "medium": 12, "low": 5}
        score = readiness
        factors = [f"Base readiness: {readiness}%"]

        for risk in risks:
            penalty = severity_penalty.get(risk["severity"], 10)
            score -= penalty
            factors.append(f"-{penalty} pts: {risk['type']} ({risk['severity']})")

        score = max(0.0, min(100.0, round(score, 1)))

        if score >= 70:
            status = "Healthy"
        elif score >= 40:
            status = "At Risk"
        else:
            status = "Critical"

        return {
            "health_score": score,
            "status": status,
            "contributing_factors": factors,
        }

    # ------------------------------------------------------------------
    # 7. Personalized Roadmap Generation
    # ------------------------------------------------------------------
    def generate_roadmap(self, profile) -> List[dict]:
        """
        Prerequisite-aware ordering: skills with satisfied prerequisites and
        higher career priority come first. Uses a simple topological pass
        over the missing-skill set combined with priority tie-breaking.
        """
        gap = self.analyze_skill_gap(profile)
        missing = gap["missing_skills"]
        if not missing:
            return []

        current_skills = set(s.lower() for s in profile.current_skills)
        remaining = {s["name"]: s for s in missing if s.get("name")}
        ordered_names: List[str] = []
        guard = 0
        max_iterations = len(remaining) * len(remaining) + 5  # cycle-safety guard

        while remaining and guard < max_iterations:
            guard += 1
            # eligible = all deps already possessed or already placed earlier in roadmap
            eligible = []
            for name, skill in remaining.items():
                info = self.get_skill_info(name)
                deps = info.get("depends_on", [])
                deps_satisfied = all(
                    d.lower() in current_skills or d in ordered_names for d in deps
                )
                if deps_satisfied:
                    eligible.append(skill)

            if not eligible:
                # Remaining skills have unmet deps outside the missing set itself
                # (e.g. depend on a skill the learner already has under a
                # different case, or an unresolved graph gap) — place by
                # priority anyway rather than dropping them silently.
                eligible = list(remaining.values())

            eligible.sort(key=lambda s: s.get("priority", 0), reverse=True)
            chosen = eligible[0]
            ordered_names.append(chosen["name"])
            del remaining[chosen["name"]]

        roadmap = []
        for name in ordered_names:
            skill = next((s for s in missing if s["name"] == name), {})
            info = self.get_skill_info(name)
            roadmap.append({
                "skill": name,
                "priority": skill.get("priority", 0),
                "difficulty": info.get("difficulty", 1),
                "prerequisites": info.get("depends_on", []),
                "recommended_resources": self.get_resources_for_skill(name),
            })

        return roadmap
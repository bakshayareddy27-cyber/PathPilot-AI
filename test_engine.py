from core.profiler import LearnerProfile
from core.intelligence_engine import IntelligenceEngine

profile = LearnerProfile(
    name="Asha",
    career_goal="Machine Learning Engineer",
    natural_language_goal="I want to become a Machine Learning Engineer",
    experience_level="Beginner",
    current_skills=["Python"],
    interests=["ml", "math"],
    completed_courses=[],
    weekly_hours=6,
    timeline_weeks=10,
    preferred_learning_style="Video",
)

engine = IntelligenceEngine()

readiness = engine.calculate_readiness_score(profile)
nba = engine.calculate_next_best_action(profile)
health = engine.calculate_path_health(profile)
risks = engine.detect_risks(profile)

print("Readiness Score:", readiness)
print("Next Best Action:", nba)
print("Path Health:", health)
print("Risks:", risks)
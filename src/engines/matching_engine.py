from models.job_requirements import JobRequirements
from models.candidate_features import CandidateFeatures
from models.match_result import MatchResult

from semantic.semantic_matcher import SemanticMatcher


class MatchingEngine:

    def __init__(self):

        self.semantic_matcher = SemanticMatcher()

    def calculate_experience_score(
        self,
        candidate_experience,
        min_experience,
        max_experience,
    ):
        """
        Calculates experience score (0-100).
        """

        if min_experience <= candidate_experience <= max_experience:
            return 100

        if candidate_experience < min_experience:

            difference = min_experience - candidate_experience

            return max(0, 100 - difference * 20)

        difference = candidate_experience - max_experience

        return max(50, 100 - difference * 10)

    def calculate_skill_score(
        self,
        required_skills,
        candidate_skills,
    ):

        matched = []
        missing = []

        candidate_lower = {
            skill.lower(): skill
            for skill in candidate_skills
        }

        for required in required_skills:

            required_lower = required.lower()

            # -------------------------
            # Exact Match
            # -------------------------

            if required_lower in candidate_lower:

                matched.append(required)
                continue

            # -------------------------
            # No skills available
            # -------------------------

            if not candidate_skills:

                missing.append(required)
                continue

            # -------------------------
            # Semantic Match
            # -------------------------

            found = False

            for candidate in candidate_skills:

                similarity = self.semantic_matcher.similarity(
                    required,
                    candidate,
                )

                if similarity >= 0.70:

                    matched.append(required)
                    found = True
                    break

            if not found:
                missing.append(required)

        score = (
            len(matched) / len(required_skills)
        ) * 100 if required_skills else 0

        return score, matched, missing

    def match(
        self,
        requirements: JobRequirements,
        candidate_features: CandidateFeatures,
    ):

        result = MatchResult()

        (
            result.skill_score,
            result.matched_skills,
            result.missing_skills,
        ) = self.calculate_skill_score(
            requirements.required_skills,
            candidate_features.skills,
        )

        result.experience_score = self.calculate_experience_score(
            candidate_features.years_of_experience,
            requirements.experience_min,
            requirements.experience_max,
        )

        result.final_score = (
            result.skill_score * 0.70
            + result.experience_score * 0.30
        )

        return result
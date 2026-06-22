from models.job_requirements import JobRequirements
from models.candidate_features import CandidateFeatures
from models.match_result import MatchResult


from models.job_requirements import JobRequirements
from models.candidate_features import CandidateFeatures
from models.match_result import MatchResult


class MatchingEngine:

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

    def match(
        self,
        requirements: JobRequirements,
        candidate_features: CandidateFeatures,
    ):

        result = MatchResult()

        # -------------------------------
        # Skill Matching
        # -------------------------------

        required = {
            skill.lower()
            for skill in requirements.required_skills
        }

        candidate = {
            skill.lower()
            for skill in candidate_features.skills
        }

        matched = required.intersection(candidate)
        missing = required.difference(candidate)

        result.matched_skills = sorted(list(matched))
        result.missing_skills = sorted(list(missing))

        if required:
            result.skill_score = (
                len(matched) / len(required)
            ) * 100

        # -------------------------------
        # Experience Matching
        # -------------------------------

        result.experience_score = self.calculate_experience_score(
            candidate_features.years_of_experience,
            requirements.experience_min,
            requirements.experience_max,
        )

        # -------------------------------
        # Final Score
        # -------------------------------

        result.final_score = (
            result.skill_score * 0.70
            + result.experience_score * 0.30
        )

        return result
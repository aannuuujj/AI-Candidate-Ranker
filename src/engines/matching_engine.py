from models.match_result import MatchResult


class MatchingEngine:

    def match(
        self,
        required_skills,
        candidate_skills,
    ):

        result = MatchResult()

        required = {
            skill.lower()
            for skill in required_skills
        }

        candidate = {
            skill.lower()
            for skill in candidate_skills
        }

        matched = required.intersection(candidate)

        missing = required.difference(candidate)

        result.matched_skills = sorted(list(matched))

        result.missing_skills = sorted(list(missing))

        if required:
            result.skill_score = (
                len(matched) / len(required)
            ) * 100

        result.final_score = result.skill_score

        return result
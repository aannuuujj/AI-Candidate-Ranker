from models.candidate_features import CandidateFeatures


class CandidateFeatureEngine:

    def extract(self, candidate: dict) -> CandidateFeatures:

        features = CandidateFeatures()

        # Candidate ID
        features.candidate_id = candidate.get("candidate_id", "")

        # Profile
        profile = candidate.get("profile", {})

        features.years_of_experience = profile.get(
            "years_of_experience", 0
        )

        features.current_role = profile.get(
            "current_title", ""
        )

        features.location = profile.get(
            "location", ""
        )

        # Skills
        features.skills = [
            skill["name"]
            for skill in candidate.get("skills", [])
        ]

        # Education
        features.education = [
            edu["degree"]
            for edu in candidate.get("education", [])
        ]

        # Certifications
        features.certifications = [
            cert.get("name", "")
            for cert in candidate.get("certifications", [])
        ]

        # Languages
        features.languages = [
            lang["language"]
            for lang in candidate.get("languages", [])
        ]

        # Redrob Signals
        signals = candidate.get("redrob_signals", {})

        features.github_score = signals.get(
            "github_activity_score", 0
        )

        features.recruiter_response_rate = signals.get(
            "recruiter_response_rate", 0
        )

        features.profile_completeness = signals.get(
            "profile_completeness_score", 0
        )

        features.open_to_work = signals.get(
            "open_to_work_flag", False
        )

        return features
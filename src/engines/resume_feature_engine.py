import re

from config.settings import PROJECT_ROOT
from engines.skill_extraction_engine import SkillExtractionEngine
from models.candidate_features import CandidateFeatures


class ResumeFeatureEngine:

    def extract(
        self,
        resume_text: str,
    ) -> CandidateFeatures:

        features = CandidateFeatures()

        # --------------------------------
        # Extract Skills
        # --------------------------------
        skill_engine = SkillExtractionEngine(
            PROJECT_ROOT / "src" / "knowledge" / "skills.json"
        )

        features.skills = skill_engine.extract(
            resume_text
        )

        # --------------------------------
        # Extract Years of Experience
        # --------------------------------
        experience = re.search(
            r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)",
            resume_text,
            re.IGNORECASE,
        )

        if experience:
            features.years_of_experience = float(
                experience.group(1)
            )

        # --------------------------------
        # Extract Email
        # --------------------------------
        emails = re.findall(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text,
        )

        if emails:

            # Prefer email containing "anuj"
            for email in emails:
                if "anuj" in email.lower():
                    features.email = email
                    break
            else:
                features.candidate_id = emails[0]

        # --------------------------------
        # Extract Phone Number
        # --------------------------------
        phone = re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            resume_text,
        )

        if phone:
            features.phone = phone.group()

        return features
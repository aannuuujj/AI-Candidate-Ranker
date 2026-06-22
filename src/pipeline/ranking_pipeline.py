from config.settings import (
    JOB_DESCRIPTION_FILE,
    CANDIDATE_DATASET,
)

from parsers.jd_parser import JobDescriptionParser
from loaders.data_loader import CandidateDataLoader
from engines.candidate_feature_engine import CandidateFeatureEngine
from engines.matching_engine import MatchingEngine


class RankingPipeline:
    """
    Main orchestration pipeline.

    Responsible for:
    - Parsing the Job Description
    - Loading candidates
    - Extracting candidate features
    - Matching candidates with the Job Description
    """

    def run(self):

        print("=" * 70)
        print("AI Candidate Discovery Platform")
        print("=" * 70)

        # --------------------------------------------------
        # Parse Job Description
        # --------------------------------------------------

        parser = JobDescriptionParser(JOB_DESCRIPTION_FILE)
        requirements = parser.parse()

        print("\nJOB REQUIREMENTS")
        print("-" * 70)

        print(f"Job Title        : {requirements.job_title}")
        print(f"Company          : {requirements.company}")
        print(f"Location         : {requirements.location}")
        print(f"Employment Type  : {requirements.employment_type}")
        print(f"Experience Min   : {requirements.experience_min}")
        print(f"Experience Max   : {requirements.experience_max}")
        print(f"Required Skills  : {requirements.required_skills}")

        # --------------------------------------------------
        # Load Candidates
        # --------------------------------------------------

        print("\n" + "=" * 70)
        print("Loading Candidate Features")
        print("=" * 70)

        loader = CandidateDataLoader(CANDIDATE_DATASET)
        feature_engine = CandidateFeatureEngine()
        matching_engine = MatchingEngine()

        count = 0

        for candidate in loader.stream_candidates():

            features = feature_engine.extract(candidate)

            match = matching_engine.match(
                requirements.required_skills,
                features.skills,
            )

            print(f"\nCandidate #{count + 1}")
            print(f"ID              : {features.candidate_id}")
            print(f"Role            : {features.current_role}")
            print(f"Experience      : {features.years_of_experience}")
            print(f"Location        : {features.location}")
            print(f"Skill Score     : {match.skill_score:.2f}%")
            print(f"Matched Skills  : {match.matched_skills}")
            print(f"Missing Skills  : {match.missing_skills}")
            print(f"GitHub Score    : {features.github_score}")
            print(f"Open To Work    : {features.open_to_work}")

            count += 1

            if count == 5:
                break

        print("\nPipeline completed successfully.")
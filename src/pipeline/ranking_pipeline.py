from config.settings import (
    JOB_DESCRIPTION_FILE,
    CANDIDATE_DATASET,
    MAX_CANDIDATES_TO_PROCESS,
    TOP_K_RESULTS,
    TOP_CANDIDATES_FILE,
)

from parsers.jd_parser import JobDescriptionParser
from loaders.data_loader import CandidateDataLoader
from engines.candidate_feature_engine import CandidateFeatureEngine
from engines.matching_engine import MatchingEngine
from engines.ranking_engine import RankingEngine

from models.ranked_candidate import RankedCandidate

from exporters.csv_exporter import CSVExporter


class RankingPipeline:
    """
    Main orchestration pipeline.

    Responsible for:
    - Parsing the Job Description
    - Loading candidates
    - Extracting candidate features
    - Matching candidates
    - Ranking candidates
    - Exporting results
    """

    def run(
        self,
        job_description_file=JOB_DESCRIPTION_FILE,
    ):

        print("=" * 70)
        print("AI Candidate Discovery Platform")
        print("=" * 70)

        # --------------------------------------------------
        # Parse Job Description
        # --------------------------------------------------

        parser = JobDescriptionParser(job_description_file)
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
        ranking_engine = RankingEngine()
        exporter = CSVExporter()

        ranked_candidates = []

        count = 0

        for candidate in loader.stream_candidates():

            features = feature_engine.extract(candidate)

            match = matching_engine.match(
                requirements,
                features,
            )

            ranked_candidate = RankedCandidate(
                candidate=features,
                match=match,
            )

            ranked_candidates.append(ranked_candidate)

            count += 1

            if count >= MAX_CANDIDATES_TO_PROCESS:
                break

        # --------------------------------------------------
        # Rank Candidates
        # --------------------------------------------------

        print("\nRanking Candidates...")

        ranked_candidates = ranking_engine.rank(
            ranked_candidates
        )

        # --------------------------------------------------
        # Export Results
        # --------------------------------------------------

        exporter.export(
            ranked_candidates[:TOP_K_RESULTS],
            TOP_CANDIDATES_FILE,
        )

        print(f"\nResults exported to: {TOP_CANDIDATES_FILE}")

        # --------------------------------------------------
        # Display Top Candidates
        # --------------------------------------------------

        print("\nTOP CANDIDATES")
        print("=" * 70)

        for index, candidate in enumerate(
            ranked_candidates[:TOP_K_RESULTS],
            start=1,
        ):

            print(f"\nRank #{index}")
            print(f"Candidate ID : {candidate.candidate.candidate_id}")
            print(f"Role         : {candidate.candidate.current_role}")
            print(f"Final Score  : {candidate.match.final_score:.2f}%")
            print(f"Skill Score  : {candidate.match.skill_score:.2f}%")
            print(f"Experience   : {candidate.match.experience_score:.2f}%")

        print("\nPipeline completed successfully.")

        return ranked_candidates[:TOP_K_RESULTS]
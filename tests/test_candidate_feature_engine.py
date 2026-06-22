import json

from engines.candidate_feature_engine import CandidateFeatureEngine


def main():

    with open("data/sample_candidates.json", "r") as file:
        candidates = json.load(file)

    candidate = candidates[0]

    engine = CandidateFeatureEngine()

    features = engine.extract(candidate)

    print("=" * 60)
    print("Candidate Features")
    print("=" * 60)

    print(f"Candidate ID        : {features.candidate_id}")
    print(f"Experience         : {features.years_of_experience}")
    print(f"Current Role       : {features.current_role}")
    print(f"Location           : {features.location}")
    print(f"Skills             : {features.skills}")
    print(f"Education          : {features.education}")
    print(f"Languages          : {features.languages}")
    print(f"GitHub Score       : {features.github_score}")
    print(f"Open To Work       : {features.open_to_work}")
    print(f"Profile Score      : {features.profile_completeness}")


if __name__ == "__main__":
    main()
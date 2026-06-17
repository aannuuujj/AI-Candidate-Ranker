from core.data_loader import CandidateDataLoader
from config.settings import CANDIDATES_FILE


def main():

    print("=" * 60)
    print("🚀 AI Candidate Discovery Platform")
    print("=" * 60)

    loader = CandidateDataLoader(CANDIDATES_FILE)

    total = loader.count_candidates()

    print(f"\nTotal Candidates : {total}\n")

    print("First 5 Candidates\n")

    for index, candidate in enumerate(loader.stream_candidates(), start=1):

        print(f"Candidate {index}")
        print(f"ID : {candidate['candidate_id']}")
        print(f"Headline : {candidate['profile']['headline']}")
        print(f"Experience : {candidate['profile']['years_of_experience']} years")
        print("-" * 50)

        if index == 5:
            break


if __name__ == "__main__":
    main()
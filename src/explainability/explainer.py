class Explainer:

    def explain(self, ranked_candidate):

        print("=" * 60)

        print(
            f"Candidate : {ranked_candidate.candidate.candidate_id}"
        )

        print(
            f"Final Score : {ranked_candidate.match.final_score:.2f}%"
        )

        print("\nMatched Skills")

        for skill in ranked_candidate.match.matched_skills:
            print(f"✓ {skill}")

        print("\nMissing Skills")

        for skill in ranked_candidate.match.missing_skills:
            print(f"✗ {skill}")
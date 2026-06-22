class RankingEngine:

    def rank(self, ranked_candidates):

        return sorted(
            ranked_candidates,
            key=lambda candidate: candidate.match.final_score,
            reverse=True,
        )
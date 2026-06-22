import csv


class CSVExporter:

    def export(self, ranked_candidates, output_file):

        with open(output_file, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Rank",
                "Candidate ID",
                "Role",
                "Final Score",
                "Skill Score",
                "Experience Score",
            ])

            for rank, candidate in enumerate(ranked_candidates, start=1):

                writer.writerow([
                    rank,
                    candidate.candidate.candidate_id,
                    candidate.candidate.current_role,
                    round(candidate.match.final_score, 2),
                    round(candidate.match.skill_score, 2),
                    round(candidate.match.experience_score, 2),
                ])
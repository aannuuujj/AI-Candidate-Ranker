class RecommendationEngine:

    def recommend(self, match):

        score = match.final_score

        if score >= 85:
            recommendation = "★★★★★ Strong Match - Interview Immediately"

        elif score >= 70:
            recommendation = "★★★★ Good Match - Shortlist"

        elif score >= 50:
            recommendation = "★★★ Moderate Match - Consider"

        elif score >= 30:
            recommendation = "★★ Weak Match"

        else:
            recommendation = "★ Not Recommended"

        reasons = []

        if match.skill_score >= 80:
            reasons.append("Excellent skill match")

        elif match.skill_score >= 60:
            reasons.append("Good skill match")

        elif match.skill_score >= 40:
            reasons.append("Partial skill match")

        else:
            reasons.append("Limited skill match")

        if match.experience_score >= 80:
            reasons.append("Experience meets requirement")

        elif match.experience_score >= 50:
            reasons.append("Experience is acceptable")

        else:
            reasons.append("Experience below requirement")

        return recommendation, reasons
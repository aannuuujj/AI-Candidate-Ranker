class SkillMatcher:

    def match(
        self,
        required,
        candidate,
    ):

        matched = required.intersection(candidate)

        missing = required.difference(candidate)

        if required:
            score = len(matched) / len(required) * 100
        else:
            score = 0

        return score, matched, missing
import json


class AliasMatcher:

    def __init__(self, alias_file):

        with open(alias_file, "r", encoding="utf-8") as f:
            self.aliases = json.load(f)

    def normalize(self, skills):

        normalized = set()

        for skill in skills:

            skill_lower = skill.lower()

            normalized.add(skill_lower)

            for canonical, aliases in self.aliases.items():

                if skill_lower == canonical.lower():

                    normalized.add(canonical.lower())

                for alias in aliases:

                    if skill_lower == alias.lower():

                        normalized.add(canonical.lower())

        return normalized
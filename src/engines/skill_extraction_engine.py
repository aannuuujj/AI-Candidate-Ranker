from loaders.knowledge_loader import KnowledgeLoader
from preprocessing.text_normalizer import TextNormalizer


class SkillExtractionEngine:
    """
    Extracts technical skills from a Job Description
    using the knowledge base.
    """

    def __init__(self, knowledge_path):
        self.skills = KnowledgeLoader(knowledge_path).load()

    def extract(self, text: str):

        text = TextNormalizer.normalize(text)

        found_skills = []

        for category in self.skills.values():

            for skill in category:

                if skill.lower() in text:
                    found_skills.append(skill)

        return sorted(list(set(found_skills)))
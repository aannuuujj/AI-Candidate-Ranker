from pathlib import Path

from loaders.knowledge_loader import KnowledgeLoader

loader = KnowledgeLoader(Path("src/knowledge/skills.json"))

skills = loader.load()

print(skills)
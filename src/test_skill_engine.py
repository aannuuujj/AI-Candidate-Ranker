from pathlib import Path

from config.settings import JOB_DESCRIPTION_FILE
from engines.skill_extraction_engine import SkillExtractionEngine
from docx import Document


doc = Document(JOB_DESCRIPTION_FILE)

text = "\n".join(
    p.text
    for p in doc.paragraphs
)

engine = SkillExtractionEngine(
    Path("src/knowledge/skills.json")
)

skills = engine.extract(text)

print("\nExtracted Skills\n")

for skill in skills:
    print("-", skill)
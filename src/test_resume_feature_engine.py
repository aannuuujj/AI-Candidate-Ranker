from pathlib import Path

from parsers.resume_parser import ResumeParser
from engines.resume_feature_engine import ResumeFeatureEngine

# Parse resume
parser = ResumeParser(
    Path("uploads/sample_resume.pdf")
)

resume_text = parser.extract_text()

# Extract features
engine = ResumeFeatureEngine()

features = engine.extract(resume_text)

print("=" * 60)
print("Resume Features")
print("=" * 60)

print("Email:", features.candidate_id)
print("Phone:", features.location)
print("Experience:", features.years_of_experience)

print()

print("=" * 60)
print("Skills")
print("=" * 60)

for skill in features.skills:
    print("-", skill)
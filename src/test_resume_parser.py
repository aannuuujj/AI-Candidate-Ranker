from pathlib import Path

from parsers.resume_parser import ResumeParser

resume = ResumeParser(
    Path("uploads/sample_resume.pdf")
)

text = resume.extract_text()

print("=" * 80)
print(text[:3000])
print("=" * 80)
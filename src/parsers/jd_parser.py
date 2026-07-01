import re
from pathlib import Path

from docx import Document
from pypdf import PdfReader
from PIL import Image
import pytesseract

from config.settings import PROJECT_ROOT
from engines.skill_extraction_engine import SkillExtractionEngine
from models.job_requirements import JobRequirements


class JobDescriptionParser:

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def parse(self) -> JobRequirements:

        extension = self.file_path.suffix.lower()

        # -----------------------------
        # Read DOCX
        # -----------------------------
        if extension == ".docx":

            document = Document(self.file_path)

            text = "\n".join(
                p.text.strip()
                for p in document.paragraphs
                if p.text.strip()
            )

        # -----------------------------
        # Read PDF
        # -----------------------------
        elif extension == ".pdf":

            reader = PdfReader(self.file_path)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        # -----------------------------
        # Read Image (OCR)
        # -----------------------------
        elif extension in [".jpg", ".jpeg", ".png"]:

            image = Image.open(self.file_path)

            text = pytesseract.image_to_string(image)

        # -----------------------------
        # Unsupported File
        # -----------------------------
        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        requirements = JobRequirements()

        # --------------------------------------------------
        # Job Title
        # --------------------------------------------------
        title = re.search(r"Job Description:\s*(.+)", text)

        if title:
            requirements.job_title = title.group(1).strip()

        # --------------------------------------------------
        # Company
        # --------------------------------------------------
        company = re.search(r"Company:\s*(.+)", text)

        if company:
            requirements.company = company.group(1).strip()

        # --------------------------------------------------
        # Location
        # --------------------------------------------------
        location = re.search(r"Location:\s*(.+)", text)

        if location:
            requirements.location = location.group(1).strip()

        # --------------------------------------------------
        # Employment Type
        # --------------------------------------------------
        employment = re.search(r"Employment Type:\s*(.+)", text)

        if employment:
            requirements.employment_type = employment.group(1).strip()

        # --------------------------------------------------
        # Experience
        # --------------------------------------------------
        experience = re.search(
            r"Experience Required:\s*(\d+)\s*[-–]\s*(\d+)",
            text
        )

        if experience:
            requirements.experience_min = int(experience.group(1))
            requirements.experience_max = int(experience.group(2))

        # --------------------------------------------------
        # Extract Required Skills
        # --------------------------------------------------
        skill_engine = SkillExtractionEngine(
            PROJECT_ROOT / "src" / "knowledge" / "skills.json"
        )

        requirements.required_skills = skill_engine.extract(text)

        return requirements
from pathlib import Path

from docx import Document
from pypdf import PdfReader
from PIL import Image
import pytesseract


class ResumeParser:

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def extract_text(self):

        extension = self.file_path.suffix.lower()

        # DOCX
        if extension == ".docx":

            document = Document(self.file_path)

            return "\n".join(
                p.text.strip()
                for p in document.paragraphs
                if p.text.strip()
            )

        # PDF
        elif extension == ".pdf":

            reader = PdfReader(self.file_path)

            text = ""

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:

                    text += page_text + "\n"

            return text

        # Images
        elif extension in [".jpg", ".jpeg", ".png"]:

            image = Image.open(self.file_path)

            return pytesseract.image_to_string(image)

        else:

            raise ValueError(
                f"Unsupported file: {extension}"
            )
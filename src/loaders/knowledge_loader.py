import json
from pathlib import Path


class KnowledgeLoader:
    """Loads JSON knowledge bases."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)
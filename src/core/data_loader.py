from pathlib import Path
import json


class CandidateDataLoader:
    """
    Streams candidate records from a JSONL file.

    Instead of loading all candidates into RAM,
    this class yields one candidate at a time.
    """

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def stream_candidates(self):
        """Yield one candidate at a time."""

        with open(self.file_path, "r", encoding="utf-8") as file:

            for line in file:

                line = line.strip()

                if line:
                    yield json.loads(line)

    def count_candidates(self):
        """Return total number of candidates."""

        count = 0

        with open(self.file_path, "r", encoding="utf-8") as file:

            for line in file:

                if line.strip():
                    count += 1

        return count
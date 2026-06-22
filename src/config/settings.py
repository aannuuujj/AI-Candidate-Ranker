from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Data Folder
DATA_DIR = PROJECT_ROOT / "data"

# Dataset Files
CANDIDATES_FILE = DATA_DIR / "candidates.jsonl"
SAMPLE_CANDIDATES_FILE = DATA_DIR / "sample_candidates.json"
JOB_DESCRIPTION_FILE = DATA_DIR / "job_description.docx"

# Output Folder
OUTPUT_DIR = PROJECT_ROOT / "outputs"

CANDIDATE_DATASET = DATA_DIR / "candidates.jsonl"
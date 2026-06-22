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

# Processing Configuration
MAX_CANDIDATES_TO_PROCESS = 100
TOP_K_RESULTS = 10

TOP_CANDIDATES_FILE = OUTPUT_DIR / "top_candidates.csv"

KNOWLEDGE_DIR = PROJECT_ROOT / "src" / "knowledge"

SKILL_ALIASES_FILE = KNOWLEDGE_DIR / "skill_aliases.json"
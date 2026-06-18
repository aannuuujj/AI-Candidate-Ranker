from config.settings import JOB_DESCRIPTION_FILE
from core.jd_parser import JobDescriptionParser


def main():

    print("=" * 70)
    print("AI Candidate Discovery Platform")
    print("=" * 70)

    parser = JobDescriptionParser(JOB_DESCRIPTION_FILE)

    requirements = parser.parse()

    print("\nJob Title        :", requirements.job_title)
    print("Company         :", requirements.company)
    print("Location        :", requirements.location)
    print("Employment Type :", requirements.employment_type)
    print("Experience Min  :", requirements.experience_min)
    print("Experience Max  :", requirements.experience_max)


if __name__ == "__main__":
    main()
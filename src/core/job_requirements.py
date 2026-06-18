from dataclasses import dataclass, field


@dataclass
class JobRequirements:
    """
    Stores structured information extracted
    from a Job Description.
    """

    job_title: str = ""
    company: str = ""
    location: str = ""
    employment_type: str = ""

    experience_min: int = 0
    experience_max: int = 0

    required_skills: list = field(default_factory=list)
    preferred_skills: list = field(default_factory=list)
    soft_skills: list = field(default_factory=list)
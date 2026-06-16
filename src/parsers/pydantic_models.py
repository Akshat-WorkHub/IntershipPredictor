from pydantic import BaseModel, Field

class Education(BaseModel):

    degree: str = Field(
        description="Degree, qualification, or educational program pursued by the candidate."
    )

    institution: str = Field(
        description="Name of the school, college, or university."
    )

    academic_score: float | None = Field(
        default=None,
        description="Numerical academic score extracted from the qualification.",
        examples=[9.18, 3.75, 85.4]
    )

    score_type: str | None = Field(
        default=None,
        description="Type of academic score.",
        examples=["CGPA", "GPA", "Percentage"]
    )

    year: str = Field(
        description="Year, tenure, or duration associated with the qualification."
    )


class Project(BaseModel):

    name: str = Field(
        description="Title or name of the project completed by the candidate."
    )

    description: str = Field(
        description="Short summary of the project including objectives, technologies used, and key outcomes."
    )


class Internship(BaseModel):

    company: str = Field(
        description="Name of the company, organization, or institution where the internship was completed."
    )

    role: str = Field(
        description="Role, designation, or internship position held by the candidate. Examples: AI Intern, Data Science Intern, Software Development Intern."
    )

class ResumeData(BaseModel):

    skills: list[str] = Field(
        description="Technical and non technical skills"
    )

    education: list[Education] = Field(
        description="Educational qualifications"
    )

    projects: list[Project] = Field(
        description="Projects completed by candidate"
    )

    internships: list[Internship] = Field(
        description="Internships completed by candidate"
    )

    certifications: list[str] = Field(
        description="Certifications earned by candidate"
    )

    hackathons: list[str] = Field(
        description="Hackathons participated in"
    )

    extracurriculars: list[str] = Field(
        description="Extracurricular activities, clubs, sports, volunteering"
    )

    achievements: list[str] = Field(
        description="Awards, achievements, recognitions"
    )
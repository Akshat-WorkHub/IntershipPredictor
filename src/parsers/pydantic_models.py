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

    resume_score: int = Field(
        description="Overall resume quality score from 1 to 10."
    )

    consistency_score: int = Field(
        description="Consistency between academics, skills, projects, internships and certifications. Score between 1 and 10."
    )

class JobDescriptionData(BaseModel):

    required_skills: list[str] = Field(
        description="Technical and non technical skills required for the job"
    )

    preferred_skills: list[str] = Field(
        description="Nice to have skills"
    )

    responsibilities: list[str] = Field(
        description="Main job responsibilities"
    )

    qualifications: list[str] = Field(
        description="Educational and experience requirements"
    )

    certifications: list[str] = Field(
        description="Required or preferred certifications"
    )

class WeekPlan(BaseModel):

    week: int = Field(
        description="Week number"
    )

    focus: str = Field(
        description="Primary learning objective"
    )

    topics: list[str] = Field(
        description="Topics to learn during this week"
    )

    resources: list[str] = Field(
        description="Learning resources"
    )

    project: str = Field(
        description="Mini project for practice"
    )

class RoadmapRequest(BaseModel):

    missing_skills: list[str] = Field(
        description="Missing skills sent by frontend for roadmap generation"
    )

class LearningRoadmap(BaseModel):

    missing_skills: list[str] = Field(
        description="Skills identified as missing from resume"
    )

    roadmap: list[WeekPlan] = Field(
        description="Four week learning roadmap"
    )

class InterviewRequest(BaseModel):

    interview_mode: str = Field(
        description="""
        Interview mode selected by the user.

        Possible values:
        - Technical Round
        - HR Round
        - Project Discussion
        - Full Mock Interview
        """,
        examples=["Full Mock Interview"]
    )

    number_of_questions: int = Field(
        description="Number of interview questions to generate."
    )

    resume_data: ResumeData = Field(
        description="Parsed resume information."
    )

    jd_data: JobDescriptionData = Field(
        description="Parsed job description information."
    )

    missing_skills: list[str] = Field(
        description="Skills missing from the candidate profile."
    )

class InterviewQuestion(BaseModel):

    question: str = Field(
        description="Interview question generated for the selected category."
    )

    difficulty: str = Field(
        description="Difficulty level of the question.",
        examples=[
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    category: str = Field(
        description="Question category.",
        examples=[
            "Technical",
            "Project Based",
            "HR",
            "Scenario Based"
        ]
    )

class InterviewQuestionSet(BaseModel):

    questions: list[InterviewQuestion] = Field(
        description="List of interview questions generated for the interview session."
    )

class InterviewAnswerRequest(BaseModel):

    question: str = Field(
        description="Interview question answered by the user."
    )

    answer: str = Field(
        description="User's response to the interview question."
    )

    category: str = Field(
        description="Interview category of the question."
    )


class QuestionEvaluation(BaseModel):

    question: str = Field(
        description="Interview question."
    )

    candidate_answer: str = Field(
        description="Candidate's submitted answer."
    )

    category: str = Field(
        description="Question category."
    )

    score: float = Field(
        description="Score awarded for this answer on a scale of 0 to 10.",
        ge=0,
        le=10,
        examples=[8.5]
    )

    status: str = Field(
        description="Evaluation status of the answer.",
        examples=[
            "Excellent",
            "Good",
            "Average",
            "Poor",
            "Not Attempted"
        ]
    )

    feedback: str = Field(
        description="Constructive feedback explaining the score."
    )

    strengths: list[str] = Field(
        description="Strong points identified in the answer."
    )

    improvements: list[str] = Field(
        description="Areas where the answer can be improved."
    )

    ideal_answer: str = Field(
        description="An ideal response demonstrating a high-quality answer."
    )

class InterviewEvaluationRequest(BaseModel):

    answers: dict = Field(
        description="All interview questions and candidate answers collected during the interview session."
    )

class InterviewEvaluation(BaseModel):

    overall_score: float = Field(
        description="Overall interview score on a scale of 0 to 10.",
        ge=0,
        le=10,
        examples=[7.8]
    )

    attempted_questions: int = Field(
        description="Number of questions attempted by the candidate."
    )

    unattempted_questions: int = Field(
        description="Number of questions marked as 'I don't know'."
    )

    strengths: list[str] = Field(
        description="Overall strengths observed across the interview."
    )

    improvements: list[str] = Field(
        description="Overall improvement areas identified across the interview."
    )

    questions_to_revise: list[str] = Field(
        description="Topics or questions the candidate should revisit."
    )

    question_analysis: list[QuestionEvaluation] = Field(
        description="Detailed evaluation of each interview question."
    )

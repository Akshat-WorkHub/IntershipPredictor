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

    resume_score: float = Field(
        description="Overall resume quality score from 1 to 10."
    )

    consistency_score: float = Field(
        description="Consistency score from 1 to 10."
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

class CandidatePrediction(BaseModel):

    prediction: int = Field(
        description="""
        Binary shortlisting prediction.

        Possible values:
        - 1 : Candidate is likely to be shortlisted.
        - 0 : Candidate is unlikely to be shortlisted.
        """
    )

    probability: float = Field(
        description="""
        Estimated probability (0 to 100) that the candidate
        will be shortlisted for the interview.
        """,
        ge=0,
        le=100,
        examples=[82.5]
    )

    decision: str = Field(
        description="""
        Overall screening decision.

        Possible values:
        - Highly Likely
        - Likely
        - Borderline
        - Unlikely
        """,
        examples=["Likely"]
    )

    reasoning: str = Field(
        description="""
        Concise explanation of the screening decision,
        summarizing how the candidate's resume,
        skills, projects, internships, academic profile,
        and Job Description compatibility influenced
        the final prediction.
        """
    )

    strengths: list[str] = Field(
        description="""
        Major strengths that positively influenced
        the candidate's screening outcome.
        """
    )

    weaknesses: list[str] = Field(
        description="""
        Key weaknesses, missing skills, or concerns
        that reduced the candidate's chances of
        being shortlisted.
        """
    )

    recommendations: list[str] = Field(
        description="""
        Actionable recommendations that would
        improve the candidate's probability of
        getting shortlisted for similar roles.
        """
    )

class SkillMatchPair(BaseModel):

    resume_skill: str = Field(
        description="Skill present in resume."
    )

    jd_skill: str = Field(
        description="Matching job description skill."
    )

class SkillGapResult(BaseModel):

    matched_skills: list[str] = Field(
        description="JD skills matched by the resume."
    )

    missing_skills: list[str] = Field(
        description="JD skills missing from the resume."
    )

    matched_pairs: list[SkillMatchPair] = Field(
        description="Semantic mapping between resume and JD skills."
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

class InterviewPreparationQuestion(BaseModel):

    category: str = Field(
        description="Category of interview question."
    )

    difficulty: str = Field(
        description="Difficulty level of the question."
    )

    question: str = Field(
        description="Interview question."
    )

    interviewer_intent: str = Field(
        description="""
        Explain why the interviewer is asking this question,
        what skills or knowledge are being evaluated,
        and what they expect from a strong candidate.
        """
    )

    candidate_answer: str = Field(
        description="""
        A complete interview-ready answer that a strong
        candidate should give.
        """
    )

    key_points: list[str] = Field(
        description="Important points that should be covered."
    )

    common_mistakes: list[str] = Field(
        description="Common mistakes candidates make."
    )


class InterviewPreparationResponse(BaseModel):

    questions: list[InterviewPreparationQuestion] = Field(
        description="List of generated interview preparation questions."
    )

class InterviewRequest(BaseModel):

    interview_mode: str = Field(
        description="""
        Interview mode selected by the user.

        Possible values:
        - Technical Round
        - HR Round
        - Project Discussion
        - Scenario Based
        - Mixed Mock Interview
        """
    )

    difficulty: str = Field(
        description="""
        Difficulty level selected by the user.

        Possible values:
        - Easy
        - Medium
        - Hard
        - Mixed
        """
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


class InterviewPreparationPDFRequest(BaseModel):

    interview_mode: str = Field(
        description="Interview mode selected by the user."
    )

    difficulty: str = Field(
        description="Difficulty level selected by the user."
    )

    questions: list[InterviewPreparationQuestion] = Field(
        description="Generated interview preparation questions."
    )
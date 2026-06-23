from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate

prompt = PromptTemplate(
    template="""
You are an expert resume parser.

Extract the following information from the resume:

- Skills
- Education
- Projects
- Internships
- Certifications
- Hackathons
- Extracurricular Activities
- Achievements

For each education entry, extract:

- Degree
- Institution
- Academic score
- Score type
- Year or duration

For Resume Score:

- Evaluate the overall quality of the resume.
- Consider skills, projects, internships, certifications, achievements, and resume completeness.
- Return a score between 1 and 10.
- 1 = Very weak profile.
- 10 = Exceptional profile.

- Consistency Score

Evaluate consistency between:

- Academic performance
- Skills claimed
- Projects completed
- Internships
- Certifications

Examples:

High Consistency (8-10):
- Strong CGPA
- Relevant projects matching skills
- Certifications aligned with career path
- Internship aligned with projects/skills

Medium Consistency (5-7):
- Some alignment between skills and projects
- Limited practical evidence

Low Consistency (1-4):
- Many skills claimed but little evidence
- No projects/internships supporting claims
- Certifications unrelated to profile

Return a score between 1 and 10.

If a field is not present, return an empty list.

Resume:

{resume_text}
""",
    input_variables=["resume_text"]
)

jd_prompt = PromptTemplate(
    template="""
You are an expert Job Description Analyzer.

Analyze the following Job Description and extract:

- Required Skills
- Preferred Skills
- Responsibilities
- Qualifications
- Certifications

Return only information that is explicitly mentioned or strongly implied.

Job Description:

{job_description_text}
""",
    input_variables=["job_description_text"]
)


roadmap_prompt = PromptTemplate(
    template="""
You are a career mentor.

Generate a personalized 4-week learning roadmap.

Missing Skills:
{skills_text}

Requirements:

1. Week-wise plan
2. Daily learning goals
3. Resources to study
4. Small project suggestions
5. Beginner friendly

Return markdown format.
""",
    input_variables=["skills_text"]
)

interview_question_prompt = PromptTemplate(
    template="""
You are an experienced interviewer.

Generate exactly {number_of_questions} interview questions.

Interview Mode:
{interview_mode}

Candidate Resume:
{resume_data}

Job Description:
{jd_data}

Missing Skills:
{missing_skills}

Instructions:

- Follow the Interview Mode Rules while generating questions.
- Personalize questions using the candidate's projects, internships, certifications, skills, and achievements whenever possible.
- Consider job description requirements while generating questions.
- Consider missing skills when creating Technical and Scenario Based questions.
- Avoid generic internet questions whenever possible.
- Questions should be relevant for placement and internship interviews.
- Difficulty should be Easy, Medium, or Hard.
- Generate exactly {number_of_questions} questions.

Interview Mode Rules:

1. Technical Round:
- Focus on technical skills, tools, frameworks, programming concepts, and technologies.

2. HR Round:
- Focus on communication, teamwork, leadership, strengths, weaknesses, goals, and behavioral questions.

3. Project Discussion:
- Focus on projects, internships, implementation decisions, challenges, and outcomes.

4. Full Mock Interview
   - Generate a mix of:
     * Technical - 40%
     * Project Based - 30%
     * HR - 20%
     * Scenario Based - 10%

   - Ensure every generated question contains its correct category.
   - Try to distribute questions as per allocated percentage across categories.

Return output matching the InterviewQuestionSet schema.
""",
    input_variables=[
        "interview_mode",
        "number_of_questions",
        "resume_data",
        "jd_data",
        "missing_skills"
    ]
)

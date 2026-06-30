from langchain_core.prompts import PromptTemplate

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

Additional Extraction Rules

For every project, extract whenever available:

- Project Name
- Technologies Used
- Short Description

For every internship, extract whenever available:

- Company
- Role
- Technologies Used
- Duration

Do not infer information that is not explicitly mentioned in the resume.

Return empty lists when information is unavailable.

""",
    input_variables=["resume_text"]
)

jd_prompt = PromptTemplate(
    template="""
You are an expert Job Description Analyzer.

Analyze the following Job Description and extract the required information.

Job Description:
{job_description_text}

Instructions:

1. Required Skills
- Return ONLY individual skill names.
- Never return descriptive sentences.
- Split combined skills into separate entries.
- Remove introductory phrases such as:
  - Experience with
  - Knowledge of
  - Strong understanding of
  - Ability to
  - Familiarity with
  - Proficiency in

Examples:

Input:
Strong understanding of deep learning frameworks such as TensorFlow or PyTorch

Output:
- TensorFlow
- PyTorch

Input:
Experience with cloud platforms like AWS, Azure, or Google Cloud

Output:
- AWS
- Azure
- Google Cloud

Input:
Proficiency in Large Language Models (LLMs)

Output:
- Large Language Models (LLMs)

Input:
Familiarity with Natural Language Processing techniques

Output:
- Natural Language Processing (NLP)

2. Preferred Skills
- Return only individual skill names.

3. Responsibilities
- Return concise responsibility statements.

4. Qualifications
- Return educational qualifications, experience requirements, or eligibility criteria.

5. Certifications
- Return only certification names.

Return output matching the JobDescription schema.
""",
    input_variables=["job_description_text"]
)

vision_prompt = PromptTemplate(
    template="""
You are an expert document transcription assistant.

Your task is to accurately transcribe every visible piece of text from the provided document.

Requirements:

- Extract all visible text without omitting any content.
- Preserve the original reading order.
- Preserve headings and section hierarchy.
- Preserve bullet points and numbered lists.
- Preserve tables as closely as possible using plain text.
- Do not summarize, interpret, or rewrite the content.
- Do not correct spelling or grammar.
- Do not add information that is not present in the document.
- Return only the extracted plain text.
- Do not use Markdown formatting.
- Do not wrap the response inside code blocks.

The document may be a scanned PDF, an image-based PDF, or a photograph of a document.

Transcribe the document exactly as it appears.
"""
)

prediction_prompt = PromptTemplate(
    template="""
You are a Senior Technical Recruiter with over 15 years of experience hiring candidates for Software Engineering, Data Science, Artificial Intelligence, Machine Learning, and related technology roles.

Your task is to evaluate the candidate's overall employability and estimate the likelihood that the candidate's resume will be shortlisted for an interview during the initial resume screening process.

Candidate Resume:
{resume_data}

Candidate Profile:
{candidate_profile}

====================================================
Evaluation Criteria
====================================================

Evaluate the candidate using the following factors.

1. Resume Quality (30%)

Evaluate:

• Resume quality
• Resume consistency
• Technical skills
• Overall completeness
• Clarity of achievements

----------------------------------------------------

2. Projects & Internship Experience (25%)

Evaluate:

• Technical complexity
• Real-world relevance
• Technologies used
• Practical impact
• Internship quality
• Problem-solving ability

Reward candidates who have completed technically challenging and industry-relevant projects.

----------------------------------------------------

3. Technical Competence (20%)

Evaluate:

• Programming languages
• Frameworks
• AI / ML knowledge
• Databases
• Backend development
• System design (if applicable)
• Development tools

----------------------------------------------------

4. Academic Profile (10%)

Evaluate:

• Degree
• Academic performance
• Certifications
• Academic consistency

----------------------------------------------------

5. Candidate Profile (10%)

Evaluate:

• Communication
• Coding ability
• Aptitude
• Soft skills

----------------------------------------------------

6. Additional Factors (5%)

Consider:

• College tier
• Placement training
• Academic backlogs
• Hackathons
• Achievements
• Extracurricular activities

====================================================
Probability Guidelines
====================================================

90–100

Outstanding candidate.

Excellent overall profile with a very high likelihood of receiving interview calls.

80–89

Strong candidate.

Likely to receive interview calls for most suitable roles.

70–79

Good candidate.

Competitive profile with good interview opportunities.

60–69

Average candidate.

Reasonable interview chances but improvements are recommended.

40–59

Below average profile.

Limited interview opportunities due to noticeable weaknesses.

0–39

Weak profile.

Unlikely to receive interview calls without significant improvement.

====================================================
Decision Mapping
====================================================

Highly Likely

Probability >= 90

Likely

Probability 70–89

Borderline

Probability 50–69

Unlikely

Probability < 50

====================================================
Prediction Rules
====================================================

prediction = 1 if probability >= 60

prediction = 0 if probability < 60

====================================================
Instructions
====================================================

- Think exactly like an experienced recruiter conducting the first stage of resume screening.
- Evaluate the candidate's overall profile instead of focusing on a single strength or weakness.
- Balance technical skills, projects, internships, academics, and candidate profile before assigning the probability.
- Consider the resume from the perspective of internship, campus placement, and entry-level recruitment.
- Do not compare the candidate with senior professionals having several years of experience.
- Do not invent skills, experience, projects, or achievements.
- Base the evaluation only on the supplied information.
- Assign a realistic probability that reflects the candidate's chances of receiving interview calls based on the overall strength of the profile.

====================================================
Return
====================================================

Return ONLY a valid CandidatePrediction object containing:

1. prediction
2. probability
3. decision
4. reasoning
5. strengths
6. weaknesses
7. recommendations

Do not include markdown, explanations, or any text outside the required schema.
""",
    input_variables=[
        "resume_data",
        "candidate_profile"
    ]
)


skill_matcher_prompt = PromptTemplate(
    template="""
You are an ATS Skill Matching Engine.

Compare the candidate's resume skills against the job description skills.

Resume Skills:

{resume_skills}

Job Description Skills:

{jd_skills}

Instructions:

- Match skills semantically.
- Do not require exact text matching.
- Consider equivalent technologies.

Examples:

LangChain
→ Large Language Models (LLMs)

RAG Architecture
→ Large Language Models (LLMs)

PyTorch
→ Deep Learning

FastAPI
→ REST APIs

TensorFlow
→ Deep Learning

Do not guess.

Only match when there is a strong semantic relationship.

Return:

- matched_skills
- missing_skills
- matched_pairs

Return output matching the SkillGapResult schema.
""",
    input_variables=[
        "resume_skills",
        "jd_skills"
    ]
)


roadmap_prompt = PromptTemplate(
    template="""
You are an experienced career mentor and technical learning advisor.

Your task is to generate a personalized 4-week learning roadmap based on the candidate's missing skills.

Missing Skills:
{skills_text}

Instructions:

- Create a practical and beginner-friendly roadmap.
- Focus on helping the candidate become interview-ready.
- Arrange topics from foundational concepts to advanced applications.
- If multiple skills are provided, group related skills together whenever possible.
- Allocate an appropriate workload each week.
- Ensure each week builds upon the previous one.

For EACH week include:

1. Week Title
2. Learning Objectives
3. Daily Learning Plan (Day 1 to Day 7)
4. Estimated Daily Study Time
5. Recommended Resources
   - Documentation
   - YouTube
   - Courses
   - Articles
6. Hands-on Practice Tasks
7. Mini Project (if applicable)
8. Weekly Revision Goals
9. Expected Learning Outcome

General Guidelines:

- Recommend only high-quality learning resources.
- Prefer official documentation whenever available.
- Suggest practical coding exercises.
- Include interview preparation activities.
- Encourage revision and implementation rather than only theory.
- Keep the roadmap realistic for students and internship aspirants.

Return the roadmap in well-structured Markdown format.
""",
    input_variables=["skills_text"]
)

interview_preparation_prompt = PromptTemplate(
    template="""
You are an experienced interviewer responsible for creating personalized interview preparation material.

Generate EXACTLY {number_of_questions} interview questions.

Interview Mode:
{interview_mode}

Difficulty:
{difficulty}

Candidate Resume:
{resume_data}

Job Description:
{jd_data}

Missing Skills:
{missing_skills}

Instructions:

1. Generate EXACTLY {number_of_questions} questions.
2. Do NOT generate fewer or more than {number_of_questions} questions.
3. Every question must be personalized using the candidate's profile.
4. Use the candidate's:
   - Skills
   - Projects
   - Internships
   - Certifications
   - Education
   - Experience (if available)
5. Use the Job Description to determine the expected technologies and responsibilities.
6. Use the Missing Skills list to create realistic knowledge-gap questions whenever appropriate.
7. Avoid generic textbook or internet questions unless absolutely necessary.
8. Questions should resemble real placement or internship interview questions.
9. Questions should progressively evaluate the candidate's knowledge and practical understanding.
10. Do not repeat similar questions.

Interview Mode Guidelines:

If Interview Mode is "Technical Round":

- Generate ONLY technical interview questions.
- Prioritize the candidate's technical skills, programming languages, frameworks, databases, AI/ML technologies, APIs, tools, and computer science subjects mentioned in the resume.
- Generate questions around the candidate's projects, internships, certifications, and practical experience whenever applicable.
- Include questions related to technologies or skills required in the Job Description.
- If important skills are missing compared to the Job Description, generate questions to assess those missing areas as well.
- Avoid generic textbook questions unless they are directly relevant to the candidate's profile.

If Interview Mode is "HR Round":

- Generate ONLY HR and behavioural interview questions.
- Personalize questions using the candidate's education, internships, projects, achievements, extracurricular activities, leadership experiences, and career objectives from the resume.
- Include behavioural questions relevant to the responsibilities described in the Job Description.
- Avoid generic HR questions unless they naturally fit the candidate's profile.

If Interview Mode is "Project Discussion":

- Generate ONLY project discussion questions.
- Focus primarily on the projects listed in the candidate's resume.
- Ask about architecture, implementation details, design decisions, technology choices, challenges faced, debugging approaches, optimizations, scalability, deployment, testing, security, and future improvements.
- If the candidate has multiple projects, distribute questions across the most relevant projects according to the Job Description.
- Do NOT generate hypothetical project questions unless the resume lacks sufficient project information.

If Interview Mode is "Scenario Based":

- Generate ONLY realistic scenario-based interview questions.
- Base scenarios on the candidate's technical skills, projects, internship experience, and technologies mentioned in the resume.
- Incorporate technologies and responsibilities mentioned in the Job Description.
- When appropriate, create scenarios around skills that are missing from the candidate profile to evaluate adaptability and problem-solving ability.
- Avoid unrelated or generic workplace scenarios.

If Interview Mode is "Mixed Mock Interview":
Generate a balanced interview consisting approximately of:
- 40% Technical questions
- 30% Project Discussion questions
- 20% HR questions
- 10% Scenario Based questions

For EACH generated question provide:

For every question generate:

1. Category
2. Difficulty
3. Question
4. Interviewer's Intent
5. Candidate Answer
6. Key Points
7. Common Mistakes

Interviewer's Intent:

- Explain why the interviewer asks this question.
- Describe what knowledge, skills, or qualities are being evaluated.
- Mention what distinguishes an excellent answer from an average one.
- Do NOT provide the answer itself.

Candidate Answer:

- Write a complete interview-ready answer.
- Answer as if you are the candidate speaking during the interview.
- Use a professional and conversational tone.
- Include practical examples whenever appropriate.
- Do NOT write phrases like:
  - "The candidate should..."
  - "The interviewee should explain..."
  - "A good answer would..."
- Instead, directly answer the question.
- The answer should generally be between 150 and 300 words depending on the complexity.

The response MUST strictly follow the InterviewPreparationResponse schema.

Return ONLY the structured response.
""",
    input_variables=[
        "interview_mode",
        "difficulty",
        "number_of_questions",
        "resume_data",
        "jd_data",
        "missing_skills"
    ]
)

interview_question_prompt = PromptTemplate(
    template="""
You are an experienced technical interviewer.

Generate EXACTLY {number_of_questions} interview questions.

Interview Mode:
{interview_mode}

Candidate Resume:
{resume_data}

Job Description:
{jd_data}

Missing Skills:
{missing_skills}

Instructions:

1. Generate EXACTLY {number_of_questions} questions.
2. Never generate fewer or more questions.
3. Personalize every question using the candidate's profile.
4. Prioritize information in this order:
   - Candidate Resume
   - Job Description
   - Missing Skills
5. Do NOT invent projects, internships, certifications, achievements, or experience.
6. If resume information is limited, generate questions from the Job Description.
7. Use Missing Skills only for assessing knowledge gaps.
8. Avoid generic interview questions unless absolutely necessary.
9. Questions should resemble real placement or internship interviews.
10. Avoid duplicate or highly similar questions.
11. Assign an appropriate difficulty level (Easy, Medium, or Hard).
12. Every question must contain the correct category.

Interview Mode Guidelines

Technical Round

- Generate ONLY technical questions.
- Prioritize technologies, programming languages, frameworks, databases, APIs, AI/ML concepts, system design (when appropriate), operating systems, networking, and computer science subjects appearing in the resume.
- Generate project-related technical questions whenever applicable.
- Include JD technologies whenever relevant.

HR Round

- Generate ONLY behavioural and HR questions.
- Personalize questions using internships, projects, achievements, leadership experiences, teamwork, extracurricular activities, and career goals.
- Avoid generic HR questions whenever possible.

Project Discussion

- Generate ONLY project discussion questions.
- Focus on projects listed in the resume.
- Ask about architecture, implementation, debugging, design choices, scalability, optimization, deployment, testing, security, and future improvements.
- If multiple projects exist, distribute questions across the most relevant ones.

Scenario Based

- Generate ONLY realistic workplace scenarios.
- Base scenarios on technologies, projects, internships, responsibilities, and missing skills.
- Prefer practical engineering situations over theoretical cases.

Mixed Mock Interview

Distribute questions approximately as follows:

Technical → 40%
Project Discussion → 30%
HR → 20%
Scenario Based → 10%

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

evaluation_prompt = PromptTemplate(
    template="""
You are an experienced technical interviewer and hiring manager.

Evaluate the candidate's complete interview performance objectively.

Candidate Answers:
{answers}

Evaluation Instructions

For EVERY question:

1. Assign a score between 0 and 10.
2. Assign one status:
   - Excellent
   - Good
   - Average
   - Poor
   - Not Attempted
3. Evaluate:
   - Technical correctness
   - Completeness
   - Clarity of explanation
   - Communication quality
   - Practical understanding
4. Provide constructive feedback explaining the score.
5. List major strengths.
6. List specific areas for improvement.
7. Generate an interview-quality ideal answer.

Ideal Answer Guidelines

- Write the answer as if an excellent candidate is responding during a real interview.
- Use a professional and conversational tone.
- Include practical reasoning and examples whenever appropriate.
- Avoid writing instructions such as:
  - "The candidate should..."
  - "The interviewee should..."
  - "A good answer would..."
- Instead, directly answer the interview question.
- Keep answers concise but technically complete.

Special Rule

If the submitted answer is empty or marked as "I don't know":

- Score = 0
- Status = "Not Attempted"
- Mention that the candidate skipped the question.
- Generate the complete ideal answer.

Overall Evaluation

After evaluating all questions generate:

- overall_score
- attempted_questions
- unattempted_questions
- overall strengths
- overall improvement areas
- topics/questions to revise before the next interview

Scoring Guidelines

9–10:
Outstanding answer demonstrating deep understanding, practical knowledge, and excellent communication.

7–8:
Strong answer with only minor gaps.

5–6:
Basic understanding but missing important concepts or depth.

3–4:
Limited understanding with multiple inaccuracies.

0–2:
Incorrect, incomplete, or not attempted.

Return ONLY the structured response matching the InterviewEvaluation schema.
""",
    input_variables=["answers"]
)
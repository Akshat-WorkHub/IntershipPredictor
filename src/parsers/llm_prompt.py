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

If a field is not present, return an empty list.

Resume:

{resume_text}
""",
    input_variables=["resume_text"]
)
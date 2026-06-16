from langchain_groq import ChatGroq
from src.parsers.llm_prompt import prompt
from src.parsers.loader import ResumeLoader
from src.parsers.pydantic_models import (ResumeData)

from dotenv import load_dotenv
load_dotenv()


class LLMResumeParser:
    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        self.structured_llm = (
            self.llm.with_structured_output(ResumeData)
        )

        self.chain = prompt | self.structured_llm

    def parse(self, filepath):
        resume_object = ResumeLoader()
        resume_text = resume_object.generate(filepath)

        response = self.chain.invoke({
            "resume_text": resume_text
        })

        return response.model_dump()
    
class FeatureBuilder:
    def build(self, resume_profile):

        return {
            "projects_count":
                len(resume_profile["projects"]),

            "internships_done":
                len(resume_profile["internships"]),

            "certifications_count":
                len(resume_profile["certifications"]),

            "hackathons_participated":
                len(resume_profile["hackathons"]),

            "extracurricular":
                1 if resume_profile["extracurriculars"] else 0
        }




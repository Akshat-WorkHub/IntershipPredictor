from langchain_groq import ChatGroq
from src.parsers.llm_prompt import prompt, jd_prompt, roadmap_prompt
from src.parsers.loader import ResumeLoader, JobDescriptionLoader
from src.parsers.pydantic_models import ResumeData, JobDescriptionData, LearningRoadmap

from dotenv import load_dotenv
load_dotenv()

class BaseLLMService:

    schema = None
    prompt_template = None

    def __init__(self):

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        self.structured_llm = (
            self.llm.with_structured_output(
                self.schema
            )
        )

        self.chain = self.prompt_template | self.structured_llm 

    def invoke_chain(self, payload):

        response = self.chain.invoke(payload)
        return response.model_dump()



class LLMResumeParser(BaseLLMService):

    schema = ResumeData
    prompt_template = prompt

    def parse(self, filepath):
        resume_object = ResumeLoader()
        resume_text = resume_object.generate(filepath)

        return self.invoke_chain({
            "resume_text": resume_text
        })
    
class LLMJDParser(BaseLLMService):

    schema = JobDescriptionData
    prompt_template = jd_prompt

    def parse(self, filepath):
        jd_object = JobDescriptionLoader()
        jd_text = jd_object.get_job_description_text(filepath)

        return self.invoke_chain({
            "job_description_text": jd_text
        })
    




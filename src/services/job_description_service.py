from src.services.llm_skill_matcher import LLMSkillMatcher
from src.parsers.llm import BaseLLMService
from src.parsers.pydantic_models import JobDescriptionData
from src.parsers.loader import JobDescriptionLoader
from src.parsers.llm_prompt import jd_prompt
import os
import tempfile

class JobDescriptionService(BaseLLMService):

    schema = JobDescriptionData
    prompt_template = jd_prompt

    def __init__(self):
        super().__init__()

    def parse(self, uploaded_file):
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )
        filepath = temp_file.name

        try:
            with temp_file as f:
                f.write(uploaded_file)

            jd_object = JobDescriptionLoader()
            jd_text = jd_object.get_job_description_text(filepath)

        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

        return self.invoke_chain({
            "job_description_text": jd_text
        })

    def compare_skills(self, resume_data: dict, jd_data: dict):
        
        matcher = LLMSkillMatcher()

        return matcher.compare(
            resume_data["skills"],
            jd_data["required_skills"]
        )
    
    

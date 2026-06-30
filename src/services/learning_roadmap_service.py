from src.parsers.llm import BaseLLMService
from src.parsers.llm_prompt import roadmap_prompt
from src.parsers.pydantic_models import LearningRoadmap

class LearningRoadmapService(BaseLLMService):

    schema = LearningRoadmap
    prompt_template = roadmap_prompt

    def generate_roadmap(self, missing_skills):
        
        return self.invoke_chain({
                "skills_text": missing_skills
        })
from src.parsers.llm import BaseLLMService
from src.parsers.llm_prompt import skill_matcher_prompt
from src.parsers.pydantic_models import SkillGapResult


class LLMSkillMatcher(BaseLLMService):

    schema = SkillGapResult
    prompt_template = skill_matcher_prompt
    model = "openai/gpt-oss-120b"

    def compare(self, resume_skills: list[str], jd_skills: list[str]):

        result = self.invoke_chain(
            {
                "resume_skills": resume_skills,
                "jd_skills": jd_skills
            }
        )

        result["match_percentage"] = round(
            (len(result["matched_skills"]) / len(jd_skills) ) * 100, 
            2 
        ) if jd_skills else 0

        return result
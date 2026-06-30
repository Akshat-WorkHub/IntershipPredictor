from src.parsers.llm import BaseLLMService
from src.parsers.llm_prompt import interview_preparation_prompt
from src.parsers.pydantic_models import InterviewPreparationResponse

class InterviewPreparationService(BaseLLMService):

    schema = InterviewPreparationResponse
    prompt_template = interview_preparation_prompt

    def generate(
        self,
        interview_mode: str,
        difficulty: str,
        number_of_questions: int,
        resume_data: dict,
        jd_data: dict,
        missing_skills: list
    ):

        return self.invoke_chain(
            {
                "interview_mode": interview_mode,
                "difficulty": difficulty,
                "number_of_questions": number_of_questions,
                "resume_data": resume_data,
                "jd_data": jd_data,
                "missing_skills": missing_skills
            }
        )
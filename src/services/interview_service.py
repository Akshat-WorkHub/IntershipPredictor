from src.parsers.llm_parser import BaseLLMService
from src.parsers.pydantic_models import InterviewQuestionSet
from src.parsers.llm_prompt import interview_question_prompt

class InterviewService(BaseLLMService):

    schema = InterviewQuestionSet
    prompt_template = interview_question_prompt

    def generate_questions(
        self,
        interview_mode,
        number_of_questions,
        resume_data,
        jd_data,
        missing_skills
    ):
        return self.invoke_chain(
            {
                "interview_mode": interview_mode,
                "number_of_questions": number_of_questions,
                "resume_data": resume_data,
                "jd_data": jd_data,
                "missing_skills": missing_skills
            }
        )
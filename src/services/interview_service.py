from src.parsers.llm import BaseLLMService
from src.parsers.pydantic_models import InterviewQuestionSet, InterviewEvaluation
from src.parsers.llm_prompt import interview_question_prompt, evaluation_prompt

class InterviewService(BaseLLMService):

    schema = InterviewQuestionSet
    prompt_template = interview_question_prompt
    model = "openai/gpt-oss-120b"

    def generate_questions(
        self,
        interview_mode,
        difficulty,
        number_of_questions,
        resume_data,
        jd_data,
        missing_skills
    ):
        return self.invoke_chain(
            {
                "interview_mode": interview_mode,
                "number_of_questions": number_of_questions,
                "difficulty": difficulty,
                "resume_data": resume_data,
                "jd_data": jd_data,
                "missing_skills": missing_skills
            }
        )
    
class InterviewEvaluationService(BaseLLMService):

    schema = InterviewEvaluation
    prompt_template = evaluation_prompt
    model = "openai/gpt-oss-120b"
    
    def evaluate_interview(self, answers):
        
        return self.invoke_chain({
                "answers": answers
            })